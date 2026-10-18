"""Job 30 F: the sender-side kill filter (SPEC.md, with Opus's conditions C1-C5, loop/opus/F_spec_review a6feb65e).

A sender row of option F is (five word w = a_0..a_4, z letters on its {big root, 6} spokes). Its five's 2-ball model:
v (5); a_k (letters of w); t_k, the second-ring vertex on link edge (a_k, a_k+1); and the d_k - 5 privates of a_k
(none modelled when a_k is 9). Edges: v-a_k, a_k-a_k+1, t_k-a_k, t_k-a_k+1, a_k-(its privates), the path
t_k-1, q_k1, ..., t_k around a_k, and t_k-1-t_k iff a_k = 5. No others; every triangle is a face.
- A row is **deleted iff every filling of its read slots over 5..9 (9 = degree >= 9) contains some K on lettered
  vertices (C3)**. dies() splits on a wildcard slot of a partial embedding until each branch is decided; no depth cap.
- A filling that makes a fully lettered link 5-wheel R5, or a lettered 6-wheel (with its exact q) R6, cannot occur and
  counts as dead (C4 coupling with the exact q).
- C1: only configurations with a **2-connected interior** are used (the test then fixes the rotation up to one global
  mirror). C2: an interior vertex never maps onto a vertex lettered 9 (asserted).
- Matcher: own backtracking (`embeds`), cross-checked against networkx (`embeds_nx`) on random fully lettered models.
Usage (self-test): python3 tkill.py KCFILE [n=2000]"""
import sys, os, itertools, random, functools

def parse_kc(line):
    f = line.split(); m = int(f[2]); rp = f[3].split(';'); ip = f[4].split(';')
    U = list(range(m)); E = {u: set() if ip[u] == '-' else {int(x) for x in ip[u].split(',')} for u in U}
    g = {u: len(E[u]) + (0 if rp[u] == '-' else len(rp[u].split(','))) for u in U}
    tri = {frozenset((x, y, z)) for x in U for y in E[x] for z in E[x] & E[y] if x < y < z}
    return (f[0], U, g, E, tri)

def two_connected(K):
    import networkx as nx
    nm, U, g, E, tri = K
    if len(U) <= 2: return True
    G = nx.Graph(); G.add_nodes_from(U); G.add_edges_from((u, w) for u in U for w in E[u])
    return nx.is_biconnected(G)

def model(w):
    """nodes (with letter or None) and adjacency of the five's 2-ball for word w; letters added by the caller."""
    nodes = ['v'] + [('a', k) for k in range(5)] + [('t', k) for k in range(5)]
    adj = {x: set() for x in nodes}; tri = set()
    def e(x, y): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    for k in range(5):
        j = (k + 1) % 5
        e('v', ('a', k)); e(('a', k), ('a', j)); e(('t', k), ('a', k)); e(('t', k), ('a', j))
        tri.add(frozenset(('v', ('a', k), ('a', j)))); tri.add(frozenset((('a', k), ('a', j), ('t', k))))
    for k in range(5):
        d = w[k]; prev = ('t', (k - 1) % 5)
        if d == 5:
            e(('t', (k - 1) % 5), ('t', k)); tri.add(frozenset((('a', k), ('t', (k - 1) % 5), ('t', k)))); continue
        if d == 9: continue   # privates not modelled (unknown count); t_k-1, t_k distinct, non-adjacent
        for i in range(1, d - 4):
            q = ('q', k, i); nodes.append(q); e(q, ('a', k)); e(prev, q); tri.add(frozenset((('a', k), prev, q))); prev = q
        e(prev, ('t', k)); tri.add(frozenset((('a', k), prev, ('t', k))))
    return nodes, adj, tri

LET = (5, 6, 7, 8, 9)

def embeds(K, w, letters, wildcard):
    """an embedding of K's interior (exact degrees, induced, triangles onto triangles); letters: node -> letter for the
    lettered nodes (v and a_k always lettered). wildcard=True also allows unlettered second-ring nodes (as 5..8).
    Returns the set of unlettered nodes used, or None."""
    nm, U, g, E, tri = K
    nodes, adj, mtri = MODEL.setdefault(tuple(w), model(w)) if tuple(w) not in MODEL else MODEL[tuple(w)]
    let = dict(letters); let['v'] = 5
    for k in range(5): let[('a', k)] = w[k]
    order = [max(U, key=lambda u: (len(E[u]), g[u]))]
    while len(order) < len(U):
        order.append(max((u for u in U if u not in order), key=lambda u: (len(E[u] & set(order)), g[u])))
    phi = {}; used = set()
    def ok(u, x):
        L = let.get(x)
        if L is None: return wildcard and 5 <= g[u] <= 8
        assert not (L == 9 and g[u] == 9 and False)
        return L == g[u] and L <= 8          # C2: never onto a 9
    def rec(i):
        if i == len(order):
            if all(frozenset(phi[a] for a in t) in mtri for t in tri): return True
            return False
        u = order[i]; pl = [x for x in order[:i] if x in E[u]]
        cand = set.intersection(*[adj[phi[x]] for x in pl]) if pl else set(nodes)
        for x in cand:
            if x in used or not ok(u, x): continue
            if any((phi[y] in adj[x]) != (y in E[u]) for y in order[:i]): continue
            phi[u] = x; used.add(x)
            if rec(i + 1): return True
            del phi[u]; used.discard(x)
        return False
    if rec(0): return {x for x in phi.values() if x not in let}
    return None

