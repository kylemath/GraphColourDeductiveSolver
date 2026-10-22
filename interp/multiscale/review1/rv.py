# Review-1 verification library: winding w(v) (chirality sum), hex-disc "pillow" spheres, crater (w=+2) colourings,
# minimal-winding constraints, hub spheres.
import sys, math, itertools, collections, random, pickle, time, json
sys.path.insert(0, '/mnt/project-files/multiscale/levelling'); sys.path.insert(0, '/mnt/project-files/multiscale/closing')
sys.path.insert(0, '/mnt/project-files/multiscale')
from lev import Tri, Cluster, bfs, bfs_set, multi_bfs, domain, n2, INC, disc_or_none, chords, PERMS, icosphere, load_map, merge
import cl as CL
from cl import CNF, level_col, closing_R, conflicts, repair_ok, rand_phases
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153

DIRS = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]

# ---------------------------------------------------------------- chirality / winding
def chir_of(a, b, c):
    """chirality of a properly coloured triangle (a,b,c) listed ccw: +1 if edge labels (a^b, b^c, c^a) are a cyclic
       rotation of (1,2,3), else -1."""
    l = (a ^ b, b ^ c, c ^ a)
    return 1 if l in ((1, 2, 3), (2, 3, 1), (3, 1, 2)) else -1

CHIR = {}
for a, b, c in itertools.permutations(range(4), 3): CHIR[(a, b, c)] = chir_of(a, b, c)

def vfaces(T):
    if not hasattr(T, 'vfaces'):
        T.vfaces = [[] for _ in T.adj]
        for i, f in enumerate(T.faces):
            for x in f: T.vfaces[x].append(i)
    return T.vfaces

def winding(T, col, v):
    """w(v) = (sum of chiralities of the faces at v)/3, for a proper colouring col (dict or list) of all of N[v]."""
    s = 0
    for i in vfaces(T)[v]:
        f = T.faces[i]; s += CHIR[(col[f[0]], col[f[1]], col[f[2]])]
    assert s % 3 == 0
    return s // 3

def windings(T, col, verts):
    return {v: winding(T, col, v) for v in verts}

def add_winding(enc, T, targets):
    """targets: dict v -> allowed set of chirality-plus counts, or 'min' (w=0 even / |w|=1 odd), or int w.
       Requires all faces at v to be inside enc.verts."""
    vf = vfaces(T); x = enc.x
    for v, tg in targets.items():
        fs = vf[v]; d = len(fs)
        cv = []
        for i in fs:
            f = T.faces[i]; z = enc.new(); cv.append(z)
            for (a, b, c), s in CHIR.items():
                if s > 0: enc.cls.append([-x(f[0], a), -x(f[1], b), -x(f[2], c), z])
                else: enc.cls.append([-x(f[0], a), -x(f[1], b), -x(f[2], c), -z])
        if tg == 'min':
            if d % 2 == 0: lo = hi = d // 2
            else: lo, hi = (d - 3) // 2, (d + 3) // 2
        elif isinstance(tg, int):   # w = tg  <=>  2*cnt - d = 3*tg
            lo = hi = (3 * tg + d) // 2
        else: lo, hi = tg
        for kind, bound in (('atleast', lo), ('atmost', hi)):
            if kind == 'atleast' and bound <= 0: continue
            if kind == 'atmost' and bound >= d: continue
            top = enc.new()
            ce = (CardEnc.atleast if kind == 'atleast' else CardEnc.atmost)(lits=cv, bound=bound, top_id=top, encoding=EncType.seqcounter)
            enc.cls.extend(ce.clauses)
            while enc.top < ce.nv: enc.new()

# ---------------------------------------------------------------- hex disc, pillow sphere
def hexdisc_pts(N):
    return [(i, j) for i in range(-N, N + 1) for j in range(-N, N + 1) if max(abs(i), abs(j), abs(i + j)) <= N]

def pillow(N):
    """two copies of the hex disc D_N glued along the boundary. returns Tri, front vertex set (incl. boundary),
       back vertex set (incl. boundary), pos dict for front/back vertices (lattice coords)."""
    P = hexdisc_pts(N); idx = {p: k for k, p in enumerate(P)}
    inner = [p for p in P if max(abs(p[0]), abs(p[1]), abs(p[0] + p[1])) < N]
    nF = len(P); back = {p: nF + k for k, p in enumerate(inner)}
    def vid(p, side):
        if side == 0 or p not in back: return idx[p]
        return back[p]
    n = nF + len(inner); adj = [set() for _ in range(n)]
    for side in (0, 1):
        for p in P:
            if side == 1 and p not in back and p not in idx: continue
            for d in DIRS:
                q = (p[0] + d[0], p[1] + d[1])
                if q in idx:
                    u, w = vid(p, side), vid(q, side); adj[u].add(w); adj[w].add(u)
    T = Tri([sorted(a) for a in adj])
    front = set(range(nF)); backset = set(back.values()) | set(idx[p] for p in P if p not in back)
    pos = {idx[p]: p for p in P}; pos.update({k: p for p, k in back.items()})
    T.pos = pos; T.front = front; T.back = backset; T.idx = idx; T.backidx = back
    return T

