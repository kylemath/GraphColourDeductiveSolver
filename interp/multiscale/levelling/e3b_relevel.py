# E3b: merge two level discs (plain min-R repair), then re-level U by recolouring a boundary collar of width w
# (plus the repair zone). Records min w so that tau(U) <= 1 again, with the deep interior of U fixed.
import sys, json, random, time
from multiprocessing import Pool
from lev import *
from e1_survey import graph
from e3_merge import level_col, splits
def relevel(T, U, col, zone, wmax=8, K2=1.0, fixed_extra=None):
    dB = multi_bfs(T.adj, U.walk, U.S)
    for w in range(0, wmax+1):
        fixed = {v: col[v] for v in U.S if dB[v] > w and v not in zone}
        r = sat_level(U, K2, fixed=fixed, budget=2*10**6)
        if r not in (None, 'UNK'): return w, r
    return None, None
def job(a):
    name, c, r, kind, seed = a
    T = graph(name); rng = random.Random(seed)
    sp = None
    for _ in range(10):
        sp = splits(T, c, r, rng, kind)
        if sp: break
    if not sp: return dict(err='nosplit')
    U, cA, cB = sp
    out = dict(name=name, c=c, r=r, kind=kind, seed=seed, nU=len(U.S), nA=len(cA.S), nB=len(cB.S), mU=U.m,
               oddA=len(cA.odd) % 2, oddB=len(cB.odd) % 2, oddU=len(U.odd) % 2)
    colA, colB = level_col(cA, seed), level_col(cB, seed+7)
    R, p, col = merge(T, cA.S, cB.S, colA, colB, U=U)
    out['R'] = R; out['tauU'], out['tU'] = U.tau(col)
    # repair zone = vertices whose colour differs from the glued colouring
    glued = {v: colA[v] for v in cA.S}; glued.update({v: p[colB[v]] for v in cB.S})
    zone = set(v for v in U.S if col[v] != glued[v])
    w, col2 = relevel(T, U, col, zone)
    out['w_relevel'] = w
    if col2: out['tU_after'] = U.tau(col2)[1]
    # depth of U (for reference)
    out['depthU'] = max(multi_bfs(T.adj, U.walk, U.S).values())
    return out
if __name__ == '__main__':
    jobs = []; rng = random.Random(5)
    for name in ['ico10', 'ico14', 'BASE_rand22', 'M3_ico22_hard']:
        n = len(graph(name).adj)
        for r in [5, 7, 9, 11]:
            for kind in ['bal', 'lop2']:
                for s in range(3):
                    jobs.append((name, rng.randrange(n), r, kind, s))
    out = open('e3b_relevel.jsonl', 'w')
    with Pool(4) as p:
        for res in p.imap_unordered(job, jobs):
            out.write(json.dumps(res)+'\n'); out.flush(); print(res, flush=True)
