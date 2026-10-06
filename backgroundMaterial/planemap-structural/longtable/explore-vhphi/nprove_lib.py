"""nprove_lib.py  [N-Prove, exploratory, post hoc, not declared]
Own implementation (shares no code with Math's tn_lib/nlab): disc lines -> T = disc + x,
certificates for triangulation/min degree/4-connectivity, pair components, swaps,
Case I / Case II of c', c'' (definitions of MathNPinchT3 sec 5.2), D'-free class graph.
Colours 0,1,2,3 = D,alpha,beta,gamma; ring u0..u4 = vertices 0..4; x = vertex V."""
import sys
from collections import deque
from itertools import combinations
D, AL, BE, GA = 0, 1, 2, 3

def parse(line):
    line = line[line.index('DISC'):].strip()
    _, rest = line.split(' ', 1)
    sz, cols, es = rest.split(';')
    col = [int(t) for t in cols.split()]
    E = [tuple(map(int, t.split('-'))) for t in es.split()]
    return col, E

def build(col, E):
    V = len(col); x = V
    adj = [set() for _ in range(V + 1)]
    for u, v in E: adj[u].add(v); adj[v].add(u)
    for r in range(5): adj[x].add(r); adj[r].add(x)
    return x, adj

def certify(adj):
    """sphere triangulation (links are cycles, Euler), min degree, no separating triangle."""
    n = len(adj); m = sum(len(a) for a in adj) // 2
    ok_euler = (m == 3 * n - 6)
    ok_links = True
    for v in range(n):
        nb = adj[v]
        sub = {u: adj[u] & nb for u in nb}
        if any(len(s) != 2 for s in sub.values()): ok_links = False; break
        s0 = next(iter(nb)); seen = {s0}; st = [s0]
        while st:
            u = st.pop()
            for w in sub[u]:
                if w not in seen: seen.add(w); st.append(w)
        if seen != nb: ok_links = False; break
    tri = sum(1 for a, b, c in combinations(range(n), 3) if b in adj[a] and c in adj[a] and c in adj[b])
    return dict(n=n, euler=ok_euler, links=ok_links, mindeg=min(len(a) for a in adj),
                triangles=tri, faces=2 * n - 4, sep_triangles=tri - (2 * n - 4))

def comps(adj, c, pair, x):
    """components of the pair subgraph of T-x for colouring c (dict/list indexable by vertex)."""
    pair = set(pair); seen = {}; out = []
    for s in range(len(adj)):
        if s == x or c[s] not in pair or s in seen: continue
        comp = [s]; seen[s] = len(out); st = [s]
        while st:
            u = st.pop()
            for w in adj[u]:
                if w != x and w not in seen and c[w] in pair:
                    seen[w] = len(out); comp.append(w); st.append(w)
        out.append(comp)
    return out, seen

def swap(c, K, a, b):
    c2 = list(c)
    for w in K: c2[w] = b if c[w] == a else a
    return c2

def conn(adj, c, p, q, pair, x):
    cs, ix = comps(adj, c, pair, x); return ix[p] == ix[q]

def canon(c):
    m = {}; return tuple(m.setdefault(v, len(m)) for v in c)

def neighbours_cprime(adj, x, col):
    K2cs, ix = comps(adj, col, (D, GA), x); K2 = K2cs[ix[2]]
    K0cs, ix = comps(adj, col, (D, BE), x); K0 = K0cs[ix[0]]
    return swap(col, K2, D, GA), swap(col, K0, D, BE), K2, K0

def case_cprime(adj, x, c0):
    """Case of c' (apex u0).  Returns 'unlocked1' / 'I' / 'II' plus the colourings c1,c2,c3 used."""
    if conn(adj, c0, 4, 1, (AL, GA), x) or conn(adj, c0, 4, 2, (AL, GA), x): return 'unlocked1', None
    cs, ix = comps(adj, c0, (AL, GA), x); Q4 = cs[ix[4]]; c1 = swap(c0, Q4, AL, GA)
    cs, ix = comps(adj, c1, (AL, BE), x); E34 = cs[ix[3]]; c2 = swap(c1, E34, AL, BE)
    caseI = conn(adj, c2, 2, 4, (BE, GA), x)
    return ('I' if caseI else 'II'), (c1, c2)

def mirror_case(adj, x, c0):
    """c'' mirror: u0<->u2, u3<->u4, beta<->gamma."""
    if conn(adj, c0, 3, 1, (AL, BE), x) or conn(adj, c0, 3, 0, (AL, BE), x): return 'unlocked1', None
    cs, ix = comps(adj, c0, (AL, BE), x); Q3 = cs[ix[3]]; c1 = swap(c0, Q3, AL, BE)
    cs, ix = comps(adj, c1, (AL, GA), x); E43 = cs[ix[4]]; c2 = swap(c1, E43, AL, GA)
    caseI = conn(adj, c2, 0, 3, (BE, GA), x)
    return ('I' if caseI else 'II'), (c1, c2)

def chain_broken(adj, x, c, apex):
    """is some chain {c(apex),k} (k != c(apex)) broken, or the ring 3-coloured, in G = T - x apex, x coloured c(apex)?"""
    s = c[apex]; ring = list(range(5))
    if len({c[r] for r in ring}) < 4: return True
    for k in range(4):
        if k == s: continue
        cs, ix = comps(adj, c, (s, k), x)
        if not any(c[w] == k and ix[w] == ix[apex] for w in ring if w != apex): return True
    return False

def dfree_class(adj, x, c0, apex):
    """Kempe class of c0 under swaps of pair components of T-x with pairs avoiding c0[apex]; nodes = canonical colourings."""
    s = c0[apex]; free = [(a, b) for a in range(4) for b in range(a + 1, 4) if s not in (a, b)]
    key = lambda c: canon(c[:x])
    dist = {key(c0): 0}; rep = {key(c0): c0}; g = {}; q = deque([c0])
    while q:
        c = q.popleft(); k0 = key(c); g[k0] = set()
        for a, b in free:
            cs, _ = comps(adj, c, (a, b), x)
            for K in cs:
                c2 = swap(c, K, a, b); k = key(c2)
                if k == k0: continue
                g[k0].add(k)
                if k not in dist: dist[k] = dist[k0] + 1; rep[k] = c2; q.append(c2)
    return dist, rep, g
