"""[exploratory] R-greedy hole walk on T4 from every radius-4 state: print trace; check it never cycles and total length."""
from collections import Counter
from pb_lib import *
def holemoves(adj, c, h):
    res = []
    for y, n in slides(adj, c, h):
        if len(adj[y]) == 5: res.append((f"slide->{y}", y, canon(n)))
    for a, b, K in comps(adj, c, h):
        c2 = swap(c, a, b, K)
        for y, n in slides(adj, c2, h):
            if len(adj[y]) == 5: res.append((f"swap{{{a},{b}}}|K|={len(K)}+slide->{y}", y, canon(n)))
    return res
def greedy(adj, h, c, verbose=False):
    seen = set(); trace = []; steps = 0
    while True:
        r = pure_radius(adj, c, h)
        trace.append((h, r))
        if r <= 1: return steps + r, trace, False
        k = (h, key(c))
        if k in seen: return None, trace, True
        seen.add(k)
        best = min(holemoves(adj, c, h), key=lambda m: (pure_radius(adj, m[2], m[1]), m[1]))
        if verbose: print("    ", best[0])
        h, c = best[1], best[2]; steps += 1
adj = from_faces(T4F); res = Counter(); first = True
for h in [u for u in adj if len(adj[u]) == 5]:
    seen = set()
    for c in colourings(adj, h):
        c = canon(c)
        if key(c) in seen: continue
        seen.add(key(c))
        if pure_radius(adj, c, h) == 4:
            n, tr, cyc = greedy(adj, h, c, verbose=first and h == 4)
            if first and h == 4: print("  trace (hole, R):", tr); first = False
            res[(n, cyc)] += 1
print("[exploratory] T4, R-greedy hole-move walk from the 22 radius-4 states: (total moves incl. final swap, cycled?) ->", dict(res))
