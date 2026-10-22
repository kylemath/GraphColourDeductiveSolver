# shape of the near-old SDP deviation along the seam: spike vs smooth ramp; rotation vs out-of-span
import os; os.environ['OPENBLAS_NUM_THREADS']='1'
from run import *
for fn in sys.argv[1:]:
    T,A,B,a,b,R0=load(fn); n=len(T.adj); allv=set(range(n)); c=close(T,A,B,a,b); col,new,K=c['col'],c['new'],c['K']
    ch=set(v for v in new if new[v]!=col[v])
    sv=set(x for u in A for w in T.adj[u] if w not in A for x in (u,w)); dS=multi_bfs(T.adj,list(sv),allv)
    cA,cB,lab=seam_geometry(T,A,B,a,c['p']); mA=cA.m
    free=[v for v in range(n) if dS[v]<=2]
    pen,Y,C=bm(T,col,free,d=12,init='old',seed=1); vm=vec_metrics(free,bm_X(Y,C))
    dist=np.zeros(mA); 
    for v in free: dist[lab[v]]=max(dist[lab[v]],vm[v]['dist'])
    chg=np.zeros(mA); conf=np.zeros(mA)
    for v in ch: chg[lab[v]]+=1
    for v in K: conf[lab[v]]+=1
    dev=[vm[v] for v in free if vm[v]['dist']>0.3]
    # runs of seam positions with max dist > 0.3
    on=dist>0.3; runs=[]; i=0
    if on.all(): runs=[mA]
    else:
        st=int(np.argmin(on)); cur=0
        for j in range(mA):
            if on[(st+j)%mA]: cur+=1
            elif cur: runs.append(cur); cur=0
        if cur: runs.append(cur)
    # do deviations sit exactly where SAT changed / conflicts are? fraction of deviated positions with a conflict within 1 position
    near=lambda arr,i: arr[[(i+j)%mA for j in (-1,0,1)]].sum()>0
    fdc=np.mean([near(conf,i) for i in range(mA) if on[i]]) if on.any() else None
    fcd=np.mean([near(on.astype(float),i) for i in range(mA) if conf[i]>0])
    # dist vs depth from seam
    bydepth={k:round(float(np.mean([vm[v]['dist'] for v in free if dS[v]==k])),3) for k in range(3)}
    print(os.path.basename(fn),'R',c['R'],'mA',mA,'pen %.0e'%pen,'pos dev>0.3: %d/%d'%(on.sum(),mA),'runs',sorted(runs,reverse=True)[:8],
          'nruns',len(runs),'| deviated verts',len(dev),'proj med %.2f'%np.median([x['proj'] for x in dev]) if dev else '',
          '| frac dev-pos near conflict %.2f, frac conflict-pos near dev %.2f'%(fdc,fcd),'| mean dist by depth',bydepth,
          '| changed',len(ch),'changed with dist>0.3: %d'%sum(1 for v in ch if v in vm and vm[v]['dist']>0.3),
          'dev verts changed by SAT %d/%d'%(sum(1 for v in free if vm[v]['dist']>0.3 and v in ch),len(dev)), flush=True)
    print('  profile (max dist per A-walk position, x10):', ''.join(str(min(9,int(10*x))) for x in dist))
    print('  conflicts                                  :', ''.join(str(min(9,int(x))) for x in conf))
    print('  SAT changed                                :', ''.join(str(min(9,int(x))) for x in chg))
