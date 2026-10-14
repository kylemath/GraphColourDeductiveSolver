# Independent Birkhoff/Heesch vertex-Kempe D-closure for the 66666 wheel (ring 10).
import itertools,sys
n=10
ringnb={1:[9,0,1],2:[1,2,3],3:[3,4,5],4:[5,6,7],5:[7,8,9]}
def extends(k):
    for c0 in range(4):
        for cs in itertools.product(range(4),repeat=5):
            ok=all(cs[i]!=c0 for i in range(5)) and all(cs[i]!=cs[(i+1)%5] for i in range(5))
            if ok and all(k[r]!=cs[i-1] for i in range(1,6) for r in ringnb[i]): return True
    return False
def norm(k):
    m={};out=[]
    for c in k:
        if c not in m: m[c]=len(m)
        out.append(m[c])
    return tuple(out)
cols=set()
for k in itertools.product(range(4),repeat=n):
    if all(k[i]!=k[(i+1)%n] for i in range(n)): cols.add(norm(k))
cols=sorted(cols); print('classes',len(cols))
good={k for k in cols if extends(k)}; print('directly extendable',len(good))
# non-crossing partitions of 0..n-1
def ncp(pts):
    if not pts: yield []; return
    first=pts[0]; rest=pts[1:]
    # block containing first: choose subset of rest, must be non-crossing => recurse on gaps
    for r in range(len(rest)+1):
        for comb in itertools.combinations(range(len(rest)),r):
            blk=[first]+[rest[i] for i in comb]
            idx=[-1]+list(comb)+[len(rest)]
            gaps=[rest[idx[j]+1:idx[j+1]] for j in range(len(idx)-1)]
            def rec(g):
                if not g: yield []; return
                for p in ncp(g[0]):
                    for q in rec(g[1:]): yield p+q
            for p in rec(gaps): yield [blk]+p
NCP=list(ncp(list(range(n)))); print('ncp',len(NCP))
pairings=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
VC={}
def valid(typ):
    typ=tuple(typ)
    if typ in VC: return VC[typ]
    out=[]
    for P in NCP:
        bid={}
        for j,b in enumerate(P):
            for v in b: bid[v]=j
        if any(len({typ[v] for v in b})>1 for b in P): continue
        if any(typ[i]==typ[(i+1)%n] and bid[i]!=bid[(i+1)%n] for i in range(n)): continue
        out.append(P)
    VC[typ]=out; return out
def good_step(k,good):
    for A,B in pairings:
        typ=[0 if c in A else 1 for c in k]
        sw={A[0]:A[1],A[1]:A[0],B[0]:B[1],B[1]:B[0]}
        allok=True
        for P in valid(typ):
            found=False
            for mask in range(1,1<<len(P)):
                k2=list(k)
                for j,b in enumerate(P):
                    if mask>>j&1:
                        for v in b: k2[v]=sw[k2[v]]
                if norm(k2) in good: found=True;break
            if not found: allok=False;break
        if allok: return True
    return False
it=0
while True:
    it+=1
    new={k for k in cols if k not in good and good_step(k,good)}
    print('iter',it,'new',len(new)); sys.stdout.flush()
    if not new: break
    good|=new
print('closure',len(good),'of',len(cols))
three=[k for k in cols if max(k)<=2]
print('3-colourings',len(three),'in closure',sum(k in good for k in three))
bad3=[k for k in three if k not in good]; print('unreached 3-col examples',bad3[:5])
