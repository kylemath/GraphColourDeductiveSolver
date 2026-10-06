import itertools,random,sys
from collections import deque,Counter
def A(r):
    F=[];ring=lambda k,i:1+5*k+(i%5);top=1+5*r
    for i in range(5): F.append((0,ring(0,i),ring(0,i+1)))
    for k in range(r-1):
        for i in range(5):
            F.append((ring(k,i),ring(k+1,i),ring(k,i+1)));F.append((ring(k+1,i),ring(k+1,i+1),ring(k,i+1)))
    for i in range(5): F.append((top,ring(r-1,i+1),ring(r-1,i)))
    return [tuple(f) for f in F]
def adjof(F):
    adj={}
    for f in F:
        for a,b in itertools.combinations(f,2): adj.setdefault(a,set()).add(b);adj.setdefault(b,set()).add(a)
    return adj
def flip(adj,rng):
    # edge flip on adjacency using common neighbours (triangulation): edge uv with exactly two common nbrs a,b forming faces
    es=[(u,w) for u in adj for w in adj[u] if u<w]; rng.shuffle(es)
    for u,w in es:
        com=adj[u]&adj[w]
        # faces uwa uwb exist iff a,b are the two common neighbours that form faces; separating triangles give >2 common
        if len(com)!=2: continue
        a,b=tuple(com)
        if b in adj[a]: continue
        if len(adj[u])<=5 or len(adj[w])<=5: continue
        new={k:set(v) for k,v in adj.items()}
        new[u].discard(w);new[w].discard(u);new[a].add(b);new[b].add(a)
        if min(len(x) for x in new.values())>=5: return new
    return None
def radii(adj,v):
    link_nb=sorted(adj[v]); cyc=[link_nb[0]]
    while len(cyc)<5:
        for w in adj[cyc[-1]]:
            if w in link_nb and w not in cyc: cyc.append(w);break
    link=cyc
    if not all(link[(i+1)%5] in adj[link[i]] for i in range(5)): return None
    V=[u for u in adj if u!=v]; idx={u:i for i,u in enumerate(V)}; Ad={u:[w for w in adj[u] if w!=v] for u in V}
    def canon(t):
        m={};o=[]
        for x in t:
            if x not in m:m[x]=len(m)
            o.append(m[x])
        return tuple(o)
    S=set()
    sys.setrecursionlimit(10000)
    def rec(k,c,m):
        if k==len(V): S.add(tuple(c[u] for u in V));return
        u=V[k]
        for x in range(min(m+1,4)):
            if all(c.get(w)!=x for w in Ad[u]):
                c[u]=x;rec(k+1,c,max(m,x+1));del c[u]
    rec(0,{},0)
    if len(S)>400000: return None
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
    def path(t,s,e,pq):
        seen={s};st=[s]
        while st:
            x=st.pop()
            if x==e:return True
            for y in Ad[x]:
                if y not in seen and t[idx[y]] in pq: seen.add(y);st.append(y)
        return False
    def dl(t):
        cs=[t[idx[x]] for x in link]
        if len(set(cs))<4: return False
        j=[j for j in range(5) if cs[j]==cs[(j+2)%5]][0];x=[link[(j+i)%5] for i in range(5)]
        return path(t,x[1],x[3],{t[idx[x[1]]],t[idx[x[3]]]}) and path(t,x[1],x[4],{t[idx[x[1]]],t[idx[x[4]]]})
    S={canon(t) for t in S}
    dist={t:0 for t in S if filled(t)}; dq=deque(dist)
    while dq:
        x=dq.popleft()
        for y in nb(x):
            if y not in dist: dist[y]=dist[x]+1;dq.append(y)
    return Counter(dist.get(t,-1) for t in S if dl(t))
rng=random.Random(2026100601)
tot=Counter();graphs=0;holes=0;worst=0;viol=[]
import time;t0=time.time()
for r in (3,4):
    for rep in range(14):
        adj=adjof(A(r))
        for _ in range(rng.randint(1,12)):
            nw=flip(adj,rng)
            if nw: adj=nw
        graphs+=1
        for v in adj:
            if len(adj[v])==5 and all(len(adj[w])==5 for w in adj[v]):
                res=radii(adj,v)
                if res is None: continue
                holes+=1; tot.update(res)
                m=max(res) if res else 0
                if -1 in res or m>3: viol.append((r,rep,v,dict(res)))
        if time.time()-t0>420: break
print("graphs",graphs,"icosahedral holes tested",holes,"radius histogram over doubly locked states",dict(sorted(tot.items())),"violations (radius>3 or targetless)",viol)
