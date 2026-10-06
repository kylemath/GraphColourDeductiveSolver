"""MathNDiscSearch / shape_profile.py [exploratory, post hoc]: shape profile of locked discs (lines from test_N_fast output, 'N-holds ... | DISC ...').
For each: sizes, degree sequence of T (x included), excess per class (sum (deg-5) over class), vertices of degree>5, separating triangles count, ring-vertex degrees."""
import sys, itertools
from collections import Counter
def prof(line):
    d=line[line.index('DISC'):]
    _,rest=d.split(' ',1); sz,cols,es=rest.split(';')
    col=list(map(int,cols.split())); E=[tuple(map(int,t.split('-'))) for t in es.split()]
    V=len(col); n=V+1; x=V
    adj=[set() for _ in range(n)]
    for u,v in E: adj[u].add(v);adj[v].add(u)
    for r in range(5): adj[x].add(r);adj[r].add(x)
    deg=[len(a) for a in adj]
    exc=[sum(deg[v]-5 for v in range(V) if col[v]==k) for k in range(4)]
    tri=sum(1 for a,b,c in itertools.combinations(range(n),3) if b in adj[a] and c in adj[a] and c in adj[b])
    sep=tri-(2*n-4)
    big=sorted(((deg[v],col[v],v<5) for v in range(V) if deg[v]>5),reverse=True)
    return dict(sizes=tuple(col.count(k) for k in range(4)),degx=deg[x],ringdeg=tuple(deg[:5]),exc=tuple(exc),sep=sep,
                nbig=len(big),maxdeg=max(deg),degseq=tuple(sorted(Counter(deg).items())))
for fn in sys.argv[1:]:
    for l in open(fn):
        if 'DISC' in l and l.startswith(('N-','CAND')):
            p=prof(l); print(p['sizes'],'exc',p['exc'],'ringdeg',p['ringdeg'],'sepTri',p['sep'],'nbig',p['nbig'],'maxdeg',p['maxdeg'],'degseq',p['degseq'])
