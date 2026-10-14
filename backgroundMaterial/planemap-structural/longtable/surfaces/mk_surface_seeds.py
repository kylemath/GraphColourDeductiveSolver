#!/usr/bin/env python3
"""Turn TrackJ surface graph files (triangulations of RP2 / torus / Klein) into face lists for s2_search (faces found
by SAT: every edge in exactly two triangles, every link one cycle)."""
import sys, json
from sf_lib import parse_line, euler, orientable
from sf_cplx import solve
out = open(sys.argv[1], 'w'); k = 0
for f in sys.argv[2:]:
    for l in open(f):
        if len(l.split()) < 3: continue
        name, adj = parse_line(l)
        a, b, K = solve(adj, armB=True, hole_link=None)
        if b is True:
            out.write(json.dumps(dict(name=name, chi=euler(K), orientable=orientable(K), faces=K)) + '\n'); k += 1
print('seeds', k)
