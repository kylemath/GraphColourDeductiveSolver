import sys, subprocess
from nlab import *
P=sys.argv[1]
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
    ex=lambda S:sum(len(adj[w])-5 for w in S)
    csg,idg=comps(adj,col,{D,ga},x); K2=csg[idg[u[2]]]
    csb,idb=comps(adj,col,{D,be},x); K0=csb[idb[u[0]]]
    X=[w for w in K2 if col[w]==D]; Y=[w for w in K2 if col[w]==ga]
    X0=[w for w in K0 if col[w]==D]; Y0=[w for w in K0 if col[w]==be]
    print("x",x,"K2: |X|,|Y|",len(X),len(Y),"exc(Y)-exc(X)=",ex(Y)-ex(X),"pred",1-3*(len(Y)-len(X)),"| K0: |X0|,|Y0|",len(X0),len(Y0),"exc(Y0)-exc(X0)=",ex(Y0)-ex(X0),"pred",1-3*(len(Y0)-len(X0)))
    print("   degrees K2",[(w,col[w],len(adj[w])) for w in sorted(K2)],"K0",[(w,col[w],len(adj[w])) for w in sorted(K0)])
