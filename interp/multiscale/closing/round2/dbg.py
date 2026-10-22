from tm import *
import collections
L=8; R=rows(L); idx={r:i for i,r in enumerate(R)}; N=len(R)
succ=[[idx[r2] for r2 in itertools.product(*[[c for c in range(4) if c!=r[k] and c!=r[(k+1)%L]] for k in range(L)]) if all(r2[k]!=r2[(k+1)%L] for k in range(L))] for r in R]
lev=[i for i,r in enumerate(R) if tau(r)[0]<=1+1e-9]
def canonp(r): return min(tuple(p[c] for c in r) for p in PERMS)
levc=set(canonp(R[i]) for i in lev)
def first(a):
    fr={a}
    for k in range(1,20):
        fr=set(y for x in fr for y in succ[x])
        if levc <= set(canonp(R[y]) for y in fr): return k
ks=collections.Counter(first(idx[c]) for c in levc)
print(ks)
bad=[c for c in levc if first(idx[c])==5]
for c in bad:
    print(c, [first(idx[c[k:]+c[:k]]) for k in range(L)])
