#!/usr/bin/env python3
"""Track S: where the free cycle C' of an in-shape state c = pi(u) sits relative to the figure-eights Q_u (= F12(c)),
Q_c = X_c u Y_c, at Phi-steps u -> c -> u2.  C' alternates M_u-edges (on Q_c) and M_c-edges (chords of Q_c).
Reports counts of C' M_u-edges on X_c / Y_c, and of C' vertices on X_u / Y_u.  usage as ts_spokes.py"""
import sys
from collections import Counter
from ts_lib import load_graphs, HoleData, phi_steps
from tl_lib import TaitState
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
C = Counter(); n = 0
for nm, h in specs:
    hd = HoleData(G[nm], h)
    for (u, c, u2) in phi_steps(hd):
        if not hd.inshape(c): continue
        Su = TaitState(hd, u); Sc = TaitState(hd, c)
        comps = Sc.components(Sc.H)
        free = [K for K in comps if not any(0 in Sc.E[k][:2] for k in K)]
        if len(free) != 1: C['bad'] += 1; continue
        Cp = free[0]; n += 1
        Mu = {k for k, e in enumerate(Su.E) if e[2] == 2}
        Mc = {k for k, e in enumerate(Sc.E) if e[2] == 2}
        Xc, Yc = set(Sc.X), set(Sc.Y); Xu, Yu = set(Su.X), set(Su.Y)
        a1 = len(Cp & Mu & Xc); a2 = len(Cp & Mu & Yc)
        vC = Sc.verts(Cp)
        b1 = len(vC & (Su.verts(Xu) - {0})); b2 = len(vC & (Su.verts(Yu) - {0}))
        # C' chords (M_c edges) relative to u's colours: on Y_u (C_u chords) or on X_u (M_{u-1} edges)
        ch = Cp & Mc; d1 = len(ch & Xu); d2 = len(ch & Yu)
        C[('Mu_on_Xc>0', a1 > 0)] += 1; C[('Mu_on_Yc>0', a2 > 0)] += 1
        C[('verts_on_Xu>0', b1 > 0)] += 1; C[('verts_on_Yu>0', b2 > 0)] += 1
        C[('Mc_on_Xu>0', d1 > 0)] += 1; C[('Mc_on_Yu>0', d2 > 0)] += 1
        C[('Mc_on_Yu=all', d1 == 0)] += 1
print('instances', n, dict(sorted(C.items(), key=str)))
