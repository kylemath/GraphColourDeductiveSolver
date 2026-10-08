#!/usr/bin/env python3
"""Track S: spoke pattern along H_t at rigid states of R-runs / Phi-steps.
At rigid t, walk the Hamiltonian cycle H_t from v along e2 (frame labels); record the positions p0, p1, p3 of the far ends
of the colour-1 spokes e0, e1, e3, and the order pattern of (p0, p1, p3).  Reports the transition table of patterns
under Phi (u -> pi^2 u).  usage: ts_spokes.py GRAPHFILE name:hole ... | GRAPHFILE stride off maxg"""
import sys
from collections import Counter
from ts_lib import load_graphs, HoleData, phi_steps
from tl_lib import TaitState


def pattern(hd, i):
    St = TaitState(hd, i); T = St.T; E = St.E
    path, last = T.trail(St.H, T.lab['e2'])
    pos = {}; x = 0
    for k, kk in enumerate(path):
        x = T.other(kk, x); pos[x] = k
    m = len(path) - 1
    far = {}
    for t in (0, 1, 3):
        kk = T.lab['e%d' % t]; far[t] = pos[T.other(kk, 0)]
    order = ''.join(str(t) for t in sorted(far, key=lambda t: far[t]))
    return order, far, m


a = sys.argv
if ':' in a[2]:
    G = load_graphs(a[1], {s.rsplit(':', 1)[0] for s in a[2:]}); specs = [(s.rsplit(':', 1)[0], int(s.rsplit(':', 1)[1])) for s in a[2:]]
else:
    s, off, mx = int(a[2]), int(a[3]), int(a[4]); G = {}; specs = []
    for ln, l in enumerate(open(a[1])):
        if ln % s != off: continue
        p = l.split(); rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
        G[p[0]] = rot; specs += [(p[0], h) for h in range(len(rot)) if len(rot[h]) == 5]
        if len(G) >= mx: break
trans = Counter(); single = Counter()
for nm, h in specs:
    hd = HoleData(G[nm], h)
    for (u, c, u2) in phi_steps(hd):
        o1, f1, m = pattern(hd, u); o2, f2, _ = pattern(hd, u2)
        trans[(o1, o2)] += 1; single[o1] += 1
print('patterns at rigid u:', dict(single))
print('Phi transitions:', dict(trans))
