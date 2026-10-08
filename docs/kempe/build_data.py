# Builds docs/kempe/data.js for the "Counting Kempe Chains" demo page.
#
# Run from anywhere:  python3 docs/kempe/build_data.py
#
# The triangulation: the 7th of the 12 triangulations of order 18 with minimum degree 5 produced by
#   plantri -m5 -a 18        (plantri 5.8, SolvingFrameworkPlan/docs/working/Census34/bin/plantri)
# with the hole at vertex 4 (degree 5). It was chosen by scanning every degree-5 hole of every minimum-degree-5
# triangulation of orders 12-20 for a small state space (86 colourings of T - v up to renaming) that still has two
# Kempe classes, rigid states (N = 8) and doubly locked pi-steps that stay doubly locked.
#
# The page recomputes everything live in the browser (its own small JS engine). This script computes the same data
# with an engine written for these pages (copied from docs/alternation/build_data.py), and asserts agreement with
#   (1) TrackM tm_lib.Hole (built on Track A's kempe_py), state by state;
#   (2) the TrackJL-review C engine rv_eng (independent, reviewed), on its counters, with zero failures;
#   (3) the chain-count formula 2N = cw + (n-1) - eta + 2(L1+L2) (mod 4) and the chain-parity law at every state.
# The page compares its live results with the numbers stored here and reports the agreement.
import sys, os, json, re, itertools, collections, subprocess, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
WK = os.path.join(ROOT, 'SolvingFrameworkPlan', 'docs', 'working')
t0 = time.time()

PAIRS = list(itertools.combinations(range(4), 2))

PLANTRI_LINE = '18 bcdefg,aghic,abijd,acjkle,adlmf,aemng,afnhb,bgnopi,bhpjc,cipkd,djpql,dkqrme,elrnf,fmrohg,hnrqp,hoqkji,kporl,lqonm'
HOLE = 4


def plantri_ascii(line):
    return [[ord(ch) - 97 for ch in w] for w in line.split()[1].split(',')]


