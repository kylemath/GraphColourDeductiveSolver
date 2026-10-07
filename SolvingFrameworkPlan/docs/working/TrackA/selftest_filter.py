#!/usr/bin/env python3
"""Track A: filter tests on known examples (icosahedron, the order-22 2.122 F-cycle graph Tri22, census graphs)."""
import json
from tracka_lib import *
P = '/Users/kylemathewson/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/'
F = []
for i in range(5):
    a, b = 1 + i, 1 + (i + 1) % 5; c, d = 6 + i, 6 + (i + 1) % 5
    F += [(0, a, b), (a, c, b), (b, c, d), (11, d, c)]
ico = rot_from_faces(F)
print('icosahedron', G(ico).summary())
T22 = json.load(open(P + 'studiointel/fcycle/fcycle_order22.json'))
print('Tri22 (F-cycle 2.122 witness)', G(rot_from_faces([tuple(f) for f in T22['faces']])).summary())
for fn in ('in-cfree-27.txt', 'in-plantri-24.txt'):
    for k, l in enumerate(open(P + 'longtable/local-runs/27-studio-positive-config/' + fn)):
        if k >= 3: break
        name, rot = parse_line(l); g = G(rot); s = g.summary(); print(name, s)
        # mirror invariance
        sm = G([r[::-1] for r in rot]).summary(); assert sm['frame'] == s['frame'] and sm['occ']['DiamondM'] == s['occ']['DiamondP'] and sm['occ']['C2122M'] == s['occ']['C2122P']
