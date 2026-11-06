import sys, os
ROOT = os.environ.get('F2B7_AUDIT_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # package root
DIS = ROOT + '/tree/ex_A97/backgroundMaterial/planemap-structural/longtable/reducibility/discharge'  # was '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge' (b8b/rings.py, ball.py there are md5-identical to the packaged ex_A97 copies)
sys.path.insert(0, DIS+'/b8b'); sys.path.insert(0, DIS)
from rings import Layered
def build2(D, LK, r2):
    L = Layered(D); L.add_ring(list(LK))
    Wr = L.rings[1]; Z = L.ring(); adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    name = {0: ('u',)}
    for i, w in enumerate(Wr): name[w] = ('w', i)
    Wi = {w: i for i, w in enumerate(Wr)}; cnt = {}
    for z in Z:
        ws = sorted(Wi[x] for x in adj[z] if x in Wi)
        if len(ws) == 2:
            i, j = ws; name[z] = ('s', j if (i, j) == (0, D - 1) else i)
        else:
            i = ws[0]; cnt[i] = cnt.get(i, 0) + 1; name[z] = ('p', i, cnt[i])
    L.add_ring([r2.get(name[z], 9) for z in Z])
    adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    return adj, name, {frozenset(t) for t in L.tris}
for D in (7,8):
  for LK in ([7]+[5]*(D-1), [7,7,5]+[5]*(D-4)+[8], [7]+[6]*(D-1)):
    adj, name, faces = build2(D, LK, {('s',j):6 for j in range(D)})
    pa = {x: {name[y] for y in adj[v] if y in name} for v, x in name.items()}
    print('D',D,'LK',LK)
    for x in sorted(pa):
        if x[0]=='p' and x[1]==0: print('  ',x,'adj',sorted(pa[x]))
    # check s convention: s_j adjacent to w_j and w_{j+1}
    for j in range(D):
        ws = sorted(y for y in pa[('s',j)] if y[0]=='w')
        assert ws == sorted([('w',j),('w',(j+1)%D)]), (j, ws)
    print('  s_j adj w_j,w_{j+1}: ok')
    pf = {frozenset(name[y] for y in f) for f in faces if all(y in name for y in f)}
    print('  faces containing w0:', sorted(sorted(f) for f in pf if ('w',0) in f))
