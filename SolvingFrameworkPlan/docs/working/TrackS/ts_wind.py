#!/usr/bin/env python3
"""Track S: Heawood signs and vertex windings along pi-cycles / pi-runs (orientable surfaces).
eps_t(f) = +1 if the Tait colours (role names 1,2,3) of the primal edges ab, bc, ca of the face f = (a,b,c) (taken in the
rotation-system orientation) are a cyclic rotation of (1,2,3), else -1.  eps_{t+1}(f) is the direction in which the
colour-2 edge (M_t) moves around f between t and t+1.  W(f) = sum_t eps_t(f) over a closed orbit is divisible by 3.
usage: ts_wind.py GRAPHFILE name:hole ..."""
import sys
from collections import Counter
from ts_lib import load_graphs, HoleData, Geo
from ts_qcyc import cycles


def tcol(roles, col, a, b):
    al, mu, A, B = roles; z = {al: 0, mu: 1, A: 2, B: 3}
    return z[col[a]] ^ z[col[b]]


def eps(hd, geo, i):
    r = hd.info[i]; col = hd.col[i]; out = {}
    for f, tri in enumerate(geo.faces):
        if hd.h in tri: continue
        a, b, c = tri
        w = (tcol(r['roles'], col, a, b), tcol(r['roles'], col, b, c), tcol(r['roles'], col, c, a))
        out[f] = 1 if w in ((1, 2, 3), (2, 3, 1), (3, 1, 2)) else -1
    return out


if __name__ == '__main__':
    G = load_graphs(sys.argv[1], {s.rsplit(':', 1)[0] for s in sys.argv[2:]})
    for spec in sys.argv[2:]:
        nm, h = spec.rsplit(':', 1); h = int(h); hd = HoleData(G[nm], h); geo = Geo(G[nm], h)
        for c in cycles(hd):
            E = [eps(hd, geo, q) for q in c]
            S = [sum(e.values()) for e in E]
            W = {f: sum(e[f] for e in E) for f in E[0]}
            print(nm, h, 'L', len(c), 'N', [hd.info[q]['N'] for q in c])
            print('   S_t =', S, ' S mod 3:', sorted(set(s % 3 for s in S)))
            print('   W(f) distribution', sorted(Counter(W.values()).items()), 'sum W', sum(W.values()))
