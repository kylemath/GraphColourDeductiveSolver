# Builds docs/physics/data.js for "The Spin-Glass View".
# Independent recomputation (imports no project module). Inputs:
#   * the face list of the order-22 graph, read from docs/cages/data.js (which cages/build_data.py made from
#     origin/studio-intel:.../fcycle/fcycle_order22.json) -- the same graph and hole 15 as the cages page;
#   * the icosahedron, built here from its standard face list;
#   * backgroundMaterial/planemap-structural/longtable/studio-explore/sage-qa-runs/run5.txt (Studio compute run 5, exploratory).
# For each demo graph: re-verify the triangulation (Euler, every edge in two faces, vertex links single cycles,
# minimum degree 5, no separating triangle), draw it planar (Tutte + hill climb, asserts no crossing),
# enumerate every proper 4-colouring of T - hole up to renaming, group them into Kempe classes (whole-component swaps),
# and compute the radius (fewest swaps to a state whose link uses <= 3 colours) and the doubly locked states.
import sys, os, json, collections, itertools, time, re
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
t0 = time.time()
def tick(msg): print('[%5.1fs] %s' % (time.time() - t0, msg), flush=True)
PAIRS = list(itertools.combinations(range(4), 2))

# ============================================================== triangulation checks and layout
def check_triangulation(faces, min_deg=5):
    n = 1 + max(max(f) for f in faces)
    edges = set()
    for a, b, c in faces:
        for x, y in ((a, b), (b, c), (c, a)): edges.add((min(x, y), max(x, y)))
    adj = [set() for _ in range(n)]
    for x, y in edges: adj[x].add(y); adj[y].add(x)
    assert n - len(edges) + len(faces) == 2, 'Euler'
    ecount = collections.Counter()
    for a, b, c in faces:
        for x, y in ((a, b), (b, c), (c, a)): ecount[(min(x, y), max(x, y))] += 1
    assert all(v == 2 for v in ecount.values()), 'each edge in two faces'
    assert len(edges) == 3 * n - 6 and len(faces) == 2 * n - 4
    rot = []
    for v in range(n):
        inc = [f for f in faces if v in f]
        nb = collections.defaultdict(list)
        for f in inc:
            x, y = [u for u in f if u != v]; nb[x].append(y); nb[y].append(x)
        start = min(nb); cyc = [start]; prev = None; cur = start
        while True:
            nxt = [w for w in nb[cur] if w != prev][0]
            if nxt == start: break
            cyc.append(nxt); prev, cur = cur, nxt
        assert len(cyc) == len(adj[v]) == len(inc), ('link not a single cycle', v)
        rot.append(cyc)
    faceset = {tuple(sorted(f)) for f in faces}
    tri = [t for t in itertools.combinations(range(n), 3) if t[1] in adj[t[0]] and t[2] in adj[t[0]] and t[2] in adj[t[1]]]
    sep = [t for t in tri if t not in faceset]
    deg = [len(a) for a in adj]
    assert min(deg) >= min_deg and not sep, ('min degree / separating triangle', min(deg), sep[:3])
    return dict(n=n, edges=edges, adj=adj, rot=rot, deg=deg, sep=len(sep))

