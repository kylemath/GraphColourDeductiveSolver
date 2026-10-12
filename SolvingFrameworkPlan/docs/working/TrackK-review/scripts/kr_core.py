"""TrackK review: independent core (written from scratch; imports nothing from TrackC/TrackI/TrackK).

Maps are oriented triangulations given by a list of oriented faces (u, v, w).  Edges are explicit
records so that multigraph maps (the filled map T°, which may have parallel edges) are handled.
"""
import random
from itertools import permutations, combinations

CYC = {(1, 2, 3), (2, 3, 1), (3, 1, 2)}
PAIRS = list(combinations(range(4), 2))
PARTS = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]


def perm_even(p):
    inv = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            inv += p[i] > p[j]
    return inv % 2 == 0


SIGMA = {}
for a, b, c in permutations(range(4), 3):
    d = ({0, 1, 2, 3} - {a, b, c}).pop()
    SIGMA[(a, b, c)] = 1 if perm_even((d, a, b, c)) else -1


def tait_cw(a, b, c):
    return (a ^ b, b ^ c, c ^ a) in CYC


# ---------------------------------------------------------------- simple oriented triangulations
class Tri:
    """Simple triangulation of a closed orientable surface; dart (u,v) -> third vertex w of face (u,v,w)."""

    def __init__(self, faces):
        self.nxt = {}
        self.adj = {}
        for (a, b, c) in faces:
            for (u, v, w) in ((a, b, c), (b, c, a), (c, a, b)):
                assert (u, v) not in self.nxt, 'dart twice'
                self.nxt[(u, v)] = w
                self.adj.setdefault(u, set()).add(v)
        for (u, v) in self.nxt:
            assert (v, u) in self.nxt, 'incoherent orientation'

    def V(self):
        return sorted(self.adj)

    def faces(self):
        out = []
        for (u, v), w in self.nxt.items():
            if u < v and u < w:
                out.append((u, v, w))
        return out

    def euler(self):
        V = len(self.adj); E = len(self.nxt) // 2; F = len(self.nxt) // 3
        return V - E + F

    def deg(self, v):
        return len(self.adj[v])

    def _del_face(self, u, v, w):
        for (a, b) in ((u, v), (v, w), (w, u)):
            del self.nxt[(a, b)]

    def _add_face(self, u, v, w):
        for (a, b, c) in ((u, v, w), (v, w, u), (w, u, v)):
            self.nxt[(a, b)] = c

    def insert(self, u, v, newv):
        w = self.nxt[(u, v)]
        self._del_face(u, v, w)
        self._add_face(u, v, newv); self._add_face(v, w, newv); self._add_face(w, u, newv)
        self.adj[newv] = {u, v, w}
        for t in (u, v, w):
            self.adj[t].add(newv)

    def can_flip(self, u, v, mindeg=3):
        w = self.nxt[(u, v)]; x = self.nxt[(v, u)]
        if w == x or x in self.adj[w]:
            return False
        return len(self.adj[u]) - 1 >= mindeg and len(self.adj[v]) - 1 >= mindeg

    def flip(self, u, v):
        w = self.nxt[(u, v)]; x = self.nxt[(v, u)]
        self._del_face(u, v, w); self._del_face(v, u, x)
        self._add_face(u, x, w); self._add_face(x, v, w)
        self.adj[u].discard(v); self.adj[v].discard(u)
        self.adj[w].add(x); self.adj[x].add(w)

    def copy(self):
        t = Tri.__new__(Tri)
        t.nxt = dict(self.nxt); t.adj = {k: set(s) for k, s in self.adj.items()}
        return t


def tetra():
    return Tri([(0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 3, 2)])


def bipyramid(m):
    # ring 0..m-1, apices m, m+1
    fs = []
    for i in range(m):
        j = (i + 1) % m
        fs.append((m, i, j)); fs.append((m + 1, j, i))
    return Tri(fs)


def torus_grid(m, k):
    idx = lambda i, j: (i % m) * k + (j % k)
    fs = []
    for i in range(m):
        for j in range(k):
            fs.append((idx(i, j), idx(i + 1, j), idx(i + 1, j + 1)))
            fs.append((idx(i, j), idx(i + 1, j + 1), idx(i, j + 1)))
    return Tri(fs)


