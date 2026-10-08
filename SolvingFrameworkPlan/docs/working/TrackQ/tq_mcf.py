#!/usr/bin/env python3
"""Track Q, Part 1, engine 2: HiGHS on the directed multicommodity-flow (arborescence) model -- an LP-strong exact
formulation, independent of the CP-SAT/MTZ model of tq_arb.py.
For every state t and part P (|P| >= 2, root r = min P): arc variables y_a in [0,1] for both orientations of every
ground edge inside P, in-degree(v) = 1 (v != r), in-degree(r) = 0; for every v != r a unit r->v flow f^v <= y;
x_e = y_uv + y_vu + z^t_e with z >= 0 continuous (non-tree kept edges); x binary.  The y's of an integral x need not
be integral, but feasibility of the flows for every v already means: the support of y (subset of the kept edges)
connects P.  Conversely any connected choice admits an integral y (BFS arborescence).  So min sum x is exact.
usage: tq_mcf.py DATA.json [--target T] [--tlim S] [--lp]"""
import sys, json, time
import numpy as np
RETURN_MODEL = False
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix


def solve_mcf(d, U, parts, target=None, tlim=3000, lp=False):
    m = len(U); nv = d['n'] - 1; base = 3 * nv - 8
    nvar = [m]; lb = [0.0] * m; ub = [1.0] * m; integ = [1] * m
    for k in d['forced']: lb[k] = 1.0
    ri, rj, vv, lo, hi = [], [], [], [], []; nr = [0]
    def var(l, u):
        lb.append(l); ub.append(u); integ.append(0); nvar[0] += 1; return nvar[0] - 1
    rowtag = []; tag = [None]
    def row(ent, l, h):
        for j, c in ent: ri.append(nr[0]); rj.append(j); vv.append(c)
        lo.append(l); hi.append(h); nr[0] += 1; rowtag.append(tag[0])
    L = len(d['cols'])
    xrow = {}  # (t,k) -> list of entries (y/z vars)
    for t in range(L):
        for k in range(m): xrow[(t, k)] = [(k, 1.0)]
    for (t, p, q, P) in parts:
        tag[0] = (t, p, q, len(P))
        r = min(P); ks = [k for k, (a, b) in enumerate(U) if a in P and b in P]
        arcs = []
        for k in ks:
            a, b = U[k]
            ya = var(0, 1); yb = var(0, 1); arcs += [(a, b, ya), (b, a, yb)]
            xrow[(t, k)] += [(ya, -1.0), (yb, -1.0)]
        for v in P:
            row([(y, 1.0) for (a, b, y) in arcs if b == v], 0 if v == r else 1, 0 if v == r else 1)
        for w in P:
            if w == r: continue
            f = [(a, b, y, var(0, 1)) for (a, b, y) in arcs if b != r and a != w]
            for (a, b, y, fv) in f: row([(fv, 1.0), (y, -1.0)], -np.inf, 0)
            for v in P:
                if v == r: continue
                ent = [(fv, 1.0) for (a, b, y, fv) in f if b == v] + [(fv, -1.0) for (a, b, y, fv) in f if a == v]
                rhs = 1 if v == w else 0
                row(ent, rhs, rhs)
    for (t, k), ent in xrow.items():
        tag[0] = (t, 'link', k)
        z = var(0, 1); row(ent + [(z, -1.0)], 0, 0)
    if target is not None: row([(k, 1.0) for k in range(m)], -np.inf, target)
    A = coo_matrix((vv, (ri, rj)), shape=(nr[0], nvar[0])).tocsr()
    c = np.zeros(nvar[0]); c[:m] = 1
    if RETURN_MODEL: return dict(A=A, lo=np.array(lo, float), hi=np.array(hi, float), lb=np.array(lb), ub=np.array(ub), c=c, rowtag=rowtag, m=m, base=base)
    t0 = time.time()
    res = milp(c, constraints=LinearConstraint(A, lo, hi), integrality=np.zeros(nvar[0]) if lp else np.array(integ), bounds=Bounds(np.array(lb), np.array(ub)),
               options=dict(time_limit=tlim, disp=False, mip_rel_gap=0.0))
    out = dict(engine='highs-mcf' + ('-lp' if lp else ''), src=d.get('src'), status=int(res.status), message=str(res.message), secs=round(time.time() - t0, 1),
               nvar=nvar[0], nrow=nr[0], base=base, target=target, dual_bound=getattr(res, 'mip_dual_bound', None), gap=getattr(res, 'mip_gap', None))
    if res.x is not None:
        out['obj'] = float(res.fun) if lp else int(round(res.x[:m].sum())); out['e'] = out['obj'] - base
        if not lp: out['K'] = [U[k] for k in range(m) if res.x[k] > 0.5]
    return out


def main():
    args = sys.argv[1:]; path = args.pop(0); target = None; tlim = 3000; lp = False
    if '--target' in args: k = args.index('--target'); target = int(args[k + 1]); del args[k:k + 2]
    if '--tlim' in args: k = args.index('--tlim'); tlim = float(args[k + 1]); del args[k:k + 2]
    if '--lp' in args: args.remove('--lp'); lp = True
    d = json.load(open(path)); U = [tuple(e) for e in d['U']]; parts = [(t, p, q, frozenset(P)) for t, p, q, P in d['parts']]
    out = solve_mcf(d, U, parts, target, tlim, lp)
    print(json.dumps({k: v for k, v in out.items() if k != 'K'}), flush=True)
    if 'K' in out: print('K', json.dumps(out['K']))


if __name__ == '__main__':
    main()
