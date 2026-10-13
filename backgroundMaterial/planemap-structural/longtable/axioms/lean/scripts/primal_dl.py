import json, itertools, random, sys
_src = open('flipsearch.py').read(); exec(_src[:_src.index('rng = random.Random')])
def analyse(F, h):
    D = darts_of(F); nxt = {}
    for (a, b, c) in F: nxt[(b, a)] = c; nxt[(c, b)] = a; nxt[(a, c)] = b
    V = sorted({x for f in F for x in f}); adj = {x: set() for x in V}
    for (u, w) in D: adj[u].add(w)
    if len(adj[h]) != 5: return None
    # link in rotation order: x0 = min nbr, x_{i+1} = nxt[(h, x_i)]
    x = [min(adj[h])]
    while len(x) < 5: x.append(nxt[(h, x[-1])])
    others = [v for v in V if v != h]
    out = []
    def comp(c, a, b, s):
        if c[s] not in (a, b): return set()
        seen = {s}; st = [s]
        while st:
            u = st.pop()
            for w in adj[u]:
                if w != h and w not in seen and c[w] in (a, b): seen.add(w); st.append(w)
        return seen
    for cols in itertools.product(range(4), repeat=len(others)):
        c = dict(zip(others, cols))
        if any(c[u] == c[w] for u in others for w in adj[u] if w != h): continue
        if c[others[0]] != 0: continue
        for j in range(5):
            X = lambda i: x[(j + i) % 5]
            al, mu, A, B = c[X(0)], c[X(1)], c[X(3)], c[X(4)]
            if c[X(2)] != al or len({al, mu, A, B}) != 4: continue
            lock1 = X(3) in comp(c, mu, A, X(1)); lock2 = X(4) in comp(c, mu, B, X(1))
            if not (lock1 and lock2): continue
            K = comp(c, al, A, X(2)); Kp = comp(c, al, A, X(0)); L = comp(c, mu, B, X(1))
            three = all((u in K or u in Kp) if c[u] in (al, A) else (u in L) for u in others)
            out.append({'c': c, 'j': j, 'three': three})
    return {'x': x, 'states': out}
w = json.load(open('witness.json'))
r = analyse([tuple(f) for f in w['primal']], w['h'])
print('witness T: DL states', len(r['states']), 'three', sum(s['three'] for s in r['states']))
rng = random.Random(3)
for n0 in (8, 9, 10):
    for trial in range(300):
        F = octa_like(n0)
        for _ in range(rng.randint(0, 25)): F = flip(F, rng)
        D = darts_of(F); deg = {}
        for (a, b) in D: deg[a] = deg.get(a, 0) + 1
        for h in [v for v in deg if deg[v] == 5]:
            r = analyse(F, h)
            if r and any(s['three'] for s in r['states']):
                s = next(s for s in r['states'] if s['three'])
                print('found n0', n0, 'h', h, 'x', r['x'], 'j', s['j'], 'c', s['c'])
                json.dump({'faces': [list(f) for f in F], 'h': h, 'x': r['x'], 'j': s['j'],
                           'c': {str(k): v for k, v in s['c'].items()}}, open('primal_witness.json', 'w'))
                sys.exit(0)
print('none')
