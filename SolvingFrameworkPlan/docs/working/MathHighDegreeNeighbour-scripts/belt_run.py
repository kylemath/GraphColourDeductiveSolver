from lib import *
import collections,sys
gs=[belt(n) for n in range(5,14)]
for n,F in gs: check(n,F)
out=run(gs,extra=['--hole','2'])
recs,links,dls=parse(out)
for r in recs:
    g=r['g']; n,F=gs[g]; Ad=adj(n,F); v=r['v']; lk=links[(g,v)]
    deg=[len(Ad[x]) for x in lk]
    kpos=[max(range(5),key=lambda i:deg[i])]
    by=collections.Counter()
    mx=collections.defaultdict(int)
    for j,d,col in dls[(g,v)]:
        k=(kpos[0]-j)%5
        by[(k,d)]+=1; mx[k]=max(mx[k],d)
    print('G_%d'%((n-2)//2),'v',v,'deg',deg,'ncol',r.get('ncol'),'ndl',r.get('ndl'),'hist_dl',r.get('hist_dl'),'unr',r.get('unreached'),'max by k',dict(mx))
