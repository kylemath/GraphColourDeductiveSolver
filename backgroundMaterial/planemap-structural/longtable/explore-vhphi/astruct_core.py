#!/usr/bin/env python3
"""astruct_core.py -- own definition of A_r, doubly-locked test, F (team A-Structure). stdlib only.
A_r: vertices v, (i,t) i=0..r-1, t in Z5, cap c. Edges: v~(0,t); (i,t)~(i,t+1); (i,t)~(i+1,t),(i+1,t-1)... i.e. (i+1,t) adjacent to (i,t),(i,t+1); c~(r-1,t).
Order 5r+2.  Link of v in rotation order: (0,0),(0,1),...,(0,4)."""
import itertools
def build(r):
    V=['v']+[(i,t) for i in range(r) for t in range(5)]+['c']
    adj={u:set() for u in V}
    def e(a,b): adj[a].add(b); adj[b].add(a)
    for t in range(5):
        e('v',(0,t)); e('c',(r-1,t))
        for i in range(r):
            e((i,t),(i,(t+1)%5))
            if i+1<r: e((i,t),(i+1,t)); e((i,(t+1)%5),(i+1,t))
    return adj
def link(r): return [(0,t) for t in range(5)]
def comp(adj,col,s,pair):
    seen={s}; st=[s]
    while st:
        u=st.pop()
        for w in adj[u]:
            if w!='v' and w not in seen and col[w] in pair: seen.add(w); st.append(w)
    return seen
def repeat_index(col,L):
    cs=[col[x] for x in L]
    if len(set(cs))!=4: return None
    js=[j for j in range(5) if cs[j]==cs[(j+2)%5]]
    return js[0] if len(js)==1 else None
def roles(L,j): return L[j],L[(j+1)%5],L[(j+2)%5],L[(j+3)%5],L[(j+4)%5]
def locks(adj,col,L):
    j=repeat_index(col,L)
    if j is None: return None
    x0,m,x2,a,b=roles(L,j)
    return (a in comp(adj,col,m,{col[m],col[a]}), b in comp(adj,col,m,{col[m],col[b]}))
def doubly(adj,col,L):
    l=locks(adj,col,L); return l==(True,True)
def F(adj,col,L):
    j=repeat_index(col,L)
    x0,m,x2,a,b=roles(L,j)
    al,c=col[x0],col[a]
    K=comp(adj,col,x2,{al,c})
    assert x0 not in K or True
    return {u:((c if col[u]==al else al) if u in K else col[u]) for u in col}
def key(col,order): return tuple(col[u] for u in order)
def canon(col,order):
    mp={};out=[]
    for u in order:
        c=col[u]
        if c not in mp: mp[c]=len(mp)
        out.append(mp[c])
    return tuple(out)
def orbit(adj,col,L,order,cap=2000,renaming=False):
    """return (period, all_doubly) following raw (renaming=False) or canonical states."""
    seen={};s=dict(col);k=0;alld=True
    while k<cap:
        kk=canon(s,order) if renaming else key(s,order)
        if kk in seen: return (k-seen[kk],seen[kk],alld,k)
        seen[kk]=k
        if not doubly(adj,s,L): alld=False; return (None,None,False,k)
        s=F(adj,s,L);k+=1
    return (None,None,alld,k)
