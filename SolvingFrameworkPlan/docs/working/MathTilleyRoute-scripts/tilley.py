import json, sys, itertools
from collections import deque
CERT="/Users/fulkanjou/GraphColour/SolvingFrameworkPlan/docs/working/MathChainSearch/lt_certs/"

def A(r):
    # centre 0, rings k=1..r of 5 vertices (k,t)->1+5(k-1)+t, far centre 5r+1
    idx=lambda k,t:1+5*(k-1)+(t%5)
    n=5*r+2; adj={i:set() for i in range(n)}
    def e(a,b): adj[a].add(b); adj[b].add(a)
    for t in range(5):
        e(0,idx(1,t)); e(n-1,idx(r,t))
        for k in range(1,r+1):
            e(idx(k,t),idx(k,t+1))
            if k<r: e(idx(k,t),idx(k+1,t)); e(idx(k,t),idx(k+1,t-1))
    return adj
def from_rot(rot):
    adj={int(k):set(v) for k,v in rot.items()}
    for a in list(adj):
        for b in adj[a]: adj.setdefault(b,set()).add(a)
    return adj
T4F=[(0,1,2),(0,1,5),(0,2,3),(0,3,4),(0,4,5),(1,2,6),(1,5,10),(1,6,10),(2,3,7),(2,6,11),(2,7,11),(3,4,8),(3,7,8),(4,5,9),(4,8,9),(5,9,10),(6,10,15),(6,11,15),(7,8,12),(7,11,12),(8,9,13),(8,12,13),(9,10,14),(9,13,14),(10,14,15),(11,12,16),(11,15,16),(12,13,16),(13,14,16),(14,15,16)]
def from_faces(F):
    adj={}
    for f in F:
        for a in f:
            for b in f:
                if a!=b: adj.setdefault(a,set()).add(b)
    return adj
def link_cycle(adj,v):
    L=list(adj[v]); cyc=[L[0]]
    while len(cyc)<len(L):
        nxt=[u for u in adj[cyc[-1]] if u in adj[v] and u not in cyc]
        if len(cyc)>1: nxt=[u for u in nxt if u!=cyc[-2]]
        cyc.append(nxt[0])
    return cyc
def canon(col,order):
    m={};out=[]
    for u in order:
        c=col[u]
        if c not in m: m[c]=len(m)
        out.append(m[c])
    return tuple(out)
def colourings(adj,verts):
    # all proper 4-colourings of induced graph on verts, canonical (first-occurrence)
    verts=sorted(verts,key=lambda u:-len(adj[u]))
    # BFS order for pruning
    order=[verts[0]];seen={verts[0]}
    while len(order)<len(verts):
        best=max((u for u in verts if u not in seen),key=lambda u:sum(1 for w in adj[u] if w in seen))
        order.append(best);seen.add(best)
    vs=set(verts);res=[];col={}
    def rec(i,mx):
        if i==len(order): res.append(dict(col)); return
        u=order[i]; used={col[w] for w in adj[u] if w in col}
        for c in range(min(4,mx+2)):
            if c not in used:
                col[u]=c; rec(i+1,max(mx,c)); del col[u]
    rec(0,-1); return res
def comp(adj,col,start,a,b,banned_edge=None):
    S={start};q=[start]
    while q:
        u=q.pop()
        for w in adj[u]:
            if w in col and w not in S and col[w] in (a,b):
                if banned_edge and {u,w}==banned_edge: continue
                S.add(w);q.append(w)
    return S
def swap(col,S,a,b):
    c=dict(col)
    for u in S: c[u]= b if col[u]==a else a
    return c
def first_order_locked(adj,col,x,y,e):
    a=col[x]
    for k in range(4):
        if k==a: continue
        if y not in comp(adj,col,x,a,k,e): return False
    return True