def make_layout(G, faces, seed=1, iters=6000, far_from=None):
    """Weighted Tutte drawing (outer face on a circle, positive weights, Floater) plus hill-climb for spacing."""
    n, edges, adj = G['n'], G['edges'], G['adj']
    Ea = np.array(sorted(edges)); Fa = np.array(faces)
    def gaps(P):
        dd = np.hypot(P[:, None, 0] - P[None, :, 0], P[:, None, 1] - P[None, :, 1])
        vv = dd[np.triu_indices(n, 1)].min()
        A_, B_ = P[Ea[:, 0]], P[Ea[:, 1]]; D_ = B_ - A_; L_ = (D_ * D_).sum(1)
        t = np.clip(((P[None, :, :] - A_[:, None, :]) * D_[:, None, :]).sum(2) / L_[:, None], 0, 1)
        Q_ = A_[:, None, :] + t[:, :, None] * D_[:, None, :]
        de = np.hypot(*(P[None, :, :] - Q_).transpose(2, 0, 1))
        de[np.arange(len(Ea)), Ea[:, 0]] = 9; de[np.arange(len(Ea)), Ea[:, 1]] = 9
        return float(vv), float(de.min())
    def score(P):
        vv, ve = gaps(P); return min(vv, 2 * ve)
    def fit(P):
        lo, hi = P.min(0), P.max(0); return (P - (lo + hi) / 2) * (2.08 / float((hi - lo).max()))
    def signs(P):
        a, b, c = P[Fa[:, 0]], P[Fa[:, 1]], P[Fa[:, 2]]
        return np.sign((b[:, 0] - a[:, 0]) * (c[:, 1] - a[:, 1]) - (b[:, 1] - a[:, 1]) * (c[:, 0] - a[:, 0]))
    def crossings(P):
        def ccw(a, b, c): return (P[b][0]-P[a][0])*(P[c][1]-P[a][1]) - (P[b][1]-P[a][1])*(P[c][0]-P[a][0])
        bad = 0
        for (a, b), (c, d) in itertools.combinations(sorted(edges), 2):
            if len({a, b, c, d}) == 4 and ccw(a, b, c) * ccw(a, b, d) < 0 and ccw(c, d, a) * ccw(c, d, b) < 0: bad += 1
        return bad
    def tutte(outer, alpha, rounds):
        P = np.zeros((n, 2))
        for k, v in enumerate(outer):
            ang = -np.pi / 2 + 2 * np.pi * k / 3; P[v] = [np.cos(ang), np.sin(ang)]
        depth = {v: 0 for v in outer}; qq = collections.deque(outer)
        while qq:
            u = qq.popleft()
            for w in adj[u]:
                if w not in depth: depth[w] = depth[u] + 1; qq.append(w)
        inner = [v for v in range(n) if v not in outer]; ix = {v: i for i, v in enumerate(inner)}
        def solve(wf):
            A = np.zeros((len(inner), len(inner))); b = np.zeros((len(inner), 2))
            for v in inner:
                i = ix[v]
                for w in adj[v]:
                    x = wf(v, w); A[i, i] += x
                    if w in ix: A[i, ix[w]] -= x
                    else: b[i] += x * P[w]
            s_ = np.linalg.solve(A, b)
            for v in inner: P[v] = s_[ix[v]]
        base = lambda v, w: float(np.exp(-alpha * depth[w]))
        solve(base)
        for _ in range(rounds):
            Lm = {(v, w): float(np.hypot(*(P[v] - P[w]))) for v in range(n) for w in adj[v]}
            solve(lambda v, w: base(v, w) * Lm[(v, w)])
        return fit(P)
    cf = faces
    if far_from is not None:   # outer face as far as possible from the hole, so the hole sits in the middle of the drawing
        dist = {far_from: 0}; qq = collections.deque([far_from])
        while qq:
            u = qq.popleft()
            for w in adj[u]:
                if w not in dist: dist[w] = dist[u] + 1; qq.append(w)
        fd = {tuple(f): min(dist[x] for x in f) for f in faces}; mxd = max(fd.values()); cf = [f for f in faces if fd[tuple(f)] == mxd]
    cands = [(score(tutte(list(f), al, r)), list(f), al, r) for f in cf for al in (0, 0.8, 1.6) for r in (0, 4)]
    _, outer, alpha, rounds = max(cands, key=lambda c: c[0])
    pos = tutte(outer, alpha, rounds); S0 = signs(pos); cur = score(pos)
    rng = np.random.default_rng(seed); movable = [v for v in range(n) if v not in outer]
    for it in range(iters):
        v = movable[rng.integers(len(movable))]; Z = pos.copy(); Z[v] += rng.normal(0, 0.03, 2)
        if (signs(Z) != S0).any(): continue
        s_ = score(Z)
        if s_ >= cur: pos, cur = Z, s_
    pos = fit(pos)
    assert (signs(pos) == S0).all() and crossings(pos) == 0, 'layout must be planar'
    return pos, outer, [round(x, 3) for x in gaps(pos)]

