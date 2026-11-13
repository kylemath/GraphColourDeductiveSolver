# W16: torus (doubly periodic) triangulations as oriented face lists, flips, canonical codes, local 2-ball words.
import random, collections

def nf(f):
    a, b, c = f; m = min(f)
    return (a, b, c) if a == m else (b, c, a) if b == m else (c, a, b)

class Torus:
    """simplicial triangulation of the torus; faces are ccw triples. n vertices 0..n-1."""
    def __init__(self, n, faces):
        self.n = n; self.faces = set(nf(f) for f in faces); self.rebuild()
    def rebuild(self):
        self.opp = {}; self.adj = [set() for _ in range(self.n)]
        for (a, b, c) in self.faces:
            for (x, y, z) in ((a, b, c), (b, c, a), (c, a, b)):
                assert (x, y) not in self.opp, ('dup dart', x, y)
                self.opp[(x, y)] = z; self.adj[x].add(y); self.adj[y].add(x)
        for (x, y) in self.opp: assert (y, x) in self.opp, ('unpaired', x, y)
        self.deg = [len(a) for a in self.adj]
    def check(self):
        V, E, F = self.n, len(self.opp) // 2, len(self.faces)
        assert V - E + F == 0, ('euler', V, E, F)
        for v in range(self.n):
            r = self.rot(v); assert len(r) == self.deg[v] and len(set(r)) == len(r), ('rot', v)
        return True
    def rot(self, v):
        """ccw neighbour cycle of v: succ(b) = opp[(v, b)] (face (v, b, c) ccw => c follows b around v)."""
        b0 = min(self.adj[v]); r = [b0]
        while True:
            nb = self.opp[(v, r[-1])]
            if nb == b0: break
            r.append(nb)
            if len(r) > self.n + 2: raise RuntimeError('rot loop')
        return r
    def flip(self, u, v):
        """flip edge uv; returns False if not allowed (would create a multi-edge)."""
        if (u, v) not in self.opp: return False
        a = self.opp[(u, v)]; b = self.opp[(v, u)]
        if a == b or b in self.adj[a]: return False
        f1 = nf((u, v, a)); f2 = nf((v, u, b))
        newf = [(a, u, b), (b, v, a)]
        self.faces.discard(f1); self.faces.discard(f2); self.faces.update(nf(f) for f in newf)
        # incremental update
        for (x, y) in ((u, v), (v, a), (a, u), (v, u), (u, b), (b, v)): del self.opp[(x, y)]
        for (p, q, r) in newf:
            for (x, y, z) in ((p, q, r), (q, r, p), (r, p, q)): self.opp[(x, y)] = z
        self.adj[u].discard(v); self.adj[v].discard(u); self.adj[a].add(b); self.adj[b].add(a)
        self.deg[u] -= 1; self.deg[v] -= 1; self.deg[a] += 1; self.deg[b] += 1
        return True
    def copy(self): return Torus(self.n, list(self.faces))

def lattice_torus(p, q, r):
    """triangular lattice Z^2 / <(p, 0), (q, r)>, n = p r vertices; neighbours (+-1,0), (0,+-1), (1,-1), (-1,1)."""
    def vid(i, j):
        k, j2 = divmod(j, r); i2 = (i - q * k) % p; return j2 * p + i2
    faces = []
    for j in range(r):
        for i in range(p):
            a, b, c, d = vid(i, j), vid(i + 1, j), vid(i, j + 1), vid(i + 1, j + 1)
            faces.append((a, b, c)); faces.append((b, d, c))
    return Torus(p * r, faces)

def letter(d): return min(d, 9)

def words(T, v):
    """(link letters, apex letters, link vertices, apex vertices) of v, ccw; apex s_i over edge (w_i, w_{i+1})."""
    r = T.rot(v); d = len(r)
    ap = [T.opp[(r[(i + 1) % d], r[i])] for i in range(d)]
    return [letter(T.deg[x]) for x in r], [letter(T.deg[x]) for x in ap], r, ap

def dihedral(w, s):
    """all 2d orientations (w', s') in the patmatch convention."""
    d = len(w); out = []
    for refl in (False, True):
        for r in range(d):
            if refl: out.append((tuple(w[(r - i) % d] for i in range(d)), tuple(s[(r - i - 1) % d] for i in range(d))))
            else: out.append((tuple(w[(i + r) % d] for i in range(d)), tuple(s[(i + r) % d] for i in range(d))))
    return out
def canon_ws(w, s):
    d = len(w); m = min(w); best = None
    for r in range(d):
        if w[r] != m: continue
        c1 = (tuple(w[(i + r) % d] for i in range(d)), tuple(s[(i + r) % d] for i in range(d)))
        c2 = (tuple(w[(r - i) % d] for i in range(d)), tuple(s[(r - i - 1) % d] for i in range(d)))
        for c in (c1, c2):
            if best is None or c < best: best = c
    return best

def canon_code(T):
    """canonical code of the oriented-or-reflected rotation system (BFS numbering from every dart, both orientations)."""
    best = None; rots = {v: T.rot(v) for v in range(T.n)}
    for refl in (False, True):
        R = {v: (rots[v][::-1] if refl else rots[v]) for v in rots}
        for v0 in range(T.n):
            for b0 in R[v0]:
                num = {v0: 0}; order = [v0]; code = []; first = {v0: b0}; k = 0; dead = False
                while k < len(order):
                    x = order[k]; rx = R[x]; j = rx.index(first[x]); dx = len(rx)
                    code.append(dx)
                    for t in range(dx):
                        y = rx[(j + t) % dx]
                        if y not in num:
                            num[y] = len(order); order.append(y); first[y] = x
                        code.append(num[y])
                    k += 1
                    if best is not None and code > best[:len(code)]: dead = True; break
                if not dead and (best is None or code < best): best = code
    return tuple(best)
