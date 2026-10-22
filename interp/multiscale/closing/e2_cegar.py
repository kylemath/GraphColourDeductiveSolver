# E2: CEGAR adversary. Find level colourings c_A, c_B that are compatible (renaming id) on the seam except in a
# window around seam vertex x, such that NO recolouring of Z = N_R(window seam vertices) gives a proper colouring.
# Then evaluate the true closing R over all 24 renamings.
import sys, json
from multiprocessing import Pool
from cl import *
import e1util

def cegar(T, cA, cB, x, omega, R, maxit=3000, rng=None, tA=None, tB=None, tlimit=600):
    n = len(T.adj); A = cA.S; allv = set(range(n)); t0 = time.time()
    seamE = seam_edges(T, A); seamV = set(v for e in seamE for v in e)
    dx = multi_bfs(T.adj, [x], allv)
    Wv = set(v for v in seamV if dx[v] <= omega)
    winE = [e for e in seamE if e[0] in Wv or e[1] in Wv]
    Kmax = set(v for e in winE for v in e)
    dz = multi_bfs(T.adj, list(Kmax), allv); Z = set(v for v in allv if dz[v] <= R)
    ring = set(w for v in Z for w in T.adj[v] if w not in Z)
    enc = CNF(range(n))
    for u in range(n):
        for w in T.adj[u]:
            if u < w and ((u in A) == (w in A)): enc.neq(u, w)
    for (u, w) in seamE:
        if (u, w) not in winE and (w, u) not in winE: enc.neq(u, w)
    eqs = []
    for (u, w) in winE:
        e = enc.new(); eqs.append(e)
        for c in range(4): enc.cls.append([-e, -enc.x(u, c), enc.x(w, c)]); enc.cls.append([-e, enc.x(u, c), -enc.x(w, c)])
    enc.cls.append(eqs)
    enc.level(cA, 1.0, t=tA); enc.level(cB, 1.0, t=tB)
    # symmetry: fix colours of one triangle in A
    f = next(T.faces[i] for i in cA.tris)
    for j in range(3): enc.fix(f[j], j)
    S = Cadical153(bootstrap_with=enc.cls)
    zl = sorted(Z)
    it = 0
    while it < maxit and time.time()-t0 < tlimit:
        it += 1
        if not S.solve(): S.delete(); return dict(status='UNSAT', it=it, nZ=len(Z), nring=len(ring), sec=round(time.time()-t0))
        mod = set(l for l in S.get_model() if l > 0)
        col = {v: next(c for c in range(4) if enc.x(v, c) in mod) for v in range(n)}
        # completion check
        ez = CNF(zl)
        for v in zl:
            for w in T.adj[v]:
                if w in Z:
                    if w > v: ez.neq(v, w)
                else: ez.cls.append([-ez.x(v, col[w])])
        d = ez.solve()
        if d is None:
            S.delete()
            return dict(status='FOUND', it=it, nZ=len(Z), nring=len(ring), col=col, sec=round(time.time()-t0))
        blk = []
        for u in ring:
            for c in set(d[z] for z in T.adj[u] if z in Z): blk.append(enc.x(u, c))
        S.add_clause(blk)
    S.delete(); return dict(status='TIMEOUT', it=it, nZ=len(Z), nring=len(ring), sec=round(time.time()-t0))

def job(a):
    mapname, kind, seed, omega, R = a
    rng = random.Random(seed)
    T, A, cA, cB, meta = e1util.make_case(mapname, kind, rng)
    if A is None: return dict(err='nosplit')
    seamV = sorted(set(v for e in seam_edges(T, A) for v in e))
    # put the window far from odd vertices when possible
    allv = set(range(len(T.adj)))
    dodd = multi_bfs(T.adj, [v for v in allv if T.deg[v] % 2], allv)
    x = max(seamV, key=lambda v: (dodd.get(v, 0), rng.random())) if seed % 2 == 0 else rng.choice(seamV)
    out = dict(map=mapname, kind=kind, seed=seed, omega=omega, Rtarget=R, n=len(T.adj), nA=len(cA.S), mA=cA.m, mB=cB.m,
               parA=cA.parity_odd, parB=cB.parity_odd, x_dist_odd=dodd.get(x), **meta)
    r = cegar(T, cA, cB, x, omega, R, rng=rng)
    out.update({k: v for k, v in r.items() if k != 'col'})
    if r['status'] == 'FOUND':
        col = r['col']
        colA = {v: col[v] for v in cA.S}; colB = {v: col[v] for v in cB.S}
        Rt, p, nk = closing_R(T, cA.S, cB.S, colA, colB)
        out.update(R_true=Rt, pi=p, nconf=nk, ia=walk_info(cA, colA), ib=walk_info(cB, colB))
        pickle.dump(dict(adj=T.adj, A=cA.S, col=col, out=out), open('e2_found_%s_%s_%d_%d_%d.pkl' % (mapname, kind, seed, omega, R), 'wb'))
    return out

if __name__ == '__main__':
    jobs = []
    for m in sys.argv[2].split(','):
        for kind in sys.argv[3].split(','):
            for s in range(int(sys.argv[4])):
                for omega in [1, 3]:
                    for R in [int(r) for r in sys.argv[5].split(',')]: jobs.append((m, kind, s, omega, R))
    out = open(sys.argv[1], 'a')
    with Pool(int(sys.argv[6]) if len(sys.argv) > 6 else 2) as P:
        for r in P.imap_unordered(job, jobs):
            out.write(json.dumps(r)+'\n'); out.flush(); print(r, flush=True)
