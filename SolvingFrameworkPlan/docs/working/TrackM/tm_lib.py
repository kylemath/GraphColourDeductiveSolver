#!/usr/bin/env python3
"""Track M [exploratory]: guided Kempe-swap escape rules ("discharge"-scored walks) at a degree-5 hole.

Engine: kempe_py.Space (Track A's stdlib bitmask engine; states = proper 4-colourings of T - h up to renaming; a move is
a whole-component Kempe swap; renamings are dropped). No planarity is used, so it runs on any triangulated surface.

Per state (frame of the state: link (alpha, mu, alpha, A, B) at x_j..x_{j+4}, as in TrackG / LockParity.md):
  filled, j, L1 = x_{j+3} in K_{mu A}(x_{j+1}), L2 = x_{j+4} in K_{mu B}(x_{j+1}), Phi = L1 + L2 (-1 if filled),
  N = total number of Kempe chains (all 6 pair graphs), ell = number of link-free chains,
  lockSize = |K_{muA}(x_{j+1})| + |K_{muB}(x_{j+1})|, lockLen = shortest-path length of the lock chains (0 if absent),
  pi (TrackF 5.2), sigma = swap K_{alpha mu}(x_{j+2}).
Per move (chain K): |K|, curv = sum_{v in K} (6 - deg_T v), dist = min_{v in K} d_T(h, v), sector/radius cell.
"""
import sys, os, itertools, json
from collections import deque, Counter
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../../..'))
sys.path.insert(0, os.path.join(ROOT, 'backgroundMaterial/planemap-structural/longtable/local-runs/common'))
from kempe_py import Space  # noqa: E402

KMAX = 10


def read_rot_lines(path, names=None):
    out = []
    for l in open(path):
        p = l.split()
        if len(p) < 3 or (names is not None and p[0] not in names): continue
        out.append((p[0], [list(map(int, r.split(','))) for r in p[2].split(';')]))
    return out


def rot_from_faces(F):
    nxt = {}
    for f in F:
        for i in range(3): nxt[(f[i], f[(i + 1) % 3])] = f[(i + 2) % 3]
    n = 1 + max(max(f) for f in F); rot = []
    for v in range(n):
        start = [b for (a, b) in nxt if a == v][0]; r = [start]
        while True:
            y = nxt[(v, r[-1])]
            if y == start: break
            r.append(y)
        rot.append(r)
    return rot


def hsh(a, b, seed=0):
    x = (a * 2654435761 + b * 40503 + seed * 97) & 0xFFFFFFFF
    x ^= x >> 15; x = (x * 2246822519) & 0xFFFFFFFF; x ^= x >> 13
    return x


