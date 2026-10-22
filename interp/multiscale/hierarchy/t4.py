import sys, random, collections
sys.path.insert(0,'/mnt/project-files/multiscale/hierarchy')
from hier import *
g=G(icosphere(10)); rng=random.Random(0)
stack=[(set(range(g.n)),None)]
while stack:
    U,w=stack.pop()
    if w is not None and len(U)<=12: continue
    r=split(g,U,w,rng,L=12)
    if r[0] is not None:
        A,B,_=r; stack.append((A,check(g,A)[1])); stack.append((B,check(g,B)[1])); continue
    print('bad node',len(U),'m',len(w),'reflex',reflex(g,U,w),'Udeg on C',collections.Counter(len(g.adj[v]&U) for v in w))
    sc,A,B=r[1]
    for X,nm in ((A,'A'),(B,'B')):
        s,ww,nch=check(g,X); print(nm,len(X),s,nch)
        if s!='chord': continue
        for (x,y) in chord_list(g,ww):
            pos={v:i for i,v in enumerate(ww)}
            i,j=sorted((pos[x],pos[y])); arc=ww[i+1:j] if j-i<len(ww)/2 else ww[j+1:]+ww[:i]
            print('  chord',x,y,'onC',x in w,y in w,'arc',len(arc),'arc onC',[v in w for v in arc],'Xdeg',[len(g.adj[v]&X) for v in arc],'Udeg',[len(g.adj[v]&U) for v in arc])
    break
