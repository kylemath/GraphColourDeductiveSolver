"""Track I review: independent core (surfaces, colourings, primal Kempe chains).

Written from scratch for the review; imports nothing from TrackH/TrackI/TrackF.
A surface is a list of triangles (frozensets of 3 vertex ids), each edge in exactly
two triangles, each vertex link a single cycle (simplicial closed surface).
"""
import random
from collections import defaultdict

# ---------------------------------------------------------------- surfaces

class Surf:
    def __init__(self, faces):
        self.faces = set(frozenset(f) for f in faces)
        self.rebuild()

    def rebuild(self):
        self.adj = defaultdict(set)
        self.ef = defaultdict(list)  # edge -> faces
        for f in self.faces:
            a, b, c = tuple(f)
            for u, v in ((a, b), (b, c), (a, c)):
                self.adj[u].add(v); self.adj[v].add(u)
                self.ef[frozenset((u, v))].append(f)
        self.V = sorted(self.adj)

    def euler(self):
        return len(self.V) - len(self.ef) + len(self.faces)

    def check(self):
        for e, fs in self.ef.items():
            if len(fs) != 2:
                return False
        for v in self.V:
            if self.link(v) is None:
                return False
        return True

    def link(self, h):
        """cyclic order of the link of h (list), or None if not a single cycle."""
        nb = defaultdict(list)
        for f in self.faces:
            if h in f:
                a, b = tuple(f - {h})
                nb[a].append(b); nb[b].append(a)
        if any(len(x) != 2 for x in nb.values()):
            return None
        start = next(iter(nb))
        cyc = [start]; prev = None; cur = start
        while True:
            nxts = nb[cur]
            nx = nxts[0] if nxts[0] != prev else nxts[1]
            if nx == start:
                break
            cyc.append(nx); prev, cur = cur, nx
            if len(cyc) > len(nb):
                return None
        if len(cyc) != len(nb):
            return None
        return cyc

    def flip(self, u, v, mindeg=3):
        e = frozenset((u, v))
        fs = self.ef.get(e)
        if not fs or len(fs) != 2:
            return False
        (w,) = tuple(fs[0] - e); (x,) = tuple(fs[1] - e)
        if w == x or x in self.adj[w]:
            return False
        if len(self.adj[u]) - 1 < mindeg or len(self.adj[v]) - 1 < mindeg:
            return False
        self.faces.discard(fs[0]); self.faces.discard(fs[1])
        self.faces.add(frozenset((u, w, x))); self.faces.add(frozenset((v, w, x)))
        self.rebuild()
        return True

    def insert(self, f):
        """stellar subdivision of face f"""
        n = max(self.V) + 1
        a, b, c = tuple(f)
        self.faces.discard(f)
        for p, q in ((a, b), (b, c), (a, c)):
            self.faces.add(frozenset((p, q, n)))
        self.rebuild()
        return n


def from_rotation(rot):
    faces = set()
    for v, r in enumerate(rot):
        k = len(r)
        for i in range(k):
            faces.add(frozenset((v, r[i], r[(i + 1) % k])))
    return Surf(faces)


def parse_census_line(line):
    parts = line.split()
    name, n, rots = parts[0], int(parts[1]), parts[2]
    rot = [[int(x) for x in r.split(',')] for r in rots.split(';')]
    assert len(rot) == n
    return name, from_rotation(rot)


ICOSA_NONE = None

def tetra():
    return Surf([(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)])

def rp2_6():
    # hemi-icosahedron, 6 vertices, 10 faces
    F = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 5), (0, 5, 1),
         (1, 2, 4), (2, 3, 5), (3, 4, 1), (4, 5, 2), (5, 1, 3)]
    s = Surf(F)
    assert s.check() and s.euler() == 1, (s.check(), s.euler())
    return s

def torus_grid(m, k):
    F = []
    idx = lambda i, j: (i % m) * k + (j % k)
    for i in range(m):
        for j in range(k):
            F.append((idx(i, j), idx(i + 1, j), idx(i + 1, j + 1)))
            F.append((idx(i, j), idx(i, j + 1), idx(i + 1, j + 1)))
    s = Surf(F)
    assert s.check() and s.euler() == 0
    return s


def random_surface(base, n, rng, nflips, mindeg=3, target_min5=False):
    s = Surf(base.faces)
    while len(s.V) < n:
        f = rng.choice(sorted(s.faces, key=lambda f: tuple(sorted(f))))
        s.insert(f)
        # flips around to spread
        for _ in range(3):
            e = rng.choice(list(s.ef))
            u, v = tuple(e)
            s.flip(u, v, mindeg)
    def deficit(S):
        return sum(max(0, 5 - len(S.adj[v])) for v in S.V)
    edges = lambda: list(s.ef)
    for it in range(nflips):
        e = rng.choice(edges())
        u, v = tuple(e)
        if target_min5:
            d0 = deficit(s)
            fs = s.ef[e]
            (w,) = tuple(fs[0] - e); (x,) = tuple(fs[1] - e)
            if w == x or x in s.adj[w]:
                continue
            # predicted deficit change
            dd = 0
            for y, ch in ((u, -1), (v, -1), (w, 1), (x, 1)):
                dg = len(s.adj[y])
                dd += max(0, 5 - (dg + ch)) - max(0, 5 - dg)
            if dd > 0 and (d0 == 0 or rng.random() > 0.05):
                continue
            s.flip(u, v, 3)
        else:
            s.flip(u, v, mindeg)
    return s


