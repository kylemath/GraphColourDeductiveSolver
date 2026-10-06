import sys, itertools, collections, pickle
from auto import TYPES, type_of, canonR, structures, ADJ as BADJ
def parse(line):
    t=line.split(); n=int(t[1]); nf=int(t[3]); fs=[tuple(map(int,t[4+3*i:7+3*i])) for i in range(nf)]
    return n,fs
def holes65(n,fs):
    adj=[set() for _ in range(n)]
    for f in fs:
        for k in range(3): adj[f[k]].add(f[(k+1)%3]); adj[f[(k+1)%3]].add(f[k])
    opp=collections.defaultdict(list)
    for f in fs:
        for k in range(3): opp[f[k]].append((f[(k+1)%3],f[(k+2)%3]))
    def cyc(u,a,b):
        # cyclic neighbour order of u starting a,b
        seq=[a,b]
        while len(seq)<len(adj[u]):
            cur,prev=seq[-1],seq[-2]; nx=None
            for e in opp[u]:
                if e[0]==cur and e[1]!=prev: nx=e[1]
                if e[1]==cur and e[0]!=prev: nx=e[0]
            seq.append(nx)
        return seq
    out=[]
    for v in range(n):
        if len(adj[v])!=5: continue
        a=min(adj[v]); b=[e for e in opp[v] if a in e][0]; b=b[1] if b[0]==a else b[0]
        x=cyc(v,a,b)
        if any(len(adj[y])!=6 for y in x): continue
        # cyclic link of x_t around x_t starting at v going to x_{t+1}? determine w_t,m_t
        W=[None]*5; M=[None]*5; ok=True
        for t in range(5):
            seq=cyc(x[t],v,x[(t+1)%5])
            # seq = v, x_{t+1}, w_t, m_t, w_{t-1}, x_{t-1}
            W[t]=seq[2]; M[t]=seq[3]
        ring=[]
        for t in range(5): ring+= [W[t],M[(t+1)%5]]
        if len(set(ring))<10 or set(ring)&set(x+[v]): continue
        out.append((v,x,ring,adj))
    return out
def colourings(adj,verts):
    order=verts; idx={u:i for i,u in enumerate(order)}; col={}
    res=[]
    def rec(i,maxc):
        if i==len(order): res.append(tuple(col[u] for u in order)); return
        u=order[i]
        for c in range(min(4,maxc+1)):
            if all(col.get(w)!=c for w in adj[u] if w in idx and idx[w]<i):
                col[u]=c; rec(i+1,max(maxc,c+1)); del col[u]
    rec(0,0); return res
def analyse(n,fs,want_states=True):
    res=[]
    for v,x,ring,adj in holes65(n,fs):
        verts=[u for u in range(n) if u!=v]
        # BFS order for faster backtracking
        order=[x[0]]; seen={x[0]}
        for u in order:
            for w in sorted(adj[u]):
                if w!=v and w not in seen: seen.add(w); order.append(w)
        cols=colourings(adj,order)
        pos={u:i for i,u in enumerate(order)}
        def canon(c):
            m={}; return tuple(m.setdefault(a,len(m)) for a in c)
        ids={c:i for i,c in enumerate(cols)}
        L=[pos[y] for y in x]
        def comp(c,p,q,s):
            K={s}; st=[s]
            while st:
                u=st.pop()
                for w in adj[order[u]]:
                    if w==v: continue
                    j=pos[w]
                    if j not in K and c[j] in (p,q): K.add(j); st.append(j)
            return K
        def filled(c): return len({c[i] for i in L})<=3
        # Kempe graph BFS from filled (distance to filled)
        nb=[set() for _ in cols]; mv={}; ballset0=set(x)|set(ring)
        for i,c in enumerate(cols):
            done=set()
            for p,q in itertools.combinations(range(4),2):
                for s in range(len(c)):
                    if c[s] in (p,q) and (p,q,s) not in done:
                        K=comp(c,p,q,s)
                        for k in K: done.add((p,q,k))
                        d=list(c)
                        for k in K: d[k]= q if c[k]==p else p
                        nb[i].add(ids[canon(d)]); mv.setdefault(i,[]).append((ids[canon(d)],all(order[k] in ballset0 for k in K),len(K)))
        dist=[None]*len(cols); Q=collections.deque()
        for i,c in enumerate(cols):
            if filled(c): dist[i]=0; Q.append(i)
        while Q:
            i=Q.popleft()
            for j in nb[i]:
                if dist[j] is None: dist[j]=dist[i]+1; Q.append(j)
        ballset=set(x)|set(ring)|{v}
        rp=[pos[r] for r in ring]
        for i,c in enumerate(cols):
            if filled(c): continue
            # DL?
            Lc=[c[k] for k in L]
            j=[t for t in range(5) if Lc[t]==Lc[(t+2)%5]][0]
            x1,x3,x4=L[(j+1)%5],L[(j+3)%5],L[(j+4)%5]
            if not (x3 in comp(c,c[x1],c[x3],x1) and x4 in comp(c,c[x1],c[x4],x1)): continue
            # rotate frame so that j=0 -> local colouring with link pattern a b a g d
            rot=j
            xs=[x[(rot+t)%5] for t in range(5)]
            rs=[ring[(2*rot+k)%10] for k in range(10)]
            cm={c[pos[xs[0]]]:0,c[pos[xs[1]]]:1,c[pos[xs[3]]]:2,c[pos[xs[4]]]:3}
            lc=tuple(cm[c[pos[u]]] for u in xs+rs)
            # outside structures per type
            Rs=[]
            for T in range(3):
                lab=list(range(10))
                for (p,q) in TYPES[T]:
                    cp=[k for k in range(10) if lc[5+k] in (p,q)]
                    for a,b in itertools.combinations(cp,2):
                        # path from rs[a] to rs[b] with interior outside ball, in colours p,q (original colours mapped)
                        inv={vv:kk for kk,vv in cm.items()}
                        P,Qc=inv[p],inv[q]
                        src=rs[a]; tgt=rs[b]; st=[src]; seen2={src}; found=False
                        while st and not found:
                            u=st.pop()
                            for w in adj[u]:
                                if w==tgt and u!=src or (w==tgt and u==src and w in adj[src] and abs(a-b)%10 not in (1,9)):
                                    found=True;break
                                if w in ballset or w in seen2: continue
                                if c[pos[w]] in (P,Qc): seen2.add(w); st.append(w)
                        if found:
                            la,lb=lab[a],lab[b]
                            lab=[la if z==lb else z for z in lab]
                Rs.append(canonR(lab))
            good=[(b,sz) for (jj,b,sz) in mv[i] if dist[jj]==dist[i]-1]
            res.append((v,lc,dist[i],Rs,good))
    return res
if __name__=='__main__':
    out=[]
    for fn in sys.argv[1:]:
        for line in open(fn):
            if not line.startswith('G'): continue
            n,fs=parse(line); r=analyse(n,fs)
            if r: out.append((fn,line.strip(),r))
    pickle.dump(out,open('real2_'+sys.argv[1].split('/')[-1]+'.pkl','wb'))
    print(len(out),'graphs with (6^5) holes; states',sum(len(r) for _,_,r in out), collections.Counter(s[2] for _,_,r in out for s in r))
