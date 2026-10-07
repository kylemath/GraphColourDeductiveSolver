#!/usr/bin/env python3
"""[Track E] For every edge e0 of T - v: edge-cube = swaps of chains of the two colours absent from e0.  Per labelled class with
locked states: is R1 u cube(e0) bipartite, and is every R1 edge itself a cube(e0) edge (then bipartiteness is automatic)?"""
import sys, json
from collections import Counter
from phase_lib import *
from c2c4 import PUF, GENTRI
C = Counter()
for n in map(int, sys.argv[1:]):
    for line in open(GENTRI % n):
        rot = gentri_rotation(line)
        for h in range(len(rot)):
            if len(rot[h]) != 5: continue
            L = LSpace(rot, h); S = L.S; NN = 24 * S
            R1 = []
            for k in range(S):
                lk = L.locks(k); r = lk[0] if lk[0] is not None else lk[1]; R1.append(r)
            full = PUF(NN)
            for k in range(S):
                for gi, g in enumerate(PERMS):
                    for pq in PAIRS:
                        for K in L.comps[k][pq]:
                            k2, g2 = L.move(k, g, pq, K); full.union(k * 24 + gi, k2 * 24 + PIDX[g2])
            croot = [full.f(x) for x in range(NN)]
            lockedcls = {croot[k * 24 + gi] for k in range(S) if R1[k] is not None for gi in range(24)}
            for (x0, y0) in L.E:
                pu = PUF(NN); inside = Counter(); tot = Counter()
                for k in range(S):
                    s = L.sp.states[k]; cube = tuple(sorted(set(range(4)) - {s[x0], s[y0]}))
                    for gi, g in enumerate(PERMS):
                        node = k * 24 + gi
                        for K in L.comps[k][cube]:
                            k2, g2 = L.move(k, g, cube, K); pu.union(node, k2 * 24 + PIDX[g2])
                        if R1[k] is not None:
                            k2, g2 = L.move(k, g, *R1[k]); pu.union(node, k2 * 24 + PIDX[g2])
                            tot[croot[node]] += 1; inside[croot[node]] += R1[k][0] == cube
                bad = {croot[x] for x in range(NN) if pu.f(x) in pu.badroots()}
                for c in lockedcls:
                    C['class-edge pairs'] += 1
                    if c not in bad:
                        C['bipartite'] += 1
                        C['bipartite & all R1 edges are cube edges'] += inside[c] == tot[c]
                        C['bipartite & some R1 edge outside cube'] += inside[c] < tot[c]
                        nl = (x0 in L.li) + (y0 in L.li); C['bip by #link ends of e0: %d' % nl] += 1
                        comps = len({pu.f(x) for x in range(NN) if croot[x] == c}); csz = sum(1 for x in range(NN) if croot[x] == c)
                        C['bip: sum of class sizes'] += csz; C['bip: sum of #components of R1+cube graph in class'] += comps
                        unl = [x for x in range(NN) if croot[x] == c and not L.sp.filled(x // 24)]
                        C['bip: unfilled states w/o R1 (uncovered)'] += sum(1 for x in unl if R1[x // 24] is None)
                        C['bip: unfilled states'] += len(unl)
                    else:
                        nl = (x0 in L.li) + (y0 in L.li); C['nonbip by #link ends of e0: %d' % nl] += 1
print(json.dumps(dict(C)))
