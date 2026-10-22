# E3: merges of two discs A,B into a disc U. Inputs: level (tau<=1) colourings vs unconstrained random colourings.
import sys, json, random, time
from multiprocessing import Pool
from lev import *
from e1_survey import graph
def level_col(cl, seed, K2=1.0):
    rng = random.Random(seed); nv = len(cl.verts)
    ph = [(4*i+c+1)*(1 if rng.random() < 0.25 else -1) for i in range(nv) for c in range(4)]
    r = sat_level(cl, K2, budget=10**6, phases=ph)
    if r == 'UNK': r = sat_level(cl, K2)
    if r is None:
        LOG.append(('level_unsat', len(cl.S), cl.m))
        r = min_tau(cl)[1]
    return r
LOG = []
def splits(T, c, r, rng, kind):
    Uset = set(bfs(T.adj, c, r)); U = disc_or_none(T, Uset)
    if U is None: return None
    if kind == 'bal':
        a = rng.choice(U.walk); da = bfs(T.adj, a); b = max(U.walk, key=lambda v: da[v])
        dA = multi_bfs(T.adj, [a], Uset); dB = multi_bfs(T.adj, [b], Uset)
        A = set(v for v in Uset if dA[v] <= dB[v]); B = Uset - A
    else:
        rho = int(kind[3:])
        x = rng.choice(U.walk); B = set(v for v in multi_bfs(T.adj, [x], Uset).items() if v[1] <= rho); B = set(v for v, _ in B); A = Uset - B
    cA, cB = disc_or_none(T, A), disc_or_none(T, B)
    if cA is None or cB is None: return None
    return U, cA, cB
def job(a):
    name, c, r, kind, seed = a
    T = graph(name); rng = random.Random(seed)
    sp = None
    for _ in range(10):
        sp = splits(T, c, r, rng, kind)
        if sp: break
    if not sp: return dict(name=name, c=c, r=r, kind=kind, err='nosplit')
    U, cA, cB = sp
    out = dict(name=name, c=c, r=r, kind=kind, seed=seed, nU=len(U.S), nA=len(cA.S), nB=len(cB.S), mU=U.m,
               seam=sum(1 for (u, w) in U.edges if (u in cA.S) != (w in cA.S)))
    t = time.time()
    colA, colB = level_col(cA, seed), level_col(cB, seed+7)
    out['tauA'], out['tauB'] = cA.tau(colA)[0], cB.tau(colB)[0]
    R, p, col = merge(T, cA.S, cB.S, colA, colB, U=U); out['R_plain_level_in'] = R
    out['tauU_after_plain'] = U.tau(col)[0] if col else None
    R, p, col = merge(T, cA.S, cB.S, colA, colB, U=U, level_K2=1.0); out['R_level_level_in'] = R
    ra, rb = rand_col(cA, seed), rand_col(cB, seed+7)
    out['tauA_rand'], out['tauB_rand'] = cA.tau(ra)[0], cB.tau(rb)[0]
    R, p, col = merge(T, cA.S, cB.S, ra, rb, U=U); out['R_plain_rand_in'] = R
    out['sec'] = round(time.time()-t, 1); out['log'] = list(LOG); LOG.clear()
    return out
if __name__ == '__main__':
    jobs = []; rng = random.Random(5)
    for name in ['ico10', 'ico14', 'BASE_rand22', 'M3_ico22_hard']:
        n = len(graph(name).adj)
        for r in [5, 7, 9]:
            for kind in ['bal', 'lop2', 'lop1']:
                for s in range(3):
                    jobs.append((name, rng.randrange(n), r, kind, s))
    out = open('e3_merge.jsonl', 'w')
    with Pool(4) as p:
        for res in p.imap_unordered(job, jobs):
            out.write(json.dumps(res)+'\n'); out.flush(); print(res, flush=True)
