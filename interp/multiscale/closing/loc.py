# localise a hard closing instance: which seam spots need radius R instead of R-1?
import sys, json
from cl import *
class G: pass
def localise(fn, rho=4):
    d = pickle.load(open(fn, 'rb')); adj = d['adj']; n = len(adj); A = d['A']; B = set(range(n)) - A
    T = Tri(adj); colA, colB = d['colA'], d['colB']
    R, p, nk = closing_R(T, A, B, colA, colB)
    allv = set(range(n)); out = dict(file=fn, R=R, nconf=nk)
    col = dict(colA); col.update({v: p[colB[v]] for v in B})
    K = conflicts(T, A, col); dK = multi_bfs(T.adj, list(K), allv)
    base = set(v for v in allv if dK.get(v, 99) <= R-1)
    big = set(v for v in allv if dK.get(v, 99) <= R)
    # does any single local ball of extra freedom suffice?
    ys = sorted(K); good = []
    for y in ys[::2]:
        by = set(bfs(T.adj, y, rho))
        if repair_ok(T, col, base | (big & by)): good.append(y)
    out['n_spots_tested'] = len(ys[::2]); out['n_spots_sufficient'] = len(good)
    # odd vertices near the sufficient spots, distance from spots to nearest odd vertex
    odd = [v for v in allv if T.deg[v] % 2]
    dodd = multi_bfs(T.adj, odd, allv)
    out['dist_odd_at_good'] = sorted(dodd[y] for y in good)[:10]
    out['dist_odd_seam_min_max'] = (min(dodd[y] for y in K), max(dodd[y] for y in K))
    # mismatch proxy per pi: number of conflicts
    return out
if __name__ == '__main__':
    for fn in sys.argv[1:]: print(localise(fn), flush=True)
