"""[exploratory] P-B follow-up helpers (Long Table, 6 Oct 2026 afternoon). Own code, stdlib.
Generalises pb_lib to a SET of holes H (uncoloured vertices). Reuses canon/key/swap/from_faces/T4F from pb_lib.
Kempe swap = whole {a,b}-component of G - H. Pure radius computed exactly by BFS from filled states over the
(undirected, swaps are involutions) swap graph of all canonical colourings of G - h."""
import itertools, random
from collections import deque
from pb_lib import canon, key, swap, from_faces, relabel, T4F, a3
from pb_struct import hexanti

def colourings_H(adj, H):
    H = set(H); vs = [u for u in sorted(adj) if u not in H]
    order = []; seen = set()
    for s in vs:
        if s in seen: continue
        q = [s]; seen.add(s)
        while q:
            u = q.pop(0); order.append(u)
            for w in sorted(adj[u]):
                if w not in H and w not in seen: seen.add(w); q.append(w)
    res = []; col = {}
    def rec(i, used):
        if i == len(order): res.append(canon(col)); return
        u = order[i]
        for c in range(min(used + 1, 4)):
            if all(col.get(w) != c for w in adj[u]):
                col[u] = c; rec(i + 1, max(used, c + 1)); del col[u]
    rec(0, 0)
    return list({key(c): c for c in res}.values())

def comps_H(adj, col, H):
    out = []
    for a, b in itertools.combinations(range(4), 2):
        seen = set()
        for s in col:
            if s in seen or col[s] not in (a, b): continue
            K = {s}; st = [s]
            while st:
                u = st.pop()
                for w in adj[u]:
                    if w not in H and w not in K and col[w] in (a, b): K.add(w); st.append(w)
            seen |= K
            out.append((a, b, frozenset(K)))
    return out

def free(adj, col, h):
    """colours available at hole h (neighbours that are holes ignored)."""
    return [c for c in range(4) if all(col.get(w) != c for w in adj[h])]

def radius_table(adj, h):
    """exact pure radius of every canonical state at hole h: dict key(col) -> r, plus list of cols."""
    cols = colourings_H(adj, {h}); idx = {key(c): c for c in cols}
    nb = {}
    for k, c in idx.items():
        nb[k] = [key(canon(swap(c, a, b, K))) for a, b, K in comps_H(adj, c, {h})]
    dist = {k: 0 for k, c in idx.items() if free(adj, c, h)}
    q = deque(dist)
    while q:
        k = q.popleft()
        for n in nb[k]:
            if n not in dist: dist[n] = dist[k] + 1; q.append(n)
    return dist, idx, nb

def move_cost(adj, col, h, y, kmax=2):
    """least number s<=kmax of Kempe swaps (in G-h) after which y's colour is a singleton on N(h), so the
    hole moves h->y by colouring h with col[y] and uncolouring y. Returns ('fill', s) if a fill is met first
    (at s swaps, s<= that), ('move', s), or None if neither within kmax swaps. BFS over swap sequences."""
    fr = [col]; seen = {key(col)}
    for s in range(kmax + 1):
        for c in fr:
            if free(adj, c, h): return ('fill', s)
        for c in fr:
            cs = [c[w] for w in adj[h]]
            if cs.count(c[y]) == 1: return ('move', s)
        if s == kmax: break
        nf = []
        for c in fr:
            for a, b, K in comps_H(adj, c, {h}):
                n = swap(c, a, b, K); k = key(n)
                if k not in seen: seen.add(k); nf.append(n)
        fr = nf
    return None

def pentakis():
    """pentakis dodecahedron (order 32): 12 apexes of degree 5 (class (6^5)), 20 vertices of degree 6."""
    faces = []
    for t in range(5):
        faces += [('N', ('a', t), ('a', (t+1) % 5)), ('S', ('b', t), ('b', (t+1) % 5)),
                  (('a', t), ('a', (t+1) % 5), ('b', (t+1) % 5)), (('b', t), ('b', (t+1) % 5), ('a', t))]
    adj = {}
    def e(a, b): adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)
    for i, f in enumerate(faces):
        for v in f: e(v, ('f', i))
        for j, g in enumerate(faces):
            if j > i and len(set(f) & set(g)) == 2: e(('f', i), ('f', j))
    return relabel(adj)[0]

def graphs():
    return [('T4', from_faces(T4F)), ('order14', hexanti()), ('A_3', a3()[0])]
