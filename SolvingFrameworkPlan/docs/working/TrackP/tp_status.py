#!/usr/bin/env python3
"""Track P: progress of tn_search runs (best score, best law-cycle penalty/profile, # examples)."""
import json, sys, glob
for f in sys.argv[1:]:
    b = None; ex = 0; srcs = set()
    for l in open(f):
        d = json.loads(l)
        if d.get('ev') == 'example': ex += 1; srcs.add(d['src']); continue
        s = d.get('sc')
        if s is not None and (b is None or s > b[0]):
            tn = d['tn']; b = (s, tn.get('win'), tn['bc'][1][8] if 'bc' in tn else None, tn['bc'][1][0] if 'bc' in tn else None, d['n'], d['nedge'])
    print(f, 'examples', ex, 'srcs', sorted(srcs)[:6], 'best', b)
