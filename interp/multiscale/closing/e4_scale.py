# E4: scaling of closing R with seam length L (random level pairs; t forced to random achievable class).
# Saves any instance with R >= 3 for localisation.
import sys, json
from multiprocessing import Pool
from cl import *
import e1util
T2 = [(0, 0), (4, 0), (0, 4), (-4, -4), (-4, 0), (0, -4), (4, 4)]
def some_cols(cl, rng, k):
    out = []
    if cl.parity_odd:
        D = domain(1.0)
        while len(out) < k:
            c = level_col(cl, rng, start=rng.choice(D + [None]*3))
            if c: out.append(c)
    else:
        ok = [t for t in T2 if level_col(cl, rng, t=t, budget=10**5) not in (None,)]
        while len(out) < k:
            c = level_col(cl, rng, t=rng.choice(ok))
            if c: out.append(c)
    return out
def job(a):
    mapname, kind, seed, npairs = a
    rng = random.Random(1000+seed); t0 = time.time()
    T, A, cA, cB, meta = e1util.make_case(mapname, kind, rng)
    if A is None: return dict(map=mapname, kind=kind, seed=seed, err='nosplit')
    ca = some_cols(cA, rng, npairs); cb = some_cols(cB, rng, npairs)
    Rs = []
    for i in range(npairs):
        R, p, nk = closing_R(T, cA.S, cB.S, ca[i], cb[i])
        Rs.append((R, nk, walk_info(cA, ca[i]), walk_info(cB, cb[i])))
        if R is None or R >= 3:
            pickle.dump(dict(map=mapname, kind=kind, seed=seed, adj=T.adj, A=cA.S, colA=ca[i], colB=cb[i], R=R),
                        open('e4_R%s_%s_%s_%d_%d.pkl' % (R, mapname, kind, seed, i), 'wb'))
    seam = seam_edges(T, A)
    return dict(map=mapname, kind=kind, seed=seed, n=len(T.adj), nA=len(cA.S), mA=cA.m, mB=cB.m, L=len(seam),
                parA=cA.parity_odd, parB=cB.parity_odd, oddA=len(cA.odd), oddB=len(cB.odd),
                odd_seam1=len(odd_near(T, set(x for e in seam for x in e), 1)),
                R=[r[0] for r in Rs], nconf=[r[1] for r in Rs], tA=[r[2]['tvec'] for r in Rs], tB=[r[3]['tvec'] for r in Rs],
                sec=round(time.time()-t0))
if __name__ == '__main__':
    jobs = []
    for m in sys.argv[2].split(','):
        for kind in sys.argv[3].split(','):
            for s in range(int(sys.argv[4])): jobs.append((m, kind, s, int(sys.argv[5])))
    out = open(sys.argv[1], 'a')
    with Pool(int(sys.argv[6])) as P:
        for r in P.imap_unordered(job, jobs):
            out.write(json.dumps(r)+'\n'); out.flush(); print(r, flush=True)
