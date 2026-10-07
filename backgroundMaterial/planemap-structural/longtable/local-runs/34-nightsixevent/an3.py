import json,sys
from collections import Counter
R=[json.loads(l) for f in sys.argv[1:] for l in open(f)]
Rv=lambda d: sum(d['c'])-8
dR=Counter(); Rpos=Counter(); span=Counter()
for r in R:
    s=r['seq']; cyc=r['kind']=='gamma'
    idx=range(len(s)) if cyc else range(1,len(s)-2)
    for i in idx:
        a=s[i]; b=s[(i+1)%len(s)]
        if not(a['DL'] and b['DL']): continue
        dR[(r['kind'],Rv(b)-Rv(a))]+=1
    if cyc:
        v=[Rv(d) for d in s]; span[(max(v)-min(v))]+=1
        for d in s: Rpos[(d['pos'],Rv(d))]+=1
print(sorted(dR.items())); print('gamma R span',sorted(span.items()))
for p in range(10): print(p,sorted((k[1],v) for k,v in Rpos.items() if k[0]==p))
