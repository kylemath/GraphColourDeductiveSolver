import sys,random,itertools,collections,numpy as np
src=open('/tmp/claude-0/ms/ms.py').read().split("if __name__=='__main__':")[0]; exec(src)
from pysat.solvers import Minisat22
def bfs(adj,srcs,allowed):
    d={s:0 for s in srcs}; q=list(srcs)
    for v in q:
        for u in adj[v]:
            if u in allowed and u not in d: d[u]=d[v]+1; q.append(u)
    return d
def random_col(adj,S,rng):
    S=sorted(S); ix={v:i for i,v in enumerate(S)}; s=Minisat22(); var=lambda v,c: ix[v]*4+c+1
    for v in S:
        s.add_clause([var(v,c) for c in range(4)])
        for u in adj[v]:
            if u in ix and u>v:
                for c in range(4): s.add_clause([-var(v,c),-var(u,c)])
    # random assumptions: try to fix random vertices to random colours
    ass=[]
    for v in rng.sample(S,len(S)//3):
        a=var(v,rng.randrange(4))
        if s.solve(assumptions=ass+[a]): ass.append(a)
    s.solve(assumptions=ass); m=set(x for x in s.get_model() if x>0)
    return {v:next(c for c in range(4) if var(v,c) in m) for v in S}
def kempe(adj,col,S,rng):
    v=rng.choice(sorted(S)); a=col[v]; b=rng.choice([c for c in range(4) if c!=a])
    G={x:[u for u in adj[x] if u in S and col[u] in (a,b)] for x in S}; ch=bfs(G,[v],S)
    for x in ch: col[x]=b if col[x]==a else a
def need_R(adj,U,colA,colB,maxR=12):
    best=None
    for p in PERMS:
        col=dict(colA); col.update({v:p[c] for v,c in colB.items()})
        conf={x for v in U for u in adj[v] if u in U and col[u]==col[v] for x in (u,v)}
        if not conf: return 0
        d=bfs(adj,conf,U)
        for R in range(0,maxR+1):
            if best is not None and R>=best: break
            free={v for v,dv in d.items() if dv<=R}
            fixed={v:col[v] for v in U if v not in free}
            if solve_free({v:[u for u in adj[v] if u in U] for v in U},fixed,free) is not None:
                best=R if best is None else min(best,R); break
    return best
def hunt(adj,center,rad,iters,rng):
    U=set(bfs(adj,[center],set(range(len(adj)))).keys()); U={v for v,dv in bfs(adj,[center],set(range(len(adj)))).items() if dv<=rad}
    s1,s2=rng.sample(sorted(U),2); d1=bfs(adj,[s1],U); d2=bfs(adj,[s2],U)
    A={v for v in U if d1.get(v,99)<=d2.get(v,99)}; B=U-A
    cA=random_col(adj,A,rng); cB=random_col(adj,B,rng); cur=need_R(adj,U,cA,cB); top=cur
    for it in range(iters):
        nA,nB=dict(cA),dict(cB)
        for _ in range(rng.randint(1,3)): kempe(adj,nA,A,rng) if rng.random()<.5 else kempe(adj,nB,B,rng)
        r=need_R(adj,U,nA,nB)
        if r>=cur: cA,cB,cur=nA,nB,r; top=max(top,r)
    return len(U),len(A),len(B),top
rng=random.Random(1)
graphs=[('ico17',icosphere(17)),('sphere3k',sphere_tri(3000,3))]
res=collections.Counter()
for name,adj in graphs:
    for trial in range(int(sys.argv[1])):
        c=rng.randrange(len(adj)); n,a,b,top=hunt(adj,c,int(sys.argv[2]),int(sys.argv[3]),rng); res[(name,top)]+=1
        print(name,'trial',trial,'|U|',n,'max R found',top,flush=True)
print(sorted(res.items()))
