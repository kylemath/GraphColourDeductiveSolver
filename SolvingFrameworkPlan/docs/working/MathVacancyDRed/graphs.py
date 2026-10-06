"""Explicit triangulations (face lists) and extraction of an r-ball configuration.

[computed, exploratory] Math worker, 2026-10-06.
"""
from collections import defaultdict


def T4():
    F = [(0,1,2),(0,1,5),(0,2,3),(0,3,4),(0,4,5),(1,2,6),(1,5,10),(1,6,10),(2,3,7),(2,6,11),
         (2,7,11),(3,4,8),(3,7,8),(4,5,9),(4,8,9),(5,9,10),(6,10,15),(6,11,15),(7,8,12),(7,11,12),
         (8,9,13),(8,12,13),(9,10,14),(9,13,14),(10,14,15),(11,12,16),(11,15,16),(12,13,16),
         (13,14,16),(14,15,16)]
    return [tuple(f) for f in F]


def A(r):
    """Stack of r-1 pentagonal antiprisms capped by two poles: 5r+2 vertices.
    A(2) = icosahedron. Pole N = 0, ring i (1..r) vertex t = 1+5(i-1)+t, pole S = 5r+1."""
    N, S = 0, 5 * r + 1
    R = lambda i, t: 1 + 5 * (i - 1) + (t % 5)
    F = []
    for t in range(5):
        F.append((N, R(1, t), R(1, t + 1)))
        F.append((S, R(r, t), R(r, t + 1)))
        for i in range(1, r):
            F.append((R(i, t), R(i, t + 1), R(i + 1, t)))
            F.append((R(i + 1, t), R(i + 1, t + 1), R(i, t + 1)))
    return F


def pentakis():
    """Pentakis dodecahedron (32 vertices): icosahedron vertices 0..11 (degree 5),
    icosahedron faces -> new vertices 12..31 (degree 6)."""
    ico = A(2)
    fid = {frozenset(f): 12 + k for k, f in enumerate(ico)}
    edge_faces = defaultdict(list)
    for f in ico:
        for a, b in ((f[0], f[1]), (f[1], f[2]), (f[0], f[2])):
            edge_faces[frozenset((a, b))].append(fid[frozenset(f)])
    F = []
    for e, (f, g) in edge_faces.items():
        a, b = tuple(e)
        F.append((a, f, g))
        F.append((b, f, g))
    return F


def adjacency(F):
    adj = defaultdict(set)
    for f in F:
        for a in f:
            for b in f:
                if a != b:
                    adj[a].add(b)
    return {k: frozenset(v) for k, v in adj.items()}


def check_triangulation(F):
    n = len({x for f in F for x in f})
    assert len(F) == 2 * n - 4, (len(F), n)
    cnt = defaultdict(int)
    for f in F:
        assert len(set(f)) == 3
        for a, b in ((f[0], f[1]), (f[1], f[2]), (f[0], f[2])):
            cnt[frozenset((a, b))] += 1
    assert all(c == 2 for c in cnt.values())
    assert len(set(frozenset(f) for f in F)) == len(F)
    return n


def ball_config(F, v, r=2):
    """K = closed r-ball around v, as a disc: inside faces = faces with all vertices at
    distance <= r and at least one at distance < r. Returns dict with
      link   : cyclic order of N(v)
      ring   : cyclic order of the boundary cycle R (vertices at distance r)
      verts  : vertices of K - v
      edges  : edges of the disc not incident to v (inside edges of K - v)
    Raises if the boundary is not a simple cycle."""
    adj = adjacency(F)
    dist = {v: 0}
    frontier = [v]
    while frontier:
        nf = []
        for x in frontier:
            for y in adj[x]:
                if y not in dist:
                    dist[y] = dist[x] + 1
                    nf.append(y)
        frontier = nf
    inside = [f for f in F if all(dist[x] <= r for x in f) and min(dist[x] for x in f) < r]
    ecount = defaultdict(int)
    for f in inside:
        for a, b in ((f[0], f[1]), (f[1], f[2]), (f[0], f[2])):
            ecount[frozenset((a, b))] += 1
    bnd = [tuple(e) for e, c in ecount.items() if c == 1]
    badj = defaultdict(list)
    for a, b in bnd:
        badj[a].append(b)
        badj[b].append(a)
    assert all(len(x) == 2 for x in badj.values()), "boundary not a simple cycle"
    start = min(badj)
    ring = [start]
    prev, cur = None, start
    while True:
        nxt = [y for y in badj[cur] if y != prev][0] if prev is not None else badj[cur][0]
        if nxt == start:
            break
        ring.append(nxt)
        prev, cur = cur, nxt
    assert len(ring) == len(badj)
    assert all(dist[x] == r for x in ring), "ring vertex not at distance r"
    # link in cyclic order
    lk = sorted(adj[v])
    link = [lk[0]]
    while len(link) < len(lk):
        cand = [y for y in adj[link[-1]] if y in adj[v] and y not in link]
        link.append(min(cand))
    verts = sorted({x for f in inside for x in f} - {v})
    edges = sorted(tuple(sorted(e)) for e in ecount if v not in e)
    return dict(link=link, ring=ring, verts=verts, edges=edges, v=v, r=r)
