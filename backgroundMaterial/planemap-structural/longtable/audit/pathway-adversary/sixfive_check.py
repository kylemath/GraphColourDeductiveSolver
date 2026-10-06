#!/usr/bin/env python3
"""P-E replay of Math's (6^5) result (MathSixFiveHole.md; 12:18 message): over plantri orders given,
every degree-5 hole whose neighbours all have degree >= 6. For each: canonical states of T - x,
pure-Kempe radius to a filled state (multi-source BFS), doubly locked (DL) states per Math's definition
(MathConfinementAttack Step 1, link = plantri rotation at x), and the radius of DL states.
Audit code (wp20_audit helpers, own lock test). [exploratory, spent orders]"""
import sys, json, time
from collections import deque, Counter
sys.path.insert(0, '../wp20-replay')
from wp20_audit import Graph, enum_colourings, swaps, canon, masks_from, comp_mask

def cls(seq):
    seq = [min(d, 9) for d in seq]; c = []
    for s in (seq, seq[::-1]):
        for i in range(5): c.append(tuple(s[i:] + s[:i]))
    return min(c)

def analyse(rot, x):
    G = Graph(rot); n = G.n; ring = rot[x]
    order = [v for v in range(n) if v != x]; pos = {v: i for i, v in enumerate(order)}
    domain = ((1 << n) - 1) & ~(1 << x)
    states = enum_colourings(G, order); idx = {s: i for i, s in enumerate(states)}
    rc = lambda s: [s[pos[r]] for r in ring]
    filled = [len(set(rc(s))) <= 3 for s in states]
    adj = [{idx[canon(m, order)] for m in swaps(G.nb, masks_from(s, order), domain)} for s in states]
    dist = [-1] * len(states); q = deque(i for i in range(len(states)) if filled[i])
    for i in q: dist[i] = 0
    while q:
        a = q.popleft()
        for b in adj[a]:
            if dist[b] < 0: dist[b] = dist[a] + 1; q.append(b)
    def dl(s):
        c = rc(s)
        if len(set(c)) != 4: return False
        j = next(j for j in range(5) if c[j] == c[(j + 2) % 5])
        m, a, b = ring[(j + 1) % 5], ring[(j + 3) % 5], ring[(j + 4) % 5]
        def joined(u, w):
            p, q2 = s[pos[u]], s[pos[w]]
            allowed = 0
            for v in order:
                if s[pos[v]] in (p, q2): allowed |= 1 << v
            return bool(comp_mask(G.nb, allowed, u) >> w & 1)
        return joined(m, a) and joined(m, b)
    DL = [i for i, s in enumerate(states) if dl(s)]
    return dict(states=len(states), targetless=dist.count(-1), max_radius=max(dist),
                dl=len(DL), dl_radius=dict(Counter(dist[i] for i in DL)))

out = {'by_class': {}, 'holes': []}
t0 = time.time()
for path in sys.argv[1:]:
    for gi, line in enumerate(open(path)):
        if not line.strip(): continue
        nn, rest = line.split(); rot = [[ord(c) - 97 for c in p] for p in rest.split(',')]
        deg = [len(r) for r in rot]
        for x in range(len(rot)):
            if deg[x] != 5 or min(deg[w] for w in rot[x]) < 6: continue
            k = cls([deg[w] for w in rot[x]]); r = analyse(rot, x)
            r.update(order=int(nn), graph=gi, x=x, cls=k); out['holes'].append(r)
            b = out['by_class'].setdefault(str(k), dict(holes=0, max_radius=0, dl=0, dl_r3plus=0, targetless=0))
            b['holes'] += 1; b['max_radius'] = max(b['max_radius'], r['max_radius']); b['dl'] += r['dl']
            b['dl_r3plus'] += sum(v for kk, v in r['dl_radius'].items() if kk >= 3); b['targetless'] += r['targetless']
out['secs'] = round(time.time() - t0, 1)
print(json.dumps(out, default=str))
