#!/usr/bin/env python3
"""pd2_lib.py -- [exploratory] helpers for the P-D afternoon pass (Variant X, potentials). stdlib only.
Builds on pd_lib (dual H, Tait colours) and astruct_core (locks, F) unchanged. Hole is renamed 'v'."""
import sys, itertools
from collections import deque
from pd_lib import *
sys.path.insert(0, '..')
import lattack_witness as W


class G:
    """graph with a degree-5 hole: adj (hole 'v'), link L, dual H, incidence, vertex order."""
    def __init__(self, name, faces, hole):
        self.name = name
        self.adj, self.fs, self.L = make_graph(faces, hole)
        self.H = dual(self.adj, self.fs)
        self.V = sorted((u for u in self.adj if u != 'v'), key=str)
        self.inc = {}
        for e, (p, q) in self.H.items():
            self.inc.setdefault(p, []).append((e, q)); self.inc.setdefault(q, []).append((e, p))
        self.pe = [frozenset((self.L[t], self.L[(t + 1) % 5])) for t in range(5)]
        self.pidx = {e: t for t, e in enumerate(self.pe)}

    # ---- colourings (canonical under colour renaming: first occurrence along self.V)
    def all_states(self):
        order = []; seen = set()
        for s in self.V:
            if s in seen: continue
            q = [s]; seen.add(s)
            while q:
                u = q.pop(0); order.append(u)
                for w in sorted(self.adj[u], key=str):
                    if w != 'v' and w not in seen: seen.add(w); q.append(w)
        res = []; col = {}
        def rec(i):
            if i == len(order): res.append(self.canon(col)); return
            u = order[i]; used = {col[w] for w in self.adj[u] if w in col}
            for c in range(4):
                if c not in used: col[u] = c; rec(i + 1); del col[u]
        col[order[0]] = 0; rec(1)
        return list({self.key(c): c for c in res}.values())

    def canon(self, col):
        mp = {}; out = {}
        for u in self.V:
            c = col[u]
            if c not in mp: mp[c] = len(mp)
            out[u] = mp[c]
        return out

    def key(self, col): return tuple(col[u] for u in self.V)

    def filled(self, col): return len({col[x] for x in self.L}) <= 3

    def swaps(self, col):
        """all whole-component Kempe swaps in G-v: yields (p,q,K,newcol)"""
        for p, q in itertools.combinations(range(4), 2):
            seen = set()
            for u in self.V:
                if u in seen or col[u] not in (p, q): continue
                K = comp(self.adj, col, u, {p, q}); seen |= K
                new = {w: ((q if c == p else p) if w in K else c) for w, c in col.items()}
                yield p, q, K, new

    # ---- Tait objects
    def tc(self, col, e):
        a, b = tuple(e); return col[a] ^ col[b]

    def ppath(self, col, t0, pair):
        """H-edges (G-edge keys) of the pair-bichromatic path leaving P by e_{t0}; returns (edges list, end index)"""
        e0 = self.pe[t0]; cur = e0; node = [q for (e, q) in self.inc['P'] if e == e0][0]; path = [e0]
        while node != 'P':
            nxt = [e for (e, q) in self.inc[node] if e != cur and self.tc(col, e) in pair]
            assert len(nxt) == 1
            cur = nxt[0]; path.append(cur); node = [q for (e, q) in self.inc[node] if e == cur][0]
        return path, self.pidx[cur]

    def side(self, start, cut):
        """vertices of G-v reachable from start without using a G-edge whose dual is in cut"""
        S = {start}; st = [start]
        while st:
            u = st.pop()
            for w in self.adj[u]:
                if w != 'v' and w not in S and frozenset((u, w)) not in cut: S.add(w); st.append(w)
        return S

    def roles(self, col):
        j = repeat_index(col, self.L)
        if j is None: return None
        e = [col[self.L[t]] ^ col[self.L[(t + 1) % 5]] for t in range(5)]
        return j, e[j], e[(j + 2) % 5], e[(j + 4) % 5]   # j, beta, gamma, delta

    def lockdata(self, col):
        """Z1 = (beta,gamma) path from e_{j+2}; Z2 = (beta,delta) path from e_{j+4}. returns dict"""
        j, be, ga, de = self.roles(col)
        Z1, end1 = self.ppath(col, (j + 2) % 5, {be, ga})
        Z2, end2 = self.ppath(col, (j + 4) % 5, {be, de})
        return dict(j=j, be=be, ga=ga, de=de, Z1=Z1, Z2=Z2, lock1=(end1 == (j + 1) % 5), lock2=(end2 == j))


def ncomp_edges(edges, H):
    nb = {}
    for e in edges:
        p, q = H[e]; nb.setdefault(p, set()).add(q); nb.setdefault(q, set()).add(p)
    seen = set(); k = 0
    for n in nb:
        if n in seen: continue
        k += 1; st = [n]; seen.add(n)
        while st:
            u = st.pop()
            for w in nb[u]:
                if w not in seen: seen.add(w); st.append(w)
    return k


def graphs(which=('T4', 'A_3', 'A_4')):
    """yield G objects: T4 all degree-5 holes; A_3 all degree-5 holes; A_4 all degree-5 holes."""
    if 'T4' in which:
        adj = {}
        for f in T4_FACES:
            for a in f: adj.setdefault(a, set()).update(x for x in f if x != a)
        for h in sorted(adj):
            if len(adj[h]) == 5: yield G('T4@%d' % h, T4_FACES, h)
    if 'A_3' in which:
        adj = {}
        for f in W.A3_FACES:
            for a in f: adj.setdefault(a, set()).update(x for x in f if x != a)
        for h in sorted(adj):
            if len(adj[h]) == 5: yield G('A_3@%d' % h, W.A3_FACES, h)
    if 'A_4' in which:
        a = build_A(4); fa = faces_from_adj(a)
        for h in sorted(a, key=str):
            if len(a[h]) == 5: yield G('A_4@%s' % (h,), fa, h)


def dist_to_fill(g, states):
    """multi-source BFS over the (symmetric) Kempe-swap graph of canonical states. returns dict key->dist"""
    byk = {g.key(c): c for c in states}
    dist = {k: 0 for k, c in byk.items() if g.filled(c)}
    dq = deque(dist)
    nbrs = {}
    for k, c in byk.items():
        nbrs[k] = [g.key(g.canon(n)) for (_, _, _, n) in g.swaps(c)]
    while dq:
        k = dq.popleft()
        for k2 in nbrs[k]:
            if k2 not in dist: dist[k2] = dist[k] + 1; dq.append(k2)
    return dist, byk, nbrs
