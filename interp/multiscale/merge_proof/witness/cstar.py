# c* test (outside reviewer): 4-row periodic colouring on the triangular lattice; comb disc A with m slanted width-2
# teeth and m-1 chords (2k,0)-(2k,-1); flat level B above the seam.  Usage: python cstar.py m depth
import sys, json, itertools
sys.path.insert(0, '/mnt/project-files/multiscale/merge_proof/witness')
from w2 import *
m, Dp = int(sys.argv[1]), int(sys.argv[2])
W, Hh = 3*m+2*Dp+8, Dp+10; x0 = Dp+3; y0 = Dp+3   # patch [0,W) x [0,Hh); lattice (x,y) -> (x+x0, y+y0)
ids = {}; adj = []
def vid(x, y):
    if (x, y) not in ids: ids[(x, y)] = len(adj); adj.append(set())
    return ids[(x, y)]
for x in range(W):
    for y in range(Hh): vid(x, y)
for x in range(W):
    for y in range(Hh):
        for dx, dy in ((1, 0), (0, 1), (1, 1)):
            if (x+dx, y+dy) in ids: a, b = ids[(x, y)], ids[(x+dx, y+dy)]; adj[a].add(b); adj[b].add(a)
apex = vid('apex', 0)
for (x, y), v in list(ids.items()):
    if v != apex and (x in (0, W-1) or y in (0, Hh-1)): adj[apex].add(v); adj[v].add(apex)
g = G([list(a) for a in adj])
L = lambda x, y: ids[(x+x0, y+y0)]
# c*: colours 0, a=1, b=2, c=3
def cstar(x, y):
    r = y % 4; e = x % 2
    return [(0, 1), (2, 3), (1, 0), (3, 2)][r][e]
# comb: teeth k=0..m-1, columns x in {2k,2k+1,2k+2} shifted by (y//2)?  slanted along (1,2): x - y/2 constant.
# rows 0..-Dp; tooth k at row y holds x with 2k <= x + y/2 <= 2k+2 ... use integer slant: x_shift(y) = -(-y)//2 ... simpler: rows y and y-1 share shift
A = set()
for y in range(0, -Dp-1, -1):
    s = (-y)//2            # shift left by 1 every 2 rows
    for k in range(m):
        for dx in (0, 1, 2):
            A.add(L(2*k+dx-s, y))
# slits: remove the shared wall column below row -1 between teeth: tooth k right wall = 2k+2-s = tooth k+1 left wall 2(k+1)-s. Make teeth width 2 with a removed wall below row -1:
A = set()
for y in range(0, -Dp-1, -1):
    s = (-y)//2
    for k in range(m):
        for dx in (0, 1, 2):
            x = 3*k+dx-s if y <= -2 else None
    # rebuild: top two rows are the solid strip x in [0, 3m-? ]
A = set()
for k in range(m):
    for y in range(0, -Dp-1, -1):
        s = (-y)//2
        for dx in (0, 1, 2):
            A.add(L(3*k+dx-s, y))
# rows 0 and -1: fill the gaps so the top is one solid seam of length 3m
for k in range(m-1):
    for y in (0, -1):
        A.add(L(3*k+3-(-y)//2, y)); A.add(L(3*k+2-(-y)//2, y))
print('A', len(A), check(g, A)[0])
DA = Disc(g, A); print('chords', len(DA.chords), 'pockets', len(DA.pockets))
col = {v: cstar(x-x0, y-y0) for (x, y), v in ids.items() if v != apex}
col[apex] = 0
proper = all(col[u] != col[w] for u in A for w in g.adj[u] if w in A)
print('proper on A', proper)
seam = [L(x, 0) for x in range(0, 3*m-1)]
taus = sorted(round(tau_walk(Wk, col), 3) for Wk in DA.pockets); tstar = sorted(round(tau_star(Wk, col), 3) for Wk in DA.pockets)
print('pocket tau (wk base point)', taus[:3], '...', taus[-3:]); print('pocket tau*', tstar[:3], '...', tstar[-3:]); print('pocket tau_strip', sorted(round(tau_strip(Wk, col), 3) for Wk in DA.pockets)[-3:])
print('strict tau*(dA)', round(tau_star(DA.whole, col), 3), 'tvec', tvec(DA.whole, col))
# unions of adjacent pockets
sys.path.insert(0, '/mnt/project-files/multiscale/merge_proof/witness'); from w2check import pocket_tris
P, padj = pocket_tris(DA); ut = []
for a in padj:
    for b in padj[a]:
        if a < b: ut.append(round(tau_star(DA.walk_of(P[a] | P[b]), col), 3))
print('adjacent-union tau*', sorted(ut)[:3], '...', sorted(ut)[-3:])
# merge with a flat level B = rectangle rows 1..4 above the seam
B = set(L(x, y) for x in range(-1, 3*m) for y in range(1, 5))
print('B', len(B), check(g, B)[0], 'U', check(g, A | B)[0])
cB = level_cols(g, B, 1, None, seed0=0, budget=3*10**7)
D = Disc(g, A | B); print('U chords', len(D.chords), 'pockets', len(D.pockets))
cA = {v: col[v] for v in A}
rec = remeasure(g, D, A, B, cA, cB[0], Rmax=5, wmax=6, nb=6)
print({k: rec.get(k) for k in ('R', 'nR', 'nconf', 'w', 'w_star', 'ptau_before', 'strict_tau_before', 'tau_star_before', 'seam_pockets', 'sec_star')})
