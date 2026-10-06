#!/usr/bin/env python3
"""P-F adversary data: degree of 4-colourings of min-degree-5 sphere triangulations, as simplicial
maps T -> boundary of the tetrahedron (deg = p - n over a target face; Mohar-Salas 2009 definition),
and whether degree (mod k) is constant on Kempe classes of the full triangulation T. Audit code. [exploratory]
usage: pf_degree.py PLANTRI_FILE [max_graphs]"""
import sys, json
from itertools import permutations
from collections import defaultdict
sys.path.insert(0, '../wp20-replay')
from wp20_audit import Graph, enum_colourings, swaps, canon, masks_from

def faces(rot):
    F = set()
    for v, r in enumerate(rot):
        for i in range(len(r)):
            t = (v, r[i], r[(i + 1) % len(r)])
            k = min((t, t[1:] + t[:1], t[2:] + t[:2]))
            F.add(k)
    assert len(F) == 2 * len(rot) - 4
    return sorted(F)

def sign(a, b, c):   # orientation of (a,b,c) relative to cyclic (0,1,2) for target face colours
    return 1 if (a, b, c) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)) else -1

def degree(F, col, target=(0, 1, 2)):
    m = {t: i for i, t in enumerate(target)}; d = 0
    for (a, b, c) in F:
        cs = (col[a], col[b], col[c])
        if sorted(cs) == sorted(target): d += sign(m[cs[0]], m[cs[1]], m[cs[2]])
    return d

out = []
lines = [l for l in open(sys.argv[1]) if l.strip()][: int(sys.argv[2]) if len(sys.argv) > 2 else None]
for gi, line in enumerate(lines):
    rot = [[ord(c) - 97 for c in p] for p in line.split()[1].split(',')]
    G = Graph(rot); n = G.n; order = list(range(n)); F = faces(rot)
    states = enum_colourings(G, order); idx = {s: i for i, s in enumerate(states)}
    degs = []
    for s in states:
        ds = {degree(F, s, t) for t in ((0,1,2),(0,1,3),(0,2,3),(1,2,3))}
        # |deg| is target-independent; sign depends on target orientation convention: use (0,1,2) value
        degs.append(degree(F, s))
    par = list(range(len(states)))
    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for i, s in enumerate(states):
        for m in swaps(G.nb, masks_from(s, order), (1 << n) - 1):
            a, b = f(i), f(idx[canon(m, order)])
            if a != b: par[a] = b
    cls = defaultdict(list)
    for i in range(len(states)): cls[f(i)].append(abs(degs[i]))
    res = dict(graph=gi, order=n, colourings=len(states), kempe_classes=len(cls),
               abs_degree_values=sorted({abs(d) for d in degs}),
               classes=[sorted(set(v)) for v in cls.values()])
    for k in (2, 3, 4, 6, 12):
        res[f'abs_deg_mod{k}_const_on_classes'] = all(len({x % k for x in v}) == 1 for v in cls.values())
    out.append(res); print(json.dumps(res), flush=True)
