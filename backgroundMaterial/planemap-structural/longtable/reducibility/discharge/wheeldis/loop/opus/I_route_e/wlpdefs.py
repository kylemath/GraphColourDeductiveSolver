"""Wheel-level discharging LP (exploratory).  See README.md section 0.
Letters 5,6,7,8,9 (9 = degree >= 9).  R5/R6 = reducible 5-/6-wheel words (Job 17 D, Lean-certified C; the six
565xxx 6-wheels excluded).  Variables y[r] for rooted words r = (u, a, b, c, e) (u >= 7 = the sender's letter, the
5's link read from u), up to the reflection (u,a,b,c,e) ~ (u,e,c,b,a).
  sender rows   : every non-R cyclic 5-word w with a big letter: sum over big positions y[root] >= 1 - t
  receiver rows : degree d (letter min(d,9)), arrangement (w_i, s_i)_{i<d}: sum over w_i = 5 of y[...] <= d - 6 + t
Receiver rows are generated lazily by a max-plus DP over states (w_{i-1}, s_{i-1}, w_i).
Usage: python3 wlp.py [extra-R-option ...]   options: noC (drop C wheels)"""
import sys, os, itertools, collections
import numpy as np
from scipy.optimize import linprog
HERE = os.path.dirname(os.path.abspath(__file__)); DIS = os.path.dirname(HERE)
OPT = set(sys.argv[1:])
L = (5, 6, 7, 8, 9)
def canon(w):
    w = tuple(w); return min(min(s[k:] + s[:k] for k in range(len(s))) for s in (w, w[::-1]))
R5, R6 = set(), set()
UNCERT = {'565667', '565676', '565677', '565757', '565767', '565777'}
for line in open(os.path.join(DIS, 'studio17', 'wheels17_verdicts.txt')):
    if line.startswith('#'): continue
    f = line.split(); nm, v = f[0], f[2]
    fam, w = nm.split('_')
    if v == 'D' or (v == 'C' and w not in UNCERT and 'noC' not in OPT):
        (R5 if fam == 'c5' else R6).add(tuple(map(int, w)))
if 'noC' in OPT: R5.discard((6, 6, 6, 6, 6))
R5 |= {canon(w) for w in OPT_EXTRA} if (OPT_EXTRA := [tuple(map(int, o[3:])) for o in OPT if o.startswith('R5=')]) else set()
FANS = []                             # D-reducible fans (fans.py, out/fans_dfast.out): F = any degree
if 'nofan' not in OPT:
    for line in open(os.path.join(HERE, 'out', 'fans_dfast.out')):
        if 'D=true' in line: FANS.append(tuple(0 if ch == 'F' else int(ch) for ch in line.split()[0][2:]))
def _match(w, pat):
    w = tuple(w)
    for s in (w, w[::-1]):
        for k in range(5):
            r = s[k:] + s[:k]
            if all(p == 0 or p == q for p, q in zip(pat, r)): return True
    return False
def isR5(w):
    return canon(w) in R5 or any(_match(w, p) for p in FANS)
def isR6(w):                          # census 6-wheels, or a 2.122 (6-centre, link 5,5,5 consecutive)
    w = tuple(w)
    return canon(w) in R6 or any(w[i] == w[(i + 1) % 6] == w[(i + 2) % 6] == 5 for i in range(6))
def root(w, j):                       # w cyclic, position j is the sender
    a = tuple(w[j:] + w[:j]); b = (a[0],) + tuple(reversed(a[1:])); return min(a, b)

