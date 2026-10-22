import sys, random
sys.path.insert(0,'/mnt/project-files/multiscale/hierarchy')
from hier import *
g=G(icosphere(5)); rng=random.Random(0)
U=set(range(g.n))
r=split(g,U,None,rng,tries=2,rep=0)
sc,A,B=r[1]
for X,nm in ((A,'A'),(B,'B')):
    s,w,nch=check(g,X); print(nm,len(X),s,nch,len(w))
    for (x,y) in chord_list(g,w):
        pos={v:i for i,v in enumerate(w)}
        print(' chord',x,y,'pos',pos[x],pos[y],'m',len(w),'common nbrs',[(c, 'A' if c in A else 'B', c in pos) for c in g.adj[x]&g.adj[y]])
        # X-degree of between vertices
        i,j=sorted((pos[x],pos[y])); arc=w[i+1:j] if j-i<len(w)/2 else w[j+1:]+w[:i]
        print('  short arc',arc,[len(g.adj[v]&X) for v in arc],[g.deg[v] for v in arc])
