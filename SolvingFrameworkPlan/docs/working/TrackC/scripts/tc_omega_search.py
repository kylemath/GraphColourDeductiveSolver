import itertools
def isCW(x,y,z): return (x,y,z) in [(1,2,3),(2,3,1),(3,1,2)]
def sig(a,b,c): return 1 if isCW(a^b,b^c,c^a) else -1
pairs=[(a,b) for a in range(4) for b in range(4) if a<b]
sols={}
for mu in range(4):
  found=[]
  for vals in itertools.product(range(8),repeat=6):
    w={}
    for (a,b),v in zip(pairs,vals): w[(a,b)]=v; w[(b,a)]=(-v)%8
    ok=True
    for a,b,c in itertools.permutations(range(4),3):
      rhs=(sig(a,b,c)-4+4*((a==mu)+(b==mu)+(c==mu)))%8
      if (w[(a,b)]+w[(b,c)]+w[(c,a)])%8!=rhs: ok=False;break
    if ok: found.append(vals)
  print(mu,len(found),found[:3])
  sols[mu]=found
# pick a uniform formula? check table with first sol
def hand(a,m,A,B): return isCW(a^m,a^A,a^B)
for mu in range(4):
  vals=sols[mu][0]
  w={}
  for (a,b),v in zip(pairs,vals): w[(a,b)]=v; w[(b,a)]=(-v)%8
  for a,A,B in itertools.permutations([x for x in range(4) if x!=mu],3):
    C=[a,mu,a,A,B]
    for s in (1,4):
      Bsum=sum(w[(C[k],C[(k+s)%5])] for k in range(5))%8
      hs = hand(a,mu,A,B) if s==1 else (not hand(a,mu,A,B))
      if Bsum != (5-2*hs)%8: print("FAIL",mu,C,s,Bsum,hs)
print("done")
