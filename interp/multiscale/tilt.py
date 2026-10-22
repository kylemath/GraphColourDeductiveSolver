import itertools, math, sys
from collections import deque
from pysat.solvers import Minisat22
# triangular lattice: vertex (i,j), neighbours +-(1,0), +-(0,1), +-(1,-1)  (e1, e2 at 60 deg)
DIRS=[(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)]
def build(L,D):
    V=[(i,j) for i in range(L+1) for j in range(-D,D)]
    idx={v:k for k,v in enumerate(V)}
    adj=[[] for _ in V]
    for v in V:
        for d in DIRS:
            w=(v[0]+d[0],v[1]+d[1])
            if w in idx: adj[idx[v]].append(idx[w])
    return V,idx,adj
# colours as elements of Z2^2 encoded 0..3 (xor = addition)
def c22(v): return (v[0]%2) | ((v[1]%2)<<1)
C3MAP=[0,1,2]
def c3(v): return C3MAP[(v[0]+2*v[1])%3]
E={1:(1,0),2:(-.5,math.sqrt(3)/2),3:(-.5,-math.sqrt(3)/2)}  # e_g,e_h,e_{g+h}; sum 0
def height_inc(u,w,col):
    # +e_label if up triangle on left of u->w. up triangles: (v, v+e1, v+e2)
    d=(w[0]-u[0],w[1]-u[1]); lab=col(u)^col(w); assert lab
    sgn={(1,0):1,(0,1):-1,(-1,1):1,(-1,0):-1,(0,-1):1,(1,-1):-1}[d]
    e=E[lab]; return (sgn*e[0],sgn*e[1])
def check_height(col,V,idx):
    # check closedness around every lattice triangle
    for v in V:
        for (a,b) in [((1,0),(0,1)),((0,1),(-1,1))]:
            p=[v,(v[0]+a[0],v[1]+a[1]),(v[0]+b[0],v[1]+b[1])]
            if all(q in idx for q in p):
                s=[0,0]
                for x,y in [(p[0],p[1]),(p[1],p[2]),(p[2],p[0])]:
                    h=height_inc(x,y,col); s[0]+=h[0]; s[1]+=h[1]
                assert abs(s[0])<1e-9 and abs(s[1])<1e-9,(v,s)
def row_increment(col,j,L):
    s=[0,0]
    for i in range(L):
        h=height_inc((i,j),(i+1,j),col); s[0]+=h[0]; s[1]+=h[1]
    return math.hypot(*s)
PERMS=list(itertools.permutations(range(4)))
def minR(L,D,colA,colB,Rmax=None):
    V,idx,adj=build(L,D)
    isA=[v[1]<0 for v in V]
    best=None
    if Rmax is None: Rmax=D
    for R in range(0,Rmax+1):
        for p in PERMS:
            col=[colA(v) if isA[k] else p[colB(v)] for k,v in enumerate(V)]
            K=[k for k in range(len(V)) if any(col[k]==col[w] for w in adj[k])]
            dist=[None]*len(V); dq=deque(K)
            for k in K: dist[k]=0
            while dq:
                x=dq.popleft()
                if dist[x]==R: continue
                for w in adj[x]:
                    if dist[w] is None: dist[w]=dist[x]+1; dq.append(w)
            free=[k for k in range(len(V)) if dist[k] is not None]
            if not K: return 0,p
            var=lambda k,c: 4*k+c+1
            s=Minisat22(); fs=set(free)
            for k in free:
                s.add_clause([var(k,c) for c in range(4)])
                for w in adj[k]:
                    for c in range(4):
                        if w in fs:
                            if w>k: s.add_clause([-var(k,c),-var(w,c)])
                        elif col[w]==c: s.add_clause([-var(k,c)])
            ok=s.solve(); s.delete()
            if ok: return R,p
    return None,None
if __name__=="__main__":
    V,idx,adj=build(12,6)
    for name,col in [("c22",c22),("c3",c3)]:
        assert all(col(V[k])!=col(V[w]) for k in range(len(V)) for w in adj[k])
        check_height(col,V,idx)
        print(name,"row height increment over 12 steps:",round(row_increment(col,0,12),3))
    for L in [3,6,9,12,15,18,21,24,30,36]:
        D=L//2+4
        R,p=minR(L,D,c22,c3)
        print("L=%d D=%d  minR(c22 | c3)=%s  bound ceil((L-6)/4)=%d"%(L,D,R,max(0,math.ceil((L-6)/4))),flush=True)
