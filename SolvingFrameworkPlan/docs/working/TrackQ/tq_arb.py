#!/usr/bin/env python3
"""Track Q, Part 1: compact EXACT models (no lazy cuts) for min |E(G'-h)| under partition-preserving surgery.
Data: out/<name>_data.json from tq_data.py (ground set U, parts (t,p,q,P), forced link edges, colourings).
Model (exact): for every state t, every edge e of U lies inside exactly one part P_t(e) (the part of its colour pair
that contains both ends).  Variables x_e (edge kept), per state t: arc vars a^t_{uv}, a^t_{vu} for each e = uv and
an 'extra' var z^t_e, with x_e = a^t_uv + a^t_vu + z^t_e.  In every part P (root r = min P) every non-root vertex has
exactly one entering arc, the root none, and levels l^t_v in [0,|P|-1] with a^t_uv => l_v >= l_u + 1 (MTZ).
So the arcs form a spanning arborescence of every part (=> the kept edges connect every part), and conversely any
connected choice admits such arcs (BFS tree) with z = the non-tree kept edges.  sum_e z^t_e = B_t (cycle rank at t).
Objective: min sum x  (equivalently e = sum x - (3nv - 8)).  Optional --target T: add sum x <= T (feasibility).
Engines: CP-SAT (ortools) and HiGHS (scipy milp, gap 0).
usage: tq_arb.py DATA.json ENGINE(cpsat|highs) [--target T] [--tlim S] [--workers W] [--hint graphfile]"""
import sys, json, time
import numpy as np


def load(path):
    d = json.load(open(path))
    U = [tuple(e) for e in d['U']]; parts = [(t, p, q, frozenset(P)) for t, p, q, P in d['parts']]
    return d, U, parts


def structure(d, U, parts):
    L = len(d['cols'])
    partof = {}
    for pi, (t, p, q, P) in enumerate(parts):
        for k, (a, b) in enumerate(U):
            if a in P and b in P: partof[(t, k)] = pi
    for t in range(L):
        for k in range(len(U)): assert (t, k) in partof, ('edge outside parts', t, U[k])
    return L, partof




def build_common(d, U, parts):
    """index structures: for each state t, for each edge k: part id; arcs list."""
    L, partof = structure(d, U, parts)
    return L, partof


def cpsat(d, U, parts, target=None, tlim=3000, workers=4, hint=None, objective=True):
    from ortools.sat.python import cp_model
    L, partof = build_common(d, U, parts)
    md = cp_model.CpModel(); m = len(U)
    x = [md.NewBoolVar('x%d' % k) for k in range(m)]
    for k in d['forced']: md.Add(x[k] == 1)
    zs = []
    for t in range(L):
        lev = {}; inn = {}
        for pi, (tt, p, q, P) in enumerate(parts):
            if tt != t: continue
            for v in P: lev[(pi, v)] = md.NewIntVar(0, len(P) - 1, ''); inn[(pi, v)] = []
            md.Add(lev[(pi, min(P))] == 0)
        for k, (u, v) in enumerate(U):
            pi = partof[(t, k)]
            a = md.NewBoolVar(''); b = md.NewBoolVar(''); z = md.NewBoolVar(''); zs.append((t, z))
            md.Add(x[k] == a + b + z)
            inn[(pi, v)].append(a); inn[(pi, u)].append(b)
            md.Add(lev[(pi, v)] >= lev[(pi, u)] + 1).OnlyEnforceIf(a)
            md.Add(lev[(pi, u)] >= lev[(pi, v)] + 1).OnlyEnforceIf(b)
        for (pi, v), arcs in inn.items():
            P = parts[pi][3]
            if v == min(P): md.Add(sum(arcs) == 0)
            else: md.Add(sum(arcs) == 1)
    tot = sum(x)
    if target is not None: md.Add(tot <= target)
    if objective: md.Minimize(tot)
    if hint is not None:
        for k in range(m): md.AddHint(x[k], int(hint[k]))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tlim; s.parameters.num_search_workers = workers
    s.parameters.log_search_progress = False
    t0 = time.time(); st = s.Solve(md)
    out = dict(engine='cpsat', status=s.StatusName(st), secs=round(time.time() - t0, 1), wall=s.WallTime())
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        out['obj'] = int(sum(s.Value(xx) for xx in x)); out['bound'] = s.BestObjectiveBound() if objective else None
        out['K'] = [U[k] for k in range(m) if s.Value(x[k])]
    return out


