import sys, random, time, collections; sys.path.insert(0, '/tmp/swarm-W16/code')
import w16lib as W, torus as TT, explore as X
W.init()
for seed, (p, q, r), allowed, steps in [(1, (4, 1, 4), (5,6,7,8,9), 4000), (2, (5, 2, 4), (5,6,7,8,9), 4000), (3, (4, 0, 5), (5,7,8), 4000)]:
    rng = random.Random(seed); T = TT.lattice_torus(p, q, r); T.check(); t0 = time.time(); found = {}
    res = X.anneal(T, set(allowed), steps, rng=rng, found=found, need=lambda c: any(l[0] != 'C' for l in c))
    st = collections.Counter()
    for v in range(T.n):
        lab = W.vertex_row(T, v); st[(T.deg[v], W.row_status(lab) if 5 <= T.deg[v] <= 9 else 'deg')] += 1
    print('n=%d allowed=%s obj=%d found=%d time %.1fs cache %d status %s' % (T.n, allowed, res, len(found), time.time() - t0, len(X._RAW), dict(st)), flush=True)
