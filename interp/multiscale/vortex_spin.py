import numpy as np, collections, random
from scipy.spatial import ConvexHull
from pysat.solvers import Minisat22
def sphere(n,seed):
    rng=np.random.default_rng(seed); p=rng.normal(size=(n,3)); p/=np.linalg.norm(p,axis=1)[:,None]
    h=ConvexHull(p); adj=[set() for _ in range(n)]
    for a,b,c in h.simplices.tolist(): adj[a]|={b,c}; adj[b]|={a,c}; adj[c]|={a,b}
    return p,adj
def rotation(p,adj,v):
    n=p[v]; t1=np.cross(n,[1,0,0] if abs(n[0])<.9 else [0,1,0]); t1/=np.linalg.norm(t1); t2=np.cross(n,t1)
    return sorted(adj[v],key=lambda u: np.arctan2(np.dot(p[u]-p[v],t2),np.dot(p[u]-p[v],t1)))
def colour(adj,seed):
    n=len(adj); s=Minisat22(); var=lambda v,c:4*v+c+1; rng=random.Random(seed)
    for v in range(n):
        s.add_clause([var(v,c) for c in range(4)])
        for u in adj[v]:
            if u>v:
                for c in range(4): s.add_clause([-var(v,c),-var(u,c)])
    ass=[]
    for v in rng.sample(range(n),n//4):
        a=var(v,rng.randrange(4))
        if s.solve(assumptions=ass+[a]): ass.append(a)
    s.solve(assumptions=ass); m=set(x for x in s.get_model() if x>0)
    return [next(c for c in range(4) if var(v,c) in m) for v in range(n)]
# labels: colours as Z2^2 ints 0..3, label = c(v)^c(w) in {1,2,3}; cyclic order 1->2->3->1 = forward
def winding(col,rot,v):
    L=[col[v]^col[u] for u in rot]; f=b=0
    for i in range(len(L)):
        a,c=L[i],L[(i+1)%len(L)]
        if c==a%3+1: f+=1
        else: b+=1
    assert (f-b)%3==0
    return (f-b)//3
for seed in range(3):
    p,adj=sphere(2000,seed); rot=[rotation(p,adj,v) for v in range(len(adj))]
    for cs in range(2):
        col=colour(adj,cs); assert all(col[v]!=col[u] for v in range(len(adj)) for u in adj[v])
        W=[winding(col,rot[v],v) for v in range(len(adj))]
        bydeg=collections.defaultdict(collections.Counter)
        for v,w in enumerate(W): bydeg[len(adj[v])][w]+=1
        percol=collections.Counter()
        for v,w in enumerate(W): percol[col[v]]+=w
        print('map',seed,'col',cs,'sum winding',sum(W),'per colour class',dict(sorted(percol.items())),'sum|w|',sum(map(abs,W)))
        if seed==0 and cs==0:
            for d in sorted(bydeg): print('   deg',d,dict(sorted(bydeg[d].items())))
