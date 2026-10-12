#!/usr/bin/env python3
"""Track I library: Tait-form objects for rigid-isolation (RI) work.

A *Tait instance* is a list of edges (a, b, colour, label) on vertices 0..n, vertex 0 = v (the contracted hole, degree 5,
half-edge labels 'e0'..'e4' with colours (1,1,2,1,3)); every other vertex is cubic and sees colours 1,2,3.
Colour 1 = alpha+mu, 2 = alpha+A, 3 = alpha+B (Z2^2, alpha=00, mu=01, A=10, B=11).

Objects (TrackH README §6 / TrackI README §1):
  H   = M2 u M3 (the {2,3}-subgraph), F12 = M1 u M2, F13 = M1 u M3,
  X   = the F13-trail of v through e1 (DL: it returns via e3), Y = the F13-trail through e4 (DL: returns via e0),
  pi  = swap colours 1<->3 on X;  after pi:  {2,3}' = H ^ X,  {1,2}' = H ^ Y,  {1,3}' = F13.
Everything here is graph-theoretic (no embedding needed) except where a rotation is passed explicitly.
"""
from collections import defaultdict

def ncm(points):
    """all non-crossing perfect matchings of a list of points in cyclic order"""
    if not points:
        yield []; return
    a = points[0]
    for k in range(1, len(points), 2):
        for m1 in ncm(points[1:k]):
            for m2 in ncm(points[k + 1:]):
                yield [(a, points[k])] + m1 + m2

def chord_instances(N):
    """all chord-model instances with N cubic vertices (TrackH th_chord.py model, independent code).
    H = v,u1..uN,v; v-u1 = e2 (colour 2), u_i u_{i+1} colour 3 (i odd) / 2 (i even), uN-v = e4 (colour 3);
    colour-1 chords: non-crossing matching inside on (u's in I) + e3, outside on (u's in O) + e0, e1."""
    U = list(range(1, N + 1))
    Hed = [(0, 1, 2, 'e2')] + [(i, i + 1, 3 if i % 2 else 2, None) for i in range(1, N)] + [(N, 0, 3, 'e4')]
    for mask in range(1 << N):
        I = [u for u in U if mask >> (u - 1) & 1]; O = [u for u in U if not mask >> (u - 1) & 1]
        if len(I) % 2 == 0 or len(O) % 2: continue
        for mi in ncm(I + ['e3']):
            for mo in ncm(O + ['e0', 'e1']):
                E = list(Hed); bad = False
                for a, b in mi + mo:
                    if isinstance(a, str) and isinstance(b, str): bad = True; break
                    if isinstance(a, str): a, b = b, a
                    E.append((a, 0, 1, b) if isinstance(b, str) else (a, b, 1, None))
                if not bad:
                    yield E, (mask, mi, mo)

class Tait:
    def __init__(self, E):
        self.E = E
        self.n = 1 + max(max(a, b) for a, b, _, _ in E)
        self.lab = {l: k for k, (a, b, c, l) in enumerate(E) if l}
        self.inc = defaultdict(list)
        for k, (a, b, c, l) in enumerate(E):
            self.inc[a].append(k); self.inc[b].append(k)

    def other(self, k, x):
        a, b = self.E[k][0], self.E[k][1]
        return b if a == x else a

    def trail(self, S, k0):
        """follow the subgraph S (set of edge ids, every vertex != 0 of degree 0/2 in S) from v along edge k0;
        returns (list of edge ids, label of the closing edge at v)"""
        path = [k0]; x = self.other(k0, 0); k = k0
        while x != 0:
            nx = [t for t in self.inc[x] if t in S and t != k]
            assert len(nx) == 1, (x, nx)
            k = nx[0]; path.append(k); x = self.other(k, x)
        return path, self.E[k][3]

    def ncomp(self, S):
        """number of connected components of the subgraph formed by edge set S (vertices = ends of S)"""
        par = {}
        def f(x):
            par.setdefault(x, x)
            while par[x] != x:
                par[x] = par[par[x]]; x = par[x]
            return x
        for k in S:
            a, b = self.E[k][0], self.E[k][1]
            ra, rb = f(a), f(b)
            if ra != rb: par[ra] = rb
        return len({f(x) for x in par})

    def pairing(self, S):
        """pairing of v's half-edges in S, as frozenset of frozensets of labels"""
        out = set(); used = set()
        for l, k in sorted(self.lab.items()):
            if k in S and k not in used:
                p, l2 = self.trail(S, k); used.add(k); used.add(self.lab[l2])
                out.add(frozenset((l, l2)))
        return frozenset(out)

