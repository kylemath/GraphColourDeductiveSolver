"""s71: statistics, exact-ish ILP check, outputs. usage: report.py SP_DIR OUT_DIR (after cover.py)"""
import pickle, re, collections, json, sys, numpy as np
SP, OUT = sys.argv[1:3]
d = pickle.load(open(OUT + '/cover.pkl', 'rb')); items = pickle.load(open(OUT + '/items.pkl', 'rb'))
cls, cand, E0, inF = d['cls'], d['cand'], d['E0'], d['inF']
items = [it for it in items if it[2]]
chosen = d['res']['A'][0]
rsr = {}
for l in open(SP + '/rsst.txt'):
    f = l.split(); rsr[f[0].split('_')[0]] = int(f[1])
def ring(n):
    if n.startswith('rsst'): return rsr[n.split('_')[0]]
    m = re.search(r'_r(\d+)$', n)
    if m: return int(m.group(1))
    m = re.match(r'[a-z]+(\d+)_', n)
    return int(m.group(1)) if m else -1
def isD(n): return cls[n].endswith('D') or cls[n] == 'nl51'
SRC = {'nl51': 'nl51', 'rsstD': 'RSST D', 'rsstC': 'RSST C', 'k3xD': 'k3x D', 'k3xC': 'k3x C', 'k3pD': 'k3p D', 'k3pC': 'k3p C'}
def stats(S):
    return collections.Counter(SRC[cls[n]] for n in S), collections.Counter(ring(n) for n in S), collections.Counter((SRC[cls[n]], ring(n)) for n in S)
# forced configs: sole non-leaked justifier of some item, by item kind
forced = collections.defaultdict(set)
for k, i, ws in items:
    if len(ws) == 1: forced[k.split('_')[0] if k.startswith('R_') else k[:2] if k.startswith('KT') else 'L3Q'].add(next(iter(ws)))
allforced = set().union(*forced.values())
nrule1 = sum(1 for it in items if it[0].startswith('R_') and len(it[2]) == 1)
nrule = sum(1 for it in items if it[0].startswith('R_'))
nkt1 = sum(1 for it in items if it[0].startswith('KT') and len(it[2]) == 1); nkt = sum(1 for it in items if it[0].startswith('KT'))
nl1 = sum(1 for it in items if it[0].startswith('L3Q') and len(it[2]) == 1); nl = sum(1 for it in items if it[0].startswith('L3Q'))
print('rules', nrule, 'single-justifier', nrule1, '| KT', nkt, nkt1, '| L3Q', nl, nl1, '| forced configs', len(allforced))
# ILP on residual
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
rem = [it for it in items if not (it[2] & allforced)]
names = sorted(set().union(*[it[2] for it in rem])); ix = {n: j for j, n in enumerate(names)}
# dominance: dedupe identical rows
rows = list({it[2] for it in rem})
A = lil_matrix((len(rows), len(names)))
for r, ws in enumerate(rows):
    for n in ws: A[r, ix[n]] = 1
print('residual items', len(rem), 'distinct', len(rows), 'cols', len(names))
c = np.ones(len(names)) - 1e-4 * np.array([n in E0 for n in names])
res = milp(c, constraints=LinearConstraint(A.tocsr(), 1, np.inf), integrality=np.ones(len(names)), bounds=Bounds(0, 1), options={'time_limit': 240})
print('milp status', res.status, res.message, 'obj', res.fun, 'bound', getattr(res, 'mip_dual_bound', None))
ilp = set(allforced)
if res.x is not None: ilp |= {n for n, x in zip(names, res.x) if x > .5}
assert all(it[2] & ilp for it in items)
print('ILP-cover size', len(ilp), 'greedy', len(chosen), 'forced', len(allforced))
lb = len(allforced) + (res.mip_dual_bound if getattr(res, 'mip_dual_bound', None) is not None else 0)
pickle.dump({'ilp': ilp, 'status': res.status, 'dual': getattr(res, 'mip_dual_bound', None), 'allforced': allforced, 'forced': dict(forced)}, open(OUT + '/ilp.pkl', 'wb'))
