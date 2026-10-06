"""[computed, exploratory, post hoc] D'-free Kempe class of c' and c'' on N=23 locked discs: size, edges, degrees, distance to first separable member."""
from tn_lib import *
from collections import deque
def canon(c):
    m={}; return tuple(m.setdefault(c[v],len(m)) for v in sorted(c))
def sep_at(adj,x,c,apex,chain_nbrs,ringcols_other):
    # separable at apex u iff ring misses a colour among others or some chain {col(apex),k} broken
    pass
def analyse(line):
    cl,edges=parse(line); n,x,adj=build(cl,edges); V=n-1
    col={v:cl[v] for v in range(V)}; D,al,be,ga=0,1,2,3
    sw=lambda c,K,a,b:{w:((b if c[w]==a else a) if w in K else c[w]) for w in c}
    out=[]
    for tag,(K,pair,apex) in (("c'",('K2',(D,ga),0)),("c''",('K0',(D,be),2))):
        cs,ix=comps(adj,col,set(pair),x)
        K=cs[ix[2 if tag=="c'" else 0]]; c0=sw(col,K,*pair)
        Dp=c0[apex]
        free=[(a,b) for a in range(4) for b in range(a+1,4) if Dp not in (a,b)]
        def good(c):  # apex chain broken or 3-coloured ring
            if len({c[r] for r in range(5)})<4: return True
            for k in range(4):
                if k==Dp: continue
                cs2,ix2=comps(adj,c,{Dp,k},x)
                if not any(c[w]==k and ix2[w]==ix2[apex] for w in range(5) if w!=apex): return True
            return False
        key=lambda c:canon(c)
        start=c0; seen={key(c0):0}; q=deque([c0]); E=set(); dist_good=None; deg={}
        while q:
            c=q.popleft(); d=seen[key(c)]
            if dist_good is None and good(c): dist_good=d
            nb=set()
            for (a,b) in free:
                cs2,_=comps(adj,c,{a,b},x)
                for K2_ in cs2:
                    c2=sw(c,K2_,a,b)
                    if key(c2)==key(c): continue
                    nb.add(key(c2))
                    if key(c2) not in seen: seen[key(c2)]=d+1; q.append(c2)
            deg[key(c)]=len(nb)
            for k2 in nb: E.add(frozenset((key(c),k2)))
        out.append((tag,len(seen),len(E),sorted(deg.values()),dist_good))
    return out
for line in open('../MathNDiscSearch/res_23.txt'):
    if 'DISC' in line:
        l=line[line.index('DISC'):].strip(); print(l[:15],analyse(l))
