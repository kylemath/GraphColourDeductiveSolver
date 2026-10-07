# edge lemma check: Delta E(alpha B) - Delta E(alpha mu) = 1 and Delta E(alpha A) = 0 on every DL->DL step
import json,sys
from collections import Counter
C=Counter()
for l in open(sys.argv[1]):
    r=json.loads(l); s=r['seq']; L=len(s); cyc=r['kind']=='gamma'
    for i in (range(L) if cyc else range(1,L-2)):
        a,b=s[i],s[(i+1)%L]
        if not(a['DL'] and b['DL'] and 'E' in a and 'E' in b): continue
        dEB=b['E'][0]-a['E'][1]; dEmu=b['E'][2]-a['E'][0]; dEA=b['E'][1]-a['E'][2]  # new frame mu'=B, A'=mu, B'=A
        C[(r['kind'],dEB-dEmu,dEA)]+=1
print(C)
