import sys,os,json
RMAX=int(sys.argv[1]); tdeg=int(sys.argv[2])
import binder as B
L,adj,name,inv,deg=B.build(tdeg)
D=B.D; LK=B.LK; SV=B.SV
j=next(j for j in range(D) if LK[j]=='5' and LK[(j+1)%D]=='5' and SV[j]=='5')
V=[('u',)]+[('w',i) for i in range(D)]+[('s',i) for i in range(D)]+[('t',)]
for x in V: assert len(adj[inv[x]])==deg[x],x
nb={x:{name[y] for y in adj[inv[x]] if name.get(y) in deg} for x in V}
core={('u',),('w',j),('w',(j+1)%D),('s',j),('t',)}
assert all(any(y in nb[x] for y in core if y!=x) for x in core)
out={}; seen=set()
def rs(S): Is={inv[x] for x in S}; return len(set(y for x in Is for y in adj[x])-Is)
def grow(S):
    k=frozenset(S)
    if k in seen: return
    seen.add(k)
    r=rs(S)
    if r<=RMAX:
        c=B.extract(adj,[inv[x] for x in S],{inv[x]:deg[x] for x in S})
        if c is not None:
            nm='t%d_%d_%s_%s_%s'%(tdeg,D,LK,SV,''.join(sorted(('u' if x==('u',) else 't' if x==('t',) else x[0]+str(x[1])) for x in S)))
            out[nm]=(c[0],'%s %d %d %s %s'%(nm,c[0],c[1],c[2],c[3]))
    if r>RMAX+3 or len(S)>=16: return
    ext=set().union(*(nb[x] for x in S))-S
    for y in ext: grow(S|{y})
grow(set(core))
for v in sorted(out.values()): print(v[1])
