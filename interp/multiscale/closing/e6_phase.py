# E6: structured adversary. Split the seam into k arcs; on arc j force A's boundary walk into the open half-plane
# <H,u_j> > 0 and B's walk (on the facing arc) into <H, v_j> > 0, with u_j, v_j random unit directions (often v=-u).
# This makes the two walks sit on opposite sides of their centres along the seam, maximising mismatch.
import sys, json
from multiprocessing import Pool
from cl import *
import e1util
U6 = [(2, 0), (0, 2), (-2, -2), (-2, 0), (0, -2), (2, 2)]
def ip(p, u): return (n2((p[0]+u[0], p[1]+u[1])) - n2(p) - n2(u)) / 2
def half(u, eps=-1e-9): return set(p for p in domain(1.0) if ip(p, u) > eps)
def facing(T, cA, cB):
    """for each B-walk index, the A-walk index of the nearest A boundary vertex"""
    posA = {v: i for i, v in enumerate(cA.walk)}
    res = []
    for v in cB.walk:
        d = multi_bfs(T.adj, [v], set(range(len(T.adj))).__class__(cA.bset | {v}))
        cand = [(d[w], posA[w]) for w in cA.bset if w in d]
        res.append(min(cand)[1] if cand else 0)
    return res
def job(a):
    mapname, kind, seed, ntries = a
    rng = random.Random(7000+seed); t0 = time.time()
    T, A, cA, cB, meta = e1util.make_case(mapname, kind, rng)
    if A is None: return dict(err='nosplit')
    # facing map via the seam edges (B-walk vertex -> an adjacent A-walk vertex)
    posA = {v: i for i, v in enumerate(cA.walk)}
    fB = []
    for v in cB.walk:
        nbA = [posA[w] for w in T.adj[v] if w in posA]
        fB.append(nbA[0] if nbA else None)
    for i in range(len(fB)):
        if fB[i] is None: fB[i] = fB[i-1] if i else 0
    res = []
    for tr in range(ntries):
        k = rng.choice([2, 3, 4, 6])
        uA = [rng.choice(U6) for _ in range(k)]
        mode = rng.choice(['neg', 'rand'])
        uB = [(-u[0], -u[1]) for u in uA] if mode == 'neg' else [rng.choice(U6) for _ in range(k)]
        off = rng.randrange(cA.m)
        arcA = lambda i: ((i - off) % cA.m) * k // cA.m
        phA = [(i, half(uA[arcA(i)])) for i in range(cA.m) if ((i - off) % cA.m) * k % cA.m > cA.m // 8 * 0]
        phB = [(i, half(uB[arcA(fB[i])])) for i in range(cB.m)]
        ca = level_col(cA, rng, phase=phA, budget=3*10**5)
        cb = level_col(cB, rng, phase=phB, budget=3*10**5) if ca else None
        if not ca or not cb:
            # relax: constrain only the middle of each arc
            phA2 = [(i, s) for (i, s) in phA if 0.25 < (((i - off) % cA.m) * k / cA.m) % 1 < 0.75]
            phB2 = [(i, s) for (i, s) in phB if 0.25 < (((fB[i] - off) % cA.m) * k / cA.m) % 1 < 0.75]
            ca = level_col(cA, rng, phase=phA2, budget=3*10**5); cb = level_col(cB, rng, phase=phB2, budget=3*10**5)
            if not ca or not cb: res.append(dict(k=k, mode=mode, R='infeasible')); continue
        R, p, nk = closing_R(T, cA.S, cB.S, ca, cb)
        res.append(dict(k=k, mode=mode, R=R, nconf=nk, ia=walk_info(cA, ca), ib=walk_info(cB, cb)))
        if R is None or R >= 3:
            pickle.dump(dict(map=mapname, kind=kind, seed=seed, adj=T.adj, A=cA.S, colA=ca, colB=cb, R=R),
                        open('e6_R%s_%s_%s_%d_%d.pkl' % (R, mapname, kind, seed, tr), 'wb'))
    Rs = [r['R'] for r in res if r['R'] != 'infeasible']
    return dict(map=mapname, kind=kind, seed=seed, n=len(T.adj), nA=len(cA.S), mA=cA.m, mB=cB.m, parA=cA.parity_odd,
                parB=cB.parity_odd, maxR=max(Rs, default=None), hist=dict(collections.Counter(Rs)), sec=round(time.time()-t0), tries=res)
if __name__ == '__main__':
    jobs = []
    for m in sys.argv[2].split(','):
        for kind in sys.argv[3].split(','):
            for s in range(int(sys.argv[4])): jobs.append((m, kind, s, int(sys.argv[5])))
    out = open(sys.argv[1], 'a')
    with Pool(int(sys.argv[6])) as P:
        for r in P.imap_unordered(job, jobs):
            out.write(json.dumps(r)+'\n'); out.flush(); print({k: v for k, v in r.items() if k != 'tries'}, flush=True)
