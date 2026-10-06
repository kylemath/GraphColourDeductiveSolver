"""N-Counter library [exploratory, undeclared, post hoc]. Own code; shares nothing with Math's test_N.py / nlab.py.
Colours: D=0, alpha=1, beta=2, gamma=3 (as in MathNDiscSearch discs). Ring u0..u4 = vertices ring[0..4], clockwise.
A state is (adj, col) with col a dict over all vertices of T except x.
"""
from collections import deque
D, A, B, G = 0, 1, 2, 3
PAIRS = [(a, b) for a in range(4) for b in range(a + 1, 4)]

def parse_disc(line):
    _, rest = line.split(' ', 1)
    sz, cols, es = rest.split(';')
    col = [int(t) for t in cols.split()]
    edges = [tuple(map(int, t.split('-'))) for t in es.split()]
    V = len(col); x = V
    adj = [set() for _ in range(V + 1)]
    for u, v in edges: adj[u].add(v); adj[v].add(u)
    for r in range(5): adj[x].add(r); adj[r].add(x)
    return adj, {v: col[v] for v in range(V)}, x, list(range(5))

def comp_of(adj, col, s, S, skip):
    """component of s in the subgraph induced by colours in S (x skipped)."""
    comp = {s}; st = [s]
    while st:
        u = st.pop()
        for w in adj[u]:
            if w != skip and w not in comp and col[w] in S:
                comp.add(w); st.append(w)
    return comp

def all_comps(adj, col, S, skip):
    seen = set(); out = []
    for s in col:
        if s in seen or col[s] not in S: continue
        c = comp_of(adj, col, s, S, skip); seen |= c; out.append(c)
    return out

def swapK(col, K, a, b):
    c2 = dict(col)
    for w in K: c2[w] = b if col[w] == a else a
    return c2

def proper(adj, col):
    return all(col[u] != col[v] for u in col for v in adj[u] if v in col)

def pair_vector(adj, col, x):
    """(comps, cyc) for the six pairs in order D-a, D-b, D-g, a-b, a-g, b-g."""
    out = []
    for a, b in [(D, A), (D, B), (D, G), (A, B), (A, G), (B, G)]:
        V = [v for v in col if col[v] in (a, b)]
        E = sum(1 for u in V for w in adj[u] if w in col and u < w and col[w] in (a, b))
        c = len(all_comps(adj, col, {a, b}, x))
        out.append((c, E - len(V) + c))
    return out

def is_rigid(adj, col, x):
    pv = pair_vector(adj, col, x)
    return [p[0] for p in pv] == [1, 2, 2, 1, 1, 1] and all(p[1] == 0 for p in pv)

def kempe_class(adj, col, x, y, cap=20000):
    """BFS over canonical colourings of G = T - xy with x coloured c(y).
    Returns (separable?, size, truncated?).  separable = a class member has c(x) != c(y)."""
    n = len(adj)
    G_ = [set(a) for a in adj]; G_[x].discard(y); G_[y].discard(x)
    st0 = [0] * n
    for v in range(n):
        st0[v] = col[v] if v != x else col[y]
    def canon(c):
        m = {}
        return tuple(m.setdefault(v, len(m)) for v in c)
    start = tuple(st0); seen = {canon(start)}; q = deque([start])
    while q:
        st = q.popleft()
        if st[x] != st[y]: return True, len(seen), False
        for a, b in PAIRS:
            done = set()
            for s in range(n):
                if st[s] not in (a, b) or s in done: continue
                comp = {s}; stk = [s]
                while stk:
                    u = stk.pop()
                    for w in G_[u]:
                        if w not in comp and st[w] in (a, b): comp.add(w); stk.append(w)
                done |= comp
                nc = list(st)
                for w in comp: nc[w] = b if st[w] == a else a
                k = canon(nc)
                if k not in seen:
                    if len(seen) >= cap: return None, len(seen), True
                    seen.add(k); q.append(tuple(nc))
    return False, len(seen), False

def fan_locks(adj, col, x, ring, cap=20000):
    """lock status at the three fans u1,u3,u4: list of (sep,size,trunc)."""
    return [kempe_class(adj, col, x, ring[j], cap) for j in (1, 3, 4)]

def classify_prime(adj, col, x, ring, D_=D, a=A, b=B, g=G):
    """Case classification of c' = swap of K2 (component of u2 in [D,g]) at apex u0, following MathNPinchT3 5.2,
    but re-implemented here.  Returns (tag, info).  tags:
      'FO'  : first-order unlocked (u0 !~ u3 in [b,D'])   [separable by one G swap]
      'S1'  : after swap Q4, c1 has u0 !~ u2 in [D,g]      [separable after one more swap]
      'II'  : explicit 3 swaps, ring becomes 3-coloured     (separable)
      'I'   : u2 ~ u4 in [b,g]_2
    info['ok'] records internal consistency checks (properness, ring-colour counts)."""
    u0, u1, u2, u3, u4 = ring
    info = {}
    K2 = comp_of(adj, col, u2, {D_, g}, x)
    c = swapK(col, K2, D_, g)
    assert proper(adj, c)
    info['K2'] = len(K2)
    # ring word of c' : D a g b g
    assert [c[r] for r in ring] == [D_, a, g, b, g], [c[r] for r in ring]
    # H1: u0 ~ u3 in [b,D]
    if u3 not in comp_of(adj, c, u0, {b, D_}, x): return 'FO', info
    Q4 = comp_of(adj, c, u4, {a, g}, x)
    info['Q4'] = len(Q4)
    if u1 in Q4 or u2 in Q4: return 'FO2', info   # criterion Cor 1 (should coincide with 'FO')
    c1 = swapK(c, Q4, a, g)
    assert proper(adj, c1)
    if u2 not in comp_of(adj, c1, u0, {D_, g}, x): return 'S1', info
    E34 = comp_of(adj, c1, u3, {a, b}, x)
    info['E34'] = len(E34)
    if u1 in E34: return 'S1b', info
    c2 = swapK(c1, E34, a, b)
    assert proper(adj, c2)
    info['ringword2'] = [c2[r] for r in ring]
    R = comp_of(adj, c2, u4, {b, g}, x)
    if u2 in R:
        info['m_Da_2'] = 2 if (u3 not in comp_of(adj, c2, u0, {D_, a}, x) and u1 not in comp_of(adj, c2, u3, {D_, a}, x)) else 'other'
        # continue with Math's Case I step c3 = swap R: record whether chain {D,b} breaks
        c3 = swapK(c2, R, b, g)
        info['c3_broken_Db'] = (u0 not in comp_of(adj, c3, u2, {D_, b}, x))
        info['R'] = len(R)
        return 'I', info
    c3 = swapK(c2, R, b, g)
    assert proper(adj, c3)
    ringcols = {c3[r] for r in ring}
    info['ringcols3'] = len(ringcols)
    assert len(ringcols) == 3
    return 'II', info

def mirror_args(ring):
    u0, u1, u2, u3, u4 = ring
    return [u2, u1, u0, u4, u3]

def classify_both(adj, col, x, ring):
    """(Case of c' , Case of c'') with c'' computed through the mirror u0<->u2, u3<->u4, beta<->gamma."""
    t1 = classify_prime(adj, col, x, ring)
    # mirror: relabel colours b<->g in a copy
    sw = {D: D, A: A, B: G, G: B}
    colm = {v: sw[c] for v, c in col.items()}
    t2 = classify_prime(adj, colm, x, mirror_args(ring))
    return t1, t2
