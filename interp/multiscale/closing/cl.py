# Closing step (b) of Conjecture LML: library.
# A, B chordless discs partitioning V(G) of a sphere triangulation. Level (tau<=1) colourings of each side,
# renaming of B, minimum repair radius R around the conflicts (exact, SAT).
import sys, math, itertools, collections, random, pickle, time
sys.path.insert(0, '/mnt/project-files/multiscale/levelling')
sys.path.insert(0, '/mnt/project-files/multiscale')
from lev import Tri, Cluster, bfs, bfs_set, multi_bfs, domain, n2, INC, disc_or_none, chords, PERMS, icosphere, load_map
from pysat.solvers import Cadical153

# ---------------------------------------------------------------- CNF builder
class CNF:
    def __init__(self, verts):
        self.verts = list(verts); self.ix = {v: i for i, v in enumerate(self.verts)}
        self.top = 4*len(self.verts); self.cls = []
        for v in self.verts:
            self.cls.append([self.x(v, c) for c in range(4)])
            for a, b in itertools.combinations(range(4), 2): self.cls.append([-self.x(v, a), -self.x(v, b)])
    def x(self, v, c): return 4*self.ix[v]+c+1
    def new(self):
        self.top += 1; return self.top
    def neq(self, u, w):
        for c in range(4): self.cls.append([-self.x(u, c), -self.x(w, c)])
    def fix(self, v, c): self.cls.append([self.x(v, c)])
    def level(self, cl, K2=1.0, t=None, start=None, phase=None):
        """boundary walk of cluster cl within sqrt(K2) of a centre (odd case: the reflection centre at 0).
           t: force translation H_m - H_0 = t (even case). start: force H_0 = start. returns H vars."""
        D = domain(K2); Ds = set(D); m = cl.m; x = self.x
        H = [{p: self.new() for p in D} for _ in range(m+1)]
        for i in range(m):
            u, w = cl.walk[i], cl.walk[(i+1) % m]
            L = {l: self.new() for l in (1, 2, 3)}
            for a in range(4):
                for b in range(4):
                    if a != b: self.cls.append([-x(u, a), -x(w, b), L[a ^ b]])
            for p in D:
                for l in (1, 2, 3):
                    d = INC[l]; q = (p[0]+cl.s[i]*d[0], p[1]+cl.s[i]*d[1])
                    if q in Ds: self.cls.append([-H[i][p], -L[l], H[i+1][q]])
                    else: self.cls.append([-H[i][p], -L[l]])
        self.cls.append([H[0][p] for p in D])
        for p, q in itertools.combinations(D, 2): self.cls.append([-H[0][p], -H[0][q]])
        if cl.parity_odd:
            for p in D: self.cls.append([-H[m][p], H[0][(-p[0], -p[1])]])
        elif t is not None:
            for p in D:   # H[m] is implied true at the real end point (others may be spuriously true): exclude them
                q = (p[0]+t[0], p[1]+t[1])
                if q not in Ds: self.cls.append([-H[0][p]]); continue
                for q2 in D:
                    if q2 != q: self.cls.append([-H[0][p], -H[m][q2]])
        if start is not None: self.cls.append([H[0][start]])
        if phase:   # list of (walk index i, allowed set of positions)
            for i, allowed in phase:
                for p in D:
                    if p not in allowed: self.cls.append([-H[i][p]])
        return H
    def solve(self, phases=None, budget=None, assumptions=()):
        if budget is None and phases is None:
            s = Cadical153(bootstrap_with=self.cls); ok = s.solve(assumptions=list(assumptions))
        else:
            from pysat.solvers import Glucose4
            s = Glucose4(bootstrap_with=self.cls)
            if phases is not None: s.set_phases(phases)
            if budget: s.conf_budget(budget); ok = s.solve_limited(assumptions=list(assumptions))
            else: ok = s.solve(assumptions=list(assumptions))
        if ok is None: s.delete(); return 'UNK'
        res = None
        if ok:
            mod = set(l for l in s.get_model() if l > 0)
            res = {v: next(c for c in range(4) if self.x(v, c) in mod) for v in self.verts}
        s.delete(); return res

def rand_phases(enc, rng, p=0.25):
    return [(4*i+c+1)*(1 if rng.random() < p else -1) for i in range(len(enc.verts)) for c in range(4)]

def level_col(cl, rng, K2=1.0, t=None, start=None, fixed=None, budget=2*10**6, phase=None):
    enc = CNF(cl.verts)
    for u, w in cl.edges: enc.neq(u, w)
    if fixed:
        for v, c in fixed.items():
            if v in enc.ix: enc.fix(v, c)
    enc.level(cl, K2, t=t, start=start, phase=phase)
    r = enc.solve(phases=rand_phases(enc, rng), budget=budget)
    if r == 'UNK': r = enc.solve()
    return r

# ---------------------------------------------------------------- closing repair
def conflicts(T, A, col):
    return set(x for u in A for w in T.adj[u] if w not in A and col[u] == col[w] for x in (u, w))

