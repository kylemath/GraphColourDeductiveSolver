"""Is there a LINEAR potential phi(M) = sum_{e in M} c_e increasing by >= 1 along every arc of D?
LP feasibility per class.  usage: linpot.py n [maxclasses]"""
import sys, json
import numpy as np
from scipy.optimize import linprog
from r0lib import G5, analyse
n = int(sys.argv[1]); mx = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9
feas = infeas = 0; bad = []
for ci, l in enumerate(open(f'out/census_n{n}_p.jsonl')):
    if ci >= mx: break
    r = json.loads(l); g = G5(r['n'], [tuple(e) for e in r['edges']], r['fv'])
    A = analyse(g); P = A['P']
    if not A['arcs']: feas += 1; continue
    rows = []
    for i, j in A['arcs']:
        row = np.zeros(g.m)
        for e in range(g.m):
            row[e] = ((P[i] >> e) & 1) - ((P[j] >> e) & 1)   # phi(M)-phi(M') <= -1
        rows.append(row)
    res = linprog(np.zeros(g.m), A_ub=np.array(rows), b_ub=-np.ones(len(rows)), bounds=[(None, None)] * g.m, method='highs')
    if res.status == 0: feas += 1
    else: infeas += 1; bad.append(ci)
print(f'n={n}: linear potential feasible {feas}, infeasible {infeas}', bad[:10])
