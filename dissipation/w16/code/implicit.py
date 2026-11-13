# W16: implicit equalities at t = 0: the sender / receiver rows that every t = 0 solution of the given row set holds at exactly 0.
# Round k: fix t = 0, add a slack s_r in [0, 1] to every not-yet-certified row, maximise the sum of slacks; rows with s_r > 1e-7
# are certainly not implicit; repeat on the rest until no new row gets slack (then the rest are implicit equalities [M]).
# usage: python3 -I implicit.py LABELS.pkl FAM OUT.json
import sys, os, pickle, json, time, collections
sys.path.insert(0, '/tmp/swarm-W16/code')
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
import w16lib as W
from lp_patterns import lab_str
T0 = time.time()
def log(*a): print(*a, '[%.0fs]' % (time.time() - T0), flush=True)
def run(rows, cand):
    keys = sorted({k for _, cf, _, _ in rows for k in cf}, key=str); idx = {k: i for i, k in enumerate(keys)}; nv = len(keys)
    sl = {r: nv + j for j, r in enumerate(sorted(cand))}; ntot = nv + len(sl)
    Ai, Aj, Av, b = [], [], [], []; Ei, Ej, Ev = [], [], []
    for ri, (lab, cf, kind, rhs) in enumerate(rows):
        if kind == 'eq':
            r = len(set(Ei)) if False else None
        if kind == 'ge':   # sum >= 1 (+ s)  ->  -sum + s <= -1
            r = len(b); b.append(-1.0)
            for k, v in cf.items(): Ai.append(r); Aj.append(idx[k]); Av.append(-float(v))
            if ri in sl: Ai.append(r); Aj.append(sl[ri]); Av.append(1.0)
        elif kind == 'le':   # sum + s <= d - 6
            r = len(b); b.append(rhs)
            for k, v in cf.items(): Ai.append(r); Aj.append(idx[k]); Av.append(float(v))
            if ri in sl: Ai.append(r); Aj.append(sl[ri]); Av.append(1.0)
        elif kind == 'mrow':
            r = len(b); b.append(0.0)
            for k, v in cf.items(): Ai.append(r); Aj.append(idx[k]); Av.append(float(v))
        else:
            r = (Ei[-1] + 1) if Ei else 0
            for k, v in cf.items(): Ei.append(r); Ej.append(idx[k]); Ev.append(float(v))
    A = coo_matrix((Av, (Ai, Aj)), shape=(len(b), ntot)).tocsr()
    neq = (max(Ei) + 1) if Ei else 0
    E = coo_matrix((Ev, (Ei, Ej)), shape=(neq, ntot)).tocsr() if neq else None
    c = np.zeros(ntot); c[nv:] = -1.0
    bounds = [(0.0, W.CAP.get(k[0])) for k in keys] + [(0.0, float(os.environ.get("SCAP", "1e-3")))] * len(sl)
    res = linprog(c, A_ub=A, b_ub=np.array(b), A_eq=E, b_eq=np.zeros(neq) if neq else None, bounds=bounds, method='highs')
    if res.status != 0: return None, res
    return {r: res.x[j] for r, j in sl.items()}, res
if __name__ == '__main__':
    ARGV = list(sys.argv); W.init()
    labs = pickle.load(open(ARGV[1], 'rb')); fam = ARGV[2]
    rows = W.build_lp(labs, fam)
    cand = {i for i, r in enumerate(rows) if r[2] in ('ge', 'le')}; log('rows %d, candidate rows %d' % (len(rows), len(cand)))
    for rnd in range(int(os.environ.get("ROUNDS", "25"))):
        s, res = run(rows, cand)
        if s is None: log('t = 0 INFEASIBLE (status %d %s)' % (res.status, res.message)); json.dump(dict(fam=fam, t0='infeasible'), open(ARGV[3], 'w')); sys.exit(0)
        freed = {r for r, v in s.items() if v > 1e-10}
        log('round %d: %d rows get slack, %d left' % (rnd, len(freed), len(cand) - len(freed)))
        if not freed: break
        cand -= freed
    imp = sorted(cand)
    out = dict(fam=fam, n_implicit=len(imp), rows=[(rows[i][0][0], lab_str(rows[i][0])) for i in imp])
    json.dump(out, open(ARGV[3], 'w'), indent=1)
    log('implicit equalities: %d: %s' % (len(imp), collections.Counter(rows[i][0][0] if rows[i][0][0] == 'S' else 'R%d' % rows[i][0][1] for i in imp)))
    for i in imp[:60]: log('   ', lab_str(rows[i][0]))
