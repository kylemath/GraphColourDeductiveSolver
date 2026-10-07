"""[exploratory] NightTwoPocket control: the local open double break gentri 24 #3611 h0 (NightLemmaS / NightA34 §4(d)). m's far neighbours,
their table-frame colours at the two R1k2 states, and the pockets. Uses ../30-nighta34/eng.py."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../30-nighta34'))
from eng import *
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from mdata import tabcol, HN
NM={(3,4):0,(1,1):1,(3,3):2,(1,0):3,(3,2):4,(1,4):5,(3,1):6,(1,3):7,(3,0):8,(1,2):9}
rot=dict(graphs(24))[3610]; Hh=H(rot,0); S=Hh.sp.states; idx=Hh.sp.index; inv={v:k for k,v in Hh.sp.idx.items()}
DL=[Hh.DL(c) for c in S]; nxt={k:idx[Hh.canon(Hh.pi(c)[0])] for k,c in enumerate(S) if DL[k]}; pd=set(nxt.values())
adj={v:set(Hh.sp.idx[u] for u in rot[inv[v]] if u!=0) for v in inv if inv[v]!=0} if False else None
for k0 in range(len(S)):
    if not DL[k0] or k0 in pd: continue
    seq=[]; c=S[k0]; kk=k0
    while DL[kk]: seq.append(c); c=Hh.pi(c)[0]; kk=idx[Hh.canon(c)]
    if len(seq)<18: continue
    nm={'p':Hh.P,'m':Hh.Mi,'y':Hh.Y,'z':Hh.Z}
    for t in range(5):
        r=(t-Hh.q)%5; nm[['p','xp','x2','x3','xm'][r]]=Hh.X[t]; nm[['z','wp','w2','w3','y'][r]]=Hh.W[t]
    A=Hh.sp.adj; I=Hh.sp.idx; print('adj type',type(A), 'len', len(A), 'idx sample', list(I.items())[:4]); adj={I[v]:set(I[u] for u in (A[v] if not isinstance(A,dict) else A[v]) if u in I) for v in (range(len(A)) if not isinstance(A,dict) else A) if v in I}
    far=sorted(adj[nm['m']]-{nm['p'],nm['y'],nm['z']}); print('deg(m) in T-h:', len(adj[nm['m']]), 'far nbrs', far, [[u for u in far if nm[k] in adj[u]] for k in ('z','y')])
    for t,c in enumerate(seq):
        f=Hh.frame(c); p=NM.get((f[1],f[2]))
        if p!=9: continue
        T=tabcol(9); phi={}
        for k in HN: phi[c[nm[k]]]=T[k]
        col={v:phi[c[v]] for v in range(len(c))}
        P={nm['m']}; st=[nm['m']]
        while st:
            u=st.pop()
            for w in adj[u]:
                if w not in P and w not in (nm['p'],nm['xp']) and col[w] in (0,2): P.add(w); st.append(w)
        print('state',t,'R1k2: far nbr colours (table frame)',[col[u] for u in far],'pocket',sorted(P),'reaches w+',nm['wp'] in P)
    break
