# Describe saved R>=3 cases from run(): local degrees, distance to binder vertices, and whether re-choosing one kid's renaming lowers R
import sys,pickle,glob,os,re,collections
sys.path.insert(0,'/mnt/project-files/multiscale/binder_maps')
import build
hs=open('/tmp/claude-0/ms/hunt.py').read().split('rng=random.Random(1)')[0]; exec(hs)
maps={}
def minR(adj,P,col,maxR=6):
    Pa={v:[u for u in adj[v] if u in P] for v in P}
    conf={x for v in P for u in Pa[v] if col[u]==col[v] for x in (u,v)}
    if not conf: return 0,0
    d=bfs(adj,conf,P)
    for R in range(maxR+1):
        free={v for v,x in d.items() if x<=R}
        if solve_free(Pa,{v:col[v] for v in P if v not in free},free) is not None: return R,len(conf)
    return None,len(conf)
rows=[]
for f in sorted(glob.glob('/mnt/project-files/multiscale/binder_maps/case_run_*.pkl')):
    m=re.match(r'case_run_(.*)_s(\d+)_L(\d+)_(\d+)_R(\d+)\.pkl',os.path.basename(f)); name=m.group(1)
    if name not in maps:
        adj=pickle.load(open('/mnt/project-files/multiscale/binder_maps/%s.pkl'%name,'rb')); deg,full,lo=build.census(adj); maps[name]=(adj,full,set(lo))
    adj,full,lo=maps[name]; cs=pickle.load(open(f,'rb')); P=set(cs['P']); col=cs['col_before']
    ends={x for e in cs['conf'] for x in e}
    dfull=bfs(adj,full,set(range(len(adj)))) if full else {}
    dmin=min(dfull.get(x,99) for x in ends) if full else None
    # local picture around the first conflict edge
    u,v=cs['conf'][0]
    dl=lambda x: ''.join(str(len(adj[w])) for w in build.link_order(adj,x))
    # try all 24 renamings of the kid containing u (others fixed); best achievable R
    kid=[set(k) for k in cs['kids'] if u in k][0]; best=None
    if len(cs['conf'])<=3:
        for p in PERMS:
            c2={x:(p[col[x]] if x in kid else col[x]) for x in P}
            r,_=minR(adj,P,c2)
            if r is not None and (best is None or r<best): best=r
    # distance from conflict to boundary of P
    bd={x for x in P if any(y not in P for y in adj[x])}; db=bfs(adj,bd,P) if bd else {}
    rows.append((name,cs['seed'],cs['level'],len(P),len(cs['kids']),len(cs['conf']),cs['R'],len(cs['free']),'%d-%d'%(len(adj[u]),len(adj[v])),dl(u)+'|'+dl(v),dmin,min(db.get(x,99) for x in ends),best))
print('| map | seed | level | |P| | kids | #conf | R | #freed | deg(u)-deg(v) | links of u, v | dist to nearest binder vertex | dist to cluster boundary | best R over 24 renamings of u\'s kid |')
print('|'+'---|'*13)
for r in rows: print('| '+' | '.join(str(x) for x in r)+' |')
