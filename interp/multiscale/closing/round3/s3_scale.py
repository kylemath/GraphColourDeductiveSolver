# S3: scaling of closing R vs seam length L on icoF, F != 0 mod 3 (where 6/6 splits force |t|=2 on both sides).
# Round-2 failure on ico30: for F = 0 mod 3 the only feasible translation of a 6-pole half is t = 0 (diag.log).
# usage: s3_scale.py out.jsonl F1,F2,.. kinds nsplits k nproc
import sys, json
sys.path.insert(0,'/mnt/project-files/multiscale/closing/round2'); sys.path.insert(0,'/mnt/project-files/multiscale/closing/round3')
from band import *
import e1util
from tcheck import band_feasible
from fastcol import fast_level_col
from multiprocessing import Pool
OUT = '/mnt/project-files/multiscale/closing/round3/'

def conflicts2(T, A, col):
    return set(x for u in A if u in col for w in T.adj[u] if w not in A and w in col and col[u] == col[w] for x in (u, w))

def closing_fast(T, A, B, colA, colB, Rmax=8):
    """as round2 closing_full (R_conf and W_band), with per-renaming BFS cached."""
    n = len(T.adj); allv = set(range(n))
    seamv = set(x for u in A for w in T.adj[u] if w not in A for x in (u, w))
    dS = multi_bfs(T.adj, list(seamv), allv)
    data = []
    for p in PERMS:
        col = dict(colA); col.update({v: p[c] for v, c in colB.items()})
        K = conflicts2(T, A, col); data.append((len(K), p, col, K))
    data.sort(key=lambda t: t[0])
    out = {}
    for W in range(0, Rmax+1):
        hit = None
        for nk, p, col, K in data:
            if nk == 0: hit = (p, col, []); break
            free = [v for v in range(n) if dS[v] <= W]
            if repair_ok(T, col, free): hit = (p, col, free); break
        if hit:
            st = recol_stats(T, hit[1], hit[2], seamv) if hit[2] else (0, -1)
            out.update(W_band=W, band_changed=st[0], band_maxd=st[1]); break
    dcache = {}
    for R in range(0, Rmax+1):
        hit = None
        for nk, p, col, K in data:
            if nk == 0: hit = (p, col, [], 0); break
            if p not in dcache: dcache[p] = multi_bfs(T.adj, list(K), allv)
            d = dcache[p]
            free = [v for v in range(n) if d.get(v, 99) <= R]
            if repair_ok(T, col, free): hit = (p, col, free, nk); break
        if hit:
            st = recol_stats(T, hit[1], hit[2], seamv) if hit[2] else (0, -1)
            out.update(R=R, nconf=hit[3], conf_changed=st[0], conf_maxd=st[1], nconf_min=data[0][0], perm=list(hit[0])); break
    return out

