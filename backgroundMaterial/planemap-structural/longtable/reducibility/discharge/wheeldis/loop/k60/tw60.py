"""EXPLORE round 60 add-on (a) (Long Table 05:26Z, from Kyle's logbook): the C3 "triple wheel".  Three mutually adjacent
7s u0, u1, u2, each of row type LK/SV (default the face row 7766556/6567566), paired Index 0 to Index 1 around the
triangle: u_i's link w0, w1 are u_(i+1), u_(i+2) in counterclockwise order.  The patch is the free disc (no
identifications) in which every vertex given a degree by some row (link w_i, apex s_i; letter 9 never) is closed with
it; a vertex asked for two degrees, a degree below its disc degree, or a forbidden chord is a clash.  Windows (r_i = the
apex s4 of u_i's 5-5-5 face w4 w5 s4, closing the triangle):
  C_13 = B1(u0) u B1(u1) minus u2, plus r0, r1;  C_14 = B1(u0) u B1(u1) plus r0, r1;  C_18 = the three B1(u_i) plus r0..r2.
Each window's interior gets its ring from the faces, written as a kc line (k60/tw/tw60_windows.txt).
usage: python3 tw60.py [LK SV]"""
import sys, os, collections
H = os.path.dirname(os.path.abspath(__file__))
LK = [int(c) for c in (sys.argv[1] if len(sys.argv) > 1 else '7766556')]
SV = [int(c) for c in (sys.argv[2] if len(sys.argv) > 2 else '6567566')]
d = len(LK)

class Clash(Exception): pass

class ODisc:
    """Disc triangulation with counterclockwise triangles; the boundary B is kept with the disc on its left."""
    def __init__(self):
        self.n = 0; self.tris = []; self.adj = collections.defaultdict(set); self.B = []; self.deg = {}; self.lab = {}
    def new(self):
        v = self.n; self.n += 1; self.lab[v] = 'v%d' % v; return v
    def tri(self, a, b, c):
        self.tris.append((a, b, c))
        for x, y in ((a, b), (b, c), (c, a)): self.adj[x].add(y); self.adj[y].add(x)
    def wheel(self, k):
        c = self.new(); W = [self.new() for _ in range(k)]
        for i in range(k): self.tri(c, W[i], W[(i + 1) % k])
        self.B = list(W); self.deg[c] = k; return c, W
    def close(self, v, k):
        if v in self.deg:
            if self.deg[v] != k: raise Clash('%s asked for %d and %d' % (self.lab[v], self.deg[v], k))
            return
        i = self.B.index(v); a, b = self.B[i - 1], self.B[(i + 1) % len(self.B)]; m = k - len(self.adj[v])
        if m < 0: raise Clash('%s needs %d but already has %d neighbours' % (self.lab[v], k, len(self.adj[v])))
        if m == 0:
            if len(self.B) <= 3 or b in self.adj[a]: raise Clash('closing %s would need a chord' % self.lab[v])
            self.tri(v, a, b); self.B.pop(i)
        else:
            X = [self.new() for _ in range(m)]; seq = [a] + X + [b]
            for j in range(len(seq) - 1): self.tri(v, seq[j], seq[j + 1])
            self.B[i:i + 1] = X
        self.deg[v] = k
    def rot(self, v):
        """Counterclockwise rotation of a closed vertex."""
        nx = {}
        for t in self.tris:
            if v in t:
                j = t.index(v); nx[t[(j + 1) % 3]] = t[(j + 2) % 3]
        start = min(nx); out = [start]
        while nx[out[-1]] != start: out.append(nx[out[-1]])
        assert len(out) == len(self.adj[v]) == self.deg[v]
        return out
    def apex(self, v, x, y):
        """The third vertex of the face on edge x y away from v, if it exists."""
        for t in self.tris:
            if x in t and y in t and v not in t: return [z for z in t if z not in (x, y)][0]
        return None

