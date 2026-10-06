"""[exploratory] successors of the highest-radius states; order-14 graph; per-hole max radius."""
import time
from collections import Counter
from pb_lib import *
from pb_struct import hexanti
def holemoves(adj, c, h):
    res = []
    for y, n in slides(adj, c, h):
        if len(adj[y]) == 5: res.append((y, canon(n)))
    for a, b, K in comps(adj, c, h):
        c2 = swap(c, a, b, K)
        for y, n in slides(adj, c2, h):
            if len(adj[y]) == 5: res.append((y, canon(n)))
    return res
t0 = time.process_time()
def hi(name, adj):
    deg = {u: len(adj[u]) for u in adj}; d5 = [u for u in adj if deg[u] == 5]
    mx = {}; 
    for h in d5:
        rs = [pure_radius(adj, canon(c), h) for c in colourings(adj, h)]
        mx[h] = max(rs)
    print(f"[exploratory] {name}: max pure radius per deg-5 hole: {mx}")
    top = max(mx.values()); prof = Counter()
    for h in d5:
        seen = set()
        for c in colourings(adj, h):
            c = canon(c)
            if key(c) in seen: continue
            seen.add(key(c))
            if pure_radius(adj, c, h) == top:
                prof[(h, tuple(sorted(Counter(pure_radius(adj, n, y) for y, n in holemoves(adj, c, h)).items())))] += 1
    print(f"   states at radius {top}: hole-move successor radius histograms (hole, [(R', count)]) -> #states")
    for k, v in sorted(prof.items()): print("    ", k, v)
hi('T4', from_faces(T4F))
hi('A_3', a3()[0])
hi('order-14 bicapped hexagonal antiprism', hexanti())
print("cpu", round(time.process_time() - t0, 1))
