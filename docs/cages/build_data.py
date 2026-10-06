# Builds docs/cages/data.js for "Cages and Diamonds".
# Independent recomputation (imports no project module). Three parts:
#   A. Fullerene duals (cages): the C60 dual (32 vertices) and the C70 dual (37 vertices), decoded from
#      backgroundMaterial/planemap-structural/studiointel/ipr/ipr_32_52.pc (buckygen planar code).
#      For one degree-5 hole per symmetry class: every proper 4-colouring of T - v up to renaming,
#      whole-component Kempe swaps (singletons allowed), swap distance rho to a filled state (link <= 3 colours),
#      doubly-locked (DL) states, and a library of start states with a shortest fill.
#   B. The Birkhoff diamond in a hexagonal ring: every ring colouring up to renaming, which ones extend
#      to the interior, and Birkhoff's D-closure (flips of unions of chain blocks, over every consistent
#      outside chain structure), so every colouring is classified "extends" or "level L, certified by a flip".
#   C. The (5,5,6,5,6) F-cycle: the order-22 graph from studiointel/fcycle/fcycle_order22.json (on branch
#      origin/studio-intel), recomputed from its face list: the F-orbit, rho of its 20 states, silent first moves.
# Everything is recomputed from face lists / rotation lists; only the face lists and the RSST rotation lists are inputs.
import sys, os, json, collections, itertools, time, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
t0 = time.time()
def tick(msg): print('[%5.1fs] %s' % (time.time() - t0, msg), flush=True)
NAMES = ['red', 'blue', 'yellow', 'green']
PAIRS = list(itertools.combinations(range(4), 2))

# ============================================================== triangulation checks and layout
def check_triangulation(faces, min_deg=5):
    n = 1 + max(max(f) for f in faces)
    edges = set()
    for a, b, c in faces:
        for x, y in ((a, b), (b, c), (c, a)): edges.add((min(x, y), max(x, y)))
    adj = [set() for _ in range(n)]
    for x, y in edges: adj[x].add(y); adj[y].add(x)
    assert n - len(edges) + len(faces) == 2, 'Euler'
    ecount = collections.Counter()
    for a, b, c in faces:
        for x, y in ((a, b), (b, c), (c, a)): ecount[(min(x, y), max(x, y))] += 1
    assert all(v == 2 for v in ecount.values()), 'each edge in two faces'
    assert len(edges) == 3 * n - 6 and len(faces) == 2 * n - 4
    rot = []
    for v in range(n):
        inc = [f for f in faces if v in f]
        nb = collections.defaultdict(list)
        for f in inc:
            x, y = [u for u in f if u != v]; nb[x].append(y); nb[y].append(x)
        start = min(nb); cyc = [start]; prev = None; cur = start
        while True:
            nxt = [w for w in nb[cur] if w != prev][0]
            if nxt == start: break
            cyc.append(nxt); prev, cur = cur, nxt
        assert len(cyc) == len(adj[v]) == len(inc), ('link not a single cycle', v)
        rot.append(cyc)
    faceset = {tuple(sorted(f)) for f in faces}
    tri = [t for t in itertools.combinations(range(n), 3) if t[1] in adj[t[0]] and t[2] in adj[t[0]] and t[2] in adj[t[1]]]
    sep = [t for t in tri if t not in faceset]
    deg = [len(a) for a in adj]
    assert min(deg) >= min_deg and not sep, ('min degree / separating triangle', min(deg), sep[:3])
    return dict(n=n, edges=edges, adj=adj, rot=rot, deg=deg, sep=len(sep))

