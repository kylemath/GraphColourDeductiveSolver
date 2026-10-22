import sys, json
sys.path.insert(0,'/mnt/project-files/multiscale/review1')
from rv import *
sys.path.insert(0,'/mnt/project-files/multiscale/levelling')
from e1_survey import graph
rows=[json.loads(l) for l in open('/mnt/project-files/multiscale/review1/t4_minw.jsonl')]
rows=[r for r in rows if 't0_anyw' in r and r['nodd']>0 and r['n']<=200]
agree=0;tot=0
for r in rows:
    T=graph(r['name']); cl=Cluster(T,bfs(T.adj,r['c'],r['r']))
    for seed in (1,2):
        _,c=level_w(T,cl.S,K2=1.0,wmode=None,seed=seed,budget=10**6)
        if c in (None,'UNK'): continue
        x=0
        for o in cl.odd: x^=c[o]
        t=cl.tau(c)[1]; tot+=1; agree+= ((x==0)==(t<1e-6))
        print(r['nodd'],r['t0_anyw'],'xor',x,'t',round(t,3),flush=True)
print('agree',agree,'of',tot)
