# E2b: necklace clusters (balls strung along a geodesic, overlapping at narrow necks -> many boundary chords).
# Does min tau grow with the number of necks/chords?
import json, random, time, sys, math
from multiprocessing import Pool
from lev import *
from e1_survey import graph
from e2_strips import ascend, geodesic
def job(a):
    name, s, L, bead, gap, seed = a
    T = graph(name); rng = random.Random(seed)
    try:
        path = geodesic(T, s, L, rng); S = set()
        for i in range(0, len(path), gap): S |= set(bfs(T.adj, path[i], bead))
        cl = Cluster(T, S)
    except Exception as e:
        return dict(name=name, L=L, err=str(e))
    t0 = time.time(); K, unk = ascend(cl); info = cl.info()
    return dict(name=name, L=L, bead=bead, gap=gap, seed=seed, tau=K, unk=unk, chords=len(chords(cl)), sec=round(time.time()-t0, 1),
                n=info['n'], m=info['m'], nodd=info['nodd'], maxdepth=info['maxdepth'], odd_par=len(cl.odd) % 2)
if __name__ == '__main__':
    jobs = []; rng = random.Random(11)
    for name in ['ico10', 'ico20', 'BASE_rand22', 'M3_ico22_hard']:
        n = len(graph(name).adj)
        for (bead, gap) in [(1, 3), (2, 4), (2, 5)]:
            for L in [12, 24, 48]:
                for k in range(3): jobs.append((name, rng.randrange(n), L, bead, gap, k))
    out = open('e2b_neck.jsonl', 'w')
    with Pool(1) as p:
        for res in p.imap_unordered(job, jobs):
            out.write(json.dumps(res)+'\n'); out.flush(); print(res, flush=True)
