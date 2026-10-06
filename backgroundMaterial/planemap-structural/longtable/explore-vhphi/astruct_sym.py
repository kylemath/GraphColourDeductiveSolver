import sys; sys.path.insert(0,'.')
from astruct_core import *
import astruct_a3 as A
adj,L,col,order,r=A.adj,A.L,A.col,A.order,A.r
def rot(c,k):
    out={}
    for u in c:
        if u in('c',): out[u]=c[u]
        else: out[u]=c[(u[0],(u[1]+k)%5)]
    return out
states=[];s=dict(col)
for n in range(20):
    states.append(s); s=F(adj,s,L)
cs=[canon(x,order) for x in states]
print("orbit up to renaming has",len(set(cs)),"states")
for k in range(1,5):
    rc=canon(rot(col,k),order)
    print("rot by",k,"-> equals canon of F^n(s) for n in",[n for n in range(20) if cs[n]==rc])
# reflection
def refl(c):
    out={}
    for u in c:
        out[u]=c[u] if u=='c' else c[(u[0],(-u[1])%5)]
    return out
print("not symmetric under rot^k combined with renaming itself:",[k for k in range(1,5) if canon(rot(col,k),order)==cs[0]])
