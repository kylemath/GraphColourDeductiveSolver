# Levelling library: clusters (discs) in planar triangulations, boundary-gauge height walk,
# boundary tilt tau, and exact SAT minimisation of tau.
# Colours 0..3 = Z2^2 (xor = addition). Labels 1,2,3 -> e_g, e_h, e_{g+h}.
# Heights in HALF-lattice units: point (A,B) = (A e_g + B e_h)/2, |.|^2 = (A^2+B^2-AB)/4.
import sys, math, itertools, collections, random, pickle
import networkx as nx
from pysat.solvers import Cadical153
sys.path.insert(0, '/mnt/project-files/multiscale')
sys.path.insert(0, '/mnt/project-files/multiscale/binder_maps')

INC = {1: (2, 0), 2: (0, 2), 3: (-2, -2)}
def n2(p): return (p[0]*p[0] + p[1]*p[1] - p[0]*p[1]) / 4.0

def icosphere(f):
    import ms_tilt
    return [set(s) for s in ms_tilt.icosphere(f)]

def load_map(name):
    return [set(s) for s in pickle.load(open('/mnt/project-files/multiscale/binder_maps/%s.pkl' % name, 'rb'))]

class Tri:
    """planar triangulation with rotation system: face[(u,w)] = id of the face traversed by the dart u->w"""
    def __init__(self, adj):
        self.adj = [set(a) for a in adj]; n = len(adj)
        G = nx.Graph(); G.add_nodes_from(range(n))
        for u in range(n):
            for w in adj[u]:
                if u < w: G.add_edge(u, w)
        ok, emb = nx.check_planarity(G); assert ok
        self.face = {}; self.faces = []; seen = set()
        for u, w in emb.edges():
            if (u, w) in seen: continue
            f = emb.traverse_face(u, w, mark_half_edges=seen)
            assert len(f) == 3, f
            fid = len(self.faces); self.faces.append(tuple(f))
            for i in range(3): self.face[(f[i], f[(i+1) % 3])] = fid
        assert len(self.faces) == 2*n - 4
        self.deg = [len(a) for a in adj]

def bfs(adj, src, rmax=None):
    d = {src: 0}; q = collections.deque([src])
    while q:
        x = q.popleft()
        if rmax is not None and d[x] >= rmax: continue
        for y in adj[x]:
            if y not in d: d[y] = d[x]+1; q.append(y)
    return d

class Cluster:
    """near-triangulated disc spanned by vertex set S (holes filled)."""
    def __init__(self, T, S):
        S = set(S)
        for _ in range(5):
            # fill holes: complement components other than the largest
            comp = []; rest = set(range(len(T.adj))) - S; seen = set()
            for v in rest:
                if v in seen: continue
                c = bfs_set(T.adj, v, rest); seen |= c; comp.append(c)
            comp.sort(key=len)
            for c in comp[:-1]: S |= c
            tris = [i for i, f in enumerate(T.faces) if all(x in S for x in f)]
            ts = set(tris)
            bd = {}  # dart u->w with cluster face, reverse not
            for i in tris:
                f = T.faces[i]
                for j in range(3):
                    u, w = f[j], f[(j+1) % 3]
                    if T.face[(w, u)] not in ts: bd.setdefault(u, []).append(w)
            V = set(x for i in tris for x in T.faces[i])
            if all(len(l) == 1 for l in bd.values()) and V == S: break
            # pinch or pendant: drop vertices not in triangles, retry
            bad = [u for u, l in bd.items() if len(l) > 1]
            S = V - set(bad) if bad else V
        else:
            raise ValueError('not a disc')
        self.T = T; self.S = S; self.tris = tris
        start = min(bd); walk = [start]
        while True:
            nx_ = bd[walk[-1]][0]
            if nx_ == start: break
            walk.append(nx_)
        assert len(walk) == len(bd), 'boundary not a single cycle'
        self.walk = walk; self.m = len(walk)
        self.bset = set(walk)
        self.verts = sorted(S); self.idx = {v: i for i, v in enumerate(self.verts)}
        self.edges = set()
        cnt = collections.Counter()
        for i in tris:
            f = T.faces[i]
            for j in range(3):
                u, w = f[j], f[(j+1) % 3]; self.edges.add((min(u, w), max(u, w))); cnt[u] += 1
        self.ntri_at = cnt
        self.odd = [v for v in S if v not in self.bset and T.deg[v] % 2 == 1]
        # boundary gauge signs
        k = [cnt[b]-1 for b in walk]
        s = [1]
        for i in range(1, self.m): s.append(s[-1]*(-1 if k[i] % 2 else 1))
        self.s = s
        closing = s[-1]*(-1 if k[0] % 2 else 1)   # sign that would follow edge m-1 at b_0
        self.parity_odd = (closing != s[0])
        assert self.parity_odd == (len(self.odd) % 2 == 1), 'parity check failed'
        # check Euler: disc
        assert len(S) - len(self.edges) + len(tris) == 1

    def walk_heights(self, col):
        H = [(0, 0)]
        for i in range(self.m):
            u, w = self.walk[i], self.walk[(i+1) % self.m]
            l = col[u] ^ col[w]; assert l
            d = INC[l]; H.append((H[-1][0]+self.s[i]*d[0], H[-1][1]+self.s[i]*d[1]))
        return H

    def tau(self, col):
        """boundary tilt (radius) and translation monodromy |t| (even case)"""
        H = self.walk_heights(col)
        if self.parity_odd:
            q = ((H[0][0]+H[-1][0])/2, (H[0][1]+H[-1][1])/2)
            return math.sqrt(max(n2((h[0]-q[0], h[1]-q[1])) for h in H)), None
        t = (H[-1][0]-H[0][0], H[-1][1]-H[0][1])
        As = [h[0] for h in H]; Bs = [h[1] for h in H]
        best = 1e9
        for A in range(min(As)-1, max(As)+2):
            for B in range(min(Bs)-1, max(Bs)+2):
                r = max(n2((h[0]-A, h[1]-B)) for h in H)
                if r < best: best = r
        return math.sqrt(best), math.sqrt(n2(t))

    def info(self):
        T = self.T
        dB = multi_bfs(T.adj, self.walk, self.S)
        od = sorted(dB[o] for o in self.odd)
        sp = None
        if len(self.odd) > 1:
            sp = min(bfs(T.adj, o, 30).get(o2, 99) for o in self.odd for o2 in self.odd if o2 != o)
        return dict(n=len(self.S), m=self.m, nodd=len(self.odd),
                    n5=sum(1 for o in self.odd if T.deg[o] == 5), n7=sum(1 for o in self.odd if T.deg[o] == 7),
                    odd_depth=od, odd_spacing=sp, maxdepth=max(dB.values()))

