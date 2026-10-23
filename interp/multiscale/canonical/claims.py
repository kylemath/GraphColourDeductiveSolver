# Side claims (a), (b), (c) of the pair-induction reformulation.
import sys, itertools, collections, json, random, math
sys.path.insert(0, '/mnt/project-files/multiscale/canonical/')
from pi import *

def walkpair(cols, s, odd):
    H = walk(None, np.array(s), np.array(cols))
    if H is None: return None
    if odd: return pair(H, odd)
    L = len(H)-1; t = H[-1]-H[0]; r = mec(H[:-1] - np.arange(L)/L*t); return (abs(t) <= 2+1e-9 and r <= 1+1e-9, r, abs(t))

out = {}
# (a) edge star of two adjacent odd vertices u, v (degrees du, dv): boundary x, u_1..u_{du-3}, y, v_1..v_{dv-3}
res_a = {}
for du, dv in [(5, 5), (5, 7), (7, 7), (5, 9)]:
    nb = ['x'] + ['u%d' % i for i in range(du-3)] + ['y'] + ['v%d' % i for i in range(dv-3)]
    k = [2] + [1]*(du-3) + [2] + [1]*(dv-3)
    fl = [(-1 if kk % 2 else 1) for kk in k]; s = [1]
    for i in range(1, len(nb)): s.append(s[-1]*fl[i])
    odd = (s[-1]*fl[0] != s[0]); assert not odd
    adjU = set(['x', 'y'] + [b for b in nb if b.startswith('u')]); adjV = set(['x', 'y'] + [b for b in nb if b.startswith('v')])
    cnt = collections.Counter(); best = {}
    cu, cv = 0, 1
    for cols in itertools.product(range(4), repeat=len(nb)):
        if any(cols[i] == cols[(i+1) % len(nb)] for i in range(len(nb))): continue
        if any(cols[i] == cu for i, b in enumerate(nb) if b in adjU): continue
        if any(cols[i] == cv for i, b in enumerate(nb) if b in adjV): continue
        r = walkpair(list(cols), s, False)
        if r is None: continue
        ok, tau, at = r
        key = (round(at, 3), None if tau is None else round(tau, 4)); cnt[key] += 1
    res_a['%d,%d' % (du, dv)] = sorted([[list(k_), v_] for k_, v_ in cnt.items()], key=lambda z: (z[0][0], z[0][1] or 9))
    print('(a)', du, dv, res_a['%d,%d' % (du, dv)][:8], flush=True)
out['a'] = res_a

# (b) c* rows on the straight degree-6 cylinder (constant sign), and c*-coloured lattice parallelogram discs
def cstar(x, y):
    return [(0, 1), (2, 3), (1, 0), (3, 2)][y % 4][x % 2]
res_b = []
for L in [8, 16, 32, 64, 128]:
    for y in range(4):
        row = [cstar(x, y) for x in range(L)]
        r = walkpair(row, [1]*L, False); res_b.append(dict(kind='cyl_rim', L=L, y=y, t=round(r[2], 3), tauH=None if r[1] is None else round(r[1], 4)))
# lattice parallelogram m x w (triangular lattice, edges (1,0),(0,1),(1,1)), boundary walk, no interior odd vertices
for m in [4, 8, 16, 32]:
    for w in [2, 3]:
        bd = [(x, 0) for x in range(m)] + [(m, y) for y in range(w)] + [(x, w) for x in range(m, 0, -1)] + [(0, y) for y in range(w, 0, -1)]
        def deg_in(p):
            x, y = p; nbrs = [(x+1, y), (x-1, y), (x, y+1), (x, y-1), (x+1, y+1), (x-1, y-1)]
            return sum(1 for (a, b) in nbrs if 0 <= a <= m and 0 <= b <= w)
        k = [deg_in(p) - 2 for p in bd]; fl = [(-1 if kk % 2 else 1) for kk in k]; s = [1]
        for i in range(1, len(bd)): s.append(s[-1]*fl[i])
        cols = [cstar(x, y) for (x, y) in bd]
        r = walkpair(cols, s, False)
        res_b.append(dict(kind='parallelogram', m=m, w=w, L=len(bd), t=None if r is None else round(r[2], 3), tauH=None if r is None or r[1] is None else round(r[1], 4)))
for r in res_b: print('(b)', r)
out['b'] = res_b
json.dump(out, open('/mnt/project-files/multiscale/canonical/claims.json', 'w'))
