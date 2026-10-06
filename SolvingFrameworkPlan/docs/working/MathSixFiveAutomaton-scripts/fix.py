from auto import *
import collections, time, pickle
def canon(c,T):
    m={}
    for x in c: m.setdefault(x,len(m))
    for x in range(4): m.setdefault(x,len(m))
    c2=tuple(m[x] for x in c)
    P=TYPES[T][0]; T2=type_of(m[P[0]],m[P[1]])
    return c2,T2
def succ(c,T,R):
    """returns (linkonly list of (c2,T,R)), (list of (c2,T,R, [c2 other types]))"""
    lo=[]; rt=[]
    for c2 in linkonly_moves(c): lo.append(c2)
    for p,q in TYPES[T]:
        for K in comps(c,p,q,R):
            if all(v<5 for v in K): continue
            rt.append(flip(c,K,p,q))
    return lo,rt
def node(c,T,R):
    c2,T2=canon(c,T); return (c2,T2,canonR(R))
t0=time.time()
nodes={}  # node -> (filled, lo successors nodes, rt list of (node, [(c2,T2) groups]))
groups={} # (c,T) canonical -> list of nodes
Q=collections.deque()
def getgroup(c,T):
    cc,TT=canon(c,T)
    if (cc,TT) not in groups:
        L=[]
        for R in structures(cc,TT):
            n=(cc,TT,canonR(R)); L.append(n)
            if n not in nodes: nodes[n]=None; Q.append(n)
        groups[(cc,TT)]=L
    return (cc,TT)
inits=[]
for p in pats:
    c=init(p); j,l1,l2=DLlocks(c)
    per=[]
    for T in range(3):
        g_=getgroup(c,T)
        ok=[n for n in groups[g_] if all(has_lock(n[0],n[2],l) for l in (l1,l2) if lockT(l)==T)]
        per.append(ok)
    inits.append((p,per))
while Q:
    n=Q.popleft(); c,T,R=n
    if filled(c): nodes[n]=(True,[],[]); continue
    lo,rt=succ(c,T,R)
    los=[]
    for c2 in lo:
        m=node(c2,T,R); los.append(m)
        if m not in nodes: nodes[m]=None; Q.append(m)
    rts=[]
    for c2 in rt:
        m=node(c2,T,R)
        if m not in nodes: nodes[m]=None; Q.append(m)
        gs=[getgroup(c2,T2) for T2 in range(3) if T2!=T]
        rts.append((m,gs))
    nodes[n]=(False,los,rts)
    if len(nodes)%200000==0: print(len(nodes),len(groups),round(time.time()-t0),flush=True)
print('explored',len(nodes),'groups',len(groups),round(time.time()-t0),flush=True)
# greatest fixpoint of BAD
bad={n for n,v in nodes.items() if not v[0]}
gbad={}
def groupbad(gk): return any(n in bad for n in groups[gk])
changed=True; it=0
while changed:
    changed=False; it+=1
    gb={gk:groupbad(gk) for gk in groups}
    rem=[]
    for n in bad:
        f,los,rts=nodes[n]
        ok=all(m in bad for m in los) and all((m in bad) and all(gb[g_] for g_ in gs) for m,gs in rts)
        if not ok: rem.append(n)
    if rem: bad-=set(rem); changed=True
    print('iter',it,'removed',len(rem),'bad',len(bad),flush=True)
gb={gk:groupbad(gk) for gk in groups}
res={}
for p,per in inits:
    res[p]=[any(n in bad for n in per[T]) for T in range(3)]
print('patterns where adversary wins forever (all three types have a bad lock-consistent structure):',sum(all(v) for v in res.values()))
pickle.dump((nodes,groups,bad,inits),open('fix.pkl','wb'))