def bfs_set(adj, v, allowed):
    c = {v}; q = [v]
    while q:
        x = q.pop()
        for y in adj[x]:
            if y in allowed and y not in c: c.add(y); q.append(y)
    return c

def multi_bfs(adj, srcs, allowed):
    d = {s: 0 for s in srcs}; q = collections.deque(srcs)
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y in allowed and y not in d: d[y] = d[x]+1; q.append(y)
    return d

def domain(K2):
    R = int(2*math.sqrt(K2))+3
    return [(A, B) for A in range(-2*R, 2*R+1) for B in range(-2*R, 2*R+1) if n2((A, B)) <= K2+1e-9]

def norms_upto(K2max):
    return sorted(set(round(n2(p), 6) for p in domain(K2max)))

def sat_level(cl, K2, fixed=None, extra=None, budget=None, phases=None):
    """Is there a proper 4-colouring of the cluster with boundary tilt^2 <= K2 ?  returns colouring dict or None.
       fixed: dict v->colour (precoloured vertices). extra: function(add_clause, var) for extra constraints."""
    V = cl.verts; ix = cl.idx; nv = len(V)
    x = lambda v, c: 4*ix[v]+c+1
    top = [4*nv]
    def new():
        top[0] += 1; return top[0]
    cls = []
    for v in V:
        cls.append([x(v, c) for c in range(4)])
        for a, b in itertools.combinations(range(4), 2): cls.append([-x(v, a), -x(v, b)])
    for u, w in cl.edges:
        for c in range(4): cls.append([-x(u, c), -x(w, c)])
    if fixed:
        for v, c in fixed.items():
            if v in ix: cls.append([x(v, c)])
    else:
        f = cl.T.faces[cl.tris[0]]
        for j in range(3): cls.append([x(f[j], j)])
    if K2 is not None:
        D = domain(K2); Ds = set(D); m = cl.m
        H = [{p: new() for p in D} for _ in range(m+1)]
        for i in range(m):
            u, w = cl.walk[i], cl.walk[(i+1) % m]
            L = {l: new() for l in (1, 2, 3)}
            for a in range(4):
                for b in range(4):
                    if a != b: cls.append([-x(u, a), -x(w, b), L[a ^ b]])
            for p in D:
                for l in (1, 2, 3):
                    d = INC[l]; q = (p[0]+cl.s[i]*d[0], p[1]+cl.s[i]*d[1])
                    if q in Ds: cls.append([-H[i][p], -L[l], H[i+1][q]])
                    else: cls.append([-H[i][p], -L[l]])
        cls.append([H[0][p] for p in D])
        for p, q in itertools.combinations(D, 2): cls.append([-H[0][p], -H[0][q]])
        if cl.parity_odd:
            for p in D:
                mp = (-p[0], -p[1])
                cls.append([-H[m][p], H[0][mp]])
    if extra: extra(cls.append, x, new)
    if budget is None:
        s = Cadical153(bootstrap_with=cls); ok = s.solve()
    else:
        from pysat.solvers import Glucose4
        s = Glucose4(bootstrap_with=cls)
        if phases is not None: s.set_phases(phases)
        s.conf_budget(budget); ok = s.solve_limited()
        if ok is None:
            s.delete(); return 'UNK'
    res = None
    if ok:
        mod = set(l for l in s.get_model() if l > 0)
        res = {v: next(c for c in range(4) if x(v, c) in mod) for v in V}
    s.delete()
    return res

