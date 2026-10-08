#!/usr/bin/env python3
"""Track L [data]: the cycle Gamma(c) of an in-shape state (the unique cycle of the AB link chain, sigma-type) and its
disc D(c) = vertices of T separated from h by Gamma.  Along maximal pi-runs in R with >= 2 in-shape states, prints
|Gamma|, |D|, |Z|, Z subset D, and the relation of D(c_i) and D(c_{i+2}).
usage: tl_gamma.py GRAPHFILE NOTABLE.jsonl MINLEN [prefix]"""
import sys, json
from collections import Counter
from tl_lib import HoleData, read_graphs


def gamma_disc(hd, i):
    r = hd.info[i]; col = hd.col[i]; al, mu, A, B = r['roles']; x = r['x']; Hh = hd.Hh
    L = Hh.comp(col, x[3], (A, B))
    deg = {v: sum(1 for w in Hh.adj[v] if w in L) for v in L}
    core = set(L); stack = [v for v in L if deg[v] <= 1]
    while stack:
        v = stack.pop()
        if v not in core: continue
        core.discard(v)
        for w in Hh.adj[v]:
            if w in core:
                deg[w] -= 1
                if deg[w] == 1: stack.append(w)
    G = core
    # outside = component of h in T - G
    seen = {hd.h}; st = [hd.h]
    while st:
        u = st.pop()
        for w in hd.rot[u]:
            if w not in seen and w not in G: seen.add(w); st.append(w)
    D = frozenset(v for v in Hh.V if v not in seen and v not in G)
    Lam = Hh.comp(col, x[2], (al, mu))
    Z = frozenset(v for v in Hh.V if col[v] in (al, mu) and v not in Lam)
    return frozenset(G), D, Z


def main():
    gf, notable, minlen = sys.argv[1], sys.argv[2], int(sys.argv[3])
    pref = sys.argv[4] if len(sys.argv) > 4 else ''
    want = {}
    for l in open(notable):
        d = json.loads(l)
        if d['Rrun'] >= minlen and d['name'].startswith(pref): want.setdefault(d['name'], []).append(d['hole'])
    T = Counter()
    for name, rot in read_graphs(gf):
        if name not in want: continue
        for h in want[name]:
            hd = HoleData(rot, h)
            inR = lambda i: i is not None and hd.info[i]['kind'] == 'DL' and hd.info[i]['N'] <= 9
            pre = {hd.info[i]['pi']: i for i in range(hd.S) if hd.info[i]['kind'] == 'DL' and hd.info[i]['pi'] is not None}
            for i in range(hd.S):
                if not inR(i) or inR(pre.get(i)): continue
                run = [i]; y = hd.info[i]['pi']
                while inR(y) and y != i: run.append(y); y = hd.info[y]['pi']
                if len(run) < minlen: continue
                ins = [s for s in run if hd.inshape(s)]
                out = []
                prevD = None
                for s in ins:
                    G, D, Z = gamma_disc(hd, s)
                    T['inshape'] += 1; T['Z_in_D'] += Z <= D
                    rel = ''
                    if prevD is not None:
                        rel = 'eq' if D == prevD else ('in' if D < prevD else ('out' if prevD < D else ('disj' if not (D & prevD) else 'cross')))
                        T[('rel', rel)] += 1
                    out.append('G%d/D%d/Z%d%s' % (len(G), len(D), len(Z), (':' + rel) if rel else ''))
                    prevD = D
                print(name, 'h%d' % h, 'run', len(run), ' '.join(out))
    print('SUMMARY', dict(sorted(T.items(), key=str)))


if __name__ == '__main__':
    main()
