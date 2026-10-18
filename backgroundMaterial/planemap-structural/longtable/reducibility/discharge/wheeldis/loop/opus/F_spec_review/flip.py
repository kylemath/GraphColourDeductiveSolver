import networkx as nx, sys
def parse(l):
    f=l.split(); r=int(f[1]); m=int(f[2]); rp=f[3].split(';'); ip=f[4].split(';')
    H=nx.Graph()
    for k in range(r): H.add_edge(('r',k),('r',(k+1)%r)); H.add_edge('apex',('r',k))
    for u in range(m):
        if rp[u]!='-':
            for x in rp[u].split(','): H.add_edge(('i',u),('r',int(x)))
        if ip[u]!='-':
            for x in ip[u].split(','): H.add_edge(('i',u),('i',int(x)))
    ok,emb=nx.check_planarity(H); assert ok
    rot={}
    for u in range(m):
        rot[u]=list(emb.neighbors_cw_order(('i',u)))
    return f[0],r,m,rot
def system(m,rot):
    # rotation over interior nbrs with ring-gap counts: S[u] = list of (nbr or 'R')
    return {u:[x[1] if x[0]=='i' else 'R' for x in rot[u]] for u in range(m)}
def canon(S):
    best=None
    for s in S:
        for d in range(len(S[s])):
            if S[s][d]=='R': continue
            for orient in (1,-1):
                lab={s:0}; q=[(s,d)]; code=[]
                # BFS: for each vertex in label order, list rotation starting at its entry dart
                start={s:d}; order=[s]; i=0
                while i<len(order):
                    u=order[i]; i+=1; L=S[u]; n=len(L); st=start[u]
                    seq=[L[(st+orient*k)%n] for k in range(n)]
                    row=[]
                    for x in seq:
                        if x=='R': row.append(-1); continue
                        if x not in lab:
                            lab[x]=len(lab); order.append(x)
                            # entry dart at x pointing to u
                            start[x]=S[x].index(u)
                        row.append(lab[x])
                    code.append(tuple(row))
                code=tuple(code)
                if best is None or code<best: best=code
    return best
def flips(m,S):
    G=nx.Graph(); G.add_nodes_from(range(m))
    for u in S:
        for x in S[u]:
            if x!='R': G.add_edge(u,x)
    out=[]
    for c in nx.articulation_points(G):
        H=G.copy(); H.remove_node(c)
        comps=list(nx.connected_components(H))
        for C2 in comps:
            T={u:list(S[u]) for u in S}
            for u in C2: T[u]=T[u][::-1]
            # at c: reverse each maximal block of C2 nbrs together with... reverse order of the C2 segment
            L=S[c]; n=len(L)
            idx=[k for k in range(n) if L[k]!='R' and L[k] in C2]
            # C2 nbrs form a contiguous (cyclic) segment; rotate so it starts at 0
            k0=[k for k in idx if (L[(k-1)%n]=='R' or L[(k-1)%n] not in C2)]
            assert len(k0)==1,(c,L)
            seg=[]; k=k0[0]
            while L[k%n]!='R' and L[k%n] in C2: seg.append(k%n); k+=1
            vals=[L[j] for j in seg][::-1]
            for j,v in zip(seg,vals): T[c][j]=v
            out.append((c,sorted(C2),T))
    return out
for l in open(sys.argv[1]):
    if not l.strip(): continue
    nm,r,m,rot=parse(l); S=system(m,rot)
    cK=canon(S); mir={u:S[u][::-1] for u in S}; cM=canon(mir)
    fl=flips(m,S)
    res=[]
    for c,C2,T in fl:
        cT=canon(T); res.append((c,C2,'same' if cT in (cK,cM) else 'DIFFERENT'))
    print(nm,r,m,'cutvertices:',res)
