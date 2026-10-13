"""Sub-conjecture test (INVARIANTS-1 task 2): on a closed 1212 orbit the A5v bit is constant (= 0).

Closed orbit, word 1212..., Hamiltonian normal form (inv_sat.Enc, axiom OFF), plus an indicator
a5[t] <-> (v's M_t-partner lies on X_t), built from the eager loop variables z[t,u] (which equal loop
membership in every accepted model).  Modes:
  any   : a5[0] or a5[1]      (WLOG by an even time shift: "the orbit has an A5v-true state")
  mixed : (a5[0] or a5[1]) and (some a5[t] false)
  t0    : a5[0] only;  t1 : a5[1] only   (split of 'any')
  P / Q : a 0->1 transition at t = 0 / t = 1 (WLOG split of 'mixed' by an even time shift)
UNSAT for 'any' at (n, L)  =>  every closed 1212 orbit of length L at that n is A5v-false at every state.
Usage: mixed.py n L mode tlimit
"""
import sys, json, time
from inv_sat import Enc, run, to_line

n, L, mode, tl = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], float(sys.argv[4])
enc = Enc(n, L, 0, word='1212', eager=1, closed=True)
P = enc.pool; v = enc.v
a5 = [P.id(('a5', t)) for t in range(L)]
for t in range(L):
    k = enc.k[t]
    for e in enc.vedges:
        a, b = enc.edges[e]; j = b if a == v else a
        z = P.id(('z', t, j))
        enc.add([-enc.lab[k][e], -z, a5[t]])
        enc.add([-enc.lab[k][e], z, -a5[t]])
if len(sys.argv) > 5:  # power control: fix the chord set of a given normal-form line (TrackU format)
    tok = list(map(int, open(sys.argv[5]).read().split()))
    m = tok[1]; ch = set()
    for i in range(m):
        a, b = sorted((tok[2 + 2 * i], tok[3 + 2 * i]))
        if (a, b) in enc.eid and enc.X[enc.eid[(a, b)]] is not None: ch.add(enc.eid[(a, b)])
    for e in range(enc.m):
        if enc.X[e] is not None: enc.add([enc.X[e]] if e in ch else [-enc.X[e]])
import os
if os.environ.get('CUBE'):   # cube: the f_1 chord at v goes to vertex CUBE (ham normal form; exhaustive over CUBE = 2..n-2)
    cj = int(os.environ['CUBE']); enc.add([enc.lab[1][enc.eid[(0, cj)]]])
if mode == 'allfalse': [enc.add([-a5[t]]) for t in range(L)]
if mode in ('any', 'mixed'): enc.add([a5[0], a5[1]])
if mode == 't0': enc.add([a5[0]])
if mode == 'P': enc.add([a5[0]]); enc.add([-a5[L - 1]])   # a 0->1 transition at t = 0
if mode == 'Q': enc.add([a5[1]]); enc.add([-a5[0]])       # a 0->1 transition at t = 1
if mode == 't1': enc.add([a5[1]])
if mode == 'mixed': enc.add([-a5[t] for t in range(L)])
print(f'cube={os.environ.get("CUBE")} n={n} L={L} mode={mode} vars={enc.pool.top} clauses={len(enc.cl)}', flush=True)
st, sols, stats = run(enc, tl, verbose=True)
print(json.dumps(dict(n=n, L=L, mode=mode, status=st, **stats)), flush=True)
for E, M, fv, info in sols:
    print('SOL', to_line(enc, E, fv), info, flush=True)
    # report the A5v pattern with the independent engine
    from ax_lib import G5, parse_line
    g = G5(*parse_line(to_line(enc, E, fv)))
    idx = {e: i for i, e in enumerate(E)}
    pat = []
    for t in range(L):
        Mt = frozenset(idx[e] for e in M[t]); d = g.dl(Mt)
        k, lp = d; fk = g.fv[k]; w = g.other(fk, g.v)
        pat.append(1 if w in lp['X'][2] else 0)
    print('A5v pattern', pat, flush=True)
