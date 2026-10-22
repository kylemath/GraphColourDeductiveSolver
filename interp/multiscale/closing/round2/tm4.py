from tm import *
L=4; R=rows(L); idx={r:i for i,r in enumerate(R)}
succ={r:[r2 for r2 in itertools.product(*[[c for c in range(4) if c!=r[k] and c!=r[(k+1)%L]] for k in range(L)]) if all(r2[k]!=r2[(k+1)%L] for k in range(L))] for r in R}
lev=[r for r in R if tau(r)[0]<=1+1e-9]
import collections
print(collections.Counter(len(succ[r]) for r in lev))
r=lev[0]; print(r, succ[r], tau(r))
# canonical classes under perm, and reachable-ever sets
def canon(r): return min(tuple(p[c] for c in r) for p in PERMS)
for r in sorted(set(canon(x) for x in lev)):
    seen={r}; fr={r}; lays=[]
    for k in range(12):
        fr=set(y for x in fr for y in succ[x]); lays.append(len(set(canon(y) for y in fr)))
    print(r, tau(r), lays, sorted(set(canon(y) for y in fr)))
