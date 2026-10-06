"""Refined Case table.  For every rigid disc of FILE and each neighbour c' (at u0) / c'' (at u2):
   type = FO/S1 (early first-order or step-1 unlock), II, Ia (Case I and chain {D,b} broken at c3: separable after 3 D-free swaps + x-swap),
          Ib (Case I and c3 intact).
Tally (type) x (lock pattern of the three original fans of c, letters L/U/? for u1,u3,u4).  Only discs whose pattern could matter
(c fans computed for every disc with at least one neighbour of type II/Ia/Ib).  [exploratory, post hoc]
usage: python3 ncounter_types.py FILE [cap]"""
import sys
from collections import Counter
from ncounter_lib import *
fn = sys.argv[1]; cap = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
def tag(r): return 'L' if r[0] is False else ('U' if r[0] else '?')
def typ(t):
    if t[0] != 'I': return t[0]
    return 'Ia' if t[1].get('c3_broken_Db') else 'Ib'
T = Counter(); ND = 0
for line in open(fn):
    if not line.startswith('DISC'): continue
    adj, col, x, ring = parse_disc(line)
    if not is_rigid(adj, col, x): continue
    ND += 1
    t1, t2 = classify_both(adj, col, x, ring)
    a, b = typ(t1), typ(t2)
    if a in ('FO', 'S1') and b in ('FO', 'S1'): continue
    L = ''.join(tag(r) for r in fan_locks(adj, col, x, ring, cap))
    T[(L, a, b)] += 1
print(fn, 'rigid discs', ND)
for k, v in sorted(T.items()): print('  ', k, v)
