"""[computed, exploratory, post hoc] Case I/II for c', c'' on locked discs (res file lines)."""
import sys
sys.argv=['x']
from tn_lib import *
def run(line):
    col_l,edges=parse(line); n,x,adj=build(col_l,edges); V=n-1
    col={v:col_l[v] for v in range(V)}; u=list(range(5)); D,al,be,ga=0,1,2,3
    csg,idg=comps(adj,col,{D,ga},x); K2=csg[idg[2]]
    csb,idb=comps(adj,col,{D,be},x); K0=csb[idb[0]]
    def sw(c,K,a,b):
        c2=dict(c)
        for w in K: c2[w]=b if c[w]==a else a
        return c2
    def conn(c,p,q,pair):
        cs,ix=comps(adj,c,set(pair),x); return ix[p]==ix[q]
    out={}
    # c' : K2 swap
    c0=sw(col,K2,D,ga)
    hit14=conn(c0,4,1,(al,ga)) or conn(c0,4,2,(al,ga))   # first-order unlock => separable
    cs,ix=comps(adj,c0,{al,ga},x); Q4=cs[ix[4]]; c1=sw(c0,Q4,al,ga)
    cs,ix=comps(adj,c1,{al,be},x); E=cs[ix[3]]; c2=sw(c1,E,al,be)
    cI=conn(c2,2,4,(be,ga))   # True = Case I
    out["c'"]=("unlocked1" if hit14 else ("I" if cI else "II"), len(Q4),len(E),len(K2))
    # c'' : K0 swap, mirror: u0<->u2,u3<->u4,beta<->gamma
    c0=sw(col,K0,D,be)
    hit=conn(c0,3,1,(al,be)) or conn(c0,3,0,(al,be))
    cs,ix=comps(adj,c0,{al,be},x); Q3=cs[ix[3]]; c1=sw(c0,Q3,al,be)
    cs,ix=comps(adj,c1,{al,ga},x); E=cs[ix[4]]; c2=sw(c1,E,al,ga)
    cI=conn(c2,0,3,(be,ga))
    out["c''"]=("unlocked1" if hit else ("I" if cI else "II"), len(Q3),len(E),len(K0))
    return out
for line in open(sys.argv[1] if len(sys.argv)>1 else '../MathNDiscSearch/res_23.txt'):
    if 'DISC' in line:
        l=line[line.index('DISC'):].strip()
        print(l[:20], run(l))
