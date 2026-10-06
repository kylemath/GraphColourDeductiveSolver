from chain import *
D_='/Users/fulkanjou/GraphColour/SolvingFrameworkPlan/docs/working/MathNDiscSearch/'
from collections import Counter
tally=Counter(); rows=[]
for fn in ['res_23.txt','res2_24_p0.txt','res2_24_p1.txt','res2_24_p2.txt','res2_24_p3.txt']:
    li=0
    for line in open(D_+fn):
        if 'DISC' not in line: continue
        li+=1
        l=line[line.index('DISC'):].strip()
        cl,edges=parse(l); n,x,adj=build(cl,edges); V=n-1
        col={v:cl[v] for v in range(V)}; D,al,be,ga=0,1,2,3
        for mir in (0,1):
            A,B=(ga,be) if not mir else (be,ga)
            ur,uq,ue,apex,goal=(2,4,3,0,2) if not mir else (0,3,4,2,0)
            cs,ix=comps(adj,col,{D,A},x); c0=sw(col,cs[ix[ur]],D,A); Dp=c0[apex]
            cs,ix=comps(adj,c0,{al,A},x); c1=sw(c0,cs[ix[uq]],al,A)
            cs,ix=comps(adj,c1,{al,B},x); c2=sw(c1,cs[ix[ue]],al,B)
            cs,ix=comps(adj,c2,{be,ga},x)
            case='I' if ix[ur]==ix[uq] else 'II'   # u2~u4 (mirror u0~u3)
            if mir: case='I' if ix[0]==ix[3] else 'II'
            R=cs[ix[goal]]; c3=sw(c2,R,be,ga); a3=goodf(adj,x,c3,apex)
            typ='II' if case=='II' else ('Ia' if a3 else 'Ib')
            # neighbours of c2 in class
            info=pairinfo(adj,x,c2,V,Dp)
            goods=[]
            for a,b in ((1,2),(1,3),(2,3)):
                cs2,ix2=comps(adj,c2,{a,b},x)
                for K in cs2:
                    c4=sw(c2,K,a,b)
                    if goodf(adj,x,c4,apex):
                        goods.append((N[a]+N[b],'ringfree' if not any(r in K for r in range(5)) else 'ring',len(cs2)))
            rows.append((fn[:9],li,mir,typ,info,goods))
            tally[(typ,tuple(sorted(set(g[:2] for g in goods))))]+=1
for k,v in sorted(tally.items(),key=str): print(v,k)
print()
for r in rows:
    if r[3]=='Ib': print(r)
print()
t2=Counter()
for r in rows: t2[(r[3],r[2],r[4])]+=1
for k,v in sorted(t2.items(),key=str): print(v,k)
