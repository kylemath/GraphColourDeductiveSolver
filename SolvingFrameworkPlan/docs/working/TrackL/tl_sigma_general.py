#!/usr/bin/env python3
"""Track L [data]: Lemma S in its general form (no DL / N hypothesis on c):
u rigid, c = pi(u), #P1(c) = 3 and #P2(c) = 3  ==>  #a_c m_c = 2, #A_c B_c = 1.   Also tallies c's kind.
usage: tl_sigma_general.py GRAPHFILE STRIDE OFFSET MAXGRAPHS"""
import sys
from collections import Counter
from tl_lib import HoleData, read_graphs
gf, stride, off, maxg = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
T = Counter()
for name, rot in read_graphs(gf, stride, off, maxg):
    for h in [v for v in range(len(rot)) if len(rot[v]) == 5]:
        hd = HoleData(rot, h)
        for u in range(hd.S):
            if not hd.rigid(u): continue
            c = hd.info[u]['pi']; rc = hd.info[c]
            T['rigid'] += 1
            if rc['kind'] == 'F': T['img_filled'] += 1; continue
            c6 = rc['c6']
            if c6[0] + c6[1] == 3 and c6[2] + c6[3] == 3:
                T[('hyp', rc['kind'])] += 1
                T['fail'] += (c6[0], c6[1]) != (2, 1)
print(gf, stride, off, dict(sorted(T.items(), key=str)), flush=True)
