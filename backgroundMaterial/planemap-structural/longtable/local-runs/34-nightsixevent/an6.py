import json,sys
from collections import Counter
R=[json.loads(l) for f in sys.argv[1:] for l in open(f)]
G=Counter(); O=Counter()
for r in R:
    s=r['seq']; L=len(s)
    if r['kind']=='gamma':
        for i in range(L):
            if not s[i]['fix']: continue
            for g in range(1,7):
                if s[(i+g)%L]['fix']: G[(g,s[i]['pos'])]+=1
    else:
        for i in range(1,L-1):
            if not s[i]['DL'] or not s[i].get('fix'): continue
            for g in range(1,7):
                if i+g<L-1 and s[i+g]['DL'] and s[i+g].get('fix'): O[(g,s[i]['pos'])]+=1
print('gamma (gap,startpos):',sorted(G.items()))
print('open  (gap,startpos):',sorted(O.items()))
