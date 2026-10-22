# E1: necklace with accumulating drift.  Pocket n of A has its boundary heights in Ball(n*v, 1); B level, Ball(0,1).
import sys, json, time
sys.dont_write_bytecode = True
import pysat_stub, wk                      # authors' Disc / tau_walk for the cross-check of weak levelness
from lat import disc_info
from neck import build
from heights import build_heights, ball_pts, colouring
from mergecheck import pockets, tau, min_R

def make(k, v, h=3, M=3.0, mside=6, mbot=6, seed=0, cB=(0, 0)):
    g, A, B, U, blob = build(k, h, M, mside, mbot)
    PA = pockets(g, A); PA.sort(key=lambda W: sum(g.pts[x][1] for x in W['walk'])/len(W['walk']))
    cons = {}
    for n, W in enumerate(PA):
        bp = set(ball_pts((n*v[0], n*v[1]), 1.0))
        for x in W['walk']: cons[x] = cons[x] & bp if x in cons else set(bp)
    hA = build_heights(g, A, cons, seed=seed)
    PB = pockets(g, B)
    consB = {x: set(ball_pts(cB, 1.0)) for W in PB for x in W['walk']}
    hB = build_heights(g, B, consB, seed=seed+1)
    return g, A, B, U, PA, PB, hA, hB

if __name__ == '__main__':
    v = tuple(int(t) for t in sys.argv[1].split(','))
    ks = [int(t) for t in sys.argv[2].split(',')]
    h = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    M = float(sys.argv[4]) if len(sys.argv) > 4 else 3.0
    for k in ks:
        t0 = time.time()
        g, A, B, U, PA, PB, hA, hB = make(k, v, h, M)
        if hA is None or hB is None: print(k, 'construction infeasible', hA is None, hB is None, flush=True); continue
        cA, cB = colouring(hA), colouring(hB)
        DA, DB = wk.Disc(g, A), wk.Disc(g, B)
        their = (max(wk.tau_walk(W, cA) for W in DA.pockets), max(wk.tau_walk(W, cB) for W in DB.pockets))
        mine = (max(tau(W, cA) for W in PA), max(tau(W, cB) for W in PB))
        strictA = wk.tau_walk(DA.whole, cA)
        rec = dict(k=k, v=v, h=h, M=M, nA=len(A), nB=len(B), pocketsA=len(PA), tauA_pockets_theirs=round(their[0], 3),
                   tauB_theirs=round(their[1], 3), tau_mine=[round(x, 3) for x in mine], strict_tauA=round(strictA, 3))
        for w in (-1, 1, 3):
            r = min_R(g, A, B, cA, cB, w=w, level=False, Rmax=10)
            rec['R_w%d' % w] = r['R']
        rec['sec'] = round(time.time()-t0, 1)
        print(json.dumps(rec), flush=True)
