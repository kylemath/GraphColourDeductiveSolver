import json,sys
from collections import Counter
R=[json.loads(l) for l in open(sys.argv[1])]
g=[r for r in R if r['kind']=='gamma']
bad=Counter(); tr=Counter(); fpos=Counter()
for r in g:
    s=r['seq']; L=len(s)
    for i in range(L):
        a,b=s[i],s[(i+1)%L]
        f,G,h=a['c'][:3]; f2,G2,h2=b['c'][:3]
        bad['g_{i+1}=h_i',G2==h]+=1
        bad['fix<=>f=1',a['fix']==(f==1)]+=1
        bad['pos+1',(a['pos']+1)%10==b['pos']]+=1
        # complement preserved: C(muB) at i = C(AB)?? new frame: muB={mu,B}={A',mu'} -> C(mu'A')
        bad['C(muB)_i=C(muA)_{i+1}',a['c'][5]==b['c'][4]]+=1
        tr[(a['pos'],'dg',f2-G,'df',h2-f)]+=1
        fpos[(a['pos'],f)]+=1
for k in sorted(bad): print(k,bad[k])
print(sorted(fpos.items()))
for p in range(10):
    print(p, sorted((k[2],k[4],v) for k,v in tr.items() if k[0]==p))
