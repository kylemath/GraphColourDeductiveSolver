"""A5v / A1 on real sphere data: plantri24 (TrackF) Tait duals at every degree-5 hole, ALL DL-good
perfect matchings (not only orbit states). Also surface seeds (seed_surf.txt). Uses TrackT tt_lib read-only."""
import sys, os, json
from collections import Counter
sys.path.insert(0, os.path.expanduser('~/GraphColour/SolvingFrameworkPlan/docs/working/TrackT'))
import tt_lib
from ax_lib import *
C = Counter()
def check(g):
    P = g.pms()
    for M in P:
        d = g.dl(M)
        if d is None: continue
        C['dl'] += 1
        f = fig8_axioms(g, M, d)
        C['A5v_ok' if f['v_into_X'] else 'A5v_FAIL'] += 1
        C['A5x_ok' if f['xy_cross'] == 0 else 'A5x_FAIL'] += 1
        C['fig8planar_ok' if f['fig8_planar'] else 'fig8planar_FAIL'] += 1
        # Hamiltonian states: P' = the other PM of E-M? H = pred ∪ M with pred the PM of E-M not containing f_{k-2}
        k = d[0]
        for N in P:
            if N & M: continue
            if g.fv[(k + 2) % 5] in N and g.ncomp(N | M) == 1:
                ch, cons = ham_diagram(g, N, M)
                nv, ed = signed_graph(ch, cons)
                C['ham'] += 1; C['A1_ok' if parity_consistent(nv, ed) else 'A1_FAIL'] += 1
mode = sys.argv[1]
if mode == 'sphere':
    stride = int(sys.argv[2])
    G = tt_lib.load_graphs(os.path.expanduser('~/GraphColour/SolvingFrameworkPlan/docs/working/TrackF/graphs/plantri24.txt'))
    names = sorted(G)[::stride]
    for nm in names:
        rot = G[nm]
        for h in range(len(rot)):
            if len(rot[h]) != 5: continue
            td = tt_lib.tait_dual(rot, h)
            g = G5(td.n, list(td.E), list(td.fv)); C['holes'] += 1
            check(g)
else:
    for line in open(sys.argv[2]):
        if line.strip():
            g = G5(*parse_line(line)); C['holes'] += 1; check(g)
print(mode, dict(C))
