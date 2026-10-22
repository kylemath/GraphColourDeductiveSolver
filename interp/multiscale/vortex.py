# Single-vertex case: triangular-lattice hexagonal disc G, A=G-v, B={v}.
import itertools, math
from collections import deque
from pysat.solvers import Minisat22
from tilt import DIRS, E
def hexdisc(r):
    V=[(i,j) for i in range(-r,r+1) for j in range(-r,r+1) if max(abs(i),abs(j),abs(i+j))<=r]
    idx={v:k for k,v in enumerate(V)}
    adj=[[idx[(v[0]+d[0],v[1]+d[1])] for d in DIRS if (v[0]+d[0],v[1]+d[1]) in idx] for v in V]
    return V,idx,adj
SG={(1,0):1,(0,1):-1,(-1,1):1,(-1,0):-1,(0,-1):1,(1,-1):-1}
def mono(cols):  # cols of link w_k = DIRS[k], ccw
    s=[0,0]
    for k in range(6):
        a=DIRS[k]; b=DIRS[(k+1)%6]; d=(b[0]-a[0],b[1]-a[1]); lab=cols[k]^cols[(k+1)%6]
        e=E[lab]; s[0]+=SG[d]*e[0]; s[1]+=SG[d]*e[1]
    return (round(s[0],6),round(s[1],6))
links={}
for cols in itertools.product(range(4),repeat=6):
    if all(cols[k]!=cols[(k+1)%6] for k in range(6)):
        links.setdefault(mono(cols),[]).append(cols)
for m,l in sorted(links.items(),key=lambda t:-math.hypot(*t[0])):
    print("monodromy",m,"norm",round(math.hypot(*m),3),"#link colourings",len(l),"e.g.",l[0], "uses4" ,any(len(set(c))==4 for c in l))
def solve(V,adj,fixed,free):
    s=Minisat22(); var=lambda k,c:4*k+c+1; fs=set(free)
    for k in free:
        s.add_clause([var(k,c) for c in range(4)])
        for w in adj[k]:
            for c in range(4):
                if w in fs:
                    if w>k: s.add_clause([-var(k,c),-var(w,c)])
                elif w in fixed and fixed[w]==c: s.add_clause([-var(k,c)])
    ok=s.solve(); m=s.get_model() if ok else None; s.delete()
    if not ok: return None
    return {k:c for k in free for c in range(4) if m[var(k,c)-1]>0}
r=9
V,idx,adj=hexdisc(r); v0=idx[(0,0)]
target=[c for m,l in links.items() if math.hypot(*m)>0.5 for c in l if len(set(c))==4][0]
fixed={idx[DIRS[k]]:target[k] for k in range(6)}
rest=[k for k in range(len(V)) if k!=v0 and k not in fixed]
col=solve(V,adj,fixed,rest); assert col is not None; col.update(fixed)
print("colouring of G-v with link",target,"monodromy",mono(target))
# repair test: v gets any colour (renaming), recolour within R of conflicts
for R in range(0,r):
    okany=False
    for cv in range(4):
        full=dict(col); full[v0]=cv
        K=[k for k in full if any(full[k]==full[w] for w in adj[k])]
        dist={k:0 for k in K}; dq=deque(K)
        while dq:
            x=dq.popleft()
            if dist[x]==R: continue
            for w in adj[x]:
                if w not in dist: dist[w]=dist[x]+1; dq.append(w)
        free=list(dist); fx={k:full[k] for k in full if k not in dist}
        if solve(V,adj,fx,free) is not None: okany=True;break
    print("r=%d R=%d repair possible: %s"%(r,R,okany))
