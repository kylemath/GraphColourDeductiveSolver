# (c) single-vertex repair radius at degree-5 and degree-6 vertices of geodesic domes,
#     starting from non-adversarial colourings of G-v (SAT + random Kempe flips), compared with Kempe's procedure.
import sys, random, math, collections, itertools
from collections import deque
from pysat.solvers import Minisat22
MARK="if __name__=="+"'__main__':"
exec(open('ms_orig.py').read().split(MARK)[0])
E={1:(1,0),2:(-.5,math.sqrt(3)/2),3:(-.5,-math.sqrt(3)/2)}
def bfs(adj,src,R=None,banned=None):
    dist={s:0 for s in src}; dq=deque(src)
    while dq:
        x=dq.popleft()
        if R is not None and dist[x]==R: continue
        for w in adj[x]:
            if w not in dist and w!=banned: dist[w]=dist[x]+1; dq.append(w)
    return dist
def sat(adj,free,fixed,phase=None,rng=None,assume=()):
    fl=sorted(free); ix={v:i for i,v in enumerate(fl)}; s=Minisat22(); var=lambda v,c:ix[v]*4+c+1
    for v in fl:
        s.add_clause([var(v,c) for c in range(4)])
        for u in adj[v]:
            if u in ix:
                if u>v:
                    for c in range(4): s.add_clause([-var(v,c),-var(u,c)])
            elif u in fixed: s.add_clause([-var(v,fixed[u])])
    if rng: s.set_phases([var(v,rng.randrange(4)) for v in fl])
    ok=s.solve(assumptions=[var(v,c) for v,c in assume])
    if not ok: s.delete(); return None
    m=set(x for x in s.get_model() if x>0); s.delete()
    return {v:next(c for c in range(4) if var(v,c) in m) for v in fl}
def link_cycle(adj,v):
    L=list(adj[v]); cyc=[L[0]]; prev=None
    while len(cyc)<len(L):
        nxt=[u for u in adj[cyc[-1]] if u in adj[v] and u!=prev and u not in cyc]
        prev=cyc[-1]; cyc.append(nxt[0])
    return cyc
def monodromy(cyc,col):
    s=[0,0]
    for k in range(len(cyc)):
        lab=col[cyc[k]]^col[cyc[(k+1)%len(cyc)]]; sg=1 if k%2==0 else -1
        s[0]+=sg*E[lab][0]; s[1]+=sg*E[lab][1]
    return math.hypot(*s)
def kempe_chain(adj,col,start,a,b,v):
    comp={start}; st=[start]
    while st:
        x=st.pop()
        for y in adj[x]:
            if y!=v and y not in comp and col[y] in (a,b): comp.add(y); st.append(y)
    return comp
def kempe_procedure(adj,col,v,dv):
    """Kempe's argument at v (deg<=5). Returns (success, radius of recoloured set)."""
    cyc=link_cycle(adj,v); cs=[col[w] for w in cyc]
    if len(set(cs))<4: return True,0
    n=len(cyc)
    for i in range(n):
        for j in range(n):
            if i!=j and cs[i]!=cs[j] and cs.count(cs[i])==1:
                comp=kempe_chain(adj,col,cyc[i],cs[i],cs[j],v)
                if not any(cyc[k] in comp for k in range(n) if cs[k]==cs[j]):
                    return True,max(dv[x] for x in comp)
    # Kempe's double swap (can fail): repeated colour a at two positions
    a=[c for c in set(cs) if cs.count(c)==2]
    if not a: return False,None
    a=a[0]; pos=[k for k in range(n) if cs[k]==a]
    newc=dict(col); changed=set()
    for k in pos:
        others=[c for c in set(cs) if c!=a]
        for b in others:
            comp=kempe_chain(adj,newc,cyc[k],a,b,v)
            if not any(newc[cyc[m]]==b and cyc[m] in comp for m in range(n)):
                for x in comp: newc[x]= b if newc[x]==a else a
                changed|=comp; break
    ok=len(set(newc[w] for w in cyc))<4 and all(newc[x]!=newc[y] for x in changed for y in adj[x] if y!=v)
    return ok,(max(dv[x] for x in changed) if changed else None)
def local_minR(adj,col,v,Rmax):
    for R in range(Rmax+1):
        for cv in range(4):
            full=dict(col); full[v]=cv
            K=[v]+[w for w in adj[v] if full[w]==cv]
            if len(K)==1: return 0
            dist=bfs(adj,K,R)
            if sat(adj,set(dist),{u:full[u] for u in range(len(adj)) if u not in dist}) is not None: return R
    return None
def random_colouring(adj,v,rng,flips,assume=()):
    n=len(adj); free=set(range(n))-{v}
    col=sat({u:[w for w in adj[u] if w!=v] for u in range(n)},free,{},rng=rng,assume=assume)
    vs=sorted(free)
    for _ in range(flips):
        x=rng.choice(vs); a=col[x]; b=rng.choice([c for c in range(4) if c!=a])
        comp=kempe_chain(adj,col,x,a,b,v)
        for y in comp: col[y]=b if col[y]==a else a
    return col
if __name__=='__main__':
    rng=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 0)
    for f in [6,10,14,20,28]:
        adj=icosphere(f); n=len(adj)
        odd=[u for u in range(n) if len(adj[u])%2]
        v5=0
        # degree-6 vertex far from all degree-5 vertices: centre of an icosahedron face
        dodd=bfs(adj,odd); v6=max((u for u in range(n) if len(adj[u])==6),key=lambda u:dodd[u])
        for vname,v in [('deg5',v5),('deg6',v6)]:
            dv=bfs(adj,[v]); stats=[]
            for rep in range(8):
                col=random_colouring(adj,v,rng,flips=200)
                cyc=link_cycle(adj,v)
                if len(set(col[w] for w in cyc))<4:
                    # condition on a blocked link: re-sample with the current link forced to use all 4 colours
                    pat=[0,1,0,2,3] if len(cyc)==5 else [0,1,0,1,2,3]
                    col=random_colouring(adj,v,rng,flips=0,assume=list(zip(cyc,pat)))
                mono=monodromy(cyc,col) if len(cyc)%2==0 else float('nan')
                kok,kr=kempe_procedure(adj,col,v,dv)
                R=local_minR(adj,col,v,Rmax=f)
                stats.append((R,kok,kr,mono))
                print('f=%2d n=%5d %s d(v,odd)=%d rep%d link4=%s mono=%.2f Kempe ok=%s radius=%s  local minR=%s'%(
                    f,n,vname,dodd[v],rep,len(set(col[w] for w in cyc))==4,mono,kok,kr,R),flush=True)
