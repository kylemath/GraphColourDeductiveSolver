#!/usr/bin/env python3
"""[exploratory] Control: same engine on the icosahedron (sphere, all degree 5) and the sphere graphs from the order-12..16 plantri-free cases."""
import sys; sys.path.insert(0, '../common')
from kempe_py import Space
from fractions import Fraction
import itertools
# icosahedron: top 0, upper ring 1-5, lower ring 6-10, bottom 11
adj = {i: set() for i in range(12)}
def e(a, b): adj[a].add(b); adj[b].add(a)
for i in range(5):
    e(0, 1 + i); e(1 + i, 1 + (i + 1) % 5); e(11, 6 + i); e(6 + i, 6 + (i + 1) % 5)
    e(1 + i, 6 + i); e(1 + i, 6 + (i + 4) % 5)
assert all(len(a) == 5 for a in adj.values())
link = [1, 2, 3, 4, 5]
sp = Space(adj, 0, link); sp.build_graph(); cl, n = sp.classes()
for c in range(n):
    ks = [k for k in range(len(sp.states)) if cl[k] == c]; f = sum(sp.filled(k) for k in ks)
    print('icosahedron class', c, 'size', len(ks), 'filled', f, Fraction(f, len(ks)))
