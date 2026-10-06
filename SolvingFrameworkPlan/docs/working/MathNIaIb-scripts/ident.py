from chain import *
from collections import Counter
D_='/Users/fulkanjou/GraphColour/SolvingFrameworkPlan/docs/working/MathNDiscSearch/'
def pc(adj,x,c,V,a,b):
    cs,ix=comps(adj,c,{a,b},x)
    nv=sum(len(K) for K in cs); ne=sum(1 for u in range(V) if c[u] in (a,b) for w in adj[u] if w<V and w>u and c[w] in (a,b))
    return len(cs), len(cs)-(nv-ne)
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
        cs,ix=comps(adj,c0,{al,A},x); c1=sw(c0,cs[ix[uq]],al,A)
        cs,ix=comps(adj,c1,{al,B},x); c2=sw(c1,cs[ix[ue]],al,B)
        cs,ix=comps(adj,c2,{be,ga},x)
        cI=(ix[2]==ix[4]) if not mir else (ix[0]==ix[3])
        if not cI: continue
        c3=sw(c2,cs[ix[goal]],be,ga); ia=goodf(adj,x,c3,apex)
        # in mirror, roles beta<->gamma: the 'beta,gamma' pair is same set; D-pairs: (D,al),(D,be),(D,ga)
        fr=[pc(adj,x,c2,V,a,b) for a,b in ((1,2),(1,3),(2,3))]
        dd=[pc(adj,x,c2,V,0,k) for k in (1,2,3)]
        cycfree=sum(f[1] for f in fr); cycD=sum(d[1] for d in dd)
        tal[('Ia' if ia else 'Ib','bg comps',fr[2][0],'cycD-1-cycfree',cycD-1-cycfree,'cycDalpha',dd[0][1])]+=1
for k,v in sorted(tal.items(),key=str): print(v,k)
