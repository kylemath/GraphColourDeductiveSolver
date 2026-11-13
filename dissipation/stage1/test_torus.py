# Soundness self-test of the row bounds: random 5/6/7 torus triangulations (flips from a lattice), random integer parameters.
# For every vertex, the TRUE final charge (simulated on the map) must be <= its row bound from net.exact; total charge is 0.
import sys, os, random, itertools
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'w16', 'code'))
import torus as TT
import rows as RW, net as NT

def rand_torus(rng, p, r, flips):
    T = TT.lattice_torus(p, 0, r)
    for _ in range(flips):
        u = rng.randrange(T.n); v = rng.choice(sorted(T.adj[u]))
        a = T.opp[(u, v)]; b = T.opp[(v, u)]
        if T.deg[u] - 1 < 5 or T.deg[v] - 1 < 5 or T.deg[a] + 1 > 7 or T.deg[b] + 1 > 7: continue
        T.flip(u, v)
    return T

def simulate(T, P, theta, Wt, margin, F_of_ctx):
    deg = T.deg; n = T.n; ch = [60 * (6 - deg[v]) * NT.SCALE for v in range(n)]
    for u in range(n):
        if deg[u] not in (5, 6): continue
        n5 = sum(deg[x] == 5 for x in T.adj[u])
        for v in T.adj[u]:
            if deg[v] < 6: continue
            x, y = T.opp[(u, v)], T.opp[(v, u)]
            a = P[NT.pidx(deg[u], deg[v], deg[x], deg[y], n5)] * NT.SCALE
            ch[u] -= a; ch[v] += a
    c1 = list(ch); out = list(ch)
    for u in range(n):
        if deg[u] != 7: continue
        w, s, r, ap = TT.words(T, u)
        sl = [j for j in range(7) if w[j] == 7]
        if not sl or c1[u] <= theta * NT.SCALE: continue
        sc = {j: int(F_of_ctx(NT.sides(w, s, j)).astype(np.int64) @ Wt) for j in sl}
        mx = max(sc.values()); S = [j for j in sl if sc[j] >= mx - margin]
        sur = c1[u] - theta * NT.SCALE
        assert sur % NT.SCALE == 0
        for j in S:
            amt = (sur // NT.SCALE) * (NT.SCALE // len(S)); out[u] -= amt; out[r[j]] += amt
    return c1, out

def main(seed=0, ntor=30):
    rng = random.Random(seed)
    D = RW.load()
    W5all = sorted({RW.canon(w) for w in itertools.product(NT.LET, repeat=5)})
    W6all = sorted({RW.canon(w) for w in itertools.product(NT.LET, repeat=6)})
    tors = []
    for t in range(ntor):
        T = rand_torus(rng, rng.choice([6, 7, 8, 9]), rng.choice([6, 7, 8]), rng.randrange(20, 200)); T.check(); tors.append(T)
    R7 = {TT.canon_ws(*TT.words(T, v)[:2]) for T in tors for v in range(T.n) if T.deg[v] == 7}
    R7 = sorted(set(tuple(map(tuple, x)) for x in R7) | set(D['R7']))
    idx = {x: i for i, x in enumerate(R7)}
    B = NT.build(R7, W5all, W6all, adm=False)
    nf = B['F'].shape[1]; cidx = {c: i for i, c in enumerate(B['ctxs'])}
    i5 = {w: i for i, w in enumerate(W5all)}; i6 = {w: i for i, w in enumerate(W6all)}
    nchk = 0; worst = 0
    for trial in range(6):
        P = np.array([3 * rng.randrange(0, 12) for _ in range(NT.NPAR)]); theta = rng.randrange(-30, 30)
        Wt = np.array([rng.randrange(-3, 4) for _ in range(nf)]); margin = rng.randrange(0, 4)
        E = NT.exact(B, P, theta, Wt, margin)
        Fc = lambda c: NT.ctx_feats(c)
        for T in tors:
            c1, fin = simulate(T, P, theta, Wt, margin, Fc)
            assert sum(fin) == sum(60 * (6 - d) * NT.SCALE for d in T.deg)
            for v in range(T.n):
                d = T.deg[v]; w, s = TT.words(T, v)[:2]
                if d == 7: bnd = E['f7'][idx[TT.canon_ws(w, s)]]
                elif d == 5: bnd = E['f5'][i5[RW.canon(w)]]
                else: bnd = E['f6'][i6[RW.canon(w)]]
                assert fin[v] <= bnd, ('VIOLATION', trial, d, w, s, fin[v], bnd)
                worst = max(worst, fin[v] - bnd); nchk += 1
    print('torus self-test OK: %d tori, %d vertex checks, true final <= row bound everywhere (max gap %d)' % (len(tors), nchk, worst))
    # how often are tori 5/6/7 with both 5s and 7s
    print('degree mix of tori:', [dict(sorted(__import__("collections").Counter(T.deg).items())) for T in tors[:5]])
if __name__ == '__main__': main()
