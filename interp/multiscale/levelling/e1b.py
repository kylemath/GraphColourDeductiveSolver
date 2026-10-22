import json, time
from lev import *
from e1_survey import graph
R=[json.loads(l) for l in open('e1_survey.jsonl')]
out=open('e1b.jsonl','w')
for r in R:
    T=graph(r['name']); cl=Cluster(T,bfs(T.adj,r['c'],r['r']))
    S3=sum(cl.s)%3
    rec=dict(name=r['name'],c=r['c'],r=r['r'],odd=cl.parity_odd,S3=S3,tau=r['tau'],exact=r['exact'])
    if not r['exact']:
        t=time.time(); col=sat_level(cl,1.0); rec['tau1_feasible']=col is not None; rec['sec']=round(time.time()-t,1)
        if col is not None:
            col2=sat_level(cl,0.75); rec['tau075_feasible']=col2 is not None
    out.write(json.dumps(rec)+'\n'); out.flush()
