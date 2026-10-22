# Cross-check of Xandu numbers: directed graph on capped rows (maxrun<=k0), edge r->r' iff r'(i) not in {r(i),r(i+1)} and r' capped.
# Report: one-step closure, #ordered pairs joined by a capped path, max shortest path (no renaming; and up to the 24 renamings of the target).
import itertools, collections, sys
from itertools import permutations
def rows(L):
    out = []
    def rec(r):
        if len(r) == L:
            if r[-1] != r[0]: out.append(tuple(r))
            return
        for c in range(4):
            if not r or c != r[-1]: rec(r + [c])
    rec([]); return out
def maxrun(r):
    m = len(r); eq = [r[i] == r[(i+2) % m] for i in range(m)]
    if all(eq): return m
    s = eq.index(False); b = c = 0
    for j in range(1, m+1):
        if eq[(s+j) % m]: c += 1; b = max(b, c)
        else: c = 0
    return b + 2
def succ(r, L):
    res = []
    def rec(i, cur):
        if i == L:
            if cur[-1] != cur[0]: res.append(tuple(cur))
            return
        for c in range(4):
            if c in (r[i], r[(i+1) % L]) or (cur and c == cur[-1]): continue
            rec(i+1, cur + [c])
    rec(0, []); return res
k0 = int(sys.argv[1]) if len(sys.argv) > 1 else 3
P = list(permutations(range(4)))
for L in range(5, 10):
    C = [r for r in rows(L) if maxrun(r) <= k0]; Cs = set(C); ix = {r: i for i, r in enumerate(C)}
    adj = [[ix[s] for s in succ(r, L) if s in Cs] for r in C]
    closure = all(adj)
    tot = 0; mx = 0; totR = 0; mxR = 0
    orbit = [set(ix[tuple(p[c] for c in r)] for p in P) for r in C]
    for s in range(len(C)):
        d = [-1]*len(C); d[s] = 0; q = collections.deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if d[v] < 0: d[v] = d[u]+1; q.append(v)
        reach = [x for x in d if x > 0 or x == 0]
        tot += sum(1 for x in d if x >= 0); mx = max(mx, max(d))
        # up to renaming of target: distance to the orbit
        dd = [min((d[j] for j in orbit[t] if d[j] >= 0), default=-1) for t in range(len(C))]
        totR += sum(1 for x in dd if x >= 0); mxR = max(mxR, max(dd))
    print(f"L={L} k0={k0} ncap={len(C)} one_step_closure={closure} pairs={len(C)**2} joined={tot} max_shortest={mx}  | up_to_renaming: joined={totR} max_shortest={mxR}", flush=True)
