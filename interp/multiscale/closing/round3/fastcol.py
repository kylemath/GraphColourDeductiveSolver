# level colouring of a side: Cadical on the depth<=Wb band (diversified by random colours forced on a few
# random band vertices, dropped if UNSAT), then 4-colour the interior with depth<=Wb-3 fixed.
import sys
sys.path.insert(0,'/mnt/project-files/multiscale/closing/round2')
from band import *
from pysat.solvers import Cadical153
def fast_level_col(T, cl, rng, t=None, dep=None, Wb=8, nrand=6, extend=True):
    if dep is None: dep = depth(T, cl)
    band = [v for v in cl.verts if dep[v] <= Wb]; bs = set(band)
    enc = CNF(band)
    for u, w in cl.edges:
        if u in bs and w in bs: enc.neq(u, w)
    enc.level(cl, 1.0, t=t)
    s = Cadical153(bootstrap_with=enc.cls)
    for tries in range(4):
        k = max(0, nrand - 2*tries)
        ass = [enc.x(v, rng.randrange(4)) for v in rng.sample(band, k)]
        if s.solve(assumptions=ass): break
    else:
        s.delete(); return None
    mod = set(l for l in s.get_model() if l > 0); s.delete()
    r = {v: next(c for c in range(4) if enc.x(v, c) in mod) for v in enc.verts}
    if not extend: return r   # band-only colouring (depth <= Wb); interior extension NOT checked
    keep = {v: c for v, c in r.items() if dep[v] <= Wb-3}
    rest = [v for v in cl.verts if v not in keep]; rs = set(rest)
    e2 = CNF(rest)
    for u, w in cl.edges:
        if u in rs and w in rs: e2.neq(u, w)
        elif u in rs: e2.cls.append([-e2.x(u, keep[w])])
        elif w in rs: e2.cls.append([-e2.x(w, keep[u])])
    r2 = e2.solve()
    if not r2: return 'EXTFAIL'
    col = dict(keep); col.update(r2); return col
if __name__ == '__main__':
    import e1util
    F = int(sys.argv[1]); rng = random.Random(1)
    T = Tri(e1util.base('ico%d' % F)); n = len(T.adj)
    poles = [v for v in range(n) if T.deg[v] == 5]
    A, r = smooth(T, grow(T, poles[0], n//2, rng), rng); cA, cB = r
    for i in range(3):
        t0 = time.time(); c = fast_level_col(T, cA, rng)
        H = cA.walk_heights(c); print(F, H[-1], cA.tau(c), round(time.time()-t0, 1), flush=True)