def min_degree(s):
    return min(len(s.adj[v]) for v in s.V)

# ---------------------------------------------------------------- colourings of T - h

def graph_minus(s, h):
    V = [v for v in s.V if v != h]
    ix = {v: i for i, v in enumerate(V)}
    nbr = [[ix[w] for w in s.adj[v] if w != h] for v in V]
    return V, ix, nbr


def enumerate_colourings(nbr, limit=None, order=None):
    """all proper 4-colourings up to colour permutation (canonical: first-use order)."""
    n = len(nbr)
    if order is None:
        # BFS order
        order = []; seen = [False] * n
        for s0 in range(n):
            if seen[s0]:
                continue
            seen[s0] = True; q = [s0]
            while q:
                x = q.pop(0); order.append(x)
                for y in sorted(nbr[x], key=lambda y: -len(nbr[y])):
                    if not seen[y]:
                        seen[y] = True; q.append(y)
    pos = {v: i for i, v in enumerate(order)}
    back = [[w for w in nbr[v] if pos[w] < pos[v]] for v in order]
    col = [-1] * n
    out = []
    def rec(i, used):
        if limit is not None and len(out) >= limit:
            return
        if i == n:
            out.append(tuple(col)); return
        v = order[i]
        forb = 0
        for w in back[i]:
            forb |= 1 << col[w]
        for c in range(min(4, used + 1)):
            if not (forb >> c) & 1:
                col[v] = c
                rec(i + 1, max(used, c + 1))
        col[v] = -1
    import sys
    sys.setrecursionlimit(10000)
    rec(0, 0)
    return out


def normalise(col):
    m = {}; out = []
    for c in col:
        if c not in m:
            m[c] = len(m)
        out.append(m[c])
    return tuple(out)


def random_colouring(nbr, rng, tries=200):
    n = len(nbr)
    for _ in range(tries):
        order = list(range(n)); rng.shuffle(order)
        # DSATUR-like randomized backtracking with node limit
        col = [-1] * n
        cnt = [0]
        def rec(k):
            cnt[0] += 1
            if cnt[0] > 20000:
                return False
            # choose uncoloured vertex with max saturation
            best = -1; bs = -1
            for v in range(n):
                if col[v] < 0:
                    sat = len({col[w] for w in nbr[v] if col[w] >= 0})
                    if sat > bs:
                        bs = sat; best = v
            if best < 0:
                return True
            cs = [0, 1, 2, 3]; rng.shuffle(cs)
            for c in cs:
                if all(col[w] != c for w in nbr[best]):
                    col[best] = c
                    if rec(k + 1):
                        return True
            col[best] = -1
            return False
        if rec(0):
            return tuple(col)
    return None


def component(nbr, col, start, p, q):
    seen = {start}; st = [start]
    while st:
        x = st.pop()
        for y in nbr[x]:
            if y not in seen and (col[y] == p or col[y] == q):
                seen.add(y); st.append(y)
    return seen


def kempe_swap(nbr, col, start, other):
    p = col[start]; q = other
    K = component(nbr, col, start, p, q)
    c = list(col)
    for x in K:
        c[x] = q if col[x] == p else p
    return tuple(c)


def n_components(nbr, col, p, q):
    seen = set(); k = 0
    for v in range(len(col)):
        if (col[v] == p or col[v] == q) and v not in seen:
            k += 1
            seen.add(v); st = [v]
            while st:
                x = st.pop()
                for y in nbr[x]:
                    if y not in seen and (col[y] == p or col[y] == q):
                        seen.add(y); st.append(y)
    return k


PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

def N_total(nbr, col):
    return sum(n_components(nbr, col, p, q) for p, q in PAIRS)

# ---------------------------------------------------------------- hole state

def hole_state(nbr, col, L):
    """L = link indices (in T-h indexing) in cyclic order.
    returns None if filled (<=3 link colours), else dict with j, roles, locks, etc."""
    lc = [col[x] for x in L]
    if len(set(lc)) < 4:
        return None
    js = [j for j in range(5) if lc[j] == lc[(j + 2) % 5]]
    assert len(js) == 1, lc
    j = js[0]
    x = [L[(j + t) % 5] for t in range(5)]
    al, mu, A, B = col[x[0]], col[x[1]], col[x[3]], col[x[4]]
    assert len({al, mu, A, B}) == 4
    K_muA = component(nbr, col, x[1], mu, A)
    K_muB = component(nbr, col, x[1], mu, B)
    L1 = x[3] in K_muA
    L2 = x[4] in K_muB
    return dict(j=j, x=x, al=al, mu=mu, A=A, B=B, L1=L1, L2=L2, DL=L1 and L2)


def pi_move(nbr, col, st):
    """swap of K_{alpha A}(x_{j+2}); None if x_j in K."""
    x = st['x']
    K = component(nbr, col, x[2], st['al'], st['A'])
    if x[0] in K:
        return None, K
    c = list(col)
    for v in K:
        c[v] = st['A'] if col[v] == st['al'] else st['al']
    return tuple(c), K


def counts6(nbr, col, st):
    a, m, A, B = st['al'], st['mu'], st['A'], st['B']
    return tuple(n_components(nbr, col, p, q) for p, q in
                 ((a, m), (A, B), (a, A), (m, B), (a, B), (m, A)))

RIGID = (1, 1, 2, 1, 2, 1)
