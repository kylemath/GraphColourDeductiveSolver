#!/usr/bin/env python3
"""lattack_symradius.py -- Kempe radius of infinite-chain colourings of A_r (r given on argv). Tiny, single process."""
import sys, lattack_sym as S, lattack_verify as LV, lattack_radius as R
for r in map(int, sys.argv[1:]):
    faces, idx = S.make(r); faces = S.fix_orientation(faces); rot = LV.faces_to_rot(faces)
    v = idx["v"]; link = rot[v]; adj = {u: [w for w in rot[u] if w != v] for u in rot if u != v}
    seen = list(link); Sx = set(seen); i = 0
    while i < len(seen):
        for w in adj[seen[i]]:
            if w not in Sx: Sx.add(w); seen.append(w)
        i += 1
    order = seen; col = {order[0]: 0}; inf = []
    def dfs(i):
        if i == len(order):
            if len(set(col[x] for x in link)) == 4:
                k, _ = LV.chain(adj, link, col, cap=40)
                if k >= 40: inf.append(dict(col))
            return
        u = order[i]; used = {col[w] for w in adj[u] if w in col}
        for c in range(4):
            if c not in used: col[u] = c; dfs(i + 1); del col[u]
    dfs(1)
    rs = [R.radius(rot, v, c)[0] for c in inf[:12]]
    print("A_%d" % r, "order", len(rot), "inf-chain colourings", len(inf), "radii of first 12:", rs, flush=True)
