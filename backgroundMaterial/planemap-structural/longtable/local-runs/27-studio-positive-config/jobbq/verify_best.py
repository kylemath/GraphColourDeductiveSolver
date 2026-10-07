#!/usr/bin/env python3
"""Job BQ (2): independent Python (jobbv/verify_bprime.py on jobuv/uv_lib.py) B' slack on the lowest-slack search graphs, min over positive-containing groups, both orientations."""
import sys, os, json, glob
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '../jobbv'))
from verify_bprime import check
for fn in sorted(glob.glob(os.path.join(HERE, 'best/*.json'))):
    d = json.load(open(fn))
    for m in (False, True):
        out = check(d['faces'], d['hole'], m); pos = [g['slack'] for g in out if g['pos']]
        print(os.path.basename(fn), 'mirror' if m else 'plantri', 'C++ slack', d['slack'], '| Python: groups', len(out), 'identity fails', sum(not g['identity'] for g in out),
              'min slack (positive groups)', min(pos) if pos else None, 'min slack (all)', min(g['slack'] for g in out))
