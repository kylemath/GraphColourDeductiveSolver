#!/usr/bin/env python3
"""Track H: for each rigid DL state c (component counts (am,AB,aA,mB,aB,mA) = (1,1,2,1,2,1)), the component-count
vector of pi(c) in pi(c)'s own frame, and (sphere) which of the counts exceed the rigid value.
usage: th_rigidnext.py GRAPHFILE MAXGRAPHS STRIDE"""
import sys
from collections import Counter
from th_engine import Hole
from th_rigidscan_lib import counts
gf, maxg, stride = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
vec = Counter(); k = 0; nr = 0
for ln, l in enumerate(open(gf)):
    if ln % stride: continue
    p = l.split()
    if len(p) < 3: continue
    rot = [list(map(int, r.split(','))) for r in p[2].split(';')]; k += 1
    if k > maxg: break
    for h in [v for v in range(len(rot)) if len(rot[v]) == 5]:
        H = Hole(rot, h)
        for i in range(len(H.states)):
            r, col = H.analyse_state(i)
            if r['kind'] != 'DL' or counts(H, col, r['roles']) != [1, 1, 2, 1, 2, 1]: continue
            nr += 1; t = r['pi']; r2, col2 = H.analyse_state(t)
            vec[(r2['kind'], tuple(counts(H, col2, r2['roles'])))] += 1
print('rigid DL states', nr)
for kv, c in vec.most_common(): print(c, kv)
