# Adversarial-ish search on random planar triangulations: random connected 2-cluster split, random proper
# 4-colourings of each side, minimal R such that some renaming of B + recolouring within R of the seam works.
import random, itertools, sys, networkx as nx
from collections import deque
def lattice(m):
    G = nx.Graph()
    idx = lambda i, j: i*m + j
    for i in range(m):
        for j in range(m):
            if j+1 < m: G.add_edge(idx(i,j), idx(i,j+1))
            if i+1 < m: G.add_edge(idx(i,j), idx(i+1,j))
            if i+1 < m and j+1 < m: G.add_edge(idx(i,j), idx(i+1,j+1))
    # close outer face with an apex to make a triangulation
    n = m*m; outer = [v for v in G if G.degree(v) < 6]
    ok, emb = nx.check_planarity(G)
    # add apex adjacent to the outer boundary cycle
    bd = []
    for i in range(m): bd.append(idx(0,i))
    for i in range(1,m): bd.append(idx(i,m-1))
    for i in range(m-2,-1,-1): bd.append(idx(m-1,i))
    for i in range(m-2,0,-1): bd.append(idx(i,0))
    for v in bd: G.add_edge(n, v)
    return G
def flips(G, k, rng):
    for _ in range(k):
        u, v = rng.choice(list(G.edges()))
        com = [w for w in G[u] if w in G[v]]
        if len(com) != 2: continue
        a, b = com
        if G.has_edge(a, b) or G.degree(u) <= 3 or G.degree(v) <= 3: continue
        G.remove_edge(u, v); G.add_edge(a, b)
        if not nx.check_planarity(G)[0]: G.remove_edge(a, b); G.add_edge(u, v)
    return G
def rcol(V, adj, fixed, rng, limit=200000):
    col = dict(fixed); free = [v for v in V if v not in col]; rng.shuffle(free)
    free.sort(key=lambda v: -sum(1 for w in adj[v] if w in col or w in free))
    cnt = [0]
    def bt(k):
        cnt[0] += 1
        if cnt[0] > limit: raise TimeoutError
        if k == len(free): return True
        v = free[k]; xs = list(range(4)); rng.shuffle(xs)
        for x in xs:
            if all(col.get(w) != x for w in adj[v]):
                col[v] = x
                if bt(k+1): return True
                del col[v]
        return False
    return dict(col) if bt(0) else None
def trial(G, rng):
    V = list(G); adj = {v: set(G[v]) for v in V}
    s = rng.choice(V); A = {s}; fr = list(G[s]); target = len(V)//2
    while len(A) < target and fr:
        v = fr.pop(rng.randrange(len(fr)))
        if v in A: continue
        A.add(v); fr += [w for w in G[v] if w not in A]
    B = set(V) - A
    if not nx.is_connected(G.subgraph(B)): return None
    cA = rcol(sorted(A), {v: adj[v] & A for v in A}, {}, rng)
    cB = rcol(sorted(B), {v: adj[v] & B for v in B}, {}, rng)
    seam = {v for v in V for w in adj[v] if (v in A) != (w in A)}
    dist = {v: 0 for v in seam}; q = deque(seam)
    while q:
        v = q.popleft()
        for w in adj[v]:
            if w not in dist: dist[w] = dist[v]+1; q.append(w)
    D = max(dist.values())
    for R in range(0, D+1):
        far = [v for v in V if dist[v] > R]
        for pi in itertools.permutations(range(4)):
            fx = {v: (cA[v] if v in A else pi[cB[v]]) for v in far}
            try:
                if rcol(V, adj, fx, rng, 50000): return R, D, len(V)
            except TimeoutError: pass
    return D, D, len(V)
rng = random.Random(int(sys.argv[1])); m = int(sys.argv[2]); T = int(sys.argv[3])
hist = {}
for t in range(T):
    G = flips(lattice(m), 4*m*m, rng)
    try: r = trial(G, rng)
    except TimeoutError: continue
    if r: hist[r[0]] = hist.get(r[0], 0) + 1; print(r, flush=True) if r[0] >= 2 else None
print('m', m, 'minR histogram', sorted(hist.items()))