# ============================================================== colourings, Kempe classes, radius, locks
def analyse(G, hole, link):
    n = G['n']; adj = G['adj']
    V = [v for v in range(n) if v != hole]; pv = {v: i for i, v in enumerate(V)}
    nb = [[pv[w] for w in sorted(adj[v]) if w != hole] for v in V]
    L = [pv[x] for x in link]
    order = []; seen = {link[0]}; q = collections.deque([link[0]])
    while q:
        u = q.popleft(); order.append(u)
        for w in sorted(adj[u]):
            if w != hole and w not in seen: seen.add(w); q.append(w)
    assert len(order) == len(V)
    raw = []; col = {}
    def bt(k, used):
        if k == len(order): raw.append(tuple(col[v] for v in V)); return
        v = order[k]; bad = {col[w] for w in adj[v] if w in col}
        for c in range(min(used + 1, 4)):
            if c not in bad: col[v] = c; bt(k + 1, max(used, c + 1)); del col[v]
    bt(0, 0)
    def canon(c):
        m = {}; out = []
        for x in c:
            if x not in m: m[x] = len(m)
            out.append(m[x])
        return tuple(out)
    states = sorted(set(canon(s) for s in raw)); sidx = {s: i for i, s in enumerate(states)}
    assert len(states) == len(raw)
    def comps(c):
        out = []
        for a, b in PAIRS:
            seen = [False] * len(V)
            for s in range(len(V)):
                if seen[s] or c[s] not in (a, b): continue
                comp = [s]; seen[s] = True
                for k in comp:
                    for j in nb[k]:
                        if not seen[j] and c[j] in (a, b): seen[j] = True; comp.append(j)
                out.append((a, b, comp))
        return out
    def swap(c, m):
        a, b, comp = m; r = list(c)
        for i in comp: r[i] = b if r[i] == a else a
        return canon(r)
    nxt = [set(sidx[swap(s, m)] for m in comps(s)) for s in states]
    for i in range(len(states)):
        for j in nxt[i]: assert i in nxt[j], 'swaps are reversible'
    filled = [len(set(s[i] for i in L)) <= 3 for s in states]
    # classes
    cls = [-1] * len(states); nc = 0
    for i in range(len(states)):
        if cls[i] >= 0: continue
        cls[i] = nc; st = [i]
        while st:
            u = st.pop()
            for j in nxt[u]:
                if cls[j] < 0: cls[j] = nc; st.append(j)
        nc += 1
    # radius by multi-source BFS from filled
    rho = [-1] * len(states); dq = collections.deque()
    for i in range(len(states)):
        if filled[i]: rho[i] = 0; dq.append(i)
    while dq:
        u = dq.popleft()
        for j in nxt[u]:
            if rho[j] < 0: rho[j] = rho[u] + 1; dq.append(j)
    def compOf(c, start, a, b):
        seen = {start}; st = [start]
        while st:
            u = st.pop()
            for j in nb[u]:
                if j not in seen and c[j] in (a, b): seen.add(j); st.append(j)
        return seen
    def dl(c):
        lc = [c[i] for i in L]
        if len(set(lc)) < 4: return False
        j = [t for t in range(5) if lc[t] == lc[(t + 2) % 5]][0]
        m, a, b = L[(j + 1) % 5], L[(j + 3) % 5], L[(j + 4) % 5]
        return a in compOf(c, m, c[m], c[a]) and b in compOf(c, m, c[m], c[b])
    dls = [dl(s) for s in states]
    # a state is not filled and not doubly locked => one swap fills it  (cross-check of the lock test)
    for i, s in enumerate(states):
        if not filled[i]:
            one = any(filled[j] for j in nxt[i])
            assert one == (not dls[i]), ('lock test disagrees with one-swap fill', i)
    hist = collections.Counter(rho)
    assert min(rho) == 0 and all(r >= 0 for r in rho), 'every state reaches a filled state (one class with a filled state)'
    return dict(states=states, V=V, cls=cls, nclasses=nc, rho=rho, dl=dls, filled=filled,
                hist={str(k): hist[k] for k in sorted(hist)}, ndl=sum(dls), maxrho=max(rho))

def pick_demo_states(an, cap=6):
    """a few start states: one per radius value (prefer doubly locked), deterministic."""
    out = []
    for r in sorted(set(an['rho'])):
        if r == 0: continue
        cand = [i for i, x in enumerate(an['rho']) if x == r]
        cand.sort(key=lambda i: (not an['dl'][i], i))
        out.append(cand[0])
    return out[:cap]

# ============================================================== the two demo graphs
ICO = [(0,1,2),(0,2,3),(0,3,4),(0,4,5),(0,5,1),(1,2,6),(2,3,7),(3,4,8),(4,5,9),(5,1,10),
       (6,7,2),(7,8,3),(8,9,4),(9,10,5),(10,6,1),(11,6,7),(11,7,8),(11,8,9),(11,9,10),(11,10,6)]
