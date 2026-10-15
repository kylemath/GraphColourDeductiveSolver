import itertools
def ncm(pts):
    if not pts: return [[]]
    a=pts[0]; rest=pts[1:]; out=[]
    for j in range(0,len(rest),2):
        for m1 in ncm(rest[:j]):
            for m2 in ncm(rest[j+1:]):
                out.append([(a,rest[j])]+m1+m2)
    return out
def faces(n2,M):
    # arcs 0..n2-1; arc j between transitions j and j+1; union-find on arcs not separated
    def same(j,jp):
        for (a,b) in M:
            lo,hi=min(a,b),max(a,b)
            if (lo<=j<hi)!=(lo<=jp<hi): return False
        return True
    lab=[-1]*n2; c=0
    for j in range(n2):
        if lab[j]<0:
            for jp in range(n2):
                if same(j,jp): lab[jp]=c
            c+=1
    return lab
def canon(col):
    mp={}; out=[]
    for x in col:
        if x not in mp: mp[x]=len(mp)
        out.append(mp[x])
    return tuple(out)
def classes(r):
    return sorted({canon(c) for c in itertools.product(range(4),repeat=r) if all(c[i]!=c[(i+1)%r] for i in range(r))})
def options(k,r,th):
    T=[v for v in range(r) if (k[v]^k[(v+1)%r]) not in (0,th)]
    if not T: return None
    n2=len(T)
    arc=lambda v: (sum(1 for t in T if t<v)+n2-1)%n2
    opts=[]
    for M in ncm(list(range(n2))):
        lab=faces(n2,M); nf=max(lab)+1
        res=set()
        for s in range(1,2**nf):
            nk=tuple(k[v]^th if (s>>lab[arc(v)])&1 else k[v] for v in range(r))
            res.add(canon(nk))
        opts.append(frozenset(res))
    return opts
def closed_sets(r):
    C=classes(r); out=[]
    for mask in range(1,2**len(C)):
        S={C[i] for i in range(len(C)) if mask>>i&1}
        ok=True
        for k in S:
            for th in (1,2,3):
                o=options(k,r,th)
                if o is None: continue
                if not any(res<=S for res in o): ok=False;break
            if not ok: break
        if ok: out.append(frozenset(S))
    return C,out
for r in (4,5):
    C,cs=closed_sets(r)
    print('r',r,'classes',len(C),'closed sets',len(cs))
    minimal=[S for S in cs if not any(T<S for T in cs)]
    print(' minimal closed sets:',[sorted(S) for S in minimal])
    disj=[(a,b) for a in cs for b in cs if not (a&b)]
    print(' disjoint pairs:',len(disj))

print('--- r=4 with side facts')
C,cs=closed_sets(4)
peq=lambda k: k[0]==k[2]; qeq=lambda k: k[1]==k[3]
facts={
 'chord pr & qs (S has p!=r and S has q!=s)': lambda S: any(not peq(k) for k in S) and any(not qeq(k) for k in S),
 'identify p~r & q~s': lambda S: any(peq(k) for k in S) and any(qeq(k) for k in S),
 'identify p~r only': lambda S: any(peq(k) for k in S),
 'chord pr only': lambda S: any(not peq(k) for k in S),
}
for name,F in facts.items():
    good=[S for S in cs if F(S)]
    disj=[(a,b) for a in good for b in good if not (a&b)]
    print(name, 'sets',len(good),'disjoint pairs',len(disj), [ (sorted(a),sorted(b)) for a,b in disj[:2]])

print('--- r=5 with chord facts')
C,cs=closed_sets(5)
fans=[[(v,(v+2)%5),(v,(v+3)%5)] for v in range(5)]   # the 5 triangulations of the pentagon
def ok(k,ch): return all(k[a]!=k[b] for a,b in ch)
F1=lambda S: all(any(ok(k,ch) for k in S) for ch in fans)
single=[[(v,(v+2)%5)] for v in range(5)]
F2=lambda S: all(any(ok(k,ch) for k in S) for ch in single)
for name,F in (('all 5 fan triangulations',F1),('each single chord',F2)):
    good=[S for S in cs if F(S)]
    disj=[(a,b) for a in good for b in good if not (a&b)]
    print(name,'sets',len(good),'disjoint pairs',len(disj), [ (sorted(a),sorted(b)) for a,b in disj[:1]])
# identifications v~v+2 (contract the face into side): colouring with k[a]==k[b]
ident=[(v,(v+2)%5) for v in range(5)]
F3=lambda S: all(any(k[a]==k[b] for k in S) for a,b in ident)
F4=lambda S: F1(S) and F3(S)
for name,F in (('all identifications',F3),('fans + identifications',F4)):
    good=[S for S in cs if F(S)]
    disj=[(a,b) for a in good for b in good if not (a&b)]
    print(name,'sets',len(good),'disjoint pairs',len(disj), [ (sorted(a),sorted(b)) for a,b in disj[:1]])

print('--- r=5 with replacement facts (other side replaced by a small disc)')
star=lambda S: any(len(set(k))<=3 for k in S)          # other side -> one vertex seeing all 5
# other side -> edge xy, x sees v0 v1 v2 (and y), y sees v2 v3 v4 v0 (and x): extends iff ...
def edge_ext(k,v):
    a,b,c,d,e=[k[(v+i)%5] for i in range(5)]
    for x in range(4):
        if x in (a,b,c): continue
        for y in range(4):
            if y!=x and y not in (c,d,e,a): return True
    return False
edge=lambda S: all(any(edge_ext(k,v) for k in S) for v in range(5))
for name,F in (('star',star),('star+edge',lambda S: star(S) and edge(S)),('star+fans',lambda S: star(S) and F1(S))):
    good=[S for S in cs if F(S)]
    disj=[(a,b) for a in good for b in good if not (a&b)]
    print(name,'sets',len(good),'disjoint pairs',len(disj), [ (sorted(a),sorted(b)) for a,b in disj[:1]])
