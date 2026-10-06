#!/usr/bin/env python3
"""studiointel core_check.py -- INDEPENDENT (imports no producer code). Is GRAPH.json a spherical triangulation of the core class
(min degree >= 5, no separating triangle)? Prints the degree counts and the link degrees of HOLE in rotation order."""
import sys, json, itertools
from collections import Counter
F = [tuple(f) for f in json.load(open(sys.argv[1]))['faces']]; hole = int(sys.argv[2])
de = Counter((f[i], f[(i + 1) % 3]) for f in F for i in range(3))
ok = all(v == 1 for v in de.values()) and all((b, a) in de for (a, b) in de)
V = {x for f in F for x in f}; E = len(de) // 2
adj = {v: set() for v in V}
for a, b in de: adj[a].add(b)
fs = {frozenset(f) for f in F}
sep = [t for t in itertools.combinations(sorted(V), 3) if t[1] in adj[t[0]] and t[2] in adj[t[0]] and t[2] in adj[t[1]] and frozenset(t) not in fs]
nxt = {f[(f.index(hole) + 1) % 3]: f[(f.index(hole) + 2) % 3] for f in F if hole in f}
x = min(nxt); L = [x]
while len(L) < len(nxt): L.append(nxt[L[-1]])
core = ok and len(V) - E + len(F) == 2 and min(len(a) for a in adj.values()) >= 5 and not sep
print('triangulation', ok, 'V-E+F', len(V) - E + len(F), 'degrees', dict(sorted(Counter(len(adj[v]) for v in V).items())), 'separating triangles', len(sep),
      'hole', hole, 'deg', len(adj[hole]), 'link degrees in rotation', [len(adj[u]) for u in L], 'CORE' if core else 'NOT CORE')
