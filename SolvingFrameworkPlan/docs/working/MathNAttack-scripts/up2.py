import sys, subprocess
from nlab import *
def kneighbors(G,n,st):
    out=[]
    for a,b in PAIRS:
        done=set()
        for s in range(n):
            if st[s] not in (a,b) or s in done: continue
            comp={s}; stk=[s]
            while stk:
                u=stk.pop()
                for w in G[u]:
                    if w not in comp and st[w] in (a,b): comp.add(w); stk.append(w)
            done|=comp
            nc=list(st)
            for w in comp: nc[w]=b if st[w]==a else a
            out.append((a,b,frozenset(comp),tuple(nc)))
    return out
def canon(st):
    m={}; return tuple(m.setdefault(v,len(m)) for v in st)
P=sys.argv[1]; x=int(sys.argv[2]); which=int(sys.argv[3]); import collections
line=subprocess.run([P,"-m5","17","-a"],capture_output=True,text=True).stdout.splitlines()[1]
rot=parse(line); n=len(rot); adj=[set(r) for r in rot]; ring=rot[x]
states=[]
for col in colourings_minus(adj,n,x):
    cl=classify(adj,x,ring,col)
    if cl is None: continue
    u,(D,al,be,ga)=cl
    pi=pair_info(adj,col,x); key=lambda p,q:(min(p,q),max(p,q))
    vec=(pi[key(D,al)],pi[key(D,be)],pi[key(D,ga)],pi[key(al,be)],pi[key(al,ga)],pi[key(be,ga)])
    if vec!=((1,0),(2,0),(2,0),(1,0),(1,0),(1,0)): continue
    if not all(not class_in_G(adj,n,x,u[j],col)[0] for j in (1,3,4)): continue
    states.append((col,u,(D,al,be,ga)))
col,u,(D,al,be,ga)=states[which]
csg,idg=comps(adj,col,{D,ga},x); K2=csg[idg[u[2]]]
csb,idb=comps(adj,col,{D,be},x); K0=csb[idb[u[0]]]
print("state",which,"u",u,"cols D a b g",D,al,be,ga,"K2",sorted(K2),"K0",sorted(K0))
print("colouring",{v:col[v] for v in sorted(col)})
def firstbroken(st,y):
    s=st[y]
    cs={}
    for k in set(range(4))-{s}:
        col2={v:st[v] for v in range(n) if v!=x}
        cs_,idx=comps(adj,col2,{s,k},x)
        if not any(st[w]==k and idx[w]==idx[y] for w in ring if w!=y): return True
    return False
for name,K,pr,yj in (("nu_gamma",K2,(D,ga),0),("nu_beta",K0,(D,be),2)):
    c2=swap_comp(col,K,*pr); y=u[yj]
    G=[set(a) for a in adj]; G[x].discard(y); G[y].discard(x)
    c0=dict(c2); c0[x]=c2[y]
    st0=tuple(c0[v] for v in range(n))
    # BFS storing all parents
    dist={canon(st0):0}; sts={canon(st0):st0}; par={canon(st0):[]}; q=deque([canon(st0)])
    target=[]
    while q:
        k=q.popleft(); st=sts[k]
        if st[x]!=st[y] or firstbroken(st,y):
            target.append(k); continue
        for a,b,K_,nc in kneighbors(G,n,st):
            kk=canon(nc)
            if kk not in dist:
                dist[kk]=dist[k]+1; sts[kk]=nc; par[kk]=[(k,a,b,K_)]; q.append(kk)
            elif dist[kk]==dist[k]+1: par[kk].append((k,a,b,K_))
    best=min(dist[k] for k in target)
    print(name,"unlock apex u%d"%yj,"first-order-broken or separated at depth",best)
    nm={D:'D',al:'a',be:'b',ga:'g'}
    # print one path per target at best depth
    def paths(k):
        if dist[k]==0: return [[]]
        out=[]
        for (pk,a,b,K_) in par[k]:
            for p in paths(pk): out.append(p+[(pk,a,b,K_)])
        return out
    summ=collections.Counter()
    for k in [t for t in target if dist[t]==best]:
        for p in paths(k):
            s=sts[canon(st0)]
            desc=[]
            cur=st0
            for (pk,a,b,K_) in p:
                desc.append((nm[a]+nm[b], len(K_), tuple(sorted(i for i in range(5) if u[i] in K_))))
            summ[tuple(desc)]+=1
    for d,cn in sorted(summ.items()): print('   ',cn,d)
