# Stronger variant of hunt_binder: lexicographic objective (R, size of smallest sufficient free set over all 24 renamings),
# so the hill-climb has a gradient on R plateaus; several restarts per centre.
import sys,random,collections,pickle,json,time
sys.path.insert(0,'/mnt/project-files/multiscale/binder_maps')
from hunt_binder import *
def need_RF(adj,U,colA,colB,maxR=12):
    best=None; Ua={v:[u for u in adj[v] if u in U] for v in U}
    for p in PERMS:
        col=dict(colA); col.update({v:p[c] for v,c in colB.items()})
        conf={x for v in U for u in adj[v] if u in U and col[u]==col[v] for x in (u,v)}
        if not conf: return (0,0)
        d=bfs(adj,conf,U)
        for R in range(0,maxR+1):
            if best is not None and R>best[0]: break
            free={v for v,dv in d.items() if dv<=R}
            if best is not None and R==best[0] and len(free)>=best[1]: break
            fixed={v:col[v] for v in U if v not in free}
            if solve_free(Ua,fixed,free) is not None:
                best=(R,len(free)) if best is None or (R,len(free))<best else best; break
    return best
def hunt_s(adj,center,rad,iters,restarts,rng):
    U={v for v,dv in bfs(adj,[center],set(range(len(adj)))).items() if dv<=rad}
    top=((-1,0),None,None,None,None)
    for r in range(restarts):
        A,B=split_through(adj,center,U,rad,rng)
        cA=random_col(adj,A,rng); cB=random_col(adj,B,rng); cur=need_RF(adj,U,cA,cB)
        for it in range(iters):
            nA,nB=dict(cA),dict(cB)
            for _ in range(rng.randint(1,3)): kempe(adj,nA,A,rng) if rng.random()<.5 else kempe(adj,nB,B,rng)
            s=need_RF(adj,U,nA,nB)
            if s>=cur: cA,cB,cur=nA,nB,s
        if cur>top[0]: top=(cur,A,B,dict(cA),dict(cB))
    return U,top
if __name__=='__main__':
    name=sys.argv[1]; trials=int(sys.argv[2]); rad=int(sys.argv[3]); iters=int(sys.argv[4]); rs=int(sys.argv[5]); ctl=sys.argv[6] if len(sys.argv)>6 else ''
    adj=pickle.load(open('/mnt/project-files/multiscale/binder_maps/%s.pkl'%name,'rb'))
    deg,full,lo=build.census(adj); rng=random.Random(11)
    fs=set(full); pool=sorted(full) if not ctl else [v for v in range(len(adj)) if len(adj[v])==(7 if ctl=='ctl7' else 6) and v not in fs]
    tag=name+('_'+ctl if ctl else '')+'_strong'; res=collections.Counter(); out=[]
    for t in range(trials):
        c=rng.choice(pool); t0=time.time()
        U,((R,nf),A,B,cA,cB)=hunt_s(adj,c,rad,iters,rs,rng); res[R]+=1
        o,sv,L,S=build.words(adj,c)
        rec=dict(center=c,deg=len(adj[c]),link=L,second=S,U=len(U),R=R,nfree=nf)
        print(tag,'trial',t,rec,'%.0fs'%(time.time()-t0),flush=True); out.append(rec)
        if R>=3:
            R2,p,conf,nfree=need_R_detail(adj,U,cA,cB); dc=bfs(adj,[c],U)
            rec.update(conf_dist_from_center=sorted(collections.Counter(dc[x] for x in conf).items()),perm=p)
            pickle.dump(dict(U=U,A=A,B=B,colA=cA,colB=cB,center=c,R=R2,perm=p,conf=conf,map=name),open('/mnt/project-files/multiscale/binder_maps/case_%s_t%d_R%d.pkl'%(tag,t,R),'wb'))
            print('   SAVED R>=3 case',rec,flush=True)
    print(tag,'R distribution',sorted(res.items()),flush=True)
    json.dump(out,open('/mnt/project-files/multiscale/binder_maps/hunt_%s.json'%tag,'w'))
