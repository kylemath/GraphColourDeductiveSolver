# E1: closing R over many level colouring pairs, incl. forced monodromy classes, on many maps / splits.
import sys, json
from multiprocessing import Pool
from cl import *
import e1util
T2 = [(0, 0), (4, 0), (0, 4), (-4, -4), (-4, 0), (0, -4), (4, 4)]   # t in 2Lambda, |t|<=2 (half-lattice units)
def cols_for(cl, rng, k):
    out = []
    if cl.parity_odd:
        D = domain(1.0); starts = [None]*2 + rng.sample(D, min(len(D), k-2))
        for st in starts[:k]:
            c = level_col(cl, rng, start=st)
            if c: out.append(('s%s' % (st,), c))
    else:
        for t in T2:
            c = level_col(cl, rng, t=t)
            if c: out.append(('t%s' % (t,), c))
        for _ in range(max(0, k-len(out))):
            c = level_col(cl, rng); out.append(('rand', c))
    return out
def job(a):
    mapname, kind, seed = a
    rng = random.Random(seed); t0 = time.time()
    T, A, cA, cB, meta = e1util.make_case(mapname, kind, rng)
    if A is None: return dict(map=mapname, kind=kind, seed=seed, err='nosplit')
    ca = cols_for(cA, rng, 7); cb = cols_for(cB, rng, 7)
    pairs = [(i, j) for i in range(len(ca)) for j in range(len(cb))]
    rng.shuffle(pairs); pairs = pairs[:30]
    res = []
    for i, j in pairs:
        R, p, nk = closing_R(T, cA.S, cB.S, ca[i][1], cb[j][1])
        res.append(dict(a=ca[i][0], b=cb[j][0], R=R, nconf=nk, ia=walk_info(cA, ca[i][1]), ib=walk_info(cB, cb[j][1])))
    seam = set(x for e in seam_edges(T, A) for x in e)
    out = dict(map=mapname, kind=kind, seed=seed, n=len(T.adj), nA=len(cA.S), nB=len(cB.S), mA=cA.m, mB=cB.m,
               oddA=len(cA.odd), oddB=len(cB.odd), parA=cA.parity_odd, parB=cB.parity_odd,
               odd_seam1=len(odd_near(T, seam, 1)), odd_seam3=len(odd_near(T, seam, 3)),
               maxR=max((r['R'] if r['R'] is not None else 99) for r in res), hist=dict(collections.Counter(r['R'] for r in res)),
               sec=round(time.time()-t0), **meta, pairs=res)
    return out
if __name__ == '__main__':
    jobs = []
    for m in sys.argv[2].split(','):
        for kind in sys.argv[3].split(','):
            for s in range(int(sys.argv[4])): jobs.append((m, kind, s))
    out = open(sys.argv[1], 'a')
    with Pool(4) as P:
        for r in P.imap_unordered(job, jobs):
            out.write(json.dumps(r)+'\n'); out.flush()
            print({k: v for k, v in r.items() if k != 'pairs'}, flush=True)
