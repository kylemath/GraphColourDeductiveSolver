# Planar rigid counterexample: stacked triangulation, A = odd core + two pendant chains, B = even core.
import networkx as nx
from collections import deque
from pysat.solvers import Minisat22
import itertools
def build(m,k):
    G=nx.Graph(); x=lambda i:('x',i)
    G.add_edges_from([(x(1),x(2)),(x(2),x(3)),(x(1),x(3))])
    for i in range(4,m+1):  # insert x_i into face (i-3,i-2,i-1)
        for j in (i-3,i-2,i-1): G.add_edge(x(i),x(j))
    def chain(name,face):
        tri=list(face)
        for t in range(1,k+1):
            u=(name,t); G.add_edges_from((u,w) for w in tri); tri=[tri[1],tri[2],u]
    chain('y',(x(1),x(2),x(4)))          # face (i,i+1,i+3), i=1 -> chain goes into (x2,x4,y1)...
    chain('z',(x(m-3),x(m-2),x(m)))
    return G
def solve(nodes,G,fixed):
    s=Minisat22(); vid={u:n for n,u in enumerate(nodes)}; var=lambda u,c:4*vid[u]+c+1
    for u in nodes:
        s.add_clause([var(u,c) for c in range(4)])
        for w in G[u]:
            for c in range(4):
                if w in vid:
                    if vid[w]>vid[u]: s.add_clause([-var(u,c),-var(w,c)])
                elif w in fixed and fixed[w]==c: s.add_clause([-var(u,c)])
    ok=s.solve(); M=s.get_model() if ok else None; s.delete()
    return None if not ok else {u:c for u in nodes for c in range(4) if M[var(u,c)-1]>0}
m,k=24,40
G=build(m,k); print("planar:",nx.check_planarity(G)[0],"n=",G.number_of_nodes(),"maxdeg",max(d for _,d in G.degree()))
# unique colourability check: fix a triangle, look for a second colouring
cU=solve(list(G),G,{}); 
s2=None
tri=[('x',1),('x',2),('x',3)]
A=[u for u in G if not (u[0]=='x' and u[1]%2==0)]; B=[u for u in G if u not in A]
print("A connected",nx.is_connected(G.subgraph(A)),"B connected",nx.is_connected(G.subgraph(B)))
# second colouring of G with same triangle colours?
fx={u:cU[u] for u in tri}; nodes=[u for u in G if u not in fx]
sv=Minisat22()  # cheap: count via blocking
sol=solve(nodes,G,fx)
diff=[u for u in nodes if sol[u]!=cU[u]]; print("colouring with same triangle differs at",len(diff),"vertices (0 => consistent w/ uniqueness)")
sigma=[1,0,2,3]
fixed={u:cU[u] for u in G if u[0]=='y'}; fixed.update({u:sigma[cU[u]] for u in G if u[0]=='z'})
odd=[u for u in A if u[0]=='x']
cA=solve(odd,G.subgraph(A),fixed); assert cA; cA.update(fixed)
for R in range(0,12):
    good=None
    for p in itertools.permutations(range(4)):
        col=dict(cA); col.update({u:p[cU[u]] for u in B})
        K=[u for u in G if any(col[u]==col[w] for w in G[u])]
        dist={u:0 for u in K}; dq=deque(K)
        while dq:
            a=dq.popleft()
            if dist[a]==R: continue
            for w in G[a]:
                if w not in dist: dist[w]=dist[a]+1; dq.append(w)
        if solve(list(dist),G,{u:col[u] for u in G if u not in dist}) is not None: good=p;break
    print("R=%d repair possible: %s"%(R,good is not None))
    if good: break
