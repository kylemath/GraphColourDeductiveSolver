import sys,pickle,collections
sys.path.insert(0,'/mnt/project-files/multiscale/binder_maps')
import build
from binder import canon,canon_link
hs=open('/tmp/claude-0/ms/hunt.py').read().split('rng=random.Random(1)')[0]; exec(hs)
for name,f in [('M2_ico22','case_run_M2_ico22_s1_L7_3_R3.pkl'),('M3_ico22_hard','case_run_M3_ico22_hard_s0_L8_0_R3.pkl')]:
    import glob
    f=glob.glob('/mnt/project-files/multiscale/binder_maps/'+f.replace('_3_R3','_*_R3').replace('_0_R3','_*_R3'))[0]
    adj=pickle.load(open('/mnt/project-files/multiscale/binder_maps/%s.pkl'%name,'rb')); deg,full,lo=build.census(adj); fs=set(full)
    cs=pickle.load(open(f,'rb')); P=set(cs['P']); col=cs['col_before']; (u,v)=cs['conf'][0]
    kidA=[set(k) for k in cs['kids'] if u in k][0]
    d=bfs(adj,[u,v],P)
    print('==',f.split('/')[-1],'conflict',u,v,'colour',col[u])
    for r in range(4):
        layer=sorted(x for x in d if d[x]==r)
        print('  dist',r,'n=%d'%len(layer),'deg',dict(sorted(collections.Counter(len(adj[x]) for x in layer).items())),'binder',sum(x in fs for x in layer),'sideA',sum(x in kidA for x in layer))
    disc={x for x in d if d[x]<=2}
    seam=[(a,b) for a in disc for b in adj[a] if b in P and b>a and ((a in kidA)!=(b in kidA))]
    print('  seam edges within R<=2 disc:',len(seam))
    for x in sorted(disc&fs):
        o,sv,L,S=build.words(adj,x); print('  binder vertex in disc',x,'dist',d[x],L,S,canon(L,S))
    # does extension fail for every renaming? (2 kids)
    res={}
    for p in PERMS:
        c2={x:(p[col[x]] if x in kidA else col[x]) for x in P}
        conf={y for a in P for b in adj[a] if b in P and c2[a]==c2[b] for y in (a,b)}
        if not conf: res[p]=0; continue
        dd=bfs(adj,conf,P)
        for R in range(6):
            free={x for x,y in dd.items() if y<=R}
            if solve_free({x:[y for y in adj[x] if y in P] for x in P},{x:c2[x] for x in P if x not in free},free) is not None: res[p]=(R,len(conf)); break
    print('  R per renaming of kid containing u:',sorted(collections.Counter(res.values()).items()))
