# Depth scan: two-vortex cap A = ball(mid, 10+k) on ico20 (vortices 20 apart), B = ball of same radius at distance 2rA+1.
# Records min R (all 24 renamings), min w, and the depths of U's vortices from dU.  Usage: python exp4.py map kmin kmax seed
import sys, json, time, random
sys.path.insert(0, '/mnt/project-files/multiscale/merge_proof')
from mp import *
name, kmin, kmax, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
g = G(make(name)); rng = random.Random(seed); n = g.n
deg5 = [v for v in range(n) if g.deg[v] % 2 == 1]
log = open('/mnt/project-files/multiscale/merge_proof/exp4_%s_s%d.jsonl' % (name, seed), 'a')
for k in range(kmin, kmax+1):
    for trial in range(3):
        o1 = rng.choice(deg5); d1 = bfs(g.adj, o1, 40)
        d, o2 = sorted((d, o) for o, d in d1.items() if o != o1 and o in deg5)[0]
        path = [o2]
        while path[-1] != o1: path.append(min((w for w in g.adj[path[-1]] if w in d1), key=lambda w: d1[w]))
        mid = path[len(path)//2]; rA = d//2 + k; A = ball(g, mid, rA)
        dm = bfs(g.adj, mid, 3*rA); far = [v for v in dm if dm[v] == 2*rA+1]
        if not far: continue
        B = ball(g, rng.choice(far), rA) - A
        if any(check(g, S)[0] == 'nodisc' for S in (A, B, A | B)): continue
        D = Disc(g, A | B); dB = multi_bfs(g.adj, list(D.bset), D.S)
        odd = [v for v in D.S if g.deg[v] % 2 and v not in D.bset]; depths = sorted(dB[o] for o in odd)
        dA_ = multi_bfs(g.adj, list(Disc(g, A).bset), A); depthsA = sorted(dA_[o] for o in A if g.deg[o] % 2 and o in dA_ and dA_[o] > 0)
        for fa in (None, 'nonzero'):
            cA = level_cols(g, A, 2, fa, seed0=11*seed+k, budget=3*10**7); cB = level_cols(g, B, 2, None, seed0=11*seed+k+5, budget=3*10**7)
            for ca in cA:
                for cb in cB:
                    t0 = time.time(); rec = merge_all24(g, D, A, B, ca, cb, Rmax=5, wmax=8)
                    rec.update(map=name, k=k, rA=rA, nA=len(A), nB=len(B), fa=fa, nodd=len(odd), depths=depths, depthsA=depthsA, sec=round(time.time()-t0, 1))
                    log.write(json.dumps(rec)+'\n'); log.flush()
                    print({kk: rec[kk] for kk in ('k', 'nA', 'nB', 'fa', 'nodd', 'depths', 'depthsA', 'tA', 'tB', 'nconf', 'R', 'w', 'wc', 'ptau_before', 'mU', 'sec')}, flush=True)
