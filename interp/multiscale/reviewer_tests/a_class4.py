# Z3 class f = sum(s) mod 3 (up to sign) of dA, dB, dU for 4-vortex configurations with all vortices interior.
import sys, itertools
sys.path.insert(0, '/mnt/project-files/multiscale/reviewer_tests')
from a_geom import *
def fc(W): f = sum(W['s']) % 3; return min(f, (3-f) % 3)   # class up to sign: 0 or 1
name = sys.argv[1]; g = G(make(name)); n = g.n; deg5 = [v for v in range(n) if g.deg[v] % 2 == 1]
dd = {o: bfs(g.adj, o, 200) for o in deg5}; sp = min(dd[deg5[0]][o] for o in deg5 if o != deg5[0])
def mid(a, b):
    path = [b]
    while path[-1] != a: path.append(min((w for w in g.adj[path[-1]]), key=lambda w: dd[a][w]))
    return path[len(path)//2]
edges = [(a, b) for a, b in itertools.combinations(deg5, 2) if dd[a][b] <= sp+1]
pa = edges[0]; mA = mid(*pa); dmA = bfs(g.adj, mA, 200)
for pb in edges:
    if set(pb) & set(pa): continue
    mB = mid(*pb); dB = bfs(g.adj, mB, 200)
    if dmA[mB] > 2*sp: continue
    for r in range(sp//2+2, sp//2+6):
        U = set(v for v in range(n) if dmA[v] <= r or dB[v] <= r)
        A = set(v for v in U if dmA[v] < dB[v] or (dmA[v] == dB[v] and v % 2 == 0)); B = U - A
        if 'nodisc' in [check(g, X)[0] for X in (A, B, U)]: print(pa, pb, r, 'nodisc'); continue
        D = Disc(g, U); dBU = multi_bfs(g.adj, list(D.bset), D.S)
        inner = sorted(dBU[v] for v in U if g.deg[v] % 2)
        print(name, pa, pb, 'dmid', dmA[mB], 'r', r, 'depths', inner, 'f A,B,U', fc(Disc(g, A).whole), fc(Disc(g, B).whole), fc(D.whole), flush=True)