def make_layout(G, faces, seed=1, iters=6000, far_from=None):
    """Weighted Tutte drawing (outer face on a circle, positive weights, Floater) plus hill-climb for spacing."""
    n, edges, adj = G['n'], G['edges'], G['adj']
    Ea = np.array(sorted(edges)); Fa = np.array(faces)
    def gaps(P):
        dd = np.hypot(P[:, None, 0] - P[None, :, 0], P[:, None, 1] - P[None, :, 1])
        vv = dd[np.triu_indices(n, 1)].min()
        A_, B_ = P[Ea[:, 0]], P[Ea[:, 1]]; D_ = B_ - A_; L_ = (D_ * D_).sum(1)
        t = np.clip(((P[None, :, :] - A_[:, None, :]) * D_[:, None, :]).sum(2) / L_[:, None], 0, 1)
        Q_ = A_[:, None, :] + t[:, :, None] * D_[:, None, :]
        de = np.hypot(*(P[None, :, :] - Q_).transpose(2, 0, 1))
        de[np.arange(len(Ea)), Ea[:, 0]] = 9; de[np.arange(len(Ea)), Ea[:, 1]] = 9
        return float(vv), float(de.min())
    def score(P):
        vv, ve = gaps(P); return min(vv, 2 * ve)
    def fit(P):
        lo, hi = P.min(0), P.max(0); return (P - (lo + hi) / 2) * (2.08 / float((hi - lo).max()))
    def signs(P):
        a, b, c = P[Fa[:, 0]], P[Fa[:, 1]], P[Fa[:, 2]]
        return np.sign((b[:, 0] - a[:, 0]) * (c[:, 1] - a[:, 1]) - (b[:, 1] - a[:, 1]) * (c[:, 0] - a[:, 0]))
    def crossings(P):
        def ccw(a, b, c): return (P[b][0]-P[a][0])*(P[c][1]-P[a][1]) - (P[b][1]-P[a][1])*(P[c][0]-P[a][0])
        bad = 0
        for (a, b), (c, d) in itertools.combinations(sorted(edges), 2):
            if len({a, b, c, d}) == 4 and ccw(a, b, c) * ccw(a, b, d) < 0 and ccw(c, d, a) * ccw(c, d, b) < 0: bad += 1
        return bad
    def tutte(outer, alpha, rounds):
        P = np.zeros((n, 2))
        for k, v in enumerate(outer):
            ang = -np.pi / 2 + 2 * np.pi * k / 3; P[v] = [np.cos(ang), np.sin(ang)]
        depth = {v: 0 for v in outer}; qq = collections.deque(outer)
        while qq:
            u = qq.popleft()
            for w in adj[u]:
                if w not in depth: depth[w] = depth[u] + 1; qq.append(w)
        inner = [v for v in range(n) if v not in outer]; ix = {v: i for i, v in enumerate(inner)}
        def solve(wf):
            A = np.zeros((len(inner), len(inner))); b = np.zeros((len(inner), 2))
            for v in inner:
                i = ix[v]
                for w in adj[v]:
                    x = wf(v, w); A[i, i] += x
                    if w in ix: A[i, ix[w]] -= x
                    else: b[i] += x * P[w]
            s_ = np.linalg.solve(A, b)
            for v in inner: P[v] = s_[ix[v]]
        base = lambda v, w: float(np.exp(-alpha * depth[w]))
        solve(base)
        for _ in range(rounds):
            Lm = {(v, w): float(np.hypot(*(P[v] - P[w]))) for v in range(n) for w in adj[v]}
            solve(lambda v, w: base(v, w) * Lm[(v, w)])
        return fit(P)
    cf = faces
    if far_from is not None:   # outer face as far as possible from the hole, so the hole sits in the middle of the drawing
        dist = {far_from: 0}; qq = collections.deque([far_from])
        while qq:
            u = qq.popleft()
            for w in adj[u]:
                if w not in dist: dist[w] = dist[u] + 1; qq.append(w)
        fd = {tuple(f): min(dist[x] for x in f) for f in faces}; mxd = max(fd.values()); cf = [f for f in faces if fd[tuple(f)] == mxd]
    cands = [(score(tutte(list(f), al, r)), list(f), al, r) for f in cf for al in (0, 0.8, 1.6) for r in (0, 4)]
    _, outer, alpha, rounds = max(cands, key=lambda c: c[0])
    pos = tutte(outer, alpha, rounds); S0 = signs(pos); cur = score(pos)
    rng = np.random.default_rng(seed); movable = [v for v in range(n) if v not in outer]
    for it in range(iters):
        v = movable[rng.integers(len(movable))]; Z = pos.copy(); Z[v] += rng.normal(0, 0.03, 2)
        if (signs(Z) != S0).any(): continue
        s_ = score(Z)
        if s_ >= cur: pos, cur = Z, s_
    pos = fit(pos)
    assert (signs(pos) == S0).all() and crossings(pos) == 0, 'layout must be planar'
    return pos, outer, [round(x, 3) for x in gaps(pos)]

