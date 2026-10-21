"""EXPLORE round 59 part 3 (Opus's census question, coordinator 05:01Z; reading confirmed by Opus 05:08Z): does a run of
face 7s in their sea of 6s force a registry configuration?
Chain of length L: u1 -> X1 -> u2 -> X2 -> u3 ..., where each u_j is exactly 7 with a 5-5-5 face (link pair w_i, w_i+1
and their apex s_i, all exactly 5), X_j is exactly 6 and is a k-vertex of u_j's face (fb6's payee: the link vertex of
u_j next to the face), and u_j+1 is another neighbour of X_j, exactly 7, with a face at any of its link positions.
L = 1 is u1, its face and X1; L = 2 adds u2 and its face; L = 3 adds X2, u3 and its face.  u1's face is (w0, w1, s0)
and X1 = w6 (the other k-vertex w2 is its mirror).
The patch is the free disc of the closed vertices (each with its whole neighbourhood, no identifications); its boundary
vertices are the 1-ring slots, each 5..9 (9 = degree >= 9, never exact).  Letters below a slot's disc degree k are
impossible.  A slot at exactly k closes off (an edge between its two boundary neighbours) and changes the structure;
splitting on every such slot gives up to 2^(slots) parts (32,129 for one L = 3 shape), so the census is run on the
open fillings (every slot above its disc degree, one fixed structure), and the closing fillings' share of the possible
ones is reported beside it.  An uncovered open filling is a genuine escape, so a "no" stands; a "yes" needs the closing
fillings too.
A filling is covered when a configuration's interior maps onto the patch (grow.embeddings: exact degrees, induced,
interior triangles onto faces; a slot's letter becomes a requirement): the registry (fam51.registry: RSST 582 + the
twoeng names of TD/TC) and, kept apart, the 2026 set (XKC).  Coverage = covered / possible fillings, per shape.
usage: python3 chain59.py TD TC XKC LMAX [OUT]   -> one line per shape, totals per L (OUT default chain59_L<LMAX>.txt)"""
import sys, os, itertools, collections, hashlib, time
H = os.path.dirname(os.path.abspath(__file__)); LOOP = os.path.join(H, '..')
sys.path.insert(0, os.path.join(LOOP, 'k51'))
import fam51 as F
import grow

class Disc:
    def __init__(self):
        self.n = 0; self.tris = set(); self.adj = collections.defaultdict(set); self.B = []; self.deg = {}; self.lab = {}
    def new(self, lab=None):
        v = self.n; self.n += 1; self.lab[v] = lab or 'v%d' % v; return v
    def copy(self):
        d = Disc(); d.n = self.n; d.tris = set(self.tris); d.adj = collections.defaultdict(set, {k: set(v) for k, v in self.adj.items()})
        d.B = list(self.B); d.deg = dict(self.deg); d.lab = dict(self.lab); return d
    def tri(self, a, b, c):
        self.tris.add(frozenset((a, b, c)))
        for x, y in ((a, b), (b, c), (c, a)): self.adj[x].add(y); self.adj[y].add(x)
    def wheel(self, d, lab):
        c = self.new(lab); W = [self.new() for _ in range(d)]
        for i in range(d): self.tri(c, W[i], W[(i + 1) % d])
        self.B = list(W); self.deg[c] = d; return c, W
    def close(self, v, d):
        """Give boundary vertex v degree d and make it interior; False if impossible (no chord, no sphere)."""
        if v in self.deg: return self.deg[v] == d
        i = self.B.index(v); a, b = self.B[i - 1], self.B[(i + 1) % len(self.B)]; m = d - len(self.adj[v])
        if m < 0: return False
        if m == 0:
            if len(self.B) <= 3 or b in self.adj[a]: return False
            self.tri(a, v, b); self.B.pop(i)
        else:
            X = [self.new() for _ in range(m)]; seq = [a] + X + [b]
            for j in range(len(seq) - 1): self.tri(v, seq[j], seq[j + 1])
            self.B[i:i + 1] = X
        self.deg[v] = d; return True
    def rot(self, v):
        """Cyclic link of a closed vertex."""
        L = self.adj[v]; start = min(L); cyc = [start]; prev = None
        while True:
            nx = [y for y in L if y != prev and y != cyc[-1] and frozenset((v, cyc[-1], y)) in self.tris]
            nx = [y for y in nx if y != (cyc[-2] if len(cyc) > 1 else None)]
            if not nx: return None
            y = min(nx)
            if y == cyc[0]: break
            prev = cyc[-1]; cyc.append(y)
        return cyc if len(cyc) == len(L) else None
    def key(self):
        """Weisfeiler-Lehman hash of the labelled disc (closed degree or boundary)."""
        c = {v: ('c%d' % self.deg[v]) if v in self.deg else 'b' for v in range(self.n)}
        for _ in range(4):
            c = {v: hashlib.md5((c[v] + '|' + ','.join(sorted(c[y] for y in self.adj[v]))).encode()).hexdigest()[:12] for v in c}
        return ''.join(sorted(c.values()))