# =============================================================== engine (written for this page)
class Hole:
    """All proper 4-colourings of T - h up to renaming (colours by first occurrence along a BFS order from link[0],
    neighbours ascending), whole-component Kempe moves, frames, locks, pi, N."""

    def __init__(self, rot, h):
        self.rot = rot; self.h = h; self.n = n = len(rot)
        self.link = link = list(rot[h]); assert len(link) == 5
        adj = [set(r) for r in rot]
        for u in range(n):
            for w in rot[u]: assert u in adj[w]
        # faces from the rotation system: (u, rot[u][i], rot[u][i+1]); each must be seen from all three corners
        fc = collections.Counter()
        for u in range(n):
            d = len(rot[u])
            for i in range(d):
                f = (u, rot[u][i], rot[u][(i + 1) % d]); k = f.index(min(f)); fc[f[k:] + f[:k]] += 1
        assert all(v == 3 for v in fc.values()) and len(fc) == 2 * n - 4, 'not a consistently oriented triangulation'
        self.faces = sorted(fc)
        assert n - sum(len(a) for a in adj) // 2 + len(self.faces) == 2
        order = [link[0]]; seen = {link[0]}
        for x in order:
            for y in sorted(adj[x]):
                if y != h and y not in seen: seen.add(y); order.append(y)
        assert len(order) == n - 1
        self.order = order; self.idx = {u: i for i, u in enumerate(order)}; self.m = m = n - 1
        self.nbm = [0] * m
        for u in order:
            for w in adj[u]:
                if w != h: self.nbm[self.idx[u]] |= 1 << self.idx[w]
        self.li = [self.idx[x] for x in link]
        self.linkmask = sum(1 << i for i in self.li)
        prev = [[j for j in range(i) if self.nbm[i] >> j & 1] for i in range(m)]
        states = []; col = [0] * m

        def rec(i, used):
            if i == m: states.append(tuple(col)); return
            forb = 0
            for j in prev[i]: forb |= 1 << col[j]
            for c in range(min(used + 1, 4)):
                if not forb >> c & 1: col[i] = c; rec(i + 1, max(used, c + 1))
        rec(1, 1)
        self.states = states; self.index = {s: k for k, s in enumerate(states)}; self.S = len(states)
        self._analyse()

    @staticmethod
    def canon(c):
        mp = {}; return tuple(mp.setdefault(x, len(mp)) for x in c)

    def cm(self, s):
        out = [0, 0, 0, 0]
        for i, x in enumerate(s): out[x] |= 1 << i
        return out

    def flood(self, start, M):
        comp = front = start
        while front:
            nb = 0; f = front
            while f:
                low = f & -f; nb |= self.nbm[low.bit_length() - 1]; f ^= low
            nb &= M & ~comp; comp |= nb; front = nb
        return comp

    def chains(self, s, cm=None):
        cm = cm or self.cm(s); out = []
        for p, q in PAIRS:
            M = cm[p] | cm[q]
            while M:
                K = self.flood(M & -M, cm[p] | cm[q]); M &= ~K; out.append((p, q, K))
        return out

    def swap(self, s, K, p, q):
        return tuple((q if x == p else p) if K >> i & 1 else x for i, x in enumerate(s))

    def frame(self, s):
        c = [s[i] for i in self.li]
        if len(set(c)) <= 3: return None
        j = [t for t in range(5) if c[t] == c[(t + 2) % 5]]; assert len(j) == 1
        return j[0]

    def _analyse(self):
        S = self.S; li = self.li
        self.N = [0] * S; self.ell = [0] * S; self.rim = [0] * S; self.filled = [False] * S
        self.j = [None] * S; self.L1 = [0] * S; self.L2 = [0] * S; self.pi = [None] * S; self.pinv = [None] * S
        self.nbrs = [None] * S; self.counts = [None] * S
        for k, s in enumerate(self.states):
            cm = self.cm(s); ch = self.chains(s, cm)
            self.N[k] = len(ch)
            self.ell[k] = sum(1 for _, _, K in ch if not K & self.linkmask)
            self.rim[k] = self.N[k] - self.ell[k]
            self.counts[k] = [sum(1 for p, q, _ in ch if (p, q) == pr) for pr in PAIRS]
            nb = set()
            for p, q, K in ch:
                t = self.index[self.canon(self.swap(s, K, p, q))]
                if t != k: nb.add(t)
            self.nbrs[k] = sorted(nb)
            j = self.frame(s)
            if j is None: self.filled[k] = True; continue
            self.j[k] = j; x = [li[(j + t) % 5] for t in range(5)]
            al, mu, A, B = s[x[0]], s[x[1]], s[x[3]], s[x[4]]
            self.L1[k] = self.flood(1 << x[1], cm[mu] | cm[A]) >> x[3] & 1
            self.L2[k] = self.flood(1 << x[1], cm[mu] | cm[B]) >> x[4] & 1
            K = self.flood(1 << x[2], cm[al] | cm[A])
            if not K >> x[0] & 1: self.pi[k] = self.index[self.canon(self.swap(s, K, al, A))]
            K = self.flood(1 << x[0], cm[al] | cm[B])
            if not K >> x[2] & 1: self.pinv[k] = self.index[self.canon(self.swap(s, K, al, B))]
        self.DL = [(not self.filled[k]) and self.L1[k] == 1 and self.L2[k] == 1 for k in range(S)]
        self.dF = self._bfs([k for k in range(S) if self.filled[k]])
        self.dNDL = self._bfs([k for k in range(S) if not self.DL[k]])
        cl = [-1] * S; nc = 0
        for s0 in range(S):
            if cl[s0] >= 0: continue
            cl[s0] = nc; q = [s0]
            for x in q:
                for t in self.nbrs[x]:
                    if cl[t] < 0: cl[t] = nc; q.append(t)
            nc += 1
        self.cl = cl; self.ncl = nc

    def _bfs(self, src):
        d = [-1] * self.S; q = collections.deque(src)
        for s in src: d[s] = 0
        while q:
            x = q.popleft()
            for t in self.nbrs[x]:
                if d[t] < 0: d[t] = d[x] + 1; q.append(t)
        return d

    def maxrun(self, inset, f):
        best = 0
        for x in range(self.S):
            if not inset[x]: continue
            k = 0; y = x; seen = set()
            while y is not None and inset[y]:
                if y in seen: return -1
                seen.add(y); k += 1; y = f[y]
            best = max(best, k)
        return best

    def cw_eta(self, s):
        """clockwise faces avoiding h (Tait triple a cyclic shift of (1,2,3)) and eta of the frame."""
        cyc = {(1, 2, 3), (2, 3, 1), (3, 1, 2)}; c = {u: s[i] for u, i in self.idx.items()}
        cw = sum(1 for (u, w, z) in self.faces if self.h not in (u, w, z)
                 and (c[u] ^ c[w], c[w] ^ c[z], c[z] ^ c[u]) in cyc)
        j = self.frame(s)
        if j is None: return cw, None
        x = [self.li[(j + t) % 5] for t in range(5)]
        al, mu, A, B = s[x[0]], s[x[1]], s[x[3]], s[x[4]]
        return cw, int((al ^ mu, al ^ A, al ^ B) in cyc)


