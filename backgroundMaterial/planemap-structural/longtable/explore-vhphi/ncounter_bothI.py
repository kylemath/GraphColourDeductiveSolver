"""For rigid discs whose c' and c'' are BOTH Case I (first-order locked, no early unlock), report which of the
three original fans (u1,u3,u4) of c is unlocked (full Kempe-class BFS, cap), and the full lock status of c', c''.
usage: python3 ncounter_bothI.py FILE [cap]   [exploratory]"""
import sys
from collections import Counter
from ncounter_lib import *
fn = sys.argv[1]; cap = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
cnt = Counter(); rows = []
for line in open(fn):
    if not line.startswith('DISC'): continue
    adj, col, x, ring = parse_disc(line)
    if not is_rigid(adj, col, x): continue
    t1, t2 = classify_both(adj, col, x, ring)
    if not (t1[0] == 'I' and t2[0] == 'I'): continue
    L = fan_locks(adj, col, x, ring, cap)
    lk = tuple('L' if r[0] is False else ('U' if r[0] else '?') for r in L)
    # c' and c'' full lock at their fans
    K2 = comp_of(adj, col, ring[2], {D, G}, x); K0 = comp_of(adj, col, ring[0], {D, B}, x)
    cp = swapK(col, K2, D, G); cpp = swapK(col, K0, D, B)
    s1 = kempe_class(adj, cp, x, ring[0], cap); s2 = kempe_class(adj, cpp, x, ring[2], cap)
    key = (lk, 'c1' + ('L' if s1[0] is False else 'U' if s1[0] else '?'), 'c2' + ('L' if s2[0] is False else 'U' if s2[0] else '?'))
    cnt[key] += 1
    rows.append((key, [r[1] for r in L], s1[1], s2[1], t1[1].get('c3_broken_Db'), t2[1].get('c3_broken_Db')))
print(fn, len(rows), 'both-Case-I rigid discs')
for k, v in sorted(cnt.items()): print(' ', k, v)
for r in rows[:6]: print('  ', r)
