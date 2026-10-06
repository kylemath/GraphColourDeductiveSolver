import sys; sys.path.insert(0,'.')
from astruct_core import *
r=int(sys.argv[1]); rows=eval(sys.argv[2]); cap=int(sys.argv[3])
adj=build(r);L=link(r)
s={'v':None,'c':cap}
for i in range(r):
    for t in range(5): s[(i,t)]=rows[i][t]
order=[u for u in adj if u!='v']
def path(col,a,b,pair):
    par={a:None};q=[a]
    for u in q:
        for w in sorted(adj[u],key=str):
            if w!='v' and w not in par and col[w] in pair: par[w]=u;q.append(w)
    if b not in par: return None
    p=[b]
    while par[p[-1]] is not None: p.append(par[p[-1]])
    return p[::-1]
def nm(u): return 'c' if u=='c' else "%d.%d"%u
for n in range(int(sys.argv[4])):
    j=repeat_index(s,L); x0,m,x2,a,b=roles(L,j)
    al,ga=s[x0],s[a]; K=comp(adj,s,x2,{al,ga})
    P1=path(s,m,a,{s[m],s[a]}); P2=path(s,m,b,{s[m],s[b]})
    print(n,"j",j,"K",sorted(map(nm,K)),"P1(m-a)",list(map(nm,P1)) ,"P2(m-b)",list(map(nm,P2)))
    s=F(adj,s,L)