def rand_col(cl, seed, fixed=None):
    rng = random.Random(seed); nv = len(cl.verts)
    ph = [(4*i+c+1)*(1 if rng.random() < 0.25 else -1) for i in range(nv) for c in range(4)]
    return sat_level(cl, None, fixed=fixed, budget=10**7, phases=ph)

def min_tau(cl, K2max=36.0, fixed=None, budget=None, seed=0):
    """returns (tau_min, colouring, tau_of_random_colouring, exact_flag). With a budget, unknown calls count as
       'not shown feasible'; exact_flag False means tau_min is an upper bound and lower bound unproved."""
    col = rand_col(cl, seed, fixed)
    if col is None: return None, None, None, True
    t0, _ = cl.tau(col)
    cands = [k for k in norms_upto(max(K2max, t0*t0+1)) if k <= t0*t0+1e-6]
    lo, hi = 0, len(cands)-1; best = col; exact = True
    while lo < hi:
        mid = (lo+hi)//2
        r = sat_level(cl, cands[mid], fixed=fixed, budget=budget)
        if r == 'UNK': exact = False; lo = mid+1
        elif r is not None: hi = mid; best = r
        else: lo = mid+1
    return math.sqrt(cands[hi]), best, t0, exact

def disc_or_none(T, S):
    """Cluster on exactly S if S spans a disc (no filling), else None."""
    try:
        cl = Cluster(T, S)
    except Exception:
        return None
    return cl if cl.S == set(S) else None

PERMS = list(itertools.permutations(range(4)))

def merge(T, A, B, colA, colB, Rmax=8, level_K2=None, perms=PERMS, U=None):
    """Glue colA on A with pi(colB) on B; smallest R (over renamings) such that recolouring the vertices of U within
       distance R of the conflicts gives a proper colouring of U (and, if level_K2, with tau(U)^2 <= level_K2).
       returns (R, pi, colouring) or (None,..)."""
    if U is None: U = disc_or_none(T, set(A) | set(B))
    Uset = U.S
    seam = [(u, w) for (u, w) in U.edges if (u in A) != (w in A)]
    data = []
    for p in perms:
        col = {v: colA[v] for v in A}; col.update({v: p[colB[v]] for v in B})
        K = set(x for e in seam if col[e[0]] == col[e[1]] for x in e)
        data.append((len(K), p, col, K))
    data.sort(key=lambda t: t[0])
    for R in range(0, Rmax+1):
        for nk, p, col, K in data:
            if not K and level_K2 is None: return 0, p, col
            d = multi_bfs(T.adj, list(K), Uset) if K else {}
            fixed = {v: col[v] for v in Uset if d.get(v, 99) > R}
            if not K:
                ok = level_K2 is None or U.tau(col)[0]**2 <= level_K2+1e-9
                if ok: return 0, p, col
                if R == 0: continue
                # nothing to repair but not level: allow recolouring near seam
                d = multi_bfs(T.adj, [x for e in seam for x in e], Uset)
                fixed = {v: col[v] for v in Uset if d.get(v, 99) > R}
            r = sat_level(U, level_K2, fixed=fixed, budget=2*10**6)
            if r not in (None, 'UNK'): return R, p, r
    return None, None, None

def chords(cl):
    pos = {v: i for i, v in enumerate(cl.walk)}
    return [(u, w) for (u, w) in cl.edges if u in pos and w in pos and (pos[u]-pos[w]) % cl.m not in (1, cl.m-1)]

def fast_disc(T, S):
    """local test: S spans a near-triangulated disc (Euler char 1, one simple boundary cycle, no isolated vertices)."""
    S = set(S)
    if not hasattr(T, 'vfaces'):
        T.vfaces = [[] for _ in T.adj]
        for i, f in enumerate(T.faces):
            for x in f: T.vfaces[x].append(i)
    tris = set(i for v in S for i in T.vfaces[v] if all(x in S for x in T.faces[i]))
    if not tris: return False
    V = set(x for i in tris for x in T.faces[i])
    if V != S: return False
    E = set()
    bd = {}
    for i in tris:
        f = T.faces[i]
        for j in range(3):
            u, w = f[j], f[(j+1) % 3]; E.add((min(u, w), max(u, w)))
            if T.face[(w, u)] not in tris:
                if u in bd: return False
                bd[u] = w
    if len(V) - len(E) + len(tris) != 1 or not bd: return False
    start = next(iter(bd)); x = bd[start]; k = 1
    while x != start:
        if x not in bd: return False
        x = bd[x]; k += 1
        if k > len(bd): return False
    return k == len(bd)