class Hole:
    def __init__(self, rot, h):
        self.rot = rot; self.h = h; Lk = rot[h]; assert len(Lk) == 5
        adj = {v: set(x) for v, x in enumerate(rot)}
        self.sp = sp = Space(adj, h, link=Lk)
        N = sp.N; self.S = S = len(sp.states)
        deg = [len(rot[sp.order[i]]) for i in range(N)]
        self.curvv = [6 - d for d in deg]
        # distance from hole in T, sector = nearest rim vertex (index in link), ties -> smallest index
        dT = {h: 0}; q = deque([h])
        while q:
            u = q.popleft()
            for w in rot[u]:
                if w not in dT: dT[w] = dT[u] + 1; q.append(w)
        self.distv = [dT[sp.order[i]] for i in range(N)]
        sec = [-1] * N; dd = [-1] * N; q = deque()
        for t, x in enumerate(sp.linki): sec[x] = t; dd[x] = 0; q.append(x)
        nbl = [[w for w in range(N) if sp.nbm[i] >> w & 1] for i in range(N)]
        while q:
            u = q.popleft()
            for w in nbl[u]:
                if dd[w] < 0: dd[w] = dd[u] + 1; sec[w] = sec[u]; q.append(w)
                elif dd[w] == dd[u] + 1 and sec[u] < sec[w]: sec[w] = sec[u]
        self.secv = sec
        self.linkmask = sum(1 << x for x in sp.linki)
        self._states()

    def _path_len(self, M, a, b):
        nbm = self.sp.nbm; d = {a: 0}; q = deque([a])
        while q:
            u = q.popleft()
            if u == b: return d[u]
            m = nbm[u] & M
            while m:
                low = m & -m; w = low.bit_length() - 1; m ^= low
                if w not in d: d[w] = d[u] + 1; q.append(w)
        return 0

    def _states(self):
        sp = self.sp; S = self.S; li = sp.linki; pc = lambda m: bin(m).count('1')
        self.filled = [False] * S; self.phi = [0] * S; self.j = [-1] * S; self.L1 = [0] * S; self.L2 = [0] * S
        self.Nch = [0] * S; self.ell = [0] * S; self.lsize = [0] * S; self.llen = [0] * S
        self.pi = [None] * S; self.pinv = [None] * S; self.sigma = [None] * S; self.kempe2 = [None] * S; self.k2info = [None] * S
        self.moves = [None] * S   # list of (t, |K|, curv, dist, cellkey, pairtype)
        for k in range(S):
            s = sp.states[k]; cm = sp.cmasks(s)
            c = [s[li[t]] for t in range(5)]
            mv = []; Ntot = 0; ell = 0; seen = set()
            for p, qq in itertools.combinations(range(4), 2):
                comps = sp.components(s, p, qq, cm)
                Ntot += len(comps)
                for K in comps:
                    if not K & self.linkmask: ell += 1
                    if len(comps) == 1: continue  # renaming
                    t = sp.index[sp.swap(s, K, p, qq)]
                    if t == k: continue
                    idx = [i for i in range(sp.N) if K >> i & 1]
                    cu = sum(self.curvv[i] for i in idx); di = min(self.distv[i] for i in idx)
                    # anchor cell: min radius vertex, its sector
                    a = min(idx, key=lambda i: (self.distv[i], self.secv[i]))
                    mv.append((t, len(idx), cu, di, (self.distv[a], self.secv[a]), (p, qq), K))
            self.moves[k] = mv; self.Nch[k] = Ntot; self.ell[k] = ell
            if len(set(c)) <= 3:
                self.filled[k] = True; self.phi[k] = -1; continue
            j = next(t for t in range(5) if c[t] == c[(t + 2) % 5]); self.j[k] = j
            x = [li[(j + t) % 5] for t in range(5)]
            al, mu, A, B = c[j], c[(j + 1) % 5], c[(j + 3) % 5], c[(j + 4) % 5]
            fl = lambda v, p, qq: sp.flood(1 << v, cm[p] | cm[qq])
            KMA = fl(x[1], mu, A); KMB = fl(x[1], mu, B)
            L1 = KMA >> x[3] & 1; L2 = KMB >> x[4] & 1
            self.L1[k] = L1; self.L2[k] = L2; self.phi[k] = L1 + L2
            self.lsize[k] = pc(KMA) + pc(KMB)
            self.llen[k] = (self._path_len(KMA, x[1], x[3]) if L1 else 0) + (self._path_len(KMB, x[1], x[4]) if L2 else 0)
            KAA = fl(x[2], al, A)
            if not (KAA >> x[0] & 1): self.pi[k] = sp.index[sp.swap(s, KAA, al, A)]
            KBj = fl(x[0], al, B)
            if not (KBj >> x[2] & 1): self.pinv[k] = sp.index[sp.swap(s, KBj, al, B)]
            KAM = fl(x[2], al, mu)
            self.sigma[k] = sp.index[sp.swap(s, KAM, al, mu)]
            if L1 and L2:
                # Kempe's 1879 double swap: swap K_{aB}(x_{j+2}) (x_{j+2} -> B), then K_{aA}(x_j) in the new colouring
                # (x_j -> A); and the mirror order. Success iff the result is filled.
                res = []
                for (v1, c1, v2, c2) in ((x[2], B, x[0], A), (x[0], A, x[2], B)):
                    K1 = fl(v1, al, c1); s1 = list(s)
                    for i in range(sp.N):
                        if K1 >> i & 1: s1[i] = c1 if s[i] == al else al
                    cm1 = [0, 0, 0, 0]
                    for i, y in enumerate(s1): cm1[y] |= 1 << i
                    if not cm1[al] >> v2 & 1:   # off-sphere only: swap 1 recoloured v2 itself
                        res.append((False, True, k)); continue
                    K2 = sp.flood(1 << v2, cm1[al] | cm1[c2]); s2 = list(s1)
                    for i in range(sp.N):
                        if K2 >> i & 1: s2[i] = c2 if s1[i] == al else al
                    ok = len({s2[i] for i in li}) <= 3
                    # interference: did swap 1 break the blocking lock chain of swap 2?
                    if v1 == x[2]:
                        blk_before = L2; blk_after = sp.flood(1 << x[1], cm1[mu] | cm1[B]) >> x[4] & 1
                    else:
                        blk_before = L1; blk_after = sp.flood(1 << x[1], cm1[mu] | cm1[A]) >> x[3] & 1
                    res.append((ok, bool(blk_before) and not blk_after, sp.index[sp.canon(s2)]))
                self.kempe2[k] = res

    # -------- all-DL pi-cycles --------
    def allDL_cycle_states(self):
        dl = lambda k: (not self.filled[k]) and self.phi[k] == 2
        seen = set(); on = set()
        for i in range(self.S):
            if not dl(i) or i in seen: continue
            path = []; pos = {}; k = i
            while k is not None and dl(k) and k not in pos and k not in seen:
                pos[k] = len(path); path.append(k); k = self.pi[k]
            seen.update(path)
            if k is not None and k in pos: on.update(path[pos[k]:])
        return on

    def classes_and_dist(self):
        S = self.S; G = [[m[0] for m in self.moves[k]] for k in range(S)]
        cl = [-1] * S; n = 0
        for s in range(S):
            if cl[s] >= 0: continue
            cl[s] = n; q = [s]
            for x in q:
                for t in G[x]:
                    if cl[t] < 0: cl[t] = n; q.append(t)
            n += 1
        d = [-1] * S; q = deque()
        for s in range(S):
            if self.filled[s]: d[s] = 0; q.append(s)
        while q:
            x = q.popleft()
            for t in G[x]:
                if d[t] < 0: d[t] = d[x] + 1; q.append(t)
        dS = [-1] * S; q = deque()
        for s in range(S):
            if self.filled[s] or self.phi[s] < 2: dS[s] = 0; q.append(s)
        while q:
            x = q.popleft()
            for t in G[x]:
                if dS[t] < 0: dS[t] = dS[x] + 1; q.append(t)
        self.cl = cl; self.ncl = n; self.dF = d; self.dNDL = dS
        return cl, d


