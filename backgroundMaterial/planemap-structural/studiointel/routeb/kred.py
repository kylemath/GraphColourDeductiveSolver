#!/usr/bin/env python3
"""studiointel routeb/kred.py -- PRODUCER. Kempe-reducibility of a configuration around a degree-5 vertex, with an adversarial outside.
Written from the SPECIFICATION in SolvingFrameworkPlan/docs/working/MathVacancyDRed/README.md sec.1 and REFINEMENT.md sec.2 only;
it imports nothing from MathVacancyDRed (independent implementation, as Math's 14:10 plan item 3(a) asks).

Configuration: a disc K (near-triangulation) containing v, given by its faces; ring R = boundary cycle (simple), H = K - v.
State: proper 4-colouring of H (canonical up to renaming); filled = link of v uses <= 3 colours (terminal, value 0).
Split theta = {0,x}|rest (x = 1,2,3 after canonical renaming). A ring edge is theta-transitional if its ends lie in different halves.
Outside pattern M_theta: a non-crossing perfect matching of the transitional ring edges (adversary's choice, 'full': any matching,
independently for the three splits). Faces of the chord diagram = regions; ring vertices in one region are joined outside.
theta-components: classes of H-vertices under (H-edges inside one half) + (same region). A move: choose theta; adversary reveals
M_theta if unknown; swap one theta-component (cost 1). Knowledge after the swap: M_theta kept; the other two kept iff the swapped
component has no ring vertex and mode == 'joint' (REFINEMENT sec.1(c)); in mode 'vdred' the other two are always forgotten.
Value: V = 0 if filled, else min_theta max_M (1 + min_C V(successor)); least fixed point by value iteration from +infinity.
Mode 'inside': the player may only swap components with no ring vertex (no outside information needed; no adversary).
"""
import sys, itertools, json
from collections import deque, defaultdict

INF = 10 ** 9

class Config:
    def __init__(self, faces, v):
        self.faces = [tuple(f) for f in faces]
        adj = defaultdict(set); de = defaultdict(int)
        for f in self.faces:
            for i in range(3):
                a, b = f[i], f[(i + 1) % 3]; adj[a].add(b); adj[b].add(a); de[(a, b)] += 1
        bnd = [(a, b) for (a, b) in de if (b, a) not in de]          # boundary directed edges (oriented faces)
        nxt = {a: b for a, b in bnd}
        assert len(nxt) == len(bnd), 'boundary not a simple cycle'
        r0 = min(nxt); ring = [r0]
        while nxt[ring[-1]] != r0: ring.append(nxt[ring[-1]])
        assert len(ring) == len(bnd), 'boundary not a single simple cycle'
        succ = {}
        for f in self.faces:
            if v in f: i = f.index(v); succ[f[(i + 1) % 3]] = f[(i + 2) % 3]
        assert len(succ) == 5 and v not in ring, 'v must be an interior degree-5 vertex'
        L = [min(succ)]
        for _ in range(4): L.append(succ[L[-1]])
        verts = sorted(u for u in adj if u != v)
        # vertex order: link first, then BFS (fixed, deterministic)
        order = list(L); seen = set(L); q = deque(L)
        while q:
            u = q.popleft()
            for w in sorted(adj[u]):
                if w != v and w not in seen: seen.add(w); order.append(w); q.append(w)
        assert len(order) == len(verts)
        self.order = order; self.idx = {u: i for i, u in enumerate(order)}; self.N = len(order)
        self.nb = [sorted(self.idx[w] for w in adj[u] if w != v) for u in order]
        self.link = [self.idx[x] for x in L]
        self.ring = [self.idx[x] for x in ring]; self.m = len(ring)
        self.isring = [False] * self.N
        for r in self.ring: self.isring[r] = True

    def colourings(self):
        N, nb = self.N, self.nb; col = [-1] * N; out = []
        def rec(i, used):
            if i == N: out.append(tuple(col)); return
            forb = {col[w] for w in nb[i] if w < i}
            for c in range(min(used + 1, 4)):
                if c not in forb: col[i] = c; rec(i + 1, max(used, c + 1))
            col[i] = -1
        col[0] = 0; rec(1, 1)
        return out

    def filled(self, c): return len({c[x] for x in self.link}) <= 3

