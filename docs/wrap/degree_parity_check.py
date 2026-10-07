import sys, itertools, collections
def graphs(path):
    for line in open(path):
        t=line.split()
        if not t or t[0]!='G': continue
        n=int(t[1]); m=int(t[3]); vals=list(map(int,t[4:4+3*m]))
        yield n,[tuple(vals[3*i:3*i+3]) for i in range(m)]
def orient(F):
    F=[list(f) for f in F]; E={}
    for i,f in enumerate(F):
        for k in range(3): E.setdefault(frozenset((f[k],f[(k+1)%3])),[]).append(i)
    done={0}; st=[0]
    while st:
        i=st.pop(); f=F[i]
        for k in range(3):
            a,b=f[k],f[(k+1)%3]
            for j in E[frozenset((a,b))]:
                if j in done: continue
                g=F[j]; 
                for q in range(3):
                    if g[q]==a and g[(q+1)%3]==b: F[j]=[g[0],g[2],g[1]]
                done.add(j); st.append(j)
    return [tuple(f) for f in F]
def analyse(n,F):
    adj=[set() for _ in range(n)]
    for a,b,c in F:
        for x,y in((a,b),(b,c),(c,a)): adj[x].add(y);adj[y].add(x)
    F=orient(F)
    order=sorted(range(n),key=lambda v:-len(adj[v])); cols=[]; col=[-1]*n
    def bt(i):
        if i==n: cols.append(tuple(col)); return
        v=order[i]
        for c in range(4):
            if all(col[w]!=c for w in adj[v]): col[v]=c; bt(i+1); col[v]=-1
    bt(0)
    idx={c:i for i,c in enumerate(cols)}; par=list(range(len(cols)))
    def find(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    for c in cols:
        for a,b in itertools.combinations(range(4),2):
            seen=set()
            for v in range(n):
                if c[v] in (a,b) and v not in seen:
                    comp=[v]; seen.add(v); st=[v]
                    while st:
                        u=st.pop()
                        for w in adj[u]:
                            if c[w] in (a,b) and w not in seen: seen.add(w); comp.append(w); st.append(w)
                    nc=list(c)
                    for u in comp: nc[u]=b if c[u]==a else a
                    x,y=find(idx[c]),find(idx[tuple(nc)])
                    if x!=y: par[x]=y
    def deg(c,m):
        rest=[x for x in range(4) if x!=m]; pos={tuple(rest[(i+k)%3] for k in range(3)) for i in range(3)}
        s=0
        for a,b,cc in F:
            t=(c[a],c[b],c[cc])
            if m in t: continue
            s+=1 if t in pos else -1
        return s
    cls=collections.defaultdict(set); mismatch=0
    for c in cols:
        ds={deg(c,m) for m in range(4)}
        if len(ds)!=1: mismatch+=1
        cls[find(idx[c])].add(deg(c,0)%2)
    return len(cls), sum(1 for s in cls.values() if len(s)>1), len({min(s) for s in cls.values()}), mismatch
tot=collections.Counter()
for N in sys.argv[1:]:
    for n,F in graphs(f'backgroundMaterial/planemap-structural/studiointel/gentri/tri{N}.txt'):
        r=analyse(n,F)
        if r is None: tot['unoriented']+=1; continue
        k,mixed,parities,mm=r
        tot['graphs']+=1; tot['classes']+=k; tot['classes_mixed_parity']+=mixed; tot['multi_class']+= k>1
        tot['multi_class_both_parities']+= (k>1 and parities==2); tot['deg_depends_on_face']+=mm
    print(N, dict(tot), flush=True)
