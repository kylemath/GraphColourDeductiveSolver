import random, itertools, subprocess, collections
def belt(n):
    # a=0,b=1,u_i=2+i,v_i=2+n+i
    a,b=0,1; u=lambda i:2+i%n; v=lambda i:2+n+i%n
    F=[]
    for i in range(n):
        F.append((a,u(i),u(i+1))); F.append((b,v(i),v(i+1)))
        F.append((u(i),v(i),u(i+1)))      # u_i u_{i+1} v_i
        F.append((u(i+1),v(i),v(i+1)))    # u_{i+1} v_i v_{i+1}
    return 2*n+2,F
def A(r):
    R=lambda i,k:1+5*(i-1)+(k%5); q=5*r+1; F=[]
    for k in range(5): F.append((0,R(1,k),R(1,k+1)))
    for i in range(1,r):
        for k in range(5): F.append((R(i,k),R(i,k+1),R(i+1,k))); F.append((R(i,k+1),R(i+1,k),R(i+1,k+1)))
    for k in range(5): F.append((q,R(r,k),R(r,k+1)))
    return 5*r+2,F
def pentakis():
    t=open('/Users/fulkanjou/GraphColour/SolvingFrameworkPlan/docs/working/MathPathways-scripts/pentakis_dodecahedron_graph.txt').read().split()
    n=int(t[1]); nf=int(t[3]); x=list(map(int,t[4:4+3*nf]))
    return n,[tuple(x[3*i:3*i+3]) for i in range(nf)]
def adj(n,F):
    A=[set() for _ in range(n)]
    for f in F:
        for i in range(3): A[f[i]].add(f[(i+1)%3]); A[f[(i+1)%3]].add(f[i])
    return A
def check(n,F):
    E=set()
    for f in F:
        for i in range(3): E.add(frozenset((f[i],f[(i+1)%3])))
    assert len(F)==2*n-4 and len(E)==3*n-6, (len(F),len(E))
    return True
def ntri(n,F):
    Ad=adj(n,F); return sum(1 for a in range(n) for b in Ad[a] if b>a for c in Ad[a]&Ad[b] if c>b)
def flip(F,x,y):
    fs=[i for i,f in enumerate(F) if x in f and y in f]
    if len(fs)!=2: return None
    z=[t for t in F[fs[0]] if t not in (x,y)][0]; w=[t for t in F[fs[1]] if t not in (x,y)][0]
    Ad=None
    for f in F:
        if z in f and w in f: return None
    G=[f for i,f in enumerate(F) if i not in fs]+[(z,w,x),(w,z,y)]
    return G
def line(n,F): return f"G {n} 0000 {len(F)} "+" ".join(f"{a} {b} {c}" for a,b,c in F)+"\n"
def run(graphs,extra=(),fn='tmp.txt'):
    open(fn,'w').write("".join(line(n,F) for n,F in graphs))
    out=subprocess.run(['./censusd',fn,'--dump',*extra],capture_output=True,text=True,check=True).stdout
    return out
def parse(out):
    import json
    recs=[];links={};dls=collections.defaultdict(list)
    for l in out.splitlines():
        if l.startswith('{'): recs.append(json.loads(l))
        elif l.startswith('L'):
            t=list(map(int,l.split()[1:])); links[(t[0],t[1])]=t[2:]
        elif l.startswith('D'):
            t=l.split(); g,v,j,d=map(int,t[1:5]); col=list(map(int,t[5:])); dls[(g,v)].append((j,d,col))
    return recs,links,dls