# =============================================================== layout (hole at the centre, its five neighbours as a ring)
def layout(rot, h, seed=1):
    """Hole at the origin, its five neighbours on a regular pentagon of radius 1, everything else outside it.
    Tutte drawing of T - h with the link as the outer pentagon, then an inversion about the origin (r -> r^-g) that
    turns the drawing inside out, then a spacing hill-climb with the hole and the ring fixed. Asserted planar."""
    n = len(rot); adj = [set(r) for r in rot]; link = list(rot[h])
    faces = set()
    for u in range(n):
        d = len(rot[u])
        for i in range(d):
            f = (u, rot[u][i], rot[u][(i + 1) % d]); k = f.index(min(f)); faces.add(f[k:] + f[:k])
    F = sorted(faces); Fa = np.array(F)
    edges = sorted({(min(u, w), max(u, w)) for u in range(n) for w in rot[u]}); Ea = np.array(edges)

    def gaps(P):
        dd = np.hypot(P[:, None, 0] - P[None, :, 0], P[:, None, 1] - P[None, :, 1])
        vv = dd[np.triu_indices(n, 1)].min()
        A_, B_ = P[Ea[:, 0]], P[Ea[:, 1]]; D_ = B_ - A_; L_ = (D_ * D_).sum(1)
        t = np.clip(((P[None, :, :] - A_[:, None, :]) * D_[:, None, :]).sum(2) / L_[:, None], 0, 1)
        Q_ = A_[:, None, :] + t[:, :, None] * D_[:, None, :]
        de = np.hypot(*(P[None, :, :] - Q_).transpose(2, 0, 1))
        de[np.arange(len(Ea)), Ea[:, 0]] = 9; de[np.arange(len(Ea)), Ea[:, 1]] = 9
        return float(vv), float(de.min())

    def signs(P):
        a, b, c = P[Fa[:, 0]], P[Fa[:, 1]], P[Fa[:, 2]]
        return np.sign((b[:, 0] - a[:, 0]) * (c[:, 1] - a[:, 1]) - (b[:, 1] - a[:, 1]) * (c[:, 0] - a[:, 0]))

    def ccw(P, a, b, c): return (P[b][0] - P[a][0]) * (P[c][1] - P[a][1]) - (P[b][1] - P[a][1]) * (P[c][0] - P[a][0])

    def crosses(P):
        for (a, b), (c, d) in itertools.combinations(edges, 2):
            if len({a, b, c, d}) == 4 and ccw(P, a, b, c) * ccw(P, a, b, d) < 0 and ccw(P, c, d, a) * ccw(P, c, d, b) < 0:
                return True
        return False

    def gscore(P):
        vv, ve = gaps(P / float(np.abs(P).max())); return min(vv, 2 * ve)

    dist = {h: 0}; q = collections.deque([h])
    while q:
        u = q.popleft()
        for w in adj[u]:
            if w not in dist: dist[w] = dist[u] + 1; q.append(w)
    # annulus Tutte drawing: the hole at the origin, the link fixed on a regular pentagon of radius r0, a far face fixed
    # on the unit circle; every other vertex a weighted average of its neighbours. Planarity is not guaranteed for an
    # annulus, so every candidate is checked (no crossing, consistent face orientation) and the best spaced one kept.
    far = sorted([f for f in F if h not in f], key=lambda f: -sum(dist[v] for v in f))[:6]
    best = None
    for outer in far:
        if set(outer) & set(link): continue
        for rev in (False, True):
            lk = link[::-1] if rev else link
            for rot0 in range(10):
                for r0 in (0.16, 0.22, 0.3):
                    fixed = {h: (0.0, 0.0)}
                    for t, x in enumerate(lk):
                        a_ = np.pi * rot0 / 5 + 2 * np.pi * t / 5; fixed[x] = (r0 * np.cos(a_), r0 * np.sin(a_))
                    for k, v in enumerate(outer):
                        a_ = -np.pi / 2 + 2 * np.pi * k / 3; fixed[v] = (np.cos(a_), np.sin(a_))
                    free = [v for v in range(n) if v not in fixed]; ix = {v: i for i, v in enumerate(free)}
                    for alpha in (0.0, 0.5):
                        A = np.zeros((len(free), len(free))); b = np.zeros((len(free), 2))
                        for v in free:
                            i = ix[v]
                            for w in adj[v]:
                                wt = float(np.exp(-alpha * abs(dist[w] - dist[v]))); A[i, i] += wt
                                if w in ix: A[i, ix[w]] -= wt
                                else: b[i] += wt * np.array(fixed[w])
                        sol = np.linalg.solve(A, b); Z = np.zeros((n, 2))
                        for v, xy in fixed.items(): Z[v] = xy
                        for v in free: Z[v] = sol[ix[v]]
                        sg = signs(Z); inner_f = [i for i, f in enumerate(F) if tuple(sorted(f)) != tuple(sorted(outer))]
                        if len(set(sg[inner_f])) != 1 or 0 in sg or crosses(Z): continue
                        sc = gscore(Z)
                        if best is None or sc > best[0]: best = (sc, Z, sg)
    if best is None:
        # fallback for larger maps: a plain Tutte drawing with a far face outside (planar by Tutte's theorem), then
        # orientation-preserving moves that pull the five neighbours onto a regular pentagon around the hole
        outer = far[0]; fixed = {}
        for k, v in enumerate(outer):
            a_ = -np.pi / 2 + 2 * np.pi * k / 3; fixed[v] = (np.cos(a_), np.sin(a_))
        free = [v for v in range(n) if v not in fixed]; ix = {v: i for i, v in enumerate(free)}
        A = np.zeros((len(free), len(free))); b = np.zeros((len(free), 2))
        for v in free:
            i = ix[v]
            for w in adj[v]:
                A[i, i] += 1
                if w in ix: A[i, ix[w]] -= 1
                else: b[i] += np.array(fixed[w])
        sol = np.linalg.solve(A, b); pos = np.zeros((n, 2))
        for v, xy in fixed.items(): pos[v] = xy
        for v in free: pos[v] = sol[ix[v]]
        pos = pos - pos[h]; S0 = signs(pos); assert 0 not in S0
        # orientation of the link around the hole in this drawing
        ang = [np.arctan2(*pos[x][::-1]) for x in link]
        sgn = 1 if ((ang[1] - ang[0]) % (2 * np.pi)) < np.pi else -1

        def target(P):
            r = float(np.mean([np.hypot(*P[x]) for x in link]))
            off = np.angle(sum(np.exp(1j * (np.arctan2(P[x][1], P[x][0]) - sgn * 2 * np.pi * t / 5)) for t, x in enumerate(link)))
            return {x: r * np.array([np.cos(off + sgn * 2 * np.pi * t / 5), np.sin(off + sgn * 2 * np.pi * t / 5)]) for t, x in enumerate(link)}

        def dev(P):
            T_ = target(P); r = float(np.mean([np.hypot(*P[x]) for x in link]))
            return sum(float(np.sum((P[x] - T_[x]) ** 2)) for x in link) / r ** 2

        def obj(P): return gscore(P) - 2.0 * dev(P)
        rng0 = np.random.default_rng(seed + 7); cur = obj(pos); mov = [v for v in range(n) if v != h]
        for it in range(40000):
            v = mov[rng0.integers(len(mov))]; Z = pos.copy()
            if v in link and rng0.random() < 0.5:
                Z[v] += 0.3 * (target(pos)[v] - pos[v])
            else:
                Z[v] += rng0.normal(0, 0.02, 2) * max(1.0, float(np.hypot(*pos[v])))
            if (signs(Z) != S0).any(): continue
            s_ = obj(Z)
            if s_ >= cur: pos, cur = Z, s_
        Z = pos.copy(); T_ = target(pos)
        for x in link: Z[x] = T_[x]
        assert (signs(Z) == S0).all() and not crosses(Z), ('ring snap failed', dev(pos))
        pos = Z; cur = gscore(pos)
    else:
        cur, pos, S0 = best
    # radial expansion about the hole (r -> r^g keeps the ring regular): give the hole's neighbourhood room
    bestg = (gscore(pos) + 0.15 * float(np.hypot(*pos[link[0]]) / np.abs(pos).max()), pos)
    for g in (0.4, 0.5, 0.6, 0.7, 0.8, 0.9):
        rr = np.hypot(pos[:, 0], pos[:, 1]); rr[rr == 0] = 1
        Z = pos * (rr ** (g - 1))[:, None]
        if (signs(Z) == S0).all() and not crosses(Z):
            sc_ = gscore(Z) + 0.15 * float(np.hypot(*Z[link[0]]) / np.abs(Z).max())
            if sc_ > bestg[0]: bestg = (sc_, Z)
    pos = bestg[1]

    def rscore(P): return gscore(P) + 0.8 * float(np.hypot(*P[link[0]]) / np.abs(P).max())
    cur = rscore(pos)
    rng = np.random.default_rng(seed); movable = [v for v in range(n) if v != h and v not in link]
    for it in range(15000):
        if rng.random() < 0.05:   # gentle radial expansion about the hole (keeps the ring regular)
            rr = np.hypot(pos[:, 0], pos[:, 1]); rr[rr == 0] = 1; Z = pos * (rr ** -0.04)[:, None]
        else:
            v = movable[rng.integers(len(movable))]; Z = pos.copy(); Z[v] += rng.normal(0, 0.04, 2) * max(1.0, float(np.hypot(*pos[v])) * 0.5)
        if (signs(Z) != S0).any(): continue
        s_ = rscore(Z)
        if s_ >= cur: pos, cur = Z, s_
    assert not crosses(pos) and (signs(pos) == S0).all()
    pos = pos / float(np.abs(pos).max())
    print('  layout: hole at the centre, regular ring of 5, gap score', round(cur, 4))
    return [[round(float(x), 4), round(float(y), 4)] for x, y in pos], link, gaps(pos)


