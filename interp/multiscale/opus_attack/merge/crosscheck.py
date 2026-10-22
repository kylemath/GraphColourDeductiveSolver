# Cross-check: authors' proper_repair_at (hierarchy/weak/wk.py, all-24 branch of do_merge) vs my min_R(w=-1).
import sys, json, time; sys.dont_write_bytecode=True
import pysat_stub, wk, evalcx
from lat import PERMS
from mergecheck import min_R, glue, conflicts
d, g, A, B, cA, cB = evalcx.load(sys.argv[1])
U = A | B; D = wk.Disc(g, U)
col = dict(cA); col.update(cB)
seam = [(u, w) for (u, w) in D.edges if (u in A) != (w in A)]
best = []
for p in PERMS:
    cc = {v: col[v] for v in A}; cc.update({v: p[col[v]] for v in B})
    K = set(x for e in seam if cc[e[0]] == cc[e[1]] for x in e); best.append((len(K), p, cc, K))
best.sort(key=lambda t: t[0])
t = time.time(); Rth = None
for RR in range(9):
    for nk, p, cc, K in best:
        r, c2 = wk.proper_repair_at(g, D.S, cc, K, RR)
        if r is not None: Rth = (RR, p); break
    if Rth: break
mine = min_R(g, A, B, cA, cB, w=-1, Rmax=8)
print(json.dumps(dict(file=sys.argv[1], theirs_R=Rth[0] if Rth else None, theirs_perm=Rth[1] if Rth else None, mine_R=mine['R'], mine_perm=mine.get('perm'), sec=round(time.time()-t))))
