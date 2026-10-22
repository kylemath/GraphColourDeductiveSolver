# Witness search for the monodromy obstruction: A = two two-vortex caps joined at a neck (>=1 chord, 2 pockets,
# each with 2 vortices), weakly 1-level with |t_A| >= 4 (pocket monodromies aligned); B = adjacent vortex-free ball.
# Then for all 24 renamings: fused pocket t, min R, min w.   Usage: python exp5.py map seed
import sys, json, time, random, math, itertools
sys.path.insert(0, '/mnt/project-files/multiscale/merge_proof')
from mp import *
from exp3 import per_renaming
name, seed = sys.argv[1], int(sys.argv[2])
g = G(make(name)); rng = random.Random(seed); n = g.n
deg5 = [v for v in range(n) if g.deg[v] % 2 == 1]
log = open('/mnt/project-files/multiscale/merge_proof/exp5_%s_s%d.jsonl' % (name, seed), 'a')
def pair_mid(o1, o2):
    d1 = bfs(g.adj, o1, 60); path = [o2]
    while path[-1] != o1: path.append(min((w for w in g.adj[path[-1]] if w in d1), key=lambda w: d1[w]))
    return path[len(path)//2], d1[o2]
dd = {o: bfs(g.adj, o, 60) for o in deg5}
pairs_ = [(o1, o2) for o1 in deg5 for o2 in deg5 if o1 < o2 and dd[o1][o2] == min(dd[o1][o] for o in deg5 if o != o1)]
rng.shuffle(pairs_); found = 0; tried = 0
for (p1, p2), (q1, q2) in itertools.combinations(pairs_, 2):
    if len({p1, p2, q1, q2}) < 4: continue
    tried += 1
    if tried > 400 or found >= 2: break
    mp_, d = pair_mid(p1, p2); mq, _ = pair_mid(q1, q2)
    dm = bfs(g.adj, mp_, 80)
    for r in range(d//2+1, d//2+4):
        if not (2*r-1 <= dm.get(mq, 999) <= 2*r+1): continue
        C1, C2 = ball(g, mp_, r), ball(g, mq, r); A = C1 | C2
        if sum(1 for v in A if v in deg5) != 4: continue
        st = check(g, A)
        if st[0] != 'chord': continue
        D_A = Disc(g, A)
        if len(D_A.pockets) < 2 or any(sum(1 for v in W['walk'] if v in deg5) for W in D_A.pockets): continue
        # B: vortex-free ball adjacent to the neck
        neck = set(C1) & set(C2); nb = [v for v in range(n) if v not in A and any(w in A for w in g.adj[v])]
        dn = multi_bfs(g.adj, list(neck), set(range(n)))
        cand = sorted(nb, key=lambda v: dn.get(v, 999))[:10]
        B = None
        for rb in (4, 5, 6, 3):
            for b in cand:
                Bb = ball(g, b, rb) - A
                if any(v in deg5 for v in Bb): continue
                if check(g, Bb)[0] == 'nodisc' or check(g, A | Bb)[0] == 'nodisc': continue
                D = Disc(g, A | Bb)
                if len(D.pockets) >= len(D_A.pockets): continue   # chords must fuse
                B = Bb; break
            if B: break
        if B is None: continue
        t0 = time.time()
        cA = sat2(D_A, D_A.pockets, 1.0, seed=seed, budget=6*10**7, big_walk=(D_A.whole, 30.0, 12.0))   # |t_A| >= 2*sqrt3
        if cA in (None, 'UNK'): print('A infeasible/unk', len(A), cA, round(time.time()-t0)); continue
        cB = level_cols(g, B, 2, None, seed0=seed, budget=3*10**7)
        tA = tvec(D_A.whole, cA); tAp = [tvec(W, cA) for W in D_A.pockets]
        dB = multi_bfs(g.adj, list(D.bset), D.S); depths = sorted(dB[o] for o in D.S if g.deg[o] % 2 and o not in D.bset)
        for cb in cB:
            rows = per_renaming(g, D, A, B, cA, cb, Rmax=4, wmax=8)
            # fused pocket t per renaming: pockets of U containing both A-pocket interiors
            rec = dict(map=name, nA=len(A), nB=len(B), r=r, chordsA=len(D_A.chords), pocketsA=len(D_A.pockets), chordsU=len(D.chords), pocketsU=len(D.pockets),
                       tA=tA, tA_pockets=tAp, tB=[tvec(W, cb) for W in Disc(g, B).pockets], depths=depths, mU=len(D.whole['walk']),
                       rows=rows, sec=round(time.time()-t0, 1))
            log.write(json.dumps(rec)+'\n'); log.flush(); found += 1
            print({k: rec[k] for k in ('nA', 'nB', 'chordsA', 'pocketsA', 'pocketsU', 'tA', 'tA_pockets', 'tB', 'depths', 'sec')},
                  sorted(set((r['R'], r.get('w')) for r in rows)), [(r['perm'], r['nconf'], r['tU_glued'], r['R'], r.get('w')) for r in rows][:6], flush=True)
        break
print('done', tried, found)