def random_tri(base, n, rng, flips, mindeg=3):
    t = base.copy()
    nv = max(t.adj) + 1
    while len(t.adj) < n:
        u, v = rng.choice(list(t.nxt))
        t.insert(u, v, nv); nv += 1
        for _ in range(3):
            a, b = rng.choice(list(t.nxt))
            if t.can_flip(a, b, mindeg):
                t.flip(a, b)
    for _ in range(flips):
        a, b = rng.choice(list(t.nxt))
        if t.can_flip(a, b, mindeg):
            t.flip(a, b)
    return t


def random_min5(n, rng, flips, tries=20000):
    """Random sphere triangulation with min degree 5 (n >= 12, n != 13), or None."""
    for _ in range(20):
        t = random_tri(tetra(), n, rng, 4 * n, 3)
        for _ in range(tries):
            low = [v for v in t.adj if len(t.adj[v]) < 5]
            if not low:
                break
            v = rng.choice(low)
            a = rng.choice(list(t.adj[v])); b = t.nxt[(v, a)]
            y = t.nxt[(b, a)]
            if y != v and y not in t.adj[v] and len(t.adj[a]) >= 6 and len(t.adj[b]) >= 6:
                t.flip(a, b)
            else:
                a, b = rng.choice(list(t.nxt))
                if t.can_flip(a, b, 3) and min(len(t.adj[a]), len(t.adj[b])) >= 5:
                    t.flip(a, b)
        if min(len(s) for s in t.adj.values()) >= 5:
            for _ in range(flips):
                a, b = rng.choice(list(t.nxt))
                if t.can_flip(a, b, 5):
                    t.flip(a, b)
            assert min(len(s) for s in t.adj.values()) >= 5
            return t
    return None


def from_census(line):
    parts = line.split()
    n = int(parts[1])
    rot = [[int(x) for x in r.split(',')] for r in parts[2].split(';')]
    assert len(rot) == n
    for orient in (0, 1):
        fs = set()
        for v in range(n):
            r = rot[v]
            for i in range(len(r)):
                u, w = r[i], r[(i + 1) % len(r)]
                f = (v, u, w) if orient == 0 else (v, w, u)
                m = min(range(3), key=lambda s: f[s])
                fs.add(f[m:] + f[:m])
        try:
            t = Tri(sorted(fs))
            if t.euler() == 2 and len(t.adj) == n:
                return t
        except AssertionError:
            pass
    raise ValueError('bad census line')


# ---------------------------------------------------------------- colourings
def random_colouring(adj, rng, verts=None, limit=200000):
    verts = list(adj) if verts is None else list(verts)
    vs = set(verts)
    order = []
    seen = set()
    start = rng.choice(verts)
    # BFS order from a random start keeps backtracking shallow
    q = [start]; seen.add(start)
    while q:
        v = q.pop(0); order.append(v)
        nb = [u for u in adj[v] if u in vs and u not in seen]
        rng.shuffle(nb)
        for u in nb:
            seen.add(u); q.append(u)
    for v in verts:
        if v not in seen:
            order.append(v); seen.add(v)
    col = {}
    steps = [0]

    def rec(i):
        if i == len(order):
            return True
        steps[0] += 1
        if steps[0] > limit:
            return False
        v = order[i]
        cs = [0, 1, 2, 3]; rng.shuffle(cs)
        used = {col[u] for u in adj[v] if u in col}
        for c in cs:
            if c not in used:
                col[v] = c
                if rec(i + 1):
                    return True
                del col[v]
        return False

    import sys
    sys.setrecursionlimit(10000)
    return col if rec(0) else None


def kempe_component(adj, col, v, other, vs):
    p, q = col[v], other
    comp = {v}; st = [v]
    while st:
        x = st.pop()
        for y in adj[x]:
            if y in vs and y not in comp and col[y] in (p, q):
                comp.add(y); st.append(y)
    return comp


def kempe_swap(adj, col, v, other, vs):
    p = col[v]
    for x in kempe_component(adj, col, v, other, vs):
        col[x] = other if col[x] == p else p


# ---------------------------------------------------------------- union find
def uf_count(nodes, pairs):
    par = {x: x for x in nodes}

    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for a, b in pairs:
        ra, rb = f(a), f(b)
        if ra != rb:
            par[ra] = rb
    return f


