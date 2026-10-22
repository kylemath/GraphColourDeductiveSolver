# E3: CEGAR for the BAND model. Exists level c_A, c_B such that for every renaming pi, no recolouring of the band
# Z = N_R(seam) gives a proper colouring?  FOUND => genuine counterexample to (b) at radius R (since N_R(K) is in Z).
# UNSAT => every level pair is band-repairable at radius R (a weaker statement than (b)).
import sys, json
from multiprocessing import Pool
from cl import *
import e1util
INV = {p: tuple(sorted(range(4), key=lambda c: p[c])) for p in PERMS}
def cegar_band(T, cA, cB, R, tlimit=900, tA=None, tB=None, extra=None):
    n = len(T.adj); A = cA.S; allv = set(range(n)); t0 = time.time()
    seamV = set(v for e in seam_edges(T, A) for v in e)
    dz = multi_bfs(T.adj, list(seamV), allv); Z = set(v for v in allv if dz[v] <= R)
    ring = set(w for v in Z for w in T.adj[v] if w not in Z)
    enc = CNF(range(n))
    for u in range(n):
        for w in T.adj[u]:
            if u < w and ((u in A) == (w in A)): enc.neq(u, w)
    enc.level(cA, 1.0, t=tA); enc.level(cB, 1.0, t=tB)
    f = next(T.faces[i] for i in cA.tris)
    for j in range(3): enc.fix(f[j], j)
    f = next(T.faces[i] for i in cB.tris)
    for j in range(3): enc.fix(f[j], j)
    if extra: extra(enc)
    S = Cadical153(bootstrap_with=enc.cls); zl = sorted(Z); it = 0; nblk = 0
    while time.time()-t0 < tlimit:
        it += 1
        if not S.solve(): S.delete(); return dict(status='UNSAT', it=it, nZ=len(Z), nring=len(ring), sec=round(time.time()-t0))
        mod = set(l for l in S.get_model() if l > 0)
        col = {v: next(c for c in range(4) if enc.x(v, c) in mod) for v in range(n)}
        found_any = False
        for p in PERMS:
            g = {v: (col[v] if v in A else p[col[v]]) for v in ring}
            ez = CNF(zl)
            for v in zl:
                for w in T.adj[v]:
                    if w in Z:
                        if w > v: ez.neq(v, w)
                    else: ez.cls.append([-ez.x(v, g[w])])
            d = ez.solve()
            if d is not None:
                found_any = True; blk = []; ip = INV[p]
                for u in ring:
                    for c in set(d[z] for z in T.adj[u] if z in Z):
                        blk.append(enc.x(u, c) if u in A else enc.x(u, ip[c]))
                S.add_clause(blk); nblk += 1
                break
        if not found_any:
            S.delete(); return dict(status='FOUND', it=it, nZ=len(Z), nring=len(ring), col=col, sec=round(time.time()-t0))
    S.delete(); return dict(status='TIMEOUT', it=it, nZ=len(Z), nring=len(ring), sec=round(time.time()-t0))

def job(a):
    mapname, kind, seed, R = a
    rng = random.Random(seed)
    T, A, cA, cB, meta = e1util.make_case(mapname, kind, rng)
    if A is None: return dict(err='nosplit')
    out = dict(map=mapname, kind=kind, seed=seed, Rband=R, n=len(T.adj), nA=len(cA.S), mA=cA.m, mB=cB.m,
               parA=cA.parity_odd, parB=cB.parity_odd, oddA=len(cA.odd), oddB=len(cB.odd), **meta)
    r = cegar_band(T, cA, cB, R)
    out.update({k: v for k, v in r.items() if k != 'col'})
    if r['status'] == 'FOUND':
        col = r['col']; colA = {v: col[v] for v in cA.S}; colB = {v: col[v] for v in cB.S}
        Rt, p, nk = closing_R(T, cA.S, cB.S, colA, colB)
        out.update(R_true=Rt, pi=p, nconf=nk, ia=walk_info(cA, colA), ib=walk_info(cB, colB))
        pickle.dump(dict(adj=T.adj, A=cA.S, col=col, out=out), open('e3_found_%s_%s_%d_%d.pkl' % (mapname, kind, seed, R), 'wb'))
    return out
if __name__ == '__main__':
    jobs = []
    for m in sys.argv[2].split(','):
        for kind in sys.argv[3].split(','):
            for s in range(int(sys.argv[4])):
                for R in [int(r) for r in sys.argv[5].split(',')]: jobs.append((m, kind, s, R))
    out = open(sys.argv[1], 'a')
    with Pool(int(sys.argv[6]) if len(sys.argv) > 6 else 2) as P:
        for r in P.imap_unordered(job, jobs):
            out.write(json.dumps(r)+'\n'); out.flush(); print(r, flush=True)
