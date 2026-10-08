# Builds docs/alternation/data.js for "The 9-8 Alternation" demo page.
#
# Run from anywhere:  python3 docs/alternation/build_data.py
#
# Sources (read-only):
#   SolvingFrameworkPlan/docs/working/Census34/out/maxima_graphs.txt   p34.r178#11764701 (record run, hole 10)
#   SolvingFrameworkPlan/docs/working/Census33/out/frame-33.txt        p33.r147#128636   (order-33 NR record, hole 2)
#   SolvingFrameworkPlan/docs/working/Census34/out/runs-34.jsonl, verify_maxima.txt     (census + second-engine records)
#   TrackO/out/frame-22..32.jsonl(.gz), Census33/out/eval-33.jsonl.gz, Census34/out/eval-34.jsonl.gz  (chart)
#
# The states, chains, locks, pi-steps and counts shown on the page are computed here by an engine written for
# this page (stdlib + numpy; no project import). Every displayed number is then cross-checked, by assert, against
#   (1) TrackM tm_lib.Hole (built on Track A's kempe_py), mapped state by state;
#   (2) the TrackJL-review C engine rv_eng (independent, reviewed), on its summary counters;
#   (3) the census records (runs-34.jsonl, verify_maxima.txt, README tables).
# The chart's per-order maxima are recomputed from the census per-hole files and asserted against the README tables;
# orders 22-25 are also recomputed from scratch with this page's engine.
import sys, os, json, gzip, re, itertools, collections, subprocess, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
WK = os.path.join(ROOT, 'SolvingFrameworkPlan', 'docs', 'working')
t0 = time.time()

PAIRS = list(itertools.combinations(range(4), 2))


def read_rot(path, name):
    for l in open(path):
        p = l.split()
        if len(p) >= 3 and p[0] == name:
            return [list(map(int, r.split(','))) for r in p[2].split(';')]
    raise KeyError(name)


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


# =============================================================== the two record holes
SRC = [
    dict(key='p34', name='p34.r178#11764701', hole=10, file=os.path.join(WK, 'Census34/out/maxima_graphs.txt'),
         label='Order 34 record', blurb='The longest π-run inside the near-rigid set in the whole order-34 census (R = NR = 8).'),
    dict(key='p33', name='p33.r147#128636', hole=2, file=os.path.join(WK, 'Census33/out/frame-33.txt'),
         label='Order 33 record', blurb='The order-33 near-rigid record (NR = 8): it starts on a rigid state and both ends leave the doubly locked set.'),
]
ROLE = ['α', 'μ', 'A', 'B']


def role_names(s, x):
    """map actual colour -> role letter for frame vertices x (x0..x4 positions in order-index space)."""
    return {s[x[0]]: 'α', s[x[1]]: 'μ', s[x[3]]: 'A', s[x[4]]: 'B'}


ROLE_ORDER = ['αμ', 'AB', 'αA', 'μB', 'αB', 'μA']


def pair_label(p, q, rn):
    a, b = rn[p], rn[q]
    for lab in ROLE_ORDER:
        if {a, b} == {lab[0], lab[1:]}: return lab
    raise ValueError


def bfs_path(H, K, a, b):
    """shortest path inside vertex mask K from index a to index b (order-index space)."""
    prev = {a: None}; q = collections.deque([a])
    while q:
        u = q.popleft()
        if u == b: break
        m = H.nbm[u] & K
        while m:
            low = m & -m; w = low.bit_length() - 1; m ^= low
            if w not in prev: prev[w] = u; q.append(w)
    path = [b]
    while prev[path[-1]] is not None: path.append(prev[path[-1]])
    return path[::-1]