def tilley_class(adj,col,x,y,order,memo):
    """Kempe class in G=T-xy of colouring col (c(x)=c(y)); returns (locked, members-keys)."""
    e={x,y}; k0=canon(col,order)
    if k0 in memo: return memo[k0]
    seen={k0:col};q=deque([col]);locked=True
    while q:
        c=q.popleft()
        if not first_order_locked(adj,c,x,y,e): locked=False
        done=set()
        for u in c:
            for b in range(4):
                a=c[u]
                if b==a or (u,b) in done: continue
                S=comp(adj,c,u,a,b,e)
                for w in S: done.add((w,b if c[w]==a else a))
                n=swap(c,S,a,b)
                if n[x]!=n[y]: locked=False; continue
                kk=canon(n,order)
                if kk not in seen: seen[kk]=n;q.append(n)
    for kk in seen: memo[kk]=(locked,len(seen))
    return memo[k0]

def analyse(name,adj,v,full=False):
    n=len(adj); X=link_cycle(adj,v); others=[u for u in adj if u!=v]
    states=colourings(adj,others)
    order=[v]+others
    out={"graph":name,"n":n,"v":v,"link":X,"link_deg":[len(adj[x]) for x in X],"states":len(states)}
    memo={i:{} for i in range(5)}
    nDL=0;filled=0;DL_classes_locked=[0,0,0];DL_total_edges=0;unf_locked_edges=0;unf_edges=0
    edge_has_unlocked=[False]*5; edge_has_colouring=[False]*5; edge_locked_classes=[0]*5
    infF_note=None
    for s in states:
        lc=[s[x] for x in X]
        is_filled=len(set(lc))<=3
        if is_filled: filled+=1
        sing=[i for i in range(5) if lc.count(lc[i])==1]
        # DL test (Step 1): repeat pair j, middle singleton j+1
        DL=False
        if not is_filled:
            j=[i for i in range(5) if lc[i]==lc[(i+2)%5]][0]
            x1,x3,x4=X[(j+1)%5],X[(j+3)%5],X[(j+4)%5]
            b,g,d=lc[(j+1)%5],lc[(j+3)%5],lc[(j+4)%5]
            DL = x3 in comp(adj,s,x1,b,g) and x4 in comp(adj,s,x1,b,d)
        if DL: nDL+=1
        for i in sing:
            col=dict(s); col[v]=lc[i]
            locked,_=tilley_class(adj,col,v,X[i],order,memo[i])
            edge_has_colouring[i]=True
            if not locked: edge_has_unlocked[i]=True
            if not is_filled:
                unf_edges+=1; unf_locked_edges+=locked
                fo=first_order_locked(adj,col,v,X[i],{v,X[i]})
                if DL: assert fo, "DL must be first-order locked"
            if DL:
                DL_total_edges+=1; DL_classes_locked[0]+=locked
    out.update(filled=filled,DL=nDL,
        DL_singleton_edges=DL_total_edges, DL_edges_in_locked_tilley_class=DL_classes_locked[0],
        unfilled_singleton_edges=unf_edges, unfilled_edges_in_locked_class=unf_locked_edges,
        whole_edge_kempe_locked=[edge_has_colouring[i] and not edge_has_unlocked[i] for i in range(5)])
    # distinct locked classes per edge
    out["locked_classes_per_edge"]=[len({id(val) for val in memo[i].values() if val[0]}) for i in range(5)]
    out["locked_class_members_per_edge"]=[sum(1 for val in memo[i].values() if val[0]) for i in range(5)]
    return out

if __name__=="__main__":
    jobs=[]
    for r in (3,4,5): jobs.append(("A_%d"%r,A(r),0))
    jobs.append(("T4",from_faces(T4F),4))
    for f in ("A3","W6"):
        d=json.load(open(CERT+f+".json")); jobs.append(("lt_cert_"+f,from_rot(d["rot"]),d["v"]))
    for name,adj,v in jobs:
        assert sum(len(a) for a in adj.values())==2*(3*len(adj)-6), name
        print(json.dumps(analyse(name,adj,v)),flush=True)
