"""Minimal obstructing collars.  Given a disc (adj,S,col,bd), collar width w and window target k0 that is UNSAT,
delete vertices (deepest first, then collar vertices) from S while the target stays UNSAT; the boundary stays.
Canonicalise the surviving set up to colour permutation and rotation/reflection of the tube coordinates.
"""
import sys, json, itertools, hashlib
sys.path.insert(0, '/mnt/project-files/multiscale/kempe_trace')
from kt import *; from collar import Collar, depth_in
PERMS = list(itertools.permutations(range(4)))
def unsat(adj, S, col, bd, w, k0):
    C = Collar(adj, S, col, bd, w); C.target_window(k0); return C.solve() is None
def shrink(adj, S, col, bd, w, k0, log=print):
    S = set(S); assert unsat(adj, S, col, bd, w, k0)
    d = depth_in(adj, S, bd)
    maxd = max(d.values())
    for dd in range(maxd, 0, -1):            # chunk pre-pass: whole depth layer at once (deepest first)
        grp = {v for v in S if d[v] == dd}
        if not grp: continue
        if unsat(adj, S - grp, col, bd, w, k0): S -= grp; log(f'  dropped layer {dd} ({len(grp)})'); continue
        for v in sorted(grp):
            S2 = S - {v}
            if unsat(adj, S2, col, bd, w, k0): S = S2
        log(f'  layer {dd}: kept {len(grp & S)} of {len(grp)}')
    return S
def canon(S, col, bd, coord, L):
    """coord: v -> (row offset from seam (0 = seam, positive = deeper), column). Returns canonical string."""
    cells = [(coord[v][0], coord[v][1], col[v]) for v in S]
    best = None
    for p in PERMS:
        for rot in range(L):
            for refl in (1, -1):
                key = tuple(sorted((r, (refl*c + rot) % L, p[cc]) for r, c, cc in cells))
                if best is None or key < best: best = key
    return best

EXT = 2
def extend_below(a, extra):
    sys.path.insert(0, '/mnt/project-files/multiscale/opus_attack/bandfill')
    from tube import band_graph
    from csp import solve
    L = len(a); n, e, t = band_graph(L, extra+1)
    dom = [set(range(4)) for _ in range(n)]
    for i in range(L): dom[extra*L+i] = {int(a[i])}
    sol = solve(n, e, t, dom); assert sol is not None
    return [''.join(map(str, sol[k*L:(k+1)*L])) for k in range(extra)]
