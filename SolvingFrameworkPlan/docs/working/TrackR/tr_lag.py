#!/usr/bin/env python3
"""Track R: Lagrangian (edge-price) form of the TrackQ flow-LP dual, solved exactly by Kelley cutting planes on
spanning trees, with exact rational re-verification.

Certificate form [elementary, any graph].  Data: states t (colourings), for every t the parts P (vertex sets of the
pair-graph components, |P| >= 2), ground set U (pairs admissible at every state), forced edges F (link 5-cycle).
A price matrix u_{t,e} >= 0 (e in U) with sum_t u_{t,e} <= 1 for e notin F gives, for every G' carrying the data,
   |E(G'-h)|  >=  sum_t sum_P MST_P(u_t)  +  sum_{e in F} (1 - sum_t u_{t,e})                       (*)
because x = 1_{E(G')} satisfies sum_e x_e >= sum_{t,e} u_{t,e} x_e + sum_F(1 - sum_t u) and, at each t, E(G') contains a
spanning tree of every part (parts of one state are disjoint).  By LP duality / integrality of the spanning-tree
dominant, max over u of the right side equals the TrackQ mcf LP value.
usage: tr_lag.py DATA.json [--window S,K (local ground set) | --gwindow S,K (global ground set)] [--norm l1|none] [--out FILE.json]
"""
import sys, os, json, time, itertools
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'TrackQ'))
from tq_exact import build  # read-only reuse


def load(path, window=None, gwindow=None):
    d = json.load(open(path)); n = d['n']; cols = d['cols']; L = len(cols)
    if gwindow is not None:   # global ground set, connectivity only at the window states
        s, k = gwindow; W = [(s + i) % L for i in range(k)]; idx = {t: i for i, t in enumerate(W)}
        U = [tuple(e) for e in d['U']]; forced = d['forced']
        parts = [(idx[t], p, q, frozenset(P)) for t, p, q, P in d['parts'] if t in idx]
    elif window is None:
        U = [tuple(e) for e in d['U']]; parts = [(t, p, q, frozenset(P)) for t, p, q, P in d['parts']]; forced = d['forced']; W = list(range(L))
    else:
        s, k = window; W = [(s + i) % L for i in range(k)]
        E = {frozenset(e) for e in d['E']}
        U, parts, forced = build(n, E, [cols[i] for i in W])
    return dict(src=d['src'], n=n, cols=[cols[i] for i in W], W=W, U=U, parts=parts, forced=list(forced), Nprof=''.join(d['Nprof'][i] for i in W), E=d['E'])


def part_edges(U, parts):
    """for every part index: list of ground-edge indices inside it"""
    pos = {}
    out = []
    for i, (t, p, q, P) in enumerate(parts):
        out.append([k for k, (a, b) in enumerate(U) if a in P and b in P])
    return out


def mst(P, U, ks, w):
    """Kruskal: returns (weight, tree edge list) of a min spanning tree of part P using ground edges ks with weights w[k]"""
    par = {v: v for v in P}
    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    tot = 0; T = []
    for k in sorted(ks, key=lambda k: w[k]):
        a, b = U[k]; ra, rb = f(a), f(b)
        if ra != rb: par[ra] = rb; tot += w[k]; T.append(k)
    assert len(T) == len(P) - 1, 'part not connected in U'
    return tot, T


def verify(D, u):
    """exact check of (*) for rational prices u[(t,k)] -> Fraction; returns lower bound on |E(G'-h)|"""
    U, parts, forced = D['U'], D['parts'], set(D['forced'])
    L = len(D['cols']); m = len(U)
    col = [sum((u.get((t, k), Fraction(0)) for t in range(L)), Fraction(0)) for k in range(m)]
    for k in range(m):
        assert all(u.get((t, k), 0) >= 0 for t in range(L))
        if k not in forced: assert col[k] <= 1, ('column sum > 1', k, col[k])
    PE = part_edges(U, parts); tot = Fraction(0)
    for i, (t, p, q, P) in enumerate(parts):
        w = {k: u.get((t, k), Fraction(0)) for k in PE[i]}
        tot += mst(P, U, PE[i], w)[0]
    tot += sum((1 - col[k] for k in forced), Fraction(0))
    return tot


