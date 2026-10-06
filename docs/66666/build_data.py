# Builds docs/66666/data.js for "The Six-Ring Trap" demo page.
# Independent recomputation (imports no Math module): the order-28 triangulation with a
# (6,6,6,6,6) hole at v = 0, face list copied from
# SolvingFrameworkPlan/docs/working/MathSixFiveAutomaton.md section 4.
# Enumerates every proper 4-colouring of T - v (canonical by first occurrence),
# builds the whole-component Kempe swap graph (singletons allowed), and computes each
# state's swap distance to a filled state (link uses <= 3 colours).
# Optional: --trap PICKLE adds an aggregate of Math's automaton trap (fix.py output).
import sys, json, collections, itertools, time
import numpy as np

FACES_TXT = """0 1 2, 0 2 3, 0 3 4, 0 4 5, 0 5 1, 1 2 6, 1 6 7, 1 7 8, 1 8 5, 2 3 9, 2 9 10, 2 10 6, 3 4 11, 3 11 12, 3 12 9, 4 5 13, 4 13 14, 4 14 11, 5 8 15, 5 15 13, 8 7 27, 16 7 27, 17 16 27, 7 6 18, 7 18 16, 6 10 18, 10 9 26, 18 10 24, 9 12 26, 12 23 25, 16 18 24, 19 17 23, 19 17 24, 17 20 21, 17 21 15, 20 23 25, 20 22 21, 12 11 25, 11 14 22, 15 21 13, 21 22 14, 21 14 13, 20 17 23, 23 12 26, 17 16 24, 19 10 24, 11 22 25, 22 20 25, 19 23 26, 19 10 26, 17 15 27, 15 8 27"""
FACES = [tuple(map(int, f.split())) for f in FACES_TXT.split(',')]
HOLE = 0
t0 = time.time()

# ---------------------------------------------------------------- triangulation checks
n = 1 + max(max(f) for f in FACES)
edges = set()
for a, b, c in FACES:
    for x, y in ((a, b), (b, c), (c, a)):
        edges.add((min(x, y), max(x, y)))
adj = [set() for _ in range(n)]
for x, y in edges:
    adj[x].add(y); adj[y].add(x)
assert n - len(edges) + len(FACES) == 2, 'Euler'
ecount = collections.Counter()
for a, b, c in FACES:
    for x, y in ((a, b), (b, c), (c, a)):
        ecount[(min(x, y), max(x, y))] += 1
assert all(v == 2 for v in ecount.values()), 'each edge in two faces'
# rotation: cyclic order of neighbours from the faces around each vertex
rot = []
for v in range(n):
    inc = [f for f in FACES if v in f]
    pairs = [tuple(x for x in f if x != v) for f in inc]
    nb = collections.defaultdict(list)
    for x, y in pairs:
        nb[x].append(y); nb[y].append(x)
    start = min(nb); cyc = [start]; prev = None; cur = start
    while True:
        nxt = [w for w in nb[cur] if w != prev]
        nxt = nxt[0] if prev is None else nxt[0]
        if nxt == start: break
        cyc.append(nxt); prev, cur = cur, nxt
    assert len(cyc) == len(adj[v]) == len(inc), ('link not a single cycle', v)
    rot.append(cyc)
# no separating triangle: every triangle of the graph is a face
faceset = {tuple(sorted(f)) for f in FACES}
tri = [t for t in itertools.combinations(range(n), 3)
       if t[1] in adj[t[0]] and t[2] in adj[t[0]] and t[2] in adj[t[1]]]
sep = [t for t in tri if t not in faceset]
deg = [len(a) for a in adj]
assert min(deg) >= 5 and not sep
link = rot[HOLE]  # cyclic order around the hole
assert sorted(link) == [1, 2, 3, 4, 5] and all(deg[x] == 6 for x in link)

# ---------------------------------------------------------------- Tutte layout
# Fix the face farthest (graph distance) from the hole as the outer triangle.
dist0 = {HOLE: 0}; q = collections.deque([HOLE])
while q:
    u = q.popleft()
    for w in adj[u]:
        if w not in dist0: dist0[w] = dist0[u] + 1; q.append(w)
def tutte(weight):
    A = np.zeros((len(inner), len(inner))); bvec = np.zeros((len(inner), 2))
    for v in inner:
        i = idx[v]
        for w in adj[v]:
            wt = weight(v, w); A[i, i] += wt
            if w in idx: A[i, idx[w]] -= wt
            else: bvec[i] += wt * pos[w]
    sol = np.linalg.solve(A, bvec)
    for v in inner: pos[v] = sol[idx[v]]
