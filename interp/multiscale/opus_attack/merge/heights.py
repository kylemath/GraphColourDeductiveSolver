# Build proper 4-colourings of a flat lattice region from height functions, with prescribed balls for chosen
# vertices (used to force every pocket boundary into a radius-1 ball around a prescribed centre).
import random
from lat import INC, n2, solve, bfs, col_of_height

def lattice_pts(rad):
    R = int(2*rad) + 3
    return [(2*a, 2*b) for a in range(-R, R+1) for b in range(-R, R+1) if n2((2*a, 2*b)) <= rad*rad + 1e-9]

def ball_pts(c, r=1.0, rad=None):
    """vertex-height lattice points (both coords even) within distance r of centre c (half units, any ints)."""
    R = int(2*r) + 4
    out = []
    for a in range(c[0]//2 - R, c[0]//2 + R + 1):
        for b in range(c[1]//2 - R, c[1]//2 + R + 1):
            p = (2*a, 2*b)
            if n2((p[0]-c[0], p[1]-c[1])) <= r*r + 1e-9: out.append(p)
    return out

def build_heights(g, S, cons, seed=0, extra_dom=None, slack=0, budget=None, forbid=None):
    """S: vertex set (flat region). cons: dict v -> set of allowed heights (e.g. ball points).
       Domain of every other vertex: points within (BFS distance to the constrained set)+slack of the allowed sets.
       forbid: optional list of (v, height) pairs forbidden.  Returns dict v->height or None."""
    S = set(S); rng = random.Random(seed)
    srcs = list(cons)
    # Lipschitz pruning: |h(v)-h(c)| <= d(v,c) for each constrained c; approximate by nearest few sources
    dom = {}
    dist_from = {}
    for c in srcs: pass
    # multi-source BFS keeping the nearest constrained vertex set
    d0 = bfs(g.adj, srcs, S)
    allp = set(p for c in srcs for p in cons[c])
    cache = {}
    for v in S:
        if v in cons: dom[v] = sorted(cons[v]); continue
        r = d0[v] + slack
        if r not in cache:
            R = int(r) + 1
            offs = [(2*a, 2*b) for a in range(-R, R+1) for b in range(-R, R+1) if n2((2*a, 2*b)) <= r*r + 1e-9]
            cache[r] = sorted(set((p[0]+o[0], p[1]+o[1]) for p in allp for o in offs))
        dom[v] = cache[r]
    if extra_dom:
        for v, ds in extra_dom.items(): dom[v] = sorted(set(dom[v]) & set(ds))
    V = sorted(S); var = {}; top = 0
    for v in V:
        for p in dom[v]: top += 1; var[(v, p)] = top
    cls = []
    for v in V:
        lits = [var[(v, p)] for p in dom[v]]
        if not lits: return None
        cls.append(lits)
        # ladder at-most-one
        prev = None
        for i, x in enumerate(lits):
            if i == len(lits) - 1:
                if prev: cls.append([-x, -prev])
                break
            top += 1; s = top
            cls.append([-x, s])
            if prev: cls.append([-prev, s]); cls.append([-x, -prev])
            prev = s
    for u in V:
        for w in g.adj[u]:
            if w not in S or w < u: continue
            sg = g.sgn(u, w)
            for p in dom[u]:
                nb = [var[(w, (p[0]+sg*INC[l][0], p[1]+sg*INC[l][1]))] for l in (1, 2, 3)
                      if (w, (p[0]+sg*INC[l][0], p[1]+sg*INC[l][1])) in var]
                cls.append([-var[(u, p)]] + nb)
            for q in dom[w]:
                nb = [var[(u, (q[0]-sg*INC[l][0], q[1]-sg*INC[l][1]))] for l in (1, 2, 3)
                      if (u, (q[0]-sg*INC[l][0], q[1]-sg*INC[l][1])) in var]
                cls.append([-var[(w, q)]] + nb)
    if forbid:
        for v, p in forbid:
            if (v, p) in var: cls.append([-var[(v, p)]])
    # randomise by permuting variable names
    perm = list(range(1, top+1)); rng.shuffle(perm); pm = {i+1: perm[i] for i in range(top)}
    cls2 = [[(pm[abs(l)] if l > 0 else -pm[abs(l)]) for l in c] for c in cls]
    rng.shuffle(cls2)
    r = solve(top, cls2, budget)
    if r is None or r == 'UNK': return r
    inv = {pm[i]: i for i in pm}
    tv = set(inv[x] for x in r)
    h = {}
    for v in V:
        hs = [p for p in dom[v] if var[(v, p)] in tv]; assert len(hs) == 1; h[v] = hs[0]
    # check increments
    for u in V:
        for w in g.adj[u]:
            if w in S:
                d = (h[w][0]-h[u][0], h[w][1]-h[u][1]); sg = g.sgn(u, w)
                assert (d[0]*sg, d[1]*sg) in INC.values(), 'bad increment'
    return h

def colouring(h): return {v: col_of_height(p) for v, p in h.items()}
