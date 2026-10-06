import sys
sys.path.insert(0,'/Users/fulkanjou/GraphColour/SolvingFrameworkPlan/docs/working/MathNCaseI-scripts')
from tn_lib import *
from collections import deque
N='Dabg'
def sw(c,K,a,b): return {w:((b if c[w]==a else a) if w in K else c[w]) for w in c}
def canon(c):
    m={}; return tuple(m.setdefault(c[v],len(m)) for v in sorted(c))
def goodf(adj,x,c,apex):
    if len({c[r] for r in range(5)})<4: return True
    for k in range(4):
        if k==c[apex]: continue
        cs2,ix2=comps(adj,c,{c[apex],k},x)
        if not any(c[w]==k and ix2[w]==ix2[apex] for w in range(5) if w!=apex): return True
    return False
def pairinfo(adj,x,c,V,Dp):
    out=[]
    for a in range(4):
        for b in range(a+1,4):
            if Dp in (a,b): continue
            cs,ix=comps(adj,c,{a,b},x)
            nv=sum(len(K) for K in cs); ne=sum(1 for u in range(V) if c[u] in (a,b) for w in adj[u] if w<V and w>u and c[w] in (a,b))
            out.append((len(cs), len(cs)-(nv-ne)))  # comps, cyc
    return tuple(out)
def neighbours(adj,x,c,Dp):
    nb={}
    for a in range(4):
        for b in range(a+1,4):
            if Dp in (a,b): continue
            cs,_=comps(adj,c,{a,b},x)
            for K in cs:
                c2=sw(c,K,a,b); k=canon(c2)
                if k!=canon(c): nb[k]=c2
    return nb
def analyse(l,mir):
    cl,edges=parse(l); n,x,adj=build(cl,edges); V=n-1
    col={v:cl[v] for v in range(V)}; D,al,be,ga=0,1,2,3
    pair,ur,apex=((D,ga),2,0) if not mir else ((D,be),0,2)
    cs,ix=comps(adj,col,set(pair),x); K=cs[ix[ur]]; c0=sw(col,K,*pair)
    Dp=c0[apex]
    # full class
    seen={canon(c0):c0}; dist={canon(c0):0}; q=deque([c0]); deg={}; par={}
    while q:
        c=q.popleft(); kc=canon(c)
        nb=neighbours(adj,x,c,Dp); deg[kc]=len(nb)
        for k,c2 in nb.items():
            if k not in seen: seen[k]=c2; dist[k]=dist[kc]+1; par[k]=kc; q.append(c2)
    good={k for k,c in seen.items() if goodf(adj,x,c,apex)}
    return dict(size=len(seen),degs=sorted(deg.values()),good=sorted(dist[k] for k in good),
        info={k:(pairinfo(adj,x,seen[k],V,Dp),deg[k],dist[k],k in good) for k in seen}, c0=canon(c0), seen=seen,adj=adj,x=x,V=V,Dp=Dp,apex=apex,dist=dist)
if __name__=='__main__':
    D='/Users/fulkanjou/GraphColour/SolvingFrameworkPlan/docs/working/MathNDiscSearch/'
    for fn in ['res_23.txt','res2_24_p0.txt','res2_24_p1.txt','res2_24_p2.txt','res2_24_p3.txt']:
        for li,line in enumerate(open(D+fn)):
            if 'DISC' not in line: continue
            l=line[line.index('DISC'):].strip()
            for mir in (0,1):
                r=analyse(l,mir)
                i0=r['info'][r['c0']]
                print(fn[:9],li,mir,'size',r['size'],'good dists',r['good'][:6],'c0',i0[0],i0[1],'degs',''.join(map(str,r['degs'])))