# ------------------------------------------------------------------ rules
def dj(H, u, t):
    """signed winding change of the repeat position, in -2..2 (0 if either side filled)"""
    if H.j[u] < 0 or H.j[t] < 0: return 0
    d = (H.j[t] - H.j[u]) % 5
    return d - 5 if d > 2 else d

# feature extractors on (H, u, move) -> number (lower = preferred after sign)
FEAT = {
    'N':     lambda H, u, m: H.Nch[m[0]] - H.Nch[u],      # Delta N (merges < 0 < splits)
    'ell':   lambda H, u, m: H.ell[m[0]] - H.ell[u],      # Delta link-free chains
    'lsize': lambda H, u, m: H.lsize[m[0]],               # lock-chain sizes in the target frame
    'llen':  lambda H, u, m: H.llen[m[0]],                # lock-chain lengths in the target frame
    'wind':  lambda H, u, m: dj(H, u, m[0]),              # winding change
    'curv':  lambda H, u, m: m[2],                        # curvature charge along K
    'dist':  lambda H, u, m: m[3],                        # distance K -> hole
    'size':  lambda H, u, m: m[1],                        # |K|
}


def make_rules():
    R = {}
    R['RAND'] = ('greedy', lambda H, u, m: ())
    R['PHI'] = ('greedy', lambda H, u, m: (H.phi[m[0]],))
    R['PHI+sigma'] = ('greedy', lambda H, u, m: (H.phi[m[0]], 0 if m[0] == H.sigma[u] else 1))
    R['sigma'] = ('greedy', lambda H, u, m: (0 if m[0] == H.sigma[u] else 1,))
    for f, fn in FEAT.items():
        for sg, nm in ((1, 'min'), (-1, 'max')):
            R['%s-%s' % (nm, f)] = ('greedy', (lambda fn, sg: lambda H, u, m: (sg * fn(H, u, m),))(fn, sg))
            R['PHI>%s-%s' % (nm, f)] = ('greedy', (lambda fn, sg: lambda H, u, m: (H.phi[m[0]], sg * fn(H, u, m)))(fn, sg))
    # combined "discharge" scores (lexicographic after Phi)
    R['PHI>lsize>N'] = ('greedy', lambda H, u, m: (H.phi[m[0]], H.lsize[m[0]], -FEAT['N'](H, u, m)))
    R['PHI>sigma>lsize'] = ('greedy', lambda H, u, m: (H.phi[m[0]], 0 if m[0] == H.sigma[u] else 1, H.lsize[m[0]]))
    R['PHI>dist>curv'] = ('greedy', lambda H, u, m: (H.phi[m[0]], m[3], -m[2]))
    R['KEMPE'] = ('kempe', None)
    for b, w in ((2, 0), (2, 2), (4, 4)):
        R['BEAM%d+%d' % (b, w)] = ('beam', (b, w))
    R['DIR'] = ('dir', None)
    R['PHI-adv'] = ('adv', None)
    R['OPT'] = ('opt', None)
    return R


