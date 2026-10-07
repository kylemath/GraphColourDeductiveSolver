#!/usr/bin/env python3
"""Job BQ (1): independent Python B' slack (jobbv/verify_bprime.py on jobuv/uv_lib.py) at the census extremes: p27#151376 h14 (min slack over positive groups, C++ 42)
and p27#134579 h23 (min slack over all groups, C++ -132), both orientations."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ('../jobbv', '../jobaw'): sys.path.insert(0, os.path.join(HERE, d))
from verify_bprime import check
from jobaw import faces_of_rot
want = {'p27#151376': (14, 42), 'p27#134579': (23, -132)}
for l in open(os.path.join(HERE, '../in-plantri-27.txt')):
    name = l.split(' ', 1)[0]
    if name not in want: continue
    rot = [[int(x) for x in s.split(',')] for s in l.split(' ', 2)[2].strip().split(';')]; h, cpp = want[name]
    for m in (False, True):
        out = check(faces_of_rot(rot), h, m); pos = [g['slack'] for g in out if g['pos']]; neg = sorted(g['slack'] for g in out if g['slack'] < 0)
        print(name, 'h%d' % h, 'mirror' if m else 'plantri', 'C++', cpp, '| Python: groups', len(out), 'identity fails', sum(not g['identity'] for g in out),
              'min slack (positive groups)', min(pos) if pos else None, 'min slack (all)', min(g['slack'] for g in out), 'negative groups', neg[:12],
              'negative groups with a positive cycle', sum(1 for g in out if g['slack'] < 0 and g['pos']))
