import json, sys
from collections import Counter
R=[json.loads(l) for l in open(sys.argv[1])]
R=[r for r in R if r['ok']]
# duality check: rank_ab = C_cd - 1 - eps
comp={'12':'34','13':'24','14':'23','34':'12','24':'13','23':'14'}
bad=Counter(); tot=0
for r in R:
  for i,st in r['st'].items():
    l1,l2=r['loc'][i][0]; al,mu,A,B=r['loc'][i][1]  # canonical colours; need absolute frame
    tot+=1
    # absolute frame from LINK table: alpha at pos i is 1 always; mu=link[j+1]
    LINK={3:[4,2,1,3,1],4:[1,2,1,3,4],5:[1,2,3,1,4],6:[2,1,3,1,4],7:[2,1,3,4,1],8:[2,3,1,4,1],9:[1,3,1,4,2]}[int(i)]
    j=next(j for j in range(5) if LINK[j]==LINK[(j+2)%5])
    a,m,Aa,Bb=LINK[j],LINK[(j+1)%5],LINK[(j+3)%5],LINK[(j+4)%5]
    k=lambda x,y:'%d%d'%tuple(sorted((x,y)))
    pred={k(m,Aa):st[k(a,Bb)][1]-1-l1, k(a,Bb):st[k(m,Aa)][1]-1-(1-l1),
          k(m,Bb):st[k(a,Aa)][1]-1-l2, k(a,Aa):st[k(m,Bb)][1]-1-(1-l2),
          k(a,m):st[k(Aa,Bb)][1]-1, k(Aa,Bb):st[k(a,m)][1]-1}
    for p,v in pred.items():
      if st[p][0]!=v: bad[(i,p)]+=1
print('states',tot,'duality violations',sum(bad.values()),dict(bad))
