#!/usr/bin/env python3
"""Track R: apply a FIXED anchored rule f (tr_rule.py --out, mode partA) to new cycles, at every anchor.
Prices u_{t,e} = f(key(t,e)); an edge whose column sum exceeds 1 has its prices scaled down (still a valid
certificate).  Exact rational evaluation of the bound (tr_lag.verify).  usage: tr_apply.py RULE.json DATA.json ..."""
import sys, os, json
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tr_lag import load, verify
from tr_rule import keys_for
R = json.load(open(sys.argv[1])); r = R['r']; mode = R['mode']
tt = lambda z: tuple(tt(y) for y in z) if isinstance(z, list) else z
f = {tt(k): Fraction(v).limit_denominator(60) for k, v in R['f']}
for path in sys.argv[2:]:
    D = load(path); L = len(D['cols']); base = 3 * (D['n'] - 1) - 8; res = []
    for a in range(L):
        K = keys_for(D, r, mode, a); u = {}
        for (t, k), key in K.items():
            if key in f: u[(t, k)] = f[key]
        col = {}
        for (t, k), v in u.items(): col[k] = col.get(k, 0) + v
        for (t, k) in list(u):
            if col[k] > 1: u[(t, k)] = u[(t, k)] / col[k]
        res.append(verify(D, u) - base)
    best = max(range(L), key=lambda a: res[a])
    print('%-28s Nprof %s  best anchor %d -> e >= %s ; by anchor %s' % (D['src'], D['Nprof'], best, res[best], [str(x) for x in res]), flush=True)
