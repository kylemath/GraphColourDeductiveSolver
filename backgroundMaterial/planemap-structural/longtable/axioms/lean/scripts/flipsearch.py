import random, json, sys
sys.setrecursionlimit(10000)
def ico():
    F = []
    for i in range(5):
        a, b = 1 + i, 1 + (i + 1) % 5; c, d = 6 + i, 6 + (i + 1) % 5
        F += [(0, a, b), (a, c, b), (b, c, d), (11, d, c)]
    return F
def octa_like(n):  # double wheel (bipyramid) on n-2 ring vertices
    m = n - 2; F = []
    for i in range(m):
        a, b = 2 + i, 2 + (i + 1) % m
        F += [(0, a, b), (1, b, a)]
    return F
def darts_of(F):
    D = {}
    for i, (a, b, c) in enumerate(F):
        for u, v in ((a, b), (b, c), (c, a)): D[(u, v)] = i
    return D
def flip(F, rng):
    D = darts_of(F); (u, v) = rng.choice(list(D))
    i, j = D[(u, v)], D[(v, u)]
    a = [x for x in F[i] if x not in (u, v)][0]; b = [x for x in F[j] if x not in (u, v)][0]
    adj = {}
    for (x, y) in D: adj.setdefault(x, set()).add(y)
    if b in adj[a] or len(adj[u]) <= 3 or len(adj[v]) <= 3: return F
    # face i contains dart (u,v) -> oriented (u,v,a); face j (v,u,b)
    G = [f for k, f in enumerate(F) if k not in (i, j)]
    G += [(a, b, v), (b, a, u)]
    # fix orientation: new faces must use darts (a,b) and (b,a) consistently with others
    D2 = {}
    for k, (x, y, z) in enumerate(G):
        for p, q in ((x, y), (y, z), (z, x)):
            if (p, q) in D2: return F
            D2[(p, q)] = k
    if not all((q, p) in D2 for (p, q) in D2): return F
    return G
def analyse(F, h):
    D = darts_of(F); nxt = {}
    for (a, b, c) in F: nxt[(b, a)] = c; nxt[(c, b)] = a; nxt[(a, c)] = b
    V = sorted({x for f in F for x in f})
    P = 'P'
    dv = lambda fi: P if h in F[fi] else fi
    dfaces = []
    for u in V:
        if u == h: continue
        nb0 = next(y for (x, y) in D if x == u); seq = []; w = nb0
        while True:
            w2 = nxt[(u, w)]; seq.append(dv(D[(u, w2)])); w = w2
            if w == nb0: break
        out = []
        for x in seq:
            if out and out[-1] == x == P: continue
            out.append(x)
        if len(out) > 1 and out[0] == P and out[-1] == P: out.pop()
        dfaces.append(out)
    lab = {P: 0}
    for i in range(len(F)):
        if h not in F[i]: lab[i] = len(lab)
    dfaces = [[lab[x] for x in f] for f in dfaces]
    N = len(lab); dd = {}
    for fi, f in enumerate(dfaces):
        for i in range(len(f)):
            p, q = f[i], f[(i + 1) % len(f)]
            if (p, q) in dd or p == q: return None
            dd[(p, q)] = fi
    dn = {}
    for f in dfaces:
        m = len(f)
        for i in range(m): dn[(f[(i + 1) % m], f[i])] = f[(i + 2) % m]
    adj = {x: set() for x in range(N)}
    for (p, q) in dd: adj[p].add(q)
    if len(adj[0]) != 5 or any(len(adj[x]) != 3 for x in range(1, N)): return None
    fs = [min(adj[0])]
    while len(fs) < 5: fs.append(dn[(0, fs[-1])])
    res = []
    def rec(used, cur):
        free = [x for x in range(N) if x not in used]
        if not free: res.append(frozenset(cur)); return
        x = free[0]
        for y in adj[x]:
            if y not in used: rec(used | {x, y}, cur + [(min(x, y), max(x, y))])
    rec(frozenset(), [])
    def reach(src, M):
        seen = {src}; st = [src]
        while st:
            a = st.pop()
            for b in adj[a]:
                if b == 0 or (min(a, b), max(a, b)) in M: continue
                if b not in seen: seen.add(b); st.append(b)
        return seen
    out = []
    for M in res:
        k = next(i for i in range(5) if (0, fs[i]) in M)
        X = reach(fs[(k + 1) % 5], M); Y = reach(fs[(k + 2) % 5], M)
        if fs[(k - 1) % 5] in X and fs[(k + 3) % 5] in Y and fs[(k + 2) % 5] not in X \
                and all(u in X or u in Y for u in range(1, N)):
            cross = sum(1 for u in X if any((min(u, y), max(u, y)) in M for y in Y))
            out.append({'M': sorted(M), 'k': k, 'xeven': len(X) % 2 == 0, 'a5v': fs[k] in X, 'cross': cross})
    return {'N': N, 'faces': dfaces, 'fs': fs, 'states': out}
rng = random.Random(int(sys.argv[1]))
best = None
for n0 in (8, 9, 10, 11, 12):
    for trial in range(400):
        F = octa_like(n0) if n0 < 12 else ico()
        for _ in range(rng.randint(0, 30)): F = flip(F, rng)
        D = darts_of(F); deg = {}
        for (x, y) in D: deg[x] = deg.get(x, 0) + 1
        for h in [x for x in deg if deg[x] == 5]:
            r = analyse(F, h)
            if r is None: continue
            good = [s for s in r['states'] if s['xeven']]
            if good:
                print('found n0', n0, 'N', r['N'], 'states', len(r['states']), 'good', len(good),
                      [(s['k'], s['a5v'], s['cross']) for s in good][:4], file=sys.stderr)
                json.dump({'primal': F, 'h': h, **r}, open('witness.json', 'w'))
                sys.exit(0)
print('none', file=sys.stderr)