def highs(d, U, parts, target=None, tlim=3000):
    from scipy.optimize import milp, LinearConstraint, Bounds
    from scipy.sparse import coo_matrix
    L, partof = build_common(d, U, parts)
    m = len(U); nvar = m
    lb = []; ub = []; integ = []
    def newvar(l, u, i):
        nonlocal nvar
        lb.append(l); ub.append(u); integ.append(i); nvar += 1; return nvar - 1
    for k in range(m): pass
    xlb = np.zeros(m); xlb[d['forced']] = 1
    lb = list(xlb); ub = [1.0] * m; integ = [1] * m
    R = []; lo = []; hi = []
    def row(ent, l, h): R.append(ent); lo.append(l); hi.append(h)
    for t in range(L):
        lev = {}; inn = {}
        for pi, (tt, p, q, P) in enumerate(parts):
            if tt != t: continue
            for v in P:
                lev[(pi, v)] = newvar(0, 0 if v == min(P) else len(P) - 1, 0); inn[(pi, v)] = []
        for k, (u, v) in enumerate(U):
            pi = partof[(t, k)]; M = len(parts[pi][3])
            a = newvar(0, 1, 1); b = newvar(0, 1, 1); z = newvar(0, 1, 1)
            row([(k, 1), (a, -1), (b, -1), (z, -1)], 0, 0)
            inn[(pi, v)].append(a); inn[(pi, u)].append(b)
            # l_v - l_u >= 1 - M(1-a)  <=>  l_v - l_u - M a >= 1 - M
            row([(lev[(pi, v)], 1), (lev[(pi, u)], -1), (a, -M)], 1 - M, np.inf)
            row([(lev[(pi, u)], 1), (lev[(pi, v)], -1), (b, -M)], 1 - M, np.inf)
        for (pi, v), arcs in inn.items():
            P = parts[pi][3]; rhs = 0 if v == min(P) else 1
            row([(a, 1) for a in arcs], rhs, rhs)
    if target is not None: row([(k, 1) for k in range(m)], -np.inf, target)
    ri = []; rj = []; vv = []
    for r, ent in enumerate(R):
        for j, c in ent: ri.append(r); rj.append(j); vv.append(c)
    A = coo_matrix((vv, (ri, rj)), shape=(len(R), nvar)).tocsr()
    c = np.zeros(nvar); c[:m] = 1
    t0 = time.time()
    res = milp(c, constraints=LinearConstraint(A, lo, hi), integrality=np.array(integ), bounds=Bounds(np.array(lb), np.array(ub)),
               options=dict(time_limit=tlim, disp=False, mip_rel_gap=0.0))
    out = dict(engine='highs', status=int(res.status), message=str(res.message), secs=round(time.time() - t0, 1),
               dual_bound=getattr(res, 'mip_dual_bound', None), gap=getattr(res, 'mip_gap', None), nvar=nvar, nrow=len(R))
    if res.x is not None:
        out['obj'] = int(round(res.x[:m].sum())); out['K'] = [U[k] for k in range(m) if res.x[k] > 0.5]
    return out


if __name__ == '__main__':
    args = sys.argv[1:]; path = args.pop(0); eng = args.pop(0)
    target = None; tlim = 3000; workers = 4
    if '--target' in args: k = args.index('--target'); target = int(args[k + 1]); del args[k:k + 2]
    if '--tlim' in args: k = args.index('--tlim'); tlim = float(args[k + 1]); del args[k:k + 2]
    if '--workers' in args: k = args.index('--workers'); workers = int(args[k + 1]); del args[k:k + 2]
    d, U, parts = load(path)
    hint = None
    Eo = {tuple(e) for e in d['E']}; hint = [1 if e in Eo else 0 for e in U]
    base = 3 * (d['n'] - 1) - 8
    r = cpsat(d, U, parts, target, tlim, workers, hint) if eng == 'cpsat' else highs(d, U, parts, target, tlim)
    r['base'] = base; r['e'] = (r['obj'] - base) if 'obj' in r else None; r['src'] = d.get('src', path); r['target'] = target
    print(json.dumps({k: v for k, v in r.items() if k != 'K'}), flush=True)
    if 'K' in r: print('K', json.dumps(r['K']))
