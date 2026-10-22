# Base-point dependence of w: same merged colouring, pocket walk re-based at 6 different boundary vertices.
# Usage: python exp6.py map k seed
import sys, json, time, random
sys.path.insert(0, '/mnt/project-files/multiscale/merge_proof')
from mp import *
name, k, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
g = G(make(name)); rng = random.Random(seed); n = g.n
deg5 = [v for v in range(n) if g.deg[v] % 2 == 1]
log = open('/mnt/project-files/multiscale/merge_proof/exp6_%s_k%d_s%d.jsonl' % (name, k, seed), 'a')
def rebase(W, j):
    walk, s = W['walk'], W['s']; m = len(walk); assert not W['odd']
    w2 = walk[j:]+walk[:j]; s2 = s[j:]+s[:j]; s2 = [x*s2[0] for x in s2]
    return dict(walk=w2, s=s2, odd=False, nv=W['nv'])
def min_w(D, walks, cR, zone, wmax=8):
    dB = multi_bfs(g.adj, list(D.bset), D.S)
    for ww in range(wmax+1):
        if ww == 0 and max(tau_walk(W, cR) for W in walks) <= 1+1e-9: return 0
        fx = {v: cR[v] for v in D.S if dB[v] > ww and v not in zone}
        r = sat2(D, walks, 1.0, fixed=fx)
        if r not in (None, 'UNK'): return ww
        if r == 'UNK': return 'UNK%d' % ww
    return '>%d' % wmax
done = 0
while done < 3:
    o1 = rng.choice(deg5); d1 = bfs(g.adj, o1, 40)
    d, o2 = sorted((d, o) for o, d in d1.items() if o != o1 and o in deg5)[0]
    path = [o2]
    while path[-1] != o1: path.append(min((w for w in g.adj[path[-1]] if w in d1), key=lambda w: d1[w]))
    mid = path[len(path)//2]; rA = d//2 + k; A = ball(g, mid, rA)
    dm = bfs(g.adj, mid, 3*rA); far = [v for v in dm if dm[v] == 2*rA+1]
    B = ball(g, rng.choice(far), rA) - A
    if any(v in deg5 for v in B) or any(check(g, S)[0] == 'nodisc' for S in (A, B, A | B)): continue
    D = Disc(g, A | B)
    if len(D.pockets) != 1 or D.whole['odd']: continue
    cA = level_cols(g, A, 2, 'nonzero', seed0=seed, budget=3*10**7); cB = level_cols(g, B, 1, None, seed0=seed+9, budget=3*10**7)
    if not cA or not cB: continue
    seam = [(u, w) for (u, w) in D.edges if (u in A) != (w in A)]
    for ca in cA:
        cb = cB[0]; best = None
        for p in PERMS:
            cc = {v: ca[v] for v in A}; cc.update({v: p[cb[v]] for v in B})
            K = set(x for e in seam if cc[e[0]] == cc[e[1]] for x in e)
            if best is None or len(K) < len(best[0]): best = (K, cc)
        K, cc = best
        R, cR = (0, cc) if not K else (None, None)
        for RR in range(0, 4):
            if cR is not None: break
            R, cR = proper_repair_at(g, D.S, cc, K, RR)
        zone = set(v for v in D.S if cR[v] != cc[v]); W = D.whole; m = len(W['walk'])
        res = []
        for j in [0, m//6, m//3, m//2, 2*m//3, 5*m//6]:
            Wj = rebase(W, j); t0 = time.time()
            res.append(dict(j=j, tau_before=round(tau_walk(Wj, cR), 3), w=min_w(D, [Wj], cR, zone), sec=round(time.time()-t0, 1)))
        rec = dict(map=name, k=k, nA=len(A), nB=len(B), mU=m, tU=tvec(W, cR), R=R, nconf=len(K), res=res)
        log.write(json.dumps(rec)+'\n'); log.flush(); print(rec, flush=True); done += 1
