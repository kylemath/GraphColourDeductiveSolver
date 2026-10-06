# For holes with p deg>=7 and others deg 5: per DL state, position k of p rel j, outer pattern, and which named swaps reach non-DL.
import collections,sys
from lib import parse,adj
from exh import graphs
from pat import *
want=sys.argv[1] if len(sys.argv)>1 else 'o5'
stats=collections.defaultdict(collections.Counter)
examples={}
for N in [16,17,18,19,20,21,22]:
    G=graphs(f'g{N}.txt'); recs,links,dls=parse(open(f'c{N}.txt').read())
    for r in recs:
        g,v=r['g'],r['v']; n,F=G[g]; Ad=adj(n,F); d=[len(a) for a in Ad]; L=links[(g,v)]
        ld=[d[x] for x in L]; top=max(ld)
        if top<7 or sorted(ld)[-2]>(5 if want=='o5' else 6) or r['sep']: continue
        kp=ld.index(top)
        dist={canon(col,v):dd for j,dd,col in dls[(g,v)]}
        for j,dd,col in dls[(g,v)]:
            k=(kp-j)%5; X=[L[(j+t)%5] for t in range(5)]
            a,b,gg,de=col[X[0]],col[X[1]],col[X[3]],col[X[4]]
            named={'AB(x1)':(a,b,X[1]),'F':(a,gg,X[2]),'B':(a,de,X[0]),'G':(gg,de,X[3]),'BG(x1)':(b,gg,X[1]),'BD(x1)':(b,de,X[1]),'AG(x0)':(a,gg,X[0]),'AD(x2)':(a,de,X[2])}
            res={}
            for nm,(p,q,s) in named.items():
                K=comp(Ad,col,p,q,s,v); c2=list(col)
                for u in K: c2[u]= q if col[u]==p else p
                t,_=classify(Ad,c2,L,v)
                res[nm]= 0 if t!='DL' else dist[canon(c2,v)]
            best=min(res.values())
            stats[(k,dd)][tuple(sorted(nm for nm in res if res[nm]==0))]+=1
            if dd>=3: examples.setdefault((k,dd),(N,g,v,j,col))
for key in sorted(stats):
    tot=sum(stats[key].values()); nobreak=stats[key].get((),0)
    single=collections.Counter()
    for t,cn in stats[key].items():
        for nm in t: single[nm]+=cn
    print('k=%d radius=%d states=%d  no named breaker=%d  per-swap breaks:'%(key[0],key[1],tot,nobreak),dict(single.most_common()))
for k,e in sorted(examples.items()): print('example',k,e[:4])