# ============================================================== the hole system: states, Kempe graph, rho
class Hole:
    def __init__(self, G, hole, link):
        self.G, self.hole, self.link = G, hole, link
        n = G['n']; adj = G['adj']
        self.V = [v for v in range(n) if v != hole]
        self.pv = {v: i for i, v in enumerate(self.V)}
        self.nbrI = [[self.pv[w] for w in sorted(adj[v]) if w != hole] for v in self.V]
        self.nbm = [sum(1 << j for j in nb) for nb in self.nbrI]
        self.Ln = [self.pv[x] for x in link]
        self.Lset = set(self.Ln)
        # BFS order for backtracking
        order = []; seen = {link[0]}; q = collections.deque([link[0]])
        while q:
            u = q.popleft(); order.append(u)
            for w in sorted(adj[u]):
                if w != hole and w not in seen: seen.add(w); q.append(w)
        assert len(order) == len(self.V)
        raw = []; col = {}
        nb = {v: [w for w in adj[v] if w != hole] for v in self.V}
        def bt(k, used):
            if k == len(order):
                raw.append(tuple(col[v] for v in self.V)); return
            v = order[k]; bad = {col[w] for w in nb[v] if w in col}
            for c in range(min(used + 1, 4)):
                if c not in bad: col[v] = c; bt(k + 1, max(used, c + 1)); del col[v]
        bt(0, 0)
        self.states = sorted(set(self.canon(s) for s in raw))
        assert len(self.states) == len(raw), 'canonical enumeration has no repeats'
        self.sidx = {s: i for i, s in enumerate(self.states)}
    @staticmethod
    def canon(col):
        m = {}
        return tuple(m.setdefault(x, len(m)) for x in col)
    def comps(self, s):
        """All whole bichromatic components: list of (a, b, mask)."""
        cls = [0] * 4
        for i, x in enumerate(s): cls[x] |= 1 << i
        out = []
        for a, b in PAIRS:
            pend = cls[a] | cls[b]
            while pend:
                seed = pend & -pend; pend ^= seed; comp = seed; fr = seed
                while fr:
                    low = fr & -fr; fr ^= low
                    new = self.nbm[low.bit_length() - 1] & pend
                    if new: pend &= ~new; comp |= new; fr |= new
                out.append((a, b, comp))
        return out
    @staticmethod
    def apply(s, a, b, mask):
        t = list(s); i = 0; m = mask
        while m:
            low = m & -m; i = low.bit_length() - 1; m ^= low
            t[i] = b if s[i] == a else a
        return tuple(t)
    def build(self):
        S = self.states
        self.moves = []
        self.nxt = []
        for i, s in enumerate(S):
            mv = []
            for a, b, mask in self.comps(s):
                j = self.sidx[self.canon(self.apply(s, a, b, mask))]
                mv.append((a, b, mask, j))
            self.moves.append(mv)
            self.nxt.append(sorted({m[3] for m in mv if m[3] != i}))
        self.filled = [len({s[i] for i in self.Ln}) <= 3 for s in S]
        d = [-1] * len(S); q = collections.deque()
        for i in range(len(S)):
            if self.filled[i]: d[i] = 0; q.append(i)
        while q:
            u = q.popleft()
            for w in self.nxt[u]:
                if d[w] < 0: d[w] = d[u] + 1; q.append(w)
        self.d = d
        cls = [-1] * len(S); k = 0
        for i in range(len(S)):
            if cls[i] >= 0: continue
            cls[i] = k; q = collections.deque([i])
            while q:
                u = q.popleft()
                for w in self.nxt[u]:
                    if cls[w] < 0: cls[w] = k; q.append(w)
            k += 1
        self.cls, self.ncls = cls, k
        self.dl = [self.dl_info(s) for s in S]
    def comp_of(self, s, start, a, b):
        seen = {start}; st = [start]
        while st:
            u = st.pop()
            for j in self.nbrI[u]:
                if j not in seen and s[j] in (a, b): seen.add(j); st.append(j)
        return seen
    def dl_info(self, s):
        """None if filled; else (j, lock1, lock2) with j the repeat index (l-attack.md section 1)."""
        Ln = self.Ln; L = [s[i] for i in Ln]
        if len(set(L)) <= 3: return None
        j = [t for t in range(5) if L[t] == L[(t + 2) % 5]][0]
        m, a, b = Ln[(j + 1) % 5], Ln[(j + 3) % 5], Ln[(j + 4) % 5]
        l1 = a in self.comp_of(s, m, s[m], s[a]); l2 = b in self.comp_of(s, m, s[m], s[b])
        return j, l1, l2
    def kind(self, i):
        if self.filled[i]: return 'filled'
        j, l1, l2 = self.dl[i]
        return 'dl' if (l1 and l2) else 'one'
    def mask_verts(self, mask):
        return [self.V[i] for i in range(len(self.V)) if mask >> i & 1]
    def link_touch(self, mask):
        return [t for t, i in enumerate(self.Ln) if mask >> i & 1]
    def shortest_path(self, i, prefer_silent=False):
        """Deterministic shortest route to a filled state: list of (a, b, mask, silent, target)."""
        path = []
        while self.d[i] > 0:
            cands = [m for m in self.moves[i] if m[3] != i and self.d[m[3]] == self.d[i] - 1]
            def key(m):
                sil = not self.link_touch(m[2])
                return (0 if (prefer_silent and sil) else 1, bin(m[2]).count('1'), m[0], m[1], m[2])
            m = min(cands, key=key)
            path.append((m[0], m[1], m[2], not self.link_touch(m[2]), m[3])); i = m[3]
        return path

