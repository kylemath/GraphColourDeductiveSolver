#!/usr/bin/env python3
"""[exploratory] Positive control: Kempe classes of 4-colourings of the triangular lattice on an L x M torus
(6-regular; neighbours (i+-1,j), (i,j+-1), (i+1,j-1), (i-1,j+1)), via kclass with hole -1, and with one hole."""
import os, subprocess, sys, json
H = os.path.dirname(os.path.abspath(__file__))
for L, M in [(3, 3), (3, 4), (4, 4), (3, 5), (5, 5), (3, 6), (4, 6), (6, 6), (3, 9), (7, 7)]:
    V = lambda i, j: (i % L) * M + (j % M)
    E = {tuple(sorted((V(i, j), V(i + a, j + b)))) for i in range(L) for j in range(M) for a, b in ((1, 0), (0, 1), (1, -1))}
    E = {e for e in E if e[0] != e[1]}
    p = "/tmp/torus_%d_%d.edges" % (L, M)
    open(p, "w").write("%d %d\n" % (L * M, len(E)) + "".join("%d %d\n" % e for e in sorted(E)))
    simple = all(len({V(i + a, j + b) for a, b in ((1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1))}) == 6 for i in range(L) for j in range(M))
    for h in (-1, 0):
        o = subprocess.run([os.path.join(H, "kclass"), p, str(h), "20000000"], capture_output=True, text=True).stdout.strip()
        print(json.dumps({"torus": [L, M], "simple_6_regular": simple, "hole": h, "out": json.loads(o)}), flush=True)
