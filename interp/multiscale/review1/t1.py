import sys, time, math; sys.path.insert(0,'/mnt/project-files/multiscale/review1')
from rv import *
# sanity: w of flat 3-colouring and crater link
T = pillow(3); print('pillow(3) n', len(T.adj), 'degrees', collections.Counter(T.deg))
cl0, c3 = three_col(T, T.front); print('3-col found', c3 is not None, 'tau', cl0.tau(c3), 'w hist', count_w2(T, c3, cl0.S))
# reviewer's D_2 construction
T2 = pillow(2); c = T2.idx[(0,0)]; link = ccw_link(T2, c); print('link ccw', [T2.pos[w] for w in link])
col = {c: 0}
for k, w in enumerate(link): col[w] = 1 + k % 3
for p, k in T2.idx.items():
    if max(abs(p[0]),abs(p[1]),abs(p[0]+p[1])) == 2:
        # corner iff one coordinate is 0 or p[0]+p[1]==0 (i.e. p = 2*dir)
        corner = p in [(2*d[0],2*d[1]) for d in DIRS]
        if corner:
            i = [ (2*d[0],2*d[1]) for d in DIRS].index(p)
            # u_i is link vertex at DIRS[i]; w_i gets c(u_{i+1})
            ui = T2.idx[DIRS[i]]; ui1 = T2.idx[DIRS[(i+1)%6]]
            col[k] = col[ui1]
        else: col[k] = 0
cl2 = Cluster(T2, T2.front)
ok = all(col[u]!=col[w] for (u,w) in cl2.edges); print('D2 construction proper', ok, 'tau', cl2.tau(col), 'w:', {T2.pos[v]: winding(T2,col,v) for v in cl2.S if v not in cl2.bset})
# SAT crater colourings for d=2..8
for d in range(2, 9):
    T = pillow(d); c = T.idx[(0,0)]
    for K2 in (0.75, 1.0):
        t=time.time(); cl, r = crater_col(T, T.front, c, K2=K2)
        if r is None: print('d', d, 'K2', K2, 'UNSAT', round(time.time()-t,1)); continue
        wh = count_w2(T, r, cl.S)
        print('d', d, 'K2', K2, 'SAT tau', [round(x,3) if x is not None else None for x in cl.tau(r)], 'w2count', wh[0], 'w hist', wh[3], 'sec', round(time.time()-t,1), flush=True)
        break