RULES = make_rules()


def walk_greedy(H, s, key, seed=0):
    """returns (steps to filled or None, path)"""
    if H.filled[s]: return 0, [s]
    vis = {s}; u = s; path = [s]
    for step in range(1, KMAX + 1):
        best = None; bk = None
        for m in H.moves[u]:
            t = m[0]
            if t in vis: continue
            if H.filled[t]: best = t; break
            k = key(H, u, m) + (hsh(u, t, seed),)
            if bk is None or k < bk: bk = k; best = t
        if best is None: return None, path
        u = best; vis.add(u); path.append(u)
        if H.filled[u]: return step, path
    return None, path


def walk_kempe(H, s):
    """Kempe 1879: if one swap fills, do it; at a DL state do the double swap (either order); otherwise give up."""
    if H.filled[s]: return 0, [s]
    for m in H.moves[s]:
        if H.filled[m[0]]: return 1, [s, m[0]]
    if H.kempe2[s] is not None:
        for ok, _, t in H.kempe2[s]:
            if ok: return 2, [s, t]
    return None, [s]


def beam(H, s, b, w):
    if H.filled[s]: return 0, [s]
    key = lambda t: (H.phi[t], H.lsize[t], -H.Nch[t])
    vis = {s}; front = [s]
    for step in range(1, KMAX + 1):
        ch = []
        for u in front:
            for m in H.moves[u]:
                t = m[0]
                if t in vis: continue
                if H.filled[t]: return step, [s, t]
                vis.add(t); ch.append(t)
        if not ch: return None, [s]
        ch.sort(key=lambda t: key(t) + (hsh(s, t),))
        front = ch[:b] + (ch[-w:] if w and len(ch) > b else [])
        front = list(dict.fromkeys(front))
    return None, [s]


def walk_dir(H, s):
    """Directional sweep: cells (radius r, sector offset o) visited radius-major, sectors starting from the repeat
    vertex x_j and going round the link; at each step the candidate chains are those anchored in the current cell
    (anchor = the chain vertex nearest the hole); take the best by (Phi, lsize); if the cell has none, advance the cursor.
    Tabu on visited states. Steps = swaps made."""
    if H.filled[s]: return 0, [s]
    maxr = max(H.distv)
    vis = {s}; u = s; path = [s]; steps = 0
    cells = [(r, o) for r in range(1, maxr + 1) for o in range(5)]
    ci = 0; idle = 0
    while steps < KMAX and idle < len(cells):
        r, o = cells[ci]; j0 = H.j[u] if H.j[u] >= 0 else 0; sec = (j0 + o) % 5
        cand = [m for m in H.moves[u] if m[4] == (r, sec) and m[0] not in vis]
        for m in H.moves[u]:
            if H.filled[m[0]] and m[0] not in vis: cand = [m]; break
        ci = (ci + 1) % len(cells)
        if not cand: idle += 1; continue
        idle = 0
        m = min(cand, key=lambda m: (H.phi[m[0]], H.lsize[m[0]], hsh(u, m[0])))
        u = m[0]; vis.add(u); path.append(u); steps += 1
        if H.filled[u]: return steps, path
        ci = 0  # restart the sweep from the hole after each swap
    return None, path


def run_rule(H, name, s):
    kind, arg = RULES[name]
    if kind == 'greedy': return walk_greedy(H, s, arg)
    if kind == 'kempe': return walk_kempe(H, s)
    if kind == 'beam': return beam(H, s, *arg)
    if kind == 'dir': return walk_dir(H, s)
    if kind == 'adv': return adv_phi(H, s)
    if kind == 'opt':
        d = H.dF[s]; return (d if 0 <= d <= KMAX else None), [s]


