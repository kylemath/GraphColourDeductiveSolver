# Evaluate a twisted instance: weak levelness (authors' code and mine), monodromy lower bound per renaming,
# and (optionally) the exact minimum R by SAT (my checker) and by the authors' proper_repair.
import sys, json, pickle, time
sys.dont_write_bytecode = True
import pysat_stub, wk
from lat import Lat, bfs, disc_info, PERMS
from heights import colouring
from mergecheck import pockets, tau, min_R, glue, conflicts
import twist

def load(path):
    d = pickle.load(open(path, 'rb'))
    g = Lat(d['pts']); A = set(d['A']); B = set(d['B']); h = d['h']
    col = colouring(h)
    return d, g, A, B, {v: col[v] for v in A}, {v: col[v] for v in B}

def levelness(g, A, B, cA, cB):
    DA, DB = wk.Disc(g, A), wk.Disc(g, B)
    return dict(pocketsA=len(DA.pockets), chordsA=len(DA.chords), pocketsB=len(DB.pockets),
                theirs_A=max(wk.tau_walk(W, cA) for W in DA.pockets), theirs_B=max(wk.tau_walk(W, cB) for W in DB.pockets),
                mine_A=max(tau(W, cA) for W in pockets(g, A)), mine_B=max(tau(W, cB) for W in pockets(g, B)),
                strict_A=wk.tau_walk(DA.whole, cA))

def cert_lb(g, A, B, cA, cB, w, Rmax=12):
    """per renaming: least R not excluded by the monodromy obstruction (a LOWER bound on the exact R(pi))."""
    U = A | B; dU = bfs(g.adj, list(disc_info(g, U)['bset']), U)
    out = {}
    for p in PERMS:
        c = glue(A, B, cA, cB, p); K = conflicts(g, A, B, c); dK = bfs(g.adj, list(K), U) if K else {}
        R = 0
        while R <= Rmax:
            Z = set(v for v in U if dK.get(v, 99) <= R or dU[v] <= w)
            if not twist.monodromy_obstruction(g, U, c, Z): break
            R += 1
        out[p] = R
    return out

if __name__ == '__main__':
    path = sys.argv[1]; ws = [int(x) for x in sys.argv[2].split(',')]; exact = len(sys.argv) > 3 and sys.argv[3] == 'exact'
    d, g, A, B, cA, cB = load(path)
    rec = dict(file=path, params=d['params'], nA=len(A), nB=len(B), **{k: round(v, 3) if isinstance(v, float) else v for k, v in levelness(g, A, B, cA, cB).items()})
    for w in ws:
        lb = cert_lb(g, A, B, cA, cB, w)
        rec['cert_lb_w%d' % w] = min(lb.values()); rec['cert_hist_w%d' % w] = sorted(lb.values())
    print(json.dumps(rec), flush=True)
    if exact:
        for w in ws:
            t = time.time(); r = min_R(g, A, B, cA, cB, w=w, Rmax=10, verbose=True)
            print(json.dumps(dict(w=w, exact_R=r['R'], perm=r.get('perm'), unk=r['unk'], sec=round(time.time()-t))), flush=True)