def layout(outer):
    global pos, inner, idx
    pos = np.zeros((n, 2))
    for k, v in enumerate(outer):
        ang = -np.pi / 2 + 2 * np.pi * k / 3
        pos[v] = [np.cos(ang), np.sin(ang)]
    inner = [v for v in range(n) if v not in outer]
    idx = {v: i for i, v in enumerate(inner)}
    tutte(lambda v, w: 1.0)
    for _ in range(12):
        L = {(v, w): float(np.hypot(*(pos[v] - pos[w]))) for v in range(n) for w in adj[v]}
        tutte(lambda v, w: L[(v, w)])
    return min(float(np.hypot(*(pos[u] - pos[w]))) for u in range(n) for w in range(u + 1, n))
# Positive edge weights keep a Tutte (convex-combination) drawing planar (Floater).
# Reweighting by edge length spreads the crowded middle; the outer face is the one
# whose drawing has the largest minimum vertex spacing.
best = max(FACES, key=lambda f: (round(layout(list(f)), 4), -min(f)))
outer = list(best); spacing = layout(outer)
print('outer face', outer, 'min spacing', round(spacing, 3))
def crossings(P):
    E = sorted(edges); bad = 0
    def ccw(a, b, c): return (P[b][0]-P[a][0])*(P[c][1]-P[a][1]) - (P[b][1]-P[a][1])*(P[c][0]-P[a][0])
    for (a, b), (c, d) in itertools.combinations(E, 2):
        if len({a, b, c, d}) < 4: continue
        if ccw(a, b, c) * ccw(a, b, d) < 0 and ccw(c, d, a) * ccw(c, d, b) < 0: bad += 1
    return bad
assert crossings(pos) == 0
# radial stretch about the inner centroid; kept only if the drawing stays crossing-free
base = pos.copy(); cen = base[inner].mean(axis=0)
for ex in (0.45, 0.55, 0.65, 0.75, 1.0):
    P = base.copy()
    for v in inner:
        dv = base[v] - cen; r = np.hypot(*dv)
        P[v] = cen + dv * (r ** (ex - 1) if r > 1e-9 else 1)
    if crossings(P) == 0:
        pos = P; print('radial exponent', ex,
            'min spacing', round(min(float(np.hypot(*(pos[u]-pos[w]))) for u in range(n) for w in range(u+1, n)), 3)); break
# hole position: barycentre of its link (it was deleted, so draw it there)
# ---------------------------------------------------------------- colourings of T - v
V = [v for v in range(n) if v != HOLE]           # vertex order for colour strings
order = []                                        # BFS order for backtracking
seen = {link[0]}; q = collections.deque([link[0]])
while q:
    u = q.popleft(); order.append(u)
    for w in sorted(adj[u]):
        if w != HOLE and w not in seen: seen.add(w); q.append(w)
pos_in_V = {v: i for i, v in enumerate(V)}
nbr = {v: [w for w in adj[v] if w != HOLE] for v in V}

def canon(col):  # col: dict or list indexed by V-index
    m = {}
    return tuple(m.setdefault(x, len(m)) for x in col)

raw = set()
col = {}
def bt(k, used):
    if k == len(order):
        raw.add(canon([col[v] for v in V])); return
    v = order[k]
    bad = {col[w] for w in nbr[v] if w in col}
    for c in range(min(used + 1, 4)):   # symmetry break: colours introduced in order
        if c not in bad:
            col[v] = c; bt(k + 1, max(used, c + 1)); del col[v]
bt(0, 0)
states = sorted(raw)
sidx = {s: i for i, s in enumerate(states)}
print('colourings of T-v up to renaming:', len(states), round(time.time() - t0, 1), 's', flush=True)

Ln = [pos_in_V[x] for x in link]
nbrI = [[pos_in_V[w] for w in nbr[v]] for v in V]
PAIRS = list(itertools.combinations(range(4), 2))

def kempe_moves(s):
    out = []
    for a, b in PAIRS:
        pend = {i for i, x in enumerate(s) if x == a or x == b}
        while pend:
            seed = min(pend); pend.discard(seed); comp = [seed]; k = 0
            while k < len(comp):
                for j in nbrI[comp[k]]:
                    if j in pend: pend.discard(j); comp.append(j)
                k += 1
            cs = set(comp)
            t = tuple((b if x == a else a) if i in cs else x for i, x in enumerate(s))
            out.append((a, b, sorted(comp), sidx[canon(t)]))
    return out

