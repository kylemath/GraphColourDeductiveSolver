# cheap structure probe of R=3 closings: for each renaming repairable at R=3, a minimal-change repair (old-colour
# phases); locate the changed vertices at distance 3 from the conflicts ("deep" changes): pole distance, seam
# corners nearby (A-seam vertex with #B-neighbours != 2), and how many separate spots they form.
import sys, json
sys.path.insert(0,'/mnt/project-files/multiscale/closing/round3')
from s3_scale import *
from pysat.solvers import Glucose4
def analyse(fn):
    d = pickle.load(open(fn, 'rb')); T = Tri(d['adj']); n = len(T.adj); allv = set(range(n))
    A = set(d['A']); colA, colB = d['colA'], d['colB']
    poles = [v for v in range(n) if T.deg[v] % 2]; dP = multi_bfs(T.adj, poles, allv)
    seamA = [u for u in A if any(w not in A for w in T.adj[u])]
    corner = set(u for u in seamA if sum(1 for w in T.adj[u] if w not in A) != 2)
    seamv = set(x for u in A for w in T.adj[u] if w not in A for x in (u, w))
    out = []
    for p in PERMS:
        col = dict(colA); col.update({v: p[c] for v, c in colB.items()})
        K = conflicts2(T, A, col); dK = multi_bfs(T.adj, list(K), allv)
        free = [v for v in range(n) if dK.get(v, 99) <= 3]
        if not repair_ok(T, col, free): continue
        fs = set(free); enc = CNF(sorted(fs))
        for v in fs:
            for w in T.adj[v]:
                if w in fs:
                    if w > v: enc.neq(v, w)
                else: enc.cls.append([-enc.x(v, col[w])])
        ph = [enc.x(v, c)*(1 if c == col[v] else -1) for v in enc.verts for c in range(4)]
        s = Glucose4(bootstrap_with=enc.cls); s.set_phases(ph); s.solve()
        mod = set(l for l in s.get_model() if l > 0); s.delete()
        deep = [v for v in enc.verts if dK[v] == 3 and enc.x(v, col[v]) not in mod]
        spots = []
        for v in deep:
            dv = bfs(T.adj, v, 6)
            for sp in spots:
                if sp[0] in dv: sp.append(v); break
            else: spots.append([v])
        near = set(u for v in deep for u in bfs(T.adj, v, 3) if u in seamA)
        out.append(dict(nK=len(K), ndeep=len(deep), spots=len(spots), pole_d_min=min([dP[v] for v in deep], default=None),
                        corner_rate_near=round(len(near & corner)/max(1, len(near)), 3)))
    return dict(file=fn.split('/')[-1], L=len(seamv), n=n, seam_corner_rate=round(len(corner)/len(seamA), 3),
                perms_R3=len(out), detail=out[:4])
if __name__ == '__main__':
    for fn in sys.argv[1:]: print(json.dumps(analyse(fn)), flush=True)
