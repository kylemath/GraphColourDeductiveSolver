# Claim 3: high-degree hub just outside the repair collar. Sphere = icosphere with B_{r-1}(c) collapsed to a hub (deg 6r).
# Split 1 (lop): B = B_D(hub), A = rest; hub at distance D from the seam. Split 2 (bal): A = ball of radius rho around a
# vertex q with dist(q,hub)=rho+D, B = rest. Closing R with and without the hub freed.
import sys, time, math, json, random; sys.path.insert(0,'/mnt/project-files/multiscale/review1')
from rv import *
out = open('t5_hub.jsonl', 'w')
def rec(d):
    print(json.dumps(d), flush=True); out.write(json.dumps(d)+'\n'); out.flush()
def closing_R_hub(T, A, B, colA, colB, hub, Rmax=8):
    """min R over renamings, with the hub always free in addition to N_R(conflicts)."""
    n = len(T.adj); allv = set(range(n)); data = []
    for p in PERMS:
        col = dict(colA); col.update({v: p[colB[v]] for v in B}); K = conflicts(T, A, col); data.append((len(K), p, col, K))
    data.sort(key=lambda t: t[0])
    for R in range(0, Rmax+1):
        for nk, p, col, K in data:
            d = multi_bfs(T.adj, list(K), allv) if K else {}
            free = [v for v in range(n) if d.get(v, 99) <= R or v == hub]
            if repair_ok(T, col, free): return R
    return None
rng = random.Random(0)
for f, r in [(10, 3), (10, 4), (14, 5), (14, 6)]:
    T = hub_sphere(f, r); hub = T.hub; n = len(T.adj); dh = bfs(T.adj, hub)
    print('f', f, 'r', r, 'n', n, 'hub degree', T.deg[hub], 'odd vertices', sum(1 for v in range(n) if T.deg[v] % 2), flush=True)
    for D in (1, 2, 3):
        for split in ('lop', 'bal'):
            if split == 'lop':
                B = set(v for v in range(n) if dh[v] <= D); A = set(range(n)) - B
            else:
                rho = 6 if f == 10 else 9
                q = next((v for v in range(n) if dh[v] == rho + D), None)
                if q is None: continue
                A = set(bfs(T.adj, q, rho)); B = set(range(n)) - A
            cA = disc_or_none(T, A); cB = disc_or_none(T, B)
            if cA is None or cB is None: rec(dict(f=f, r=r, D=D, split=split, note='not discs')); continue
            seamv = set(x for u in A for w in T.adj[u] if w not in A for x in (u, w))
            dseam = min(dh[v] for v in seamv); nb_on_seam = sum(1 for w in T.adj[hub] if w in seamv)
            for s in range(3):
                t0 = time.time()
                colA = level_col(cA, rng, K2=1.0); colB = level_col(cB, rng, K2=1.0)
                if colA is None or colB is None: rec(dict(f=f, r=r, D=D, split=split, note='no level colouring')); continue
                R, p, nk = closing_R(T, A, B, colA, colB, Rmax=8)
                Rh = closing_R_hub(T, A, B, colA, colB, hub, Rmax=8)
                rec(dict(f=f, r=r, n=n, hubdeg=T.deg[hub], D=D, split=split, nA=len(A), nB=len(B), seam_len=len(seamv), hub_dist_seam=dseam, hub_nbrs_on_seam=nb_on_seam,
                         hub_in=('A' if hub in A else 'B'), seed=s, tauA=round(cA.tau(colA)[0],3), tauB=round(cB.tau(colB)[0],3), R=R, R_hub_free=Rh, nconf=nk, sec=round(time.time()-t0,1)))
