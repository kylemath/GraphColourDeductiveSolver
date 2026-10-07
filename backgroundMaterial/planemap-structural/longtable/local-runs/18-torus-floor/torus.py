#!/usr/bin/env python3
"""[exploratory] Torus triangulation generator: lattice T(r,s) + random edge flips, with full validation."""
import random, itertools
from collections import defaultdict

def lattice(r, s):
    vid = lambda i, j: (i % r) * s + (j % s)
    F = set()
    for i in range(r):
        for j in range(s):
            F.add(frozenset((vid(i,j), vid(i+1,j), vid(i+1,j+1))))
            F.add(frozenset((vid(i,j), vid(i+1,j+1), vid(i,j+1))))
    return r * s, F

def edges_of(F):
    E = defaultdict(list)
    for f in F:
        for a, b in itertools.combinations(sorted(f), 2): E[(a, b)].append(f)
    return E

def adjacency(F, n):
    adj = {v: set() for v in range(n)}
    for f in F:
        for a, b in itertools.combinations(f, 2): adj[a].add(b); adj[b].add(a)
    return adj

def link_cycle(F, v):
    """cyclic order of neighbours of v from the faces at v; None if the link is not a single cycle."""
    nb = defaultdict(list)
    for f in F:
        if v in f:
            a, b = sorted(f - {v}); nb[a].append(b); nb[b].append(a)
    if not nb or any(len(x) != 2 for x in nb.values()): return None
    start = min(nb); cyc = [start]; prev = None; cur = start
    while True:
        nxt = [x for x in nb[cur] if x != prev]
        nx = nxt[0] if prev is not None else nb[cur][0]
        if nx == start: break
        cyc.append(nx); prev, cur = cur, nx
        if len(cyc) > len(nb): return None
    return cyc if len(cyc) == len(nb) else None

def validate(n, F, mindeg=5):
    """Euler V-E+F=0, every edge in 2 faces, links single cycles, simple, min degree, no non-facial triangle."""
    E = edges_of(F)
    if n - len(E) + len(F) != 0: return "euler"
    if any(len(x) != 2 for x in E.values()): return "edge-face"
    if any(len(f) != 3 for f in F): return "degenerate face"
    for v in range(n):
        if link_cycle(F, v) is None: return "link"
    adj = adjacency(F, n)
    if min(len(a) for a in adj.values()) < mindeg: return "mindeg"
    # no triangle that is not a face (separating contractible or non-contractible 3-cycle)
    for a in range(n):
        for b in adj[a]:
            if b > a:
                for c in adj[a] & adj[b]:
                    if c > b and frozenset((a, b, c)) not in F: return "nonfacial triangle"
    return None

def flip(n, F, edge, mindeg=5):
    """flip an edge if the result keeps simplicity and min degree; return the new face set or None"""
    a, b = edge
    fs = [f for f in F if a in f and b in f]
    if len(fs) != 2: return None
    x = next(iter(fs[0] - {a, b})); y = next(iter(fs[1] - {a, b}))
    if x == y: return None
    adj = adjacency(F, n)
    if y in adj[x]: return None
    if len(adj[a]) - 1 < mindeg or len(adj[b]) - 1 < mindeg: return None
    G = (F - set(fs)) | {frozenset((x, y, a)), frozenset((x, y, b))}
    return G

def random_walk(n, F, steps, rng, bias5=0.0, mindeg=5):
    """random flips keeping validity; bias5 in [0,1): probability to prefer flips raising the number of degree-5 vertices"""
    for _ in range(steps):
        E = list(edges_of(F))
        for _ in range(50):
            e = rng.choice(E)
            G = flip(n, F, e, mindeg)
            if G is None or validate(n, G, mindeg): continue
            if bias5 and rng.random() < bias5:
                d0 = sum(1 for v in adjacency(F, n).values() if len(v) == 5)
                d1 = sum(1 for v in adjacency(G, n).values() if len(v) == 5)
                if d1 < d0: continue
            F = G; break
    return F

def invariant(n, F):
    """isomorphism-ish invariant (WL refinement hash, 3 rounds)"""
    adj = adjacency(F, n); col = {v: len(adj[v]) for v in adj}
    for _ in range(4):
        col = {v: hash((col[v], tuple(sorted(col[w] for w in adj[v])))) for v in adj}
    return hash(tuple(sorted(col.values())))
