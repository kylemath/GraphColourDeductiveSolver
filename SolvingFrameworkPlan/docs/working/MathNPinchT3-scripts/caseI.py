import sys, subprocess
from collections import deque
from nlab import *
P="/private/tmp/planemap-next/plantri58/plantri"
line=subprocess.run([P,"-m5","17","-a"],capture_output=True,text=True).stdout.splitlines()[1]
rot=parse(line); n=len(rot); adj=[set(r) for r in rot]
x=5; ring=rot[x]
def chain_ok(cc,y,u):
    s=cc[y]; bad=[]
    for kk in range(4):
        if kk==s: continue
        cs,idx=comps(adj,cc,{s,kk},x)
        if not any(cc[w]==kk and idx[w]==idx[y] for w in ring if w!=y): bad.append(kk)
    return bad
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
    c0=swap_comp(col,K2,D,ga); y=u[0]
    cs,idx=comps(adj,c0,{al,ga},x); Q4=cs[idx[u[4]]]; c1=swap_comp(c0,Q4,al,ga)
    cs,idx=comps(adj,c1,{al,be},x); E34=cs[idx[u[3]]]; c2=swap_comp(c1,E34,al,be)
    rw=lambda cc:''.join(nm[cc[w]] for w in u)
    print("state: c' ring(u0..u4)",rw(c0),"c1",rw(c1),"c2",rw(c2))
    print("  Q4",sorted(Q4),"E34",sorted(E34),"u:",u)
    cs3,idx3=comps(adj,c2,{be,ga},x)
    print("  [b,g]_2 u2~u4:",idx3[u[2]]==idx3[u[4]])
    for (a,b) in PAIRS:
        if D in (a,b): continue
        cs,idx=comps(adj,c2,{a,b},x)
        for K in cs:
            c3=swap_comp(c2,K,a,b)
            ringin=[i for i in range(5) if u[i] in K]
            print("   swap",nm[a]+nm[b],sorted(K),"ring verts",ringin,"-> ring",rw(c3),"broken",[nm[k] for k in chain_ok(c3,y,u)], "ringcolours",len(set(c3[w] for w in u)))
