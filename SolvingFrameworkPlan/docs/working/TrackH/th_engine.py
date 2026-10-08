#!/usr/bin/env python3
"""Track H engine (independent pure-Python code; reads graphs in the TrackF 'name n rot;rot;...' format).

States: proper 4-colourings of T - h up to colour renaming (normal form = first-occurrence relabelling in a fixed
vertex order).  Moves: swap any Kempe component (any colour pair) of T - h.

Per unfilled state (link (alpha, mu, alpha, A, B) at x_j..x_{j+4}) we record
  L1 = x3 in K_{muA}(x1), L2 = x4 in K_{muB}(x1), inA = x0 in K_{alphaA}(x2), inB = x0 in K_{alphaB}(x2)
  (indices relative to j), D2 ok iff L2 == not inA, D1 ok iff L1 == not inB,
  pi  = swap K_{alphaA}(x2) (defined iff not inA),  sigma = swap K_{alphaMu}(x2) (always defined),
  sizes / odd-G-degree counts of K_{alphaA}(x2), K_{alphaB}(x2), K_{alphaMu}(x2).
Every Kempe move out of a state: (pair, component, link vertices met, target index).
"""
import sys, json
from collections import deque

def read_graphs(path):
    out = {}
    for l in open(path):
        p = l.split()
        if len(p) >= 3:
            out[p[0]] = [list(map(int, r.split(','))) for r in p[2].split(';')]
    return out

PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

class Hole:
    def __init__(self, rot, h):
        self.rot = rot; self.h = h; n = len(rot)
        self.X = list(rot[h]); assert len(self.X) == 5
        self.V = [v for v in range(n) if v != h]
        self.adj = {v: [w for w in rot[v] if w != h] for v in self.V}
        self.odd = {v for v in self.V if len(rot[v]) % 2}
        order = list(self.X); seen = set(order) | {h}
        for u in order:
            for w in self.adj[u]:
                if w not in seen: seen.add(w); order.append(w)
        assert len(order) == n - 1, 'T - h disconnected'
        self.order = order; self.pos = {v: i for i, v in enumerate(order)}
        self._enum()

    def norm(self, col):
        mp = {}
        return tuple(mp.setdefault(col[v], len(mp)) for v in self.order)

    def _enum(self):
        states = []; c = {}; order = self.order; adj = self.adj
        sys.setrecursionlimit(10000)
        def rec(i, used):
            if i == len(order): states.append(tuple(c[v] for v in order)); return
            v = order[i]; forb = {c[w] for w in adj[v] if w in c}
            for a in range(min(used + 1, 4)):
                if a not in forb: c[v] = a; rec(i + 1, max(used, a + 1)); del c[v]
        rec(0, 0)
        self.states = states; self.idx = {s: i for i, s in enumerate(states)}

    def col(self, i):
        st = self.states[i]; return {v: st[self.pos[v]] for v in self.V}

    def comp(self, col, s, pair):
        seen = {s}; st = [s]
        while st:
            u = st.pop()
            for w in self.adj[u]:
                if w not in seen and col[w] in pair: seen.add(w); st.append(w)
        return seen

    def swap(self, col, K, p, q):
        d = dict(col)
        for v in K: d[v] = q if col[v] == p else p
        return self.idx[self.norm(d)]

    def analyse_state(self, i):
        col = self.col(i); X = self.X
        lk = [col[x] for x in X]
        r = dict(i=i, link=lk)
        if len(set(lk)) <= 3:
            r['kind'] = 'F'; return r, col
        j = next(t for t in range(5) if lk[t] == lk[(t + 2) % 5])
        x = [X[(j + t) % 5] for t in range(5)]
        al, mu, A, B = col[x[0]], col[x[1]], col[x[3]], col[x[4]]
        KmA = self.comp(col, x[1], (mu, A)); KmB = self.comp(col, x[1], (mu, B))
        KA = self.comp(col, x[2], (al, A)); KB = self.comp(col, x[2], (al, B)); KM = self.comp(col, x[2], (al, mu))
        L1 = x[3] in KmA; L2 = x[4] in KmB; inA = x[0] in KA; inB = x[0] in KB
        r.update(kind='DL' if (L1 and L2) else ('S' if (L1 or L2) else 'N'), j=j, roles=(al, mu, A, B),
                 L1=L1, L2=L2, inA=inA, inB=inB, D1=(L1 == (not inB)), D2=(L2 == (not inA)),
                 KA=len(KA), KB=len(KB), KM=len(KM), oA=len(KA & self.odd), oB=len(KB & self.odd), oM=len(KM & self.odd),
                 KmA=len(KmA), KmB=len(KmB))
        r['pi'] = None if inA else self.swap(col, KA, al, A)
        r['sigma'] = self.swap(col, KM, al, mu)
        return r, col

    def build(self):
        S = len(self.states); self.info = [None] * S; self.moves = [None] * S
        par = list(range(S))
        def f(a):
            while par[a] != a: par[a] = par[par[a]]; a = par[a]
            return a
        Xs = set(self.X)
        for i in range(S):
            r, col = self.analyse_state(i); self.info[i] = r
            mv = []
            for (p, q) in PAIRS:
                left = {v for v in self.V if col[v] in (p, q)}
                while left:
                    s = next(iter(left)); K = self.comp(col, s, (p, q)); left -= K
                    k = self.swap(col, K, p, q)
                    hit = tuple(sorted(t for t in range(5) if self.X[t] in K))
                    mv.append((p, q, hit, len(K), k, min(K)))
                    a, b = f(i), f(k)
                    if a != b: par[a] = b
            self.moves[i] = mv
        self.cls = [f(i) for i in range(S)]
        return self

    def class_members(self, i):
        r = self.cls[i]; return [k for k in range(len(self.states)) if self.cls[k] == r]

    def allDL_cycles(self):
        info = self.info; on = set(); cycs = []
        for i in range(len(info)):
            if info[i]['kind'] != 'DL' or i in on: continue
            path = []; posd = {}; k = i
            while k is not None and info[k]['kind'] == 'DL' and k not in posd and k not in on:
                posd[k] = len(path); path.append(k); k = info[k]['pi']
            if k is not None and k in posd:
                c = path[posd[k]:]; on.update(c); cycs.append(c)
        return cycs

    def dist_to(self, srcs, pred, members):
        """BFS in the Kempe graph (restricted to members) from each src to the nearest state satisfying pred."""
        res = {}
        for s in srcs:
            dq = deque([s]); d = {s: 0}; prev = {s: None}; hit = None
            while dq:
                u = dq.popleft()
                if pred(u): hit = u; break
                for m in self.moves[u]:
                    v = m[4]
                    if v not in d: d[v] = d[u] + 1; prev[v] = (u, m); dq.append(v)
            path = []
            u = hit
            while u is not None and prev[u] is not None:
                path.append(prev[u]); u = prev[u][0]
            res[s] = (d.get(hit), list(reversed(path)))
        return res

if __name__ == '__main__':
    g = read_graphs(sys.argv[1])[sys.argv[2]]; H = Hole(g, int(sys.argv[3])).build()
    print(len(H.states), [len(c) for c in H.allDL_cycles()])