def build():
    D = ODisc(); u0, W = D.wheel(7)
    U = [u0, W[0], W[1]]
    for i, u in enumerate(U): D.lab[u] = 'u%d' % i
    req = {}
    def want(v, k, why):
        if k == 9: return False
        if v in req and req[v][0] != k: raise Clash('%s asked for %d (%s) and %d (%s)' % (D.lab[v], req[v][0], req[v][1], k, why))
        if v in req: return False
        req[v] = (k, why); return True
    for i, u in enumerate(U): want(u, d, 'u%d' % i)
    changed = True
    while changed:
        changed = False
        for v, (k, why) in list(req.items()):
            if v not in D.deg and v in D.B: D.close(v, k); changed = True
        for i, u in enumerate(U):
            if u not in D.deg: continue
            R = D.rot(u); j = R.index(U[(i + 1) % 3])
            if R[(j + 1) % d] != U[(i + 2) % 3]: raise Clash('u%d: u%d does not follow u%d counterclockwise' % (i, (i + 2) % 3, (i + 1) % 3))
            R = R[j:] + R[:j]
            for a in range(d):
                if D.lab[R[a]].startswith('v'): D.lab[R[a]] = 'u%d.w%d' % (i, a)
                changed |= want(R[a], LK[a], 'u%d.w%d' % (i, a))
            for a in range(d):
                s = D.apex(u, R[a], R[(a + 1) % d])
                if s is None: continue
                if D.lab[s].startswith('v'): D.lab[s] = 'u%d.s%d' % (i, a)
                changed |= want(s, SV[a], 'u%d.s%d' % (i, a))
    return D, U, req

def window(D, I, name):
    I = sorted(set(I)); Is = set(I)
    for v in I: assert v in D.deg, D.lab[v]
    RS = sorted({w for v in I for w in D.adj[v]} - Is)
    nb = {x: set() for x in RS}
    for t in D.tris:
        st = set(t)
        if st & Is and len(st - Is) == 2:
            x, y = sorted(st - Is); nb[x].add(y); nb[y].add(x)
    assert all(len(nb[x]) == 2 for x in RS), [(D.lab[x], len(nb[x])) for x in RS if len(nb[x]) != 2]
    cyc = [RS[0]]; prev = None
    while True:
        nx = sorted(nb[cyc[-1]] - ({prev} if prev is not None else set()))[0]
        if nx == cyc[0]: break
        prev = cyc[-1]; cyc.append(nx)
    assert len(cyc) == len(RS), 'ring is not one cycle'
    ri = {x: k for k, x in enumerate(cyc)}; ii = {v: k for k, v in enumerate(I)}
    rp = ';'.join(','.join(str(k) for k in sorted(ri[w] for w in D.adj[v] if w in ri)) or '-' for v in I)
    ip = ';'.join(','.join(str(k) for k in sorted(ii[w] for w in D.adj[v] if w in ii)) or '-' for v in I)
    return '%s %d %d %s %s' % (name, len(cyc), len(I), rp, ip), [D.lab[v] + '=%d' % D.deg[v] for v in I], [D.lab[x] for x in cyc]

def main():
    try:
        D, U, req = build()
    except Clash as e:
        print('CLASH:', e); return
    print('# triple wheel %s/%s: realisable, %d vertices, %d closed, boundary %d' % (''.join(map(str, LK)), ''.join(map(str, SV)), D.n, len(D.deg), len(D.B)))
    B1 = {}
    for i, u in enumerate(U): B1[i] = {u} | D.adj[u]
    r = {}
    for i, u in enumerate(U):
        R = D.rot(u); j = R.index(U[(i + 1) % 3]); R = R[j:] + R[:j]
        r[i] = D.apex(u, R[4], R[5]); assert D.deg.get(r[i]) == 5 and LK[4] == LK[5] == 5 and SV[4] == 5
    wins = [('tw13', (B1[0] | B1[1]) - {U[2]} | {r[0], r[1]}), ('tw14', B1[0] | B1[1] | {r[0], r[1]}),
            ('tw18', B1[0] | B1[1] | B1[2] | {r[0], r[1], r[2]})]
    os.makedirs(os.path.join(H, 'tw'), exist_ok=True)
    out = open(os.path.join(H, 'tw', 'tw60_windows.txt'), 'w')
    for nm, I in wins:
        line, il, rl = window(D, I, nm)
        print('#', nm, 'interior', len(il), ' '.join(il)); print('#   ring', len(rl), ' '.join(rl)); print(line)
        out.write(line + '\n')

if __name__ == '__main__':
    main()
