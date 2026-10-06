import sys; sys.path.insert(0,'.')
from astruct_core import *
import lattack_witness as W
# map witness numbering: v=0, ring i vertex t = 1+5i+t (i=0..2), cap 16
r=3; adj=build(r); L=link(r)
col={'v':None}
col={}
for i in range(r):
    for t in range(5): col[(i,t)]=W.A3_COL[1+5*i+t]
col['c']=W.A3_COL[16]
# check adjacency equals witness graph
wadj={}
for f in W.A3_FACES:
    for a in f: wadj.setdefault(a,set()).update(x for x in f if x!=a)
nm=lambda u: 0 if u=='v' else 16 if u=='c' else 1+5*u[0]+u[1]
assert all({nm(w) for w in adj[u]}==wadj[nm(u)] for u in adj), "graph mismatch"
print("graph equals witness graph; proper:",all(col[u]!=col[w] for u in col for w in adj[u] if w!='v'))
order=[u for u in adj if u!='v']
print("ring colours:",[[col[(i,t)] for t in range(5)] for i in range(r)],col['c'])
print("orbit raw (period,preperiod,alld,steps):",orbit(adj,col,L,order))
print("orbit up to renaming:",orbit(adj,col,L,order,renaming=True))
