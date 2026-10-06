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
    nm={D:'D',al:'a',be:'b',ga:'g'}
    csg,idg=comps(adj,col,{D,ga},x); K2=csg[idg[u[2]]]
    csb,idb=comps(adj,col,{D,be},x); K0=csb[idb[u[0]]]
    print("x",x,"ring",u,"K2",sorted(K2),"K0",sorted(K0), "K2 colours",[nm[col[w]] for w in sorted(K2)],"K0 colours",[nm[col[w]] for w in sorted(K0)])
    print("  degrees ring",[len(adj[w]) for w in u], "sizes", {nm[k]:sum(1 for v in col if col[v]==k) for k in nm})
    for name,K,pr in (("nu_g",K2,(D,ga)),("nu_b",K0,(D,be))):
        c2=swap_comp(col,K,*pr)
        pi2=pair_info(adj,c2,x)
        # names in c2: colours same labels
        print("  ",name,{ ''.join(sorted(nm[a]+nm[b])):v for (a,b),v in pi2.items()})
    # K2 vs K0 overlap
    print("  K2&K0",sorted(K2&K0))