def describe(H, k, col):
    """col: actual colours (order-index space, values 0..3) whose canonical form is state k."""
    assert H.canon(col) == H.states[k]
    s = tuple(col); cm = H.cm(s); V = H.order
    ch = H.chains(s, cm)
    out = dict(id=k, col=[None] * H.n, N=H.N[k], ell=H.ell[k], rim=H.rim[k], kd=len(H.nbrs[k]),
               dF=H.dF[k], filled=H.filled[k], DL=H.DL[k])
    for i, u in enumerate(V): out['col'][u] = s[i]
    if H.filled[k]:
        out['type'] = 'filled'
        out['chains'] = [dict(p=p, q=q, v=sorted(V[i] for i in range(H.m) if K >> i & 1), rim=bool(K & H.linkmask)) for p, q, K in ch]
        return out, None
    j = H.j[k]; x = [H.li[(j + t) % 5] for t in range(5)]; rn = role_names(s, x)
    out.update(j=j, frame=[V[i] for i in x], roles={ROLE[t]: [s[x[0]], s[x[1]], s[x[3]], s[x[4]]][t] for t in range(4)},
               L1=H.L1[k], L2=H.L2[k], dNDL=H.dNDL[k])
    al, mu, A, B = s[x[0]], s[x[1]], s[x[3]], s[x[4]]
    KL1 = H.flood(1 << x[1], cm[mu] | cm[A]); KL2 = H.flood(1 << x[1], cm[mu] | cm[B])
    Kpi = H.flood(1 << x[2], cm[al] | cm[A]); Ksig = H.flood(1 << x[2], cm[al] | cm[mu])
    chains = []
    for p, q, K in ch:
        e = dict(p=p, q=q, t=pair_label(p, q, rn), v=sorted(V[i] for i in range(H.m) if K >> i & 1), rim=bool(K & H.linkmask))
        if K == KL1: e['lock'] = 1
        if K == KL2: e['lock'] = 2
        if K == Kpi: e['pi'] = True
        if K == Ksig: e['sigma'] = True
        chains.append(e)
    chains.sort(key=lambda e: (ROLE_ORDER.index(e['t']), not e['rim'], -len(e['v'])))
    out['chains'] = chains
    out['tcount'] = {lab: sum(1 for e in chains if e['t'] == lab) for lab in ROLE_ORDER}
    out['locks'] = []
    if H.L1[k]: out['locks'].append([V[i] for i in bfs_path(H, KL1, x[1], x[3])])
    if H.L2[k]: out['locks'].append([V[i] for i in bfs_path(H, KL2, x[1], x[4])])
    extra = [e for e in chains if not e['rim']]
    out['extra'] = [e['t'] for e in extra]
    cw, eta = H.cw_eta(s)
    out.update(cw=cw, eta=eta)
    if H.DL[k]:
        if H.N[k] == 8: out['type'] = 'rigid'
        elif H.N[k] == 9:
            ins = H.pi[k] is not None and H.pinv[k] is not None and H.N[H.pi[k]] == 8 and H.N[H.pinv[k]] == 8 \
                and H.DL[H.pi[k]] and H.DL[H.pinv[k]]
            out['type'] = 'inshape' if ins else 'nine'
        else: out['type'] = 'dl'
    else:
        out['type'] = 'single'
        # Kempe's step: the open lock's chain from x3 (L1 open) or x4 (L2 open) is swapped, which fills the hole
        if not H.L1[k]: K = H.flood(1 << x[3], cm[mu] | cm[A]); fp = (mu, A)
        else: K = H.flood(1 << x[4], cm[mu] | cm[B]); fp = (mu, B)
        assert not K >> x[1] & 1
        out['fill'] = dict(lock=1 if not H.L1[k] else 2, v=sorted(V[i] for i in range(H.m) if K >> i & 1), pair=list(fp))
    return out, (al, A, Kpi)