def half(c, x):            # split x: halves {0,x} and the rest
    return 0 if c in (0, x) else 1

def nc_matchings(points):
    """all non-crossing perfect matchings of points (in cyclic order), as frozensets of pairs"""
    if not points: return [frozenset()]
    out = []; p0 = points[0]
    for k in range(1, len(points), 2):                # partner must leave an even number on each side
        inner, outer = points[1:k], points[k + 1:]
        for a in nc_matchings(inner):
            for b in nc_matchings(outer): out.append(a | b | {(p0, points[k])})
    return out

def regions(m, trans, M):
    """ring positions -> region id. trans: sorted transitional edge indices (edge i joins ring i and i+1). M: pairs of edge indices."""
    if not trans: return [0] * m
    t = len(trans); pos = {e: k for k, e in enumerate(trans)}
    partner = {}
    for a, b in M: partner[a] = b; partner[b] = a
    # gap k = ring positions after transitional edge trans[k-1] up to edge trans[k]  (cyclic); face walk: gap k -> point k -> chord -> gap after partner
    gap_face = [-1] * t; f = 0
    for g in range(t):
        if gap_face[g] >= 0: continue
        x = g
        while gap_face[x] < 0:
            gap_face[x] = f
            e = trans[x]                                  # gap x ends at transitional edge trans[x]
            x = (pos[partner[e]] + 1) % t                 # continue in the gap after the partner edge
        f += 1
    reg = [0] * m
    for k in range(t):
        start = (trans[k - 1] + 1) % m; end = trans[k]   # gap k: positions start .. end (cyclic), gap k precedes edge trans[k]
        i = start
        while True:
            reg[i] = gap_face[k]
            if i == end: break
            i = (i + 1) % m
    return reg

