from tilley import *
from collections import Counter
def edge_scan(name,adj):
    verts=list(adj); order=verts
    res=[]
    for x in verts:
        for y in adj[x]:
            if y<x: continue
            # colourings of T-xy with c(x)=c(y): colour T/xy, i.e. colourings of T-x with y's colour absent from N(x)-{y}
            others=[u for u in verts if u!=x]
            locked_all=True; ncl=0; nl=0; memo={}
            for s in colourings(adj,others):
                if any(s[w]==s[y] for w in adj[x] if w!=y): continue
                col=dict(s); col[x]=s[y]
                k=canon(col,order)
                if k in memo: continue
                lk,sz=tilley_class(adj,col,x,y,order,memo)
                ncl+=1; nl+=lk
                if not lk: locked_all=False
            res.append((x,y,len(adj[x]),len(adj[y]),ncl,nl,locked_all))
    tot=len(res); wl=[r for r in res if r[6]]; cl=[r for r in res if r[5]>0]
    print(name,"edges",tot,"whole-edge Kempe-locked",len(wl),wl[:5],"edges with >=1 locked class",len(cl),
          "deg pairs of class-locked edges",Counter((min(r[2],r[3]),max(r[2],r[3])) for r in cl))
for name,adj in [("A_3",A(3)),("T4",from_faces(T4F)),("W6",from_rot(json.load(open(CERT+"W6.json"))["rot"]))]:
    edge_scan(name,adj)
# T4 locked classes at v=4 detail
adj=from_faces(T4F); v=4; X=link_cycle(adj,v); others=[u for u in adj if u!=v]; order=[v]+others
for i in range(5):
    memo={}; classes={}
    for s in colourings(adj,others):
        lc=[s[x] for x in X]
        if lc.count(lc[i])!=1: continue
        col=dict(s); col[v]=lc[i]; k=canon(col,order)
        if k in memo: continue
        before=set(memo); lk,sz=tilley_class(adj,col,v,X[i],order,memo)
        if lk:
            Tm=[u for u in adj if u!=v]
            print("T4 edge",(v,X[i]),"locked class size",sz,"T-v class sizes",sorted(Counter(s[u] for u in Tm).values()),"link word",canon({j:lc[j] for j in range(5)},range(5)))
