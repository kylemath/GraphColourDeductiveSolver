# fast exact check of which translations t are band-feasible: Cadical on the depth<=Wb band, colour symmetry broken
# by fixing one boundary edge's colours (0,1). Band-UNSAT implies full-UNSAT (band = subset of constraints).
import sys
sys.path.insert(0,'/mnt/project-files/multiscale/closing/round2')
from band import *
from pysat.solvers import Cadical153
def band_feasible(T, cl, t, Wb=6, dep=None, tlimit=None):
    if dep is None: dep = depth(T, cl)
    bs = set(v for v in cl.verts if dep[v] <= Wb)
    enc = CNF(sorted(bs))
    for u, w in cl.edges:
        if u in bs and w in bs: enc.neq(u, w)
    enc.level(cl, 1.0, t=t)
    u0, w0 = cl.walk[0], cl.walk[1]
    enc.fix(u0, 0); enc.fix(w0, 1)
    s = Cadical153(bootstrap_with=enc.cls); ok = s.solve(); s.delete(); return ok
if __name__ == '__main__':
    import e1util
    F = int(sys.argv[1]); Wb = int(sys.argv[2]); rng = random.Random(1)
    T = Tri(e1util.base('ico%d' % F)); n = len(T.adj)
    poles = [v for v in range(n) if T.deg[v] == 5]
    A, r = smooth(T, grow(T, poles[0], n//2, rng), rng); cA, cB = r
    for t in [(0, 0)]:
        t0 = time.time(); print(F, Wb, t, band_feasible(T, cA, t, Wb), round(time.time()-t0, 1), flush=True)
