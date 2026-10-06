"""nprove_regions.py: region decomposition of H = T - x - V_D' (D' = colour of the apex in c' / c'').
H-triangles = faces of T with no vertex in V_D' u {x}; regions = edge-adjacency components of H-triangles;
loose vertices = H-vertices in no H-triangle.  The decomposition depends only on (T, V_D'), not on the 3-colouring,
so it is constant on the D'-free Kempe class.  Also checks Proposition R (every swap acts on each region as a
global transposition) by brute force on the class."""
import sys
from itertools import combinations
from nprove_lib import *
fn = sys.argv[1]
def regions(adj, x, Dset):
    n = len(adj); rem = set(Dset) | {x}
    tris = [t for t in combinations(range(n), 3) if t[1] in adj[t[0]] and t[2] in adj[t[0]] and t[2] in adj[t[1]]]
    # faces = all 3-cliques when no separating triangle (checked by certify); else cliques are a superset
    H = [t for t in tris if not (set(t) & rem)]
    par = list(range(len(H)))
    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    edge = {}
    for i, t in enumerate(H):
        for e in combinations(t, 2):
            if e in edge: par[f(i)] = f(edge[e])
            else: edge[e] = i
    reg = {}
    for i, t in enumerate(H): reg.setdefault(f(i), set()).update(t)
    covered = set().union(*reg.values()) if reg else set()
    loose = [v for v in range(n) if v not in rem and v not in covered]
    return list(reg.values()), loose
for i, line in enumerate(l for l in open(fn) if 'DISC' in l):
    col, E = parse(line); x, adj = build(col, E)
    assert certify(adj)['sep_triangles'] == 0
    cp, cpp, K2, K0 = neighbours_cprime(adj, x, col + [0])
    for name, c0, apex in (("c'", cp, 0), ("c''", cpp, 2)):
        Dset = [v for v in range(x) if c0[v] == c0[apex]]
        R, loose = regions(adj, x, Dset)
        dist, rep, g = dfree_class(adj, x, c0, apex)
        # Prop R check: for every member and every swap, each region is acted on by identity or one global transposition
        ok = True
        for k, c in rep.items():
            for a, b in [(p, q) for p in range(4) for q in range(p + 1, 4) if c0[apex] not in (p, q)]:
                cs, ix = comps(adj, c, (a, b), x)
                for K in cs:
                    c2 = swap(c, K, a, b)
                    Ks = set(K)
                    for r in R:
                        ab = [v for v in r if c[v] in (a, b)]
                        inK = {v in Ks for v in ab}
                        if len(inK) == 2: ok = False   # region only partially in K
        print(i, name, "class", len(dist), "regions", len(R), "sizes", sorted(len(r) for r in R), "loose", len(loose), "|D'|", len(Dset), "PropR ok", ok)