def build_run(src):
    rot = read_rot(src['file'], src['name']); h = src['hole']; H = Hole(rot, h); S = H.S
    inNR = [H.DL[k] and H.N[k] <= 9 for k in range(S)]
    inR = [H.DL[k] and H.dNDL[k] >= 2 for k in range(S)]
    NR = H.maxrun(inNR, H.pi); NRi = H.maxrun(inNR, H.pinv); R = H.maxrun(inR, H.pi); Ri = H.maxrun(inR, H.pinv)
    assert NR == NRi and R == Ri
    # every unfilled state of this hole has exactly 8 chains meeting the rim (TrackJL-review J1 identity on the sphere)
    unf = [k for k in range(S) if not H.filled[k]]
    assert all(H.rim[k] == 8 for k in unf)
    # chain-count formula 2N = cw + (n-1) - eta + 2(L1+L2) mod 4 at every unfilled state; law at every DL state
    for k in unf:
        cw, eta = H.cw_eta(H.states[k])
        assert (2 * H.N[k] - cw - (H.n - 1) + eta - 2 * (H.L1[k] + H.L2[k])) % 4 == 0, 'formula'
    for k in range(S):
        if H.DL[k]:
            assert H.pi[k] is not None and H.pinv[H.pi[k]] == k
            u = H.pi[k]; assert (H.N[u] - H.N[k]) % 2 == int(H.DL[u]), 'law'
            assert H.j[u] == (H.j[k] + 3) % 5, 'frame advances by 3'
    # longest NR run (by pi), then its maximal doubly locked stretch, then the non-DL states at both ends
    runs = []
    for x in range(S):
        if inNR[x] and not (H.pinv[x] is not None and inNR[H.pinv[x]]):
            r = [x]; y = H.pi[x]
            while y is not None and inNR[y]: r.append(y); y = H.pi[y]
            runs.append(r)
    runs.sort(key=len, reverse=True); run = runs[0]; assert len(run) == NR and len(runs[1]) < NR
    back = []; y = H.pinv[run[0]]
    while y is not None and H.DL[y]: back.append(y); y = H.pinv[y]
    start = y; assert start is not None and not H.DL[start] and not H.filled[start]
    fwd = []; y = H.pi[run[-1]]
    while y is not None and H.DL[y]: fwd.append(y); y = H.pi[y]
    end = y; assert end is not None and not H.DL[end] and not H.filled[end]
    seq = [start] + back[::-1] + run + fwd + [end]
    # actual colours carried along the orbit by the real swaps (so colours stay continuous on screen)
    col = list(H.states[start]); steps = []
    for i, k in enumerate(seq):
        d, (al, A, Kpi) = describe(H, k, col)
        d['inRun'] = k in run
        steps.append(d)
        if i + 1 < len(seq):
            nxt = list(H.swap(tuple(col), Kpi, al, A))
            assert H.index[H.canon(nxt)] == H.pi[k] == seq[i + 1]
            d['next'] = 'pi'
            col = nxt
    # the fills at both ends (Kempe's step) give filled states
    pre, post = [], []
    for which, k, colk in (('pre', start, H.states[start]), ('post', end, col)):
        st = steps[0] if which == 'pre' else steps[-1]
        if which == 'pre': colk = [st['col'][u] for u in H.order]
        p, q = st['fill']['pair']; Kmask = sum(1 << H.idx[u] for u in st['fill']['v'])
        fc = list(H.swap(tuple(colk), Kmask, p, q)); kf = H.index[H.canon(fc)]
        assert H.filled[kf] and kf in H.nbrs[k]
        fd, _ = describe(H, kf, fc); fd['inRun'] = False
        (pre if which == 'pre' else post).append(fd)
    allsteps = pre + steps + post
    # census record check (runs-34.jsonl) for the p34 hole: N and Kempe degree along the run, before/after N, kd
    Ns = [H.N[k] for k in run]; kds = [len(H.nbrs[k]) for k in run]
    before = H.pinv[run[0]]; after = H.pi[run[-1]]
    if src['key'] == 'p34':
        rec = [json.loads(l) for l in open(os.path.join(WK, 'Census34/out/runs-34.jsonl')) if '11764701' in l]
        rec = [r for r in rec if r['h'] == h and r['L'] == 8][0]
        assert rec['N'] == Ns and rec['kd'] == kds, (rec, Ns, kds)
        assert rec['before'][1:] == [H.N[before], len(H.nbrs[before])] and rec['after'][1:] == [H.N[after], len(H.nbrs[after])]
        assert Ns == [9, 8, 9, 8, 9, 8, 9, 8] and H.N[before] == 10 and H.N[after] == 11
        vm = [l for l in open(os.path.join(WK, 'Census34/out/verify_maxima.txt')) if l.startswith(src['name'] + ' ')][0]
        nums = dict(re.findall(r'(\w+(?:\(\w+\))?)=(-?\d+)', vm))
        DLc = sum(H.DL); interior = sum(inR)
        assert int(nums['S']) == S and int(nums['DL']) == DLc and int(nums['interior']) == interior
        assert int(nums['R(pi)']) == R == 8 and int(nums['NR(pi)']) == NR == 8
    if src['key'] == 'p33':
        assert NR == 8 and R == 2 and Ns == [8, 9, 8, 9, 8, 9, 8, 9]
    # ---- cross-check (1): TrackM tm_lib.Hole (Track A kempe_py), state by state on the whole window + global counts
    sys.path.insert(0, os.path.join(WK, 'TrackM'))
    from tm_lib import Hole as TMHole
    T = TMHole(rot, h); T.classes_and_dist()
    assert T.S == S
    tmap = {}
    for k in range(S):
        cdict = {u: H.states[k][i] for u, i in H.idx.items()}
        tmap[k] = T.sp.state_of(cdict)
    assert len(set(tmap.values())) == S
    for k in range(S):
        t = tmap[k]
        assert T.Nch[t] == H.N[k] and T.ell[t] == H.ell[k] and T.filled[t] == H.filled[k] and T.dF[t] == H.dF[k]
        if not H.filled[k]:
            assert T.L1[t] == H.L1[k] and T.L2[t] == H.L2[k] and T.j[t] == H.j[k]
            assert (T.pi[t] is None) == (H.pi[k] is None) and (H.pi[k] is None or T.pi[t] == tmap[H.pi[k]])
        assert len({m[0] for m in T.moves[t]}) == len(H.nbrs[k])
    assert T.ncl == H.ncl
    # ---- cross-check (2): rv_eng (TrackJL-review), summary counters
    rv = os.path.join(WK, 'TrackJL-review', 'rv_eng')
    line = src['name'] + ' ' + str(H.n) + ' ' + ';'.join(','.join(map(str, r)) for r in rot) + '\n'
    outp = subprocess.run([rv, '-E', '2', '-H', str(h)], input=line, capture_output=True, text=True, check=True).stdout
    summ = dict(re.findall(r'(\w+)=(\d+)', outp.splitlines()[0]))
    assert int(summ['states']) == S and int(summ['maxRrun']) == NR and int(summ['Rcycles']) == 0
    chk = {m.group(1).strip(): (int(m.group(2)), int(m.group(3))) for m in re.finditer(r'^\s+(.*?)\s+checks=(\d+) fails=(\d+)', outp, re.M)}
    assert all(f == 0 for _, f in chk.values()), 'rv_eng failures'
    assert chk['DL states'][0] == sum(H.DL)
    assert chk['rigid states'][0] == sum(1 for k in range(S) if H.DL[k] and H.N[k] == 8)
    assert chk['chain-parity law N(pi c)-N(c) = [pi c DL] mod 2 (sphere)'][0] == sum(H.DL)
    nins = sum(1 for k in range(S) if H.DL[k] and H.N[k] == 9 and H.pi[k] is not None and H.pinv[k] is not None
               and H.DL[H.pi[k]] and H.DL[H.pinv[k]] and H.N[H.pi[k]] == 8 and H.N[H.pinv[k]] == 8)
    assert chk['in-shape states'][0] == nins
    # Z-type: at in-shape states on the window the extra chain is alpha-mu (sigma-type lemma)
    for d in allsteps:
        if d['type'] == 'inshape': assert d['extra'] == ['αμ']
        if d['type'] == 'rigid': assert d['tcount'] == {'αμ': 1, 'AB': 1, 'αA': 2, 'μB': 1, 'αB': 2, 'μA': 1}
        if d['type'] in ('rigid', 'inshape', 'nine', 'dl', 'single'): assert d['rim'] == 8
    pos, outer, gp = layout(rot, h)
    deg = [len(r) for r in rot]
    edges = sorted({(min(u, w), max(u, w)) for u in range(H.n) for w in rot[u]})
    stats = dict(S=S, DL=sum(H.DL), rigid=sum(1 for k in range(S) if H.DL[k] and H.N[k] == 8), inshape=nins,
                 unfilled=len(unf), filled=S - len(unf), classes=H.ncl, NR=NR, R=R, interior=sum(inR),
                 runsNR=sorted([len(r) for r in runs], reverse=True)[:6], maxdF=max(H.dF))
    print(src['name'], 'h', h, stats, 'window', len(allsteps), 'N', [d['N'] for d in allsteps], round(time.time() - t0, 1), 's')
    return dict(key=src['key'], name=src['name'], label=src['label'], blurb=src['blurb'], n=H.n, hole=h, link=H.link,
                deg=deg, pos=pos, edges=edges, faces=H.faces, stats=stats, steps=allsteps,
                runStart=len(pre) + 1 + len(back), runLen=NR)


