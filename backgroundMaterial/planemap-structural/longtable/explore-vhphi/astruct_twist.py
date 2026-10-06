#!/usr/bin/env python3
"""astruct_twist.py file r : for every listed solution test F^n s ~ rot^k s (up to colour renaming), smallest n>=1, all k."""
import sys,collections; sys.path.insert(0,'.')
from astruct_core import *
def rot(c,k):
    return {u:(c[u] if u=='c' or u=='v' else c[(u[0],(u[1]+k)%5)]) for u in c}
def run(lines,r):
    adj=build(r);L=link(r);order=[u for u in adj if u!='v']
    res=collections.Counter()
    for l in lines:
        p=l.split(); rows=p[:-2]; cc=int(p[-1])
        s={'v':None,'c':cc}
        for i in range(r):
            for t in range(5): s[(i,t)]=int(rows[i][t])
        c0=canon(s,order); x=dict(s); found=None
        for n in range(1,41):
            x=F(adj,x,L)
            ks=[k for k in range(5) if canon(rot(x,k),order)==c0]
            if ks and found is None: found=(n,tuple(ks))
        res[found]+=1
    return res
if __name__=="__main__":
    for r in range(3,9):
        lines=open('/private/tmp/claude-501/x/l%d.txt'%r).read().splitlines()[1:] if r>=7 else None
        if lines is None:
            from astruct_list import listsol
            lines=[" ".join("".join(map(str,x)) for x in seq)+" cap "+str(cc) for seq,cc in listsol(r)]
        print("r",r,"n solutions",len(lines),"(smallest n with F^n s ~ rot^k s, ks):",dict(run(lines,r)))
