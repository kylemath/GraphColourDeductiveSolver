"""[exploratory] pathway P-B helpers: vacancy game on an explicit graph (adjacency only).
State = (hole h, colouring of G-h, canonical by first occurrence over sorted vertices).
Moves: whole-component Kempe swap in G-h; singleton slide of y in N(h) whose colour is unique on N(h).
Filled: N(h) uses <= 3 colours. Own code (stdlib); graph T4 from MathConjectureR.md faces."""
import sys, itertools
from collections import deque
sys.path.insert(0, '..')
T4F = [(0,1,2),(0,1,5),(0,2,3),(0,3,4),(0,4,5),(1,2,6),(1,5,10),(1,6,10),(2,3,7),(2,6,11),(2,7,11),(3,4,8),(3,7,8),(4,5,9),(4,8,9),(5,9,10),(6,10,15),(6,11,15),(7,8,12),(7,11,12),(8,9,13),(8,12,13),(9,10,14),(9,13,14),(10,14,15),(11,12,16),(11,15,16),(12,13,16),(13,14,16),(14,15,16)]
def from_faces(F):
    adj = {}
    for f in F:
        for a, b in itertools.permutations(f, 2): adj.setdefault(a, set()).add(b)
    return adj
def relabel(adj):
    ks = sorted(adj, key=str); m = {k: i for i, k in enumerate(ks)}
    return {m[k]: {m[w] for w in adj[k]} for k in ks}, m
def a3():
    import astruct_core as C
    adj = C.build(3); return relabel(adj)
def canon(col):
    mp = {}; out = {}
    for u in sorted(col):
        c = col[u]
        if c not in mp: mp[c] = len(mp)
        out[u] = mp[c]
    return out
def key(col): return tuple(sorted(col.items()))
def colourings(adj, h):
    vs = [u for u in sorted(adj) if u != h]
    order = []; seen = set()
    for s in vs:
        if s in seen: continue
        q = [s]; seen.add(s)
        while q:
            u = q.pop(0); order.append(u)
            for w in sorted(adj[u]):
                if w != h and w not in seen: seen.add(w); q.append(w)
    res = []; col = {}
    def rec(i, used):
        if i == len(order): res.append(dict(col)); return
        u = order[i]
        for c in range(min(used + 1, 4)):
            if all(col.get(w) != c for w in adj[u]):
                col[u] = c; rec(i + 1, max(used, c + 1)); del col[u]
    rec(0, 0); return res
def filled(adj, col, h): return len({col[w] for w in adj[h]}) <= 3
def comps(adj, col, h):
    out = []
    for a, b in itertools.combinations(range(4), 2):
        seen = set()
        for s in col:
            if s in seen or col[s] not in (a, b): continue
            K = {s}; st = [s]
            while st:
                u = st.pop()
                for w in adj[u]:
                    if w != h and w not in K and col[w] in (a, b): K.add(w); st.append(w)
            seen |= K; out.append((a, b, frozenset(K)))
    return out
def swap(col, a, b, K): return {u: ((b if c == a else a) if u in K else c) for u, c in col.items()}
def slides(adj, col, h):
    """list of (y, newcol, newhole): y's colour unique on N(h) (so h can take it)."""
    cs = [col[w] for w in adj[h]]; out = []
    for y in adj[h]:
        if cs.count(col[y]) == 1:
            n = dict(col); c = n.pop(y); n[h] = c; out.append((y, n))
    return out
def pure_radius(adj, col, h, cap=8):
    s0 = key(canon(col)); seen = {s0}; fr = [col]; d = 0
    while fr and d <= cap:
        for c in fr:
            if filled(adj, c, h): return d
        nf = []
        for c in fr:
            for a, b, K in comps(adj, c, h):
                n = canon(swap(c, a, b, K)); k = key(n)
                if k not in seen: seen.add(k); nf.append(n)
        fr = nf; d += 1
    return None
def mobility(adj, col, h, y):
    """shortest: [] filled-already; else list of ops reaching hole y or a filled state with <=1 swap+1 slide. returns (ops, newcol, newhole)"""
    if filled(adj, col, h): return ('filled0', col, h)
    for yy, n in slides(adj, col, h):
        if yy == y: return ('slide', n, y)
    for a, b, K in comps(adj, col, h):
        c2 = swap(col, a, b, K)
        if filled(adj, c2, h): return ('swap-fills', c2, h)
        for yy, n in slides(adj, c2, h):
            if yy == y: return ('swap+slide', n, y)
    return None
