import itertools,sys,time
from collections import deque,Counter
def load(path):
    out=[]
    for l in open(path):
        if not l.startswith('G'): continue
        t=l.split(); nf=int(t[3]); f=list(map(int,t[4:4+3*nf])); F=[tuple(f[3*i:3*i+3]) for i in range(nf)]
        adj={}
        for x in F:
            for a,b in itertools.combinations(x,2): adj.setdefault(a,set()).add(b);adj.setdefault(b,set()).add(a)
        out.append(adj)
    return out
def hole(adj,v):
    nbv=list(adj[v]); cyc=[nbv[0]]
    while len(cyc)<5:
        for w in adj[cyc[-1]]:
            if w in nbv and w not in cyc: cyc.append(w);break
    link=cyc
    V=[u for u in adj if u!=v]; idx={u:i for i,u in enumerate(V)}; Ad={u:[w for w in adj[u] if w!=v] for u in V}
    def canon(t):
        m={};o=[]
        for x in t:
            if x not in m:m[x]=len(m)
            o.append(m[x])
        return tuple(o)
    S=set()
    def rec(k,c,m):
        if k==len(V): S.add(canon(tuple(c[u] for u in V)));return
        u=V[k]
        for x in range(min(m+1,4)):
            if all(c.get(w)!=x for w in Ad[u]):
                c[u]=x;rec(k+1,c,max(m,x+1));del c[u]
    rec(0,{},0)
    def nb(t):
        out=set()
        for p,q in itertools.combinations(range(4),2):
            seen=set()
            for u in V:
                if t[idx[u]] in(p,q) and u not in seen:
                    comp=[u];seen.add(u);st=[u]
                    while st:
                        x=st.pop()
                        for y in Ad[x]:
                            if t[idx[y]] in(p,q) and y not in seen: seen.add(y);comp.append(y);st.append(y)
                    d=list(t)
                    for x in comp:d[idx[x]]=q if t[idx[x]]==p else p
                    out.add(canon(d))
        return out
    filled=lambda t: len({t[idx[x]] for x in link})<=3
    dist={t:0 for t in S if filled(t)}; dq=deque(dist)
    while dq:
        x=dq.popleft()
        for y in nb(x):
            if y not in dist: dist[y]=dist[x]+1;dq.append(y)
    res=[]
    for j in range(5):
        xj=link[j]
        if link[(j+2)%5] in adj[xj] or link[(j+3)%5] in adj[xj]: res.append(None); continue   # illegal fan
        adm=[t for t in S if all(t[idx[xj]]!=t[idx[link[k]]] for k in range(5) if k!=j)]
        res.append(max(dist[t] for t in adm) if adm else 0)
    return res
tab=Counter(); worst=[]
t0=time.time()
for path in sys.argv[1:]:
    for gi,adj in enumerate(load(path)):
        for v in adj:
            if len(adj[v])!=5: continue
            r=hole(adj,v)
            legal=[x for x in r if x is not None]
            if not legal: tab['no_legal_fan']+=1; continue
            best=min(legal); tab[('best_fan_max_radius',best)]+=1
            if best>=2: worst.append((path.split('/')[-1],gi,v,r))
        if time.time()-t0>500: break
print(sorted((str(k),c) for k,c in tab.items()))
print("holes whose best fan still has max admitted radius >=2:",len(worst),worst[:6])
