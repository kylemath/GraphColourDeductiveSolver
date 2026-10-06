#!/usr/bin/env python3
"""lattack_sym.py -- exhaustive F-chain census on the C5-symmetric stacked-antiprism triangulations A_r
(v, r pentagonal rings joined by antiprism strips, cap vertex v'); order 2+5r.  All proper 4-colourings of T-v with a
4-coloured link are enumerated (raw colourings, i.e. 24x over-count of colour renamings) and chain lengths histogrammed.
Single process, standard library + lattack_verify.  Validation / structured-family result only."""
import sys, math, time
import lattack_verify as LV
from collections import Counter

def antiprism_faces(r):
    pos = {}; name = lambda i, t: ("v" if i < 0 else "c" if i == r else (i, t % 5))
    pos["v"] = (0.0, 0.0); pos["c"] = (0.0, 0.0)
    for i in range(r):
        for t in range(5):
            th = 2 * math.pi * (t + 0.5 * i) / 5; rad = i + 1
            pos[(i, t)] = (rad * math.cos(th), rad * math.sin(th))
    tris = []
    for t in range(5): tris.append(("v", (0, t), (0, t + 1)))
    for i in range(r - 1):
        for t in range(5):
            tris.append(((i, t), (i, t + 1), (i + 1, t)))            # outer b_t between a_t, a_{t+1}
            tris.append(((i + 1, t), (i + 1, t + 1), (i, t + 1)))
    for t in range(5): tris.append(("c", (r - 1, t + 1), (r - 1, t)))  # cap
    def nm(x): return x if isinstance(x, str) else (x[0], x[1] % 5)
    out = []
    for (a, b, c) in tris:
        a, b, c = nm(a), nm(b), nm(c)
        # orient ccw using positions (cap/centre handled by sign choice below)
        out.append((a, b, c))
    return out

def make(r):
    tris = antiprism_faces(r)
    idx = {}
    for tr in tris:
        for x in tr: idx.setdefault(x, len(idx))
    faces = {tuple(idx[x] for x in tr) for tr in tris}
    return faces, idx

def fix_orientation(faces):
    """make the orientation consistent (each directed edge in exactly one face) by flipping faces greedily."""
    faces = list(faces); n = len(faces); orient = [None] * n; orient[0] = faces[0]
    edge_faces = {}
    for i, f in enumerate(faces):
        for k in range(3): edge_faces.setdefault(frozenset((f[k], f[(k + 1) % 3])), []).append(i)
    stack = [0]
    while stack:
        i = stack.pop(); f = orient[i]
        for k in range(3):
            a, b = f[k], f[(k + 1) % 3]
            for j in edge_faces[frozenset((a, b))]:
                if j == i or orient[j] is not None: continue
                g = faces[j]
                has = any((g[m], g[(m + 1) % 3]) == (a, b) for m in range(3))
                orient[j] = (g[0], g[2], g[1]) if has else g; stack.append(j)
    return set(orient)

def census(r):
    faces, idx = make(r); faces = fix_orientation(faces); rot = LV.faces_to_rot(faces)
    ok, msg = LV.check_triangulation(rot); assert ok, msg
    v = idx["v"]; link = rot[v]; adj = {u: [w for w in rot[u] if w != v] for u in rot if u != v}
    order = [u for u in adj]  # BFS order from link
    seen = list(link); S = set(seen); i = 0
    while i < len(seen):
        for w in adj[seen[i]]:
            if w not in S: S.add(w); seen.append(w)
        i += 1
    order = seen; col = {}; hist = Counter(); n4 = 0
    def dfs(i):
        nonlocal n4
        if i == len(order):
            if len(set(col[x] for x in link)) != 4: return
            n4 += 1; k, _ = LV.chain(adj, link, col); hist[k] += 1; return
        u = order[i]; used = {col[w] for w in adj[u] if w in col}
        for c in range(4):
            if c not in used: col[u] = c; dfs(i + 1); del col[u]
    # fix link colours for the first vertex to cut renaming a bit: x0 = colour 0 (x6 over-count instead of x24)
    col[order[0]] = 0; used0 = None
    # note: dfs below starts at index 1
    def start():
        dfs(1)
    start()
    return {"r": r, "order": len(rot), "colourings_with_4col_link(x0=0 fixed)": n4, "chain_hist": dict(sorted(hist.items()))}

if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    for r in map(int, sys.argv[1:]):
        t0 = time.process_time(); print(census(r), "cpu %.1f" % (time.process_time() - t0), flush=True)
