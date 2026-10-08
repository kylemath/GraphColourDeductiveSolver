#!/usr/bin/env python3
"""Track I: how often does K = K_{alpha A}(x_{j+2}) have holes (pi's Tait effect = X plus extra closed {1,3}-cycles)?
Tallies the chain-parity law  N(pi c) - N(c) == [pi c DL] (mod 2)  separately for hole-free and holed K.
usage: ti_holes.py GRAPHFILE STRIDE MAXGRAPHS"""
import sys, os
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'TrackH'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from th_engine import Hole
from ti_lib import Tait, primal_to_tait
from ti_chains import nchains
gf, stride, maxg = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
st = Counter(); k = 0
for ln, l in enumerate(open(gf)):
    if ln % stride: continue
    p = l.split()
    if len(p) < 3: continue
    rot = [list(map(int, r.split(','))) for r in p[2].split(';')]; k += 1
    if k > maxg: break
    for h in [v for v in range(len(rot)) if len(rot[v]) == 5]:
        Hh = Hole(rot, h); S = len(Hh.states); info = []; Nc = []; cols = []
        for i in range(S):
            r, col = Hh.analyse_state(i); info.append(r); cols.append(col); Nc.append(nchains(Hh, col))
        for i in range(S):
            r = info[i]
            if r['kind'] != 'DL': continue
            col = cols[i]; al, mu, A, B = r['roles']; X5 = rot[h]; x = [X5[(r['j'] + t) % 5] for t in range(5)]
            K = Hh.comp(col, x[2], (al, A))
            dK = sum(1 for u in K for w in Hh.adj[u] if w not in K)
            E = primal_to_tait(rot, h, col, r['roles'], r['j']); T = Tait(E)
            F13 = {q for q, e in enumerate(E) if e[2] in (1, 3)}
            Xp, _ = T.trail(F13, T.lab['e1'])
            # dK counts boundary edges of T-h (link edges x1x2, x3x4 are duals of e1, e3)
            holed = dK != len(Xp)
            t = r['pi']; d = (Nc[t] - Nc[i]) % 2; law = d == (info[t]['kind'] == 'DL')
            st[('holed' if holed else 'holefree', 'law_ok' if law else 'LAW_FAIL')] += 1
print(gf, 'graphs', min(k, maxg), dict(st))
