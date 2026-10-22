import numpy as np, random, itertools, collections, sys, json
from scipy.spatial import ConvexHull
from pysat.solvers import Minisat22
PERMS=list(itertools.permutations(range(4)))
def sphere_tri(n,seed):
    rng=np.random.default_rng(seed); p=rng.normal(size=(n,3)); p/=np.linalg.norm(p,axis=1)[:,None]
    h=ConvexHull(p); adj=[set() for _ in range(n)]
    for a,b,c in h.simplices:
        adj[a]|={b,c}; adj[b]|={a,c}; adj[c]|={a,b}
    return adj
REF={}
def icosphere(f):
    REF.clear()
    t=(1+5**.5)/2
    V=[(-1,t,0),(1,t,0),(-1,-t,0),(1,-t,0),(0,-1,t),(0,1,t),(0,-1,-t),(0,1,-t),(t,0,-1),(t,0,1),(-t,0,-1),(-t,0,1)]
    F=[(0,11,5),(0,5,1),(0,1,7),(0,7,10),(0,10,11),(1,5,9),(5,11,4),(11,10,2),(10,7,6),(7,1,8),(3,9,4),(3,4,2),(3,2,6),(3,6,8),(3,8,9),(4,9,5),(2,4,11),(6,2,10),(8,6,7),(9,8,1)]
    V=[np.array(v,float) for v in V]; idx={}
    def pt(i,j,a):
        key=(min(i,j),max(i,j),a if i<j else f-a)
        if a==0: return i
        if a==f: return j
        if key not in idx: V.append(V[i]*(1-a/f)+V[j]*(a/f)); idx[key]=len(V)-1
        return idx[key]
    tris=[]
    for (A,B,C) in F:
        grid={}
        for i in range(f+1):
            for j in range(f+1-i):
                k=f-i-j
                P=V[A]*i/f+V[B]*j/f+V[C]*k/f
                key=('f',A,B,C,i,j)
                # vertices on edges must be shared: use canonical keys
                if i==f: grid[i,j]=A
                elif j==f: grid[i,j]=B
                elif k==f: grid[i,j]=C
                elif k==0: grid[i,j]=pt(A,B,j)
                elif j==0: grid[i,j]=pt(A,C,k)
                elif i==0: grid[i,j]=pt(B,C,k)
                else: V.append(P); grid[i,j]=len(V)-1
                REF.setdefault(grid[i,j],(i+2*j)%3)
        for i in range(f):
            for j in range(f-i):
                tris.append((grid[i,j],grid[i+1,j],grid[i,j+1]))
                if i+j<f-1: tris.append((grid[i+1,j],grid[i+1,j+1],grid[i,j+1]))
    adj=[set() for _ in V]
    for a,b,c in tris: adj[a]|={b,c}; adj[b]|={a,c}; adj[c]|={a,b}
    return adj
def hierarchy(adj,rng):
    n=len(adj); lab=list(range(n)); levels=[[ [v] for v in range(n)]]
    while len(levels[-1])>1:
        cl=levels[-1]; cid={}
        for i,c in enumerate(cl):
            for v in c: cid[v]=i
        Q=[set() for _ in cl]
        for v in range(n):
            for u in adj[v]:
                if cid[u]!=cid[v]: Q[cid[v]].add(cid[u])
        order=list(range(len(cl))); rng.shuffle(order); own=[-1]*len(cl); new=[]
        for i in order:
            if own[i]>=0: continue
            grp=[i]+[j for j in Q[i] if own[j]<0]
            for j in grp: own[j]=len(new)
            new.append(grp)
        levels.append([sum((cl[j] for j in g),[]) for g in new])
        levels[-1+0]  # keep
        levels[-1]=[c for c in levels[-1]]
        levels[-1+0]=levels[-1]
        levels[-2] and None
        levels[-1]=levels[-1]
        levels[-1]=levels[-1]
        levels[-1]=levels[-1]
        levels.append(None); levels.pop()
        levels[-1]=levels[-1]
        levels[-1]=levels[-1]
        # store children grouping
        levels[-1]=[c for c in levels[-1]]
        groups.append(new)
    return levels
