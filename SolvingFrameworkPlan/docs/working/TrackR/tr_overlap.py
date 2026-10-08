#!/usr/bin/env python3
"""Track R: overlap of anchored part-tag keys (tr_rule.py partA, radius r) between a reference cycle and others,
for every anchor; picks the type-aligned anchor with the largest overlap.  usage: tr_overlap.py R REF.json OTHER.json ..."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tr_lag import load
from tr_rule import keys_for
r = int(sys.argv[1]); R = load(sys.argv[2]); KR = set(keys_for(R, r, 'partA', 0).values())
for f in sys.argv[3:]:
    D = load(f); L = len(D['cols']); best = None
    for b in range(L):
        K = set(keys_for(D, r, 'partA', b).values()); ov = len(K & KR) / len(K)
        if best is None or ov > best[1]: best = (b, ov, len(K))
    print('%s@%d overlap %.3f keys %d' % (f, best[0], best[1], best[2]), flush=True)