def solve(D, norm='l1', verbose=True, maxit=4000, tol=1e-7):
    U, parts, forced = D['U'], D['parts'], set(D['forced'])
    L = len(D['cols']); m = len(U); nP = len(parts)
    PE = part_edges(U, parts)
    # variables: u_{t,k} for k in some part at state t (always true) -> index t*m+k ; then w_i
    nu = L * m; nvar = nu + nP
    def ui(t, k): return t * m + k
    # objective (maximise): sum w + sum_F (1 - sum_t u)  -> minimise -sum w + sum_F sum_t u
    c = np.zeros(nvar); c[nu:] = -1.0
    for k in forced:
        for t in range(L): c[ui(t, k)] += 1.0
    const = float(len(forced))
    # column sums
    Ari, Arj, Arv, b = [], [], [], []; nr = 0
    for k in range(m):
        if k in forced: continue
        for t in range(L): Ari.append(nr); Arj.append(ui(t, k)); Arv.append(1.0)
        b.append(1.0); nr += 1
    base_rows = nr
    cuts = []  # (part i, tree edge list)
    seen = set()
    def add_tree(i, T):
        key = (i, tuple(sorted(T)))
        if key in seen: return False
        seen.add(key); cuts.append(key); return True
    for i in range(nP):
        add_tree(i, mst(parts[i][3], U, PE[i], {k: 0 for k in PE[i]})[1])
    bounds = [(0, 1)] * nu + [(None, None)] * nP

    def lp(cvec, extra=None):
        ri, rj, rv, bb = list(Ari), list(Arj), list(Arv), list(b); r = base_rows
        for (i, T) in cuts:   # w_i - sum_{k in T} u_{t,k} <= 0
            t = parts[i][0]
            ri.append(r); rj.append(nu + i); rv.append(1.0)
            for k in T: ri.append(r); rj.append(ui(t, k)); rv.append(-1.0)
            bb.append(0.0); r += 1
        if extra is not None:
            ri += [r] * len(extra[0]); rj += list(extra[0]); rv += list(extra[1]); bb.append(extra[2]); r += 1
        A = coo_matrix((rv, (ri, rj)), shape=(r, nvar)).tocsr()
        res = linprog(cvec, A_ub=A, b_ub=np.array(bb), bounds=bounds, method='highs')
        assert res.status == 0, res.message
        return res

    def round_loop(cvec, extra=None, label=''):
        it = 0; t0 = time.time()
        while True:
            it += 1
            res = lp(cvec, extra); x = res.x; new = 0; lb = const - sum(x[ui(t, k)] for k in forced for t in range(L))
            for i, (t, p, q, P) in enumerate(parts):
                w = {k: x[ui(t, k)] for k in PE[i]}
                val, T = mst(P, U, PE[i], w); lb += val
                if val < x[nu + i] - tol:
                    new += add_tree(i, T)
            ub = -res.fun + const if extra is None else None
            if verbose and (it % 20 == 0 or new == 0):
                print('  %s it %d cuts %d LB(u) %.6f %s new %d %.1fs' % (label, it, len(cuts), lb - const + const, ('UB %.6f' % ub) if ub is not None else '', new, time.time() - t0), flush=True)
            if new == 0 or it >= maxit: return x, lb
    x, lb = round_loop(c, None, 'max')
    opt = lb
    if norm == 'l1':
        # among optimal duals minimise total price sum_{t,k} u (sparsest-ish), keeping value >= opt
        c2 = np.zeros(nvar); c2[:nu] = 1.0
        # constraint: -(sum w - sum_F sum_t u) <= -(opt - const) + 1e-7
        idx = list(range(nu, nvar)) + [ui(t, k) for k in forced for t in range(L)]
        vals = [-1.0] * nP + [1.0] * (len(forced) * L)
        x, lb = round_loop(c2, (idx, vals, -(opt - const) + 1e-6), 'l1')
    u = {}
    for t in range(L):
        for k in range(m):
            if x[ui(t, k)] > 1e-9: u[(t, k)] = Fraction(x[ui(t, k)]).limit_denominator(60)
    return opt, u


def main():
    a = sys.argv[1:]; path = a.pop(0); window = None; norm = 'l1'; out = None
    if '--window' in a: i = a.index('--window'); window = tuple(int(z) for z in a[i + 1].split(',')); del a[i:i + 2]
    gw = None
    if '--gwindow' in a: i = a.index('--gwindow'); gw = tuple(int(z) for z in a[i + 1].split(',')); del a[i:i + 2]
    if '--norm' in a: i = a.index('--norm'); norm = a[i + 1]; del a[i:i + 2]
    if '--out' in a: i = a.index('--out'); out = a[i + 1]; del a[i:i + 2]
    D = load(path, window, gw); base = 3 * (D['n'] - 1) - 8
    print('src', D['src'], 'W', D['W'], 'U', len(D['U']), 'parts', len(D['parts']), 'base', base, flush=True)
    opt, u = solve(D, norm)
    ex = verify(D, u)
    print('LP opt %.6f  e_LP %.6f ; rational certificate bound %s = %.6f (e >= %s)' % (opt, opt - base, ex, float(ex), ex - base))
    if out:
        json.dump(dict(src=D['src'], W=D['W'], glob=gw is not None, base=base, opt=opt, cert=str(ex), u=[[t, k, str(v)] for (t, k), v in sorted(u.items())]), open(out, 'w'))


if __name__ == '__main__':
    main()
