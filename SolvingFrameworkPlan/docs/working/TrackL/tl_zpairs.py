#!/usr/bin/env python3
"""Track L [data]: relation between the extra chains Z(c) and Z(c'') of in-shape states c and c'' = pi^2(c)
(pi(c) rigid, c'' in-shape), as vertex sets of T - h: equal / nested / disjoint / crossing; also whether Z(c'') lies in
K(c) u K(pi c) (the two swap sets), and the Tait-side data.  Sphere holes from a notable list (or all holes).
usage: tl_zpairs.py GRAPHFILE STRIDE OFFSET MAXGRAPHS"""
import sys
from collections import Counter
from tl_lib import HoleData, read_graphs


def zset(hd, i):
    r = hd.info[i]; col = hd.col[i]; al, mu, A, B = r['roles']; x = r['x']
    L = hd.Hh.comp(col, x[2], (al, mu))
    return frozenset(v for v in hd.Hh.V if col[v] in (al, mu) and v not in L)


def main():
    gf, stride, off, maxg = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    T = Counter()
    for name, rot in read_graphs(gf, stride, off, maxg):
        for h in [v for v in range(len(rot)) if len(rot[v]) == 5]:
            hd = HoleData(rot, h)
            for i in range(hd.S):
                if not hd.inshape(i): continue
                u = hd.info[i]['pi']; c2 = hd.info[u]['pi']
                T['inshape'] += 1
                if c2 is None or not hd.inshape(c2): continue
                Z0 = zset(hd, i); Z2 = zset(hd, c2)
                r0 = hd.info[i]; col0 = hd.col[i]; al, mu, A, B = r0['roles']; x = r0['x']
                K0 = hd.Hh.comp(col0, x[2], (al, A))
                ru = hd.info[u]; colu = hd.col[u]; a1, m1, A1, B1 = ru['roles']; xu = ru['x']
                K1 = hd.Hh.comp(colu, xu[2], (a1, A1))
                rel = 'equal' if Z0 == Z2 else ('Z2<Z0' if Z2 < Z0 else ('Z0<Z2' if Z0 < Z2 else ('disjoint' if not (Z0 & Z2) else 'cross')))
                T[('pair', rel)] += 1
                T[('Z0 meets K0', bool(Z0 & K0)), ('Z0 meets K1', bool(Z0 & K1))] += 1
                T[('Z2 sub K0uK1', Z2 <= (K0 | K1))] += 1
    print(gf, dict(sorted(T.items(), key=str)), flush=True)


if __name__ == '__main__':
    main()
