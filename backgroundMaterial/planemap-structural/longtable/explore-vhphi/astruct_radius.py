#!/usr/bin/env python3
"""astruct_radius.py : Kempe radius (min # Kempe swaps, any bichromatic component of T-v, to a state whose link has <=3 colours)
for every listed infinite-chain colouring of A_r (ring0=01023 fixed), r=3..8; BFS depth<=5, canonical states."""
import sys,itertools,collections; sys.path.insert(0,'.')
from astruct_core import *
from astruct_delete import S
def comps_all(adj,col):
    out=[]
    for pair in itertools.combinations(range(4),2):
        seen=set()
        for u in col:
            if u=='v' or col[u] not in pair or u in seen: continue
            K=comp(adj,col,u,set(pair)); seen|=K; out.append((pair,frozenset(K)))
    return out
def swap(col,pair,K):
    a,b=pair; return {u:((b if col[u]==a else a) if u in K else col[u]) for u in col}
def filled(col,L): return len(set(col[x] for x in L))<=3
def radius(adj,L,order,col,maxd=5):
    c0=canon(col,order); seen={c0}; front=[(col,[])]
    for d in range(1,maxd+1):
        nf=[]
        for c,path in front:
            for pair,K in comps_all(adj,c):
                n=swap(c,pair,K); k=canon(n,order)
                if k in seen: continue
                seen.add(k)
                if filled(n,L): return d,path+[(pair,sorted(map(str,K)))]
                nf.append((n,path+[(pair,sorted(map(str,K)))]))
        front=nf
    return None,None
if __name__=="__main__":
    for r in range(3,9):
        adj=build(r);L=link(r);order=[u for u in adj if u!='v']; H=collections.Counter(); ex=None
        for seq,cc in S[r]:
            col={'v':None,'c':cc}
            for i in range(r):
                for t in range(5): col[(i,t)]=seq[i][t]
            d,p=radius(adj,L,order,col)
            H[d]+=1
            if ex is None: ex=(seq,cc,d,p)
        print("r",r,"radius histogram over the infinite-chain colourings (ring0 fixed):",dict(H),flush=True)
        if r in (3,6): print("  example",ex[2],ex[3])
