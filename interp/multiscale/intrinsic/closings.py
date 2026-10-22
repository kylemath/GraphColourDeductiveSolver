# Step 3(b): closings under the intrinsic invariant tau_int <= T on both sides (forced-|t|=2-class splits of
# closing/round3), sides coloured by the exact tau_int encoding; 'rand' colourings and 'drift' colourings
# (adversary: lap forced to extend >= D Lambda-steps along t).  R measured as in round3 (closing_fast).
# usage: closings.py out.jsonl F1,F2 nsplits nproc T
import sys, json, time, random, collections, pickle, threading
sys.path.insert(0, '/mnt/project-files/multiscale/intrinsic')
sys.path.insert(0, '/mnt/project-files/multiscale/closing/round2'); sys.path.insert(0, '/mnt/project-files/multiscale/closing/round3')
import ic
from s3_scale import make_split, closing_fast
from band import depth, CNF
from pysat.solvers import Cadical153, Glucose4
from multiprocessing import Pool

def solve_tl(cls, tl, assumptions=()):
    s = Glucose4(bootstrap_with=cls); tm = threading.Timer(tl, s.interrupt); tm.start()
    ok = s.solve_limited(assumptions=list(assumptions), expect_interrupt=True); tm.cancel()
    mod = set(l for l in s.get_model() if l > 0) if ok else None; s.delete(); return ok, mod

