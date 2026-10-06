import sys, subprocess, collections
from nlab import *
exec(open('up.py').read().split("P=sys.argv[1]")[0].split("from nlab import *")[1])
P=sys.argv[1]; x=int(sys.argv[2]); which=int(sys.argv[3])
line=subprocess.run([P,"-m5","17","-a"],capture_output=True,text=True).stdout.splitlines()[1]
rot=parse(line); n=len(rot); adj=[set(r) for r in rot]; ring=rot[x]
states=[]
for col in colourings_minus(adj,n,x):
    cl=classify(adj,x,ring,col)
    if cl is None: continue
    u,(D,al,be,ga)=cl
    pi=pair_info(adj,col,x); key=lambda p,q:(min(p,q),max(p,q))
    vec=(pi[key(D,al)],pi[key(D,be)],pi[key(D,ga)],pi[key(al,be)],pi[key(al,ga)],pi[key(be,ga)])
    if vec!=((1,0),(2,0),(2,0),(1,0),(1,0),(1,0)): continue
    if not all(not class_in_G(adj,n,x,u[j],col)[0] for j in (1,3,4)): continue
    states.append((col,u,(D,al,be,ga)))
col,u,(D,al,be,ga)=states[which]
nm={D:'D',al:'a',be:'b',ga:'g'}
csg,idg=comps(adj,col,{D,ga},x); K2=csg[idg[u[2]]]
c2=swap_comp(col,K2,D,ga)
y=u[0]
fixed=c2[y]   # colour of u0 in c' = D
print("c' word",[nm[c2[w]] for w in u])
# hexagon: D-free swaps only (pairs not containing colour `fixed`), x coloured fixed
G=[set(a) for a in adj]; G[x].discard(y); G[y].discard(x)
def fmt(st): return ''.join(nm[st[w]] for w in u)
st0=tuple((c2[v] if v!=x else fixed) for v in range(n))
seen={canon(st0):st0}; q=deque([st0]); E=[]
while q:
    st=q.popleft()
    for a,b,K,nc in kneighbors(G,n,st):
        if fixed in (a,b): continue
        k=canon(nc)
        if k not in seen: seen[k]=nc; q.append(nc)
print("D'-free hexagon size",len(seen))
def pairstr(st):
    colx={v:st[v] for v in range(n) if v!=x}
    pi=pair_info(adj,colx,x)
    return ' '.join(nm[a]+nm[b]+':'+str(pi[(a,b)][0])+('c'+str(pi[(a,b)][1]) if pi[(a,b)][1] else '') for (a,b) in PAIRS)
def broken(st):
    colx={v:st[v] for v in range(n) if v!=x}
    cs_,idx=comps(adj,colx,{st[y],be},x)
    return not any(st[w]==be and idx[w]==idx[y] for w in ring if w!=y)
for k,st in seen.items():
    print(" node word",fmt(st),"|",pairstr(st))
    # one D-involving swap -> broken?
    outs=[]
    for a,b,K,nc in kneighbors(G,n,st):
        if fixed not in (a,b): continue
        stn=nc
        colx={v:stn[v] for v in range(n) if v!=x}
        # first-order broken for apex u0 in nc: chain {c(u0),k}
        s=stn[y]; brk=[]
        for kk in set(range(4))-{s}:
            cs_,idx=comps(adj,colx,{s,kk},x)
            if not any(stn[w]==kk and idx[w]==idx[y] for w in ring if w!=y): brk.append(nm[kk])
        outs.append((nm[a]+nm[b],len(K),'x' if x in K else '',tuple(brk)))
    print("     D-swaps (pair,size,hasx,broken chains):",outs)
