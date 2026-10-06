#!/usr/bin/env python3
"""astruct_certify.py : finite certificate of the closing criterion (Lemma B) for every infinite-chain colouring of A_r, r=3..8 (ring0=01023 listing).
Checks: (a) s,Fs,F2s,F3s doubly locked; (b) F^4 s = pi o (s o sigma) exactly, sigma = rotation t->t+3, pi a colour permutation, cycle type reported;
(c) equivariance F(s o sigma)=F(s) o sigma and doubly(s o sigma)=doubly(s) for those s.  Single process, stdlib."""
import sys,collections; sys.path.insert(0,'.')
from astruct_core import *
from astruct_delete import S
def sig(c,k=3): return {u:(c[u] if u in('c','v') else c[(u[0],(u[1]+k)%5)]) for u in c}
tot=collections.Counter()
for r in range(3,9):
    adj=build(r);L=link(r);res=collections.Counter()
    for seq,cc in S[r]:
        s={'v':None,'c':cc}
        for i in range(r):
            for t in range(5): s[(i,t)]=seq[i][t]
        x=dict(s);ok_a=True
        for n in range(4):
            ok_a&=bool(doubly(adj,x,L)); 
            # equivariance
            ok_c=(doubly(adj,sig(x),L)==doubly(adj,x,L)) and (F(adj,sig(x),L)==sig(F(adj,x,L)))
            res['equivariance_ok' if ok_c else 'equivariance_FAIL']+=1
            x=F(adj,x,L)
        tw=sig(s); pi={}
        good=all(pi.setdefault(tw[u],x[u])==x[u] for u in s if u!='v')
        cyc=None
        if good:
            cols=sorted(set(pi)); seen=set();cyc=[]
            for a in cols:
                if a in seen: continue
                l=1;b=pi[a];seen.add(a)
                while b!=a: seen.add(b);b=pi[b];l+=1
                cyc.append(l)
            cyc=tuple(sorted(cyc))
        res[("locked4=%s"%ok_a,"F4=pi*s*sigma:%s"%good,"cycle type %s"%(cyc,))]+=1
    print("r",r,"order",5*r+2,"solutions",len(S[r]),dict(res))