def side_col(T_, cl, rng, T, drift=None, Wb=6, dmax=2.0, tl=300, tmax=None):
    dep = depth(T_, cl); band = [v for v in cl.verts if dep[v] <= Wb]; bs = set(band)
    enc = ic.Enc(band)
    for u, w in cl.edges:
        if u in bs and w in bs: enc.neq(u, w)
    W = dict(walk=cl.walk, s=cl.s, odd=cl.parity_odd)
    enc.walk_int(W, T, dmax=dmax, gcap=cl.m//2 + 2, min_drift=drift, tmax=tmax)
    ass = [enc.x(v, rng.randrange(4)) for v in rng.sample(band, 4)]
    ok, mod = solve_tl(enc.cls, tl, ass)
    if not ok: ok, mod = solve_tl(enc.cls, tl)
    if ok is None: return 'TIMEOUT'
    if not ok: return 'UNSAT'
    r = {v: next(c for c in range(4) if enc.x(v, c) in mod) for v in band}
    keep = {v: c for v, c in r.items() if dep[v] <= Wb-3}
    rest = [v for v in cl.verts if v not in keep]; rs = set(rest); e2 = CNF(rest)
    for u, w in cl.edges:
        if u in rs and w in rs: e2.neq(u, w)
        elif u in rs: e2.cls.append([-e2.x(u, keep[w])])
        elif w in rs: e2.cls.append([-e2.x(w, keep[u])])
    ok2, mod2 = solve_tl(e2.cls, tl)
    if ok2 is None: return 'EXT_TIMEOUT'
    if not ok2: return 'EXTFAIL'
    col = dict(keep); col.update({v: next(c for c in range(4) if e2.x(v, c) in mod2) for v in rest})
    return col

def info(cl, col):
    W = dict(walk=cl.walk, s=cl.s, odd=cl.parity_odd); t = ic.tvec(W, col)
    return dict(tau_int=round(ic.tau_int(W, col), 3), onelap=round(ic.tau_walk(W, col), 3), drift=round(ic.drift(W, col), 2),
                t=round(math.sqrt(ic.n2(t)), 3) if t else 0, hodge=round(ic.tau_hodge(W, col), 3))

import math
from cl import conflicts, PERMS, multi_bfs
def repair_tl(T_, col, free, tl):
    fs = set(free); e = CNF(sorted(fs))
    for v in fs:
        for w in T_.adj[v]:
            if w in fs:
                if w > v: e.neq(v, w)
            else: e.cls.append([-e.x(v, col[w])])
    ok, _ = solve_tl(e.cls, tl); return ok
def closing_R(T_, A, B, colA, colB, Rmax=8, tl=10):
    n = len(T_.adj); allv = set(range(n)); data = []
    for p in PERMS:
        col = dict(colA); col.update({v: p[c] for v, c in colB.items()})
        K = conflicts(T_, A, col); data.append((len(K), p, col, K))
    data.sort(key=lambda t: t[0]); unk = 0; dc = {}
    for R in range(Rmax+1):
        for nk, p, col, K in data:
            if nk == 0: return dict(R=0, nconf=0, unk=unk)
            if p not in dc: dc[p] = multi_bfs(T_.adj, list(K), allv)
            free = [v for v in range(n) if dc[p].get(v, 99) <= R]
            ok = repair_tl(T_, col, free, tl)
            if ok: return dict(R=R, nconf=nk, nconf_min=data[0][0], unk=unk, perm=list(p))
            if ok is None: unk += 1
    return dict(R='>%d' % Rmax, unk=unk, nconf_min=data[0][0])
def job(a):
    F, seed, T, kinds, TMAX = a; t0 = time.time()
    r = make_split(F, 'pole', seed)
    if r[0] is None: return dict(F=F, seed=seed, err='nosplit')
    T_, A, cA, cB, dA, dB, feas, os1, seam, rng, rej, att = r
    B = cB.S; cols = {'A': [], 'B': []}; fails = collections.Counter()
    for nm, cl in (('A', cA), ('B', cB)):
        for kind, dr in kinds:
            D = None if dr is None else max(2, int(dr*cl.m))
            c = side_col(T_, cl, rng, T, drift=D, tmax=TMAX)
            if isinstance(c, dict): cols[nm].append((kind, D, c, info(cl, c))); print('side', F, seed, nm, kind, D, cols[nm][-1][3], round(time.time()-t0), flush=True)
            else: fails['%s_%s' % (kind, c)] += 1
    res = []
    for ka, Da, ca, ia in cols['A']:
        for kb, Db, cb, ib in cols['B']:
            o = closing_R(T_, A, B, ca, cb, Rmax=8)
            o.update(kA=ka, kB=kb, DA=Da, DB=Db, iA=ia, iB=ib); res.append(o)
            if o.get('R', 99) >= 4:
                pickle.dump(dict(F=F, seed=seed, adj=T_.adj, A=A, colA=ca, colB=cb, out=o),
                            open('/mnt/project-files/multiscale/intrinsic/hardc_%d_%d_%s%s.pkl' % (F, seed, ka, kb), 'wb'))
    return dict(F=F, seed=seed, T=T, tmax=TMAX, L=len(seam), mA=cA.m, mB=cB.m, parity='even+even', fails=dict(fails), res=res, sec=round(time.time()-t0))

if __name__ == '__main__':
    out, Fs, ns, npr, T = sys.argv[1], [int(x) for x in sys.argv[2].split(',')], int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5])
    kinds = [('rand', None), ('rand', None), ('drift', 0.25), ('drift', 0.5)]
    if len(sys.argv) > 6: kinds = json.loads(sys.argv[6])
    TMAX = float(sys.argv[7]) if len(sys.argv) > 7 and sys.argv[7] != 'none' else None
    jobs = [(F, s, T, kinds, TMAX) for F in Fs for s in range(ns)]
    with Pool(npr) as P:
        for r in P.imap_unordered(job, jobs):
            open(out, 'a').write(json.dumps(r)+'\n')
            rr = r.get('res', [])
            print(r.get('F'), r.get('seed'), 'L', r.get('L'), r.get('fails'), 'R', sorted(collections.Counter(x.get('R') for x in rr).items()),
                  'byKind', sorted(collections.Counter((x['kA'], x['kB'], x.get('R')) for x in rr).items()),
                  'drifts', sorted(set((x['iA']['drift'], x['iA']['t'], x['iA']['tau_int']) for x in rr)), r.get('sec'), flush=True)
