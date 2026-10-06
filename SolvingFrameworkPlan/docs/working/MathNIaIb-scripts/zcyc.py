from chain import *
from collections import Counter
D_='/Users/fulkanjou/GraphColour/SolvingFrameworkPlan/docs/working/MathNDiscSearch/'
def core(adj,x,c,V,a,b):
    # 2-core of pair graph [a,b]
    S={v for v in range(V) if c[v] in (a,b)}
    deg={v:sum(1 for w in adj[v] if w in S) for v in S}
    st=[v for v in S if deg[v]<=1]; rem=set()
    while st:
        v=st.pop()
        if v in rem: continue
        rem.add(v)
        for w in adj[v]:
            if w in S and w not in rem:
                deg[w]-=1
                if deg[w]<=1: st.append(w)
    return S-rem
tal=Counter()
for fn in ['res_23.txt','res2_24_p0.txt','res2_24_p1.txt','res2_24_p2.txt','res2_24_p3.txt']:
  for line in open(D_+fn):
    if 'DISC' not in line: continue
    l=line[line.index('DISC'):].strip()
    cl,edges=parse(l); n,x,adj=build(cl,edges); V=n-1
    col={v:cl[v] for v in range(V)}; D,al,be,ga=0,1,2,3
    for mir in (0,1):
        A,B=(ga,be) if not mir else (be,ga)
        ur,uq,ue,apex,goal=(2,4,3,0,2) if not mir else (0,3,4,2,0)
        cs,ix=comps(adj,col,{D,A},x); c0=sw(col,cs[ix[ur]],D,A)
        Z=core(adj,x,c0,V,0,al)   # D' is colour of apex now = D? apex colour
        Dp=c0[apex]
        Z=core(adj,x,c0,V,Dp,al)
        cs,ix=comps(adj,c0,{al,A},x); Q=cs[ix[uq]]; c1=sw(c0,Q,al,A)
        cs,ix=comps(adj,c1,{al,B},x); E=cs[ix[ue]]; c2=sw(c1,E,al,B)
        cs,ix=comps(adj,c2,{be,ga},x)
        cI=(ix[2]==ix[4]) if not mir else (ix[0]==ix[3])
        if not cI: continue
        c3=sw(c2,cs[ix[goal]],be,ga); ia=goodf(adj,x,c3,apex)
        Zr=sorted(r for r in range(5) if r in Z)
        tal[('Ia' if ia else 'Ib','|Z|',len(Z),'ringZ',tuple(Zr),'Q∩Z',len(Q&Z),'E∩Z',len(E&Z))]+=1
for k,v in sorted(tal.items(),key=str): print(v,k)
