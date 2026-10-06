#!/usr/bin/env python3
"""lattack_sym_component.py -- Kempe-class (all swaps on T-v) of the infinite-chain colourings of A_r: do they reach a
filled state (link <= 3 colours)?  Standard library + lattack_verify, lattack_sym.  Single process, tiny."""
import sys, lattack_sym as S, lattack_verify as LV
from collections import Counter

def run(r):
    faces, idx = S.make(r); faces = S.fix_orientation(faces); rot = LV.faces_to_rot(faces)
    v = idx["v"]; link = rot[v]; adj = {u: [w for w in rot[u] if w != v] for u in rot if u != v}
    verts = sorted(adj)
    seen = list(link); Sx = set(seen); i = 0
    while i < len(seen):
        for w in adj[seen[i]]:
            if w not in Sx: Sx.add(w); seen.append(w)
        i += 1
    order = seen; col = {order[0]: 0}; allcol = []
    def dfs(i):
        if i == len(order): allcol.append(tuple(col[u] for u in verts)); return
        u = order[i]; used = {col[w] for w in adj[u] if w in col}
        for c in range(4):
            if c not in used: col[u] = c; dfs(i + 1); del col[u]
    dfs(1)
    pos = {u: k for k, u in enumerate(verts)}
    def kempe_nbrs(t):
        c = {u: t[pos[u]] for u in verts}; out = set(); done = set()
        for u in verts:
            for d in range(4):
                if d == c[u]: continue
                key = (u, frozenset((c[u], d)))
                K = LV.comp(adj, c, u, {c[u], d})
                if (min(K), frozenset((c[u], d))) in done: continue
                done.add((min(K), frozenset((c[u], d))))
                n = dict(c)
                for w in K: n[w] = d if c[w] == c[u] else c[u]
                out.add(tuple(n[x] for x in verts))
        return out
    # note: swapping can change colour 0 of order[0]; classes are therefore over all 24 renamings: normalise by
    # canonical renaming (first-seen order of colours along `order`) to keep the state space small.
    def canon(t):
        m = {}; res = []
        for u in order: m.setdefault(t[pos[u]], len(m))
        return tuple(m[t[pos[u]]] for u in verts)
    states = {canon(t) for t in allcol}
    def has4(t): return len({t[pos[x]] for x in link}) == 4
    # components of the canonical state graph
    comp_id = {}; comps = []
    for s0 in sorted(states):
        if s0 in comp_id: continue
        cid = len(comps); comp_id[s0] = cid; st = [s0]; mem = [s0]
        while st:
            t = st.pop()
            for n in kempe_nbrs(t):
                n = canon(n)
                if n not in comp_id: comp_id[n] = cid; st.append(n); mem.append(n)
        comps.append(mem)
    print("order", len(rot), "states(canonical)", len(states), "components", len(comps))
    for cid, mem in enumerate(comps):
        nf = sum(1 for t in mem if not has4(t)); 
        chains = Counter()
        for t in mem:
            if has4(t):
                c = {u: t[pos[u]] for u in verts}; k, _ = LV.chain(adj, link, c, cap=40); chains[k] += 1
        print(" comp", cid, "size", len(mem), "filled", nf, "unfilled", len(mem) - nf, "chain hist (unfilled)", dict(sorted(chains.items())))

if __name__ == "__main__":
    for r in map(int, sys.argv[1:]): run(r)
