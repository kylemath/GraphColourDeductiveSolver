# Abstract ring-connection automaton at a (6^5) hole.
import itertools, sys, functools
sys.setrecursionlimit(100000)
# vertices 0..4 link x_t ; 5..14 ring positions 0..9 = w0 m1 w1 m2 w2 m3 w3 m4 w4 m0
RN=['w0','m1','w1','m2','w2','m3','w3','m4','w4','m0']
ADJ=[set() for _ in range(15)]
def ae(a,b): ADJ[a].add(b); ADJ[b].add(a)
for t in range(5):
    ae(t,(t+1)%5)
    for p in ((2*t-2)%10,(2*t-1)%10,(2*t)%10): ae(t,5+p)
for i in range(10): ae(5+i,5+(i+1)%10)
TYPES=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
def type_of(p,q):
    for k,T in enumerate(TYPES):
        if (min(p,q),max(p,q)) in T: return k
# noncrossing homogeneous partitions of 2m alternating arcs
def ncp(n):
    # all noncrossing set partitions of range(n) as label tuples
    res=[]
    def rec(i,lab,blocks):
        if i==n: res.append(tuple(lab)); return
        for b in range(len(blocks)+1):
            # check noncrossing: adding i to block b
            if b<len(blocks):
                last=blocks[b][-1]
                ok=True
                for b2 in range(len(blocks)):
                    if b2==b: continue
                    # any element of b2 strictly between last and i, and an element of b2 outside [blocks[b][0], i]? noncrossing test
                    if any(last<x<i for x in blocks[b2]) and any(x<last for x in blocks[b2]): ok=False;break
                    if any(last<x<i for x in blocks[b2]) and False: pass
                if not ok: continue
                blocks[b].append(i); lab.append(b); rec(i+1,lab,blocks); lab.pop(); blocks[b].pop()
            else:
                blocks.append([i]); lab.append(b); rec(i+1,lab,blocks); lab.pop(); blocks.pop()
    rec(0,[],[])
    # verify noncrossing properly
    out=[]
    for L in res:
        good=True
        for a,b,c_,d in itertools.combinations(range(n),4):
            if L[a]==L[c_] and L[b]==L[d] and L[a]!=L[b]: good=False;break
        if good: out.append(L)
    return out
ARC={}
for m in range(1,6):
    n=2*m
    ARC[m]=[L for L in ncp(n) if all((i-j)%2==0 for i in range(n) for j in range(n) if L[i]==L[j])]
def structures(c,T):
    """list of ring-label tuples (length 10) = outside-join structures for type T"""
    P0=TYPES[T][0]
    cls=[c[5+i] in P0 for i in range(10)]
    if all(x==cls[0] for x in cls): return [tuple([0]*10)]
    # rotate so position 0 starts an arc
    s=[i for i in range(10) if cls[i]!=cls[i-1]][0]
    arcs=[]; cur=[]
    for k in range(10):
        i=(s+k)%10
        if cur and cls[i]!=cls[cur[-1]]: arcs.append(cur); cur=[]
        cur.append(i)
    arcs.append(cur)
    m=len(arcs)//2
    out=[]
    for L in ARC[m]:
        lab=[0]*10
        for a,arc in enumerate(arcs):
            for i in arc: lab[i]=L[a]
        out.append(tuple(lab))
    return out
def comps(c,p,q,R):
    """components (frozensets of ball vertices) of pq-subgraph of ball + outside joins R"""
    par=list(range(15))
    def f(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    S=[v for v in range(15) if c[v] in (p,q)]
    for v in S:
        for w in ADJ[v]:
            if c[w] in (p,q): par[f(v)]=f(w)
    if R is not None:
        first={}
        for i in range(10):
            if c[5+i] in (p,q):
                if R[i] in first: par[f(5+i)]=f(first[R[i]])
                else: first[R[i]]=5+i
    d={}
    for v in S: d.setdefault(f(v),set()).add(v)
    return [frozenset(K) for K in d.values()]
def flip(c,K,p,q):
    c=list(c)
    for v in K: c[v]= q if c[v]==p else p
    return tuple(c)
def filled(c): return len(set(c[:5]))<=3
def linkonly_moves(c):
    out=set()
    for p,q in itertools.combinations(range(4),2):
        for K in comps(c,p,q,None):
            if all(v<5 for v in K): out.add(flip(c,K,p,q))
    return out
def canonR(R):
    m={}; return tuple(m.setdefault(x,len(m)) for x in R)
@functools.lru_cache(maxsize=None)
def g(k,c,T,R):
    if filled(c): return True
    if k==0: return False
    if g(k-1,c,T,R): return True
    for c2 in linkonly_moves(c):
        if g(k-1,c2,T,R): return True
    for pq in TYPES[T]:
        p,q=pq
        for K in comps(c,p,q,R):
            if all(v<5 for v in K): continue
            c2=flip(c,K,p,q)
            if V(k-1,c2,T,R): return True
    return False
def V(k,c,T,R):
    if g(k,c,T,R): return True
    for T2 in range(3):
        if T2!=T and A(k,c,T2): return True
    return False
@functools.lru_cache(maxsize=None)
def A(k,c,T):
    return all(g(k,c,T,canonR(R)) for R in structures(c,T))
def DLlocks(c):
    """returns (j, lock1 pair, lock2 pair) for 4-coloured link"""
    L=c[:5]
    j=[t for t in range(5) if L[t]==L[(t+2)%5]][0]
    x1,x3,x4=(j+1)%5,(j+3)%5,(j+4)%5
    return j,(x1,x3,(L[x1],L[x3])),(x1,x4,(L[x1],L[x4]))
def has_lock(c,R,lock):
    a,b,(p,q)=lock
    for K in comps(c,p,q,R):
        if a in K: return b in K
def lockT(lock): return type_of(*lock[2])
pats=open('../six/local.txt').read().split()
CM={'a':0,'b':1,'g':2,'d':3}
def init(pat): return tuple([0,1,0,2,3]+[CM[x] for x in pat])
def radius_bound(c,k):
    j,l1,l2=DLlocks(c)
    for T in range(3):
        ok=True
        for R in structures(c,T):
            R=canonR(R)
            if lockT(l1)==T and not has_lock(c,R,l1): continue
            if lockT(l2)==T and not has_lock(c,R,l2): continue
            if not g(k,c,T,R): ok=False;break
        if ok: return T
    return None
if __name__=='__main__':
    print({m:len(ARC[m]) for m in ARC})
    K=int(sys.argv[1]) if len(sys.argv)>1 else 3
    for k in range(1,K+1):
        bad=[p for p in pats if radius_bound(init(p),k) is None]
        print('k',k,'unresolved',len(bad),bad[:10],flush=True)
