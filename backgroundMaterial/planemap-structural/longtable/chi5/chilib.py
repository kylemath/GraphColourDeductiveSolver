"""chi5 library (Studio Job 6, 13 Oct 2026, exploratory): exact 4-colourability by SAT, graph-line I/O, and the
non-4-colourable seed triangulations used by the walks.

A triangulation is handled as TrackF does (`TrackF/src/surfaces.py`): a face list of 3-tuples, or a graph line
'name n r0;r1;...' (r_v = cyclic link of v).
"""
import os, sys, itertools
from pysat.solvers import Cadical153

TRACKF = '/Users/kylemathewson/GraphColourDeductiveSolver/SolvingFrameworkPlan/docs/working/TrackF'
sys.path.insert(0, os.path.join(TRACKF, 'src'))
import surfaces  # noqa: E402  (read-only reuse: Tri, validate, orientable, link_cycle, to_line, connected_sum, RP2_6)


def read_line(l):
    p = l.split()
    return p[0], [[int(x) for x in r.split(',')] for r in p[2].split(';')]


def adj_of_rot(rot):
    return [set(r) for r in rot]


def colourable(adj, k=4, skip=None):
    """exact k-colourability of the graph (adjacency sets) with vertex `skip` deleted; returns a colouring or None"""
    n = len(adj); V = [v for v in range(n) if v != skip]
    var = lambda v, c: v * k + c + 1
    s = Cadical153()
    for v in V:
        s.add_clause([var(v, c) for c in range(k)])
    for v in V:
        for w in adj[v]:
            if w > v and w != skip:
                for c in range(k): s.add_clause([-var(v, c), -var(w, c)])
    # symmetry: fix the colours of one edge (or one vertex)
    v0 = V[0]; s.add_clause([var(v0, 0)])
    nb = [w for w in adj[v0] if w != skip]
    if nb: s.add_clause([var(nb[0], 1)])
    ok = s.solve()
    col = None
    if ok:
        m = set(x for x in s.get_model() if x > 0)
        col = {v: next(c for c in range(k) if var(v, c) in m) for v in V}
    s.delete()
    return col


def chi_at_most(adj, k):
    return colourable(adj, k) is not None


def chromatic(adj, kmax=8):
    for k in range(1, kmax + 1):
        if colourable(adj, k) is not None: return k
    return None


# ---------------- non-4-colourable seeds ----------------

def k7_torus():
    """K7 on the torus (Moebius-Kantor / Heawood): faces (i, i+1, i+3) and (i, i+2, i+3) mod 7"""
    F = []
    for i in range(7):
        F.append((i, (i + 1) % 7, (i + 3) % 7)); F.append((i, (i + 2) % 7, (i + 3) % 7))
    return 7, F


def k6_rp2():
    return 6, list(surfaces.RP2_6)


def seeds(rng):
    """(surface, chi_euler, n, F) non-4-colourable starting triangulations"""
    T7 = k7_torus(); P6 = k6_rp2()
    out = [('torus', 0) + T7, ('rp2', 1) + P6]
    out.append(('klein', 0) + surfaces.connected_sum(P6, P6, rng))
    out.append(('genus2', -2) + surfaces.connected_sum(T7, T7, rng))
    out.append(('rp2x3', -1) + surfaces.connected_sum(surfaces.connected_sum(P6, P6, rng), P6, rng))
    out.append(('rp2x3', -1) + surfaces.connected_sum(T7, P6, rng))   # torus # RP2 = N3
    for s, chi, n, F in out:
        assert surfaces.validate(n, F, chi) is None, (s, surfaces.validate(n, F, chi))
        assert surfaces.orientable(F) == (s in ('torus', 'genus2')), s
    return out


def rot_of(n, F):
    return [surfaces.link_cycle(F, v) for v in range(n)]


def good_holes(rot, adj=None):
    """degree-5 vertices h with T - h 4-colourable (T itself assumed non-4-colourable)"""
    adj = adj or adj_of_rot(rot)
    return [h for h in range(len(rot)) if len(rot[h]) == 5 and colourable(adj, 4, skip=h) is not None]