# fix orientation-independent: faces are vertex sets; check below
cd = open(os.path.join(HERE, '..', 'cages', 'data.js')).read()
CD = json.loads(cd[cd.index('=') + 1:].strip().rstrip(';'))
F22 = [list(f) for f in CD['fcycle']['faces']]
assert CD['fcycle']['order'] == 22 and CD['fcycle']['hole'] == 15

graphs = []
for name, label, faces, hole, blurb in [
    ('ico', 'Icosahedron minus one vertex', [list(f) for f in ICO], 0,
     'The smallest triangulation with every degree at least 5. Every colouring here is filled or one swap from filled, so nothing gets stuck.'),
    ('o22', 'Order 22, hole 15 (the F-cycle graph)', F22, 15,
     'The graph of the cages page. It has doubly locked colourings, and one Kempe class that does contain filled colourings.')]:
    G = check_triangulation(faces)
    assert G['deg'][hole] == 5, 'hole has degree 5'
    link = G['rot'][hole]
    pos, outer, gp = make_layout(G, faces, far_from=hole, iters=2500)
    tick('%s: n=%d edges=%d min deg=%d, layout planar, gaps=%s' % (name, G['n'], len(G['edges']), min(G['deg']), gp))
    an = analyse(G, hole, link)
    tick('%s: %d colourings of T-hole (up to renaming), %d class(es), radius hist %s, doubly locked %d'
         % (name, len(an['states']), an['nclasses'], an['hist'], an['ndl']))
    demo = pick_demo_states(an)
    graphs.append(dict(
        name=name, label=label, blurb=blurb, order=G['n'], edges=len(G['edges']), hole=hole, link=link,
        linkDeg=[G['deg'][x] for x in link], deg=G['deg'], rot=G['rot'], faces=faces,
        pos=[[round(float(x), 4), round(float(y), 4)] for x, y in pos],
        summary=dict(colourings=len(an['states']), classes=an['nclasses'], hist=an['hist'], doublyLocked=an['ndl'], maxRadius=an['maxrho']),
        start=[dict(c=[int(x) for x in an['states'][i]], rho=an['rho'][i], dl=bool(an['dl'][i])) for i in demo],
        # all states: so the page can show "class size" and need no search for the radius
        all=[[int(x) for x in s] for s in an['states']], rho=an['rho'], dlflag=[int(x) for x in an['dl']]))

# ============================================================== Studio run 5 (exploratory), parsed from the committed text file
R5 = os.path.join(ROOT, 'backgroundMaterial', 'planemap-structural', 'longtable', 'studio-explore', 'sage-qa-runs', 'run5.txt')
rows = []
for line in open(R5):
    m = re.match(r'^(.*?) (\{.*\})\s*$', line.strip())
    d = json.loads(m.group(2)); cand = d['candidates']
    rows.append(dict(name=m.group(1), hole=d['hole'], states=d['states'], unfilled=d['unfilled'],
                     lock_size=cand['lock_size']['lower'], lock_dist=cand['lock_dist']['lower'],
                     lex=cand['lex_3_1_2']['lower'],
                     best_other=min(v['lower'] for k, v in cand.items() if k not in ('lock_size', 'lock_dist', 'lex_3_1_2')),
                     ncand=len(cand)))
assert len(rows) == 8 and all(r['ncand'] == 11 for r in rows)
# the page's claims: lock_size has 2..10 stuck states, out of 60..2713 unfilled; lock_dist reaches 0 only at Errera
assert min(r['lock_size'] for r in rows) == 2 and max(r['lock_size'] for r in rows) == 10
assert min(r['unfilled'] for r in rows) == 60 and max(r['unfilled'] for r in rows) == 2713
assert all(r['lock_size'] > 0 for r in rows)
assert [r['name'] for r in rows if r['lock_dist'] == 0] == ['Errera h0', 'Errera h4']
# every other candidate is stuck somewhere on every hole
for line in open(R5):
    d = json.loads(re.match(r'^(.*?) (\{.*\})\s*$', line.strip()).group(2))['candidates']
    for k, v in d.items():
        if k != 'lock_dist': assert v['lower'] > 0, (k, line[:30])
tick('run 5 parsed: %d holes' % len(rows))

data = {'graphs': graphs, 'run5': rows}
out = os.path.join(HERE, 'data.js')
with open(out, 'w') as f:
    f.write('// Generated by docs/physics/build_data.py. Do not edit.\nwindow.PHYSICS_DATA = ' + json.dumps(data, separators=(',', ':')) + ';\n')
tick('wrote %s (%d bytes)' % (out, os.path.getsize(out)))
