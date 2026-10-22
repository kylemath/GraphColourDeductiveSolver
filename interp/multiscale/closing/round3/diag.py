# diagnose which t are band-feasible on each side, vs F and split type / pole count
import sys, json
sys.path.insert(0,'/mnt/project-files/multiscale/closing/round2')
from band import *
import e1util
from multiprocessing import Pool
def job(a):
    F, kind, seed = a
    rng = random.Random(100*F+seed); adj = e1util.base('ico%d'%F); T = Tri(adj); n = len(adj)
    poles = [v for v in range(n) if T.deg[v] == 5]
    c = rng.choice(poles) if kind=='pole' else rng.randrange(n)
    A0 = grow(T, c, n//2, rng, wiggle=0.0)
    A, r = smooth(T, A0, rng)
    if A is None: return dict(F=F, kind=kind, err='smooth')
    cA, cB = r
    seam = seam_edges(T, A); sv = set(x for e in seam for x in e)
    out = dict(F=F, kind=kind, seed=seed, L=len(seam), podd=[cA.parity_odd, cB.parity_odd], npA=len(cA.odd), npB=len(cB.odd), os1=len(odd_near(T, sv, 1)))
    if cA.parity_odd or cB.parity_odd: return out
    for nm, cl in (('A', cA), ('B', cB)):
        dp = depth(T, cl)
        out[nm] = [t for t in [(0,0),(4,0),(-4,0)] if band_level_col(T, cl, rng, t=t, dep=dp, Wb=6) is not None]
    return out
if __name__ == '__main__':
    jobs = [(F, k, s) for F in map(int, sys.argv[1].split(',')) for k in ('pole','bal') for s in range(int(sys.argv[2]))]
    with Pool(4) as P:
        for r in P.imap_unordered(job, jobs): print(json.dumps(r), flush=True)
