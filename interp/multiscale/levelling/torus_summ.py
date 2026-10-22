import json, itertools, collections
def ew(p,q,r):
    best=99
    for a in range(-3,4):
        for b in range(-3,4):
            if (a,b)==(0,0): continue
            x=a*p+b*r; y=b*q
            best=min(best,(abs(x)+abs(y)+abs(x+y))//2)
    return best
R=[json.loads(l) for l in open('e5_torus.jsonl')]
print(len(R),'tori up to n=',max(r['n'] for r in R))
c=collections.Counter()
for r in R:
    w=ew(r['p'],r['q'],r['r']); r['ew']=w
    c[(r['col3'],r['col4'],min(w,9))]+=1
for k in sorted(c): print('col3,col4,edgewidth',k,c[k])
print('non-4-col with ew>=4:',[ (r['p'],r['q'],r['r']) for r in R if not r['col4'] and r['ew']>=4])
z=collections.Counter((r['col3'],r.get('zero_periods'),r.get('min_t1sq'),r.get('min_t2sq')) for r in R if 'zero_periods' in r)
print('zero-period status (col3, zero_periods, min|t1|^2, min|t2|^2):',dict(z))
print('examples non3col 4col zero?',[ (r['p'],r['q'],r['r'],r['ew'],r.get('zero_periods'),r.get('min_t1sq'),r.get('min_t2sq')) for r in R if r['col4'] and not r['col3'] and 'zero_periods' in r][:30])