def P(*pairs):
    return frozenset(frozenset(p) for p in pairs)

DL12 = P(('e0', 'e3'), ('e1', 'e2'))
DL13 = P(('e1', 'e3'), ('e0', 'e4'))
DLimg = P(('e1', 'e4'), ('e2', 'e3'))     # {2,3}' = H^X pairing that makes pi(c) DL
NDLimg = P(('e1', 'e2'), ('e3', 'e4'))

def analyse(E):
    """returns None if not DL; else dict with rigid flag and, for rigid states, the pi-image data."""
    T = Tait(E)
    M = {c: {k for k, e in enumerate(E) if e[2] == c} for c in (1, 2, 3)}
    H = M[2] | M[3]; F12 = M[1] | M[2]; F13 = M[1] | M[3]
    p12 = T.pairing(F12); p13 = T.pairing(F13)
    if p12 != DL12 or p13 != DL13: return None
    r = dict(T=T, M=M, H=H, F12=F12, F13=F13)
    r['k'] = (T.ncomp(H), T.ncomp(F12), T.ncomp(F13))
    r['rigid'] = r['k'] == (1, 1, 1)
    X, _ = T.trail(F13, T.lab['e1']); Y, _ = T.trail(F13, T.lab['e4'])
    X = set(X); Y = set(Y); r['X'] = X; r['Y'] = Y
    HX = H ^ X; HY = H ^ Y; F12X = F12 ^ X      # true {2,3}' = H^X, true {1,2}' = F12^X (= H^Y iff F13 = X u Y)
    r['HX'] = HX; r['HY'] = HY; r['F12X'] = F12X
    r['kHX'] = T.ncomp(HX); r['kHY'] = T.ncomp(HY); r['kF12X'] = T.ncomp(F12X); r['pHX'] = T.pairing(HX)
    r['img_dl'] = r['pHX'] == DLimg
    r['img_rigid'] = r['img_dl'] and r['kHX'] == 1 and r['kF12X'] == 1   # {1,3}' = F13 unchanged; rigid c has it connected
    return r

# ---------- conversion of a primal state (triangulated sphere, rotation system) into a Tait instance ----------

def triangle_faces(rot):
    """faces of a triangulated closed surface (any surface): the triangles {u, r[i], r[i+1]} of consecutive
    neighbours in each vertex's link cycle; checks that every edge lies in exactly two faces."""
    F = set()
    for u, r in enumerate(rot):
        for i in range(len(r)):
            F.add(frozenset((u, r[i], r[(i + 1) % len(r)])))
    F = sorted(F, key=sorted)
    cnt = defaultdict(int)
    for f in F:
        a, b, c = sorted(f)
        for e in ((a, b), (a, c), (b, c)): cnt[e] += 1
    assert all(v == 2 for v in cnt.values()), 'not a closed triangulated surface'
    return F

def primal_to_tait(rot, h, col, roles, j):
    """col: dict vertex->colour (0..3) on V-h; roles (al,mu,A,B); j = frame. Returns the Tait edge list (dual of T,
    with the five faces at h merged into v = 0; dual of link edge x_{j+t} x_{j+t+1} labelled e_t). No orientation used."""
    al, mu, A, B = roles
    z = {al: 0, mu: 1, A: 2, B: 3}          # Z2^2 encoding: alpha=00, mu=01, A=10, B=11 -> colour = z(u) xor z(w)
    F = triangle_faces(rot)
    ef = defaultdict(list)
    for t, f in enumerate(F):
        a, b, c = sorted(f)
        for e in ((a, b), (a, c), (b, c)): ef[e].append(t)
    hf = {t for t, f in enumerate(F) if h in f}
    ren = {}
    def vid(t):
        if t in hf: return 0
        if t not in ren: ren[t] = len(ren) + 1
        return ren[t]
    X = rot[h]; x = [X[(j + t) % 5] for t in range(5)]
    linklab = {frozenset((x[t], x[(t + 1) % 5])): 'e%d' % t for t in range(5)}
    E = []
    for (u, w), (f1, f2) in sorted(ef.items()):
        if h in (u, w): continue
        E.append((vid(f1), vid(f2), z[col[u]] ^ z[col[w]], linklab.get(frozenset((u, w)))))
    return E
