# Soundness self-test for net2 (three rounds): simulate on random 5/6/7 tori; true final <= row bound for every vertex.
import sys, os, random, itertools, collections, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'w16', 'code'))
import torus as TT, rows as RW, net2 as N2
from test_torus import rand_torus

def simulate(T, P, th7, th6, W2, m2, W3, m3):
    deg = T.deg; S = N2.SCALE; ch = [60 * (6 - deg[v]) * S for v in range(T.n)]
    for u in range(T.n):
        if deg[u] not in (5, 6): continue
        rot = T.rot(u); d = len(rot)
        for i, v in enumerate(rot):
            if deg[v] < 6: continue
            x, y = rot[(i - 1) % d], rot[(i + 1) % d]; hx, hy = rot[(i - 2) % d], rot[(i + 2) % d]
            o = deg[rot[(i + 3) % d]] if deg[u] == 6 else None
            a = P[N2.pkey(deg[u], deg[v], (deg[x], deg[hx]), (deg[y], deg[hy]), o)] * S
            ch[u] -= a; ch[v] += a
    c1 = list(ch)
    def send(u, targets_deg, W, m, amount_total):
        w, s, r, ap = TT.words(T, u); sl = [j for j in range(len(w)) if w[j] in targets_deg]
        if not sl: return []
        sc = {j: int(N2.ctx_feats((w[j], N2.sides(w, s, j))).astype(np.int64) @ W) for j in sl}
        mx = max(sc.values()); Sx = [j for j in sl if sc[j] >= mx - m]
        return [(r[j], amount_total // len(Sx)) for j in Sx]
    c2 = list(c1)
    for u in range(T.n):
        if deg[u] == 7 and c1[u] > th7 * S:
            for v, a in send(u, (6, 7), W2, m2, (c1[u] - th7 * S) // S * S): c2[u] -= a; c2[v] += a
    fin = list(c2)
    for u in range(T.n):
        if deg[u] == 6 and c2[u] > th6 * S:
            amt = c2[u] - th6 * S
            for v, a in send(u, (7,), W3, m3, amt):
                assert amt % len(send(u, (7,), W3, m3, amt)) == 0
                fin[u] -= a; fin[v] += a
    return fin

def main(seed=0, ntor=30, trials=5):
    rng = random.Random(seed); D = RW.load()
    tors = []
    for t in range(ntor):
        T = rand_torus(rng, rng.choice([6, 7, 8, 9]), rng.choice([6, 7, 8]), rng.randrange(20, 200)); T.check(); tors.append(T)
    rw = lambda T, v: TT.canon_ws(*TT.words(T, v)[:2])
    R7 = sorted(set(D['R7']) | {rw(T, v) for T in tors for v in range(T.n) if T.deg[v] == 7})
    R6 = sorted({rw(T, v) for T in tors for v in range(T.n) if T.deg[v] == 6} | set(N2.rows6(D['W6'])))
    W5 = sorted({RW.canon(w) for w in itertools.product(N2.LET, repeat=5)})
    B = N2.build(R7, R6, W5, adm=False)
    i7 = {x: i for i, x in enumerate(R7)}; i6 = {x: i for i, x in enumerate(R6)}; i5 = {x: i for i, x in enumerate(W5)}
    n = 0; touched = collections.Counter()
    for tr in range(trials):
        P = np.array([3 * rng.randrange(0, 10) for _ in range(N2.NPAR)])
        th7, th6 = rng.randrange(-30, 30), rng.randrange(-20, 20)
        W2 = np.array([rng.randrange(-3, 4) for _ in range(B['F2'].shape[1])]); W3 = np.array([rng.randrange(-3, 4) for _ in range(B['F3'].shape[1])])
        m2, m3 = rng.randrange(0, 4), rng.randrange(0, 4)
        E = N2.exact(B, P, th7, th6, W2, m2, W3, m3)
        touched['R2'] += int((E['sur2'] > 0).sum()); touched['R3'] += int((E['sur3'] > 0).sum())
        for T in tors:
            fin = simulate(T, P, th7, th6, W2, m2, W3, m3)
            assert sum(fin) == sum(60 * (6 - d) * N2.SCALE for d in T.deg)
            for v in range(T.n):
                d = T.deg[v]
                b = E['f7'][i7[rw(T, v)]] if d == 7 else E['f6'][i6[rw(T, v)]] if d == 6 else E['f5'][i5[RW.canon(TT.words(T, v)[0])]]
                assert fin[v] <= b, ('VIOLATION', tr, d, TT.words(T, v)[:2], fin[v], b)
                n += 1
    print('torus self-test (3 rounds) OK: %d tori x %d parameter sets, %d vertex checks; rows forwarding R2/R3: %s' % (ntor, trials, n, dict(touched)))
if __name__ == '__main__': main()
