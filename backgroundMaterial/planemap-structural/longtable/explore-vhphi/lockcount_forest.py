"""EXPLORATORY. For each locked member: edge counts e_ij between colour classes in T-x, whether complementary
pairs {j,l} (not containing c(y)) induce forests, and slack in the counting inequalities.
Usage: plantri FLAGS N -a | python3 lockcount_forest.py N IDX[,IDX...]"""
import sys, itertools
from collections import Counter
import tilley_apex as TA, vhphi_explore as E, lock_anatomy as LA
n = int(sys.argv[1]); want = set(map(int, sys.argv[2].split(",")))
lines = [l for l in sys.stdin if l.strip()]
def forest(adj, S):
    seen = set(); 
    for s in S:
        if s in seen: continue
        comp = {s}; st = [s]
        while st:
            u = st.pop()
            for w in adj[u]:
                if w in S and w not in comp: comp.add(w); st.append(w)
        seen |= comp
        if sum(1 for u in comp for w in adj[u] if w in S)//2 != len(comp)-1: return False
    return True
agg = Counter()
for gi in sorted(want):
    rot = TA.parse(lines[gi]); N = len(rot); adj = [set(r) for r in rot]
    for x in range(N):
        if len(rot[x]) != 5: continue
        legal = {f[0] for f in E.legal_fans(rot, x, adj)}
        for i, y in enumerate(rot[x]):
            if i not in legal: continue
            G = [set(a) for a in adj]; G[x].discard(y); G[y].discard(x)
            allc, comp = LA.classes(G, N)
            sep = {comp[c] for c in allc if c[x] != c[y]}
            locked = {comp[c] for c in allc if c[x] == c[y]} - sep
            for k in locked:
                for c in (c for c in allc if comp[c] == k):
                    one = c[y]; T = [w for w in range(N) if w != x]
                    sz = {a: sum(1 for w in T if c[w] == a) for a in range(4)}
                    e = Counter()
                    for u in T:
                        for w in adj[u]:
                            if w > u and w != x: e[tuple(sorted((c[u], c[w])))] += 1
                    full = all(LA.chain(G, c, y, o) == {w for w in range(N) if c[w] in (one, o)} for o in set(range(4))-{one})
                    oth = sorted(set(range(4)) - {one})
                    fo = [forest({u: adj[u] - {x} for u in T}, {w for w in T if c[w] in p}) for p in itertools.combinations(oth, 2)]
                    S1 = sum(e[tuple(sorted((one, o)))] for o in oth)
                    e234 = sum(e[p] for p in itertools.combinations(oth, 2))
                    agg[(tuple(sorted(sz.values())), full, tuple(fo), S1, e234)] += 1
print("order", n, "(sizes, chains-full, complement-pairs-forest, S1'=sum deg of colour-of-y class in T-x, E234) : count")
for k, v in sorted(agg.items()): print(k, v)
