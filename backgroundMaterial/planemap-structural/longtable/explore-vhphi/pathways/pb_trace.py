"""[exploratory] explicit traces + descent test.  python3 pb_trace.py"""
import sys, time
from collections import deque, Counter
from pb_lib import *
t0 = time.process_time()
def moves(adj, c, h):
    out = []
    for a, b, K in comps(adj, c, h):
        out.append((f"swap{{{a},{b}}}|K|={len(K)}", h, canon(swap(c, a, b, K))))
    for y, n in slides(adj, c, h): out.append((f"slide {h}->{y}", y, canon(n)))
    return out
def bfs_path(adj, h, c):
    s = (h, key(c)); par = {s: None}; dq = deque([(h, c)])
    while dq:
        hh, cc = dq.popleft()
        if filled(adj, cc, hh):
            path = []; k = (hh, key(cc))
            while par[k]: path.append(par[k][1]); k = par[k][0]
            return path[::-1], (hh, cc)
        for lab, h2, c2 in moves(adj, cc, hh):
            k2 = (h2, key(c2))
            if k2 not in par: par[k2] = ((hh, key(cc)), lab); dq.append((h2, c2))
def linkword(adj, c, h, ring): return [c[w] for w in ring]
def show(adj, c, h, ring):
    return f"hole {h} link {linkword(adj,c,h,ring)} R={pure_radius(adj,c,h)}"
# ---- T4: hole 4, link 0,3,8,9,5 (cyclic order from MathConjectureR)
adj = from_faces(T4F); deg = {u: len(adj[u]) for u in adj}
ring4 = [0, 3, 8, 9, 5]
cols = [canon(c) for c in colourings(adj, 4)]
uniq = {key(c): c for c in cols}.values()
r4 = [c for c in uniq if pure_radius(adj, c, 4) == 4]
print("[exploratory] T4 hole 4 radius-4 states:", len(r4))
for c in r4:
    p, (hf, cf) = bfs_path(adj, 4, c)
    print(" state link word", linkword(adj, c, 4, ring4), "full-game shortest:", len(p), "moves:", p)
# ---- T4 hole-move descent test: successors by hole-moving moves only (slide, swap+slide) across deg-5 holes
def holemoves(adj, c, h):
    res = []
    for y, n in slides(adj, c, h):
        if len(adj[y]) == 5: res.append((y, canon(n)))
    for a, b, K in comps(adj, c, h):
        c2 = swap(c, a, b, K)
        for y, n in slides(adj, c2, h):
            if len(adj[y]) == 5: res.append((y, canon(n)))
    return res
def descent(name, adj):
    deg = {u: len(adj[u]) for u in adj}; d5 = [u for u in adj if deg[u] == 5]
    R = {}
    for h in d5:
        for c in colourings(adj, h):
            c = canon(c); R[(h, key(c))] = (pure_radius(adj, c, h), c)
    stuck = []; strict = 0; tot = 0; cyc = 0
    for (h, k), (r, c) in R.items():
        if r == 0: continue
        tot += 1
        succ = [R[(y, key(n))][0] for y, n in holemoves(adj, c, h)]
        if succ and min(succ) < r: strict += 1
        else: stuck.append((h, k, r, sorted(set(succ))))
    print(f"[exploratory] {name}: states with R>=1 at deg-5 holes: {tot}; some hole-move strictly lowers R: {strict}; none lowers R (hole-move-greedy stuck): {len(stuck)}")
    cs = Counter((r, tuple(s)) for h, k, r, s in stuck)
    print("   stuck profile (R, successor-R set):", dict(cs))
    return R, stuck
RT, stT = descent('T4', adj)
adjA, mA = a3()
RA, stA = descent('A_3', adjA)
# ---- A_3 witness trace (rings 01023|23101|02323, cap 1), hole v = id 16, ring0 = ids 0..4
col = {}
rings = ["01023", "23101", "02323"]
for i, s in enumerate(rings):
    for t, ch in enumerate(s): col[i * 5 + t] = int(ch)
col[15] = 1
assert all(col[u] != col[w] for u in col for w in adjA[u] if w in col), "witness not proper"
ringA = [0, 1, 2, 3, 4]
print("[exploratory] A_3 witness: link word", linkword(adjA, col, 16, ringA), "R at pole:", pure_radius(adjA, col, 16))
p, _ = bfs_path(adjA, 16, canon(col)); print(" shortest fill, full game:", len(p), p)
for y in ringA:
    r = mobility(adjA, canon(col), 16, y)
    print(f" mobility pole->{y}: {r[0]}  new hole {r[2]}  R_new={pure_radius(adjA, r[1], r[2])}")
print("cpu", round(time.process_time() - t0, 1))
