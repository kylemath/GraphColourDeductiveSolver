import sys,collections; sys.path.insert(0,'.')
from astruct_core import *
from astruct_census import rings,nxt
def hist(r,cap=60):
    adj=build(r);L=link(r);order=[u for u in adj if u!='v']
    H=collections.Counter(); lk=collections.Counter(); n=0
    def chain(col):
        s=dict(col);k=0
        while k<cap:
            if repeat_index(s,L) is None or not doubly(adj,s,L): return k
            s=F(adj,s,L);k+=1
        return k
    def rec(seq):
        nonlocal n
        if len(seq)==r:
            for cc in range(4):
                if cc in seq[-1]: continue
                col={'v':None,'c':cc}
                for i in range(r):
                    for t in range(5): col[(i,t)]=seq[i][t]
                n+=1; H[chain(col)]+=1
                if len(set(col[x] for x in L))==4: lk[locks(adj,col,L)]+=1
            return
        for b in nxt[seq[-1]]: rec(seq+[b])
    for a in rings:
        if len(set(a))==4 and a[0]==0: rec([a])
    return n,dict(sorted(H.items())),dict(lk)
for r in range(2,6): print("r",r,hist(r))
