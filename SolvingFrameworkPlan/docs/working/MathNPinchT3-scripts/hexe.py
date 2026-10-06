import sys, subprocess
from collections import deque
from nlab import *
P="/private/tmp/planemap-next/plantri58/plantri"
line=subprocess.run([P,"-m5","17","-a"],capture_output=True,text=True).stdout.splitlines()[1]
rot=parse(line); n=len(rot); adj=[set(r) for r in rot]
def canon(c):
    m={}; return tuple(m.setdefault(c[v],len(m)) for v in sorted(c))
x=5; ring=rot[x]
for col in colourings_minus(adj,n,x):
    cl=classify(adj,x,ring,col)
    if cl is None: continue
    u,(D,al,be,ga)=cl
    pi=pair_info(adj,col,x); key=lambda p,q:(min(p,q),max(p,q))
    vec=(pi[key(D,al)],pi[key(D,be)],pi[key(D,ga)],pi[key(al,be)],pi[key(al,ga)],pi[key(be,ga)])
    if vec!=((1,0),(2,0),(2,0),(1,0),(1,0),(1,0)): continue
    if not all(not class_in_G(adj,n,x,uj,col)[0] for uj in [None] ) if False else False: pass
    if not all(not class_in_G(adj,n,x,u[j],col)[0] for j in (1,3,4)): continue
    csg,idg=comps(adj,col,{D,ga},x); K2=csg[idg[u[2]]]
    c1=swap_comp(col,K2,D,ga); y=u[0]; s=c1[y]
    dist={canon(c1):0}; rep={canon(c1):c1}; q=deque([c1]); g={}
    while q:
        cc=q.popleft(); k0=canon(cc); g[k0]=set()
        for a,b in PAIRS:
            if s in (a,b): continue
            cs,idx=comps(adj,cc,{a,b},x)
            for K_ in cs:
                c2=swap_comp(cc,K_,a,b); k=canon(c2)
                if k==k0: continue
                g[k0].add(k)
                if k not in dist: dist[k]=dist[k0]+1; rep[k]=c2; q.append(c2)
    ids={k:i for i,k in enumerate(sorted(dist,key=lambda k:dist[k]))}
    nmcol={}
    for k,cc in sorted(rep.items(),key=lambda kv:ids[kv[0]]):
        word=[cc[w] for w in u]   # u0..u4 aligned
        # name colours by roles at this node: doubled -> 'P', others by first appearance letters
        names={}; letters='DABC'
        for c_ in [cc[u[0]]]+[cc[w] for w in u[1:]]:
            if c_ not in names: names[c_]=letters[len(names)]
        w=''.join(names[c] for c in word)
        for kx in range(4):
            if kx not in names: names[kx]='ABCD'[len(names)] if len(names)<4 else '?'
        pp=pair_info(adj,cc,x)
        d=' '.join(f"{names[a]}{names[b]}:{v[0]}/{v[1]}" for (a,b),v in sorted(pp.items(),key=lambda t:(names[t[0][0]]+names[t[0][1]])) )
        bro=[]
        for kk in range(4):
            if kk==s: continue
            cs,idx=comps(adj,cc,{s,kk},x)
            if not any(cc[w_]==kk and idx[w_]==idx[y] for w_ in ring if w_!=y): bro.append(names[kk])
        print(ids[k],"dist",dist[k],"ringword(u0..u4)",w,d,"broken chains:",bro,"nbrs",sorted(ids[b] for b in g[k]))
