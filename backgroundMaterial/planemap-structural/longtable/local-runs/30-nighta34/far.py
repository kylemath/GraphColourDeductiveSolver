import json; from eng import *
NM={(3,4):0,(1,1):1,(3,3):2,(1,0):3,(3,2):4,(1,4):5,(3,1):6,(1,3):7,(3,0):8,(1,2):9}
recs=[json.loads(l) for f in ('s2223.jsonl','s24.jsonl') for l in open(f)]
G={}
for r in recs:
    n=r['n']
    if n not in G: G[n]=dict(graphs(n))
    rot=G[n][r['g']]; rot=[list(reversed(x)) for x in rot] if r['mir'] else rot
    Hh=H(rot,r['h']); S=Hh.sp.states; idx=Hh.sp.index
    DL=[Hh.DL(c) for c in S]; nx={k:idx[Hh.canon(Hh.pi(c)[0])] for k,c in enumerate(S) if DL[k]}; pd=set(nx.values())
    for k0 in range(len(S)):
        if not DL[k0] or k0 in pd: continue
        seq=[]; c=S[k0]; kk=k0
        while DL[kk]: seq.append(c); c=Hh.pi(c)[0]; kk=idx[Hh.canon(c)]
        if len(seq)!=r['runlen']: continue
        i=r['i']; c8,c9=seq[i],seq[i+1]
        if not(NM[Hh.frame(c8)[1:3]]==8 and Hh.J(c8) and not Hh.J(c9)): continue
        q=Hh.q; loc=set(Hh.X)|set(Hh.W)|{Hh.Mi}
        Zb=Hh.comp(c9,Hh.Z,c9[Hh.Y],c9[Hh.Z]); d8=seq[i+10]; al,mu,A,B=Hh.frame(d8)[3]
        K2=Hh.comp(d8,Hh.X[(q+2)%5],al,A); al0,mu0,A0,B0=Hh.frame(c8)[3]; K1=Hh.comp(c8,Hh.X[(q+2)%5],al0,A0)
        # Lock2 chain at R3k3 of period b+2 if exists
        print(r['n'],r['g'],r['mir'],'second',r['second'],'|Zb|',len(Zb),'Zb far',len(Zb-loc),'K2 far',len(K2-loc),'K2∩Zb far',len((K2&Zb)-loc),'K2∩Zb local',[v for v in K2&Zb&loc],'K1 far',len(K1-loc),'K1∩K2 far',len((K1&K2)-loc))
        break
