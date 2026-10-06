#!/usr/bin/env python3
"""pd_lib.py -- [exploratory] Tait (edge-colouring) view of a degree-5 hole. stdlib only.
Colours 0..3 are read as Z2xZ2 (bit vectors); Tait colour of edge uw of G-v is c(u)^c(w) in {1,2,3}.
Reuses astruct_core (locks, F, comp) unchanged: hole vertex is named 'v'."""
import sys, itertools
sys.path.insert(0, '..')
from astruct_core import build as build_A, locks, doubly, F, comp, repeat_index, roles, canon

T4_FACES = [(0,1,2),(0,1,5),(0,2,3),(0,3,4),(0,4,5),(1,2,6),(1,5,10),(1,6,10),(2,3,7),(2,6,11),(2,7,11),(3,4,8),(3,7,8),(4,5,9),(4,8,9),(5,9,10),(6,10,15),(6,11,15),(7,8,12),(7,11,12),(8,9,13),(8,12,13),(9,10,14),(9,13,14),(10,14,15),(11,12,16),(11,15,16),(12,13,16),(13,14,16),(14,15,16)]

def faces_from_adj(adj):
    V = list(adj); idx = {u: i for i, u in enumerate(V)}
    fs = set()
    for a in V:
        for b in adj[a]:
            for c in adj[a] & adj[b]:
                fs.add(frozenset((a, b, c)))
    return [tuple(f) for f in fs]

def make_graph(faces, hole):
    """relabel: hole -> 'v'. returns adj (hole named 'v'), faces, link order L."""
    nm = lambda u: 'v' if u == hole else ('v0' if u == 'v' else u)
    fs = [tuple(nm(u) for u in f) for f in faces]
    adj = {}
    for f in fs:
        for a in f:
            adj.setdefault(a, set()).update(x for x in f if x != a)
    # link order: cycle through faces containing v
    nb = {}
    for f in fs:
        if 'v' in f:
            a, b = [u for u in f if u != 'v']
            nb.setdefault(a, []).append(b); nb.setdefault(b, []).append(a)
    start = sorted(nb, key=str)[0]; L = [start]; prev = None; cur = start
    while True:
        nxt = [w for w in nb[cur] if w != prev][0] if prev is not None else nb[cur][0]
        if nxt == start: break
        L.append(nxt); prev, cur = cur, nxt
    assert len(L) == 5 and len(nb) == 5
    return adj, fs, L

def dual(adj, fs):
    """dual H of G-v: nodes = triangles without v, plus 'P'. edges: dict edge(frozenset)->(node1,node2)."""
    node = lambda f: 'P' if 'v' in f else frozenset(f)
    ef = {}
    for f in fs:
        for a, b in itertools.combinations(f, 2):
            if a == 'v' or b == 'v': continue
            ef.setdefault(frozenset((a, b)), []).append(node(f))
    assert all(len(x) == 2 for x in ef.values())
    return {e: tuple(x) for e, x in ef.items()}

def tait(col, H):
    """edge colour dict, vertex-colour xor"""
    return {e: col[next(iter(e))] ^ col[list(e)[1]] for e in H}

def check_tait(col, H):
    """each non-P node has 3 distinct nonzero edge colours; P has 5 edges with xor 0"""
    inc = {}
    for e, (p, q) in H.items():
        t = col[next(iter(e))] ^ col[list(e)[1]]
        assert t in (1, 2, 3)
        inc.setdefault(p, []).append(t); inc.setdefault(q, []).append(t)
    for n, ts in inc.items():
        if n == 'P':
            x = 0
            for t in ts: x ^= t
            assert len(ts) == 5 and x == 0
        else:
            assert sorted(ts) == [1, 2, 3], (n, ts)
    return True

def hole_edges(col, adj, L):
    """P-edge Tait colours e_t = c(x_t)^c(x_{t+1}), t=0..4"""
    return [col[L[t]] ^ col[L[(t + 1) % 5]] for t in range(5)]

def components(H, tcol, pair):
    """connected components of H restricted to edges with Tait colour in pair; returns list of node sets"""
    nbr = {}
    for e, (p, q) in H.items():
        if tcol[e] in pair:
            nbr.setdefault(p, []).append(q); nbr.setdefault(q, []).append(p)
    allnodes = set(x for pq in H.values() for x in pq)
    seen = set(); comps = []
    for n in allnodes:
        if n in seen: continue
        c = {n}; st = [n]
        while st:
            u = st.pop()
            for w in nbr.get(u, []):
                if w not in c: c.add(w); st.append(w)
        seen |= c; comps.append(c)
    return comps

def p_paths(H, tcol, L, adj, pair):
    """follow (pair)-bichromatic paths out of P. returns dict t -> t' (indices of P-edges e_t, e_t') paired by a path,
    only for P-edges whose colour is in pair."""
    # edge index t <-> edge frozenset(L[t],L[t+1])
    pe = {frozenset((L[t], L[(t + 1) % 5])): t for t in range(5)}
    inc = {}
    for e, (p, q) in H.items():
        inc.setdefault(p, []).append((e, q)); inc.setdefault(q, []).append((e, p))
    res = {}
    for e0, t0 in pe.items():
        if tcol[e0] not in pair: continue
        cur_e = e0; node = [q for (e, q) in inc['P'] if e == e0][0]
        while node != 'P':
            want = [e for (e, q) in inc[node] if tcol[e] in pair and e != cur_e]
            assert len(want) == 1
            cur_e = want[0]; node = [q for (e, q) in inc[node] if e == cur_e][0]
        res[t0] = pe[cur_e]
    return res

def colourings(adj, L, x0=0):
    """all proper 4-colourings of G-v (hole 'v') with c(L[0])=x0 and 4-coloured link, as dict"""
    V = [u for u in adj if u != 'v']
    # BFS order from L[0]
    order = [L[0]]; seen = {L[0]}
    for u in order:
        for w in sorted(adj[u], key=str):
            if w != 'v' and w not in seen: seen.add(w); order.append(w)
    col = {L[0]: x0}; out = []
    def rec(i):
        if i == len(order):
            if len({col[x] for x in L}) == 4: out.append(dict(col))
            return
        u = order[i]
        used = {col[w] for w in adj[u] if w in col}
        for c in range(4):
            if c not in used:
                col[u] = c; rec(i + 1); del col[u]
    rec(1)
    return out, order
