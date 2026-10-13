"""R0 relaxation variants (pure SAT, no cuts): planar circle rule with a chosen rotation at v and a chosen
frame advance per step.  R0 = H = M_0 u M_1 Hamiltonian (normal form) + M_0..M_{L-1} perfect matchings,
M_t n M_{t+1} = 0 cyclically, v-edge of M_t = f_{k_t}, k_t = 2 + adv*t (mod 5).
VPOS order/sides: rule 'planar' = circle 1..n-1,[f4],[f1],[f3], side(f1) != side(f3) = side(f4).
usage: relax2.py n L adv rule   (rule in: planar, none, perm:<a><b><c>:<lone>)"""
import sys, time
import sat_planar
from sat_t1v import Enc
from pysat.solvers import Cadical153
n, L, rule = int(sys.argv[1]), int(sys.argv[2]), sys.argv[4]
adv = sys.argv[3][1:] if sys.argv[3].startswith('p') else int(sys.argv[3])
Enc._eager_loops = lambda self: None
orig_init = Enc.__init__
def init(self, *a, **kw):
    orig_init(self, *a, **kw)
Enc.__init__ = init
# frame advance: patch k after construction is too late (used in _eager); patch via subclass
class E2(Enc):
    free_L = True
    def _eager(self):
        self.k = ([int(adv[t % len(adv)]) for t in range(self.L)] if isinstance(adv, str) else [(2 if t % 2 == 0 else 0) for t in range(self.L)] if adv == 99 else [(2 + adv * t) % 5 for t in range(self.L)])
        # f2 in M_0, and M_1's v-edge f_{2+adv} must be (0,n-1): relabel requirement handled below
        Enc._eager(self)
# The base _eager pins lab[2]=(0,1) and lab[0]=(0,n-1); with adv != -2 the M_1 v-edge is f_{2+adv}:
def pin_patch(self):
    pass
t0 = time.time()
if rule == 'none':
    enc = E2(n, L, 0, eager=0, closed=("open" not in sys.argv))
else:
    class P2(E2, sat_planar.PEnc): pass
    if rule.startswith('perm'):
        _, order, lone = rule.split(':')
        sat_planar.VPOS = {int(order[0]): .25, int(order[1]): .5, int(order[2]): .75}
        LONE = int(lone)
        def _pl(self, f=sat_planar.PEnc._planar):
            f(self)
        # rebuild side constraints: replace the default (lone f1) by lone LONE
        old = sat_planar.PEnc._planar
        def newplanar(self):
            nb = len(self.cl); old(self)
            P = self.pool; sl = {s: P.id(('vside', s)) for s in (1, 3, 4)}
            # drop the 4 default side clauses (first 4 clauses added by _planar)
            del self.cl[nb:nb + 4]
            others = [s for s in (1, 3, 4) if s != LONE]
            self.add([sl[LONE], sl[others[0]]]); self.add([-sl[LONE], -sl[others[0]]])
            self.add([-sl[others[0]], sl[others[1]]]); self.add([sl[others[0]], -sl[others[1]]])
        sat_planar.PEnc._planar = newplanar
    enc = sat_planar.PEnc.__new__(P2); P2.__init__(enc, n, L, 0, closed=("open" not in sys.argv))
s = Cadical153(bootstrap_with=enc.cl)
r = s.solve()
print(f'n={n} L={L} adv={adv} rule={rule} -> {"SAT" if r else "UNSAT"} ({time.time()-t0:.1f}s)', flush=True)

if r and '--verify' in sys.argv:
    # independent check of the decoded closed sequence: perfect matchings, consecutive disjointness, frames,
    # Hamiltonian M_0 u M_1, and planarity with the rotation (networkx 5-wheel gadget)
    sys.path.insert(0, '..')
    from ax_lib import G5, parse_line, planar_rot
    from sat_t1v import to_line
    E, M, fv = enc.decode(s.get_model())
    g = G5(*parse_line(to_line(enc, E, fv))); idx = {e: i for i, e in enumerate(E)}
    Ms = [frozenset(idx[e] for e in M[t]) for t in range(L)]
    pm = all(sorted(x for e in Mt for x in g.E[e]) == list(range(n)) for Mt in Ms)
    dis = all(not (Ms[t] & Ms[(t + 1) % L]) for t in range(L))
    fr = [g.kidx(Mt) for Mt in Ms]
    print('verify: PM', pm, 'disjoint', dis, 'frames', fr, 'ham01', g.ncomp(Ms[0] | Ms[1]) == 1, 'planar_rot', planar_rot(g))
