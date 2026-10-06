#!/usr/bin/env python3
"""studiointel config_free_count.py -- [exploratory] Math 16:15 item (a): how many 4-connected min-degree-5 triangulations of each order
contain neither the Birkhoff diamond (RSST #0) nor 2.122 (RSST #1)? Input: gen_tri files. Writes the configuration-free graphs to cfree/."""
import sys, os, json
sys.path.insert(0, '.')
import causal_test as CT
from r55566_test import graphs_from
os.makedirs('cfree', exist_ok=True)
for arg in sys.argv[1:]:
    tot = free = 0
    for name, F in graphs_from(arg):
        tot += 1
        if CT.count_occ(F, CT.P[0], cap=1) == 0 and CT.count_occ(F, CT.P[1], cap=1) == 0:
            free += 1; json.dump({'faces': [list(f) for f in F], 'source': name}, open('cfree/%s.json' % name.replace('#', '_'), 'w'))
    print(arg, 'graphs', tot, 'configuration-free', free, flush=True)
