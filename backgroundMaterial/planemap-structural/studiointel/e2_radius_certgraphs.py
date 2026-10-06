#!/usr/bin/env python3
"""studiointel e2_radius_certgraphs.py -- [computed, exploratory, post hoc] radius of every E2 record in the four Phase C radius-5 graphs,
with deg(w0,w1,w3) and the lock status after AB. Frame as in intern-A-cycle2."""
import sys, json, itertools
from collections import Counter, defaultdict, deque
sys.path.insert(0, '.')
import radius, graphs
from ring_patterns import third
res = Counter()
for t in ('91a307d1852a1764', '8a23ee3ec7b2bb33', '62661a3f304f4caa', '80b930d1540e4ee3'):
    faces = [tuple(f) for f in json.load(open('run-C-2026-10-06/cert/%s.graph.json' % t))['faces']]
    deg = graphs.degrees(faces); adjT = graphs.adjacency(faces)
    fbe = defaultdict(list)
    for f in faces:
        for e in itertools.combinations(f, 2): fbe[frozenset(e)].append([z for z in f if z not in e][0])
    for hole in sorted(v for v in deg if deg[v] == 5):
        order, idx, nb, link = radius.prepare(faces, hole); L = [order[i] for i in link]
        states = radius.enumerate_states(nb, 10 ** 6); cls = {s: radius.classify(nb, link, s) for s in states}
        dist = {s: 0 for s in states if cls[s] != 2}; q = deque(dist)
        nbr = {}
        while q:
            s = q.popleft()
            for u in radius.swaps(nb, s):
                if u not in dist: dist[u] = dist[s] + 1; q.append(u)
        for s in states:
            if cls[s] != 2: continue
            col = {order[i]: s[i] for i in range(len(s))}
            lc = [col[x] for x in L]; j = [j for j in range(5) if lc[j] == lc[(j + 2) % 5]][0]
            for sense in (1, -1):
                X = [L[(j + k) % 5] for k in range(5)] if sense > 0 else [L[(j + 2 - k) % 5] for k in range(5)]
                if not (deg[X[3]] == 6 and deg[X[4]] == 6 and all(deg[X[k]] == 5 for k in (0, 1, 2))): continue
                A, B, G, D = col[X[0]], col[X[1]], col[X[3]], col[X[4]]; let = {A: 'a', B: 'b', G: 'g', D: 'd'}
                W = [third(fbe, X[k], X[(k + 1) % 5], hole) for k in range(5)]
                if ''.join(let[col[w]] for w in W) != 'dgdag': continue
                m = {k: [u for u in adjT[X[k]] if u not in {hole, X[(k - 1) % 5], X[(k + 1) % 5], W[(k - 1) % 5], W[k]}][0] for k in (3, 4)}
                if not (let[col[m[3]]] == 'b' and let[col[m[4]]] == 'b'): continue
                res[(t[:8], hole, (deg[W[0]], deg[W[1]], deg[W[3]]), 'radius', 1 + dist[s] if s in dist else None)] += 1
for k, v in sorted(res.items()): print(v, k)
