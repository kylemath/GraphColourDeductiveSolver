import sys
from chain import *
from collections import Counter
D_='/Users/fulkanjou/GraphColour/SolvingFrameworkPlan/docs/working/MathNDiscSearch/'
def classify(adj,x,V,col,mir):
    D,al,be,ga=0,1,2,3
    A,B=(ga,be) if not mir else (be,ga)
    ur,uq,ue,apex,goal=(2,4,3,0,2) if not mir else (0,3,4,2,0)
    u1=1
    cs,ix=comps(adj,col,{D,A},x); c0=sw(col,cs[ix[ur]],D,A); Dp=c0[apex]
    cs,ix=comps(adj,c0,{al,A},x)
    if ix[uq]==ix[1] or ix[uq]==ix[goal]: return ('unl1',)
    c1=sw(c0,cs[ix[uq]],al,A)
    cs,ix=comps(adj,c1,{al,B},x); c2=sw(c1,cs[ix[ue]],al,B)
    cs,ix=comps(adj,c2,{be,ga},x)
    cI = (ix[2]==ix[4]) if not mir else (ix[0]==ix[3])
    if not cI: return ('II',)
    c3=sw(c2,cs[ix[goal]],be,ga)
    if goodf(adj,x,c3,apex): return ('Ia',)
    # Ib: test neighbours of c2
    info=pairinfo(adj,x,c2,V,Dp)
    nb=[]
    for a,b in ((1,2),(1,3),(2,3)):
        cs2,ix2=comps(adj,c2,{a,b},x)
        for K in cs2:
            if goodf(adj,x,sw(c2,K,a,b),apex): nb.append((N[a]+N[b],len(cs2)))
    return ('Ib',info,tuple(sorted(set(nb))))
tal=Counter()
for fn in sys.argv[1:]:
    for line in open(D_+fn):
        if 'DISC' not in line: continue
        l=line[line.index('DISC'):].strip()
        cl,edges=parse(l); n,x,adj=build(cl,edges); V=n-1
        col={v:cl[v] for v in range(V)}
        for mir in (0,1):
            r=classify(adj,x,V,col,mir)
            tal[(fn,)+((r[0],r[1],r[2]) if r[0]=='Ib' else (r[0],))]+=1
for k,v in sorted(tal.items(),key=str): print(v,k)
