#!/usr/bin/env python3
"""[exploratory] Local compute (MacBook): a plain-Python Kempe engine, written fresh, stdlib only, no team code imported.

Definitions (same as the studio-explore READMEs):
- T is a plane triangulation, v a hole (or None). A STATE is a proper 4-colouring of T - v up to renaming of colours:
  the colours are relabelled by first occurrence along a fixed vertex order (BFS of T - v from link[0], neighbours ascending).
- A MOVE is a whole-component Kempe swap: pick two colours {p, q} and one connected component of the {p, q}-subgraph
  of T - v (singletons allowed) and exchange p and q on it. Moves that only rename colours (the component is the whole
  {p, q}-subgraph) give the same state up to renaming; they are kept as edges s -> s (self loops) and ignored for BFS.
- FILLED: the hole's link uses <= 3 colours. dist(s) = fewest moves from s to a filled state (-1 if none).
- A class (connected component of the move graph) is TARGETLESS if it has no filled state. rho = max over states of dist.
"""
import itertools
from collections import deque


def plantri_ascii(line):
    """'n bcd,ace,...' -> rotation lists (0-based)."""
    return [[ord(ch) - 97 for ch in w] for w in line.split()[1].split(",")]


def gentri_rotation(line):
    """gentri line 'G n HEX F faces...' -> rotation lists (0-based). HEX is planar code: 1-based neighbours, 00 ends a vertex."""
    parts = line.split(); n = int(parts[1]); h = parts[2]
    bs = [int(h[i:i + 2], 16) for i in range(0, len(h), 2)]
    rot, cur = [], []
    for b in bs:
        if b == 0: rot.append(cur); cur = []
        else: cur.append(b - 1)
    assert len(rot) == n, (len(rot), n)
    return rot


def adj_from_rot(rot):
    return {v: set(nb) for v, nb in enumerate(rot)}


def link_cycle(rot, hole):
    return list(rot[hole])


class Space:
    """All states of T - hole (hole may be None), with the move graph."""

    def __init__(self, adj, hole=None, link=None, start=None):
        self.adj = adj; self.hole = hole
        self.link = list(link) if link is not None else (sorted(adj[hole]) if hole is not None else [])
        V = [u for u in adj if u != hole]
        A = {u: sorted(w for w in adj[u] if w != hole) for u in V}
        s0 = start if start is not None else (self.link[0] if hole is not None else min(V))
        order, seen = [s0], {s0}
        for x in order:
            for y in A[x]:
                if y not in seen: seen.add(y); order.append(y)
        assert len(order) == len(V), "T - v disconnected"
        self.order = order; self.idx = {u: i for i, u in enumerate(order)}; self.N = N = len(order)
        self.nbm = [0] * N
        for u in V:
            for w in A[u]: self.nbm[self.idx[u]] |= 1 << self.idx[w]
        self.linki = [self.idx[x] for x in self.link]
        self._enumerate()

    def _enumerate(self):
        N, nbm = self.N, self.nbm
        prev = [[j for j in range(i) if nbm[i] >> j & 1] for i in range(N)]
        states = []; col = [0] * N

        def rec(i, used):
            if i == N: states.append(tuple(col)); return
            forb = 0
            for j in prev[i]: forb |= 1 << col[j]
            for c in range(min(used + 1, 4)):
                if not forb >> c & 1: col[i] = c; rec(i + 1, max(used, c + 1))
        rec(1, 1)  # col[0] = 0 (first vertex gets colour 0 by canonical form)
        self.states = states; self.index = {s: k for k, s in enumerate(states)}

    def canon(self, c):
        mp = {}; return tuple(mp.setdefault(x, len(mp)) for x in c)

    def flood(self, start, M):
        comp = front = start; nbm = self.nbm
        while front:
            nb = 0; f = front
            while f:
                low = f & -f; nb |= nbm[low.bit_length() - 1]; f ^= low
            nb &= M & ~comp; comp |= nb; front = nb
        return comp

    def cmasks(self, s):
        cm = [0, 0, 0, 0]
        for i, x in enumerate(s): cm[x] |= 1 << i
        return cm

    def components(self, s, p, q, cm=None):
        cm = cm or self.cmasks(s); M = cm[p] | cm[q]; out = []
        while M:
            K = self.flood(M & -M, cm[p] | cm[q]); M &= ~K; out.append(K)
        return out

    def swap(self, s, K, p, q):
        d = list(s)
        for i in range(self.N):
            if K >> i & 1: d[i] = q if s[i] == p else p
        return self.canon(d)

    def moves(self, k):
        """list of (target index, p, q, component mask), all components of all 6 pairs (including renamings)."""
        s = self.states[k]; cm = self.cmasks(s); out = []
        for p, q in itertools.combinations(range(4), 2):
            for K in self.components(s, p, q, cm):
                out.append((self.index[self.swap(s, K, p, q)], p, q, K))
        return out

    def build_graph(self):
        self.G = [sorted({t for t, *_ in self.moves(k) if t != k}) for k in range(len(self.states))]
        return self.G

    def filled(self, k):
        return len({self.states[k][i] for i in self.linki}) <= 3

    def classes(self):
        G = self.G; cl = [-1] * len(G); n = 0
        for s in range(len(G)):
            if cl[s] >= 0: continue
            cl[s] = n; q = [s]
            for x in q:
                for t in G[x]:
                    if cl[t] < 0: cl[t] = n; q.append(t)
            n += 1
        self.cl = cl; self.ncl = n
        return cl, n

    def dist_to_filled(self):
        G = self.G; dist = [-1] * len(G); q = deque()
        for s in range(len(G)):
            if self.filled(s): dist[s] = 0; q.append(s)
        while q:
            x = q.popleft()
            for t in G[x]:
                if dist[t] < 0: dist[t] = dist[x] + 1; q.append(t)
        self.dist = dist
        return dist

    def state_of(self, colouring):
        """colouring: dict vertex -> colour (any labels) -> state index"""
        return self.index[self.canon([colouring[u] for u in self.order])]

    def mask_vertices(self, K):
        return sorted(self.order[i] for i in range(self.N) if K >> i & 1)