class Game:
    def __init__(self, cfg, mode='joint', max_nodes=10 ** 7):
        self.cfg = cfg; self.mode = mode; self.max_nodes = max_nodes
        self.mcache = {}

    def canon(self, c, K):
        mp = {}; out = []
        for x in c:
            if x not in mp: mp[x] = len(mp)
        for x in range(4):
            if x not in mp: mp[x] = len(mp)
        nc = tuple(mp[x] for x in c)
        nK = [None, None, None]
        for x in (1, 2, 3):
            if K[x - 1] is None: continue
            a, b = mp[0], mp[x]
            y = b if a == 0 else a if b == 0 else ({1, 2, 3} - {a, b}).pop()
            nK[y - 1] = K[x - 1]
        return nc, tuple(nK)

    def trans(self, c, x):
        R, m = self.cfg.ring, self.cfg.m
        return tuple(i for i in range(m) if half(c[R[i]], x) != half(c[R[(i + 1) % m]], x))

    def matchings(self, tr):
        if tr not in self.mcache: self.mcache[tr] = nc_matchings(list(tr))
        return self.mcache[tr]

    def components(self, c, x, M, tr):
        cfg = self.cfg; N = cfg.N
        par = list(range(N))
        def find(a):
            while par[a] != a: par[a] = par[par[a]]; a = par[a]
            return a
        for u in range(N):
            for w in cfg.nb[u]:
                if w > u and half(c[u], x) == half(c[w], x): par[find(u)] = find(w)
        if M is not None:
            reg = regions(cfg.m, list(tr), M); first = {}
            for i, r in enumerate(cfg.ring):
                k = reg[i]
                if k in first: par[find(r)] = find(first[k])
                else: first[k] = r
        groups = defaultdict(list)
        for u in range(N): groups[find(u)].append(u)
        return list(groups.values())

    def solve(self):
        cfg = self.cfg; cols = cfg.colourings()
        starts = [c for c in cols if not cfg.filled(c)]
        nodes = {}; keys = []; edges = []            # edges[n] = list over theta of list over M of list of successor node ids; None = filled
        def nid(key):
            if key not in nodes:
                nodes[key] = len(keys); keys.append(key); edges.append(None)
                if len(keys) > self.max_nodes: raise OverflowError('more than %d nodes' % self.max_nodes)
            return nodes[key]
        q = deque()
        for c in starts:
            n = nid(self.canon(c, (None, None, None))); q.append(n)
        done = set()
        while q:
            n = q.popleft()
            if n in done: continue
            done.add(n); c, K = keys[n]
            if cfg.filled(c): edges[n] = None; continue
            per_theta = []
            for x in (1, 2, 3):
                tr = self.trans(c, x)
                if self.mode == 'inside':
                    Ms = [None]
                else:
                    Ms = [K[x - 1]] if K[x - 1] is not None else self.matchings(tr)
                per_M = []
                for M in Ms:
                    succ = []
                    for C in self.components(c, x, M, tr):
                        ringy = any(cfg.isring[u] for u in C)
                        if self.mode == 'inside' and ringy: continue
                        nc = list(c); A = {0, x}
                        for u in C:
                            p = c[u]
                            if p in A: nc[u] = (A - {p}).pop()
                            else: nc[u] = ({0, 1, 2, 3} - A - {p}).pop()
                        if self.mode == 'inside': nK = (None, None, None)
                        else:
                            nK = [None, None, None]; nK[x - 1] = M
                            if self.mode == 'joint' and not ringy:
                                for y in (1, 2, 3):
                                    if y != x: nK[y - 1] = K[y - 1]
                        s = nid(self.canon(tuple(nc), tuple(nK))); succ.append(s)
                        if s not in done: q.append(s)
                    per_M.append(succ)
                per_theta.append(per_M)
            edges[n] = per_theta
        V = [0 if edges[n] is None else INF for n in range(len(keys))]
        changed = True; rounds = 0
        while changed:
            changed = False; rounds += 1; old = V[:]
            for n in range(len(keys)):
                if edges[n] is None: continue
                best = INF
                for per_M in edges[n]:
                    worst = 0
                    for succ in per_M:
                        a = 1 + min((old[s] for s in succ), default=INF) if succ else INF
                        if a > worst: worst = a
                        if worst >= best: break
                    if not per_M: worst = INF
                    best = min(best, worst)
                if best < V[n]: V[n] = best; changed = True
        self.nodes, self.keys, self.V, self.edges = nodes, keys, V, edges
        startval = {}
        for c in starts:
            startval[c] = V[nodes[self.canon(c, (None, None, None))]]
        lost = sum(1 for v in startval.values() if v >= INF)
        hist = defaultdict(int)
        for v in startval.values():
            if v < INF: hist[v] += 1
        return {'mode': self.mode, 'ring': cfg.m, 'H': cfg.N, 'colourings': len(cols), 'unfilled': len(starts), 'nodes': len(keys),
                'decision_nodes': sum(1 for e in edges if e is not None), 'reducible': lost == 0, 'lost': lost,
                'depth': max(hist) if lost == 0 and hist else None, 'hist': dict(sorted(hist.items())), 'startval': startval}

def ball_from_degrees(ds):
    """2-ball K around v from the cyclic link-degree sequence (REFINEMENT sec.3 structural fact): v=0, x_i = 1..5,
    ring: for each i, w_{i-1}, (d_i - 4) private vertices, w_i ... with w_i shared by x_i, x_{i+1}. Faces counter-clockwise."""
    v = 0; X = [1, 2, 3, 4, 5]; nxt = [6]
    def new():
        nxt[0] += 1; return nxt[0] - 1
    W = [new() for _ in range(5)]                       # w_i on edge x_i x_{i+1}
    faces = []
    for i in range(5):
        faces.append((v, X[i], X[(i + 1) % 5]))
        faces.append((X[(i + 1) % 5], X[i], W[i]))
    for i in range(5):
        # fan at x_i between w_{i-1} and w_i: outer vertices w_{i-1}, p_1..p_k, w_i with k = d_i - 5
        k = ds[i] - 5; assert k >= 0, 'link degrees must be >= 5'
        seq = [W[(i - 1) % 5]] + [new() for _ in range(k)] + [W[i]]
        for a, b in zip(seq, seq[1:]): faces.append((X[i], a, b))
    return faces, v

if __name__ == '__main__':
    ds = tuple(int(t) for t in sys.argv[1].split(',')); mode = sys.argv[2] if len(sys.argv) > 2 else 'joint'
    f, v = ball_from_degrees(ds); r = Game(Config(f, v), mode).solve(); r.pop('startval')
    print(json.dumps({'degrees': ds, **r}))