def crater_col(T, S, centre, K2=0.75, others='min', fixed_extra=None, budget=None, seed=0, t=None):
    """level colouring of cluster S (tau^2<=K2) with w(centre)=+2 (link 1,2,3,1,2,3 around colour 0) and w=0
       at every other interior even vertex / |w|=1 at odd ones (others='min'), or no constraint (others=None)."""
    cl = Cluster(T, S); enc = CNF(cl.verts)
    for u, w in cl.edges: enc.neq(u, w)
    if centre is not None:
        enc.fix(centre, 0)
        # order the link ccw via the faces
        link = ccw_link(T, centre)
        for k, w in enumerate(link): enc.fix(w, 1 + (k % 3))
    if fixed_extra:
        for v, c in fixed_extra.items(): enc.fix(v, c)
    tg = {}
    if others == 'min':
        for v in cl.S:
            if v not in cl.bset and v != centre: tg[v] = 'min'
    add_winding(enc, T, tg)
    enc.level(cl, K2, t=t)
    rng = random.Random(seed)
    r = enc.solve(phases=rand_phases(enc, rng), budget=budget) if budget else enc.solve()
    return cl, r

def ccw_link(T, v):
    nb = {}
    for i in vfaces(T)[v]:
        f = T.faces[i]; j = f.index(v); nb[f[(j + 1) % 3]] = f[(j + 2) % 3]
    start = next(iter(nb)); link = [start]
    while nb[link[-1]] != start: link.append(nb[link[-1]])
    return link

def three_col(T, S):
    """3-colouring of an Eulerian disc S (SAT, colours 1,2,3), or None"""
    cl = Cluster(T, S); enc = CNF(cl.verts)
    for u, w in cl.edges: enc.neq(u, w)
    for v in cl.verts: enc.cls.append([-enc.x(v, 0)])
    return cl, enc.solve()

# ---------------------------------------------------------------- generic level colouring with winding constraints
def level_w(T, S, K2=1.0, wmode='min', t=None, seed=0, budget=3 * 10 ** 6, extra_fix=None):
    cl = Cluster(T, S); enc = CNF(cl.verts)
    for u, w in cl.edges: enc.neq(u, w)
    if extra_fix:
        for v, c in extra_fix.items(): enc.fix(v, c)
    else:
        f = T.faces[cl.tris[0]]
        for j in range(3): enc.fix(f[j], j)
    if wmode == 'min':
        add_winding(enc, T, {v: 'min' for v in cl.S if v not in cl.bset})
    enc.level(cl, K2, t=t)
    rng = random.Random(seed)
    r = enc.solve(phases=rand_phases(enc, rng), budget=budget)
    if r == 'UNK': r = enc.solve()
    return cl, r

def count_w2(T, col, S=None):
    """count even-degree vertices with |w|=2 and odd with |w|>=3 among vertices whose closed nbhd is coloured."""
    verts = S if S is not None else range(len(T.adj))
    c2 = 0; c3 = 0; tot = 0; hist = collections.Counter()
    for v in verts:
        if any(w not in col for w in T.adj[v]) or v not in col: continue
        w = winding(T, col, v); tot += 1; hist[(T.deg[v] % 2, abs(w))] += 1
        if T.deg[v] % 2 == 0 and abs(w) >= 2: c2 += 1
        if T.deg[v] % 2 == 1 and abs(w) >= 3: c3 += 1
    return c2, c3, tot, dict(hist)

# ---------------------------------------------------------------- hub spheres
def hub_sphere(f, r, centre=None):
    """icosphere f with the open ball B_{r-1}(c) replaced by one hub vertex adjacent to the ring at distance r."""
    adj = icosphere(f); n = len(adj)
    if centre is None:
        odd = [v for v in range(n) if len(adj[v]) % 2]
        dd = {}
        for o in odd:
            for v, d in bfs(adj, o).items(): dd[v] = min(dd.get(v, 99), d)
        centre = max(dd, key=dd.get)
    d = bfs(adj, centre, r)
    inner = [v for v, k in d.items() if k < r]; ring = [v for v, k in d.items() if k == r]
    keep = [v for v in range(n) if v not in d or d[v] >= r]
    new = {v: i for i, v in enumerate(keep)}; hub = len(keep)
    adj2 = [set() for _ in range(hub + 1)]
    for v in keep:
        for w in adj[v]:
            if w in new: adj2[new[v]].add(new[w])
    for v in ring: adj2[new[v]].add(hub); adj2[hub].add(new[v])
    T = Tri([sorted(a) for a in adj2]); T.hub = hub
    return T
