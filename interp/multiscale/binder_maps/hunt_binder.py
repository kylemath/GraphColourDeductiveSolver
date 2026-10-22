# hunt.py adversary (copied), regions centred at binder-matching vertices, seam forced through the centre's 1-ball
import sys,random,collections,pickle,json,time
sys.path.insert(0,'/mnt/project-files/multiscale/binder_maps')
hs=open('/tmp/claude-0/ms/hunt.py').read().split('rng=random.Random(1)')[0]; exec(hs)
import build
def need_R_detail(adj,U,colA,colB,maxR=12):
    best=None
    for p in PERMS:
        col=dict(colA); col.update({v:p[c] for v,c in colB.items()})
        conf={x for v in U for u in adj[v] if u in U and col[u]==col[v] for x in (u,v)}
        if not conf: return (0,p,set(),0)
        d=bfs(adj,conf,U)
        for R in range(0,maxR+1):
            if best is not None and R>=best[0]: break
            free={v for v,dv in d.items() if dv<=R}
            fixed={v:col[v] for v in U if v not in free}
            if solve_free({v:[u for u in adj[v] if u in U] for v in U},fixed,free) is not None:
                best=(R,p,conf,len(free)); break
    return best
def split_through(adj,center,U,rad,rng):
    ball1=build.ball(adj,[center],1)
    for _ in range(200):
        dc=bfs(adj,[center],U); ring=[v for v,x in dc.items() if x==rad]
        s1=rng.choice(ring); d1=bfs(adj,[s1],U); far=max(d1[v] for v in ring)
        s2=rng.choice([v for v in ring if d1[v]>=far-1]); d2=bfs(adj,[s2],U)
        A={v for v in U if (d1[v],rng.random())<(d2[v],rng.random()) or d1[v]<d2[v]}
        A={v for v in U if d1[v]<d2[v] or (d1[v]==d2[v] and v%2==0)}; B=U-A
        if (ball1&A) and (ball1&B) and center in ball1: return A,B
    return None
def hunt_c(adj,center,rad,iters,rng):
    U={v for v,dv in bfs(adj,[center],set(range(len(adj)))).items() if dv<=rad}
    A,B=split_through(adj,center,U,rad,rng)
    cA=random_col(adj,A,rng); cB=random_col(adj,B,rng); cur=need_R(adj,U,cA,cB); top=(cur,dict(cA),dict(cB))
    for it in range(iters):
        nA,nB=dict(cA),dict(cB)
        for _ in range(rng.randint(1,3)): kempe(adj,nA,A,rng) if rng.random()<.5 else kempe(adj,nB,B,rng)
        r=need_R(adj,U,nA,nB)
        if r>=cur:
            cA,cB,cur=nA,nB,r
            if r>top[0]: top=(r,dict(nA),dict(nB))
    return U,A,B,top
if __name__=='__main__':
    name=sys.argv[1]; trials=int(sys.argv[2]); rad=int(sys.argv[3]); iters=int(sys.argv[4]); ctl=sys.argv[5] if len(sys.argv)>5 else ''
    adj=pickle.load(open('/mnt/project-files/multiscale/binder_maps/%s.pkl'%name,'rb'))
    deg,full,lo=build.census(adj); rng=random.Random(7)
    fs=set(full); pool=sorted(full) if not ctl else [v for v in range(len(adj)) if len(adj[v])==(7 if ctl=='ctl7' else 6) and v not in fs]
    res=collections.Counter(); out=[]; tag=name+('_'+ctl if ctl else '')
    for t in range(trials):
        c=rng.choice(pool); t0=time.time()
        U,A,B,(R,cA,cB)=hunt_c(adj,c,rad,iters,rng); res[R]+=1
        o,sv,L,S=build.words(adj,c)
        rec=dict(center=c,deg=len(adj[c]),link=L,second=S,U=len(U),A=len(A),B=len(B),R=R)
        print(tag,'trial',t,rec,'%.0fs'%(time.time()-t0),flush=True); out.append(rec)
        if R>=3:
            R2,p,conf,nfree=need_R_detail(adj,U,cA,cB)
            dc=bfs(adj,[c],U)
            rec.update(conf_dist_from_center=sorted(collections.Counter(dc[x] for x in conf).items()),nfree=nfree,perm=p)
            pickle.dump(dict(adj=adj,U=U,A=A,B=B,colA=cA,colB=cB,center=c,R=R2,perm=p,conf=conf),open('/mnt/project-files/multiscale/binder_maps/case_%s_t%d_R%d.pkl'%(tag,t,R),'wb'))
            print('   SAVED R>=3 case',rec,flush=True)
    print(tag,'R distribution',sorted(res.items()),flush=True)
    json.dump(out,open('/mnt/project-files/multiscale/binder_maps/hunt_%s.json'%tag,'w'))
