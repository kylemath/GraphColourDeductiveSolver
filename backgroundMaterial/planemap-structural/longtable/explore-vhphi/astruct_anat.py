import sys; sys.path.insert(0,'.')
from astruct_core import *
import astruct_a3 as A
adj,L,col,order,r=A.adj,A.L,A.col,A.order,A.r
def show(c):
    return " | ".join("".join(str(c[(i,t)]) for t in range(5)) for i in range(r))+" | cap "+str(c['c'])
s=dict(col)
for n in range(24):
    j=repeat_index(s,L); x0,m,x2,a,b=roles(L,j)
    al,ga=s[x0],s[a]; K=comp(adj,s,x2,{al,ga})
    print(n,show(s),"j=%d"%j,"link",[s[x] for x in L],"swapK size",len(K),"K rings",sorted(str(u[0]) if u!='c' else 'c' for u in K))
    s=F(adj,s,L)
