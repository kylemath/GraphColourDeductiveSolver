import json,sys
from collections import Counter
sys.argv=['x','dump','/dev/null']
exec(open('simg.py').read().split("if __name__")[0])
d=json.load(open(os.path.join(HERE,'../27-studio-positive-config/jobuv/jobak-66dump.json'))); seen=set()
C=Counter()
def lt(H,s,r):
    if s==r: return 'fix'
    l1,l2=H.locks(s); return 'DL' if l1 and l2 else 'L2' if l2 else 'L1' if l1 else 'no'
for r in d:
    key=(r['run'],r['name'],r['hole'])
    if key in seen: continue
    seen.add(key)
    res,H=analyse(r['rotation'],r['hole'],'')
    for z in res:
        Z=H.cycles[z['cyc']]; L=len(Z); pos=[x['pos'] for x in z['rows']]
        S=[H.sigma(x) for x in Z]
        for n in range(L):
            a=S[n]; b=S[(n+1)%L]; rel=None
            x=a
            for t in range(1,6):
                x=H.pi[x]
                if x==b: rel=t;break
            if rel is None:
                x=a
                for t in range(1,6):
                    x=H.pinv[x]
                    if x==b: rel=-t;break
            C[(pos[n],lt(H,a,Z[n]),pos[(n+1)%L],lt(H,b,Z[(n+1)%L]),rel)]+=1
for k,v in sorted(C.items(),key=lambda kv:(kv[0][0],-kv[1])): print(k,v)
