# E5: closing on 6-regular tori T(p,q,r). A = rows j < q/2, B = the other rows: two annuli, seam = two
# non-contractible loops. Each band gets its (unique up to renaming) 3-colouring, so both are perfectly flat
# (tau = sqrt3/2 on every boundary loop). Closing R = min over renamings of min R (exact SAT).
import sys, json
sys.path.insert(0, '/mnt/project-files/multiscale/levelling')
from e5_torus import torus
from cl import *
class G: pass
def colour(adj, verts, k, rng):
    enc = CNF(sorted(verts)); vs = set(verts)
    for v in vs:
        for w in adj[v]:
            if w in vs and w > v: enc.neq(v, w)
    for v in vs: enc.cls.append([enc.x(v, c) for c in range(k)])
    return enc.solve(phases=rand_phases(enc, rng))
def job(a):
    p, q, r = a
    n, adj, nb, idx, simple = torus(p, q, r)
    if not simple: return None
    rng = random.Random(p*1000+q*10+r)
    allv = list(range(n))
    c3 = colour(adj, allv, 3, rng); c4 = colour(adj, allv, 4, rng)
    out = dict(p=p, q=q, r=r, n=n, col3=c3 is not None, col4=c4 is not None)
    if c3 is not None or c4 is None: return out
    A = set(idx(i, j) for i in range(p) for j in range(q//2)); B = set(allv) - A
    cA = colour(adj, A, 3, rng); cB = colour(adj, B, 3, rng)
    out['bands3'] = (cA is not None, cB is not None)
    if cA is None or cB is None:
        cA = colour(adj, A, 4, rng); cB = colour(adj, B, 4, rng)
    T = G(); T.adj = adj
    R, pi, nk = closing_R(T, A, B, cA, cB, Rmax=12)
    out.update(R=R, nconf=nk)
    # sphere-type control: same torus, A = a disc (ball), B = complement is NOT a disc; skip
    return out
if __name__ == '__main__':
    jobs = []
    for q in [4, 6, 8, 10]:
        for p in range(6, 61, 3) if len(sys.argv) < 2 else [int(x) for x in sys.argv[1].split(',')]:
            for r in range(p):
                jobs.append((p, q, r))
    random.Random(0).shuffle(jobs)
    out = open('e5_torus_closing.jsonl', 'w'); cnt = collections.Counter()
    from multiprocessing import Pool
    with Pool(1) as P:
        for res in P.imap_unordered(job, jobs[:160]):
            if res is None: continue
            out.write(json.dumps(res)+'\n'); out.flush()
            if 'R' in res: print(res, flush=True)
