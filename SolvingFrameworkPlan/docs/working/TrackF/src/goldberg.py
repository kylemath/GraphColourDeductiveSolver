#!/usr/bin/env python3
"""Track F [exploratory]: icosahedral fullerene duals.
 gc_k0(k): Goldberg-Coxeter (k,0) of the icosahedron (geodesic subdivision), dual of C_{20k^2};
 leapfrog(rot): sqrt(3)-subdivision of a triangulation (dual of the leapfrog fullerene; multiplies T by 3).
 GC(1,1) = leapfrog(icosahedron) = C60 dual; GC(3,0) = leapfrog(C60 dual) = C180; GC(2,2) = leapfrog(GC(2,0)) = C240.
Output: 'name n rot' lines (rotation systems from networkx planarity)."""
import sys
import networkx as nx
sys.path.insert(0, 'src')

ICO_F = [(0,1,2),(0,2,3),(0,3,4),(0,4,5),(0,5,1),(1,6,2),(2,7,3),(3,8,4),(4,9,5),(5,10,1),
         (6,7,2),(7,8,3),(8,9,4),(9,10,5),(10,6,1),(11,7,6),(11,8,7),(11,9,8),(11,10,9),(11,6,10)]

def embed(edges):
    G = nx.Graph(); G.add_edges_from(edges); n = G.number_of_nodes()
    assert sorted(G.nodes()) == list(range(n))
    ok, emb = nx.check_planarity(G); assert ok
    assert G.number_of_edges() == 3 * n - 6
    return [list(emb.neighbors_cw_order(v)) for v in range(n)]

def gc_k0(k):
    ids = {}
    def vid(key):
        if key not in ids: ids[key] = len(ids)
        return ids[key]
    def point(a, b, c, i, j):   # barycentric (i, j, k-i-j) on corners (a, b, c) -> canonical key
        w = {a: i, b: j, c: k - i - j}
        nz = tuple(sorted((x, y) for x, y in w.items() if y > 0))
        return nz
    E = set()
    for (a, b, c) in ICO_F:
        P = {}
        for i in range(k + 1):
            for j in range(k + 1 - i):
                P[(i, j)] = vid(point(a, b, c, i, j))
        for i in range(k + 1):
            for j in range(k + 1 - i):
                u = P[(i, j)]
                for di, dj in ((1, 0), (0, 1), (-1, 1)):
                    q = (i + di, j + dj)
                    if q in P: E.add(tuple(sorted((u, P[q]))))
    return embed(E)

def leapfrog(rot):
    n = len(rot); faces = set()
    for u in range(n):
        d = len(rot[u])
        for t in range(d):
            v, w = rot[u][t], rot[u][(t + 1) % d]
            f = (u, v, w); m = f.index(min(f)); faces.add(f[m:] + f[:m])
    fid = {f: n + i for i, f in enumerate(sorted(faces))}
    E = set()
    for f, x in fid.items():
        for u in f: E.add(tuple(sorted((u, x))))
    # each old edge uv is replaced by the edge between its two face-vertices
    ef = {}
    for f, x in fid.items():
        for i in range(3):
            u, v = f[i], f[(i + 1) % 3]; ef.setdefault(tuple(sorted((u, v))), []).append(x)
    for e, xs in ef.items():
        assert len(xs) == 2; E.add(tuple(sorted(xs)))
    return embed(E)

def line(name, rot): return f"{name} {len(rot)} " + ";".join(",".join(map(str, r)) for r in rot)

if __name__ == '__main__':
    ico = gc_k0(1)
    out = {'GC10_C20': ico, 'GC20_C80': gc_k0(2), 'GC30_C180': gc_k0(3), 'GC40_C320': gc_k0(4),
           'GC11_C60': leapfrog(ico)}
    out['GC22_C240'] = leapfrog(out['GC20_C80'])
    out['GC33_C540'] = leapfrog(out['GC30_C180'])
    for name, rot in out.items():
        deg = [len(r) for r in rot]
        assert deg.count(5) == 12 and all(d in (5, 6) for d in deg), name
        print(line(name, rot))
