import time
from lev import *
adj=icosphere(12); T=Tri(adj)
odd=[v for v in range(len(adj)) if T.deg[v]%2]
print('n',len(adj),'odd',len(odd))
# vertex far from deg5
dd={}
for o in odd:
    for v,d in bfs(adj,o).items(): dd[v]=min(dd.get(v,99),d)
far=max(dd,key=dd.get); print('far',far,dd[far])
for r in [3,5,7]:
  for c in [far,0]:
    S=bfs(adj,c,r); cl=Cluster(T,S); print(r,c,cl.info())
    # random colourings: check closure for Eulerian
    for seed in range(3):
        col=sat_level(cl,None); print('  rand tau',cl.tau(col))
    t=time.time(); K,col,t0=min_tau(cl); print('  min tau',K,'init',t0,'%.1fs'%(time.time()-t))
