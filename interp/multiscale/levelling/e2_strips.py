# E2: thin clusters. (a) strips = width-w neighbourhoods of a geodesic of length L (chordless in 5-connected maps);
# (b) necklaces = radius-2 balls strung along a geodesic, touching at necks (boundary chords).
# min tau found by ascending exact SAT tests at tau^2 in LADDER (each call budgeted; 'UNK' counts as not shown).
import json, random, time, sys, math
from multiprocessing import Pool
from lev import *
from e1_survey import graph
LADDER = [0.75, 1.0, 1.75, 2.25, 3.0, 4.0, 5.25, 6.25, 7.0, 9.0, 12.0, 16.0]
def ascend(cl):
    unk = False
    for K2 in LADDER:
        r = sat_level(cl, K2, budget=3*10**6)
        if r == 'UNK': unk = True; continue
        if r is not None: return math.sqrt(K2), unk
    return None, unk
def geodesic(T, s, L, rng):
    d = bfs(T.adj, s); far = [v for v, x in d.items() if x == L]
    t = rng.choice(far); path = [t]
    while path[-1] != s:
        x = path[-1]; path.append(min(T.adj[x], key=lambda y: d[y]))
    return path
def job(a):
    name, s, L, w, seed = a
    T = graph(name); rng = random.Random(seed)
    try:
        path = geodesic(T, s, L, rng)
        if w == 'neck':
            S = set()
            for i in range(0, len(path), 5): S |= set(bfs(T.adj, path[i], 2))
        else:
            S = set(v for v, x in multi_bfs(T.adj, path, set(range(len(T.adj)))).items() if x <= w)
        cl = Cluster(T, S)
    except Exception as e:
        return dict(name=name, L=L, w=w, err=str(e))
    t0 = time.time(); K, unk = ascend(cl); info = cl.info()
    return dict(name=name, L=L, w=w, seed=seed, tau=K, lower_bound_uncertain=unk, chords=len(chords(cl)),
                sec=round(time.time()-t0, 1), n=info['n'], m=info['m'], nodd=info['nodd'],
                maxdepth=info['maxdepth'], odd_par=len(cl.odd) % 2)
if __name__ == '__main__':
    jobs = []; rng = random.Random(3)
    for name in ['BASE_rand22', 'M3_ico22_hard', 'ico10', 'ico20']:
        n = len(graph(name).adj)
        for w in [1, 2, 'neck']:
            for L in [10, 20, 40]:
                for k in range(3):
                    jobs.append((name, rng.randrange(n), L, w, k))
    out = open('e2_strips.jsonl', 'w')
    with Pool(2) as p:
        for res in p.imap_unordered(job, jobs):
            out.write(json.dumps(res)+'\n'); out.flush(); print(res, flush=True)
