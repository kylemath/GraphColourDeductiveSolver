import json,sys
from collections import Counter
R=[json.loads(l) for f in sys.argv[1:] for l in open(f)]
def show(seq):
    return ' '.join(('%s:%d%d%d%s'%(d['pos'],*d['c'][:3],'*' if d.get('fix') else '') if d.get('c') else 'X') if d['DL'] else ('[%s]'%(d['pos'],)) for d in seq)
g=[r for r in R if r['kind']=='gamma']
for r in g[:12]: print(r['tag'],show(r['seq']))
print()
o=[r for r in R if r['kind']=='open']
n=0
for r in o:
    s=r['seq']
    for i in range(1,len(s)-5):
        if s[i]['pos']==4 and all(s[i+t]['DL'] for t in range(5)) and s[i]['fix'] and s[i+4]['fix']:
            n+=1
            if n<=25: print(r['tag'],len(s)-2,show(s[max(0,i-6):i+11]))
print(n)
