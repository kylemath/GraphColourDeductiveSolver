#!/usr/bin/env python3
"""Track T library: the matching form of near-rigid runs (TrackS S1-S4) on an abstract graph, plus the chord
diagram / interlace graph of a Hamiltonian state.

Abstract setting (no embedding needed except the cyclic labelling f0..f4 of the edges at v):
  G: vertex 0 = v (degree 5), all other vertices cubic; multi-edges allowed, no loops.
  A state is a pair (P, M) of disjoint perfect matchings (P = M_{t-1}, M = M_t).  k = index of M's v-edge.
  Q = E - M.  DL-type: Q connected, v-loops of Q pair (f_{k-1} f_{k+1}) (loop X) and (f_{k+2} f_{k-2}) (loop Y),
  and P contains f_{k+2}  (then P is one of the two perfect matchings of the figure-eight Q).
  step: (P, M) -> (M, P ^ Y).     (TrackS Lemma S3: M_{t+1} = M_{t-1} xor Y_t.)
  H = P | M, k(H) = number of components.  Rigid-like ("Hamiltonian") state: k(H) = 1 and also Q_{t-1} = E - P
  connected of DL type (F12 condition), which is automatic along a run.

Edge sets are Python ints (bitmasks over edge ids)."""
import sys, os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))


class G5:
    def __init__(self, n, edges, fv):
        """n vertices (0 = v), edges list of (a, b), fv = edge ids of v in rotation order f0..f4"""
        self.n = n; self.E = list(edges); self.m = len(edges); self.fv = list(fv)
        self.inc = [[] for _ in range(n)]
        for k, (a, b) in enumerate(self.E):
            self.inc[a].append(k); self.inc[b].append(k)
        assert len(self.inc[0]) == 5 and sorted(self.inc[0]) == sorted(fv)
        assert all(len(self.inc[x]) == 3 for x in range(1, n)), [len(i) for i in self.inc]
        self.fidx = {e: t for t, e in enumerate(fv)}
        self.ALL = (1 << self.m) - 1

    def other(self, k, x):
        a, b = self.E[k]
        return b if a == x else a

    def edges_of(self, S):
        k = 0
        while S:
            if S & 1: yield k
            S >>= 1; k += 1

    def vedge(self, M):
        for t, e in enumerate(self.fv):
            if M >> e & 1: return t
        return None

    def ncomp(self, S):
        par = list(range(self.n)); seen = set()
        def f(x):
            while par[x] != x:
                par[x] = par[par[x]]; x = par[x]
            return x
        for k in self.edges_of(S):
            a, b = self.E[k]; seen.add(a); seen.add(b)
            ra, rb = f(a), f(b)
            if ra != rb: par[ra] = rb
        return len({f(x) for x in seen})

    def loop(self, S, e0):
        """follow S (degree 2 at every non-v vertex it meets) from v along v-edge e0 back to v;
        returns (edge mask, closing v-edge)"""
        mask = 1 << e0; x = self.other(e0, 0); k = e0
        while x != 0:
            nx = [t for t in self.inc[x] if (S >> t & 1) and t != k]
            if len(nx) != 1: return None, None
            k = nx[0]; mask |= 1 << k; x = self.other(k, x)
        return mask, k

    def is_pm(self, M):
        cnt = [0] * self.n
        for k in self.edges_of(M):
            a, b = self.E[k]; cnt[a] += 1; cnt[b] += 1
        return all(c == 1 for c in cnt)

    def dl_info(self, P, M):
        """returns (k, X, Y) if (P, M) is a DL-type state with Q = E - M connected, else None"""
        k = self.vedge(M)
        if k is None: return None
        Q = self.ALL & ~M
        f = self.fv
        X, cl = self.loop(Q, f[(k - 1) % 5])
        if X is None or cl != f[(k + 1) % 5]: return None
        Y, cl = self.loop(Q, f[(k + 2) % 5])
        if Y is None or cl != f[(k - 2) % 5]: return None
        if (X | Y) != Q: return None          # Q connected (figure-eight)
        if not (P >> f[(k + 2) % 5] & 1): return None
        if P & M: return None
        return k, X, Y

    def step(self, P, M):
        d = self.dl_info(P, M)
        if d is None: return None
        return (M, P ^ d[2])

    def kH(self, P, M):
        return self.ncomp(P | M)


