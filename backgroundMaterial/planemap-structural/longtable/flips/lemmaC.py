"""lemmaC.py -- structural one-chord lemma inside the A' class (n small, Python).
H = C_n + T1 + D (D cap T1 = empty, D non-crossing outside chords, k=|D| < n-3).
Lemma C: some admissible outside chord e=uw (not in T1 u D, crossing no D chord) has
   t(u,w) = #common neighbours >= 2  AND  H/e in class 3 (2-connected, every 2-cut {x,y} adjacent).
If the class-3 bound P >= 24*2^miss holds on n-1 vertices, Lemma C gives Lemma W, hence A' for H
from A' for H+e (induction on missing edges; base = 4CT).
Usage: python3 lemmaC.py n"""
import sys, itertools, networkx as nx
n = int(sys.argv[1])
def tris(i, j):
    if j - i < 2: yield []; return
    for k in range(i + 1, j):
        for a in tris(i, k):
            for b in tris(k, j):
                yield a + b + ([(i, k)] if k - i >= 2 else []) + ([(k, j)] if j - k >= 2 else [])
def canon(T):
    best = None
    for r in range(n):
        for f in (0, 1):
            s = []
            for u, v in T:
                if f: u, v = (n - u) % n, (n - v) % n
                u, v = (u + r) % n, (v + r) % n
                s.append((min(u, v), max(u, v)))
            s = tuple(sorted(s)); best = s if best is None or s < best else best
    return best
T1s = sorted({canon(T) for T in tris(0, n - 1)})
chords = [(u, v) for u in range(n) for v in range(u + 2, n) if not (u == 0 and v == n - 1)]
def cross(e, f):
    a, b = e; c, d = f
    if len({a, b, c, d}) < 4: return False
    return (a < c < b) != (a < d < b)
def class3(G):
    if not nx.is_biconnected(G): return False
    for x, y in itertools.combinations(G.nodes(), 2):
        if G.has_edge(x, y): continue
        H = G.copy(); H.remove_nodes_from([x, y])
        if H.number_of_nodes() and not nx.is_connected(H): return False
    return True
tested = fails = 0; reasons = {}
for T in T1s:
    base = nx.cycle_graph(n); base.add_edges_from(T)
    out = [c for c in chords if c not in T]
    def rec(start, D):
        global tested, fails
        adm = [e for e in out if e not in D and not any(cross(e, d) for d in D)]
        if adm:
            H = base.copy(); H.add_edges_from(D)
            okC = False; why = []
            for (u, w) in adm:
                t = len(set(H[u]) & set(H[w]))
                if t < 2: why.append('t1'); continue
                Hc = nx.contracted_nodes(H, u, w, self_loops=False)
                if class3(Hc): okC = True; break
                why.append('cls')
            tested += 1
            if not okC:
                fails += 1
                key = 'all t=1' if all(x == 't1' for x in why) else 'some t>=2 but contraction leaves class 3'
                reasons[key] = reasons.get(key, 0) + 1
                if fails <= 3: print("CFAIL T1", T, "D", D, key)
        for i in range(start, len(out)):
            e = out[i]
            if any(cross(e, d) for d in D): continue
            rec(i + 1, D + [e])
    rec(0, [])
print(f"n={n} tested={tested} lemmaC_fails={fails} {reasons}")
