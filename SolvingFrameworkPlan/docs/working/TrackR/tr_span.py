#!/usr/bin/env python3
"""Track R: certificate span.  Global ground set U (pairs admissible at ALL cycle states), connectivity imposed only
at a window of k consecutive states.  Prints, for every k, the LP excess bound of every window (Lagrangian LP of
tr_lag.py, exact optimum).  The smallest k with some window > 0 is the span of the shortest certificate.
usage: tr_span.py DATA.json [KMAX]"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tr_lag import load, solve
D0 = load(sys.argv[1]); L = len(D0['cols']); base = 3 * (D0['n'] - 1) - 8
kmax = int(sys.argv[2]) if len(sys.argv) > 2 else L
for k in range(2, kmax + 1):
    row = []
    for s in (range(L) if k < L else [0]):
        W = [(s + i) % L for i in range(k)]; idx = {t: i for i, t in enumerate(W)}
        D = dict(D0); D['cols'] = [D0['cols'][t] for t in W]
        D['parts'] = [(idx[t], p, q, P) for (t, p, q, P) in D0['parts'] if t in idx]
        opt, u = solve(D, norm='none', verbose=False)
        row.append(round(opt - base, 3))
    print(json.dumps(dict(src=D0['src'], k=k, Nprof=D0['Nprof'], e_by_start=row)), flush=True)
    if k < L and min(row) > 0.5: break
