from tw import *
fn=sys.argv[1]; k=int(sys.argv[2])
T,A,B,cA_,cB_,R0=load(fn); c=close(T,A,B,cA_,cB_)
print('R',c['R'],R0,'nconf',len(c['K']))
n=len(T.adj); sv=set(x for u in A for w in T.adj[u] if w not in A for x in (u,w))
dS=multi_bfs(T.adj,list(sv),set(range(n)))
free=[v for v in range(n) if dS[v]<=k]
print('band',len(free))
st,X,sec=sdp(T,c['col'],free)
print(st,round(sec,1), resid(T,c['col'],free,X) if X is not None else None)
