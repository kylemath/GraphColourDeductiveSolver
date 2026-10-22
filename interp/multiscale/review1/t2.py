# Claim 1(ii): crater disc A merged with a flat disc B. (a) lattice merge inside hemisphere U=D_{2D}; (b) pillow closing.
import sys, time, math, json; sys.path.insert(0,'/mnt/project-files/multiscale/review1')
from rv import *
out = open('t2_merge.jsonl', 'a')
def rec(d):
    print(json.dumps(d), flush=True); out.write(json.dumps(d)+'\n'); out.flush()
# (a) also: does a crater without the w=0-elsewhere constraint allow a flat boundary?
for d in (2, 3, 4):
    T = pillow(d); c = T.idx[(0,0)]
    cl, r = crater_col(T, T.front, c, K2=0.75, others=None)
    rec(dict(test='crater_flat_boundary_no_w_constraint', d=d, sat=r is not None, w2=(count_w2(T, r, cl.S)[0] if r else None)))
# (b) pillow closing: front = crater D_d, back = 3-coloured
for d in range(2, 9):
    T = pillow(d); c = T.idx[(0,0)]
    clA, cA = crater_col(T, T.front, c, K2=1.0)
    clB, cB = three_col(T, T.back)
    assert cA and cB
    t = time.time(); R, p, nk = closing_R(T, clA.S, clB.S - clA.bset, cA, cB, Rmax=d+2)
    rec(dict(test='pillow_closing', d=d, n=len(T.adj), tauA=round(clA.tau(cA)[0],3), tauB=round(clB.tau(cB)[0],3), R=R, nconf=nk, sec=round(time.time()-t,1)))
# (c) lattice merge: U = front hemisphere of pillow(2D), A = {i<=0}, B = {i>=1}, crater at (-D,0)
for D in range(2, 8):
    N = 2*D; T = pillow(N); U = T.front
    A = set(v for v in U if T.pos[v][0] <= 0); B = U - A
    c = T.idx[(-D, 0)]
    clA, cA = crater_col(T, A, c, K2=1.0)
    if cA is None:
        rec(dict(test='lattice_merge', D=D, note='no crater colouring of A at K2=1')); continue
    clB, cB = three_col(T, B)
    clU = Cluster(T, U)
    seamv = set(x for (u, w) in clU.edges if (u in A) != (w in A) for x in (u, w))
    dist_c = min(bfs(T.adj, c).get(v, 99) for v in seamv)
    t = time.time(); R, p, col = merge(T, A, B, cA, cB, Rmax=D+2, U=clU)
    res = dict(test='lattice_merge', D=D, N=N, nU=len(U), tauA=round(clA.tau(cA)[0],3), dist_crater_seam=dist_c, R=R, sec=round(time.time()-t,1))
    if col:
        w2 = count_w2(T, col, clU.S); res['w2_after'] = w2[0]; res['w_after_at_crater'] = winding(T, col, c)
        res['tauU'] = round(clU.tau(col)[0], 3)
    rec(res)
    # same but B is a random level w=0 colouring instead of a 3-colouring
    clB2, cB2 = level_w(T, B, K2=1.0, wmode='min', seed=D)
    if cB2:
        t = time.time(); R2, p2, col2 = merge(T, A, B, cA, cB2, Rmax=D+2, U=clU)
        rec(dict(test='lattice_merge_Blevel', D=D, tauB=round(clB2.tau(cB2)[0],3), R=R2, sec=round(time.time()-t,1)))
