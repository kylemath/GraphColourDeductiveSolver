import sys, subprocess
from nlab import *
def full_class(adj,n,x,y,col):
    G=[set(a) for a in adj]; G[x].discard(y); G[y].discard(x)
    c0=dict(col); c0[x]=col[y]
    def canon(st):
        m={}; return tuple(m.setdefault(v,len(m)) for v in st)
    start=tuple(c0[v] for v in range(n))
    seen={canon(start):start}; q=deque([start]); edges=[]
    while q:
        st=q.popleft()
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
                k=canon(nc)
                if k not in seen: seen[k]=tuple(nc); q.append(tuple(nc))
    return seen
P=sys.argv[1]
gi=1
line=subprocess.run([P,"-m5","17","-a"],capture_output=True,text=True).stdout.splitlines()[gi]
rot=parse(line); n=len(rot); adj=[set(r) for r in rot]
x=5; ring=rot[x]
for col in colourings_minus(adj,n,x):
    cl=classify(adj,x,ring,col)
    if cl is None: continue
    u,(D,al,be,ga)=cl
    pi=pair_info(adj,col,x)
    key=lambda p,q:(min(p,q),max(p,q))
    vec=(pi[key(D,al)],pi[key(D,be)],pi[key(D,ga)],pi[key(al,be)],pi[key(al,ga)],pi[key(be,ga)])
    if vec!=((1,0),(2,0),(2,0),(1,0),(1,0),(1,0)): continue
    if not all(not class_in_G(adj,n,x,u[j],col)[0] for j in (1,3,4)): continue
    print("state ring",u,"cols",(D,al,be,ga))
    print(" colouring", [col[v] if v!=x else '-' for v in range(n)])
    for j in (1,3,4,0,2):
        cl2=full_class(adj,n,x,u[j],col) if j in (1,3,4) else None
        if cl2: print(" fan u%d class size %d"%(j,len(cl2)))
    c1=swap_comp(col,comps(adj,col,{D,ga},x)[0][comps(adj,col,{D,ga},x)[1][u[2]]],D,ga)
    cl0=full_class(adj,n,x,u[0],c1)
    print(" nu_gamma class at u0 size",len(cl0), " members' separations:",sum(1 for s in cl0.values() if s[x]!=s[u[0]]))
    # structure of the members: ring words
    for k,s in cl0.items():
        print("   ", [s[v] for v in ring], "x=",s[x])
    break