def apex(D, c, y, z):
    s = [x for x in D.adj[y] & D.adj[z] if x != c and frozenset((y, z, x)) in D.tris]
    return s[0] if len(s) == 1 else None

def with_face(D, c, y, z, tag):
    """Close link pair (y, z) of c and their apex at 5; None if impossible."""
    D = D.copy()
    for v, lb in ((y, tag + 'a'), (z, tag + 'b')):
        if not D.close(v, 5): return None
        D.lab[v] = D.lab[v] if D.lab[v][0] in 'uX' else lb
    a = apex(D, c, y, z)
    if a is None or not D.close(a, 5): return None
    if D.lab[a][0] not in 'uX': D.lab[a] = tag + 'c'
    return D

def faces_at(D, c, tag):
    R = D.rot(c); out = []
    for i in range(len(R)):
        y, z = R[i], R[(i + 1) % len(R)]
        if all(D.deg.get(x, 5) == 5 and (x in D.deg or len(D.adj[x]) <= 5) for x in (y, z)):
            E = with_face(D, c, y, z, tag)
            if E is not None: out.append((E, (y, z), (R[i - 1], R[(i + 2) % len(R)])))
    return out

def shapes(LMAX):
    D = Disc(); u1, W = D.wheel(7, 'u1')
    D = with_face(D, u1, W[0], W[1], 'f1'); assert D is not None
    for i, w in enumerate(W):
        if D.lab[w][0] == 'v': D.lab[w] = 'w%d' % i
    X1 = W[6]; assert D.close(X1, 6); D.lab[X1] = 'X1'
    for x in D.adj[X1]:              # X1's other neighbours: s6 (apex across w6 w0), s5 (across w5 w6), p (its private)
        if D.lab[x][0] != 'v': continue
        D.lab[x] = 's6' if W[0] in D.adj[x] else ('s5' if W[5] in D.adj[x] else 'p6')
    out = {1: [(D, 'u1 face w0 w1 s0, X1 = w6')]}
    cur = [(D, u1, X1, {u1}, {X1}, 'X1 = w6')]
    for L in range(2, LMAX + 1):
        nxt = []; out[L] = []
        for D0, up, Xp, U, XS, desc in cur:
            for u in sorted(D0.adj[Xp]):
                if u in U or D0.deg.get(u, 7) != 7 or (u not in D0.deg and len(D0.adj[u]) > 7): continue
                D1 = D0.copy()
                if not D1.close(u, 7): continue
                D1.lab[u] = 'u%d' % L
                for E, (y, z), (k1, k2) in faces_at(D1, u, 'f%d' % L):
                    d2 = '%s; u%d = %s, face %s %s' % (desc, L, D0.lab[u], *(D1.lab[x] if D1.lab[x][0] != 'v' else 'new' for x in (y, z)))
                    out[L].append((E, d2))
                    if L < LMAX:
                        for k in (k1, k2):
                            if k in XS or E.deg.get(k, 6) != 6 or (k not in E.deg and len(E.adj[k]) > 6): continue
                            E2 = E.copy()
                            if not E2.close(k, 6): continue
                            E2.lab[k] = 'X%d' % L
                            nxt.append((E2, u, k, U | {u}, XS | {k}, d2 + ', X%d = %s' % (L, E.lab[k] if E.lab[k][0] != 'v' else 'new')))
        cur = nxt
    for L in out:            # dedupe isomorphic shapes (WL hash)
        seen = {}; keep = []
        for E, d in out[L]:
            k = E.key()
            if k not in seen: seen[k] = len(keep); keep.append([E, d, 1])
            else: keep[seen[k]][2] += 1
        out[L] = keep
    return out

def open_lets(D):
    """Slot letters of the open fillings (above the disc degree), and the number of possible fillings in all."""
    lets = {x: tuple(l for l in (5, 6, 7, 8, 9) if l > len(D.adj[x]) or (l == 9 and len(D.adj[x]) >= 9)) for x in D.B}
    allp = prod(len([l for l in (5, 6, 7, 8, 9) if l >= len(D.adj[x]) or l == 9]) for x in D.B)
    return lets, allp

