# S1: scaling of closing on Eulerian-seam, |t|=2-forced splits of icoF (the R=3 regime of round 1).
# usage: s1_scale.py out.jsonl F1,F2,.. kinds nsplits k nproc
import sys, json
sys.path.insert(0,'/mnt/project-files/multiscale/closing/round2')
from band import *
import e1util
from multiprocessing import Pool
def job(a):
    F, kind, seed, k = a
    mapname = 'ico%d' % F; rng = random.Random(7000+97*F+seed); t0 = time.time()
    adj = e1util.base(mapname); T = Tri(adj); n = len(adj)
    rej = collections.Counter()
    for attempt in range(40):
        if kind.startswith('pole'):
            poles = [v for v in range(n) if T.deg[v] == 5]
            A0 = grow(T, rng.choice(poles), n//2 + rng.randint(-n//25, n//25), rng, wiggle=0.0 if kind == 'pole' else 0.3)
        else:
            A0 = grow(T, rng.randrange(n), n//2, rng, wiggle=0.0 if kind == 'bal' else 1.0)
        A, r = smooth(T, A0, rng)
        if A is None: continue
        cA, cB = r
        if cA.parity_odd or cB.parity_odd: rej['par'] += 1; continue
        seam = seam_edges(T, A); sv = set(x for e in seam for x in e)
        os1 = len(odd_near(T, sv, 1))
        if os1 > 1: rej['odd'] += 1; continue
        dA, dB = depth(T, cA), depth(T, cB)
        feas = {}
        for nm, cl, dp in (('A', cA, dA), ('B', cB, dB)):
            feas[nm] = [t for t in [(0, 0), (4, 0), (-4, 0)] if band_level_col(T, cl, rng, t=t, dep=dp, Wb=6) not in (None,)]
        if (0, 0) in feas['A'] or (0, 0) in feas['B']: rej['t0'] += 1; continue
        break
    else:
        return dict(F=F, kind=kind, seed=seed, err='nosplit', rej=dict(rej))
    B = cB.S
    # odd vertex distance to seam
    allv = set(range(n)); dS = multi_bfs(T.adj, list(sv), allv)
    odd_d = sorted(dS[v] for v in range(n) if T.deg[v] % 2)
    ca, cb = [], []
    orbit = lambda t: [t, (t[1], t[0]), (-t[0]-t[1] if False else -4, -4)]
    for lst, cl, dp, nm in ((ca, cA, dA, 'A'), (cb, cB, dB, 'B')):
        t = feas[nm][0]
        orb = [(4, 0), (0, 4), (-4, -4)] if t == (4, 0) else [(-4, 0), (0, -4), (4, 4)]
        while len(lst) < k:
            c = band_level_col(T, cl, rng, t=rng.choice(orb), dep=dp)
            if isinstance(c, dict): lst.append(c)
    res = []
    for i in range(k):
        for j in range(k):
            o = closing_full(T, A, B, ca[i], cb[j]); res.append(o)
            if o.get('R', 9) >= 3 or o.get('W_band', 9) >= 3:
                pickle.dump(dict(F=F, kind=kind, seed=seed, adj=T.adj, A=A, colA=ca[i], colB=cb[j], out=o),
                            open('/mnt/project-files/multiscale/closing/round2/s1_hard_%d_%s_%d_%d_%d.pkl' % (F, kind, seed, i, j), 'wb'))
    return dict(F=F, kind=kind, seed=seed, n=n, L=len(seam), mA=cA.m, mB=cB.m, odd_seam1=os1, odd_d=odd_d[:4],
                feasA=feas['A'], feasB=feas['B'], res=res, sec=round(time.time()-t0))
if __name__ == '__main__':
    jobs = []
    for s in range(int(sys.argv[4])):
        for F in sys.argv[2].split(','):
            for kind in sys.argv[3].split(','): jobs.append((int(F), kind, s, int(sys.argv[5])))
    out = open(sys.argv[1], 'a')
    with Pool(int(sys.argv[6])) as P:
        for r in P.imap_unordered(job, jobs):
            out.write(json.dumps(r)+'\n'); out.flush()
            rr = r.get('res', [])
            print(r.get('F'), r.get('kind'), r.get('seed'), r.get('L'), r.get('err'), 'R', sorted(collections.Counter(x.get('R') for x in rr).items()),
                  'W', sorted(collections.Counter(x.get('W_band') for x in rr).items()), 'maxch', max([x.get('conf_changed', 0) for x in rr], default=None), r.get('sec'), flush=True)
