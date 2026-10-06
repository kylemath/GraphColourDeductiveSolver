import sys, subprocess, itertools
from collections import deque
from nlab import *
P="/private/tmp/planemap-next/plantri58/plantri"
line=subprocess.run([P,"-m5","17","-a"],capture_output=True,text=True).stdout.splitlines()[1]
rot=parse(line); n=len(rot); adj=[set(r) for r in rot]
def canon(c):
    m={}; return tuple(m.setdefault(c[v],len(m)) for v in sorted(c))
def broken(cc,x,ring,y):
    s=cc[y]; out=[]
    for kk in range(4):
        if kk==s: continue
        cs,idx=comps(adj,cc,{s,kk},x)
        if not any(cc[w]==kk and idx[w]==idx[y] for w in ring if w!=y): out.append(kk)
    return out
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
    K2=comps(adj,col,{D,ga},x); K0=comps(adj,col,{D,be},x)
    csg,idg=K2; K2=csg[idg[u[2]]]; csb,idb=K0; K0=csb[idb[u[0]]]
    for name,K,pr,ai in (("c'",K2,(D,ga),0),("c''",K0,(D,be),2)):
        c1=swap_comp(col,K,*pr); y=u[ai]; s=c1[y]
        dist={canon(c1):0}; rep={canon(c1):c1}; q=deque([c1]); g={}
        while q:
            cc=q.popleft(); k0=canon(cc); g[k0]=set()
            for a,b in PAIRS:
                if s in (a,b): continue
                cs,idx=comps(adj,cc,{a,b},x)
                for K_ in cs:
                    c2=swap_comp(cc,K_,a,b); k=canon(c2)
                    if k==k0: continue
                    g[k0].add(k)
                    if k not in dist: dist[k]=dist[k0]+1; rep[k]=c2; q.append(c2)
        degs=sorted(len(v) for v in g.values())
        bd=[dist[k] for k,cc in rep.items() if broken(cc,x,ring,y)]
        print("x",x,name,"class",len(dist),"degrees",degs,"dist to broken",sorted(bd),"dist multiset",sorted(dist.values()))
        if x==5 and name=="c'":
            ids={k:i for i,k in enumerate(sorted(dist,key=lambda k:dist[k]))}
            E=sorted({tuple(sorted((ids[a],ids[b]))) for a,bs in g.items() for b in bs})
            print("   edges",E,"dist",{ids[k]:dist[k] for k in dist},"broken",[ids[k] for k,cc in rep.items() if broken(cc,x,ring,y)])
