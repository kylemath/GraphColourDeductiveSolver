import csv,sys,itertools,random,numpy as np,cvxpy as cp
sys.path.insert(0,'/tmp/claude-0/ml'); from feat import parse
from pysat.solvers import Minisat22
T=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])/np.sqrt(3)   # tetra corners; coords = the 3 pairings
def ring_cols(r):
    out=[]
    def rec(s,used):
        if len(s)==r:
            if s[-1]!=s[0]: out.append(tuple(s))
            return
        for c in range(min(used+1,4)):
            if s and c==s[-1]: continue
            rec(s+[c],max(used,c+1))
    rec([0],1); return out
def extends(r,m,adj,rc):
    s=Minisat22(); var=lambda j,c: 4*j+c+1
    for j in range(m):
        v=r+j; s.add_clause([var(j,c) for c in range(4)])
        for u in adj[v]:
            if u<r: s.add_clause([-var(j,rc[u])])
            elif u>v:
                for c in range(4): s.add_clause([-var(j,c),-var(u-r,c)])
    return s.solve()
def sdp_ok(r,m,adj,rc):
    # interior vectors: Gram over [4 tetra anchors + m interior]; edge => dot = -1/3
    n=4+m; X=cp.Variable((n,n),PSD=True); cons=[cp.diag(X)==1]
    G=T@T.T
    for a in range(4):
        for b in range(4): cons.append(X[a,b]==G[a,b])
    for j in range(m):
        v=r+j
        for u in adj[v]:
            if u<r: cons.append(X[rc[u],4+j]==-1/3)
            elif u>v: cons.append(X[4+j,4+u-r]==-1/3)
    pr=cp.Problem(cp.Minimize(0),cons)
    try: pr.solve(solver='CLARABEL')
    except BaseException:
        try: pr.solve(solver='SCS',eps=1e-7,max_iters=20000)
        except BaseException: return None
    return pr.status in ('optimal','optimal_inaccurate')
rows=[x for x in csv.DictReader(open('/mnt/project-files/explore/dataset/windows_judged.tsv'),delimiter='\t') if int(x['ring'])<=10 and int(x['m'])>=4]
random.Random(0).shuffle(rows)
tot=[0,0,0,0]
for x in rows[:int(sys.argv[1])]:
    w=dict(r=int(x['ring']),m=int(x['m']),ra=x['ring_adj'],ia=x['int_adj']); r,m,adj=parse(w)
    RC=ring_cols(r); ne=0; caught=0; fp=0
    for rc in RC:
        e=extends(r,m,adj,rc); s=sdp_ok(r,m,adj,rc)
        if not e:
            ne+=1; caught+= (s is False)
        elif s is False: fp+=1
    tot[0]+=len(RC); tot[1]+=ne; tot[2]+=caught; tot[3]+=fp
    print(x['name'],'r',r,'m',m,'classes',len(RC),'non-extending',ne,'caught by sphere SDP',caught,'false alarms',fp,'label',x['kc_D'],x['kc_C'],flush=True)
print('TOTAL classes %d non-extending %d caught %d (%.1f%%) false alarms %d'%(tot[0],tot[1],tot[2],100*tot[2]/max(tot[1],1),tot[3]))