# =============================================================== census chart: max run length by order
def census_chart():
    rows = {}
    for n in range(22, 33):
        p = os.path.join(WK, 'TrackO/out', 'frame-%d.jsonl' % n)
        f = open(p) if os.path.exists(p) else gzip.open(p + '.gz', 'rt')
        R = NR = holes = 0; cnt = collections.Counter()
        for l in f:
            d = json.loads(l)
            if 'run' in d: continue
            holes += 1; R = max(R, d['R']); NR = max(NR, d['NR']); cnt[('NR', d['NR'])] += 1; cnt[('R', d['R'])] += 1
            assert d['NRcyc'] == 0
        rows[n] = dict(n=n, R=R, NR=NR, holes=holes, atNR=cnt[('NR', NR)], atR=cnt[('R', R)])
    for n, p in ((33, 'Census33/out/eval-33.jsonl.gz'), (34, 'Census34/out/eval-34.jsonl.gz')):
        R = NR = holes = 0; cnt = collections.Counter()
        for l in gzip.open(os.path.join(WK, p), 'rt'):
            d = json.loads(l)
            for hh, x in d['holes'].items():
                holes += 1; R = max(R, x['R']); NR = max(NR, x['NR']); cnt[('NR', x['NR'])] += 1; cnt[('R', x['R'])] += 1
                assert x['NRcyc'] == 0
        rows[n] = dict(n=n, R=R, NR=NR, holes=holes, atNR=cnt[('NR', NR)], atR=cnt[('R', R)])
    # the README trend table of Census34 (orders 22-34)
    txt = open(os.path.join(WK, 'Census34/README.md')).read()
    def row(lbl):
        m = re.search(r'^\| ' + re.escape(lbl) + r' \|(.*)$', txt, re.M)
        return [int(x.strip().strip('*')) for x in m.group(1).split('|') if x.strip()]
    tR, tNR, tatNR = row('max R'), row('max NR'), row('holes at max NR')
    for i, n in enumerate(range(22, 35)):
        assert rows[n]['R'] == tR[i] and rows[n]['NR'] == tNR[i] and rows[n]['atNR'] == tatNR[i], (n, rows[n])
    assert rows[34]['holes'] == 3612341
    # orders 22-25 recomputed from scratch with this page's engine (every frame-class hole)
    for n in (22, 23, 24, 25):
        R = NR = 0
        for l in open(os.path.join(WK, 'Census29/out', 'frame-%d.txt' % n)):
            p = l.split(); rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
            for h in range(len(rot)):
                if len(rot[h]) != 5: continue
                H = Hole(rot, h); S = H.S
                inNR = [H.DL[k] and H.N[k] <= 9 for k in range(S)]
                inR = [H.DL[k] and H.dNDL[k] >= 2 for k in range(S)]
                NR = max(NR, H.maxrun(inNR, H.pi)); R = max(R, H.maxrun(inR, H.pi))
        assert (R, NR) == (rows[n]['R'], rows[n]['NR']), (n, R, NR)
    print('chart', [(n, rows[n]['R'], rows[n]['NR']) for n in range(22, 35)], round(time.time() - t0, 1), 's')
    return [rows[n] for n in range(22, 35)]


if __name__ == '__main__':
    runs = [build_run(s) for s in SRC]
    chart = census_chart()
    data = dict(runs=runs, chart=chart, built=time.strftime('%Y-%m-%d'),
                note='Generated by docs/alternation/build_data.py; every number cross-checked against tm_lib, rv_eng and the census files.')
    with open(os.path.join(HERE, 'data.js'), 'w') as f:
        f.write('// Generated by docs/alternation/build_data.py. Do not edit.\n')
        f.write('window.ALT_DATA = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
    print('wrote data.js', os.path.getsize(os.path.join(HERE, 'data.js')), 'bytes', round(time.time() - t0, 1), 's')