def run_from(g, P, M, maxlen=400):
    """iterate the step from (P, M) while the state is DL-type (Q connected).  Returns (states, closed)."""
    st = [(P, M)]; seen = {(P, M): 0}
    while len(st) <= maxlen:
        nx = g.step(*st[-1])
        if nx is None: return st, False
        if nx in seen:
            return st, (seen[nx] == 0) and True or ('rho', seen[nx])
        seen[nx] = len(st); st.append(nx)
    return st, 'long'


def run_back(g, P, M, maxlen=400):
    """backward iteration: predecessor of (P, M) is (P', P) with P' = M ^ Y(P) where Y(P) is the Y-loop of
    E - P at the state (?, P) -- by S3, M_{t-2} = M_t ^ Y_{t-1}."""
    st = [(P, M)]
    while len(st) <= maxlen:
        P, M = st[-1]
        # state (P2, P) must be DL-type with Y-loop Y; P2 = M ^ Y
        k = g.vedge(P)
        if k is None: return st
        Q = g.ALL & ~P; f = g.fv
        Y, cl = g.loop(Q, f[(k + 2) % 5])
        if Y is None or cl != f[(k - 2) % 5]: return st
        P2 = M ^ Y
        if g.step(P2, P) != (P, M): return st
        st.append((P2, P))
    return st


# ---------------- construction of the Tait dual from a triangulated surface ----------------

def triangles(rot):
    F = set()
    for u, r in enumerate(rot):
        for i in range(len(r)):
            F.add(frozenset((u, r[i], r[(i + 1) % len(r)])))
    return sorted(F, key=sorted)


def tait_dual(rot, h):
    """G5 of the triangulation rot with hole h: vertices = triangles not at h, plus v = 0; edges = primal edges
    not at h (dual); f_t = dual of link edge x_t x_{t+1}, x = rot[h].  Also returns the primal edge of each id."""
    F = triangles(rot)
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
    x = rot[h]
    edges = []; prim = []; fv = [None] * 5
    lab = {frozenset((x[t], x[(t + 1) % 5])): t for t in range(5)}
    for (u, w), fl in sorted(ef.items()):
        if h in (u, w): continue
        assert len(fl) == 2
        k = len(edges); edges.append((vid(fl[0]), vid(fl[1]))); prim.append((u, w))
        t = lab.get(frozenset((u, w)))
        if t is not None: fv[t] = k
    g = G5(1 + len(ren), edges, fv)
    g.prim = prim; g.pid = {p: k for k, p in enumerate(prim)}
    return g


def load_graphs(path, names=None):
    out = {}
    for l in open(path):
        p = l.split()
        if len(p) < 3: continue
        if names is not None and p[0] not in names: continue
        out[p[0]] = [list(map(int, r.split(','))) for r in p[2].split(';')]
    return out


# ---------------- Hamiltonian cycles through v (rigid candidates) ----------------