def repair_ok(T, col, free):
    fs = set(free); enc = CNF(sorted(fs))
    for v in fs:
        for w in T.adj[v]:
            if w in fs:
                if w > v: enc.neq(v, w)
            else: enc.cls.append([-enc.x(v, col[w])])
    s = Cadical153(bootstrap_with=enc.cls); ok = s.solve(); s.delete(); return ok

def closing_R(T, A, B, colA, colB, Rmax=15, perms=PERMS):
    """min over renamings pi of min R such that recolouring N_R(conflicts) gives a proper colouring of G.
       returns (R, pi, nconf_best, per-pi conflict counts)"""
    n = len(T.adj); allv = set(range(n))
    data = []
    for p in perms:
        col = dict(colA); col.update({v: p[colB[v]] for v in B})
        K = conflicts(T, A, col)
        data.append((len(K), p, col, K))
    data.sort(key=lambda t: t[0])
    if data[0][0] == 0: return 0, data[0][1], 0
    dists = {}
    for R in range(0, Rmax+1):
        for nk, p, col, K in data:
            if p not in dists: dists[p] = multi_bfs(T.adj, list(K), allv)
            d = dists[p]
            free = [v for v in range(n) if d.get(v, 99) <= R]
            if repair_ok(T, col, free): return R, p, nk
    return None, None, data[0][0]

# ---------------------------------------------------------------- splits
def seam_edges(T, A):
    return [(u, w) for u in A for w in T.adj[u] if w not in A]

def valid_split(T, A):
    n = len(T.adj); B = set(range(n)) - A
    cA = disc_or_none(T, A); cB = disc_or_none(T, B)
    if cA is None or cB is None: return None
    if chords(cA) or chords(cB): return None
    return cA, cB

def smooth(T, A, rng, iters=200):
    """local moves to make A and its complement chordless discs."""
    n = len(T.adj); A = set(A)
    for it in range(iters):
        r = valid_split(T, A)
        if r: return A, r
        B = set(range(n)) - A
        # boundary vertices
        bA = [v for v in A if any(w not in A for w in T.adj[v])]
        bB = [v for v in B if any(w in A for w in T.adj[v])]
        # add B vertices with many A neighbours, drop A vertices with few A neighbours
        cand = []
        for v in bB:
            k = sum(1 for w in T.adj[v] if w in A)
            if 2*k > len(T.adj[v]) or k >= len(T.adj[v])-1: cand.append(('add', v))
        for v in bA:
            k = sum(1 for w in T.adj[v] if w in A)
            if 2*k < len(T.adj[v]) - 1 or k <= 2: cand.append(('del', v))
        if not cand:
            v = rng.choice(bB + bA); cand = [('add', v) if v in B else ('del', v)]
        rng.shuffle(cand)
        for op, v in cand[:max(1, len(cand)//4)]:
            if op == 'add': A.add(v)
            else: A.discard(v)
    return None, None

def grow(T, seed, size, rng, wiggle=0.0, avoid=None):
    """region growth; wiggle in [0,1]: 0 = BFS ball-like, 1 = random frontier (fractal/wiggly)."""
    A = {seed}; front = list(T.adj[seed]); inA = A
    order_d = bfs(T.adj, seed)
    while len(A) < size and front:
        if rng.random() < wiggle:
            i = rng.randrange(len(front))
        else:
            i = min(range(len(front)), key=lambda j: (order_d[front[j]], rng.random()))
        v = front.pop(i)
        if v in A or (avoid and v in avoid): continue
        A.add(v)
        front.extend(w for w in T.adj[v] if w not in A)
    return A

def odd_near(T, S, d):
    """odd-degree vertices within distance d of the vertex set S"""
    dd = multi_bfs(T.adj, list(S), set(range(len(T.adj))))
    return [v for v, k in dd.items() if k <= d and T.deg[v] % 2 == 1]

def flip_defects_near(adj, centres, radius, nflips, rng, mindeg=5, maxdeg=9):
    adj = [set(a) for a in adj]; n = len(adj)
    region = set()
    for c in centres: region |= set(bfs(adj, c, radius))
    region = sorted(region); done = 0; tries = 0
    while done < nflips and tries < nflips*300:
        tries += 1; a = rng.choice(region); b = rng.choice(sorted(adj[a])); cn = adj[a] & adj[b]
        if len(cn) != 2: continue
        c, d = cn
        if d in adj[c]: continue
        if len(adj[a])-1 < mindeg or len(adj[b])-1 < mindeg or len(adj[c])+1 > maxdeg or len(adj[d])+1 > maxdeg: continue
        adj[a].discard(b); adj[b].discard(a); adj[c].add(d); adj[d].add(c); done += 1
    return adj

def walk_info(cl, col):
    H = cl.walk_heights(col)
    tau, t = cl.tau(col)
    return dict(tau=round(tau, 3), t=None if t is None else round(t, 3),
                tvec=None if cl.parity_odd else (H[-1][0]-H[0][0], H[-1][1]-H[0][1]))
