#!/usr/bin/env python3
"""ST-120 B5 partial-mirror demonstration (task 1): link word 5567757 (d = 7), configurations 184.3686406
(rsst213), nl0078_r11, fw_f7c75a21e2 (kc lines from st127/k767_kc.txt). Every checkEmb-valid placement into the
window host graph (u host with letter d; apex/private hosts at the letter the placement needs) is classified as
rotation-respecting (one common chirality) or mirror-only. Output: mirror/demo_5567757.txt"""
import os, sys, collections
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import export_cert as E, rotcheck as RC
R = E.R; R.U_HOST_ALWAYS = True
d = 7; link = [5, 5, 6, 7, 7, 5, 7]
W = R.Window(d, link, None)
host, adj, var = R.window_hostgraph(W)
kc = {l.split()[0]: l for l in open(os.path.join(E.os.path.dirname(H), 'st127', 'k767_kc.txt'))}
want = ['rsst213_184o3686406', 'nl0078_r11', 'fw_f7c75a21e2']
out = ['# link 5567757 (d=7); host codes: u 0, w_i 1+i, s_i 8+i, p_i.(k+1) 15+3i+k', '']
for nm in want:
    name, r, m, cyc = RC.krot(kc[nm]); p = E.prep_kc(kc[nm])
    deg = p['deg']; E_ = p['E']; order = p['order']
    phi = {}; used = set(); res = collections.Counter(); ex = {}
    def rec(k):
        if k == m:
            letters = {h: (W.link[h[1]] if h[0] == 'w' else d if h == 'u' else deg[x]) for x, h in phi.items()}
            common, per = RC.chirality(W, dict(phi), cyc, letters)
            kind = 'rot+' if 1 in common else ('rot-' if -1 in common else
                   ('MIRROR-ONLY' if all(per.values()) else 'no-chirality'))
            res[kind] += 1
            if kind not in ex: ex[kind] = (dict(phi), {x: sorted(v) for x, v in per.items()})
            return
        x = order[k]; nb = [y for y in order[:k] if y in E_[x]]
        for t in sorted(adj[phi[nb[0]]] if nb else host.keys(), key=repr):
            if t in used or deg[x] not in host[t]: continue
            if any((y in E_[x]) != (phi[y] in adj[t]) for y in order[:k]): continue
            phi[x] = t; used.add(t); rec(k + 1); del phi[x]; used.discard(t)
    rec(0)
    out.append('%s: checkEmb-valid placements %d; %s' % (nm, sum(res.values()), dict(res)))
    for kind, (ph, per) in sorted(ex.items()):
        codes = [E.vcode(d, ph[x]) for x in range(m)]
        need = ['%s=%d' % (var[ph[x]], deg[x]) for x in range(m) if ph[x] in var]
        out.append('  %s example: e = %s  (letters needed: %s)  per-vertex chiralities %s' %
                   (kind, ','.join(map(str, codes)), ' '.join(need) or '-', per))
    out.append('')
txt = '\n'.join(out); print(txt)
open(os.path.join(os.path.dirname(H), 'mirror', 'demo_5567757.txt'), 'w').write(txt + '\n')
