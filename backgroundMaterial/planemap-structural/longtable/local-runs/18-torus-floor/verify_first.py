#!/usr/bin/env python3
"""[exploratory] Independent check (no kempe_py) of the smallest violation found: T(4,4)-family n=16, v=11, a frozen 4-colouring of T-v whose link uses 4 colours."""
import itertools
faces = [[0,1,5],[0,1,12],[0,3,4],[0,3,12],[0,4,5],[1,2,6],[1,2,13],[1,5,6],[1,12,13],[2,3,7],[2,3,14],[2,6,7],[2,13,14],[3,4,7],[3,12,15],[3,14,15],[4,5,8],[4,7,8],[5,6,10],[5,8,9],[5,9,10],[6,7,11],[6,10,15],[6,11,15],[7,8,11],[8,9,13],[8,11,12],[8,12,13],[9,10,14],[9,13,14],[10,14,15],[11,12,15]]
v = 11
order = [6,1,2,5,7,10,15,0,12,13,3,14,4,8,9]; cols = (0,1,2,3,3,2,1,2,3,0,0,3,1,2,1)
col = dict(zip(order, cols))
adj = {i: set() for i in range(16)}
E = set()
for f in faces:
    for a, b in itertools.combinations(f, 2): adj[a].add(b); adj[b].add(a); E.add((min(a,b),max(a,b)))
assert 16 - len(E) + len(faces) == 0, "Euler"
print('V,E,F =', 16, len(E), len(faces), 'degrees', [len(adj[i]) for i in range(16)])
assert all(col[a] != col[b] for a in col for b in adj[a] if b != v and a != v), "not proper"
link = sorted(adj[v]); print('link', link, 'colours', [col[x] for x in link], '-> colours used', len(set(col[x] for x in link)))
frozen = True
for p, q in itertools.combinations(range(4), 2):
    S = [u for u in col if col[u] in (p, q)]; seen = set(); ncomp = 0
    for s in S:
        if s in seen: continue
        ncomp += 1; st = [s]; seen.add(s)
        while st:
            x = st.pop()
            for y in adj[x]:
                if y in col and col[y] in (p, q) and y not in seen: seen.add(y); st.append(y)
    print('pair', (p, q), 'vertices', len(S), 'components', ncomp)
    frozen &= (ncomp == 1)
print('FROZEN (every {p,q}-subgraph connected, so every Kempe swap is a renaming):', frozen)