def find_configs(G, faces):
    """Birkhoff diamonds (RSST 0.7322) and RSST 2.122 occurrences, by the audit's definition
    (messages/2026-10-06/..._1516_audit_..._Lean-ready-definitions...md sections 3-4)."""
    adj, deg = G['adj'], G['deg']; fs = {tuple(sorted(f)) for f in faces}
    isface = lambda a, b, c: tuple(sorted((a, b, c))) in fs
    dia, c2122 = set(), set()
    for q, r in itertools.combinations(range(G['n']), 2):
        if r not in adj[q]: continue
        com = [w for w in adj[q] & adj[r] if isface(q, r, w)]
        for p, s in itertools.combinations(sorted(com), 2):
            if s in adj[p]: continue
            if deg[p] == deg[s] == 5 and deg[q] == deg[r] == 5: dia.add((tuple(sorted((q, r))), (p, s)))
            for h, c in ((q, r), (r, q)):
                if deg[h] == 6 and deg[c] == deg[p] == deg[s] == 5: c2122.add((h, c, p, s))
    return sorted(dia), sorted(c2122)

# ============================================================== A. fullerene duals
def read_planar_code(path):
    b = open(path, 'rb').read(); i = len(b'>>planar_code<<'); assert b[:i] == b'>>planar_code<<'
    gs = []
    while i < len(b):
        n = b[i]; i += 1; adj = []
        for v in range(n):
            l = []
            while b[i] != 0: l.append(b[i] - 1); i += 1
            i += 1; adj.append(l)
        gs.append(adj)
    return gs

def faces_from_rotation(g):
    fs = set()
    for v, nb in enumerate(g):
        for k in range(len(nb)): fs.add(tuple(sorted((v, nb[k], nb[(k + 1) % len(nb)]))))
    return sorted(fs)

def hole_profile(G, v):
    """Isomorphism-invariant profile of a vertex: degrees by BFS layer, two layers of neighbour-degree sequences."""
    dist = {v: 0}; q = collections.deque([v])
    while q:
        u = q.popleft()
        for w in G['adj'][u]:
            if w not in dist: dist[w] = dist[u] + 1; q.append(w)
    return tuple(tuple(sorted(G['deg'][u] for u in dist if dist[u] == k)) for k in range(max(dist.values()) + 1))

def build_cage(name, graphs, nv, label):
    g = [x for x in graphs if len(x) == nv]
    assert len(g) == 1, 'exactly one planar-code graph with %d vertices' % nv
    g = g[0]
    faces = faces_from_rotation(g)
    G = check_triangulation(faces)
    deg = G['deg']; dc = collections.Counter(deg)
    assert dc == {5: 12, 6: nv - 12}, dc
    fives = [v for v in range(nv) if deg[v] == 5]
    assert not any(w in G['adj'][v] for v in fives for w in fives), 'IPR: no two degree-5 vertices adjacent'
    dia, c2122 = find_configs(G, faces)
    assert not dia and not c2122, 'cage is configuration-free'
    pos, outer, gp = make_layout(G, faces, iters=5000, far_from=fives[0])
    tick('%s layout done, gaps %s' % (name, gp))
    # one hole per profile class (isomorphism invariant; vertices in one class are inequivalent only if the profile differs)
    prof = collections.defaultdict(list)
    for v in fives: prof[hole_profile(G, v)].append(v)
    holes = []
    for pr, vs in sorted(prof.items(), key=lambda kv: kv[1][0]):
        hv = vs[0]; link = G['rot'][hv]
        H = Hole(G, hv, link); H.build()
        # every other hole with the same profile must give the same rho histogram (checked, not assumed)
        for ov in vs[1:]:
            H2 = Hole(G, ov, G['rot'][ov]); H2.build()
            same = lambda A: sorted(collections.Counter(A.d[i] for i in range(len(A.states)) if A.kind(i) == 'dl').items())
            assert len(H2.states) == len(H.states) and same(H2) == same(H), ('holes in one profile class differ', hv, ov)
        lk_deg = [deg[x] for x in link]
        assert all(x == 6 for x in lk_deg), 'IPR: link all degree 6'
        S = H.states; kinds = [H.kind(i) for i in range(len(S))]
        ndl = [i for i in range(len(S)) if kinds[i] == 'dl']
        hist_all = collections.Counter(H.d); hist_dl = collections.Counter(H.d[i] for i in ndl)
        assert min(H.d) == 0 and -1 not in H.d, 'every colouring reaches a filled state'
        # unfilled non-DL are one swap from filled
        assert all(H.d[i] == 1 for i in range(len(S)) if kinds[i] == 'one'), 'non-DL unfilled fills in one swap'
        assert all(H.d[i] >= 2 for i in ndl)
        rng = np.random.default_rng(7)
        pick = lambda ids, k: sorted(rng.choice(ids, size=min(k, len(ids)), replace=False).tolist()) if ids else []
        lib_ids = []
        by_rho = collections.defaultdict(list)
        for i in ndl: by_rho[H.d[i]].append(i)
        maxr = max(hist_dl)
        for r in sorted(by_rho, reverse=True):
            lib_ids += pick(by_rho[r], {2: 4}.get(r, 6))
        lib_ids += pick([i for i in range(len(S)) if kinds[i] == 'one'], 3)
        lib_ids += pick([i for i in range(len(S)) if kinds[i] == 'filled'], 1)
        lib = []
        for i in lib_ids:
            path = H.shortest_path(i)
            lib.append({'c': list(S[i]), 'd': H.d[i], 'k': kinds[i],
                        'path': [[a, b, H.mask_verts(m), int(sil)] for a, b, m, sil, _ in path]})
        holes.append({'hole': hv, 'orbit': len(vs), 'orbitMembers': vs, 'link': link,
                      'summary': {'colourings': len(S), 'classes': H.ncls, 'filled': sum(H.filled), 'dl': len(ndl),
                                  'allHist': {str(k): v for k, v in sorted(hist_all.items())},
                                  'dlHist': {str(k): v for k, v in sorted(hist_dl.items())}, 'maxRadius': maxr},
                      'lib': lib})
        tick('%s hole %d (profile class of %d): %d colourings, %d classes, DL %s, max rho %d' %
             (name, hv, len(vs), len(S), H.ncls, dict(sorted(hist_dl.items())), maxr))
    return {'name': name, 'label': label, 'order': nv, 'faces': [list(f) for f in faces], 'rot': G['rot'],
            'pos': [[round(float(x), 4), round(float(y), 4)] for x, y in pos], 'outer': outer, 'deg': deg,
            'degCount': {str(k): v for k, v in sorted(dc.items())}, 'edges': len(G['edges']),
            'separatingTriangles': G['sep'], 'diamonds': len(dia), 'conf2122': len(c2122), 'holes': holes}

