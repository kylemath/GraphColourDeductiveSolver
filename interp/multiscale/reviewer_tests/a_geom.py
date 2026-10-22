# Task A geometry: on ico20 take a rhombus of 4 vortices (two adjacent icosahedron faces o1 o2 o3 / o2 o3 o4),
# pair A = {o1, o3}, B = {o2, o4} (opposite sides), U = ball(mA, r) + ball(mB, r), A/B = Voronoi split of U.
import sys
sys.path.insert(0, '/mnt/project-files/multiscale/merge_proof/witness'); sys.path.insert(0, '/mnt/project-files/multiscale/merge_proof')
from w2 import *
def build(name='ico17', d=1, which=0, pairs=((0, 1), (5, 9))):
    g = G(make(name)); n = g.n; deg5 = [v for v in range(n) if g.deg[v] % 2 == 1]
    o1 = deg5[0]; dd = {o: bfs(g.adj, o, 100) for o in deg5}
    sp = min(dd[o1][o] for o in deg5 if o != o1)
    nb = lambda o: [p for p in deg5 if p != o and dd[o][p] == sp]
    rh = []
    for o2 in nb(o1):
        for o3 in nb(o1):
            if o3 <= o2 or o3 not in nb(o2): continue
            for o4 in nb(o2):
                if o4 != o1 and o4 in nb(o3): rh.append((o1, o2, o3, o4))
    if pairs is None: o1, o2, o3, o4 = rh[which]
    else: (o1, o3), (o2, o4) = pairs
    def mid(a, b):
        path = [b]
        while path[-1] != a: path.append(min((w for w in g.adj[path[-1]]), key=lambda w: dd[a][w]))
        return path[len(path)//2]
    mA, mB = mid(o1, o3), mid(o2, o4)
    dA, dB = bfs(g.adj, mA, 100), bfs(g.adj, mB, 100)
    r = sp//2 + d
    U = set(v for v in range(n) if dA[v] <= r or dB[v] <= r)
    A = set(v for v in U if dA[v] < dB[v] or (dA[v] == dB[v] and v % 2 == 0)); B = U - A
    return g, dict(vort=(o1, o2, o3, o4), A=A, B=B, U=U, r=r, sp=sp)
if __name__ == '__main__':
    for d in range(1, 7):
        g, c = build(d=d); A, B, U = c['A'], c['B'], c['U']
        st = [check(g, X)[0] for X in (A, B, U)]
        D = Disc(g, U); dBU = multi_bfs(g.adj, list(D.bset), D.S)
        deg5 = set(v for v in U if g.deg[v] % 2)
        DA = Disc(g, A) if st[0] != 'nodisc' else None
        dA_ = multi_bfs(g.adj, list(DA.bset), DA.S) if DA else {}
        print(d, c['r'], len(A), len(B), len(U), st, 'vort in U', len(deg5), 'depth U', sorted(dBU[o] for o in deg5),
              'depth in A', sorted(dA_[o] for o in deg5 if o in A), 'mU', len(D.whole['walk']), 'mA', len(DA.whole['walk']) if DA else None)
