#!/usr/bin/env python3
"""studiointel corridor.py -- [exploratory] Math 16:15 item (b): at every hole with rho >= 4, do the lock paths of the hardest states run
through a vertex of a Birkhoff diamond or 2.122 occurrence? For each state s: lock components K1 ({mu,A} of m, contains a) and K2
({mu,B} of m, contains b) in T - v. Three measures per lock: (i) the component meets a configuration vertex, (ii) a shortest m-a (m-b)
path does, (iii) EVERY such path does (removing configuration vertices disconnects). Hardest states (max radius) versus a control of
radius-2 DL states at the same hole. Also the fraction of graph vertices that lie in some configuration occurrence."""
import sys, json, random
from collections import deque, Counter
sys.path.insert(0, '.')
import radius, graphs
import causal_test as CT
from r55566_test import graphs_from

def occ_vertices(F, P_):
    adj = graphs.adjacency(F); tf = {frozenset(f) for f in F}; degT = {u: len(a) for u, a in adj.items()}
    order = P_['order']; found = set(); phi = {}; used = set()
    def rec(i):
        if i == len(order):
            if all(frozenset(phi[x] for x in f) in tf for f in P_['faces']): found.update(phi.values())
            return
        u = order[i]; placed = order[:i]; nbr = [w for w in placed if w in P_['E'][u]]
        for t in (adj[phi[nbr[0]]] if nbr else adj.keys()):
            if t in used or degT[t] != P_['deg'][u]: continue
            if any((w in P_['E'][u]) != (phi[w] in adj[t]) for w in placed): continue
            phi[u] = t; used.add(t); rec(i + 1); del phi[u]; used.discard(t)
    rec(0); return found

def bfs_path(nb, ok, s, t):
    prev = {s: None}; q = deque([s])
    while q:
        u = q.popleft()
        if u == t:
            p = []
            while u is not None: p.append(u); u = prev[u]
            return p
        for w in nb[u]:
            if w not in prev and ok(w): prev[w] = u; q.append(w)
    return None

def measures(nb, link, col, cfg):
    lc = [col[x] for x in link]; j = [j for j in range(5) if lc[j] == lc[(j + 2) % 5]][0]
    m, a, b = link[(j + 1) % 5], link[(j + 3) % 5], link[(j + 4) % 5]; out = []
    for t in (a, b):
        cols = (col[m], col[t]); ok = lambda w: col[w] in cols
        comp_ = set(); st = [m]; comp_.add(m)
        while st:
            u = st.pop()
            for w in nb[u]:
                if w not in comp_ and ok(w): comp_.add(w); st.append(w)
        p = bfs_path(nb, ok, m, t)
        forced = bfs_path(nb, lambda w: ok(w) and (w not in cfg or w == t), m, t) is None if m not in cfg else True
        out.append((bool(comp_ & cfg), bool(set(p) & cfg), forced))
    return out

if __name__ == '__main__':
    tally = {'hard': Counter(), 'control': Counter()}; holes = 0; frac = []
    for arg in sys.argv[1:]:
        for name, F in graphs_from(arg):
            deg = graphs.degrees(F); cand = [v for v in deg if deg[v] == 5]
            cfgV = None
            for v in cand:
                order, idx, nb, link = radius.prepare(F, v)
                states = radius.enumerate_states(nb, 10 ** 7); cls = {s: radius.classify(nb, link, s) for s in states}
                if not any(c == 2 for c in cls.values()): continue
                dist = {s: 0 for s in states if cls[s] != 2}; q = deque(dist)
                while q:
                    s = q.popleft()
                    for t in radius.swaps(nb, s):
                        if t not in dist: dist[t] = dist[s] + 1; q.append(t)
                rmax = max(1 + dist[s] for s in states if cls[s] == 2)
                if rmax < 4: continue
                if cfgV is None:
                    cfgV = occ_vertices(F, CT.P[0]) | occ_vertices(F, CT.P[1]); frac.append(len(cfgV) / len(deg))
                cfg = {idx[u] for u in cfgV if u in idx}
                holes += 1
                hard = [s for s in states if cls[s] == 2 and 1 + dist[s] == rmax]
                ctrl = [s for s in states if cls[s] == 2 and 1 + dist[s] == 2]
                random.Random(v).shuffle(ctrl); ctrl = ctrl[:len(hard)]
                for lab, S in (('hard', hard), ('control', ctrl)):
                    for s in S:
                        for k, (c, p, f) in enumerate(measures(nb, link, s, cfg)):
                            tally[lab]['lock%d n' % (k + 1)] += 1; tally[lab]['lock%d component meets' % (k + 1)] += c
                            tally[lab]['lock%d shortest path meets' % (k + 1)] += p; tally[lab]['lock%d every path meets' % (k + 1)] += f
    print('holes with rho>=4:', holes, ' mean fraction of vertices in a configuration:', round(sum(frac) / max(1, len(frac)), 3))
    for lab in ('hard', 'control'): print(lab, dict(sorted(tally[lab].items())))
