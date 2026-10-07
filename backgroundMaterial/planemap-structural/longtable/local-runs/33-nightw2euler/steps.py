import json, sys
from collections import Counter
LINK={3:[4,2,1,3,1],4:[1,2,1,3,4],5:[1,2,3,1,4],6:[2,1,3,1,4],7:[2,1,3,4,1],8:[2,3,1,4,1],9:[1,3,1,4,2]}
def frame(i):
  L=LINK[i]; j=next(j for j in range(5) if L[j]==L[(j+2)%5]); return L[(j+1)%5],L[(j+3)%5],L[(j+4)%5]
comp={2:'34',3:'24',4:'23'}
C=Counter(); D=Counter()
for f in sys.argv[1:]:
  for l in open(f):
    r=json.loads(l)
    if not r['ok']: continue
    st=r['st']
    for i in range(3,9):
      if str(i) not in st or str(i+1) not in st: continue
      if not (r['DL'].get(str(i),True) if i==3 else True): continue
      mu,A,B=frame(i)
      a=lambda k,c: st[str(k)]['1%d'%c][1]; b=lambda k,c: st[str(k)][comp[c]][1]
      d={role:(a(i+1,c)-a(i,c), b(i+1,c)-b(i,c)) for role,c in (('mu',mu),('A',A),('B',B))}
      Rd=sum(v[0] for v in st[str(i+1)].values())-sum(v[0] for v in st[str(i)].values())
      C[(r['gamma'], 'dmu',d['mu'],'dB',d['B'],'dA',d['A'])]+=1
      D[(r['gamma'],Rd)]+=1
for k in sorted(D): print(k,D[k])
for k in sorted(C, key=lambda k:-C[k])[:40]: print(k,C[k])