# ---------------------------------------------------------------- maps with explicit edges
class Map:
    """faces: list of oriented triples; edges: list of (u, v, fa, fb) with dart u->v in fa and v->u in fb."""

    def __init__(self, verts, faces, edges):
        self.verts = list(verts); self.faces = faces; self.edges = edges

    def validate(self, chi):
        V, E, F = len(self.verts), len(self.edges), len(self.faces)
        assert V - E + F == chi, (V, E, F, chi)
        inc = [0] * F
        for (u, v, fa, fb) in self.edges:
            assert u != v and fa != fb
            assert self._has_dart(fa, u, v) and self._has_dart(fb, v, u)
            inc[fa] += 1; inc[fb] += 1
        assert all(x == 3 for x in inc)
        for f in self.faces:
            assert len(set(f)) == 3

    def _has_dart(self, fi, u, v):
        a, b, c = self.faces[fi]
        return (u, v) in ((a, b), (b, c), (c, a))


def map_of_tri(t):
    faces = []; fid = {}
    for f in t.faces():
        fid[f] = len(faces); faces.append(f)

    def face_of_dart(u, v):
        w = t.nxt[(u, v)]
        f = (u, v, w); m = min(range(3), key=lambda s: f[s])
        return fid[f[m:] + f[:m]]
    edges = []
    for (u, v) in t.nxt:
        if u < v:
            edges.append((u, v, face_of_dart(u, v), face_of_dart(v, u)))
    return Map(t.V(), faces, edges)


def oriented_link(t, h):
    succ = {}
    for a in t.adj[h]:
        succ[a] = t.nxt[(h, a)]     # face (h, a, succ[a])
    a0 = min(succ); L = [a0]
    while succ[L[-1]] != a0:
        L.append(succ[L[-1]])
    assert len(L) == len(t.adj[h])
    return L


def filled_map(t, h, x):
    """T° : delete h, add diagonals x1x3, x1x4 (always as NEW edges).  x = link in roles order x0..x4,
    with faces (h, x_t, x_{t+1}) in T's orientation."""
    faces = []; fid = {}
    for f in t.faces():
        if h in f:
            continue
        fid[f] = len(faces); faces.append(f)
    F1 = len(faces); faces.append((x[1], x[2], x[3]))
    F2 = len(faces); faces.append((x[1], x[3], x[4]))
    F3 = len(faces); faces.append((x[4], x[0], x[1]))
    newdart = {(x[0], x[1]): F3, (x[1], x[2]): F1, (x[2], x[3]): F1, (x[3], x[4]): F2, (x[4], x[0]): F3}

    def face_of_dart(u, v):
        w = t.nxt[(u, v)]
        if w == h:
            return newdart[(u, v)]
        f = (u, v, w); m = min(range(3), key=lambda s: f[s])
        return fid[f[m:] + f[:m]]
    edges = []
    for (u, v) in t.nxt:
        if u < v and h not in (u, v):
            edges.append((u, v, face_of_dart(u, v), face_of_dart(v, u)))
    edges.append((x[1], x[3], F2, F1))   # dart x1->x3 in F2, x3->x1 in F1
    edges.append((x[1], x[4], F3, F2))   # dart x1->x4 in F3, x4->x1 in F2
    verts = [v for v in t.V() if v != h]
    return Map(verts, faces, edges)


