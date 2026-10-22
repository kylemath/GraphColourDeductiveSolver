import sys, json, time
sys.path.insert(0,'/mnt/project-files/multiscale/review1')
from rv import *
sys.path.insert(0,'/mnt/project-files/multiscale/levelling')
from e1_survey import graph
rows=[json.loads(l) for l in open('/mnt/project-files/multiscale/review1/t4_minw.jsonl')]
rows=[r for r in rows if 't0_anyw' in r and r['nodd']==2]
for r in rows:
    T=graph(r['name']); cl=Cluster(T,bfs(T.adj,r['c'],r['r']))
    u,v=sorted(cl.odd)
    res=dict(name=r['name'],c=r['c'],r=r['r'],n=r['n'],d_uv=bfs(T.adj,u)[v])
    for lab,K2 in (('any',None),('level',1.0)):
        enc=CNF(cl.verts)
        for a,b in cl.edges: enc.neq(a,b)
        enc.fix(u,0); enc.fix(v,0)
        if K2: enc.level(cl,K2)
        s=enc.solve()
        res['same_'+lab]= s is not None
        if s and s!='UNK': res['t_same_'+lab]=round(cl.tau(s)[1] or 0,3)
    # a level colouring, check c(u)!=c(v)
    _,c=level_w(T,cl.S,K2=1.0,wmode=None,seed=3)
    res['level_cu_ne_cv']=c[u]!=c[v]; res['level_t']=round(cl.tau(c)[1],3)
    print(json.dumps(res),flush=True)
