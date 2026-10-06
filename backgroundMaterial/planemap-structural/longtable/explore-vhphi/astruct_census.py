#!/usr/bin/env python3
"""astruct_census.py r : ring-transfer enumeration of all proper 4-colourings of A_r - v with x0=0 and 4-colour link,
keep those whose F-orbit (raw, cap 400) is all doubly locked; report orbit classes up to renaming. Single process."""
import sys,itertools,time; sys.path.insert(0,'.')
from astruct_core import *
rings=[c for c in itertools.product(range(4),repeat=5) if all(c[t]!=c[(t+1)%5] for t in range(5))]
def compat(a,b): # ring i = a, ring i+1 = b: b_t ~ a_t,a_{t+1}
    return all(b[t]!=a[t] and b[t]!=a[(t+1)%5] for t in range(5))
nxt={a:[b for b in rings if compat(a,b)] for a in rings}
def census(r,cap=400):
    adj=build(r);L=link(r);order=[u for u in adj if u!='v']
    res={}; n=0; capex=[]
    def rec(seq):
        nonlocal n
        if len(seq)==r:
            used=set(seq[-1])
            for ccol in range(4):
                if ccol in used: continue
                col={'v':None,'c':ccol}
                for i in range(r):
                    for t in range(5): col[(i,t)]=seq[i][t]
                n+=1
                o=orbit(adj,col,L,order,cap=cap,renaming=True)
                if o[2] and o[0] is not None:
                    res.setdefault(canon(col,order),o)
                elif o[2]: capex.append(1)
            return
        for b in nxt[seq[-1]]: rec(seq+[b])
    for a in rings:
        if len(set(a))==4 and a[0]==0: rec([a])
    print(' cap-exhausted all-locked (undecided):',len(capex)); return n,res
if __name__=="__main__":
    for r in map(int,sys.argv[1:]):
        t0=time.process_time(); n,res=census(r)
        print("r",r,"colourings(x0=0,4-colour link)",n,"periodic all-locked states (x0=0, canonical forms; fixed-x0 raw classes):",len(res),"cpu %.1f"%(time.process_time()-t0),flush=True)
        import collections
        print(" periods(up to renaming):",collections.Counter(v[0] for v in res.values()))
        for k in list(res)[:1]:
            print(" example ring colours:",[k[5*i:5*i+5] for i in range(r)],k[-1] if False else "")
