"""For local step-8 breaks whose run stays DL to step 9 of period b+1: R_b (Job AM def), r_far, and its relation to period b+1's step-8 component K' and Z_{b+1}."""
import json; from eng import *
NM={(3,4):0,(1,1):1,(3,3):2,(1,0):3,(3,2):4,(1,4):5,(3,1):6,(1,3):7,(3,0):8,(1,2):9}
G={}
for f in ('s2223.jsonl','s24.jsonl'):
  for l in open(f):
    r=json.loads(l); n=r['n']
    if n not in G: G[n]=dict(graphs(n))
    rot=G[n][r['g']]; rot=[list(reversed(x)) for x in rot] if r['mir'] else rot
    Hh=H(rot,r['h']); S=Hh.sp.states; idx=Hh.sp.index; q=Hh.q
    lab={Hh.P:'p',Hh.Mi:'m',Hh.Y:'y',Hh.Z:'z'}
    for t in range(5): lab.setdefault(Hh.X[t],'x%d'%((t-q)%5)); lab.setdefault(Hh.W[t],'w%d'%((t-q)%5))
    DL=[Hh.DL(c) for c in S]; nx={k:idx[Hh.canon(Hh.pi(c)[0])] for k,c in enumerate(S) if DL[k]}; pd=set(nx.values())
    for k0 in range(len(S)):
        if not DL[k0] or k0 in pd: continue
        seq=[]; c=S[k0]; kk=k0
        while DL[kk]: seq.append(c); c=Hh.pi(c)[0]; kk=idx[Hh.canon(c)]
        if len(seq)!=r['runlen']: continue
        i=r['i']; c8,c9=seq[i],seq[i+1]
        if not(NM[Hh.frame(c8)[1:3]]==8 and Hh.J(c8) and not Hh.J(c9)): continue
        c0,c1=seq[i+2],seq[i+3]; K0=Hh.pi(c0)[2]; K1=Hh.pi(c1)[2]
        Zb=Hh.comp(c9,Hh.Z,c9[Hh.Y],c9[Hh.Z])
        R=[v for v in K0|K1 if any(w in Zb for w in Hh.nb[v])]; far=[v for v in R if v not in lab]
        d8,d9=seq[i+10],seq[i+11]; Kp=Hh.pi(d8)[2]; Z2=Hh.comp(d9,Hh.Z,d9[Hh.Y],d9[Hh.Z])
        heal=Hh.comp(seq[i+4],Hh.Z,seq[i+4][Hh.Y],seq[i+4][Hh.Z])  # z's G_J comp at R3k3^{b+1}
        print(n,r['g'],r['mir'],'second',r['second'],'|R|',len(R),'far',len(far),
              'rfar in K\'',[v in Kp for v in far],'rfar in Z_{b+1}',[v in Z2 for v in far],'rfar adj Z_{b+1}',[any(w in Z2 for w in Hh.nb[v]) for v in far],
              'rfar on heal comp',[v in heal for v in far],'|Zb∩Z_{b+1}|',len(Zb&Z2),'Zb∩K\'',len(Zb&Kp),'K0∩K\'far',len((K0-set(lab))&Kp))
        break
