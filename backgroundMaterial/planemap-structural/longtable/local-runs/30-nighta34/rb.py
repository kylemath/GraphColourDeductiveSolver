"""R_b at step-8 breaks on local DL runs: Job AM's definition (K0, K1 = pi-step components at R3k4^{b+1}, R1k1^{b+1}; R_b = vertices of K0 u K1 adjacent to Z_b).
Classifies each R_b vertex: hole label or far, colour role at R3k4^{b+1}, which of K0/K1, in Z_b or not, and which Z_b vertices it touches."""
import sys, json; from eng import *
from collections import Counter
NM={(3,4):0,(1,1):1,(3,3):2,(1,0):3,(3,2):4,(1,4):5,(3,1):6,(1,3):7,(3,0):8,(1,2):9}
st=Counter(); ex=[]
for n in [int(x) for x in sys.argv[1].split(',')]:
  for gi,rot0 in graphs(n):
    for mirror in (0,1):
      rot=[list(reversed(r)) for r in rot0] if mirror else rot0
      for h in holes6(rot):
        Hh=H(rot,h); S=Hh.sp.states; q=Hh.q
        lab={Hh.P:'p',Hh.Mi:'m',Hh.Y:'y',Hh.Z:'z'}
        for t in range(5): lab.setdefault(Hh.X[t],'x%d'%((t-q)%5)); lab.setdefault(Hh.W[t],'w%d'%((t-q)%5))
        for c in S:
            if not Hh.DL(c): continue
            f=Hh.frame(c)
            if NM.get(f[1:3])!=8 or not Hh.J(c): continue
            c9,_,_,_=Hh.pi(c)
            if not Hh.DL(c9) or Hh.J(c9): continue
            c0,_,Pi,_=Hh.pi(c9)
            if not Hh.DL(c0): continue
            c1,_,K0,pr0=Hh.pi(c0)
            if not Hh.DL(c1): st['R1k1 not DL']+=1; continue
            c2,_,K1,pr1=Hh.pi(c1)
            a,b=c9[Hh.Y],c9[Hh.Z]; Zb=Hh.comp(c9,Hh.Z,a,b)
            R=[v for v in K0|K1 if any(w in Zb for w in Hh.nb[v])]
            al,mu,A,B=Hh.frame(c0)[3]; role={al:'al',mu:'mu',A:'A',B:'B'}
            desc=[]
            for v in R:
                desc.append((lab.get(v,'far'),'K0' if v in K0 else '', 'K1' if v in K1 else '', role[c0[v]], 'inZ' if v in Zb else 'bdry', tuple(sorted(lab.get(w,'far') for w in Hh.nb[v] if w in Zb))))
            cc=c2; okDL=True
            for _ in range(3):
                if not Hh.DL(cc): okDL=False; break
                cc=Hh.pi(cc)[0]
            tag='DL to pos4' if okDL else 'leaves by pos4'
            st[(tag,'|R|',len(R),'|Rfar|',sum(1 for d in desc if d[0]=='far'))]+=1
            if okDL: st[(tag,'R', tuple(sorted(desc)))]+=1
            if okDL and len(R)==2:
                fv=[v for v in R if v not in lab][0]
                # is the far vertex adjacent to z?  which K? recoloured to what at pos 2?
                st[(tag,'far vtx adj z', Hh.Z in Hh.nb[fv], 'zjoins w2 at pos2 through fv', fv in Hh.comp(c2,Hh.Z,c2[Hh.Y],c2[Hh.Z]))]+=1
            st[('|R|',len(R))]+=1
            st[('R', tuple(sorted(desc)))]+=1
            st[('Zb hole part', tuple(sorted(lab[v] for v in Zb if v in lab)))]+=1
            st[('DL at pos2', Hh.DL(c2))]+=1
  print(n, flush=True)
for k,v in sorted(st.items(), key=lambda kv:-kv[1])[:40]: print(v,k)
