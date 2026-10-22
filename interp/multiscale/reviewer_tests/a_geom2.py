# Task A geometry, version 2 (f_U != 0): ico17, pairs PA=(0,1), PB=(6,8) (opposite-ish icosahedron edges, midpoints 26 apart),
# U = ball(mA, r) + ball(mB, r) + corridor (radius cw around a geodesic mA-mB); A/B = Voronoi split (seam across the corridor).
import sys, itertools
sys.path.insert(0, '/mnt/project-files/multiscale/merge_proof/witness'); sys.path.insert(0, '/mnt/project-files/multiscale/merge_proof')
from w2 import *
def build(d=1, name='ico17', pairs=((0, 1), (6, 8)), cw=3, tie=0):
    g = G(make(name)); n = g.n; deg5 = [v for v in range(n) if g.deg[v] % 2 == 1]
    dd = {o: bfs(g.adj, o, 200) for o in deg5}
    def mid(a, b):
        path = [b]
        while path[-1] != a: path.append(min((w for w in g.adj[path[-1]]), key=lambda w: dd[a][w]))
        return path, path[len(path)//2]
    (pa, mA), (pb, mB) = mid(*pairs[0]), mid(*pairs[1])
    dA, dB = bfs(g.adj, mA, 200), bfs(g.adj, mB, 200)
    path = [mB]
    while path[-1] != mA: path.append(min(g.adj[path[-1]], key=lambda w: dA[w]))
    dP = multi_bfs(g.adj, path, set(range(n)))
    sp = len(pa)-1; r = (sp+1)//2 + d
    U = set(v for v in range(n) if dA[v] <= r or dB[v] <= r or dP[v] <= cw)
    A = set(v for v in U if dA[v] < dB[v] or (dA[v] == dB[v] and v % 2 == tie)); B = U - A
    for _ in range(20):   # remove chords of A / B by moving a chord endpoint's ear across the seam
        ch = [(X, Y) for X, Y in ((A, B), (B, A)) if check(g, X)[0] == 'chord']
        if not ch: break
        X, Y = ch[0]; DX = Disc(g, X); moved = False
        for (u, w) in DX.chords:
            for z in (u, w, *(g.adj[u] & g.adj[w])):      # move a seam vertex of the pinch across
                if z in X and g.adj[z] & Y and check(g, X - {z})[0] != 'nodisc' and check(g, Y | {z})[0] != 'nodisc':
                    X.discard(z); Y.add(z); moved = True; break
            if moved: break
        if not moved: break
    return g, dict(vort=tuple(pairs[0]) + tuple(pairs[1]), A=A, B=B, U=U, r=r, sp=sp)
if __name__ == '__main__':
    fc = lambda W: min(sum(W['s']) % 3, (3 - sum(W['s']) % 3) % 3)
    for d in range(0, 6):
        g, c = build(d=d, cw=int(sys.argv[1]) if len(sys.argv) > 1 else 3); A, B, U = c['A'], c['B'], c['U']
        st = [check(g, X)[0] for X in (A, B, U)]
        if 'nodisc' in st: print(d, st); continue
        D = Disc(g, U); dBU = multi_bfs(g.adj, list(D.bset), D.S); vort = [v for v in U if g.deg[v] % 2]
        print(d, c['r'], len(A), len(B), len(U), st, 'vort', len(vort), 'depths', sorted(dBU[o] for o in vort), 'f A,B,U', fc(Disc(g, A).whole), fc(Disc(g, B).whole), fc(D.whole), 'mU', len(D.whole['walk']), flush=True)
