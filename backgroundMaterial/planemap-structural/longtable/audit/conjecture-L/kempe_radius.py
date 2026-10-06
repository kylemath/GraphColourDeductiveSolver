#!/usr/bin/env python3
"""Kempe class in T - v (whole two-colour components, v absent) of the L witnesses: size in
canonical states, number filled (link <= 3 colours), BFS distance from s to the nearest filled state.
Audit code; uses only l_check.py."""
import json
from l_check import (from_faces, link, comp, W6_FACES, W6_V, W6_COL, A3_FACES, A3_V, A3_COL, build_A,
                     colourings, repeat_index, locked, chain)

def canon(col, order):
    m = {}; return tuple(m.setdefault(col[w], len(m)) for w in order)

def kclass(adj, col, L, v, cap=2_000_000):
    order = sorted(w for w in adj if w != v)
    start = canon(col, order); dist = {start: 0}; q = [dict(zip(order, start))]; filled = {}; i = 0
    while i < len(q):
        c = q[i]; i += 1; k = canon(c, order); d = dist[k]
        if len({c[x] for x in L}) <= 3: filled[k] = d
        for p in range(4):
            for r in range(p + 1, 4):
                done = set()
                for s in order:
                    if c[s] in (p, r) and s not in done:
                        K = comp(adj, c, s, p, r, v); done |= K
                        n = dict(c)
                        for w in K: n[w] = r if c[w] == p else p
                        kn = canon(n, order)
                        if kn not in dist:
                            if len(dist) >= cap: return None
                            dist[kn] = d + 1; q.append(n)
    return dict(class_size=len(dist), filled=len(filled), radius=min(filled.values()) if filled else None)

out = {}
adj = from_faces(W6_FACES); out['W6'] = kclass(adj, W6_COL, [13, 8, 3, 5, 1], W6_V)
adj = from_faces(A3_FACES); out['A3_witness'] = kclass(adj, A3_COL, link(A3_FACES, A3_V), A3_V)
for r in (3, 4, 5):
    faces, v = build_A(r); adj = from_faces(faces); L = link(faces, v)
    radii = {}; seen = set(); nclass = 0
    for col in colourings(adj, v, {L[0]: 0}):
        if repeat_index(col, L) is None or not locked(adj, col, L, v): continue
        if chain(adj, col, L, v)[1] != 'infinite': continue
        res = kclass(adj, col, L, v)
        key = (res['class_size'], res['filled'], res['radius']); radii[str(key)] = radii.get(str(key), 0) + 1
    out[f'A{r}_all_infinite_chain_states'] = radii
print(json.dumps(out, indent=1))
