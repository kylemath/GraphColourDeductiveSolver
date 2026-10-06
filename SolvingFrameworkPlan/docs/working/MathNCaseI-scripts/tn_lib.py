"""MathNDiscSearch / test_N.py  [exploratory, undeclared, post hoc]
Reads DISC lines from disc_gen, builds T = disc + x (x = vertex V adjacent to ring 0..4),
checks planar-triangulation counts, min degree 5, rigid structure, the three fans locked
(Kempe class in G = T - x y, x coloured c(y), does not separate), then tests statement (N):
nu_gamma c separable at u0, or nu_beta c separable at u2.
Usage: python3 test_N.py FILE [--budget CLASS_CAP]
Prints, per disc, a verdict line; a candidate counterexample line begins 'CAND'.
"""
import sys
from collections import deque
PAIRS = [(a, b) for a in range(4) for b in range(a + 1, 4)]

def parse(line):
    _, rest = line.split(' ', 1)
    sz, cols, es = rest.split(';')
    col = [int(t) for t in cols.split()]
    edges = [tuple(map(int, t.split('-'))) for t in es.split()]
    return col, edges

def build(col, edges):
    V = len(col); n = V + 1; x = V
    adj = [set() for _ in range(n)]
    for u, v in edges: adj[u].add(v); adj[v].add(u)
    for r in range(5): adj[x].add(r); adj[r].add(x)
    return n, x, adj

def comps(adj, col, S, skip):
    seen = {}; out = []
    for s in col:
        if s == skip or col[s] not in S or s in seen: continue
        comp = {s}; st = [s]
        while st:
            u = st.pop()
            for w in adj[u]:
                if w != skip and w in col and w not in comp and col[w] in S:
                    comp.add(w); st.append(w)
        for u in comp: seen[u] = len(out)
        out.append(comp)
    return out, seen

def kempe_class_separable(adj, n, x, y, col0, cap):
    """BFS over Kempe classes in G = T - xy with x coloured c(y); returns (separable, size, truncated)."""
    G = [set(a) for a in adj]; G[x].discard(y); G[y].discard(x)
    c0 = [col0[v] for v in range(n - 1)] + [col0[y]]
    def canon(c):
        m = {}
        return tuple(m.setdefault(v, len(m)) for v in c)
    start = tuple(c0)
    seen = {canon(start)}
    q = deque([start])
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
                    for w in G[u]:
                        if w not in comp and st[w] in (a, b): comp.add(w); stk.append(w)
                done |= comp
                nc = list(st)
                for w in comp: nc[w] = b if st[w] == a else a
                k = canon(nc)
                if k not in seen:
                    if len(seen) >= cap: return None, len(seen), True
                    seen.add(k); q.append(tuple(nc))
    return False, len(seen), False

def main():
    fn = sys.argv[1]; cap = 200000
    stats = dict(discs=0, rigid_ok=0, locked3=0, Nholds=0, CAND=0, trunc=0)
    for line in open(fn):
        if not line.startswith('DISC'): continue
        col_l, edges = parse(line); stats['discs'] += 1
        n, x, adj = build(col_l, edges); V = n - 1
        if len(edges) + 5 != 3 * n - 6 - 5 + 0 and len(edges) + 5 != 3 * (V) - 3 - 0 + 0: pass
        if sum(len(a) for a in adj) // 2 != 3 * n - 6: continue
        if any(len(a) < 5 for a in adj): continue
        col = {v: col_l[v] for v in range(V)}
        ring = list(range(5)); u = ring
        D, al, be, ga = 0, 1, 2, 3
        # rigid structure (re-verify)
        vec = []
        okf = True
        for a, b in [(D, al), (D, be), (D, ga), (al, be), (al, ga), (be, ga)]:
            cs, _ = comps(adj, col, {a, b}, x)
            Vp = sum(1 for v in col if col[v] in (a, b))
            Ep = sum(1 for p in col for w in adj[p] if w in col and p < w and col[p] in (a, b) and col[w] in (a, b))
            if Ep != Vp - len(cs): okf = False
            vec.append(len(cs))
        if not okf or vec != [1, 2, 2, 1, 1, 1]: continue
        stats['rigid_ok'] += 1
        res = []
        for j in (1, 3, 4):
            sep, sz, tr = kempe_class_separable(adj, n, x, u[j], col, cap)
            res.append((sep, sz, tr))
        if any(r[0] is not False for r in res):
            if any(r[2] for r in res): stats['trunc'] += 1
            continue
        stats['locked3'] += 1
        csg, idg = comps(adj, col, {D, ga}, x); K2 = csg[idg[u[2]]]
        csb, idb = comps(adj, col, {D, be}, x); K0 = csb[idb[u[0]]]
        def swap(K, a, b):
            c2 = dict(col)
            for w in K: c2[w] = b if col[w] == a else a
            return c2
        sA = kempe_class_separable(adj, n, x, u[0], swap(K2, D, ga), cap)
        sB = kempe_class_separable(adj, n, x, u[2], swap(K0, D, be), cap)
        tag = 'N-holds' if (sA[0] is True or sB[0] is True) else ('N-UNDECIDED(trunc)' if (sA[2] or sB[2]) else 'CAND')
        if tag == 'N-holds': stats['Nholds'] += 1
        elif tag == 'CAND': stats['CAND'] += 1
        else: stats['trunc'] += 1
        sizes = tuple(sum(1 for v in col if col[v] == k) for k in range(4))
        print(f"{tag} n={n} sizes(D,a,b,g)={sizes} nu_gamma@u0 sep={sA[0]} class={sA[1]}; nu_beta@u2 sep={sB[0]} class={sB[1]} | {line.strip()}")
    print('[computed, exploratory, post hoc] summary', stats)
