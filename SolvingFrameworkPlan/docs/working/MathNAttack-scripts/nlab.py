"""Math-team scratch (MathNAttack). Exploratory, undeclared, orders 17 only (graphs 17:0, 17:1).
Self-contained: parses plantri -m5 17 -a output, enumerates proper 4-colourings of T-x with
4-coloured ring, detects rigid triply locked states (six forests, comps (1,2,2,1,1,1)), builds
nu_gamma c and nu_beta c, tests lock criteria.
Usage: python3 nlab.py PLANTRI
"""
import sys, subprocess, itertools
from collections import deque

PAIRS = list(itertools.combinations(range(4), 2))

def parse(line):
    _, body = line.split()
    return [[ord(ch) - 97 for ch in r] for r in body.split(",")]

def colourings_minus(adj, n, x):
    verts = [v for v in range(n) if v != x]
    # order: BFS from ring for pruning
    order = []
    seen = set()
    q = deque([adj[x] and sorted(adj[x])[0]])
    seen.add(q[0])
    while q:
        v = q.popleft(); order.append(v)
        for w in sorted(adj[v]):
            if w != x and w not in seen:
                seen.add(w); q.append(w)
    assert len(order) == n - 1
    col = {}
    out = []
    def go(i, top):
        if i == len(order):
            out.append(dict(col)); return
        v = order[i]
        blocked = {col[w] for w in adj[v] if w in col}
        for a in range(min(3, top + 1) + 1):
            if a not in blocked:
                col[v] = a
                go(i + 1, max(top, a))
                del col[v]
    go(0, -1)
    return out

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

def pair_info(adj, col, x):
    info = {}
    for a, b in PAIRS:
        cs, idx = comps(adj, col, {a, b}, x)
        V = [w for w in col if col[w] in (a, b)]
        e = sum(1 for u in V for w in adj[u] if w > u and w in col and col[w] in (a, b))
        info[(a, b)] = (len(cs), e - len(V) + len(cs))
    return info

def path_in(adj, col, S, s, t, skip):
    """unique/any path s->t in subgraph [S] avoiding skip (BFS); returns list or None"""
    prev = {s: None}; q = deque([s])
    while q:
        u = q.popleft()
        if u == t:
            p = []
            while u is not None: p.append(u); u = prev[u]
            return p[::-1]
        for w in adj[u]:
            if w != skip and w in col and w not in prev and col[w] in S:
                prev[w] = u; q.append(w)
    return None

def swap_comp(col, K, a, b):
    c2 = dict(col)
    for w in K: c2[w] = b if col[w] == a else a
    return c2

def classify(adj, x, ring, col):
    """return roles if ring word is D a D b g pattern: u[0..4], colours"""
    word = [col[w] for w in ring]
    if len(set(word)) != 4: return None
    D = [k for k in set(word) if word.count(k) == 2][0]
    pD = [i for i in range(5) if word[i] == D]
    p = pD[0] if (pD[1] - pD[0]) % 5 == 2 else pD[1]
    u = [ring[(p + i) % 5] for i in range(5)]
    return u, (col[u[0]], col[u[1]], col[u[3]], col[u[4]])

def class_in_G(adj, n, x, y, col):
    """Kempe class (whole components) in G=T-xy, x coloured c(y). col covers T-x; returns (separable?, class size, set)"""
    G = [set(a) for a in adj]; G[x].discard(y); G[y].discard(x)
    c0 = dict(col); c0[x] = col[y]
    def canon(c):
        m = {}
        return tuple(m.setdefault(c[v], len(m)) for v in range(n))
    start = tuple(c0[v] for v in range(n))
    seen = {canon(c0): start}
    q = deque([start]); sep = False
    while q:
        st = q.popleft()
        if st[x] != st[y]: sep = True; break
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
                m = {}
                key = tuple(m.setdefault(v, len(m)) for v in nc)
                if key not in seen:
                    seen[key] = tuple(nc); q.append(tuple(nc))
    return sep, len(seen)

def main():
    P = sys.argv[1]
    for gi in (0, 1):
        line = subprocess.run([P, "-m5", "17", "-a"], capture_output=True, text=True).stdout.splitlines()[gi]
        rot = parse(line); n = len(rot); adj = [set(r) for r in rot]
        print(f"=== 17:{gi}")
        for x in range(n):
            if len(rot[x]) != 5: continue
            ring = rot[x]
            allc = colourings_minus(adj, n, x)
            for col in allc:
                cl = classify(adj, x, ring, col)
                if cl is None: continue
                u, (D, al, be, ga) = cl
                pi = pair_info(adj, col, x)
                key = lambda p, q: (min(p, q), max(p, q))
                vec = (pi[key(D, al)], pi[key(D, be)], pi[key(D, ga)], pi[key(al, be)], pi[key(al, ga)], pi[key(be, ga)])
                if vec != ((1, 0), (2, 0), (2, 0), (1, 0), (1, 0), (1, 0)): continue
                # rigid candidate (all forests, comps 1,2,2,1,1,1); legality of fans
                if any(u[j] in adj[u[(j + 2) % 5]] or u[j] in adj[u[(j + 3) % 5]] for j in range(5)): pass
                # K2 = [D,ga]-component of u2; K0 = [D,be]-comp of u0
                csg, idg = comps(adj, col, {D, ga}, x); K2 = csg[idg[u[2]]]
                csb, idb = comps(adj, col, {D, be}, x); K0 = csb[idb[u[0]]]
                P13 = path_in(adj, col, {al, be}, u[1], u[3], x)
                P14 = path_in(adj, col, {al, ga}, u[1], u[4], x)
                lockedc = [not class_in_G(adj,n,x,u[j],col)[0] for j in (1,3,4)]
                if not all(lockedc): continue
                cprime = swap_comp(col, K2, D, ga)   # nu_gamma
                cdouble = swap_comp(col, K0, D, be)  # nu_beta
                sepA, szA = class_in_G(adj, n, x, u[0], cprime)
                sepB, szB = class_in_G(adj, n, x, u[2], cdouble)
                P14g = [w for w in P14 if col[w] == ga]; P13b = [w for w in P13 if col[w] == be]
                hit2 = [w for w in P14g if w in K2]; hit0 = [w for w in P13b if w in K0]
                print(f" x={x} ring={u} cols D,a,b,g={D,al,be,ga} |K2|={len(K2)} |K0|={len(K0)} P13={P13} P14={P14}")
                print(f"    P14 gamma-vertices in K2: {hit2}; P13 beta-vertices in K0: {hit0}")
                print(f"    nu_gamma c separable at u0: {sepA} (class {szA}); nu_beta c separable at u2: {sepB} (class {szB})")

if __name__ == "__main__":
    main()
