import sys, time
sys.path.insert(0,'/mnt/project-files/multiscale/closing/round2')
from band import *
import e1util
F=int(sys.argv[1]); rng=random.Random(1)
adj=e1util.base('ico%d'%F); T=Tri(adj); n=len(adj); A0=grow(T,rng.randrange(n),n//2,rng); A,r=smooth(T,A0,rng)
cA,cB=r; print('m',cA.m,cB.m)
for t in [(0,0),(4,0),(0,4)]:
  t0=time.time(); c=band_level_col(T,cA,rng,t=None if cA.parity_odd else t); print('band lvl',t, type(c), time.time()-t0,flush=True)
  if isinstance(c,dict):
    ok=all(c[u]!=c[w] for u,w in cA.edges); print('proper',ok, cA.tau(c))
  t0=time.time(); d=band_level_col(T,cB,rng,t=None if cB.parity_odd else t); print('B', type(d), time.time()-t0, cB.tau(d) if isinstance(d,dict) else '')
  if isinstance(c,dict) and isinstance(d,dict):
    t0=time.time(); print(closing_full(T,cA.S,cB.S,c,d), time.time()-t0)