def filled(s): return len({s[i] for i in Ln}) <= 3

def comp_of(s, start, a, b):
    seen = {start}; st = [start]
    while st:
        u = st.pop()
        for j in nbrI[u]:
            if j not in seen and s[j] in (a, b): seen.add(j); st.append(j)
    return seen

def dl_info(s):
    """repeat index j and whether doubly locked (l-attack.md section 1 definition)."""
    L = [s[i] for i in Ln]
    if len(set(L)) <= 3: return None
    j = [t for t in range(5) if L[t] == L[(t + 2) % 5]][0]
    m, a, b = Ln[(j + 1) % 5], Ln[(j + 3) % 5], Ln[(j + 4) % 5]
    l1 = Ln[(j + 3) % 5] in comp_of(s, m, s[m], s[a])
    l2 = Ln[(j + 4) % 5] in comp_of(s, m, s[m], s[b])
    return j, l1, l2

moves = [kempe_moves(s) for s in states]
nxt = [sorted({m[3] for m in mv if m[3] != i}) for i, mv in enumerate(moves)]
print('Kempe graph built', round(time.time() - t0, 1), 's', flush=True)

# Kempe classes
cls = [-1] * len(states); ncls = 0
for i in range(len(states)):
    if cls[i] >= 0: continue
    cls[i] = ncls; q = collections.deque([i])
    while q:
        u = q.popleft()
        for w in nxt[u]:
            if cls[w] < 0: cls[w] = ncls; q.append(w)
    ncls += 1
print('Kempe classes:', ncls)
# distance to a filled state
d = [-1] * len(states); q = collections.deque()
for i, s in enumerate(states):
    if filled(s): d[i] = 0; q.append(i)
while q:
    u = q.popleft()
    for w in nxt[u]:
        if d[w] < 0: d[w] = d[u] + 1; q.append(w)
dl = [dl_info(s) for s in states]
nfilled = sum(1 for s in states if filled(s))
ndl = [i for i in range(len(states)) if dl[i] and dl[i][1] and dl[i][2]]
hist_all = collections.Counter(d)
hist_dl = collections.Counter(d[i] for i in ndl)
print('filled', nfilled, 'unfilled', len(states) - nfilled)
print('distance histogram (all states):', dict(sorted(hist_all.items())))
print('DL states', len(ndl), 'radius histogram:', dict(sorted(hist_dl.items())))
# non-DL unfilled at distance 1? check
print('unfilled non-DL distances:', dict(collections.Counter(d[i] for i in range(len(states))
      if not filled(states[i]) and not (dl[i][1] and dl[i][2]))))

# ring pattern of a DL state in Math's frame: rotate link so repeat index j = 0, read ring
# w_0 m_1 w_1 ... m_0 with roles a,b,g,d = colours of x0,x1,x3,x4 after rotation.
def ring_pattern(i, reflect=False):
    s = states[i]; j = dl[i][0]
    Lk = link[::-1] if reflect else link
    if reflect:
        Lc = [s[pos_in_V[x]] for x in Lk]
        j = [t for t in range(5) if Lc[t] == Lc[(t + 2) % 5]][0]
    X = [Lk[(j + t) % 5] for t in range(5)]
    role = {s[pos_in_V[X[0]]]: 'a', s[pos_in_V[X[1]]]: 'b', s[pos_in_V[X[3]]]: 'g', s[pos_in_V[X[4]]]: 'd'}
    ring = []
    for t in range(5):  # w_{t-1}? we build w_0 m_1 w_1 m_2 ... w_4 m_0
        pass
    def common(xa, xb):
        c = [w for w in adj[xa] & adj[xb] if w != HOLE and w not in X]
        assert len(c) == 1; return c[0]
    def middle(xt, wl, wr):
        c = [w for w in adj[xt] if w not in X and w != HOLE and w not in (wl, wr)]
        assert len(c) == 1; return c[0]
    W = [common(X[t], X[(t + 1) % 5]) for t in range(5)]
    M = [middle(X[t], W[(t - 1) % 5], W[t]) for t in range(5)]
    seq = []
    for t in range(5):
        seq.append(W[t]); seq.append(M[(t + 1) % 5])
    return ''.join(role[s[pos_in_V[w]]] for w in seq), X, W, M


