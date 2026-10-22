import sys, time, math, json, random; sys.path.insert(0,'/mnt/project-files/multiscale/review1')
from rv import *
out = open('t6_dome_crater.jsonl', 'a')
def rec(d):
    print(json.dumps(d), flush=True); out.write(json.dumps(d)+'\n'); out.flush()
rng = random.Random(1)
adj = icosphere(20); T = Tri(adj); n = len(adj)
odd = [v for v in range(n) if T.deg[v] % 2]; dd = {}
for o in odd:
    for v, d in bfs(adj, o).items(): dd[v] = min(dd.get(v, 99), d)
p = max(dd, key=dd.get)
for rho in (6, 8, 10):
    A = set(bfs(adj, p, rho)); B = set(range(n)) - A
    cA = disc_or_none(T, A); cB = disc_or_none(T, B)
    t0 = time.time(); clA, colA = crater_col(T, A, p, K2=1.0)
    for s in range(2):
        colB = level_col(cB, rng, K2=1.0)
        R, pi, nk = closing_R(T, A, B, colA, colB, Rmax=rho+2)
        rec(dict(f=20, n=n, rho=rho, dist_crater_odd=dd[p], nA=len(A), tauA=round(cA.tau(colA)[0],3), tauB=round(cB.tau(colB)[0],3), seed=s, R=R, nconf=nk, sec=round(time.time()-t0,1)))
