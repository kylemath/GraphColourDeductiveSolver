#!/usr/bin/env python3
"""Pure-Kempe fill radius at one degree-5 hole: for every state of T - x (up to renaming), the
least number of whole-component swaps in T - x to a filled state (ring <= 3 colours).
Multi-source BFS from the filled states. Uses the audit's own wp20_audit helpers. [exploratory]"""
import sys, json, time
from collections import deque, Counter
sys.path.insert(0, '../wp20-replay')
from wp20_audit import Graph, enum_colourings, swaps, canon, masks_from

def radius(rot, x):
    G = Graph(rot); n = G.n; ring = rot[x]
    order = [v for v in range(n) if v != x]; pos = {v: i for i, v in enumerate(order)}
    domain = ((1 << n) - 1) & ~(1 << x)
    t = time.time(); states = enum_colourings(G, order); idx = {s: i for i, s in enumerate(states)}
    filled = [len({s[pos[r]] for r in ring}) <= 3 for s in states]
    adj = []
    for s in states:
        adj.append({idx[canon(m2, order)] for m2 in swaps(G.nb, masks_from(s, order), domain)})
    dist = [-1] * len(states); q = deque()
    for i, f in enumerate(filled):
        if f: dist[i] = 0; q.append(i)
    while q:
        a = q.popleft()
        for b in adj[a]:
            if dist[b] < 0: dist[b] = dist[a] + 1; q.append(b)
    h = Counter(dist)
    return dict(x=x, states=len(states), filled=sum(filled), radius_hist={str(k): v for k, v in sorted(h.items())},
                targetless=h.get(-1, 0), secs=round(time.time() - t, 1))

if __name__ == '__main__':
    rot = json.load(open(sys.argv[1]))['rot']
    print(json.dumps(radius(rot, int(sys.argv[2]))))
