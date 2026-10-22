import itertools, math
E={1:(1,0),2:(-.5,math.sqrt(3)/2),3:(-.5,-math.sqrt(3)/2)}
add=lambda a,b:(a[0]+b[0],a[1]+b[1]); sc=lambda s,a:(s*a[0],s*a[1]); nrm=lambda a:math.hypot(*a)
# 1. hole: degree-6 vertex removed, rim 6-cycle, alternating face sign
res={}
for cyc in itertools.product(range(4),repeat=6):
    if any(cyc[i]==cyc[(i+1)%6] for i in range(6)): continue
    H=(0,0)
    for i in range(6): H=add(H,sc((-1)**i,E[cyc[i]^cyc[(i+1)%6]]))
    k=len(set(cyc)); res.setdefault(k,set()).add(round(nrm(H),3))
print('hole monodromy |t| by #colours on link:',res)
# 4. wheel W_d: rim colours in {1,2,3} (hub 0); boundary gauge s flips each step (one interior edge per rim vertex)
def walk(r,start):
    d=len(r); r=r[start:]+r[:start]; H=[(0,0)]; s=1
    for i in range(d):
        H.append(add(H[-1],sc(s,E[r[i]^r[(i+1)%d]]))); s=-s
    return H
def tau(H,odd):
    if odd:
        q=sc(.5,add(H[0],H[-1])); return max(nrm(add(h,sc(-1,q))) for h in H)
    # even: min over half-lattice centres
    best=9
    for a in range(-8,9):
        for b in range(-8,9):
            p=add(sc(a/2,E[1]),sc(b/2,E[2])); best=min(best,max(nrm(add(h,sc(-1,p))) for h in H))
    return best
def maxalt(r):
    # longest cyclic run of 2-colour alternation (vertices)
    d=len(r); best=0
    for s in range(d):
        cols={r[s]}; n=1
        while n<d:
            c=r[(s+n)%d]; cols.add(c)
            if len(cols)>2: break
            n+=1
        best=max(best,n)
    return best
for d in range(4,13):
    lv=[];allr=0
    for r in itertools.product((1,2,3),repeat=d):
        if any(r[i]==r[(i+1)%d] for i in range(d)): continue
        allr+=1
        t=min(tau(walk(list(r),s),d%2) for s in range(d))
        if t<=1+1e-9: lv.append(maxalt(r))
    print('W_%d: rim colourings %d, level %d, min alternation run among level %s'%(d,allr,len(lv),min(lv) if lv else None), flush=True)
# 6. frozen period-4 rainbow row on straight cylinder, L=8,12: forced successor and t
for L in (4,8,12):
    r=[i%4 for i in range(L)]
    succ=[q for q in itertools.product(range(4),repeat=L) if all(q[i]!=q[(i+1)%L] for i in range(L)) and all(q[i] not in (r[i],r[(i+1)%L]) for i in range(L))]
    H=(0,0)
    for i in range(L): H=add(H,E[r[i]^r[(i+1)%L]])
    print('L=%d rainbow row: #successors %d, |t|=%.2f'%(L,len(succ),nrm(H)))
