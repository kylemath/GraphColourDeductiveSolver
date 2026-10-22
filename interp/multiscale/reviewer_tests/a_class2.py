# how f = sum(s) mod 3 of dA, dU changes when single outer vertices are added to A (U = A+B)
import sys
sys.path.insert(0, '/mnt/project-files/multiscale/reviewer_tests')
from a_geom import *
def fclass(W): return sum(W['s']) % 3
g, c = build(d=1); A, B, U = c['A'], c['B'], c['U']
print('base', fclass(Disc(g, A).whole), fclass(Disc(g, B).whole), fclass(Disc(g, U).whole))
outer = [x for x in range(g.n) if x not in U and len(g.adj[x] & A) >= 2 and not (g.adj[x] & B)]
seen = 0
for x in outer[:12]:
    A2 = A | {x}; U2 = U | {x}
    if check(g, A2)[0] != 'ok' or check(g, U2)[0] != 'ok': continue
    print(x, len(g.adj[x] & A), 'f A,B,U', fclass(Disc(g, A2).whole), fclass(Disc(g, B).whole), fclass(Disc(g, U2).whole))
