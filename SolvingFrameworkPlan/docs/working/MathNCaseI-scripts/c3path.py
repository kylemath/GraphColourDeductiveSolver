from tn_lib import *
from geo23 import path
def run(line):
    cl,edges=parse(line); n,x,adj=build(cl,edges); V=n-1
    col={v:cl[v] for v in range(V)}; D,al,be,ga=0,1,2,3
    sw=lambda c,K,a,b:{w:((b if c[w]==a else a) if w in K else c[w]) for w in c}
    csg,ig=comps(adj,col,{D,ga},x); K2=csg[ig[2]]
    csb,ib=comps(adj,col,{D,be},x); K0=csb[ib[0]]
    P13=path(adj,col,{al,be},1,3,x); P14=path(adj,col,{al,ga},1,4,x)
    names='Dabg'
    def side(tag,c0,a_,b_,Qu,Ev,c_end_pair,Rv,ring_pair):
        pass
    res=[]
    # c'
    c0=sw(col,K2,D,ga); cs,ix=comps(adj,c0,{al,ga},x)
    if ix[4]==ix[1] or ix[4]==ix[2]: return
    Q4=cs[ix[4]]; c1=sw(c0,Q4,al,ga)
    cs,ix=comps(adj,c1,{al,be},x); E=cs[ix[3]]; c2=sw(c1,E,al,be)
    cs,ix=comps(adj,c2,{be,ga},x)
    if ix[2]!=ix[4]: return
    R=cs[ix[2]]; c3=sw(c2,R,be,ga)
    cs,ix=comps(adj,c3,{al,ga},x)
    which=[nm for nm,(p,q) in (('u1~u3',(1,3)),('u1~u4',(1,4))) if ix[p]==ix[q]]
    comp=cs[ix[1]]
    pth=path(adj,c3,{al,ga},1,3 if which[0]=='u1~u3' else 4,x)
    print("c' CaseI: break via",which,"path",[(v,names[col[v]],names[c3[v]]) for v in pth])
    print("   P13",P13,"P14",P14,"K2",sorted(K2),"Q4",sorted(Q4),"E",sorted(E),"R",sorted(R))
for line in open('../MathNDiscSearch/res_23.txt'):
    if 'DISC' in line: print(line[line.index('DISC'):][:25]); run(line[line.index('DISC'):].strip())
