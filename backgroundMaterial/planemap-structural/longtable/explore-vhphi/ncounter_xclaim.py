"""Relaxed lock table over ALL rigid discs of a list: for each Case-I neighbour c' (resp. c'') record lock of c' at u0
(resp. c'' at u2) against the lock status of the three original fans of c.  Tests the observation
   c' locked at u0  =>  original fan u4 separable ;  c'' locked at u2  =>  original fan u3 separable.   [exploratory]
usage: python3 ncounter_xclaim.py FILE [cap]"""
import sys
from collections import Counter
from ncounter_lib import *
fn = sys.argv[1]; cap = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
def tag(r): return 'L' if r[0] is False else ('U' if r[0] else '?')
cp, cpp = Counter(), Counter(); nI = 0; unk = 0
for line in open(fn):
    if not line.startswith('DISC'): continue
    adj, col, x, ring = parse_disc(line)
    if not is_rigid(adj, col, x): continue
    t1, t2 = classify_both(adj, col, x, ring)
    if t1[0] != 'I' and t2[0] != 'I': continue
    nI += 1
    L = None
    K2 = comp_of(adj, col, ring[2], {D, G}, x); K0 = comp_of(adj, col, ring[0], {D, B}, x)
    if t1[0] == 'I':
        s = kempe_class(adj, swapK(col, K2, D, G), x, ring[0], cap)
        if L is None: L = ''.join(tag(r) for r in fan_locks(adj, col, x, ring, cap))
        cp[(tag(s), L)] += 1
    if t2[0] == 'I':
        s = kempe_class(adj, swapK(col, K0, D, B), x, ring[2], cap)
        if L is None: L = ''.join(tag(r) for r in fan_locks(adj, col, x, ring, cap))
        cpp[(tag(s), L)] += 1
print(fn, 'rigid discs with a Case-I neighbour:', nI)
print(" c' at u0: (c' status, fans u1u3u4 of c):", dict(sorted(cp.items())))
print(" c'' at u2:", dict(sorted(cpp.items())))
