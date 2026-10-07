import sys, json; from eng import *
from collections import Counter
NM={(3,4):0,(1,1):1,(3,3):2,(1,0):3,(3,2):4,(1,4):5,(3,1):6,(1,3):7,(3,0):8,(1,2):9}
def pos(Hh,c):
    f=Hh.frame(c); return NM.get((f[1],f[2]))
def pocket(Hh,c):
    q=Hh.q; xp=Hh.X[(q+1)%5]; wp=Hh.W[(q+1)%5]; a,b=c[Hh.P],c[Hh.Mi]
    if c[xp] not in (a,b) or c[wp] not in (a,b): return None
    return Hh.Mi in Hh.comp(c,wp,a,b,avoid=(Hh.P,xp))
out=open(sys.argv[2],'w'); stats=Counter()
for n in [int(x) for x in sys.argv[1].split(',')]:
  for gi,rot0 in graphs(n):
    for mirror in (0,1):
      rot=[list(reversed(r)) for r in rot0] if mirror else rot0
      for h in holes6(rot):
        Hh=H(rot,h); S=Hh.sp.states; idx=Hh.sp.index
        DL=[Hh.DL(c) for c in S]
        if not any(DL): continue
        nxt=[idx[Hh.canon(Hh.pi(c)[0])] if DL[k] else None for k,c in enumerate(S)]
        hasprev=set(t for k,t in enumerate(nxt) if t is not None)
        seen=set()
        for k in range(len(S)):
            if not DL[k]: continue
            # T1/T2 checks on every DL state
            c=S[k]; p_=pos(Hh,c)
            if p_==9:
                pk=pocket(Hh,c); stats[('T1 pocket<=>notJ',p_, pk==(not Hh.J(c)))]+=1
            if p_==8:
                q=Hh.q; f=Hh.frame(c); al,mu,A,B=f[3]
                l2=Hh.locks(c)[1]; alt=Hh.X[(q+4)%5] in Hh.comp(c,Hh.Z,mu,B,avoid=(Hh.X[(q+1)%5],))
                stats[('T2 lock2@R3k0 <=> z~x- avoiding x+', l2==alt)]+=1
                K=Hh.comp(c,Hh.X[(q+2)%5],al,A); stats[('F1 step8 K avoids pmyz', not (K & {Hh.P,Hh.Mi,Hh.Y,Hh.Z}))]+=1
            # runs: start at DL states without DL predecessor, or Gamma cycles
        starts=[k for k in range(len(S)) if DL[k]]
        prevDL=set(nxt[k] for k in range(len(S)) if DL[k])
        for k0 in starts:
            if k0 in seen: continue
            # walk back to run start
            k=k0
            # find a predecessor chain: only start at states with no DL predecessor; Gamma handled by seen
            if k0 in prevDL: continue
            seq=[]; c=S[k0]; kk=k0
            while DL[kk] and len(seq)<400:
                seq.append(c); seen.add(kk); c2,kind,Ksw,pr=Hh.pi(c); c=c2; kk=idx[Hh.canon(c)]
            end=c
            P=[pos(Hh,x) for x in seq]
            for i in range(1,len(seq)):
                if P[i]==0 and P[i-1]==9: stats[('T1 in-run R3k4', pocket(Hh,seq[i])==(not Hh.J(seq[i])))]+=1
            for i in range(len(seq)-1):
                if P[i]==8 and Hh.J(seq[i]) and not Hh.J(seq[i+1]):
                    stats['break']+=1
                    i2=i+10
                    if i2+1>=len(seq): stats['break, run ends before next step 8']+=1; continue
                    second=not Hh.J(seq[i2+1])
                    c8,c9=seq[i],seq[i+1]; q=Hh.q
                    al,mu,A,B=Hh.frame(c8)[3]
                    K=Hh.comp(c8,Hh.X[(q+2)%5],al,A)
                    Pi=Hh.comp(c9,Hh.P,c9[Hh.P],c9[Hh.Mi])
                    Zb=Hh.comp(c9,Hh.Z,c9[Hh.Y],c9[Hh.Z])
                    Wb=Hh.comp(c9,Hh.X[(q+4)%5],c9[Hh.Y],c9[Hh.Z])
                    d8=seq[i2]; al2,mu2,A2,B2=Hh.frame(d8)[3]
                    K2=Hh.comp(d8,Hh.X[(q+2)%5],al2,A2)
                    L1=Hh.comp(d8,Hh.X[(q+1)%5],mu2,A2); L2=Hh.comp(d8,Hh.X[(q+1)%5],mu2,B2)
                    # Lock2 status forward
                    tail=seq[i2:]; dist_end=len(seq)-i2
                    rec=dict(n=n,g=gi,mir=mirror,h=h,i=i,runlen=len(seq),second=second,
                      K2K=len(K2&K),K2Pi=len(K2&Pi),K2Zb=len(K2&Zb),K2Wb=len(K2&Wb),L2K=len(L2&K),L2Zb=len(L2&Zb),L1K=len(L1&K),L2Pi=len(L2&Pi),
                      KinZb=len(K&Zb),KinWb=len(K&Wb),dist_end=dist_end,gamma=(kk in seen and DL[kk]))
                    out.write(json.dumps(rec)+'\n'); stats[('cont',second)]+=1
  print(n,dict(stats),flush=True)
