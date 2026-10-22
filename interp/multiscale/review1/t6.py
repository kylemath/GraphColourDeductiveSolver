# Claim 1(ii) on a real dome: ico10/ico20, crater at a face centre p, A = B_rho(p) (crater at distance rho from seam), B = rest.
import sys, time, math, json, random; sys.path.insert(0,'/mnt/project-files/multiscale/review1')
from rv import *
out = open('t6_dome_crater.jsonl', 'w')
def rec(d):
    print(json.dumps(d), flush=True); out.write(json.dumps(d)+'\n'); out.flush()
rng = random.Random(1)
for f, rhos in [(10, (2, 3, 4, 5)), (20, (4, 6, 8))]:
    adj = icosphere(f); T = Tri(adj); n = len(adj)
    odd = [v for v in range(n) if T.deg[v] % 2]; dd = {}
    for o in odd:
        for v, d in bfs(adj, o).items(): dd[v] = min(dd.get(v, 99), d)
    p = max(dd, key=dd.get)
    for rho in rhos:
        A = set(bfs(adj, p, rho)); B = set(range(n)) - A
        cA = disc_or_none(T, A); cB = disc_or_none(T, B)
        if cA is None or cB is None: rec(dict(f=f, rho=rho, note='not discs')); continue
        t0 = time.time()
        clA, colA = crater_col(T, A, p, K2=1.0)
        if colA is None: rec(dict(f=f, rho=rho, note='no crater colouring')); continue
        for s in range(2):
            colB = level_col(cB, rng, K2=1.0)
            R, pi, nk = closing_R(T, A, B, colA, colB, Rmax=rho+2)
            rec(dict(f=f, n=n, rho=rho, dist_crater_odd=dd[p], nA=len(A), tauA=round(cA.tau(colA)[0],3), tauB=round(cB.tau(colB)[0],3), seed=s, R=R, nconf=nk,
                     w2_in_B=count_w2(T, colB, B)[0], sec=round(time.time()-t0,1)))
        # also B with minimal winding (reviewer's invariant on B), A crater
        clB2, colB2 = level_w(T, B, K2=1.0, wmode='min', seed=rho)
        if colB2 and colB2 != 'UNK':
            R, pi, nk = closing_R(T, A, B, colA, colB2, Rmax=rho+2)
            rec(dict(f=f, rho=rho, B='minw', tauB=round(cB.tau(colB2)[0],3), R=R, nconf=nk, sec=round(time.time()-t0,1)))