groups=[]
BUDGET=200000
TIMEOUTS=[0]
def solve_free(adj,col,free,pref=None):
    fl=sorted(free); ix={v:i for i,v in enumerate(fl)}; s=Minisat22()
    var=lambda v,c: ix[v]*4+c+1
    for v in fl:
        s.add_clause([var(v,c) for c in range(4)])
        for u in adj[v]:
            if u in ix and u>v:
                for c in range(4): s.add_clause([-var(v,c),-var(u,c)])
            elif u not in ix and col.get(u) is not None:
                s.add_clause([-var(v,col[u])])
    if pref: s.set_phases([var(v,pref[v]) for v in fl if v in pref])

    s.conf_budget(BUDGET); st=s.solve_limited()
    if st is None: TIMEOUTS[0]+=1
    if not st: return None
    m=set(x for x in s.get_model() if x>0)
    return {v:next(c for c in range(4) if var(v,c) in m) for v in fl}
def run(adj,seed,ref=None):
    rng=random.Random(seed); groups.clear(); levels=hierarchy(adj,rng)
    col={v:(ref[v] if ref else 0) for v in range(len(adj))}; stats=[]
    for L in range(1,len(levels)):
        prev=levels[L-1]
        for g,parent in zip(groups[L-1],levels[L]):
            P=set(parent)
            kids=[prev[j] for j in g]; kid_of={v:k for k,c in enumerate(kids) for v in c}
            # greedy permutation choice
            perm=[PERMS[0]]*len(kids)
            def conflicts():
                return [(v,u) for v in parent for u in adj[v] if u in P and u>v and kid_of[u]!=kid_of[v] and perm[kid_of[v]][col[v]]==perm[kid_of[u]][col[u]]]
            for _ in range(3):
                for k in range(1,len(kids)):
                    best=None
                    for p in PERMS:
                        perm[k]=p; c=len(conflicts())
                        if best is None or c<best[0]: best=(c,p)
                    perm[k]=best[1]
            for v in parent: col[v]=perm[kid_of[v]][col[v]]
            conf=[(v,u) for v in parent for u in adj[v] if u in P and u>v and col[u]==col[v]]
            if not conf: stats.append((L,len(parent),0,0,0)); continue
            # BFS distance inside parent from conflict endpoints
            dist={}; frontier=set(x for e in conf for x in e)
            for x in frontier: dist[x]=0
            d=0; R=None
            sub={v:col[v] for v in parent}
            pref=None
            if ref:
                bp=max(PERMS,key=lambda p:sum(col[v]==p[ref[v]] for v in parent))
                pref={v:bp[ref[v]] for v in parent}
            while True:
                free={v for v in dist if dist[v]<=d}
                fixed={v:col[v] for v in parent if v not in free}
                sol=solve_free({v:[u for u in adj[v] if u in P] for v in parent},fixed,free,pref)
                if sol: 
                    for v,c in sol.items(): col[v]=c
                    R=d; break
                d+=1; new=set()
                for v in list(dist):
                    if dist[v]==d-1:
                        for u in adj[v]:
                            if u in P and u not in dist: dist[u]=d; new.add(u)
                if not new and len(dist)==len(P): pass
            stats.append((L,len(parent),len(conf),R,len(free)))
            print('   merge L%d size %d conflicts %d R=%d timeouts_so_far=%d'%(L,len(parent),len(conf),R,TIMEOUTS[0]),flush=True)
    # verify
    assert all(col[v]!=col[u] for v in range(len(adj)) for u in adj[v])
    return stats

def flatness(col,ref,adj):
    # fraction of vertices whose colour equals the best permutation of ref on its radius-3 ball (local flatness proxy)
    import random as _r
    rr=_r.Random(1); n=len(adj); good=0; S=400
    for _ in range(S):
        v=rr.randrange(n); ball={v}; fr={v}
        for _ in range(3):
            fr={u for x in fr for u in adj[x]}-ball; ball|=fr
        if any(u not in ref for u in ball): S-=1; continue
        bp=max(PERMS,key=lambda p:sum(col[u]==p[ref[u]] for u in ball))
        good+= all(col[u]==bp[ref[u]] for u in ball)
    return good/max(S,1)
if __name__=='__main__':
    import time
    f=int(sys.argv[1]); mode=sys.argv[2]; seed=int(sys.argv[3])
    adj=icosphere(f); ref=dict(REF) if mode=='tilt' else None
    t=time.time(); st=run(adj,seed,ref)
    byL=collections.defaultdict(list)
    for L,sz,nc,R,nf in st: byL[L].append((sz,nc,R))
    print('ico%d n=%d mode=%s seed=%d time=%.0fs'%(f,len(adj),mode,seed,time.time()-t))
    for L in sorted(byL):
        v=byL[L]; Rs=[x[2] for x in v if x[1]>0]
        print('  L%2d clusters %4d meanSize %7.1f withConflicts %4d R: %s'%(L,len(v),np.mean([x[0] for x in v]),len(Rs),dict(sorted(collections.Counter(Rs).items()))))
