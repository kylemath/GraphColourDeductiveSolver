import sys, subprocess
from nlab import *
P="/private/tmp/planemap-next/plantri58/plantri"
line=subprocess.run([P,"-m5","17","-a"],capture_output=True,text=True).stdout.splitlines()[1]
rot=parse(line); n=len(rot); adj=[set(r) for r in rot]
faces=set()
for v in range(n):
    r=rot[v]
    for i in range(len(r)):
        faces.add(frozenset((v,r[i],r[(i+1)%len(r)])))
faces=list(faces)
def region(x,start_face,Zedges):
    # faces reachable from start_face across edges not in Zedges
    seen={start_face}; st=[start_face]
    while st:
        f=st.pop()
        for e in [frozenset(p) for p in __import__('itertools').combinations(f,2)]:
            if e in Zedges: continue
            for g in faces:
                if g!=f and e<=g and g not in seen:
                    seen.add(g); st.append(g)
    return seen
def pedges(P,x,a,b):
    E={frozenset((P[i],P[i+1])) for i in range(len(P)-1)}
    E|={frozenset((x,a)),frozenset((x,b))}
    return E
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
    cn=lambda v: nm[col[v]] if v in col else 'x'
    csg,idg=comps(adj,col,{D,ga},x); K2=csg[idg[u[2]]]
    csb,idb=comps(adj,col,{D,be},x); K0=csb[idb[u[0]]]
    P13=path_in(adj,col,{al,be},u[1],u[3],x); P14=path_in(adj,col,{al,ga},u[1],u[4],x)
    X=[v for v in K2 if col[v]==D]; Y=[v for v in K2 if col[v]==ga]
    X0=[v for v in K0 if col[v]==D]; Y0=[v for v in K0 if col[v]==be]
    f_in=region(x,frozenset((x,u[1],u[2])),pedges(P13,x,u[1],u[3]))
    f_in0=region(x,frozenset((x,u[0],u[1])),pedges(P14,x,u[1],u[4]))
    # Lemma 2: every face of f_in touches K2; D/gamma vertices of closed disc in K2
    L2=all(any(v in K2 for v in f) for f in f_in)
    L20=all(any(v in K0 for v in f) for f in f_in0)
    fD=sum(1 for f in f_in if x not in f and sorted(cn(v) for v in f)==sorted('Dab'))
    fg=sum(1 for f in f_in if x not in f and sorted(cn(v) for v in f)==sorted('gab'))
    d=len(Y)-len(X)
    tau=d-(fg-fD-1)/2
    # c' pair data
    def pairdata(cc):
        pp=pair_info(adj,cc,x); return {''.join(sorted(nm[a]+nm[b])):v for (a,b),v in pp.items()}
    c1=swap_comp(col,K2,D,ga)
    print("x",x,"u",u,"tau",tau,"fD,fg",fD,fg,"d",d,"L2",L2,"L20",L20,"|Fin|",len(f_in),len(f_in0))
    lam=f_in&f_in0
    print("  Lambda faces",[sorted(f) for f in lam],"X&X0",set(X)&set(X0),"Y-Y0 edges",[(g,h) for g in Y for h in Y0 if h in adj[g]])
    print("  cprime",pairdata(c1))
    c2=swap_comp(col,K0,D,be)
    print("  cdouble",pairdata(c2))
