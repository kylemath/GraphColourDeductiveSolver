import sys, time
sys.path.insert(0,'/mnt/project-files/multiscale/closing')
from cl import *
import e1util
F=int(sys.argv[1]); rng=random.Random(1)
t0=time.time(); adj=e1util.base('ico%d'%F); T=Tri(adj); print('tri',time.time()-t0,len(adj),flush=True)
n=len(adj); A0=grow(T,rng.randrange(n),n//2,rng); t0=time.time(); A,r=smooth(T,A0,rng); print('smooth',time.time()-t0,flush=True)
cA,cB=r; print('m',cA.m,cB.m,cA.parity_odd,len(cA.odd))
for t in [(0,0),(4,0)]:
  t0=time.time(); enc=CNF(cA.verts)
  for u,w in cA.edges: enc.neq(u,w)
  enc.level(cA,1.0,t=t); r=enc.solve(); print('full level t',t,r is not None,time.time()-t0,flush=True)
