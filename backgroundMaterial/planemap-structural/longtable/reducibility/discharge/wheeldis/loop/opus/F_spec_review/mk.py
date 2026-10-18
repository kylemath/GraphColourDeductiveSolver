import sys; sys.argv=[None,'cut.txt']
exec(open('flip.py').read().split('for l in open')[0])
import networkx as nx
def rebuild(m,T,side):
    par={}
    def f(x):
        while par.setdefault(x,x)!=x: x=par[x]
        return x
    def un(a,b): par[f(a)]=f(b)
    for u in T:
        L=T[u]; n=len(L)
        for j in range(n):
            if L[j]=='R':
                f((u,j))
                for dj,ds in ((1,side),(-1,-side)):
                    w=L[(j+dj)%n]
                    if w!='R':
                        Lw=T[w]; k=Lw.index(u); un((u,j),(w,(k+ds)%len(Lw)))
    ring=nx.Graph()
    for u in T:
        L=T[u]; n=len(L)
        for j in range(n):
            if L[j]=='R' and L[(j+1)%n]=='R': ring.add_edge(f((u,j)),f((u,(j+1)%n)))
        for j in range(n):
            if L[j]=='R': ring.add_node(f((u,j)))
    # also check R slots map consistently
    for (u,j),_ in list(par.items()):
        assert T[u][j]=='R'
    return f,ring
line=[l for l in open(sys.argv[1] if len(sys.argv)>1 else "cut.txt") if l.startswith('k42_rsst062')][0]
nm,r,m,rot=parse(line); S=system(m,rot)
# find side using original
for side in (1,-1):
    try:
        f,ring=rebuild(m,S,side)
        cyc=nx.cycle_basis(ring)
        if ring.number_of_nodes()==r and all(d==2 for _,d in ring.degree()) and nx.is_connected(ring):
            print('side',side,'ok'); SIDE=side
    except AssertionError as e: pass
for c,C2,T in flips(m,S):
    f,ring=rebuild(m,T,SIDE)
    print('flip at',c,'side',C2,'ringnodes',ring.number_of_nodes(),'cycle?',all(d==2 for _,d in ring.degree()) and nx.is_connected(ring))
    cyc=[x[0] for x in nx.find_cycle(ring)]
    ri={x:k for k,x in enumerate(cyc)}
    rp=[];ip=[]
    for u in range(m):
        rs=sorted({ri[f((u,j))] for j in range(len(T[u])) if T[u][j]=='R'})
        rp.append(','.join(map(str,rs)) or '-'); ip.append(','.join(map(str,sorted(x for x in T[u] if x!='R'))) or '-')
    print('%s_flip%s %d %d %s %s'%(nm,''.join(map(str,C2)),len(cyc),m,';'.join(rp),';'.join(ip)))
# sanity: rebuild original
f,ring=rebuild(m,S,SIDE); cyc=[x[0] for x in nx.find_cycle(ring)]; ri={x:k for k,x in enumerate(cyc)}
print('orig', ';'.join(','.join(map(str,sorted({ri[f((u,j))] for j in range(len(S[u])) if S[u][j]=='R'}))) or '-' for u in range(m)))
print(line.strip())