def adv_phi(H, s, budget=200000):
    """Phi-greedy against an ADVERSARIAL tie-break (tabu on visited states): returns the worst-case number of swaps to a
    filled state over all tie-breaks, or None if some tie-break sequence fails within KMAX (trapped or too long).
    Rule: take a filled neighbour if any; else move to an unvisited neighbour of minimal Phi (adversary picks which)."""
    if H.filled[s]: return 0, [s]
    cnt = [0]

    def rec(u, vis, depth):
        cnt[0] += 1
        if cnt[0] > budget: raise OverflowError
        cand = [m[0] for m in H.moves[u] if m[0] not in vis]
        if any(H.filled[t] for t in cand): return depth + 1
        if not cand or depth + 1 >= KMAX: return None
        mp = min(H.phi[t] for t in cand); worst = 0
        for t in dict.fromkeys(t for t in cand if H.phi[t] == mp):
            vis.add(t); r = rec(t, vis, depth + 1); vis.discard(t)
            if r is None: return None
            worst = max(worst, r)
        return worst
    try:
        r = rec(s, {s}, 0)
    except OverflowError:
        return -1, [s]   # budget exceeded (reported separately)
    return r, [s]


def adv_key(H, s, key, budget=200000):
    """Greedy rule with lexicographic key, against an ADVERSARIAL choice among the key-minimal candidates (tabu on
    visited states). Returns (worst-case swaps to filled, None if some tie-break sequence fails within KMAX; -1 budget)."""
    if H.filled[s]: return 0, [s]
    cnt = [0]

    def rec(u, vis, depth):
        cnt[0] += 1
        if cnt[0] > budget: raise OverflowError
        ms = [m for m in H.moves[u] if m[0] not in vis]
        if any(H.filled[m[0]] for m in ms): return depth + 1
        if not ms or depth + 1 >= KMAX: return None
        ks = [(key(H, u, m), m[0]) for m in ms]; kmin = min(k for k, _ in ks); worst = 0
        for t in dict.fromkeys(t for k, t in ks if k == kmin):
            vis.add(t); r = rec(t, vis, depth + 1); vis.discard(t)
            if r is None: return None
            worst = max(worst, r)
        return worst
    try:
        return rec(s, {s}, 0), [s]
    except OverflowError:
        return -1, [s]


K_PHI = lambda H, u, m: (H.phi[m[0]],)
K_PI = lambda H, u, m: (H.phi[m[0]], 0 if m[0] == H.pi[u] else 1)
K_PIINV = lambda H, u, m: (H.phi[m[0]], 0 if m[0] == H.pinv[u] else 1)
K_MINW = lambda H, u, m: (H.phi[m[0]], dj(H, u, m[0]))
K_MAXW = lambda H, u, m: (H.phi[m[0]], -dj(H, u, m[0]))
K_ABSW = lambda H, u, m: (H.phi[m[0]], -abs(dj(H, u, m[0])))
K_PIW = lambda H, u, m: (H.phi[m[0]], 0 if m[0] == H.pi[u] else 1, dj(H, u, m[0]))
RULES2 = {
    'PHI>pi': ('greedy', K_PI), 'PHI>piinv': ('greedy', K_PIINV), 'PHI>min-wind': ('greedy', K_MINW),
    'PHI>min-wind#1': ('greedy1', K_MINW), 'PHI>min-wind#2': ('greedy2', K_MINW), 'PHI>max-wind': ('greedy', K_MAXW),
    'PHI>abs-wind': ('greedy', K_ABSW), 'PHI>pi>min-wind': ('greedy', K_PIW),
    'PHI>pi-ADV': ('advk', K_PI), 'PHI>min-wind-ADV': ('advk', K_MINW), 'PHI>max-wind-ADV': ('advk', K_MAXW),
    'PHI>pi>min-wind-ADV': ('advk', K_PIW), 'OPT': ('opt', None),
}


def run_rule2(H, name, s):
    kind, arg = RULES2[name]
    if kind == 'greedy': return walk_greedy(H, s, arg)
    if kind == 'greedy1': return walk_greedy(H, s, arg, seed=1)
    if kind == 'greedy2': return walk_greedy(H, s, arg, seed=2)
    if kind == 'advk': return adv_key(H, s, arg)
    if kind == 'opt':
        d = H.dF[s]; return (d if 0 <= d <= KMAX else None), [s]
