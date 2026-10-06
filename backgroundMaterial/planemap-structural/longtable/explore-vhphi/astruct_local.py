#!/usr/bin/env python3
"""astruct_local.py: is the set of infinite-chain ring sequences (ring0=01023, rings only; cap forced up to the 2-fold swap) equal to the set of
all paths in the layered 'union graph' of its own consecutive-ring transitions (position dependent, window 2)?  r=4..8."""
import sys,collections; sys.path.insert(0,'.')
from astruct_delete import S
for r in range(4,9):
    rs=set(seq for seq,cc in S[r])
    E=[set() for _ in range(r-1)]
    for s in rs:
        for i in range(r-1): E[i].add((s[i],s[i+1]))
    paths=[(s,) for s in set(x[0] for x in E[0])]  # ring0
    paths=[(a,b) for (a,b) in E[0]]
    for i in range(1,r-1):
        paths=[p+(b,) for p in paths for (a,b) in E[i] if a==p[-1]]
    print("r",r,"ring sequences (true)",len(rs),"paths in union graph",len(paths),"equal" if set(paths)==rs else "NOT equal")
print("--- layer stability: is E_r[i] (consecutive-ring transitions at depth i->i+1) equal for r=7 and r=8? as sets")
EE={}
for r in range(4,9):
    rs=set(seq for seq,cc in S[r]); E=[set() for _ in range(r-1)]
    for s in rs:
        for i in range(r-1): E[i].add((s[i],s[i+1]))
    EE[r]=E
for r in (7,8):
    print("r",r,"sizes of E[i]:",[len(x) for x in EE[r]])
for i in range(7):
    print("depth",i,"E_7==E_8:",EE[7][i]==EE[8][i] if i<6 else None, "subset:",EE[8][i]<=EE[7][i] if i<6 else None)
# solutions of r=8 restricted to shorter depth: is the set of first k rings of r=8 solutions == that of r=7 solutions?
for k in (3,4,5,6):
    a=set(s[:k] for s,c in S[8]); b=set(s[:k] for s,c in S[7]); print("first",k,"rings: r=8 prefixes",len(a),"r=7 prefixes",len(b),"r8 subset r7" ,a<=b,"equal",a==b)
