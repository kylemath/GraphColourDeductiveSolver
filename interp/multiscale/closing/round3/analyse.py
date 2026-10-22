# structure of hard closings: for the best renaming(s), split conflicts into clusters, local repair radius per
# cluster (other clusters freed with radius 6), and geometry (pole distance, seam corners) of the bottleneck clusters.
import sys, json, glob
sys.path.insert(0,'/mnt/project-files/multiscale/closing/round2')
from band import *
def clusters(T, K, gap=3):
    K = list(K); left = set(K); out = []
    while left:
        s = left.pop(); comp = {s}; fr = [s]
        while fr:
            x = fr.pop(); d = bfs(T.adj, x, gap)
            for y in list(left):
                if y in d: left.discard(y); comp.add(y); fr.append(y)
        out.append(comp)
    return out
NP = 4
def analyse(fn, Rmax=6):
    d = pickle.load(open(fn, 'rb')); T = Tri(d['adj']); n = len(T.adj); allv = set(range(n))
    A = set(d['A']); B = allv - A; colA, colB = d['colA'], d['colB']
    poles = [v for v in range(n) if T.deg[v] % 2]
    dP = multi_bfs(T.adj, poles, allv)
    seamA = [u for u in A if any(w not in A for w in T.adj[u])]
    seamv = set(x for u in A for w in T.adj[u] if w not in A for x in (u, w))
    # seam corners: A-side seam vertices with B-neighbour count != 2 (2 = straight seam on a degree-6 lattice)
    corner = {u for u in seamA if sum(1 for w in T.adj[u] if w not in A) != 2}
    perR = []; cand = []
    for p in PERMS:
        col = dict(colA); col.update({v: p[colB[v]] for v in B})
        cand.append((len(conflicts(T, A, col)), p))
    cand.sort()
    for _, p in cand[:NP]:
        col = dict(colA); col.update({v: p[colB[v]] for v in B})
        K = conflicts(T, A, col)
        if not K: perR.append((0, p, [])); continue
        cl = clusters(T, K)
        info = []
        for c in cl:
            others = K - c
            dO = multi_bfs(T.adj, list(others), allv) if others else {}
            dc = multi_bfs(T.adj, list(c), allv)
            rc = None
            for R in range(Rmax+1):
                free = [v for v in range(n) if dc.get(v, 99) <= R or dO.get(v, 99) <= 6]
                if repair_ok(T, col, free): rc = R; break
            near = [v for v in range(n) if dc.get(v, 99) <= 3]
            info.append(dict(rc=rc, size=len(c), pole_d=min(dP[v] for v in c),
                             corners=sum(1 for v in near if v in corner), seam_near=sum(1 for v in near if v in seamA)))
        perR.append((max(i['rc'] if i['rc'] is not None else 99 for i in info), p, info))
    perR.sort(key=lambda t: t[0])
    best = perR[0][0]
    bott = [i for r, p, info in perR if r == best for i in info if i['rc'] == best]
    hist = collections.Counter(r for r, _, _ in perR)
    allc = [i for r, p, info in perR for i in info]
    cr = lambda L: round(sum(i['corners'] for i in L)/max(1, sum(i['seam_near'] for i in L)), 3)
    return dict(file=fn.split('/')[-1], n=n, L=len(seamv), R_local=best, perm_R_hist=sorted(hist.items()),
                n_best_perms=sum(1 for r, _, _ in perR if r == best),
                bottleneck=bott[:6], bott_pole_d=sorted(i['pole_d'] for i in bott)[:6],
                corner_rate_bottleneck=cr(bott), corner_rate_all=cr(allc),
                size_bott=sorted(i['size'] for i in bott)[-3:], size_all_med=sorted(i['size'] for i in allc)[len(allc)//2])
if __name__ == '__main__':
    for fn in sys.argv[1:]: print(json.dumps(analyse(fn)), flush=True)