tick('reading planar code')
graphs = read_planar_code(os.path.join(ROOT, 'backgroundMaterial/planemap-structural/studiointel/ipr/ipr_32_52.pc'))
nfile = collections.Counter(len(g) for g in graphs)
ipr_index = {nv: [k for k, g in enumerate(graphs) if len(g) == nv][0] for nv in (32, 37)}
print('planar code file: %d graphs; one graph of order 32 (index %d), one of order 37 (index %d)' % (len(graphs), ipr_index[32], ipr_index[37]))
cages = [build_cage('C60', graphs, 32, 'C60 dual'), build_cage('C70', graphs, 37, 'C70 dual')]

# ============================================================== B. D-reducibility of a ring configuration
# RSST file entries as read by the audit (message 2026-10-06_1516_audit_..._Lean-ready-definitions..., sections 3 and 4):
# ring vertices 1..r, interior vertices r+1..n, each interior vertex's neighbours in rotation order.
RSST_DIAMOND = {7: [2, 8, 9, 10, 1], 8: [2, 3, 4, 9, 7], 9: [8, 4, 5, 10, 7], 10: [9, 5, 6, 1, 7]}   # 0.7322, ring 6
RSST_2122 = {8: [2, 3, 9, 10, 11, 1], 9: [3, 4, 5, 10, 8], 10: [9, 5, 6, 11, 8], 11: [10, 6, 7, 1, 8]}  # 2.122, ring 7

PARTS = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]
def set_partitions(items):
    if not items: yield []; return
    first, rest = items[0], items[1:]
    for p in set_partitions(rest):
        yield [[first]] + p
        for k in range(len(p)): yield p[:k] + [[first] + p[k]] + p[k + 1:]

