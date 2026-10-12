#!/usr/bin/env python3
"""[Track E] Labelled-colouring Kempe space of T - v with phase statistics, swap types, lock involution.

Engine: kempe_py.Space (project engine; canonical states = proper 4-colourings of T - v up to renaming).  A LABELLED
colouring is (k, g): canonical state k with colours renamed by the permutation g (tuple, g[c] = new colour), 24 per k.
All swaps are whole-component Kempe swaps of labelled colourings (no renaming afterwards), so a phase phi(labelled
colouring) and its change under one chain swap are well defined.

Statistics (integers) of a labelled colouring c, used as candidate exponents of (-1)^f, i^f, zeta^f:
  P      #triangular faces of T - v with Heawood sign +1   (H = 2P - m, so i^H = const * (-1)^P)
  Pr     same, on the 5 ring faces x_t x_{t+1} w_t only
  n0..n3 colour-class sizes;  l0..l3 colour counts on the link
  AT1_*  descents of c along a fixed acyclic orientation (u -> w iff u < w), 12 colour orders (Alon-Tarsi-type sign)
  KS_*   descents along a Kasteleyn orientation of T - v (every triangular face has an odd number of clockwise
         edges), 12 colour orders
  io_pq  # {p,q}-Kempe components whose least vertex has colour p (the "cube coordinate" parity), 6 pairs
  kc_pq  # {p,q}-Kempe components, 6 pairs
  fil    filled indicator;  W winding of the pi-orbit (Theorem W, NightEulerHole);  lam;  rep (repeat/unique index, Z5)
  L1 L2  lock bits;  hv_t  Heawood vertex sum (sum of face signs around link vertex x_t, T - v faces only), 5 values
"""
import sys, os, itertools
from collections import Counter
LT = '/Users/kylemathewson/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/local-runs'
sys.path.insert(0, os.path.join(LT, 'common')); sys.path.insert(0, os.path.join(LT, '22-winding-escape'))
from kempe_py import Space, gentri_rotation, adj_from_rot
from escape import pi_of

PERMS = list(itertools.permutations(range(4)))
PIDX = {p: i for i, p in enumerate(PERMS)}
PAIRS = list(itertools.combinations(range(4), 2))
ORDERS = [p for p in PERMS if p[0] < p[3]]          # 12 colour orders up to reversal

def psign(p):
    s = 1; p = list(p)
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]: s = -s
    return s

def compose(g, h):  # (g o h)[c] = g[h[c]]
    return tuple(g[h[c]] for c in range(4))

def inv(g):
    r = [0] * 4
    for c in range(4): r[g[c]] = c
    return tuple(r)

STAT_NAMES = (['P', 'Pr'] + ['n%d' % c for c in range(4)] + ['l%d' % c for c in range(4)]
              + ['AT1_%s' % ''.join(map(str, o)) for o in ORDERS] + ['KS_%s' % ''.join(map(str, o)) for o in ORDERS]
              + ['io_%d%d' % pq for pq in PAIRS] + ['kc_%d%d' % pq for pq in PAIRS]
              + ['fil', 'W', 'lam', 'rep', 'L1', 'L2'] + ['hv%d' % t for t in range(5)])
NS = len(STAT_NAMES)
SI = {n: i for i, n in enumerate(STAT_NAMES)}

