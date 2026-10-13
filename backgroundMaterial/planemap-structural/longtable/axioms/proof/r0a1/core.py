"""Group-level minimal UNSAT core of planar R0 (r0sat.R0Enc, mode r0, closed).  Groups: graph, vrot, planar,
ham, pm<t>, frame<t>, disj<t>.  Deletion-based minimisation over groups.  usage: core.py n L"""
import sys
from pysat.solvers import Glucose4
from r0sat import R0Enc
n, L = int(sys.argv[1]), int(sys.argv[2])
enc = R0Enc(n, L, 'r0', True, True)
names = sorted(enc.groups)
sel = {g: enc.pool.id(('sel', g)) for g in names}
s = Glucose4()
for g in names:
    for c in enc.groups[g]: s.add_clause(c + [-sel[g]])
assert not s.solve(assumptions=[sel[g] for g in names])
core = set(names)
# try to drop groups one at a time (order: frames, disjointness, pms, then others)
order = sorted(names, key=lambda g: (g.rstrip('0123456789') not in ('frame', 'disj', 'pm'), g))
for g in order:
    trial = [sel[h] for h in core if h != g]
    if not s.solve(assumptions=trial): core.discard(g)
print(f'n={n} L={L}: minimal group core ({len(core)} of {len(names)}):', sorted(core, key=lambda x: (x.rstrip("0123456789"), int(x[len(x.rstrip("0123456789")):] or -1))))
