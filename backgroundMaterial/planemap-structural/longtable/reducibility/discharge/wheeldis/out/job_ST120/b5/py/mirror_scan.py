#!/usr/bin/env python3
"""Control for rotcheck: classify every checkEmb-valid placement of every K768 configuration into one window link word.
usage: python3 -I mirror_scan.py LINKWORD"""
import os, sys, collections
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import export_cert as E, rotcheck as RC
R = E.R; R.U_HOST_ALWAYS = True
link = [int(c) for c in sys.argv[1]]; d = len(link)
W = R.Window(d, link, None); host, adj, var = R.window_hostgraph(W)
tot = collections.Counter(); byc = collections.defaultdict(collections.Counter); bad = []
for l in open(os.path.join(os.path.dirname(H), 'st127', 'k767_kc.txt')):
    nm = l.split()[0]
    try: name, r, m, cyc = RC.krot(l)
    except Exception as ex: bad.append((nm, str(ex))); continue
    p = E.prep_kc(l); deg = p['deg']; E_ = p['E']; order = p['order']
    if m > len(host): continue
    phi = {}; used = set()
    def rec(k):
        if k == m:
            letters = {h: (W.link[h[1]] if h[0] == 'w' else d if h == 'u' else deg[x]) for x, h in phi.items()}
            common, per = RC.chirality(W, dict(phi), cyc, letters)
            kind = 'rot' if common else ('mirror-only' if all(per.values()) else 'no-chirality')
            tot[kind] += 1; byc[nm][kind] += 1; return
        x = order[k]; nb = [y for y in order[:k] if y in E_[x]]
        for t in (adj[phi[nb[0]]] if nb else host.keys()):
            if t in used or deg[x] not in host[t]: continue
            if any((y in E_[x]) != (phi[y] in adj[t]) for y in order[:k]): continue
            phi[x] = t; used.add(t); rec(k + 1); del phi[x]; used.discard(t)
    rec(0)
print(sys.argv[1], dict(tot), 'configs with placements', len(byc), 'krot failures', len(bad), bad[:3])
print('configs with only non-rotation placements:', sorted(n for n, c in byc.items() if not c['rot'])[:40])
