# Build min-degree-5 triangulations steered (simulated annealing over edge flips) towards binder link words.
import sys,random,itertools,collections,pickle,math,time
sys.path.insert(0,'/mnt/project-files/multiscale/binder_maps')
src=open('/tmp/claude-0/ms/ms.py').read().split("if __name__=='__main__':")[0]; exec(src)
from binder import load_rows,dihedral,canon
ROWS=load_rows(); import os; FB=float(os.environ.get("FB","3"))
def link_order(adj,u):
    nb=adj[u]; w0=next(iter(nb)); order=[w0]; prev=None; cur=w0
    while True:
        cn=[x for x in adj[cur] if x in nb and x!=prev]
        nxt=cn[0] if (prev is not None or True) and cn[0]!=prev else cn[1]
        if prev is None: nxt=cn[0]
        if nxt==w0: break
        order.append(nxt); prev,cur=cur,nxt
        if len(order)>len(nb): raise RuntimeError('bad link')
    return order
def letter(x): return str(min(x,9))
def words(adj,u):
    o=link_order(adj,u); d=len(o)
    L=''.join(letter(len(adj[w])) for w in o); S=[]; sv=[]
    for i in range(d):
        a,b=o[i],o[(i+1)%d]; s=[x for x in adj[a]&adj[b] if x!=u]
        sv.append(s[0]); S.append(letter(len(adj[s[0]])))
    return o,sv,L,''.join(S)
def setup(target_rows,maxdeg):
    OL=collections.defaultdict(set)  # oriented link -> oriented second rings
    for (l,s) in target_rows:
        for L,S in dihedral(l,s): OL[L].add(S)
    LD={}
    for d in set(len(l) for l in OL):
        if d>maxdeg: continue
        Ls=[l for l in OL if len(l)==d]
        for t in itertools.product('5678'[:maxdeg-4],repeat=d):
            t=''.join(t); LD[t]=min(sum(x!=y for x,y in zip(t,l)) for l in Ls)
    return OL,LD
def vscore(adj,u,OL,LD):
    d=len(adj[u])
    if d<7: return 0.0
    o,sv,L,S=words(adj,u)
    dl=LD.get(L)
    if dl is None: return 0.0
    sc=max(0,3-dl)/3
    if dl==0:
        ds=min(sum(x!=y for x,y in zip(S,s)) for s in OL[L])
        sc+=1+2*max(0,4-ds)/4+FB*(ds==0)
    return sc
def ball(adj,X,r):
    seen=set(X); fr=set(X)
    for _ in range(r):
        fr={u for v in fr for u in adj[v]}-seen; seen|=fr
    return seen
def anneal(adj,steps,rng,OL,LD,maxdeg=8,T0=0.6,T1=0.02,log=None):
    n=len(adj); sc=[vscore(adj,u,OL,LD) for u in range(n)]; tot=sum(sc); acc=0; t0=time.time()
    for it in range(steps):
        T=T0*(T1/T0)**(it/steps)
        a=rng.randrange(n); b=rng.choice(tuple(adj[a])); cn=adj[a]&adj[b]
        c,d=cn
        if len(adj[a])<=5 or len(adj[b])<=5 or len(adj[c])>=maxdeg or len(adj[d])>=maxdeg: continue
        if adj[c]&adj[d]!={a,b}: continue   # would create separating triangle / multi-edge
        # chordless 4-cycle through new edge c-d: c-d-x-y with x~d,y~c,x~y, c!~x, d!~y
        bad=False
        Nc=adj[c]|{a,b}; 
        for x in adj[d]:
            if x in (a,b) or x in adj[c]: continue
            for y in adj[x]:
                if y in adj[c] and y not in adj[d] and y!=d: bad=True; break
            if bad: break
        if bad: continue
        aff=ball(adj,(a,b,c,d),2)
        old=sum(sc[v] for v in aff)
        adj[a].discard(b); adj[b].discard(a); adj[c].add(d); adj[d].add(c)
        new={v:vscore(adj,v,OL,LD) for v in aff}; dlt=sum(new.values())-old
        if dlt>=0 or rng.random()<math.exp(dlt/T):
            for v,s in new.items(): sc[v]=s
            tot+=dlt; acc+=1
        else:
            adj[c].discard(d); adj[d].discard(c); adj[a].add(b); adj[b].add(a)
        if log and it%log==0: print('  it',it,'T %.3f'%T,'score %.1f'%tot,'acc',acc,'%.0fs'%(time.time()-t0),flush=True)
    return adj
def census(adj,rows=ROWS):
    deg=collections.Counter(len(a) for a in adj); full=[];linkonly=[]
    links={canon(l,l)[0] for (l,s) in rows}  # canonical link
    from binder import canon_link
    links={canon_link(l) for (l,s) in rows}
    for u in range(len(adj)):
        if len(adj[u])<7: continue
        o,sv,L,S=words(adj,u)
        if canon(L,S) in rows: full.append(u)
        elif canon_link(L) in links: linkonly.append(u)
    return deg,full,linkonly
def sep_checks(adj):
    n=len(adj); st=0; c4=0
    for u in range(n):
        for v in adj[u]:
            if v>u and len(adj[u]&adj[v])!=2: st+=1
    # chordless 4-cycles: pairs x,y nonadjacent with two nonadjacent common nbrs
    for x in range(n):
        two=collections.defaultdict(list)
        for a in adj[x]:
            for y in adj[a]:
                if y>x and y not in adj[x]: two[y].append(a)
        for y,cs in two.items():
            for a,b in itertools.combinations(cs,2):
                if b not in adj[a]: c4+=1
    return st,c4
if __name__=='__main__':
    name=sys.argv[1]; f=int(sys.argv[2]); steps=int(sys.argv[3]); seed=int(sys.argv[4]); mode=sys.argv[5]
    rng=random.Random(seed); adj=icosphere(f)
    if mode=='hard':  # only the four highlighted hard link words
        hl={'5566776','5566767','5566766'}  # canon of 7766556,7676655/5566767,7665566
        from binder import canon_link
        T={k:v for k,v in ROWS.items() if canon_link(k[0]) in hl}
    else: T={k:v for k,v in ROWS.items() if len(k[0])<=8}
    if mode=='rand' or 'rand' in mode:
        exec(open('/tmp/claude-0/ms/defect.py').read().split('rng=random.Random(5)')[0].split('exec(src)')[1])
        adj=flip_defects(adj,len(adj)//3,rng)
    OL,LD=setup(T,8)
    print(name,'n',len(adj),'targets',len(T),flush=True)
    adj=anneal(adj,steps,rng,OL,LD,log=max(1,steps//10))
    deg,full,lo=census(adj); st,c4=sep_checks(adj)
    print(name,'n',len(adj),'deg',sorted(deg.items()),'fullmatch',len(full),'linkonly',len(lo),'septri',st,'chordless4',c4,flush=True)
    pickle.dump(adj,open('/mnt/project-files/multiscale/binder_maps/%s.pkl'%name,'wb'))
