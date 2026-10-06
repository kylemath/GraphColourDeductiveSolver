#!/usr/bin/env python3
"""astruct_list.py r: list infinite-chain colourings of A_r with ring0 = 01023 exactly (renaming fixed by ring 0) """
import sys,itertools; sys.path.insert(0,'.')
from astruct_core import *
from astruct_census import rings,nxt
def listsol(r):
    adj=build(r);L=link(r);order=[u for u in adj if u!='v'];out=[]
    def rec(seq):
        if len(seq)==r:
            for cc in range(4):
                if cc in seq[-1]: continue
                col={'v':None,'c':cc}
                for i in range(r):
                    for t in range(5): col[(i,t)]=seq[i][t]
                o=orbit(adj,col,L,order,cap=400,renaming=True)
                if o[2] and o[0] is not None: out.append((seq,cc))
            return
        for b in nxt[seq[-1]]: rec(seq+[b])
    rec([(0,1,0,2,3)]); return out
if __name__=="__main__":
    r=int(sys.argv[1]); sol=listsol(r); print(r,len(sol))
    for seq,cc in sol: print(" ".join("".join(map(str,x)) for x in seq),"cap",cc)
