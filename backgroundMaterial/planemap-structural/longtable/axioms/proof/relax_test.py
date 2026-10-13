"""Which part of the eager encoding makes planar closed L=10 orbits impossible?  Pure SAT on the eager clauses
(no CEGAR cuts: no connectivity of E - M_t, no word letters except the fixed Hamiltonian H = M_0 u M_1).
Levels: R0 = graph + perfect matchings + consecutive disjointness + frames (v-edge of M_t is f_{2-2t});
R1 = R0 + z-propagation along E - M_t with frame-forced ends (forces the DL pairing on the v-component);
R2 = R1 + |z^{-1}(1)| even; R3 = R2 + A5v (z(partner) = 1).  Planarity clauses on/off.
usage: relax_test.py n L level planar(0/1) [anti]"""
import sys, time
import sat_t1v
from sat_planar import PEnc
from sat_t1v import Enc
from pysat.solvers import Cadical153

n, L, level, planar = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
axv = 2 if 'anti' in sys.argv else 1
orig = Enc._eager_loops
def patched(self):
    if level == 0: return
    keep = []
    before = len(self.cl)
    orig(self)
    new = self.cl[before:]
    # identify clause kinds by variables: rebuild selectively
    del self.cl[before:]
    P = self.pool
    for c in new:
        self.cl.append(c)
    if level < 3:
        # remove A5v unit implications: clauses [-lab[k_t][e], +/- z[t][j]] of length 2 with a lab literal
        labs = {self.lab[s][e] for s in range(5) for e in self.vedges}
        self.cl = self.cl[:before] + [c for c in self.cl[before:] if not (len(c) == 2 and -c[0] in labs)]
    if level < 2:
        # remove parity chain (clauses on 'par' vars and the final unit)
        parv = {v for k, v in P.obj2id.items() if isinstance(k, tuple) and k and k[0] == 'par'}
        self.cl = self.cl[:before] + [c for c in self.cl[before:] if not any(abs(x) in parv for x in c)
                                      and not (len(c) == 1)]
Enc._eager_loops = patched
t0 = time.time()
enc = PEnc(n, L, axv, closed=True, word='1212') if planar else Enc(n, L, axv, eager=1, closed=True)
s = Cadical153(bootstrap_with=enc.cl)
r = s.solve()
print(f'n={n} L={L} level=R{level} planar={planar} axv={axv} -> {"SAT" if r else "UNSAT"} ({time.time()-t0:.1f}s)', flush=True)
