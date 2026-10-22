# Vortex absorption test: the tilted|flat seam (c22 | c3) on a lattice parallelogram, with edge flips
# (each creates two degree-5 and two degree-7 vertices) placed in A along the seam every s columns.
import sys, itertools
from collections import deque
from pysat.solvers import Minisat22
from tilt import build, c22, c3, PERMS
def minR_graph(adj,colA,isA,colB,Rmax):
    n=len(adj)
    for R in range(Rmax+1):
        for p in PERMS:
            col=[colA[k] if isA[k] else p[colB[k]] for k in range(n)]
            K=[k for k in range(n) if any(col[k]==col[w] for w in adj[k])]
            if not K: return 0
            dist={k:0 for k in K}; dq=deque(K)
            while dq:
                x=dq.popleft()
                if dist[x]==R: continue
                for w in adj[x]:
                    if w not in dist: dist[w]=dist[x]+1; dq.append(w)
            s=Minisat22(); var=lambda k,c:4*k+c+1
            for k in dist:
                s.add_clause([var(k,c) for c in range(4)])
                for w in adj[k]:
                    for c in range(4):
                        if w in dist:
                            if w>k: s.add_clause([-var(k,c),-var(w,c)])
                        elif col[w]==c: s.add_clause([-var(k,c)])
            ok=s.solve(); s.delete()
            if ok: return R
    return None
L=36; D=14
for s in [None,18,12,8,6,4,3]:
    for row in [-2,-3]:
        V,idx,adj=build(L,D); adj=[set(a) for a in adj]
        isA=[v[1]<0 for v in V]; cA=[c22(v) for v in V]; cB=[c3(v) for v in V]
        nflip=0
        if s:
            for i in range(1,L-1,s):
                a,b=idx[(i,row)],idx[(i+1,row)]
                c,d=[w for w in adj[a]&adj[b]]
                if all(isA[x] for x in (a,b,c,d)) and cA[c]!=cA[d]:
                    adj[a].discard(b); adj[b].discard(a); adj[c].add(d); adj[d].add(c); nflip+=1
        assert all(cA[k]!=cA[w] for k in range(len(V)) if isA[k] for w in adj[k] if isA[w])
        R=minR_graph([sorted(a) for a in adj],cA,isA,cB,Rmax=D-2)
        print("L=%d spacing=%s flipRow=%d flips=%d  minR=%s"%(L,s,row,nflip,R),flush=True)
        if not s: break
