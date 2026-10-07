import sys; from eng import *
NM={(3,4):0,(1,1):1,(3,3):2,(1,0):3,(3,2):4,(1,4):5,(3,1):6,(1,3):7,(3,0):8,(1,2):9}
def pos(Hh,c):
    f=Hh.frame(c); return NM.get((f[1],f[2]))
n,gi,h,mir=[int(x) for x in sys.argv[1:5]]
rot=dict(graphs(n))[gi]; rot=[list(reversed(r)) for r in rot] if mir else rot
Hh=H(rot,h); S=Hh.sp.states; idx=Hh.sp.index
DL=[Hh.DL(c) for c in S]; nxt={k:idx[Hh.canon(Hh.pi(c)[0])] for k,c in enumerate(S) if DL[k]}
pd=set(nxt.values())
nm='p m y z'.split(); V4=[Hh.P,Hh.Mi,Hh.Y,Hh.Z]
inv={v:k for k,v in Hh.sp.idx.items()}
lab={Hh.P:'p',Hh.Mi:'m',Hh.Y:'y',Hh.Z:'z'}
for t in range(5): lab[Hh.X[t]]='x%d'%((t-Hh.q)%5); lab[Hh.W[t]]= lab.get(Hh.W[t],'w%d'%((t-Hh.q)%5))
L=lambda S_: '{'+','.join(sorted(lab.get(v,str(inv[v])) for v in S_))+'}'
names='R3k4 R1k1 R3k3 R1k0 R3k2 R1k4 R3k1 R1k3 R3k0 R1k2'.split()
for k0 in range(len(S)):
    if not DL[k0] or k0 in pd: continue
    seq=[]; c=S[k0]; kk=k0
    while DL[kk]: seq.append(c); c=Hh.pi(c)[0]; kk=idx[Hh.canon(c)]
    seq.append(c)
    if len(seq)<18: continue
    print('labels relative to q: x0=p, x1=x+, x4=x-, w0=z, w4=y, w1=w+')
    for i,c in enumerate(seq):
        f=Hh.frame(c)
        if f is None or not Hh.DL(c):
            print(i,'LEAVE', 'link',[c[x] for x in Hh.X], f, Hh.locks(c)[:2] if f else ''); break
        j,ty,k,(al,mu,A,B)=f; l1,l2,K1,K2=Hh.locks(c)
        c2,kind,K,pr=Hh.pi(c)
        print(i,names[pos(Hh,c)],'J',int(Hh.J(c)),'colors p m y z',[c[v] for v in V4],'roles',(al,mu,A,B),
              'x_{j+1}=',lab[Hh.X[(j+1)%5]],'L1',L(K1) if len(K1)<14 else len(K1),'L2',L(K2) if len(K2)<14 else len(K2),'| swap',pr,'K',L(K))
