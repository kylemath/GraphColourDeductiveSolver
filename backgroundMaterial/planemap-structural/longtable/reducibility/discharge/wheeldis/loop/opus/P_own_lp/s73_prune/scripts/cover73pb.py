"""cover73.py SET.json|all|drop276 OUTTSV : ring-weighted min-cost config cover for tables + the given rule subset (ids into rules_drop276 universe)"""
import os, pickle, re, collections, sys, json, numpy as np
sys.path.insert(0, '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s73_prune/scripts')
from lib import *
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
spec, OUT = sys.argv[1:3]
SP = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/sp'
S71 = B + 's71_ruleset/'
d = pickle.load(open(S71 + 'cover.pkl', 'rb')); items = [it for it in pickle.load(open(S71 + 'items.pkl', 'rb')) if it[2]]
cls, cand, E0 = d['cls'], d['cand'], d['E0']
L, off = load_uni()
Nn = lambda r: json.dumps(r, sort_keys=True, separators=(',', ':'))
def key(g, r):
    if g.endswith('w6'): return 'R_' + g + '_0', Nn(r)
    return 'R_' + g, Nn(r)     # g = d7_w7_1 -> R_d7_w7_1
if spec == 'all': sel = None
else:
    ids = range(len(L)) if spec == 'drop276' else json.load(open(spec)); sel = {key(*L[i]) for i in ids}
import pickle as _pk
_pc = _pk.load(open('' + B + 's73_prune/cells/percell_all.pkl','rb'))
tabs = [(t, str(j), set(ws)) for t in _pc for j, ws in enumerate(_pc[t])]; rl = [it for it in items if it[0].startswith('R_')]
keepr = rl if sel is None else [it for it in rl if (it[0], it[1]) in sel]
if sel is not None: assert len(keepr) == len(sel), (len(keepr), len(sel))
items = tabs + keepr; print('items: tables', len(tabs), 'rules', len(keepr))
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
W = {13: .1, 14: 25 / 60, 15: 1.25, 16: 4, 17: 13}
def cost(n):
    if not isD(n): return .25
    r = ring(n)
    if r == -1: return 2.
    if r <= 12: return 2 / 60
    return W[r]
names = sorted(set().union(*[it[2] for it in items])); ix = {n: j for j, n in enumerate(names)}
rows = list({frozenset(it[2]) for it in items}); A = lil_matrix((len(rows), len(names)))
for r, ws in enumerate(rows):
    for n in ws: A[r, ix[n]] = 1
c = np.array([1.0 if os.environ.get('COUNT') else cost(n) for n in names]); c2 = c - 1e-7 * np.array([n in E0 for n in names])
res = milp(c2, constraints=LinearConstraint(A.tocsr(), 1, np.inf), integrality=np.ones(len(names)), bounds=Bounds(0, 1), options={'time_limit': 900, 'mip_rel_gap': 1e-9})
S = {n for n, x in zip(names, res.x) if x > .5}; assert all(it[2] & S for it in items)
D = [n for n in S if isD(n)]
print('status', res.status, 'dual', res.mip_dual_bound, 'cost h %.3f' % sum(cost(n) for n in S), 'n', len(S), 'D', len(D), 'C', len(S) - len(D))
print('D ring hist', sorted(collections.Counter(ring(n) for n in D).items()))
print('C ring hist', sorted(collections.Counter(ring(n) for n in S if not isD(n)).items()))
print('forced', len({next(iter(it[2])) for it in items if len(it[2]) == 1}))
with open(OUT, 'w') as f:
    f.write('# name\tclass\tring\tcost_h\n')
    for n in sorted(S, key=lambda x: (not isD(x), ring(x), x)): f.write('%s\t%s\t%d\t%.4f\n' % (n, cls[n], ring(n), cost(n)))