# ---------------------------------------------------------------- the per-map analysis (no hole)
def analyse(M, col, genus, want_sep=False):
    """All intermediate quantities of FProof §1-2 for a proper colouring col of the map M.
    Returns dict; raises nothing (checks are done by the caller)."""
    V = M.verts; n = len(V)
    size = [0] * 4
    for v in V:
        size[col[v]] += 1
    degA = [0] * 4
    ecount = {}
    for (u, v, fa, fb) in M.edges:
        a, b = col[u], col[v]
        assert a != b, 'improper'
        degA[a] += 1; degA[b] += 1
        k = (min(a, b), max(a, b)); ecount[k] = ecount.get(k, 0) + 1
    # chains per pair (with representatives)
    p = {}; find = {}
    for (X, Y) in PAIRS:
        nodes = [v for v in V if col[v] in (X, Y)]
        f = uf_count(nodes, [(u, v) for (u, v, _, _) in M.edges if {col[u], col[v]} == {X, Y}])
        find[(X, Y)] = f
        p[(X, Y)] = len({f(v) for v in nodes})
    N = sum(p.values())
    # cw and Fisk degree
    cw = 0; dt = {}
    for (a, b, c) in M.faces:
        ca, cb, cc = col[a], col[b], col[c]
        cw += tait_cw(ca, cb, cc)
        t = frozenset((ca, cb, cc)); dt[t] = dt.get(t, 0) + SIGMA[(ca, cb, cc)]
    ds = [dt.get(frozenset(s), 0) for s in combinations(range(4), 3)]
    F = len(M.faces)
    res = dict(n=n, N=N, cw=cw, F=F, ds=ds, degA=degA, p=p, size=size)
    # Tait 2-factors
    parts = []
    for (XY, ZW) in PARTS:
        cls = lambda c: 0 if c in XY else 1
        cross = [i for i, (u, v, fa, fb) in enumerate(M.edges) if cls(col[u]) != cls(col[v])]
        fdeg = [0] * F
        for i in cross:
            fdeg[M.edges[i][2]] += 1; fdeg[M.edges[i][3]] += 1
        two_reg = all(x == 2 for x in fdeg)
        ff = uf_count(range(F), [(M.edges[i][2], M.edges[i][3]) for i in cross])
        cyc_of_edge = {i: ff(M.edges[i][2]) for i in cross}
        cycles = sorted(set(cyc_of_edge.values()))
        k = len(cycles)
        # regions = chains of XY and ZW; boundary curves per chain
        fXY, fZW = find[XY], find[ZW]

        def chain(v):
            return ('XY', fXY(v)) if col[v] in XY else ('ZW', fZW(v))
        bnd = {}
        cyc_sides = {c: set() for c in cycles}
        for i in cross:
            u, v = M.edges[i][0], M.edges[i][1]
            for w in (u, v):
                q = chain(w); bnd.setdefault(q, set()).add(cyc_of_edge[i])
                cyc_sides[cyc_of_edge[i]].add(q)
        # each curve borders exactly one XY region and one ZW region
        sides_ok = all(len(s) == 2 and {q[0] for q in s} == {'XY', 'ZW'} for s in cyc_sides.values())
        # chi of each chain (V - E) and its genus 2 - b - chi = 2 g
        Vq = {}; Eq = {}
        for v in V:
            q = chain(v); Vq[q] = Vq.get(q, 0) + 1
        for i, (u, v, fa, fb) in enumerate(M.edges):
            if cls(col[u]) == cls(col[v]):
                q = chain(u); Eq[q] = Eq.get(q, 0) + 1
        G = 0; gen_ok = True; nreg = len(Vq)
        for q in Vq:
            twog = 2 - len(bnd.get(q, ())) - (Vq[q] - Eq.get(q, 0))
            if twog < 0 or twog % 2:
                gen_ok = False
            G += twog // 2
        pXY = p[XY]; pZW = p[ZW]
        sumXYb = sum(len(bnd.get(q, ())) for q in Vq if q[0] == 'XY')
        part = dict(k=k, two_reg=two_reg, sides_ok=sides_ok, gen_ok=gen_ok, G=G, nreg=nreg,
                    a_exact=(2 * pXY - k == size[XY[0]] + size[XY[1]] - ecount.get(XY, 0)) if G == 0 else None,
                    a_gen=(2 * pXY - 2 * sum((2 - len(bnd.get(q, ())) - (Vq[q] - Eq.get(q, 0))) // 2
                                             for q in Vq if q[0] == 'XY') - k
                           == size[XY[0]] + size[XY[1]] - ecount.get(XY, 0)),
                    a_mod2=((k - size[XY[0]] - size[XY[1]] - ecount.get(XY, 0)) % 2 == 0),
                    b=(pXY + pZW == k + 1), b_gen=(pXY + pZW == k + 1 - genus + G),
                    sumXYb=(sumXYb == k))
        if want_sep:
            # contractibility on the torus: a simple closed curve is null-homotopic iff it separates
            allsep = True
            for c in cycles:
                f2 = uf_count(V, [(u, v) for i, (u, v, fa, fb) in enumerate(M.edges)
                                  if not (i in cyc_of_edge and cyc_of_edge[i] == c)])
                if len({f2(v) for v in V}) == 1:
                    allsep = False; break
            part['allsep'] = allsep
        parts.append(part)
    res['parts'] = parts
    res['G'] = sum(pt['G'] for pt in parts)
    return res


def lemma0_checks(r):
    """Lemma 0, Lemma 0' and F0 pieces; returns dict of booleans (sphere unless noted)."""
    ds = r['ds']; d = ds[0]; ccw = r['F'] - r['cw']
    return dict(
        d_equal=len(set(ds)) == 1,
        cw_minus_ccw=(r['cw'] - ccw == 4 * d),
        cw_formula=(r['cw'] == r['F'] // 2 + 2 * d),
        degA_parity=all((r['degA'][A] - d) % 2 == 0 for A in range(4)),
    )
