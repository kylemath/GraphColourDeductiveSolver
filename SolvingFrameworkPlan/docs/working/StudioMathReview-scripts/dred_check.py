# Independent D-reducibility check (Birkhoff/Heesch D) for small configurations.
# Configuration: ring 0..r-1 (cycle), interior vertices with adjacency to ring/interior.
import itertools, sys
from functools import lru_cache

def proper_ring(r):
    for k in itertools.product(range(4), repeat=r):
        if all(k[i] != k[(i+1)%r] for i in range(r)) and k[0]==0:
            yield k

def canon(k):
    m={}; out=[]
    for x in k:
        if x not in m: m[x]=len(m)
        out.append(m[x])
    return tuple(out)

def extendable(k, interior, adj_ring, adj_int):
    m=len(interior)
    for lam in itertools.product(range(4), repeat=m):
        ok=True
        for a in range(m):
            if any(lam[a]==k[t] for t in adj_ring[a]): ok=False;break
            if any(lam[a]==lam[b] for b in adj_int[a] if b>a): ok=False;break
        if ok: return True
    return False

PAIRS=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]

def noncrossing_partitions(pos):
    # all set partitions of list pos (in cyclic order) that are non-crossing
    pos=list(pos)
    if not pos: yield []; return
    first=pos[0]; rest=pos[1:]
    # block containing first: choose subset S of rest; then blocks inside gaps
    for mask in range(1<<len(rest)):
        S=[rest[i] for i in range(len(rest)) if mask>>i&1]
        block=[first]+S
        # remaining elements split into gaps between consecutive block elements
        gaps=[]; cur=[]
        bset=set(block)
        for x in rest:
            if x in bset:
                gaps.append(cur); cur=[]
            else: cur.append(x)
        gaps.append(cur)
        def rec(i):
            if i==len(gaps): yield []; return
            for p in noncrossing_partitions(gaps[i]):
                for q in rec(i+1): yield p+q
        for q in rec(0): yield [block]+q

def crossing(b1,b2):
    # cyclic positions; blocks cross if exist a<b<c<d alternating
    s1=set(b1); s2=set(b2)
    allp=sorted(s1|s2)
    lab=[1 if x in s1 else 2 for x in allp]
    # count alternations: crossing iff pattern contains 1..2..1..2 cyclically
    for a,b,c,d in itertools.combinations(range(len(allp)),4):
        if lab[a]==lab[c]!=lab[b]==lab[d]: return True
    return False

def structures(k, pi, r):
    A,Bc=pi
    t1=[i for i in range(r) if k[i] in A]; t2=[i for i in range(r) if k[i] in Bc]
    res=[]
    for P1 in noncrossing_partitions(t1):
        # ring edges between consecutive type-1 vertices force same block
        if not respects(P1,k,A,r): continue
        for P2 in noncrossing_partitions(t2):
            if not respects(P2,k,Bc,r): continue
            if any(crossing(x,y) for x in P1 for y in P2): continue
            res.append((P1,P2))
    return res

def respects(P,k,cols,r):
    blk={}
    for bi,b in enumerate(P):
        for x in b: blk[x]=bi
    for i in range(r):
        j=(i+1)%r
        if k[i] in cols and k[j] in cols and blk[i]!=blk[j]: return False
    return True

def flips(k,P,cols):
    a,b=cols
    for mask in range(1,1<<len(P)):
        kk=list(k)
        for bi,blk in enumerate(P):
            if mask>>bi&1:
                for x in blk: kk[x]= b if kk[x]==a else a
        yield tuple(kk)

def dred(name, r, adj_ring, adj_int):
    m=len(adj_ring)
    cols=sorted(set(canon(k) for k in proper_ring(r)))
    good={k for k in cols if extendable(k, range(m), adj_ring, adj_int)}
    print(name, "ring",r,"classes",len(cols),"extendable",len(good))
    level=0
    while True:
        level+=1
        new=set()
        for k in cols:
            if k in good: continue
            for pi in PAIRS:
                ok=True
                for (P1,P2) in structures(k,pi,r):
                    if not (any(canon(x) in good for x in flips(k,P1,pi[0])) or any(canon(x) in good for x in flips(k,P2,pi[1]))):
                        ok=False;break
                if ok: new.add(k);break
        print(" level",level,"new",len(new))
        if not new: break
        good|=new
    print(" D-reducible:", len(good)==len(cols), "bad:", [k for k in cols if k not in good][:5])

# Birkhoff diamond (RSST 0.7322): ring 1..6 -> 0..5; interior 7,8,9,10 -> 0..3
# 7: 2 8 9 10 1 ; 8: 2 3 4 9 7 ; 9: 8 4 5 10 7 ; 10: 9 5 6 1 7
def build(int_lists, r, base):
    idx={v:i for i,v in enumerate(sorted(int_lists))}
    adj_ring=[[] for _ in idx]; adj_int=[[] for _ in idx]
    for v,nb in int_lists.items():
        for u in nb:
            if u<=r: adj_ring[idx[v]].append(u-1)
            else: adj_int[idx[v]].append(idx[u])
    return adj_ring, adj_int
d_ring,d_int=build({7:[2,8,9,10,1],8:[2,3,4,9,7],9:[8,4,5,10,7],10:[9,5,6,1,7]},6,7)
dred("diamond",6,d_ring,d_int)
c_ring,c_int=build({8:[2,3,9,10,11,1],9:[3,4,5,10,8],10:[9,5,6,11,8],11:[10,6,7,1,8]},7,8)
dred("conf2122",7,c_ring,c_int)
