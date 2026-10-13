"""Coordinator test (invariants agent, item 2): is R0 UNSAT under ONLY the chord-order condition at the
Hamiltonian state, with no other planarity?  At the Ham state (M0, M1) (frame k = 0 at t = 1: e2 = f0, e4 = f2,
e0 = f3, e1 = f4, e3 = f1; frame numbering p = n - (normal-form position)), "e1 before e0" means
pos(f3 end) < pos(f4 end) in the normal form.  Variants:
  order      : no crossing clauses, only pos(f3) < pos(f4)
  order_rev  : no crossing clauses, only pos(f3) > pos(f4) (the T1 order)
  nest       : order + f1's end strictly between them (e3 nested)  /  out: f1 end outside [f3, f4]
usage: order_test.py n L"""
import sys, time
from pysat.solvers import Glucose4
from r0sat import R0Enc
n, L = int(sys.argv[1]), int(sys.argv[2])
def run(tag, rel):
    enc = R0Enc(n, L, 'r0', False, True)
    P = lambda s, j: enc.pres[('v%d' % s, 0, j)]
    cl = enc.clauses()
    J = range(2, n - 1)
    for a in J:
        for b in J:
            for c in J:
                if len({a, b, c}) == 3 and not rel(a, b, c):   # a = pos f3, b = pos f4, c = pos f1
                    cl.append([-P(3, a), -P(4, b), -P(1, c)])
    t0 = time.time(); s = Glucose4(bootstrap_with=cl); r = s.solve()
    print(f'n={n} L={L} {tag}: {"SAT" if r else "UNSAT"} ({time.time()-t0:.1f}s)', flush=True)
run('order (f3 < f4)', lambda a, b, c: a < b)
run('order_rev (f3 > f4)', lambda a, b, c: a > b)
run('order + f1 between', lambda a, b, c: a < c < b)
run('order + f1 outside', lambda a, b, c: a < b and not a < c < b)
