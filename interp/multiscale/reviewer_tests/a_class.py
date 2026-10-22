# Z3 class f(t) = sum of boundary signs (mod 3) of dA, dB, dU for the pairings of a rhombus of vortices on ico20.
import sys
sys.path.insert(0, '/mnt/project-files/multiscale/reviewer_tests')
from a_geom import *
def fclass(W): return sum(W['s']) % 3
g = G(make('ico20')); n = g.n; deg5 = [v for v in range(n) if g.deg[v] % 2 == 1]
dd = {o: bfs(g.adj, o, 100) for o in deg5}
def mid(a, b):
    path = [b]
    while path[-1] != a: path.append(min((w for w in g.adj[path[-1]]), key=lambda w: dd[a][w]))
    return path[len(path)//2]
def pair_region(pa, pb, d, sp=20):
    mA, mB = mid(*pa), mid(*pb); dA, dB = bfs(g.adj, mA, 100), bfs(g.adj, mB, 100); r = sp//2 + d
    U = set(v for v in range(n) if dA[v] <= r or dB[v] <= r)
    A = set(v for v in U if dA[v] < dB[v] or (dA[v] == dB[v] and v % 2 == 0)); return A, U - A, U
o1 = deg5[0]; nb = lambda o: [p for p in deg5 if p != o and dd[o][p] == 20]
import itertools
for o2, o3 in itertools.combinations(nb(o1), 2):
    if o3 not in nb(o2): continue
    o4 = [p for p in nb(o2) if p in nb(o3) and p != o1][0]
    for pa, pb in [((o1, o3), (o2, o4)), ((o1, o2), (o3, o4)), ((o2, o3), (o1, o4))]:
        A, B, U = pair_region(pa, pb, 1)
        st = [check(g, X)[0] for X in (A, B, U)]
        if 'nodisc' in st: print(pa, pb, st); continue
        vU = sum(1 for v in U if g.deg[v] % 2)
        print(pa, pb, st, 'vortU', vU, 'f A,B,U', fclass(Disc(g, A).whole), fclass(Disc(g, B).whole), fclass(Disc(g, U).whole))
    break
print('--- all pairs of disjoint icosahedron edges containing o1-edge, midpoint distance <= 26')
edges = [(a, b) for a, b in itertools.combinations(deg5, 2) if dd[a][b] == 20]
pa = edges[0]; mA = mid(*pa); dmA = bfs(g.adj, mA, 100); res = []
for pb in edges:
    if set(pb) & set(pa): continue
    mB = mid(*pb)
    if dmA[mB] > 26: continue
    A, B, U = pair_region(pa, pb, 1)
    if 'nodisc' in [check(g, X)[0] for X in (A, B, U)] or sum(1 for v in U if g.deg[v] % 2) != 4: print(pa, pb, dmA[mB], 'bad'); continue
    print(pa, pb, dmA[mB], 'f A,B,U', fclass(Disc(g, A).whole), fclass(Disc(g, B).whole), fclass(Disc(g, U).whole), flush=True)