def dreduce(RSST, r, full=True):
    """Birkhoff's D-closure for a configuration with ring 1..r. Returns a dict of classes with levels and certificates."""
    RING = list(range(1, r + 1)); INT = sorted(RSST)
    iedges = set(); ring_edges = {(min(RING[k], RING[(k + 1) % r]), max(RING[k], RING[(k + 1) % r])) for k in range(r)}
    for v, nb in RSST.items():
        for w in nb:
            iedges.add((min(v, w), max(v, w)))
            if w in RSST: assert v in RSST[w], 'interior adjacency symmetric'
    assert iedges & ring_edges == set(), 'no ring chord'
    dfaces = set()
    for v, nb in RSST.items():
        for k in range(len(nb)): dfaces.add(tuple(sorted((v, nb[k], nb[(k + 1) % len(nb)]))))
    all_edges = iedges | ring_edges
    assert r + len(INT) - len(all_edges) + len(dfaces) == 1, 'disc: V - E + F = 1'
    ecnt = collections.Counter()
    for f in dfaces:
        for x, y in itertools.combinations(f, 2): ecnt[(x, y)] += 1
    assert all((ecnt[e] == 1) if e in ring_edges else (ecnt[e] == 2) for e in all_edges), 'ring edges in one face, the rest in two'
    RP = {v: [RING.index(w) for w in nb if w in RING] for v, nb in RSST.items()}
    IA = {v: [w for w in nb if w in RSST] for v, nb in RSST.items()}
    ring_classes = sorted({Hole.canon(c) for c in itertools.product(range(4), repeat=r) if all(c[i] != c[(i + 1) % r] for i in range(r))})
    rc_idx = {c: i for i, c in enumerate(ring_classes)}
    def extend(c):
        for col in itertools.product(range(4), repeat=len(INT)):
            ic = dict(zip(INT, col))
            if all(not any(c[p] == ic[v] for p in RP[v]) and not any(ic[w] == ic[v] for w in IA[v]) for v in INT): return list(col)
        return None
    ext = {c: extend(c) for c in ring_classes}
    level = {c: 0 for c in ring_classes if ext[c] is not None}
    E0 = len(level)
    def noncrossing(blocks):
        lab = {p: bi for bi, b in enumerate(blocks) for p in b}
        return not any(lab[a] == lab[c] and lab[b] == lab[d] and lab[a] != lab[b] for a, b, c, d in itertools.combinations(range(r), 4))
    def structures(c, pi):
        """All consistent chain structures: partitions of each colour pair's ring positions, ring edges inside blocks, jointly non-crossing."""
        P, Q = pi
        posP = [i for i in range(r) if c[i] in P]; posQ = [i for i in range(r) if c[i] in Q]
        def ok_edges(parts):
            lab = {p: bi for bi, b in enumerate(parts) for p in b}
            return all(lab[i] == lab[(i + 1) % r] for i in lab if (i + 1) % r in lab)
        PP = [p for p in set_partitions(posP) if ok_edges(p)]; QQ = [q for q in set_partitions(posQ) if ok_edges(q)]
        for p in PP:
            for q in QQ:
                if noncrossing(p + q): yield p, q
    def flips(c, pi, p, q):
        for side, blocks, pair in ((0, p, pi[0]), (1, q, pi[1])):
            a, b = pair
            for rr in range(1, len(blocks) + 1):
                for sub in itertools.combinations(range(len(blocks)), rr):
                    cc = list(c)
                    for bi in sub:
                        for pos in blocks[bi]: cc[pos] = b if c[pos] == a else a
                    yield side, sub, Hole.canon(cc)
    rounds = [E0]; cert = {}
    while True:
        good = set(level); new = {}
        for c in ring_classes:
            if c in good: continue
            best = None
            for pi in PARTS:
                st = list(structures(c, pi)); ok = True; rec = []
                for p, q in st:
                    found = None
                    for side, sub, tgt in flips(c, pi, p, q):
                        if tgt in good and (found is None or len(sub) < len(found[1])): found = (side, sub, tgt)
                    if found is None: ok = False; break
                    rec.append((p, q, found))
                if ok and st and (best is None or len(st) < len(best[1])): best = (pi, rec)
            if best: new[c] = best
        if not new: break
        for c, bst in new.items(): level[c] = len(rounds); cert[c] = bst
        rounds.append(len(new))
    out = {'ring': RING, 'interior': {str(k): v for k, v in RSST.items()}, 'classes': [],
           'counts': {'classes': len(ring_classes), 'extend': E0, 'rounds': rounds[1:], 'allGood': len(level) == len(ring_classes)}}
    for c in ring_classes:
        rec = {'c': list(c), 'ext': ext[c], 'level': level.get(c)}
        if c in cert and full:
            pi, st = cert[c]
            rec['pi'] = [list(pi[0]), list(pi[1])]
            rec['structs'] = [{'P': p, 'Q': q, 'side': f[0], 'sub': list(f[1]), 'to': rc_idx[f[2]]} for p, q, f in st]
        out['classes'].append(rec)
    if full:
        for rec in out['classes']:
            for s in rec.get('structs', []): assert out['classes'][s['to']]['level'] < rec['level']
    return out, RP

diamond, RPd = dreduce(RSST_DIAMOND, 6)
c2122, _ = dreduce(RSST_2122, 7, full=False)
print('diamond: classes', diamond['counts'])
print('2.122  : classes', c2122['counts'])
assert diamond['counts']['allGood'] and c2122['counts']['allGood']
assert (diamond['counts']['classes'], diamond['counts']['extend'], diamond['counts']['rounds']) == (31, 16, [4, 3, 4, 3, 1])
assert (c2122['counts']['classes'], c2122['counts']['extend']) == (91, 39)
# interior shape: K4 minus an edge (centres 7, 9; tips 8, 10), interior degrees 5
assert sorted(e for e in {(min(v, w), max(v, w)) for v, nb in RSST_DIAMOND.items() for w in nb if w in RSST_DIAMOND}) == [(7, 8), (7, 9), (7, 10), (8, 9), (9, 10)]
assert len(RPd[7]) == 2 and len(RPd[9]) == 2 and len(RPd[8]) == 3 and len(RPd[10]) == 3
# drawing: ring on a hexagon, interior placed inside; assert no two edges cross
def seg_cross(p1, p2, p3, p4):
    def o(a, b, c): return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
    return o(p1, p2, p3) * o(p1, p2, p4) < 0 and o(p3, p4, p1) * o(p3, p4, p2) < 0