# =============================================================== the page's data
ROLE_ORDER = ['αμ', 'AB', 'αA', 'μB', 'αB', 'μA']


def role_counts(H, k):
    """chain counts in role order (αμ, AB, αA, μB, αB, μA) at an unfilled state."""
    s = H.states[k]; j = H.j[k]; x = [H.li[(j + t) % 5] for t in range(5)]
    rc = {s[x[0]]: 'α', s[x[1]]: 'μ', s[x[3]]: 'A', s[x[4]]: 'B'}
    out = {}
    for (p, q), c in zip(PAIRS, H.counts[k]):
        a, b = rc[p], rc[q]
        lab = [l for l in ROLE_ORDER if {a, b} == {l[0], l[1:]}][0]
        out[lab] = c
    return [out[l] for l in ROLE_ORDER]


def main():
    rot = plantri_ascii(PLANTRI_LINE)
    plantri = os.path.join(WK, 'Census34', 'bin', 'plantri')
    if os.path.exists(plantri):
        outp = subprocess.run([plantri, '-m5', '-a', '18'], capture_output=True, text=True).stdout.splitlines()
        assert outp[6].strip() == PLANTRI_LINE, 'plantri regeneration differs'
        print('plantri -m5 -a 18: graph 7 of', len(outp), 'regenerated identically')
    H = Hole(rot, HOLE); S = H.S; n = H.n
    assert sorted(len(r) for r in rot)[0] == 5 and len(rot[HOLE]) == 5
    unf = [k for k in range(S) if not H.filled[k]]
    cwe = [H.cw_eta(H.states[k]) for k in range(S)]
    for k in unf:
        cw, eta = cwe[k]
        assert (2 * H.N[k] - cw - (n - 1) + eta - 2 * (H.L1[k] + H.L2[k])) % 4 == 0, 'formula'
        assert H.rim[k] == 8
    # filled states: the closed-sphere form 2N = cw + n (mod 4) does not apply (v is missing); store cw anyway
    law = []
    for k in range(S):
        if not H.DL[k]: continue
        u = H.pi[k]; assert u is not None and H.pinv[u] == k
        assert (H.N[u] - H.N[k]) % 2 == int(H.DL[u])
        # Lemma W on the actual colours (cw itself depends on the naming of colours; the formula does not)
        st = H.states[k]; j = H.j[k]; x = [H.li[(j + t) % 5] for t in range(5)]; cm = H.cm(st)
        Kpi = H.flood(1 << x[2], cm[st[x[0]]] | cm[st[x[3]]]); pst = H.swap(st, Kpi, st[x[0]], st[x[3]])
        assert H.index[H.canon(pst)] == u
        cwpi_actual = H.cw_eta(pst)[0]
        assert (cwpi_actual - cwe[k][0]) % 4 == 2, 'Lemma W'
        assert H.j[u] == (H.j[k] + 3) % 5
        law.append(dict(s=k, N=H.N[k], pi=u, Npi=H.N[u], piDL=H.DL[u], cw=cwe[k][0], cwpi=cwpi_actual))
    rigid = [k for k in range(S) if H.DL[k] and H.N[k] == 8]
    for k in rigid: assert role_counts(H, k) == [1, 1, 2, 1, 2, 1]
    # Kempe swap structure: swapping a pq-chain never changes the pq- and rs-chain counts (checked on every move)
    nmoves = 0; dN = collections.Counter()
    for k in range(S):
        s = H.states[k]
        for p, q, K in H.chains(s):
            t = H.swap(s, K, p, q); r = [c for c in range(4) if c not in (p, q)]
            cm2 = H.cm(t); cnt2 = []
            for a, b in PAIRS:
                M = cm2[a] | cm2[b]; c = 0
                while M: KK = H.flood(M & -M, M); M &= ~KK; c += 1
                cnt2.append(c)
            assert cnt2[PAIRS.index((p, q))] == H.counts[k][PAIRS.index((p, q))]
            assert cnt2[PAIRS.index(tuple(r))] == H.counts[k][PAIRS.index(tuple(r))]
            assert sum(cnt2) == H.N[H.index[H.canon(t)]]
            nmoves += 1; dN[sum(cnt2) - H.N[k]] += 1
    # classes
    sizes = collections.Counter(H.cl); fl = collections.Counter(H.cl[k] for k in range(S) if H.filled[k])
    classes = [dict(id=c, size=sizes[c], filled=fl[c], DL=sum(1 for k in range(S) if H.cl[k] == c and H.DL[k]),
                    rigid=sum(1 for k in rigid if H.cl[k] == c)) for c in range(H.ncl)]
    # ---- cross-check (1): tm_lib, state by state
    sys.path.insert(0, os.path.join(WK, 'TrackM'))
    from tm_lib import Hole as TMHole
    T = TMHole(rot, HOLE); T.classes_and_dist(); assert T.S == S and T.ncl == H.ncl
    tmap = {k: T.sp.state_of({u: H.states[k][i] for u, i in H.idx.items()}) for k in range(S)}
    assert len(set(tmap.values())) == S
    for k in range(S):
        t = tmap[k]
        assert T.Nch[t] == H.N[k] and T.filled[t] == H.filled[k] and T.dF[t] == H.dF[k] and T.ell[t] == H.ell[k]
        assert len({m[0] for m in T.moves[t]}) == len(H.nbrs[k])
        assert sorted(tmap[x] for x in H.nbrs[k]) == sorted({m[0] for m in T.moves[t]})
        if not H.filled[k]:
            assert (T.L1[t], T.L2[t], T.j[t]) == (H.L1[k], H.L2[k], H.j[k])
            assert (H.pi[k] is None and T.pi[t] is None) or T.pi[t] == tmap[H.pi[k]]
    # same partition into classes
    assert len({(H.cl[k], T.cl[tmap[k]]) for k in range(S)}) == H.ncl
    # ---- cross-check (2): rv_eng
    rv = os.path.join(WK, 'TrackJL-review', 'rv_eng')
    line = 'k18 ' + str(n) + ' ' + ';'.join(','.join(map(str, r)) for r in rot) + '\n'
    outp = subprocess.run([rv, '-E', '2', '-H', str(HOLE)], input=line, capture_output=True, text=True, check=True).stdout
    summ = dict(re.findall(r'(\w+)=(\d+)', outp.splitlines()[0]))
    chk = {m.group(1).strip(): (int(m.group(2)), int(m.group(3))) for m in re.finditer(r'^\s+(.*?)\s+checks=(\d+) fails=(\d+)', outp, re.M)}
    assert int(summ['states']) == S and all(f == 0 for _, f in chk.values())
    assert chk['DL states'][0] == len(law) and chk['rigid states'][0] == len(rigid)
    assert chk['chain-parity law N(pi c)-N(c) = [pi c DL] mod 2 (sphere)'] == (len(law), 0)
    assert chk['LemmaE(Sum chi P1,P2,P3)'][0] == len(unf)
    pos, outer, gp = layout(rot, HOLE, seed=3)
    edges = sorted({(min(u, w), max(u, w)) for u in range(n) for w in rot[u]})
    states = [dict(c=list(H.states[k]), N=H.N[k], cnt=H.counts[k], f=int(H.filled[k]), dl=int(H.DL[k]),
                   L1=H.L1[k], L2=H.L2[k], j=H.j[k], pi=H.pi[k], cl=H.cl[k], cw=cwe[k][0], eta=cwe[k][1],
                   kd=len(H.nbrs[k]), dF=H.dF[k], nb=H.nbrs[k]) for k in range(S)]
    stats = dict(S=S, filled=S - len(unf), unfilled=len(unf), DL=len(law), rigid=len(rigid),
                 DLtoDL=sum(1 for r in law if r['piDL']), classes=H.ncl, moves=nmoves,
                 dN=sorted(dN.items()), rvChecks=sum(c for c, _ in chk.values()))
    data = dict(n=n, hole=HOLE, rot=rot, link=H.link, order=H.order, edges=edges, faces=H.faces, pos=pos, deg=[len(r) for r in rot],
                states=states, classes=classes, law=law, rigid=rigid, stats=stats, built=time.strftime('%Y-%m-%d'),
                source='plantri -m5 -a 18, graph 7; hole at vertex 4')
    with open(os.path.join(HERE, 'data.js'), 'w') as f:
        f.write('// Generated by docs/kempe/build_data.py. Do not edit.\n')
        f.write('window.KEMPE_DATA = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
    print('stats', stats)
    print('classes', classes)
    print('wrote data.js', os.path.getsize(os.path.join(HERE, 'data.js')), 'bytes', round(time.time() - t0, 1), 's')


if __name__ == '__main__':
    main()
