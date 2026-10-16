"""EXPLORE round 12: for each wlp3 output, can its certificate receivers be split into adjacent pairs (pairs.py fits)
with matching dual weights?  If yes, the certificate is also one for the pair-averaging model (charge(u) + charge(v)
<= 2t on adjacent bigs).  Small LP: mu[A,B] >= 0 on fitting pairs, sum over pairs containing A (A-A counted twice)
= lambda_A.  Usage: python3 certpair.py WLP3_OUT..."""
import sys, re, os, itertools
import numpy as np
from scipy.optimize import linprog
sys.argv, FILES = [sys.argv[0]], sys.argv[1:]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pairs.py')).read(); exec(src[:src.index('arrs = [')])
for fn in FILES:
    R = []
    for line in open(fn):
        m = re.match(r'\s+([\d.]+)\s+receiver d=(\d+) link (\S+) s (\S+),', line)
        if m: R.append((float(m.group(1)), m.group(3), m.group(4)))
    n = len(R); P = []
    for a, b in itertools.combinations_with_replacement(range(n), 2):
        A, B = R[a][1:], R[b][1:]
        ok = any(fits(view(A[0], A[1], i), B) for i, ch in enumerate(A[0]) if ch in '789')
        if ok: P.append((a, b))
    if not P: print('%s: %d receivers, no fitting pair' % (os.path.basename(fn), n)); continue
    M = np.zeros((n, len(P)))
    for k, (a, b) in enumerate(P): M[a, k] += 1; M[b, k] += 1
    res = linprog(np.zeros(len(P)), A_eq=M, b_eq=[r[0] for r in R], bounds=[(0, None)] * len(P), method='highs')
    tt = re.search(r't\* = ([\d.]+)', open(fn).read())
    print('%s: t = %s, %d receivers, fitting pairs %s -> pair certificate %s' % (os.path.basename(fn), tt.group(1) if tt else '?', n,
          ['%s-%s' % (R[a][1], R[b][1]) for a, b in P], 'EXISTS' if res.status == 0 else 'none'))