th0 = np.radians(-120)
dpos = {}
for k in range(6): dpos[k + 1] = (0.78 * np.cos(th0 + k * np.pi / 3), 0.78 * np.sin(th0 + k * np.pi / 3))
for v, rad, ang in ((7, 0.26, 30), (9, 0.26, 210), (8, 0.46, 120), (10, 0.46, 300)):
    dpos[v] = (rad * np.cos(th0 + np.radians(ang)), rad * np.sin(th0 + np.radians(ang)))
dedges = sorted({(min(v, w), max(v, w)) for v, nb in RSST_DIAMOND.items() for w in nb} | {(min(k, k % 6 + 1), max(k, k % 6 + 1)) for k in range(1, 7)})
assert not any(len({a, b, c, d}) == 4 and seg_cross(dpos[a], dpos[b], dpos[c], dpos[d]) for (a, b), (c, d) in itertools.combinations(dedges, 2)), 'diamond drawing planar'
diamond['pos'] = {str(k): [round(float(x), 4), round(float(y), 4)] for k, (x, y) in dpos.items()}
diamond['conf2122'] = c2122['counts']
tick('diamond and 2.122 classification done')

# ============================================================== C. the F-cycle graph (order 22, hole 15)
FC_REL = 'backgroundMaterial/planemap-structural/studiointel/fcycle/fcycle_order22.json'
FC_PATH = os.path.join(ROOT, FC_REL)
if os.path.exists(FC_PATH): fc = json.load(open(FC_PATH)); fc_src = FC_REL
else:
    fc = json.loads(subprocess.check_output(['git', 'show', 'origin/studio-intel:' + FC_REL], cwd=ROOT)); fc_src = 'origin/studio-intel:' + FC_REL
ffaces = [tuple(f) for f in fc['faces']]
FG = check_triangulation(ffaces)
FH_HOLE, FLINK = fc['hole'], fc['link']
assert FG['n'] == 22 and FG['deg'][FH_HOLE] == 5
cyc = FG['rot'][FH_HOLE]
assert sorted(cyc) == sorted(FLINK) and all(FLINK[(k + 1) % 5] in FG['adj'][FLINK[k]] for k in range(5)), 'link is a cycle'
fdeg = [FG['deg'][x] for x in FLINK]
assert sorted(fdeg) == [5, 5, 5, 6, 6] and any(fdeg[k:] + fdeg[:k] in ([5, 5, 6, 5, 6], [6, 5, 6, 5, 5]) for k in range(5)), 'link degrees (5,5,6,5,6)'
fdia, f2122 = find_configs(FG, ffaces)
assert len(fdia) == 5, ('five Birkhoff diamonds', len(fdia))
FH = Hole(FG, FH_HOLE, FLINK); FH.build()
tick('F graph: %d colourings of T - v, %d Kempe classes' % (len(FH.states), FH.ncls))
# JSON states -> canonical indices
json_states = []
for cs in fc['cycle_canonical_states']:
    col = tuple(cs['state'][str(v)] for v in FH.V)
    assert all(col[FH.pv[a]] != col[FH.pv[b]] for a, b in FG['edges'] if FH_HOLE not in (a, b)), 'proper'
    json_states.append((FH.sidx[Hole.canon(col)], cs))
assert len({i for i, _ in json_states}) == 20
# the F move on exact colourings (fcycle_census.py: swap the {alpha, c(x_{j+3})}-component of x_{j+2})
def F_move(col):
    L = [col[i] for i in FH.Ln]; j = [t for t in range(5) if L[t] == L[(t + 2) % 5]][0]
    x2, x3 = FH.Ln[(j + 2) % 5], FH.Ln[(j + 3) % 5]; al, A = col[x2], col[x3]
    mask = 0
    for a, b, m in FH.comps(col):
        if {a, b} == {al, A} and m >> x2 & 1: mask = m
    assert mask
    return j, al, A, mask, Hole.apply(col, al, A, mask)   # exact (not canonical) colouring, labelled
start = FH.states[json_states[0][0]]
orbit = [start]; fmoves = []
while True:
    j, al, A, mask, nx = F_move(orbit[-1]); fmoves.append((j, al, A, mask))
    if nx == orbit[0]: break
    orbit.append(nx); assert len(orbit) < 1000
