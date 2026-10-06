import sys, subprocess
from nlab import *
P="/private/tmp/planemap-next/plantri58/plantri"
line=subprocess.run([P,"-m5","17","-a"],capture_output=True,text=True).stdout.splitlines()[1]
rot=parse(line); n=len(rot); adj=[set(r) for r in rot]
for x in (5,15):
  ring=rot[x]
  for col in colourings_minus(adj,n,x):
    cl=classify(adj,x,ring,col)
    if cl is None: continue
    u,(D,al,be,ga)=cl
    pi=pair_info(adj,col,x); key=lambda p,q:(min(p,q),max(p,q))
    vec=(pi[key(D,al)],pi[key(D,be)],pi[key(D,ga)],pi[key(al,be)],pi[key(al,ga)],pi[key(be,ga)])
    if vec!=((1,0),(2,0),(2,0),(1,0),(1,0),(1,0)): continue
    if not all(not class_in_G(adj,n,x,u[j],col)[0] for j in (1,3,4)): continue
    nm={D:'D',al:'a',be:'b',ga:'g'}
    csg,idg=comps(adj,col,{D,ga},x); K2=csg[idg[u[2]]]
    csb,idb=comps(adj,col,{D,be},x); K0=csb[idb[u[0]]]
    P13=path_in(adj,col,{al,be},u[1],u[3],x); P14=path_in(adj,col,{al,ga},u[1],u[4],x)
    print("x",x,"ring",u,"rot(x)",ring)
    print(" col",{v:nm[col[v]] for v in sorted(col)})
    print(" P13",P13,"P14",P14,"shared",[v for v in P14 if v in P13],[v for v in P13 if v in P14])
    print(" K2",sorted(K2),"K0",sorted(K0))
    print(" edges", sorted((a,b) for a in col for b in adj[a] if b in col and a<b))
