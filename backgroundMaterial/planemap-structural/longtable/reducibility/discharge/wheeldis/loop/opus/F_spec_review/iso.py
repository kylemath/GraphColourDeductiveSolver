import networkx as nx,sys
def H(l):
    f=l.split(); r=int(f[1]); m=int(f[2]); rp=f[3].split(';'); ip=f[4].split(';')
    G=nx.Graph()
    for k in range(r): G.add_edge(('r',k),('r',(k+1)%r)); G.add_edge('apex',('r',k))
    for u in range(m):
        for x in ([] if rp[u]=='-' else rp[u].split(',')): G.add_edge(('i',u),('r',int(x)))
        for x in ([] if ip[u]=='-' else ip[u].split(',')): G.add_edge(('i',u),('i',int(x)))
    for v in G: G.nodes[v]['t']=v[0] if v!='apex' else 'a'
    for u in range(m): G.nodes[('i',u)]['t']='i%d'%G.degree(('i',u))
    assert nx.check_planarity(G)[0]
    return G
L=[l for l in open(sys.argv[1]) if l.strip()]
Gs=[H(l) for l in L]
nm=lambda a,b:a['t']==b['t']
for i in range(len(L)):
    for j in range(i+1,len(L)):
        print(L[i].split()[0],L[j].split()[0],nx.is_isomorphic(Gs[i],Gs[j],node_match=nm))
