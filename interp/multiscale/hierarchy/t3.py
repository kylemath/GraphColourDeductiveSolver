import sys, random, collections, time
sys.path.insert(0,'/mnt/project-files/multiscale/hierarchy')
from hier import *
g=G(icosphere(20))
five=[v for v in range(g.n) if g.deg[v]==5]
dd=bfs_in(g,five,set(range(g.n)))
far=max(dd,key=dd.get); print('far',far,dd[far])
def ball(c,r):
    return set(v for v,d in bfs_in(g,[c],set(range(g.n))).items() if d<=r)
for r in (1,2):
    U=ball(far,r); s,w,_=check(g,U)
    print('r',r,len(U),s,'bdeg',collections.Counter(len(g.adj[v]&U) for v in w))
    t=time.time(); e=exhaustive_split(g,U); print(' exhaustive split:', e and (len(e[0]),len(e[1])), round(time.time()-t,1))
# face peels for larger hexagons
for r in (3,4,6):
    U=ball(far,r); s,w,_=check(g,U); ok=0
    tris=[f for f in g.faces if all(x in U for x in f)]
    for f in tris:
        if check(g,U-set(f))[0]=='ok': ok+=1
    print('r',r,len(U),s,'bdeg',collections.Counter(len(g.adj[v]&U) for v in w),'valid face peels',ok)
