import sys, itertools, collections
L = "46 70 1 2 1 3 3 4 4 5 5 6 2 6 1 7 2 8 8 9 9 10 7 10 3 11 7 12 11 12 4 13 11 14 13 14 5 0 13 15 15 16 16 0 6 17 17 0 8 18 17 19 18 19 9 20 18 21 20 21 10 22 20 23 23 24 22 24 12 25 22 25 14 26 25 27 27 28 26 28 15 29 26 29 16 30 29 31 30 31 30 32 32 33 0 33 19 34 0 34 21 35 34 36 35 36 23 37 35 37 24 38 38 39 37 40 39 40 27 38 28 41 41 42 39 42 31 41 32 43 42 43 33 44 44 45 43 45 36 44 40 45 20 46 48 22 17".split()
x = list(map(int, L)); n, m = x[0], x[1]
E = [(x[2+2*i], x[3+2*i]) for i in range(m)]
F = x[2+2*m:]
print('n', n, 'm', m, 'f-edge ids', F, '->', [E[i] for i in F], 'tail len', len(F))
deg = collections.Counter(a for e in E for a in e)
print('deg v=0:', deg[0], ' other degrees:', collections.Counter(deg[u] for u in range(1, n)))
inc = collections.defaultdict(list)
for i, (a, b) in enumerate(E): inc[a].append(i); inc[b].append(i)
# all perfect matchings (as frozensets of edge ids)
PM = []
def rec(used, chosen):
    u = next((w for w in range(n) if w not in used), None)
    if u is None: PM.append(frozenset(chosen)); return
    for i in inc[u]:
        a, b = E[i]; w = b if a == u else a
        if w not in used:
            used.add(u); used.add(w); chosen.append(i); rec(used, chosen); chosen.pop(); used.discard(u); used.discard(w)
rec(set(), [])
fidx = {e: k for k, e in enumerate(F)}
def k_of(M): return next(fidx[i] for i in M if i in fidx)
print('#PM', len(PM))
def ham(A, B):
    S = A | B; adj = collections.defaultdict(list)
    for i in S: a, b = E[i]; adj[a].append(b); adj[b].append(a)
    seen = {0}; st = [0]
    while st:
        u = st.pop()
        for w in adj[u]:
            if w not in seen: seen.add(w); st.append(w)
    return len(seen) == n
idx = {M: i for i, M in enumerate(PM)}
arcs = collections.defaultdict(list); narcs = 0; nham = 0
for M in PM:
    k = k_of(M)
    for M2 in PM:
        if not (M & M2) and k_of(M2) == (k - 2) % 5:
            arcs[idx[M]].append(idx[M2]); narcs += 1; nham += ham(M, M2)
print('#arcs', narcs, '#Ham arcs', nham)
# SCCs (Tarjan, iterative-ish via recursion limit)
sys.setrecursionlimit(10000)
index = {}; low = {}; onst = set(); st = []; sccs = []; c = [0]
def sc(v):
    index[v] = low[v] = c[0]; c[0] += 1; st.append(v); onst.add(v)
    for w in arcs[v]:
        if w not in index: sc(w); low[v] = min(low[v], low[w])
        elif w in onst: low[v] = min(low[v], index[w])
    if low[v] == index[v]:
        comp = []
        while True:
            w = st.pop(); onst.discard(w); comp.append(w)
            if w == v: break
        sccs.append(comp)
for v in range(len(PM)):
    if v not in index: sc(v)
cyc = [s for s in sccs if len(s) > 1]
print('cyclic SCCs', [len(s) for s in cyc])
for s in cyc:
    S = set(s); hin = [(a, b) for a in s for b in arcs[a] if b in S and ham(PM[a], PM[b])]
    print(' SCC size', len(s), 'Ham arcs inside', len(hin))
    # connectivity of E - M (figure-eight?) for states in SCC
    for a in s:
        rest = set(range(m)) - PM[a]
        adj = collections.defaultdict(list)
        for i in rest: p, q = E[i]; adj[p].append(q); adj[q].append(p)
        seen = {0}; stk = [0]
        while stk:
            u = stk.pop()
            for w in adj[u]:
                if w not in seen: seen.add(w); stk.append(w)
        comps = 1 + sum(1 for _ in [])  # placeholder
        # count components of E-M
        allv = set(range(n)); ncomp = 0; vis = set()
        for s0 in range(n):
            if s0 in vis: continue
            ncomp += 1; stk = [s0]; vis.add(s0)
            while stk:
                u = stk.pop()
                for w in adj[u]:
                    if w not in vis: vis.add(w); stk.append(w)
        print('   state', a, 'k', k_of(PM[a]), 'components of E-M:', ncomp)
