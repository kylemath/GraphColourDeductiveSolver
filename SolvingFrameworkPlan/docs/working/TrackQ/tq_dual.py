#!/usr/bin/env python3
"""Track Q: LP dual of the mcf model (tq_mcf.py) -- how the LP lower bound splits over cycle states and pair graphs.
Bound = sum_rows y_r * rhs_r + bound terms; we report sum y*rhs aggregated by state t and by (t, pair).
usage: tq_dual.py DATA.json"""
import sys, os, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import tq_mcf
from scipy.optimize import linprog
from scipy.sparse import vstack
tq_mcf.RETURN_MODEL = True
d = json.load(open(sys.argv[1])); U = [tuple(e) for e in d['U']]; parts = [(t, p, q, frozenset(P)) for t, p, q, P in d['parts']]
M = tq_mcf.solve_mcf(d, U, parts, None, 600, True)
A, lo, hi = M['A'], M['lo'], M['hi']
eq = np.where(lo == hi)[0]; ge = np.where((lo > -np.inf) & (lo != hi))[0]; le = np.where((hi < np.inf) & (lo != hi))[0]
A_ub = vstack([A[le], -A[ge]]).tocsr(); b_ub = np.concatenate([hi[le], -lo[ge]])
res = linprog(M['c'], A_ub=A_ub, b_ub=b_ub, A_eq=A[eq], b_eq=lo[eq], bounds=list(zip(M['lb'], M['ub'])), method='highs')
print('LP', res.fun, 'e_LP', res.fun - M['base'])
yeq = res.eqlin.marginals; yub = res.ineqlin.marginals
contrib = collections.Counter(); byt = collections.Counter()
for k, r in enumerate(eq):
    v = yeq[k] * lo[r]
    if abs(v) > 1e-9: tg = M['rowtag'][r]; contrib[str(tg)] += v; byt[tg[0]] += v
for k, r in enumerate(list(le) + list(ge)):
    rhs = hi[r] if k < len(le) else -lo[r]
    v = yub[k] * rhs
    if abs(v) > 1e-9: tg = M['rowtag'][r]; contrib[str(tg)] += v; byt[tg[0] if tg else 'target'] += v
bnd = res.fun - sum(byt.values())
print('row part', round(sum(byt.values()), 4), 'bound part (forced link edges etc.)', round(bnd, 4))
Np = d['Nprof']
print('by state:', {t: round(v, 3) for t, v in sorted(byt.items(), key=lambda x: str(x[0]))}, 'Nprof', Np)