class LSpace:
    def __init__(self, rot, h):
        self.rot = rot; self.h = h; n = len(rot)
        adj = adj_from_rot(rot)
        self.sp = sp = Space(adj, h, link=rot[h]); self.S = S = len(sp.states); N = sp.N
        idx = sp.idx; self.link = rot[h]; self.li = sp.linki
        self.linkmask = 0
        for i in self.li: self.linkmask |= 1 << i
        # faces (consistent orientation from rotation) ; check each directed edge once
        faces = set()
        for v in range(n):
            r = rot[v]
            for i in range(len(r)):
                f = (v, r[i], r[(i + 1) % len(r)]); m = f.index(min(f)); faces.add(f[m:] + f[:m])
        de = Counter()
        for f in faces:
            for i in range(3): de[(f[i], f[(i + 1) % 3])] += 1
        assert all(c == 1 for c in de.values()) and len(faces) == 2 * n - 4, 'rotation not a consistent triangulation'
        self.tri = [tuple(idx[x] for x in f) for f in faces if h not in f]     # triangular faces of T - v, oriented
        L = self.link; self.ring = []
        for f in self.tri:
            vs = [sp.order[x] for x in f]
            for t in range(5):
                if L[t] in vs and L[(t + 1) % 5] in vs: self.ring.append(f)
        assert len(self.ring) == 5
        self.vfaces = [[f for f in self.tri if self.li[t] in f] for t in range(5)]
        # edges and orientations
        E = set()
        for f in self.tri:
            for i in range(3): E.add((min(f[i], f[(i + 1) % 3]), max(f[i], f[(i + 1) % 3])))
        self.E = sorted(E)
        self.O1 = list(self.E)                     # u -> w with u < w (BFS index order)
        self.O2 = self.kasteleyn()
        # canonical-state data
        self.pi = [0] * S; self.lam = [0] * S
        for k in range(S): t, l, _ = pi_of(sp, k); self.pi[k] = t; self.lam[k] = l
        self.W = [0] * S; seen = [False] * S
        for k in range(S):
            if seen[k]: continue
            z = []; x = k
            while not seen[x]: seen[x] = True; z.append(x); x = self.pi[x]
            w = sum(self.lam[y] for y in z) // 5
            for y in z: self.W[y] = w
        self.comps = [None] * S; self.raw = [None] * S; self.trans = [None] * S
        for k in range(S): self._prep(k)

    def kasteleyn(self):
        """orientation of E(T - v): every triangular face (oriented f0->f1->f2) has an odd number of edges directed against it."""
        ori = {e: e for e in self.E}       # current direction (a, b): a -> b
        # dual spanning tree rooted at the hole: faces adjacent via edges; leaves fixed first
        e2f = {}
        for fi, f in enumerate(self.tri):
            for i in range(3): e2f.setdefault((min(f[i], f[(i + 1) % 3]), max(f[i], f[(i + 1) % 3])), []).append(fi)
        ROOT = -1
        adjf = {}
        for e, fs in e2f.items():
            if len(fs) == 1: fs = fs + [ROOT]
            a, b = fs; adjf.setdefault(a, []).append((b, e)); adjf.setdefault(b, []).append((a, e))
        par = {ROOT: None}; order = [ROOT]
        for x in order:
            for y, e in adjf[x]:
                if y not in par: par[y] = (x, e); order.append(y)
        tree_e = {par[y][1] for y in par if par[y] is not None}
        def against(fi):
            f = self.tri[fi]; c = 0
            for i in range(3):
                a, b = f[i], f[(i + 1) % 3]
                if ori[(min(a, b), max(a, b))] != (a, b): c += 1
            return c
        for y in reversed(order):
            if y == ROOT: continue
            if against(y) % 2 == 0:
                e = par[y][1]; a, b = ori[e]; ori[e] = (b, a)
        assert all(against(fi) % 2 == 1 for fi in range(len(self.tri)))
        return [ori[e] for e in self.E]

    def _prep(self, k):
        sp = self.sp; s = sp.states[k]; cm = sp.cmasks(s)
        comps = {}; trans = {}
        for pq in PAIRS:
            cl = sp.components(s, pq[0], pq[1], cm); comps[pq] = cl
            for K in cl:
                d = list(s)
                for i in range(sp.N):
                    if K >> i & 1: d[i] = pq[1] if s[i] == pq[0] else pq[0]
                mp = {}; cd = tuple(mp.setdefault(x, len(mp)) for x in d)
                hmap = [None] * 4
                for a_, b_ in mp.items(): hmap[a_] = b_
                miss = [c for c in range(4) if c not in mp.values()]; j = 0
                for a_ in range(4):
                    if hmap[a_] is None: hmap[a_] = miss[j]; j += 1
                trans[(pq, K)] = (sp.index[cd], tuple(hmap))     # canonical(d) = hmap o d
        self.comps[k] = comps; self.trans[k] = trans
        # raw data for labelled stats
        sig = lambda f: psign((s[f[0]], s[f[1]], s[f[2]], 6 - s[f[0]] - s[f[1]] - s[f[2]]))
        cnt = Counter(s); lc = Counter(s[i] for i in self.li)
        R = {}
        R['sigsum'] = sum(sig(f) for f in self.tri); R['rsigsum'] = sum(sig(f) for f in self.ring)
        R['hv'] = [sum(sig(f) for f in self.vfaces[t]) for t in range(5)]
        R['n'] = [cnt[c] for c in range(4)]; R['l'] = [lc[c] for c in range(4)]
        R['desc1'] = {o: sum(1 for (u, w) in self.O1 if o.index(s[u]) > o.index(s[w])) for o in PERMS}
        R['desc2'] = {o: sum(1 for (u, w) in self.O2 if o.index(s[u]) > o.index(s[w])) for o in PERMS}
        io = {}
        for pq in PAIRS:
            for p, q in (pq, pq[::-1]):
                io[(p, q)] = sum(1 for K in comps[pq] if s[(K & -K).bit_length() - 1] == p)
        R['io'] = io; R['kc'] = {pq: len(comps[pq]) for pq in PAIRS}
        R['fil'] = int(sp.filled(k)); R['W'] = self.W[k]; R['lam'] = self.lam[k]
        c = [s[i] for i in self.li]; cc = Counter(c)
        if len(cc) == 4:
            j = next(j for j in range(5) if c[j] == c[(j + 2) % 5] and cc[c[j]] == 2); R['rep'] = j
            lk = self.locks(k); R['L'] = (int(lk[0] is not None), int(lk[1] is not None))
        else:
            R['rep'] = next(i for i in range(5) if cc[c[i]] == 1); R['L'] = (0, 0)
        self.raw[k] = R

    def locks(self, k):
        """(lock1 chain, lock2 chain) as ((p,q) canonical pair, mask) or None; None, None if filled."""
        sp = self.sp; s = sp.states[k]; li = self.li; c = [s[i] for i in li]; cc = Counter(c)
        if len(cc) != 4: return (None, None)
        j = next(j for j in range(5) if c[j] == c[(j + 2) % 5] and cc[c[j]] == 2)
        mu, A, B = c[(j + 1) % 5], c[(j + 3) % 5], c[(j + 4) % 5]; m, a, b = li[(j + 1) % 5], li[(j + 3) % 5], li[(j + 4) % 5]
        out = []
        for X, x in ((A, a), (B, b)):
            pq = tuple(sorted((mu, X))); hit = None
            for K in self.comps[k][pq]:
                if K >> m & 1 and K >> x & 1: hit = (pq, K)
            out.append(hit)
        return tuple(out)

    def stats(self, k, g):
        """stat vector of labelled colouring g o s_k."""
        R = self.raw[k]; gi = inv(g); sg = psign(g)
        P = (sg * R['sigsum'] + len(self.tri)) // 2; Pr = (sg * R['rsigsum'] + 5) // 2
        v = [P, Pr] + [R['n'][gi[c]] for c in range(4)] + [R['l'][gi[c]] for c in range(4)]
        # descents of g o s under order o  ==  descents of s under order o' with o'.index(x) = o.index(g[x])
        for key in ('desc1', 'desc2'):
            for o in ORDERS:
                o2 = tuple(sorted(range(4), key=lambda x: o.index(g[x])))
                v.append(R[key][o2])
        for p, q in PAIRS: v.append(R['io'][(gi[p], gi[q])])
        for p, q in PAIRS: v.append(R['kc'][tuple(sorted((gi[p], gi[q])))])
        v += [R['fil'], R['W'], R['lam'], R['rep'], R['L'][0], R['L'][1]]
        v += [sg * x for x in R['hv']]
        return v

    def move(self, k, g, pq, K):
        """labelled swap of component K (a {pq}-component of canonical s_k; labelled pair g[pq]) -> (k', g')."""
        k2, hmap = self.trans[k][(pq, K)]
        # labelled result = g o d, and canonical s_k2 = hmap o d  =>  g o d = (g o hmap^-1) o s_k2
        return k2, compose(g, inv(hmap))

    def chain_type(self, k, pq, K):
        nl = bin(K & self.linkmask).count('1')
        allK = len(self.comps[k][pq]) == 1
        return nl, allK
