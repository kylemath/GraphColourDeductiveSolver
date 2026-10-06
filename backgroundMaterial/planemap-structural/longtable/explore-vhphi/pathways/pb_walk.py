"""[exploratory] (1) mobility consistency on all deg-5 holes/states; (2) A_3: walk to the pole; (3) mixed vacancy-game distance vs pure radius on T4, A_3."""
import sys, time
from collections import deque, Counter
from pb_lib import *
t0 = time.process_time()
def run(name, adj):
    deg = {u: len(adj[u]) for u in adj}
    d5 = [u for u in adj if deg[u] == 5]
    allst = {}; fail = 0; tot = 0; kinds = Counter()
    for h in d5:
        cols = [canon(c) for c in colourings(adj, h)]
        uniq = {key(c): c for c in cols}; allst[h] = list(uniq.values())
        for c in allst[h]:
            if filled(adj, c, h): continue
            for y in adj[h]:
                if deg[y] != 5: continue
                tot += 1
                r = mobility(adj, c, h, y)
                if r is None: fail += 1
                else: kinds[r[0]] += 1
    print(f"[exploratory] {name}: deg-5 holes {len(d5)}; unfilled (state,deg5-neighbour) pairs {tot}; mobility failures {fail}; kinds {dict(kinds)}")
    # pure radius per hole
    for h in d5:
        hist = Counter(); 
        for c in allst[h]:
            r = pure_radius(adj, c, h); hist[r] += 1
        print(f"   hole {h}: states {len(allst[h])}, pure-radius hist {dict(sorted(hist.items(), key=lambda x: str(x[0])))}")
    # mixed game over (hole,col) for holes of any degree (slides only; swaps); BFS from filled states backwards is awkward -> forward BFS per state is costly; do multi-source reverse via full graph
    states = {}
    for h in adj:
        for c in colourings(adj, h): states[(h, key(canon(c)))] = (h, canon(c))
    print(f"   mixed game: {len(states)} states over all holes")
    nbr = {k: [] for k in states}
    for k, (h, c) in states.items():
        for a, b, K in comps(adj, c, h):
            n = canon(swap(c, a, b, K)); nbr[k].append((h, key(n)))
        for y, n in slides(adj, c, h):
            nn = canon(n); nbr[k].append((y, key(nn)))
    # distance to filled: reverse BFS
    rev = {k: [] for k in states}
    for k, vs in nbr.items():
        for v in vs:
            assert v in states
            rev[v].append(k)
    dist = {k: 0 for k, (h, c) in states.items() if filled(adj, c, h)}
    q = deque(dist)
    while q:
        k = q.popleft()
        for p in rev[k]:
            if p not in dist: dist[p] = dist[k] + 1; q.append(p)
    # compare at deg-5 holes: mixed dist vs pure radius (pure = hole fixed)
    cmp = Counter()
    for h in d5:
        for c in allst[h]:
            kk = (h, key(canon(c)))
            pr = pure_radius(adj, c, h); md = dist.get(kk)
            cmp[(pr, md)] += 1
    print("   (pure radius, mixed distance) counts at deg-5 holes:", dict(sorted(cmp.items(), key=str)))
    unreached = sum(1 for k in states if k not in dist)
    print("   unreached states in mixed game:", unreached)
    return adj, allst, dist
adjT = from_faces(T4F)
run('T4', adjT)
run('A_3', a3()[0])
print("cpu", round(time.process_time() - t0, 1))
