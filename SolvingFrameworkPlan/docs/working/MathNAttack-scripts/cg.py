import sys, subprocess
from nlab import *
def kneighbors(G,n,st,skipx=None):
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
P=sys.argv[1]; x=int(sys.argv[2])
line=subprocess.run([P,"-m5","17","-a"],capture_output=True,text=True).stdout.splitlines()[1]
rot=parse(line); n=len(rot); adj=[set(r) for r in rot]
ring=rot[x]
def describe(st):
    col={v:st[v] for v in range(n) if v!=x}
    pi=pair_info(adj,col,x)
    return ''.join(str(pi[p][0])+(('c%d'%pi[p][1]) if pi[p][1] else '') +',' for p in PAIRS)
# find states A: all rigid triply locked at x
states=[]
for col in colourings_minus(adj,n,x):
    cl=classify(adj,x,ring,col)
    if cl is None: continue
    u,(D,al,be,ga)=cl
    pi=pair_info(adj,col,x); key=lambda p,q:(min(p,q),max(p,q))
    vec=(pi[key(D,al)],pi[key(D,be)],pi[key(D,ga)],pi[key(al,be)],pi[key(al,ga)],pi[key(be,ga)])
    if vec!=((1,0),(2,0),(2,0),(1,0),(1,0),(1,0)): continue
    if not all(not class_in_G(adj,n,x,u[j],col)[0] for j in (1,3,4)): continue
    states.append((col,u))
print(len(states),"rigid states at x=",x)
canonset={}
for i,(col,u) in enumerate(states):
    st=tuple(col.get(v,col[u[1]]) for v in range(n)) # x coloured as u1 (alpha)
    canonset[canon(tuple(col[v] if v!=x else -1 for v in range(n)))]=i
col,u=states[0]
for j in (1,3,4):
    y=u[j]
    G=[set(a) for a in adj]; G[x].discard(y); G[y].discard(x)
    c0=dict(col); c0[x]=col[y]
    st0=tuple(c0[v] for v in range(n))
    seen={canon(st0):st0}; q=deque([st0]); 
    while q:
        st=q.popleft()
        for a,b,K,nc in kneighbors(G,n,st):
            k=canon(nc)
            if k not in seen: seen[k]=nc; q.append(nc)
    print("fan u%d class %d:"%(j,len(seen)))
    for k,st in seen.items():
        ck=canon(tuple(st[v] if v!=x else -1 for v in range(n)))
        tag = "RIGID#%d"%canonset[ck] if ck in canonset else ""
        print("   ring word",[st[v] for v in ring],"x",st[x],describe(st),tag)

print("---- class graph per fan (edges = one component swap), nodes numbered")
for j in (1,3,4):
    y=u[j]
    G=[set(a) for a in adj]; G[x].discard(y); G[y].discard(x)
    c0=dict(col); c0[x]=col[y]
    st0=tuple(c0[v] for v in range(n))
    seen={canon(st0):0}; sts=[st0]; q=deque([st0]); E=set()
    while q:
        st=q.popleft(); i=seen[canon(st)]
        for a,b,K,nc in kneighbors(G,n,st):
            k=canon(nc)
            if k not in seen: seen[k]=len(sts); sts.append(nc); q.append(nc)
            j2=seen[k]
            if j2!=i: E.add((min(i,j2),max(i,j2),(('x' if x in K else '')+str(len(K)))))
    print("fan u%d"%j, sorted(E))
    for i,st in enumerate(sts):
        ck=canon(tuple(st[v] if v!=x else -1 for v in range(n)))
        print("   node",i,[st[v] for v in ring],describe(st),"RIGID#%d"%canonset[ck] if ck in canonset else "")
