"""[computed, exploratory, post hoc] pinch/(O)/tau data and c3 data on locked discs."""
import sys
from tn_lib import *
def path(adj,col,S,a,b,x):
    prev={a:None}; q=[a]
    for u in q:
        for w in adj[u]:
            if w!=x and w in col and col[w] in S and w not in prev: prev[w]=u; q.append(w)
    p=[b]
    while prev[p[-1]] is not None: p.append(prev[p[-1]])
    return p[::-1]
def run(line):
    cl,edges=parse(line); n,x,adj=build(cl,edges); V=n-1
    col={v:cl[v] for v in range(V)}; D,al,be,ga=0,1,2,3
    deg=lambda v:len(adj[v])
    csg,ig=comps(adj,col,{D,ga},x); K2=csg[ig[2]]
    csb,ib=comps(adj,col,{D,be},x); K0=csb[ib[0]]
    X={v for v in K2 if col[v]==D}; Y={v for v in K2 if col[v]==ga}
    X0={v for v in K0 if col[v]==D}; Y0={v for v in K0 if col[v]==be}
    P13=path(adj,col,{al,be},1,3,x); P14=path(adj,col,{al,ga},1,4,x)
    S=[v for v in P13 if v in P14]
    O=[v for v in P14 if v in S]==S
    ex=lambda s:sum(deg(v)-5 for v in s)
    d=len(Y)-len(X); tau2=-1-3*d-(ex(Y)-ex(X))
    faces=[f for f in range(0)]
    # faces of T: triangles
    tri=[(a,b,c) for a in range(n) for b in adj[a] if b>a for c in adj[a]&adj[b] if c>b]
    inO13=set(); 
    f13=[t for t in tri if x not in t and any(v in K2 for v in t)]
    f14=[t for t in tri if x not in t and any(v in K0 for v in t)]
    Lam=[t for t in f13 if t in f14]
    return dict(O=O,S=S,P13hitY0=[v for v in P13 if v in Y0],P14hitY=[v for v in P14 if v in Y],d=d,tau=tau2/2,XX0=X&X0,Lam=len(Lam),exY=ex(Y),exX=ex(X))
for line in open('../MathNDiscSearch/res_23.txt'):
    if 'DISC' in line:
        l=line[line.index('DISC'):].strip(); print(l[:20],run(l))
