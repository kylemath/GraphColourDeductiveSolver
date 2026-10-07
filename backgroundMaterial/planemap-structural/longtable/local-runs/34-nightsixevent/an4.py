import json,sys
from collections import Counter
R=[json.loads(l) for l in open(sys.argv[1])]
def cc(d): return '%d%d%d|%d%d%d'%tuple(d['c'])
P=Counter()
for r in R:
    if r['kind']!='gamma': continue
    s=r['seq']; L=len(s)
    for i in range(L):
        if s[i]['pos']==4 and s[i]['fix']:
            w=[s[(i+t)%L] for t in range(-2,7)]
            P[' '.join(cc(d)+('*' if d['fix'] else ' ') for d in w)]+=1
for k,v in sorted(P.items(),key=lambda x:-x[1]): print(v,k)