def ham_states(g, limit=10 ** 7):
    """all (P, M) with H = P|M a Hamiltonian cycle through v using f_k (in M) and f_{k+2} (in P), such that
    both (P, M) and the reversed-role F12 condition hold: Q = E - M and E - P connected DL-type is checked by
    the caller.  Simple DFS with degree pruning; fine up to ~40 vertices of a cubic graph."""
    n = g.n; out = []
    for k in range(5):
        a_e = g.fv[k]; b_e = g.fv[(k + 2) % 5]
        a = g.other(a_e, 0); b = g.other(b_e, 0)
        if a == b: continue
        # path from a to b through all vertices 1..n-1, edges not at v; degree pruning:
        # avail[z] = # neighbours (not v) of unvisited z that are unvisited or the current path end
        used = [False] * n; used[0] = True; used[a] = True
        nb = [[g.other(e, x) for e in g.inc[x] if g.other(e, x) != 0] for x in range(n)]
        avail = [sum(1 for w in nb[z] if w != 0) for z in range(n)]
        path_e = [a_e]
        def dfs(x, cnt):
            if x == b:
                if cnt == n - 1:
                    yield list(path_e)
                return
            for e in g.inc[x]:
                y = g.other(e, x)
                if used[y] or y == 0: continue
                # x becomes interior: unvisited neighbours of x other than y lose one
                bad = False; dec = []
                for z in nb[x]:
                    if not used[z] and z != y:
                        avail[z] -= 1; dec.append(z)
                        if avail[z] < (1 if z == b else 2): bad = True
                if not bad:
                    used[y] = True; path_e.append(e)
                    yield from dfs(y, cnt + 1)
                    path_e.pop(); used[y] = False
                for z in dec: avail[z] += 1
        for pe in dfs(a, 1):
            pe = pe + [b_e]
            # alternate colours: pe[0] = f_k in M, then P, M, ...
            M = 0; P = 0
            for i, e in enumerate(pe):
                if i % 2 == 0: M |= 1 << e
                else: P |= 1 << e
            # pe has n edges (Hamiltonian cycle), n even so last edge (f_{k+2}) has index n-1 odd -> P. good
            out.append((P, M))
            if len(out) > limit: return out
    return out


# ---------------- chord diagram & interlace ----------------

def chord_diagram(g, P, M):
    """H = P|M Hamiltonian. Returns (order, chords): order = list of circle positions (vertex or v-blowup
    tokens), chords = list of (pos1, pos2, edge id).  v is blown up into 3 points between its H-neighbours:
    [nbr via f_k] f_{k-1} f_{k+1} f_{k-2} [nbr via f_{k+2}] (f_{k+1} is the lone side; its position among the
    three only affects interlacing with chords of the other side)."""
    k = g.vedge(M); f = g.fv
    H = P | M
    # walk H from v along f_{k+2} ... back via f_k
    seq = []; x = g.other(f[(k + 2) % 5], 0); e = f[(k + 2) % 5]
    while x != 0:
        seq.append(x)
        nx = [t for t in g.inc[x] if (H >> t & 1) and t != e]
        e = nx[0]; x = g.other(e, x)
    assert len(seq) == g.n - 1
    # circle: seq (from f_{k+2}-nbr to f_k-nbr), then v-blowup from the f_k side to the f_{k+2} side
    order = list(seq) + [('v', (k - 1) % 5), ('v', (k + 1) % 5), ('v', (k - 2) % 5)]
    pos = {}
    for i, t in enumerate(order): pos[t] = i
    chords = []
    C = g.ALL & ~H
    for e in g.edges_of(C):
        a, b = g.E[e]
        pa = pos[('v', g.fidx[e])] if a == 0 else pos[a]
        pb = pos[('v', g.fidx[e])] if b == 0 else pos[b]
        chords.append((min(pa, pb), max(pa, pb), e))
    return order, chords


def interlace(chords):
    m = len(chords); A = [0] * m
    for i in range(m):
        a1, b1, _ = chords[i]
        for j in range(i + 1, m):
            a2, b2, _ = chords[j]
            if (a1 < a2 < b1) != (a1 < b2 < b1):
                A[i] |= 1 << j; A[j] |= 1 << i
    return A


def bipartition(A):
    """2-colouring of the graph with adjacency bitmasks A, or None"""
    m = len(A); col = [-1] * m
    for s in range(m):
        if col[s] >= 0: continue
        col[s] = 0; st = [s]
        while st:
            x = st.pop(); y = A[x]; j = 0
            while y:
                if y & 1:
                    if col[j] < 0: col[j] = 1 - col[x]; st.append(j)
                    elif col[j] == col[x]: return None
                y >>= 1; j += 1
    return col


def gf2_rank(rows):
    rows = [r for r in rows if r]; rank = 0
    piv = {}
    for r in rows:
        while r:
            hb = r.bit_length() - 1
            if hb in piv: r ^= piv[hb]
            else:
                piv[hb] = r; rank += 1; break
    return rank
