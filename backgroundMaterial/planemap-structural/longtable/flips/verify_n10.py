import networkx as nx, itertools, sys
lines=open('run2/tri-10.txt').read().split('\n')
def build(t, idxs):
    parts=lines[t].split(); n=int(parts[0]); rot=[list(map(int,p.split(','))) for p in parts[1:]]
    E=[]
    for u in range(n):
        for v in rot[u]:
            if u<v: E.append((u,v))
    return n,[E[i] for i in idxs]
def P4(G):
    order=list(nx.dfs_preorder_nodes(G,0)); col={}; cnt=0
    def rec(i):
        nonlocal cnt
        if i==len(order): cnt+=1; return
        v=order[i]
        for c in range(4):
            if all(col.get(u)!=c for u in G[v]): col[v]=c; rec(i+1); del col[v]
    rec(0); return cnt
for t,idx in [(2,[0,1,2,4,6,8,9,11,12,13,14,16,17,20,21]),(4,[0,1,2,4,5,7,9,10,11,14,15,17,18,19,21,23]),(2,[0,1,2,4,6,8,9,10,11,14,15,17,18,19,20])]:
    n,E=build(t,idx); G=nx.Graph(E)
    ok,emb=nx.check_planarity(G); seen=set(); faces=[]
    for u,v in emb.edges():
        if (u,v) in seen: continue
        faces.append(emb.traverse_face(u,v,mark_half_edges=seen))
    miss=3*n-6-G.number_of_edges(); P=P4(G)
    print("n",n,"E",G.number_of_edges(),"planar",ok,"3-conn",nx.node_connectivity(G),"degs",sorted(d for _,d in G.degree()),
          "faces",sorted(len(f) for f in faces),"miss",miss,"P",P,"bound",24*2**miss)
    print("  edges",sorted(E)); print("  faces",[f for f in faces if len(f)>3])
