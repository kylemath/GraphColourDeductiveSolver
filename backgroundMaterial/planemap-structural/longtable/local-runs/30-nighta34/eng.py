import sys
from collections import Counter
import os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'../common'))
from kempe_py import Space, gentri_rotation, adj_from_rot
import os
GT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../../studiointel/gentri/tri%d.txt')
def graphs(n):
    for i,l in enumerate(open(GT%n)):
        if l.startswith('G'): yield i, gentri_rotation(l)
class H:
    """hole h with link pattern (5,5,5,5,6); colourings are tuples over Space order (actual colours)."""
    def __init__(s, rot, h):
        s.rot=rot; s.h=h; L=rot[h]; s.L=L
        s.sp=sp=Space(adj_from_rot(rot), h, link=L); s.N=sp.N; s.nb=[[sp.idx[u] for u in rot[sp.order[i]] if u!=h] for i in range(sp.N)]
        s.w=[]
        for t in range(5):
            a,b=L[t],L[(t+1)%5]; ra=rot[a]; p=ra.index(b); c1,c2=ra[(p+1)%len(ra)],ra[(p-1)%len(ra)]
            s.w.append(c2 if c1==h else c1)
        s.q=next(t for t in range(5) if len(rot[L[t]])==6)
        p=L[s.q]; y=s.w[(s.q+4)%5]; z=s.w[s.q]
        s.m=next(u for u in rot[p] if u not in (h,L[(s.q+1)%5],L[(s.q+4)%5],y,z))
        I=sp.idx; s.X=[I[x] for x in L]; s.W=[I[x] for x in s.w]; s.P=I[p]; s.Mi=I[s.m]; s.Y=I[y]; s.Z=I[z]
        s.hnb=set(s.X)
    def comp(s,c,v,a,b,avoid=()):
        if c[v] not in (a,b) or v in avoid: return set()
        S={v}; st=[v]
        while st:
            u=st.pop()
            for t in s.nb[u]:
                if t not in S and t not in avoid and c[t] in (a,b): S.add(t); st.append(t)
        return S
    def swap(s,c,K,a,b):
        d=list(c)
        for v in K: d[v]= b if c[v]==a else a
        return tuple(d)
    def frame(s,c):
        lc=[c[x] for x in s.X]; cnt=Counter(lc)
        if len(cnt)!=4: return None
        j=next(j for j in range(5) if lc[j]==lc[(j+2)%5])
        al,mu,A,B=lc[j],lc[(j+1)%5],lc[(j+3)%5],lc[(j+4)%5]
        w0,w3=c[s.W[j]],c[s.W[(j+3)%5]]
        ty=1 if w0==A else (2 if (w0==B and w3==al) else (3 if (w0==B and w3==mu) else 0))
        return j,ty,(s.q-j)%5,(al,mu,A,B)
    def locks(s,c):
        f=s.frame(c); j,ty,k,(al,mu,A,B)=f; X=s.X
        K1=s.comp(c,X[(j+1)%5],mu,A); K2=s.comp(c,X[(j+1)%5],mu,B)
        return X[(j+3)%5] in K1, X[(j+4)%5] in K2, K1, K2
    def DL(s,c):
        f=s.frame(c)
        if f is None: return False
        l1,l2,_,_=s.locks(c); return l1 and l2
    def pi(s,c):
        """returns (next colouring, kind, swapped set, pair)"""
        X=s.X; lc=[c[x] for x in X]; cnt=Counter(lc)
        if len(cnt)==4:
            j,ty,k,(al,mu,A,B)=s.frame(c)
            if X[(j+4)%5] in s.comp(c,X[(j+1)%5],mu,B):
                K=s.comp(c,X[(j+2)%5],al,A); return s.swap(c,K,al,A),'R3',K,(al,A)
            K=s.comp(c,X[(j+4)%5],mu,B); return s.swap(c,K,mu,B),'phiB',K,(mu,B)
        i=next(i for i in range(5) if cnt[lc[i]]==1)
        Wc,Xc,Yc=lc[i],lc[(i+1)%5],lc[(i+2)%5]; Zc=({0,1,2,3}-{Wc,Xc,Yc}).pop()
        K=s.comp(c,X[(i+2)%5],Yc,Zc)
        if X[(i+4)%5] not in K: return s.swap(c,K,Yc,Zc),'phiA',K,(Yc,Zc)
        K=s.comp(c,X[(i+3)%5],Wc,Xc); return s.swap(c,K,Wc,Xc),'tau',K,(Wc,Xc)
    def J(s,c):
        return s.Z in s.comp(c,s.Y,c[s.Y],c[s.Z])
    def canon(s,c):
        mp={}; return tuple(mp.setdefault(x,len(mp)) for x in c)
def holes6(rot):
    for h in range(len(rot)):
        if len(rot[h])!=5: continue
        d=sorted(len(rot[x]) for x in rot[h])
        if d==[5,5,5,5,6]: yield h
