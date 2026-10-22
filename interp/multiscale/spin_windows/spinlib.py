"""Spin / disc-Stokes library for coloured near-triangulated discs (windows).
Conventions as in ../vortex_spin.py: colours in Z2^2={0,1,2,3}, label(uv)=c(u)^c(v),
a step a->b in a cyclic label sequence is forward iff b==a%3+1; spin w=(f-b)/3."""
import itertools, random
import networkx as nx
from pysat.solvers import Minisat22

def parse_window(r, m, ringadj, intadj):
    """vertices: ring 0..r-1 (cycle), interior r..r+m-1. returns adjacency sets."""
    n = r + m; adj = [set() for _ in range(n)]
    def add(a, b): adj[a].add(b); adj[b].add(a)
    for i in range(r): add(i, (i + 1) % r)
    ra = ringadj.split(';'); ia = intadj.split(';')
    for j in range(m):
        if ra[j] not in ('-', ''):
            for x in ra[j].split(','): add(r + j, int(x))
        if ia[j] not in ('-', ''):
            for x in ia[j].split(','): add(r + j, r + int(x))
    return adj

def embed_disc(adj, r):
    """Rotation system of a near-triangulated disc whose outer face is the ring 0..r-1.
    Adds an apex joined to the ring (-> sphere triangulation, unique embedding) and uses networkx.
    Returns rot: interior v -> cyclic neighbour list; ring v -> fan list from one ring neighbour to the other
    (same orientation for all), and ring successor order (ring traversed with interior consistently on one side)."""
    n = len(adj); G = nx.Graph(); A = n
    for v in range(n):
        for u in adj[v]: G.add_edge(v, u)
    for i in range(r): G.add_edge(A, i)
    ok, emb = nx.check_planarity(G)
    if not ok: raise ValueError('not planar')
    rot = {}
    for v in range(n):
        cw = list(emb.neighbors_cw_order(v))
        if v < r:
            k = cw.index(A); cw = cw[k + 1:] + cw[:k]   # fan: ring nbr, interior..., ring nbr
        rot[v] = cw
    # triangle-count sanity: every consecutive pair in a rotation must be adjacent (triangulated)
    for v in range(n):
        L = rot[v]; pairs = list(zip(L, L[1:])) + ([(L[-1], L[0])] if v >= r else [])
        for a, b in pairs:
            if b not in adj[a]: raise ValueError('not triangulated at %d' % v)
    succ = {v: rot[v][0] for v in range(r)}   # ring walk direction induced by the embedding
    return rot, succ

def steps(labels, cyclic):
    f = b = 0; L = labels; rng = range(len(L)) if cyclic else range(len(L) - 1)
    for i in rng:
        a, c = L[i], L[(i + 1) % len(L)]
        if c == a % 3 + 1: f += 1
        else: b += 1
    return f - b

def spin(col, rot, v):
    t = steps([col[v] ^ col[u] for u in rot[v]], True); assert t % 3 == 0; return t // 3

def fan_turn(col, rot, v):
    return steps([col[v] ^ col[u] for u in rot[v]], False)

def triangles(adj, rot, r):
    T = set()
    for v in range(len(adj)):
        L = rot[v]; pairs = list(zip(L, L[1:])) + ([(L[-1], L[0])] if v >= r else [])
        for a, b in pairs: T.add(tuple(sorted((v, a, b))))
    return T

def orient_sign(col, rot, tri):
    """+1 if the triangle is mapped preserving orientation, read off at its first vertex."""
    v, a, b = tri; L = rot[v]
    # find the order of a,b around v
    for x, y in list(zip(L, L[1:])) + [(L[-1], L[0])]:
        if (x, y) == (a, b): p, q = a, b; break
        if (x, y) == (b, a): p, q = b, a; break
    else: raise ValueError
    l1, l2 = col[v] ^ col[p], col[v] ^ col[q]
    return 1 if l2 == l1 % 3 + 1 else -1

def perm_sign(p):
    s = 1; p = list(p)
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]: s = -s
    return s

def ring_word(succ, r):
    w = [0]; 
    while len(w) < r: w.append(succ[w[-1]])
    return w   # ring vertex order along the embedding-induced direction

def flux(word_cols):
    """delta[c][d] = #ring steps c->d minus #d->c along the induced direction."""
    D = [[0] * 4 for _ in range(4)]; r = len(word_cols)
    for i in range(r):
        c, d = word_cols[i], word_cols[(i + 1) % r]; D[c][d] += 1; D[d][c] -= 1
    return D

def Psi12(word_cols, s=1):
    """12*Psi_a = s * sum_{b!=a} sgn(a,b,c,d)*delta(c->d), {c,d} the complement, c<d."""
    D = flux(word_cols); out = []
    for a in range(4):
        tot = 0
        for b in range(4):
            if b == a: continue
            c, d = [x for x in range(4) if x not in (a, b)]
            tot += perm_sign((a, b, c, d)) * D[c][d]
        out.append(s * tot)
    return out

def sat_colourings(adj, fixed=None, k=1, seed=0, randomise=True):
    n = len(adj); var = lambda v, c: 4 * v + c + 1; rng = random.Random(seed); out = []
    s = Minisat22()
    for v in range(n):
        s.add_clause([var(v, c) for c in range(4)])
        for c in range(4):
            for c2 in range(c + 1, 4): s.add_clause([-var(v, c), -var(v, c2)])
        for u in adj[v]:
            if u > v:
                for c in range(4): s.add_clause([-var(v, c), -var(u, c)])
    base = [var(v, c) for v, c in (fixed or {}).items()]
    for _ in range(k):
        ass = list(base)
        if randomise:
            for v in rng.sample(range(n), n):
                if fixed and v in fixed: continue
                a = var(v, rng.randrange(4))
                if s.solve(assumptions=ass + [a]): ass.append(a)
        if not s.solve(assumptions=ass): s.delete(); return out
        mset = set(x for x in s.get_model() if x > 0)
        out.append([next(c for c in range(4) if var(v, c) in mset) for v in range(n)])
    s.delete(); return out
