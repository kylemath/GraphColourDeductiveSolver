import sys; from eng import *
from collections import Counter
NM={(3,4):0,(1,1):1,(3,3):2,(1,0):3,(3,2):4,(1,4):5,(3,1):6,(1,3):7,(3,0):8,(1,2):9}
st=Counter()
for n in [int(x) for x in sys.argv[1].split(',')]:
  for gi,rot0 in graphs(n):
    for mirror in (0,1):
      rot=[list(reversed(r)) for r in rot0] if mirror else rot0
      for h in holes6(rot):
        Hh=H(rot,h); q=Hh.q; w2=Hh.W[(q+2)%5]
        for c in Hh.sp.states:
            if not Hh.DL(c): continue
            p_=NM.get(Hh.frame(c)[1:3])
            if p_ is None: continue
            a,b=c[Hh.Y],c[Hh.Z]
            if c[w2] not in (a,b): continue
            Cy=Hh.comp(c,Hh.Y,a,b)
            Cz=Hh.comp(c,Hh.Z,a,b)
            st[(p_, 'y~w2',w2 in Cy,'z~w2',w2 in Cz,'J',Hh.Z in Cy)]+=1
for k in sorted(st): print(k, st[k])
