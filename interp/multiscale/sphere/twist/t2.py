from tw import *
fn=sys.argv[1]
T,A,B,cA_,cB_,R0=load(fn); c=close(T,A,B,cA_,cB_)
n=len(T.adj); sv=set(x for u in A for w in T.adj[u] if w not in A for x in (u,w))
dS=multi_bfs(T.adj,list(sv),set(range(n)))
print('R',c['R'],'nconf',len(c['K']))
for k in range(0,4):
    free=[v for v in range(n) if dS[v]<=k]
    for d in (3,6,12):
        t0=time.time(); r=[bm(T,c['col'],free,d=d,seed=s,iters=3000) for s in range(2)]+[bm(T,c['col'],free,d=d,init='old',iters=3000)]
        print(k,len(free),d,['%.1e'%v[0] for v in r],round(time.time()-t0,1),flush=True)