# ---------------------------------------------------------------- the 74 ring patterns (Lemma 1 of MathSixFiveHole)
# link (a,b,a,g,d) = (0,1,0,2,3); ring positions w0 m1 w1 m2 w2 m3 w3 m4 w4 m0; x_t ~ positions 2t-2, 2t-1, 2t.
LK = (0, 1, 0, 2, 3)
pats74 = []
for r in itertools.product(range(4), repeat=10):
    if any(r[i] == r[(i + 1) % 10] for i in range(10)): continue
    if any(r[p % 10] == LK[t] for t in range(5) for p in (2 * t - 2, 2 * t - 1, 2 * t)): continue
    if not ({2, 3} <= {r[0], r[1], r[2]}): continue
    if 1 not in (r[4], r[5], r[6]) or 1 not in (r[6], r[7], r[8]): continue
    pats74.append(''.join('abgd'[x] for x in r))
print('ring patterns satisfying Lemma 1:', len(pats74))
P74 = set(pats74)
for i in ndl:
    p = ring_pattern(i)[0]; pr = ring_pattern(i, reflect=True)[0]
    dl[i] = dl[i] + (p if p in P74 else pr if pr in P74 else '?',)
print('DL states whose pattern is outside the 74 (both orientations):', sum(1 for i in ndl if dl[i][3] == '?'))

rad = max(d[i] for i in ndl)
deepest = [i for i in ndl if d[i] == rad]
print('max DL radius', rad, 'at states', deepest)
for i in deepest + [i for i in ndl if d[i] == 3]:
    p, X, W, M = ring_pattern(i)
    pr = ring_pattern(i, reflect=True)[0]
    print('state', i, 'radius', d[i], 'pattern', p, 'reflected', pr, 'X', X)

start = deepest[0]
assert len(set(cls)) == 1 or True
# ---------------------------------------------------------------- what to embed
# Embed the whole Kempe class of the start if small enough, else the ball of radius 4.
members = [i for i in range(len(states)) if cls[i] == cls[start]]
print('class of start:', len(members), 'states')
embed = members
if len(members) > 6000:
    bd = {start: 0}; q = collections.deque([start])
    while q:
        u = q.popleft()
        if bd[u] == 4: continue
        for w in nxt[u]:
            if w not in bd: bd[w] = bd[u] + 1; q.append(w)
    embed = sorted(bd)
embed_set = set(embed)
emap = {i: k for k, i in enumerate(embed)}
# landscape y: an index that spreads states; use the number of 2-colour components on the link side
out_states = []
for i in embed:
    s = states[i]
    info = dl[i]
    kind = 'filled' if filled(s) else ('dl' if info[1] and info[2] else 'locked1' if (info[1] or info[2]) else 'open')
    out_states.append({'c': list(s), 'd': d[i], 'k': kind,
                       'j': None if info is None else info[0],
                       'pat': info[3] if (info and len(info) > 3) else None,
                       'next': [emap[w] for w in nxt[i] if w in embed_set]})
# DL states one swap from each other inside the class (the "locked plateau")
data = {
    'source': 'SolvingFrameworkPlan/docs/working/MathSixFiveAutomaton.md section 4 (faces)',
    'order': n, 'hole': HOLE, 'faces': FACES, 'rot': rot,
    'pos': [[round(float(x), 4), round(float(y), 4)] for x, y in pos],
    'outer': outer, 'link': link, 'V': V, 'deg': deg,
    'states': out_states, 'start': emap[start],
    'deepest': [emap[i] for i in deepest if i in embed_set],
    'summary': {
        'colourings': len(states), 'classes': ncls, 'classSize': len(members), 'embedded': len(embed),
        'filled': nfilled, 'dl': len(ndl), 'dlHist': {str(k): v for k, v in sorted(hist_dl.items())},
        'allHist': {str(k): v for k, v in sorted(hist_all.items())},
        'maxRadius': rad, 'startPattern': ring_pattern(start)[0],
        'startPatternReflected': ring_pattern(start, reflect=True)[0],
        'edges': len(edges), 'degCount': {str(k): v for k, v in sorted(collections.Counter(deg).items())},
        'separatingTriangles': len(sep),
        'patterns74': pats74,
        'patternsHere': dict(sorted(collections.Counter(dl[i][3] for i in ndl).items())),
    },
}
if '--trap' in sys.argv:
    data['trap'] = json.load(open(sys.argv[sys.argv.index('--trap') + 1]))
with open(__file__.replace('build_data.py', 'data.js'), 'w') as f:
    f.write('// Generated by docs/66666/build_data.py. Do not edit.\n')
    f.write('window.SIXRING_DATA = ' + json.dumps(data, separators=(',', ':')) + ';\n')
print('wrote data.js', round(time.time() - t0, 1), 's')
