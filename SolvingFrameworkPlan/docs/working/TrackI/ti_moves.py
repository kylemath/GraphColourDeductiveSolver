#!/usr/bin/env python3
"""Track I: parity of the chain count N under every Kempe move between unfilled states, and the candidate invariant
    psi(s) = N(s) + L1(s) + L2(s) + j(s)   (mod 2)          (j = repeat index of the unfilled state).
Remark 7 (Track I, hand): a link-free swap preserves N + L1 + L2 (mod 2) on the sphere; pi (from a DL state) flips
N + L1 + L2 and shifts j by 3.  Tallies (move type, parity change of N, of psi).
usage: ti_moves.py GRAPHFILE STRIDE MAXGRAPHS"""
import sys, os
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'TrackH'))
from th_engine import Hole
from ti_chains import nchains
gf, stride, maxg = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); st = Counter(); k = 0
for ln, l in enumerate(open(gf)):
    if ln % stride: continue
    p = l.split()
    if len(p) < 3: continue
    rot = [list(map(int, r.split(','))) for r in p[2].split(';')]; k += 1
    if k > maxg: break
    for h in [v for v in range(len(rot)) if len(rot[v]) == 5]:
        H = Hole(rot, h).build(); S = len(H.states)
        N = [nchains(H, H.col(i)) for i in range(S)]
        psi = [None] * S
        for i in range(S):
            r = H.info[i]
            if r['kind'] != 'F': psi[i] = (N[i] + r['L1'] + r['L2'] + r['j']) % 2
        for i in range(S):
            for (a, b, hit, sz, t, mn) in H.moves[i]:
                if psi[i] is None or psi[t] is None: continue
                typ = 'linkfree' if not hit else 'link'
                st[(typ, 'dN', (N[t] - N[i]) % 2)] += 1
                st[(typ, 'dN+dL', (N[t] + H.info[t]['L1'] + H.info[t]['L2'] - N[i] - H.info[i]['L1'] - H.info[i]['L2']) % 2)] += 1
                st[(typ, 'dpsi', (psi[t] - psi[i]) % 2)] += 1
print(gf, 'graphs', min(k, maxg), dict(sorted(st.items(), key=str)))