def make_split(F, kind, seed, maxatt=40):
    rng = random.Random(9000+97*F+seed)
    adj = e1util.base('ico%d' % F); T = Tri(adj); n = len(adj)
    poles = [v for v in range(n) if T.deg[v] == 5]
    rej = collections.Counter()
    for attempt in range(maxatt):
        wig = {'pole': 0.0, 'polew': 0.3, 'polew2': 0.6, 'bal': 0.0}[kind]
        c = rng.choice(poles) if kind.startswith('pole') else rng.randrange(n)
        A0 = grow(T, c, n//2 + rng.randint(-n//25, n//25), rng, wiggle=wig)
        A, r = smooth(T, A0, rng)
        if A is None: rej['smooth'] += 1; continue
        cA, cB = r
        if cA.parity_odd or cB.parity_odd: rej['par'] += 1; continue
        seam = seam_edges(T, A); sv = set(x for e in seam for x in e)
        os1 = len(odd_near(T, sv, 1))
        if os1 > 1: rej['odd'] += 1; continue
        dA, dB = depth(T, cA), depth(T, cB)
        # t = 0 excluded exactly (band-UNSAT => full-UNSAT, Cadical + colour symmetry break); then read the
        # translation orbit off one level colouring (avoids slow Glucose UNSAT proofs of the other orbit).
        if band_feasible(T, cA, (0, 0), 6, dA) or band_feasible(T, cB, (0, 0), 6, dB): rej['t0'] += 1; continue
        feas = {}
        for nm, cl, dp in (('A', cA, dA), ('B', cB, dB)):
            c = fast_level_col(T, cl, rng, t=None, dep=dp, Wb=6, extend=F < 35)
            H = cl.walk_heights(c); t = (H[-1][0]-H[0][0], H[-1][1]-H[0][1])
            feas[nm] = [(4, 0) if t in [(4, 0), (0, 4), (-4, -4)] else (-4, 0) if t in [(-4, 0), (0, -4), (4, 4)] else list(t)]
        if not all(tuple(feas[x][0]) in [(4, 0), (-4, 0)] for x in 'AB'): rej['tbig'] += 1; continue
        return T, A, cA, cB, dA, dB, feas, os1, seam, rng, dict(rej), attempt
    return None, dict(rej)

def job(a):
    F, kind, seed, k = a; t0 = time.time()
    r = make_split(F, kind, seed)
    if r[0] is None: return dict(F=F, kind=kind, seed=seed, err='nosplit', rej=r[1])
    T, A, cA, cB, dA, dB, feas, os1, seam, rng, rej, att = r
    n = len(T.adj); B = cB.S; sv = set(x for e in seam for x in e)
    dS = multi_bfs(T.adj, list(sv), set(range(n)))
    odd_d = sorted(dS[v] for v in range(n) if T.deg[v] % 2)
    tsplit = time.time()-t0
    ca, cb = [], []
    for lst, cl, dp, nm in ((ca, cA, dA, 'A'), (cb, cB, dB, 'B')):
        t = feas[nm][0]
        orb = [(4, 0), (0, 4), (-4, -4)] if t == (4, 0) else [(-4, 0), (0, -4), (4, 4)]
        while len(lst) < k:
            c = fast_level_col(T, cl, rng, t=rng.choice(orb), dep=dp, Wb=6, extend=F < 35)
            if isinstance(c, dict): lst.append(c)
    tcol = time.time()-t0-tsplit
    res = []
    for i in range(k):
        for j in range(k):
            o = closing_fast(T, A, B, ca[i], cb[j], Rmax=8 if F < 35 else 4); res.append(o)
            if not isinstance(o.get('R'), int) or o['R'] >= 3 or not isinstance(o.get('W_band', 0), int) or o.get('W_band', 0) >= 3:
                pickle.dump(dict(F=F, kind=kind, seed=seed, adj=T.adj, A=A, colA=ca[i], colB=cb[j], out=o),
                            open(OUT + 'hard_%d_%s_%d_%d_%d.pkl' % (F, kind, seed, i, j), 'wb'))
    return dict(F=F, kind=kind, seed=seed, n=n, L=len(seam), mA=cA.m, mB=cB.m, odd_seam1=os1, odd_d=odd_d[:4],
                feasA=feas['A'], feasB=feas['B'], rej=rej, att=att, res=res,
                sec=[round(tsplit), round(tcol), round(time.time()-t0)])

if __name__ == '__main__':
    jobs = []
    for s in range(int(sys.argv[4])):
        for F in sys.argv[2].split(','):
            for kind in sys.argv[3].split(','): jobs.append((int(F), kind, s, int(sys.argv[5])))
    jobs.sort(key=lambda j: j[0])
    out = open(sys.argv[1], 'a')
    with Pool(int(sys.argv[6])) as P:
        for r in P.imap_unordered(job, jobs):
            out.write(json.dumps(r)+'\n'); out.flush()
            rr = r.get('res', [])
            print(r.get('F'), r.get('kind'), r.get('seed'), 'L', r.get('L'), r.get('err'), r.get('rej'), 'R', sorted(collections.Counter(x.get('R') for x in rr).items()),
                  'W', sorted(collections.Counter(x.get('W_band') for x in rr).items()), 'maxch', max([x.get('conf_changed', 0) for x in rr], default=None), r.get('sec'), flush=True)
