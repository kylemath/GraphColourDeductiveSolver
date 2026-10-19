"""Cone test: a plane triangulation with finitely many non-6 vertices (all-6 rings outside a core) and sum(6-d) >= 1.
If one avoids the forbidden set, no discharging rule of ANY radius (whose admissible views are the registry-free ones)
proves t <= 0: far-out flat views carry zero net transfer (180-degree symmetry), so the core keeps sum(6-d) > 0."""
import sys, collections
from ball import *
def regstats(C):
    allsix = [c[0] for c in C if all(c[3][u] == 6 for u in c[2])]
    diam = 0
    for c in C:
        U, E = c[2], c[4]
        for s in U:
            d = {s: 0}; q = [s]
            for x in q:
                for y in E[x]:
                    if y not in d: d[y] = d[x] + 1; q.append(y)
            assert len(d) == len(U), c[0]
            diam = max(diam, max(d.values()))
    return allsix, diam
def build(D, rings, extra):
    """rings: list of degree lists for rings 1..K (exact); then `extra` all-6 rings; then one unknown ring (99) + 9s."""
    L = Layered(D)
    for r in rings: L.add_ring(r)
    for _ in range(extra): L.add_ring([6] * len(L.ring()))
    last = list(L.ring()); L.add_ring([9] * len(last))
    deg = dict(L.deg); deg[0] = D
    for x in last: deg[x] = 99
    names = [x for x in deg]
    adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    P = names; S = set(P)
    pa = {x: {y for y in adj[x] if y in S} for x in P}
    pf = {frozenset(f) for f in L.tris if all(y in S for y in f)}
    return L, P, pa, pf, deg
def contains(C, P, pa, pf, fd, stop=True):
    hits = []
    for c in C:
        e = grow.embeddings(c, P, pa, pf, fd)
        if e:
            hits.append((c[0], sorted(next(iter(e)))))
            if stop: break
    return hits
if __name__ == '__main__':
    C = registry(); a, dm = regstats(C); print('configs', len(C), 'all-6 configs', a, 'max interior diameter', dm)
    for D in (5,):
        L, P, pa, pf, fd = build(5, [], dm + 3)
        print('single five in hex plane: |P|', len(P), 'ring lengths', [len(r) for r in L.rings])
        h = contains(C, P, pa, pf, fd, stop=False); print('hits', len(h), h[:5])