def count(cyl, slots, lets, memo=None):
    """Number of fillings of slots (letters lets) inside the union of the cylinders (dicts slot -> letter).  Branches on the
    most frequent slot; letters that no cylinder names there share one sub-problem, and sub-problems are memoised (keyed
    by the cylinders and the letters of the slots they name, so one memo can serve calls that differ in other letters)."""
    cyl = [frozenset(c.items()) for c in cyl if all(v in lets[k] for k, v in c.items())]
    if not cyl: return 0
    if memo is None: memo = {}
    def inv(cs): return {k for c in cs for k, _ in c}
    def cov(cs):                       # covered count over the slots the cylinders name
        cs = frozenset(cs); I = inv(cs); key = (cs, tuple((x, lets[x]) for x in sorted(I)))
        if key in memo: return memo[key]
        if frozenset() in cs: r = prod(len(lets[x]) for x in I)
        else:
            fr = collections.Counter(k for c in cs for k, _ in c); x = max(fr, key=lambda s: (fr[s], s))
            named = {v for c in cs for k, v in c if k == x}; r = 0; rest = I - {x}
            base = [c for c in cs if all(k != x for k, _ in c)]
            for l in lets[x]:
                if l not in named and l != min(set(lets[x]) - named, default=None): continue
                sub = [frozenset((k, v) for k, v in c if k != x) for c in cs if dict(c).get(x, l) == l]
                if sub: v = cov(sub) * prod(len(lets[y]) for y in rest - inv(sub))
                else: v = 0
                r += v * (len(set(lets[x]) - named) if l not in named else 1)
        memo[key] = r; return r
    return cov(cyl) * prod(len(lets[x]) for x in slots if x not in inv(cyl))
def prod(it):
    p = 1
    for v in it: p *= v
    return p
def minimal(cyl):
    cyl = sorted({tuple(sorted(c.items())) for c in cyl}, key=len); keep = []
    for c in cyl:
        if not any(all(dict(c).get(k) == v for k, v in m) for m in keep): keep.append(c)
    return [dict(c) for c in keep]

def cover(D, lets, REG, XR):
    P = list(range(D.n)); pa = {v: set(D.adj[v]) for v in P}; pf = set(D.tris); fd = dict(D.deg)
    def cyls(C):
        out = []; who = {}
        for c in C:
            if len(c[2]) > len(P): continue
            for e in grow.embeddings(c, P, pa, pf, fd):
                req = {v: c[3][u] for u, v in e if v not in fd}
                if all(req[v] in lets[v] for v in req):
                    out.append(req); who.setdefault(tuple(sorted(req.items())), c[0])
        return minimal(out), who
    cr, wr = cyls(REG); cx, wx = cyls(XR)
    S = sorted(lets); tot = prod(len(lets[x]) for x in S)
    return tot, count(cr, S, lets), count(cr + cx, S, lets), cr, wr, cx, wx

def main():
    TD, TC, XKC, LMAX = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    OUT = sys.argv[5] if len(sys.argv) > 5 else os.path.join(H, 'chain59_L%d.txt' % LMAX)
    REG, miss = F.registry(TD, TC)
    XR = [grow.kcline(l, 'xreg') for l in open(XKC) if l.strip()]
    log = open(OUT, 'w')
    def say(*a):
        s = ' '.join(map(str, a)); print(s, flush=True); log.write(s + '\n'); log.flush()
    say('# chain59 %s: registry %d (%d names not found), 2026 set %d; LMAX %d' % (time.strftime('%H:%MZ', time.gmtime()), len(REG), miss, len(XR), LMAX))
    SH = shapes(LMAX)
    for L in sorted(SH):
        say('# L = %d: %d shapes (after merging isomorphic ones)' % (L, len(SH[L])))
        T = C1 = C2 = AP = 0; full1 = full2 = 0; worst = None
        for j, (E, desc, mult) in enumerate(SH[L]):
            t0 = time.time(); lets, allp = open_lets(E)
            st, sr, sx, cyr, wr, cyx, wx = cover(E, lets, REG, XR)
            reqs = collections.Counter(wr[tuple(sorted(c.items()))] for c in cyr)
            AP += allp
            T += st; C1 += sr; C2 += sx; full1 += sr == st; full2 += sx == st
            r = sx / st if st else 1.0
            if worst is None or r < worst[0]: worst = (r, j)
            say('L%d shape %d (x%d): %s | %d slots, %d open fillings (%.1f%% of %d possible), covered: registry %.4f%%, +2026 %.4f%%, %d left | %.0fs | top %s' % (
                L, j, mult, desc, len(E.B), st, 100.0 * st / allp, allp, 100.0 * sr / st if st else 100,
                100.0 * sx / st if st else 100, st - sx, time.time() - t0, ' '.join('%s:%d' % kv for kv in reqs.most_common(3))))
        say('# L = %d total: %d shapes, %d open fillings (%.1f%% of possible), registry %.4f%% (%d shapes at 100%%), with 2026 %.4f%% (%d at 100%%), worst shape %s at %.4f%%' % (
            L, len(SH[L]), T, 100.0 * T / AP if AP else 100, 100.0 * C1 / T if T else 100, full1, 100.0 * C2 / T if T else 100, full2,
            worst[1] if worst else '-', 100 * worst[0] if worst else 100))

if __name__ == '__main__':
    main()
