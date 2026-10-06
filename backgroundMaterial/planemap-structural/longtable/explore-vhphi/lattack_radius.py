#!/usr/bin/env python3
"""lattack_radius.py -- Kempe distance r(s) from a state to the nearest filled state (link <= 3 colours), by BFS over
ALL Kempe swaps of T-v (states canonically renamed).  Used to compare the L-chain witnesses with 'targetless'
(r = infinity).  Standard library + lattack_verify.  Single process; BFS capped at CAP states."""
import sys, json, lattack_verify as LV
CAP = 300000

def radius(rot, v, col, cap=CAP):
    link = rot[v]; adj = {u: [w for w in rot[u] if w != v] for u in rot if u != v}; verts = sorted(adj)
    pos = {u: i for i, u in enumerate(verts)}; ordr = sorted(adj, key=lambda u: (u not in link, u))
    def canon(c):
        m = {}
        for u in ordr: m.setdefault(c[u], len(m))
        return tuple(m[c[u]] for u in verts)
    def filled(t): return len({t[pos[x]] for x in link}) < 4
    s0 = canon(col); dist = {s0: 0}; fr = [s0]; d = 0
    while fr:
        if any(filled(t) for t in fr): return d, len(dist)
        nxt = []
        for t in fr:
            c = {u: t[pos[u]] for u in verts}; done = set()
            for u in verts:
                for e in range(4):
                    if e == c[u]: continue
                    K = LV.comp(adj, c, u, {c[u], e}); key = (min(K), frozenset((c[u], e)))
                    if key in done: continue
                    done.add(key); n = dict(c)
                    for w in K: n[w] = e if c[w] == c[u] else c[u]
                    n = canon(n)
                    if n not in dist:
                        dist[n] = d + 1; nxt.append(n)
        fr = nxt; d += 1
        if len(dist) > cap: return None, len(dist)
    return float("inf"), len(dist)

