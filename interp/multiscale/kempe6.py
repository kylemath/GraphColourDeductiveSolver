# deg-6 vortex on geodesic domes: min single-vertex repair radius vs distance to nearest odd (degree-5) vertex.
# Proved lower bound (height monodromy, nonzero, Eulerian ball): R >= d(v,odd) - 2, so the search starts at max(0,d-4).
import sys, random
MARK="\nif __name__"
exec(open('kempe5.py').read().split(MARK)[0])
def local_minR_from(adj,col,v,R0,Rmax):
    for R in range(R0,Rmax+1):
        for cv in range(4):
            full=dict(col); full[v]=cv
            K=[v]+[w for w in adj[v] if full[w]==cv]
            if len(K)==1: return 0
            dist=bfs(adj,K,R)
            if sat(adj,set(dist),{u:full[u] for u in range(len(adj)) if u not in dist}) is not None: return R
    return None
rng=random.Random(7)
for f in [6,10,14,20,28]:
    adj=icosphere(f); n=len(adj); odd=[u for u in range(n) if len(adj[u])%2]; dodd=bfs(adj,odd)
    v=max((u for u in range(n) if len(adj[u])==6),key=lambda u:dodd[u]); d=dodd[v]
    cyc=link_cycle(adj,v)
    for rep in range(3):
        col=random_colouring(adj,v,rng,flips=0,assume=list(zip(cyc,[0,1,0,1,2,3])))
        mono=monodromy(cyc,col)
        R=local_minR_from(adj,col,v,max(0,d-4),f+2)
        print("f=%2d n=%5d deg6 d(v,odd)=%d mono=%.2f minR=%s (search from %d)"%(f,n,d,mono,R,max(0,d-4)),flush=True)
