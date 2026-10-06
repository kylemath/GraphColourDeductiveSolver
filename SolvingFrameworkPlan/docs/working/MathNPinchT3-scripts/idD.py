import sys, subprocess, itertools
from nlab import *
P="/private/tmp/planemap-next/plantri58/plantri"
tot=bad=0
for N in (12,14,15,16,17):
  out=subprocess.run([P,"-m5",str(N),"-a"],capture_output=True,text=True).stdout.splitlines()
  for line in out:
    rot=parse(line); n=len(rot); adj=[set(r) for r in rot]
    for x in range(n):
      if len(rot[x])!=5: continue
      ring=rot[x]
      for col in colourings_minus(adj,n,x):
        # 4-colour ring or not: test all
        for (p,q) in PAIRS:
          r,s=[k for k in range(4) if k not in (p,q)]
          cs,idx=comps(adj,col,{r,s},x)
          m=len({idx[w] for w in ring if col[w] in (r,s)})
          cpq,_=comps(adj,col,{p,q},x)
          Vp=[w for w in col if col[w] in (p,q)]
          e=sum(1 for u in Vp for w in adj[u] if w>u and w in col and col[w] in (p,q))
          cyc=e-len(Vp)+len(cpq)
          tot+=1
          if len(cs)!=cyc+m: bad+=1
  print(N,tot,bad,flush=True)
