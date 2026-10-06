import pickle
from auto import *
nodes,groups,bad0,inits=pickle.load(open('fix.pkl','rb'))
from fixJ import joins
# attractor ranks for us when adversary limited to <=J joins (J=2): rank = least k with g^k true
J=2
allowed={n for n in nodes if joins(*n)<=J}
rank={n:0 for n in allowed if nodes[n][0]}
gr={}
for k in range(1,12):
    grk={gk:all(n in rank for n in L if n in allowed) for gk,L in groups.items()}
    new={}
    for n in allowed:
        if n in rank: continue
        f,los,rts=nodes[n]
        if any(m in rank for m in los) or any(((m in rank) or any(grk[g_] for g_ in gs)) for m,gs in rts):
            new[n]=k
    # note: m in rank only counts if m allowed (rank only has allowed); a leaked T-move keeps R so m allowed iff n allowed
    rank.update(new)
    # pattern resolution
    res=[]
    for p,per in inits:
        ok=any(all(n in rank for n in per[T] if n in allowed) for T in range(3))
        res.append(ok)
    print('k',k,'new',len(new),'patterns resolved',sum(res),flush=True)
    if all(res): break
