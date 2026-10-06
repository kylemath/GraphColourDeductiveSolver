#!/usr/bin/env python3
"""Pentakis dodecahedron: dodecahedron (20 vertices) plus a centre vertex on each of its 12 faces.
Check: sphere triangulation, minimum degree 5, every degree-5 vertex has all five neighbours of degree 6
(no 5-5 edge). Audit code, [hand + computed]."""
import itertools, math
phi = (1 + 5 ** 0.5) / 2
# dodecahedron coordinates
P = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
for a, b in ((0, 1 / phi), ):
    pass
P += [(0, s / phi, t * phi) for s in (-1, 1) for t in (-1, 1)]
P += [(s / phi, t * phi, 0) for s in (-1, 1) for t in (-1, 1)]
P += [(s * phi, 0, t / phi) for s in (-1, 1) for t in (-1, 1)]
d = lambda a, b: math.dist(a, b)
el = min(d(a, b) for a, b in itertools.combinations(P, 2))
E = {frozenset((i, j)) for i, j in itertools.combinations(range(20), 2) if abs(d(P[i], P[j]) - el) < 1e-9}
assert len(E) == 30
adj = {i: {j for j in range(20) if frozenset((i, j)) in E} for i in range(20)}
# pentagonal faces = 5-cycles of the dodecahedral graph (girth 5, so 5-cycles are faces: 12 of them)
faces = set()
for a in range(20):
    for b in adj[a]:
        for c in adj[b] - {a}:
            for dd in adj[c] - {a, b}:
                for e in adj[dd] - {a, b, c}:
                    if a in adj[e]: faces.add(frozenset((a, b, c, dd, e)))
assert len(faces) == 12, len(faces)
A = {i: set(adj[i]) for i in range(20)}
for k, f in enumerate(faces):
    c = 20 + k; A[c] = set(f)
    for v in f: A[v].add(c)
n = len(A); m = sum(len(s) for s in A.values()) // 2
deg = {v: len(A[v]) for v in A}
print('order', n, 'edges', m, '3n-6', 3 * n - 6, 'degrees', sorted(set(deg.values())),
      'count deg5', sum(1 for v in A if deg[v] == 5),
      '5-5 edges', sum(1 for v in A for w in A[v] if v < w and deg[v] == deg[w] == 5),
      'deg5 link classes', {tuple(sorted(deg[w] for w in A[v])) for v in A if deg[v] == 5})
