# run() from /tmp/claude-0/ms/ms.py, copied; adds per-merge flag: does a conflict endpoint lie within dist<=1 of a binder vertex
import sys,random,collections,pickle,json,time
sys.path.insert(0,'/mnt/project-files/multiscale/binder_maps')
src=open('/tmp/claude-0/ms/ms.py').read().split("if __name__=='__main__':")[0]; exec(src)
import build
def run2(adj,seed,near,dump=None):
    rng=random.Random(seed); groups.clear(); levels=hierarchy(adj,rng)
    col={v:0 for v in range(len(adj))}; stats=[]
    for L in range(1,len(levels)):
        prev=levels[L-1]
        for g,parent in zip(groups[L-1],levels[L]):
            P=set(parent)
            kids=[prev[j] for j in g]; kid_of={v:k for k,c in enumerate(kids) for v in c}
            perm=[PERMS[0]]*len(kids)
            def conflicts():
                return [(v,u) for v in parent for u in adj[v] if u in P and u>v and kid_of[u]!=kid_of[v] and perm[kid_of[v]][col[v]]==perm[kid_of[u]][col[u]]]
            for _ in range(3):
                for k in range(1,len(kids)):
                    best=None
                    for p in PERMS:
                        perm[k]=p; c=len(conflicts())
                        if best is None or c<best[0]: best=(c,p)
                    perm[k]=best[1]
            for v in parent: col[v]=perm[kid_of[v]][col[v]]
            conf=[(v,u) for v in parent for u in adj[v] if u in P and u>v and col[u]==col[v]]
            if not conf: stats.append((L,len(parent),0,0,0,0)); continue
            dist={}; frontier=set(x for e in conf for x in e)
            nb=int(any(x in near for x in frontier))
            for x in frontier: dist[x]=0
            d=0; R=None; before={v:col[v] for v in parent}
            while True:
                free={v for v in dist if dist[v]<=d}
                fixed={v:col[v] for v in parent if v not in free}
                sol=solve_free({v:[u for u in adj[v] if u in P] for v in parent},fixed,free)
                if sol:
                    for v,c in sol.items(): col[v]=c
                    R=d; break
                d+=1
                for v in list(dist):
                    if dist[v]==d-1:
                        for u in adj[v]:
                            if u in P and u not in dist: dist[u]=d
            if dump is not None and R>=3:
                dump.append(dict(seed=seed,level=L,P=sorted(P),kids=[sorted(k) for k in kids],col_before=before,conf=conf,R=R,free=sorted(free),col_after={v:col[v] for v in parent}))
            stats.append((L,len(parent),len(conf),R,len(free),nb))
    assert all(col[v]!=col[u] for v in range(len(adj)) for u in adj[v])
    return stats
if __name__=='__main__':
    name=sys.argv[1]; seeds=int(sys.argv[2])
    adj=pickle.load(open('/mnt/project-files/multiscale/binder_maps/%s.pkl'%name,'rb'))
    deg,full,lo=build.census(adj); near=build.ball(adj,full,1)
    allst=[]
    for seed in range(seeds):
        t=time.time(); dump=[]; st=run2(adj,seed,near,dump); allst.append(st)
        for k,cs in enumerate(dump):
            pickle.dump(cs,open('/mnt/project-files/multiscale/binder_maps/case_run_%s_s%d_L%d_%d_R%d.pkl'%(name,seed,cs['level'],k,cs['R']),'wb'))
            print('  SAVED run() R>=3 case level',cs['level'],'|P|',len(cs['P']),'#conf',len(cs['conf']),'nfree',len(cs['free']),flush=True)
        byL=collections.defaultdict(list)
        for s in st: byL[s[0]].append(s)
        print(name,'seed',seed,'%.0fs'%(time.time()-t),flush=True)
        for L in sorted(byL):
            v=byL[L]; Rs=[x[3] for x in v if x[2]>0]; Rb=[x[3] for x in v if x[2]>0 and x[5]]
            print('  L%2d clusters %5d meanSize %8.1f withConf %4d R %s  nearBinder R %s maxFree %d'%(L,len(v),sum(x[1] for x in v)/len(v),len(Rs),dict(sorted(collections.Counter(Rs).items())),dict(sorted(collections.Counter(Rb).items())),max([x[4] for x in v]+[0])),flush=True)
    json.dump(allst,open('/mnt/project-files/multiscale/binder_maps/runms_%s.json'%name,'w'))
