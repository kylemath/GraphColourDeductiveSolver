# Adversarial local search for a large closing radius R: keep a split with forced |t|=2 on both sides, and
# repeatedly re-solve one side's level colouring inside a random seam window (rest fixed, levelness kept on the
# whole walk). Accept if score = (R, #renamings that fail at radius R-1... ) does not decrease.
# usage: adv.py F kind seed iters out_prefix [init.pkl]
import sys, json
sys.path.insert(0,'/mnt/project-files/multiscale/closing/round3')
from s3_scale import *

def Rscore(T, A, B, colA, colB, Rmax=4):
    n = len(T.adj); allv = set(range(n)); data = []
    for p in PERMS:
        col = dict(colA); col.update({v: p[c] for v, c in colB.items()})
        K = conflicts2(T, A, col)
        if not K: return (0, 0)
        data.append((len(K), col, multi_bfs(T.adj, list(K), allv)))
    data.sort(key=lambda t: t[0])
    for R in range(Rmax+1):
        ok = 0
        for nk, col, d in data:
            if repair_ok(T, col, [v for v in range(n) if d.get(v, 99) <= R]): ok += 1
        if ok: return (R, 24-ok)   # larger second entry = fewer renamings repairable at this R = harder
    return (Rmax+1, 0)

def perturb(T, cl, col, rng, r, t):
    walk = set(cl.walk); S = cl.S
    b = rng.choice(cl.walk); win = set(v for v in bfs(T.adj, b, r) if v in S and v in col)
    verts = sorted(win | walk); vs = set(verts); enc = CNF(verts)
    for u, w in cl.edges:
        if u in vs and w in vs: enc.neq(u, w)
        elif u in win and w in col: enc.cls.append([-enc.x(u, col[w])])
        elif w in win and u in col: enc.cls.append([-enc.x(w, col[u])])
    for v in walk - win: enc.fix(v, col[v])
    enc.level(cl, 1.0, t=t)
    res = enc.solve(phases=rand_phases(enc, rng), budget=10**6)
    if not isinstance(res, dict): return None
    new = dict(col); new.update(res); return new

if __name__ == '__main__':
    F, kind, seed, iters, pre = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    r = make_split(F, kind, seed)
    T, A, cA, cB, dA, dB, feas, os1, seam, rng, rej, att = r
    B = cB.S; rng = random.Random(seed*31+F)
    if len(sys.argv) > 6:
        d = pickle.load(open(sys.argv[6], 'rb')); assert set(d['A']) == set(A); colA, colB = d['colA'], d['colB']
    else:
        colA = fast_level_col(T, cA, rng, t=tuple(feas['A'][0]), dep=dA, Wb=6, extend=F < 35); colB = fast_level_col(T, cB, rng, t=tuple(feas['B'][0]), dep=dB, Wb=6, extend=F < 35)
    tA = tuple(cA.walk_heights(colA)[-1]); tB = tuple(cB.walk_heights(colB)[-1])
    sc = Rscore(T, A, B, colA, colB); best = sc; t0 = time.time()
    print('init', F, kind, seed, 'L', len(seam), 'score', sc, flush=True)
    for it in range(iters):
        side = rng.random() < 0.5; rad = rng.choice([3, 4, 5, 6])
        if side: nA = perturb(T, cA, colA, rng, rad, tA); nB = colB
        else: nB = perturb(T, cB, colB, rng, rad, tB); nA = colA
        if nA is None or nB is None: continue
        s2 = Rscore(T, A, B, nA, nB)
        if s2 >= sc:
            colA, colB, sc = nA, nB, s2
            if sc > best:
                best = sc; pickle.dump(dict(F=F, kind=kind, seed=seed, adj=T.adj, A=A, colA=colA, colB=colB, score=sc),
                                        open(pre + '_best.pkl', 'wb'))
        print(it, 'side', 'A' if side else 'B', rad, 'cand', s2, 'cur', sc, 'best', best, round(time.time()-t0), flush=True)
