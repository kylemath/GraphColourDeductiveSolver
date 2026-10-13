import networkx as nx, itertools
def P4(G):
    V=list(G.nodes()); idx={v:i for i,v in enumerate(V)}
    order=sorted(V,key=lambda v:-G.degree(v))
    # BFS order for pruning
    order=list(nx.bfs_tree(G,order[0]).nodes()) if nx.is_connected(G) else V
    col={}; cnt=0
    def rec(i):
        nonlocal cnt
        if i==len(order): cnt+=1; return
        v=order[i]
        for c in range(4):
            if all(col.get(u)!=c for u in G[v]):
                col[v]=c; rec(i+1); del col[v]
    rec(0); return cnt
I=nx.icosahedral_graph()
print("P(ico)",P4(I))
G=I.copy(); v=0; L=list(I[v]); G.remove_node(v)
n=G.number_of_nodes(); E=G.number_of_edges(); miss=3*n-6-E
print("ico-v n",n,"E",E,"miss",miss,"P",P4(G),"bound",24*2**miss)
link=nx.cycle_graph(0)
H=I.subgraph(L)
print("link cycle?",sorted(d for _,d in H.degree()))
for u,w in itertools.combinations(L,2):
    if not G.has_edge(u,w):
        Gc=nx.contracted_nodes(G,u,w,self_loops=False)
        Ge=G.copy(); Ge.add_edge(u,w)
        t=len(set(G[u])&set(G[w]))
        print("chord",u,w,"t",t,"P(G/e)",P4(Gc),"P(G+e)",P4(Ge),"half-bound",12*2**miss)
