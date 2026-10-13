"""Enumerate all (graph, window) solutions of the open-window problem (sat_window.py) with blocking
clauses on the graph (chord set + v-labels).  INVARIANTS-1, Long Table, 13 Oct 2026.

In the Hamiltonian normal form (inv_sat.py = copy of ../sat_t1v.py) the window M_0..M_{W-1} is
determined by (chords, labels f1,f3,f4) because the successor rule is deterministic, so blocking the
graph blocks exactly that solution.  Different start positions of one longer run give different
normal forms; dedup to (graph, maximal run) happens in runs.py.

Usage: enum_win.py n W axv(0|1|2) cap tlimit out.jsonl
"""
import sys, json, time
from inv_sat import Enc, to_line
from pysat.solvers import Cadical153

n, W, axv, cap, tl, outp = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]), sys.argv[6]
enc = Enc(n, W, axv, word='1212', eager=1, closed=False)
s = Cadical153(bootstrap_with=enc.cl)
t0 = time.time(); it = 0; nsol = 0; status = None
out = open(outp, 'w')
while True:
    if time.time() - t0 > tl: status = 'TIMEOUT'; break
    if nsol >= cap: status = 'CAP'; break
    if not s.solve(): status = 'UNSAT(exhausted)'; break
    it += 1
    E, M, fv = enc.decode(s.get_model())
    cuts, info = enc.check(E, M, fv)
    if cuts:
        for c in cuts: s.add_clause(c)
        continue
    nsol += 1
    idx = {e: i for i, e in enumerate(E)}
    out.write(json.dumps(dict(n=n, W=W, axv=axv, line=to_line(enc, E, fv),
                              M=[sorted(idx[e] for e in M[t]) for t in range(W)], word=info['word'])) + '\n')
    out.flush()
    blk = [-enc.X[e] for e in E if enc.X[e] is not None]
    blk += [-enc.lab[sl][fv[sl]] for sl in (1, 3, 4)]
    s.add_clause(blk)
s.delete()
print(json.dumps(dict(n=n, W=W, axv=axv, status=status, sols=nsol, iters=it, sec=round(time.time() - t0, 1))), flush=True)
