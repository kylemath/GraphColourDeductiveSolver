#!/usr/bin/env python3
"""Track N: flow formulation of the tn_forest.py ILP (single MILP solve, no lazy cuts), used for the --add ground set.
Variables: x_e (binary, e in ground), per state s and arc (u->v) of an edge whose colour pair is a pair graph at s:
flow f_{s,uv} >= 0; per (s, pair, component C, |C|>=2) root r = min C: r emits |C|-1, every other vertex of C absorbs 1,
f_{s,uv} + f_{s,vu} <= (|C|-1) x_e.  (233) rows with slacks d+ - d-; objective min sum(d+ + d-) (+ tiny random).
Returns (mindev, K)."""
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix
from tn_forest import MT, PAIRS, components


def solve_flow(n, E, cols, ground, tlim=300, seed=0, lp=False):
    nv = n - 1; m = len(ground)
    link = {frozenset((t, t % 5 + 1)) for t in range(1, 6)}
    Eo = [tuple(sorted(e)) for e in E]
    nvar = m; rows_i = []; rows_j = []; vals = []; lo = []; hi = []; r = 0
    def addrow(entries, l, h):
        nonlocal r
        for j, v in entries: rows_i.append(r); rows_j.append(j); vals.append(v)
        lo.append(l); hi.append(h); r += 1
    slack0 = None
    flowvars = []  # (state, edge k) -> var index of u->v ; +1 for v->u
    fidx = {}
    for si, c in enumerate(cols):
        for k, (u, v) in enumerate(ground):
            fidx[(si, k)] = nvar; nvar += 2
    nslack0 = nvar
    for si, c in enumerate(cols):
        lm = [0, 0, 0]
        for t in range(1, 6): lm[MT[c[t]][c[t % 5 + 1]]] += 1
        for mm in range(3):
            ent = [(k, 1) for k, (u, v) in enumerate(ground) if MT[c[u]][c[v]] == mm]
            ent += [(nvar, 1), (nvar + 1, -1)]; nvar += 2
            t = nv - 1 - (5 - lm[mm]) // 2
            addrow(ent, t, t)
    nslack1 = nvar
    bigM = {}
    for si, c in enumerate(cols):
        for (p, q) in PAIRS:
            V = [v for v in range(1, n) if c[v] in (p, q)]
            for C in components(V, [e for e in Eo if c[e[0]] in (p, q) and c[e[1]] in (p, q)]):
                if len(C) < 2: continue
                root = min(C)
                ks = [k for k, (a, b) in enumerate(ground) if a in C and b in C]
                for k in ks: bigM[(si, k)] = len(C) - 1
                for v in C:
                    ent = []
                    for k in ks:
                        a, b = ground[k]; fv = fidx[(si, k)]
                        if a == v: ent += [(fv, -1), (fv + 1, 1)]   # out a->b is fv ; in b->a is fv+1
                        elif b == v: ent += [(fv, 1), (fv + 1, -1)]
                    d = -(len(C) - 1) if v == root else 1
                    addrow(ent, d, d)   # inflow - outflow = demand
    for (si, k), M in bigM.items():
        fv = fidx[(si, k)]; addrow([(fv, 1), (fv + 1, 1), (k, -M)], -np.inf, 0)
    A = coo_matrix((vals, (rows_i, rows_j)), shape=(r, nvar)).tocsr()
    lb = np.zeros(nvar); ub = np.full(nvar, np.inf); ub[:m] = 1
    for k, e in enumerate(ground):
        if frozenset(e) in link: lb[k] = 1
    # flow vars of (state, edge) pairs not inside any component get ub 0
    for (si, k), fv in fidx.items():
        if (si, k) not in bigM: ub[fv] = 0; ub[fv + 1] = 0
    rng = np.random.default_rng(seed)
    cobj = np.zeros(nvar); cobj[nslack0:nslack1] = 1; cobj[:m] = rng.random(m) * 1e-3
    integ = np.zeros(nvar)
    if not lp: integ[:m] = 1
    res = milp(cobj, constraints=LinearConstraint(A, lo, hi), integrality=integ, bounds=Bounds(lb, ub), options=dict(time_limit=tlim, disp=False))
    if res.x is None: return None, None, res.message
    x = np.round(res.x[:m]).astype(int)
    dev = float(res.x[nslack0:nslack1].sum()) if lp else int(round(res.x[nslack0:nslack1].sum()))
    if lp: return dev, None, res.message
    return dev, [ground[k] for k in range(m) if x[k]], res.message


def addable(n, E, cols):
    """non-edges xy (not link-link), properly coloured at every state and inside one component of their pair graph at
    every state (adding never merges components)."""
    Eo = [tuple(sorted(e)) for e in E]; compid = []
    for c in cols:
        d = {}
        for (p, q) in PAIRS:
            V = [v for v in range(1, n) if c[v] in (p, q)]
            for k, C in enumerate(components(V, [e for e in Eo if c[e[0]] in (p, q) and c[e[1]] in (p, q)])):
                for v in C: d[(p, q, v)] = k
        compid.append(d)
    out = []
    for x in range(1, n):
        for y in range(x + 1, n):
            if frozenset((x, y)) in E or (x <= 5 and y <= 5): continue
            ok = True
            for c, d in zip(cols, compid):
                if c[x] == c[y]: ok = False; break
                pq = tuple(sorted((c[x], c[y])))
                if d[pq + (x,)] != d[pq + (y,)]: ok = False; break
            if ok: out.append((x, y))
    return out
