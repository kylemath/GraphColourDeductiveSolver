import networkx as nx
def P4(G):
    order=list(nx.dfs_preorder_nodes(G,list(G.nodes())[0])); col={}; cnt=0
    def rec(i):
        nonlocal cnt
        if i==len(order): cnt+=1; return
        v=order[i]
        for c in range(4):
            if all(col.get(u)!=c for u in G[v]): col[v]=c; rec(i+1); del col[v]
    rec(0); return cnt
K=nx.Graph([(0,1),(0,7),(0,9),(1,2),(1,7),(2,3),(2,8),(3,4),(3,8),(4,5),(4,9),(5,6),(5,9),(6,7),(6,8)])
# glue stacked triangulation on edge (0,1): K4 on {0,1,a,b} then stack c in a face
G=K.copy(); a,b,c=10,11,12
G.add_edges_from([(0,a),(1,a),(0,b),(1,b),(a,b),(0,c),(a,c),(b,c)])
n=G.number_of_nodes(); E=G.number_of_edges(); miss=3*n-6-E
print("planar",nx.check_planarity(G)[0],"n",n,"E",E,"2n-3",2*n-3,"miss",miss,"P",P4(G),"bound",24*2**miss,"conn",nx.node_connectivity(G))