assert len(orbit) == 60, 'labelled F-orbit length 60'
orb_idx = [FH.sidx[Hole.canon(c)] for c in orbit]
assert len(set(orb_idx)) == 20 and all(orb_idx[m] == orb_idx[m % 20] for m in range(60)), '20 canonical states, period 20 up to renaming'
assert set(orb_idx) == {i for i, _ in json_states}, "the 20 states are exactly Studio intel's 20"
assert all(FH.kind(i) == 'dl' for i in orb_idx), 'all 20 doubly locked'
jr = {i: cs['radius'] for i, cs in json_states}
assert all(FH.d[i] == jr[i] for i in orb_idx), 'radii agree with the JSON'
rho_hist = collections.Counter(FH.d[i] for i in orb_idx[:20])
assert dict(rho_hist) == {2: 8, 3: 8, 4: 4}, rho_hist
members = sum(1 for i in range(len(FH.states)) if FH.cls[i] == FH.cls[orb_idx[0]])
assert all(FH.cls[i] == FH.cls[orb_idx[0]] for i in orb_idx)
assert min(FH.d[i] for i in range(len(FH.states)) if FH.cls[i] == FH.cls[orb_idx[0]]) == 0, 'the class has a filled state: not targetless'
# per labelled state: first moves toward a fill (all of them), silence, and one shortest route preferring silent moves
def toward(col):
    i = FH.sidx[Hole.canon(col)]; out = []
    for a, b, mask in FH.comps(col):
        j = FH.sidx[FH.canon(FH.apply(col, a, b, mask))]
        if j != i and FH.d[j] == FH.d[i] - 1: out.append((a, b, mask, j))
    return out
fstates = []; silent_canon = set(); json_sil = set()
for m in range(60):
    col = orbit[m]; i = orb_idx[m]
    fm = toward(col)
    firsts = [{'a': a, 'b': b, 'comp': FH.mask_verts(mk), 'link': FH.link_touch(mk), 'silent': int(not FH.link_touch(mk)),
               'to': FH.d[j]} for a, b, mk, j in fm]
    # route: at each step prefer a silent move, then the smallest chain
    route = []; cur = col
    for step in range(FH.d[i]):
        opts = toward(cur)
        def key(o): return (0 if not FH.link_touch(o[2]) else 1, bin(o[2]).count('1'), o[0], o[1], o[2])
        a, b, mk, j = min(opts, key=key)
        route.append({'a': a, 'b': b, 'comp': FH.mask_verts(mk), 'link': FH.link_touch(mk), 'silent': int(not FH.link_touch(mk))})
        cur = FH.apply(cur, a, b, mk)
    assert FH.filled[FH.sidx[Hole.canon(cur)]]
    if any(f['silent'] for f in firsts): silent_canon.add(i)
    j, al, A, mk = fmoves[m]
    fstates.append({'c': list(col), 'k': m % 20, 'd': FH.d[i], 'F': {'a': al, 'b': A, 'comp': FH.mask_verts(mk), 'link': FH.link_touch(mk), 'j': j},
                    'first': firsts, 'route': route})
for i, cs in json_states:
    if any(not fm['link_positions_in_K'] for fm in cs['first_moves_toward_fill']): json_sil.add(i)
assert len(silent_canon) == 8, ('silent first-move count', len(silent_canon))
silent_agree = silent_canon == json_sil
tick('F-cycle: rho %s, silent states %d, JSON agrees on silent set: %s, class size %d' % (dict(rho_hist), len(silent_canon), silent_agree, members))
# per-state silence in canonical order (k = m mod 20)
silent_by_k = [int(orb_idx[k] in silent_canon) for k in range(20)]
fpos, fouter, fgp = make_layout(FG, [list(f) for f in ffaces], iters=5000, far_from=FH_HOLE)
tick('F graph layout done, gaps %s' % fgp)
cyc_vertices = set()
fdata = {
    'source': fc_src, 'graphId': fc['graph'], 'order': FG['n'], 'hole': FH_HOLE, 'link': FLINK, 'linkDeg': fdeg,
    'faces': [list(f) for f in ffaces], 'rot': FG['rot'], 'V': FH.V, 'deg': FG['deg'],
    'pos': [[round(float(x), 4), round(float(y), 4)] for x, y in fpos], 'outer': fouter,
    'diamonds': [{'centres': list(c), 'tips': list(t)} for c, t in fdia], 'conf2122': len(f2122),
    'states': fstates, 'silentByK': silent_by_k,
    'summary': {'colourings': len(FH.states), 'classes': FH.ncls, 'classSize': members, 'rhoHist': {str(k): v for k, v in sorted(rho_hist.items())},
                'silentStates': len(silent_canon), 'jsonSilentAgrees': bool(silent_agree), 'labelledLength': 60, 'canonicalLength': 20,
                'edges': len(FG['edges']), 'separatingTriangles': FG['sep'],
                'degCount': {str(k): v for k, v in sorted(collections.Counter(FG['deg']).items())}},
}

data = {'cages': cages, 'diamond': diamond, 'fcycle': fdata,
        'planarCode': {'graphsInFile': len(graphs), 'index32': ipr_index[32], 'index37': ipr_index[37]}}
with open(os.path.join(HERE, 'data.js'), 'w') as f:
    f.write('// Generated by docs/cages/build_data.py. Do not edit.\n')
    f.write('window.CAGES_DATA = ' + json.dumps(data, separators=(',', ':')) + ';\n')
print('wrote data.js', os.path.getsize(os.path.join(HERE, 'data.js')), 'bytes', round(time.time() - t0, 1), 's')