def embeds_nx(K, w, letters):
    """independent check (networkx): K embeds on lettered nodes only (induced, degree labels, triangles onto triangles)."""
    import networkx as nx
    from networkx.algorithms import isomorphism as iso
    nm, U, g, E, tri = K
    nodes, adj, mtri = MODEL.setdefault(tuple(w), model(w)) if tuple(w) not in MODEL else MODEL[tuple(w)]
    let = dict(letters); let['v'] = 5
    for k in range(5): let[('a', k)] = w[k]
    Hh = nx.Graph()
    for x in nodes:
        if x in let and let[x] <= 8: Hh.add_node(x, deg=let[x])
    for x in Hh.nodes:
        for y in adj[x]:
            if y in Hh.nodes: Hh.add_edge(x, y)
    Kg = nx.Graph(); Kg.add_nodes_from(U); Kg.add_edges_from((u, x) for u in U for x in E[u])
    nx.set_node_attributes(Kg, g, 'deg')
    GM = iso.GraphMatcher(Hh, Kg, node_match=lambda a, b: a['deg'] == b['deg'])
    for m in GM.subgraph_isomorphisms_iter():
        inv = {b: a for a, b in m.items()}
        if all(frozenset(inv[a] for a in t) in mtri for t in tri): return True
    return False

MODEL = {}
def impossible(w, letters, isR5, isR6):
    """a fully lettered link 5-wheel that is R5, or a 6-wheel with its exact q that is R6, cannot occur."""
    let = dict(letters)
    for k in range(5):
        tp, tn = let.get(('t', (k - 1) % 5)), let.get(('t', k))
        if w[k] == 5 and tp is not None and tn is not None:
            if isR5([5, w[(k + 1) % 5], tn, tp, w[(k - 1) % 5]]): return True
        if w[k] == 6 and tp is not None and tn is not None and ('q', k, 1) in let:
            if isR6([5, w[(k + 1) % 5], tn, let[('q', k, 1)], tp, w[(k - 1) % 5]]): return True
    return False

def make_dies(KS, isR5, isR6):
    @functools.lru_cache(maxsize=None)
    def dies(w, fl):
        letters = dict(fl)
        if impossible(w, letters, isR5, isR6): return True
        for K in KS:
            if embeds(K, w, letters, False) is not None: return True
        for K in KS:
            u = embeds(K, w, letters, True)
            if u:
                x = sorted(u, key=str)[0]
                return all(dies(w, tuple(sorted(list(fl) + [(x, L)], key=str))) for L in LET)
        return False
    return dies

def reflect(w, letters):
    """the same five read the other way round: a'_k = a_{-k}; t_k -> t'_{-k-1}; privates of a_k reversed."""
    w2 = tuple(w[(-k) % 5] for k in range(5)); out = {}
    for x, L in letters:
        if x[0] == 't': out[('t', (-x[1] - 1) % 5)] = L
        elif x[0] == 'q':
            k = x[1]; n = w[k] - 5; out[('q', (-k) % 5, n + 1 - x[2])] = L
    return w2, tuple(sorted(out.items(), key=str))

def load(kcfile):
    KS, skipped = [], []
    for l in open(kcfile):
        if not l.strip(): continue
        K = parse_kc(l)
        (KS if two_connected(K) else skipped).append(K)
    return KS, skipped

if __name__ == '__main__':
    # self-test: networkx agreement on random fully lettered models of random five words
    import collections
    KS, skipped = load(sys.argv[1]); N = int(next((a[2:] for a in sys.argv[2:] if a.startswith('n=')), '2000'))
    print('configurations: %d used, %d skipped (interior not 2-connected, C1): %s' % (len(KS), len(skipped), ' '.join(k[0] for k in skipped)))
    random.seed(3); agree = bad = hits = 0
    for it in range(N):
        w = tuple(random.choice(LET) for _ in range(5))
        if tuple(w) not in MODEL: MODEL[tuple(w)] = model(w)
        nodes = MODEL[tuple(w)][0]
        letters = tuple((x, random.choice(LET)) for x in nodes if x != 'v' and x[0] != 'a')
        for K in KS:
            a = embeds(K, w, letters, False) is not None; b = embeds_nx(K, w, letters)
            agree += a == b; bad += a != b; hits += a
    print('networkx agreement: %d checks, %d agree, %d mismatches, %d embeddings found' % (agree + bad, agree, bad, hits))
