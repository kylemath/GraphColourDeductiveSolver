"""Among enumerated A5v windows: which also satisfy A1-local (e0,e1 uncrossed) at every Hamiltonian state,
and which are planar with the rotation at v (ax_lib.planar_rot)?"""
import sys, json
sys.path.insert(0, '..')
from ax_lib import G5, planar_rot
from win_lib import load
for path in sys.argv[1:]:
    ws = load(path); a1 = 0; pl = 0; both = 0
    for w in ws:
        ok = all(w.ham_positions(t)[2][1] < w.ham_positions(t)[2][0] for t in range(1, w.W, 2))
        E = w.E; idx = {tuple(sorted(e)): i for i, e in enumerate(E)}
        g = G5(w.n, E, [idx[tuple(sorted(e))] for e in w.fv]); p = planar_rot(g)
        a1 += ok; pl += p; both += ok and p
    print(path, 'windows', len(ws), 'A1-local at all Ham states', a1, 'planar', pl)
