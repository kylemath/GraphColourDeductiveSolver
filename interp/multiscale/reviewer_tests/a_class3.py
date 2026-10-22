import sys, itertools
sys.path.insert(0, '/mnt/project-files/multiscale/reviewer_tests')
from a_geom import *
def fclass(W): return sum(W['s']) % 3
for name in sys.argv[1].split(','):
    g = G(make(name)); n = g.n; deg5 = [v for v in range(n) if g.deg[v] % 2 == 1]
    dd = {o: bfs(g.adj, o, 100) for o in deg5}; sp = min(dd[deg5[0]][o] for o in deg5 if o != deg5[0])
    def mid(a, b):
        path = [b]
        while path[-1] != a: path.append(min((w for w in g.adj[path[-1]]), key=lambda w: dd[a][w]))
        return path[len(path)//2]
    edges = [(a, b) for a, b in itertools.combinations(deg5, 2) if dd[a][b] == sp]
    pa = edges[0]; mA = mid(*pa); dmA = bfs(g.adj, mA, 100)
    for pb in edges:
        if set(pb) & set(pa): continue
        mB = mid(*pb)
        if dmA[mB] > sp+3: continue
        dB = bfs(g.adj, mB, 100); r = sp//2 + 1
        U = set(v for v in range(n) if dmA[v] <= r or dB[v] <= r)
        A = set(v for v in U if dmA[v] < dB[v] or (dmA[v] == dB[v] and v % 2 == 0)); B = U - A
        st = [check(g, X)[0] for X in (A, B, U)]
        if 'nodisc' in st: print(name, pa, pb, 'nodisc'); continue
        print(name, sp, pa, pb, 'f A,B,U', fclass(Disc(g, A).whole), fclass(Disc(g, B).whole), fclass(Disc(g, U).whole), 'vortU', sum(1 for v in U if g.deg[v] % 2), flush=True)
