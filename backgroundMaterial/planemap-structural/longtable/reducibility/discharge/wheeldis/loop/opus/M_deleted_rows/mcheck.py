"""M_deleted_rows: independent check of Studio's 163 option-F sender-row deletions (job30f, bd8472d9).
Own model + own matcher (exact degrees, induced, triangles onto faces, rotation-faithful at every interior vertex with
ring-gap positions, one global mirror).  For each row: all embeddings of every K into the five's 2-ball (free
second-ring slots allowed, each embedding then requires letters on the free slots it uses); then every filling of the
relevant free slots over 5..9 is checked.  Only wlp.py's isR5/isR6/senders (the registry) are reused.
Usage: python3 mcheck.py [sample=200]"""
import os, sys, itertools, random
import numpy as np, networkx as nx
MH = os.path.dirname(os.path.abspath(__file__)); WD = os.path.abspath(os.path.join(MH, "..", "..", ".."))
src = open(os.path.join(WD, 'wlp.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(WD, 'wlp.py')))
sys.argv = sys.argv[:1] + []; _a = sys.argv; sys.argv = ['wlp']; exec(src[:src.index('# ---- option bigw')]); sys.argv = _a
LET = (5, 6, 7, 8, 9)

# ---------- kill configurations
def parse(line):
    f = line.split(); n, m = int(f[1]), int(f[2]); rp, ip = f[3].split(';'), f[4].split(';')
    G = nx.Graph(); G.add_nodes_from(range(m))
    for i in range(n): G.add_edge(('r', i), ('r', (i + 1) % n)); G.add_edge(('r', i), 'hub')
    for u in range(m):
        if rp[u] != '-':
            for x in rp[u].split(','): G.add_edge(u, ('r', int(x)))
        if ip[u] != '-':
            for x in ip[u].split(','): G.add_edge(u, int(x))
    ok, emb = nx.check_planarity(G); assert ok
    assert nx.node_connectivity(G) >= 3, f[0]          # unique embedding up to mirror
    U = list(range(m)); deg = {u: G.degree(u) for u in U}; E = {u: {x for x in G[u] if isinstance(x, int)} for u in U}
    pos = {}
    for u in U:
        rot = list(emb.neighbors_cw_order(u))
        for i in range(len(rot)): assert G.has_edge(rot[i], rot[(i + 1) % len(rot)])   # faces are triangles
        pos[u] = {x: i for i, x in enumerate(rot) if isinstance(x, int)}
    tri = {frozenset((a, b, c)) for a in U for b in E[a] for c in E[a] & E[b] if a < b < c}
    bic = nx.is_biconnected(G.subgraph(U))
    return dict(name=f[0], U=U, deg=deg, E=E, pos=pos, tri=tri, bic=bic)

# ---------- the five's 2-ball (my own construction from SPEC section 1)
def model(w):
    faces = []; nodes = ['v'] + [('a', k) for k in range(5)] + [('t', k) for k in range(5)]
    for k in range(5):
        j = (k + 1) % 5; faces += [('v', ('a', k), ('a', j)), (('a', k), ('t', k), ('a', j))]
    for k in range(5):
        if w[k] == 9: continue
        path = [('t', (k - 1) % 5)] + [('q', k, i) for i in range(1, w[k] - 4)] + [('t', k)]
        nodes += path[1:-1]
        for p, q in zip(path, path[1:]): faces.append((('a', k), p, q))
    adj = {x: set() for x in nodes}; succ = {x: {} for x in nodes}
    for f in faces:
        for i in range(3):
            x, y, z = f[i], f[(i + 1) % 3], f[(i + 2) % 3]
            adj[x] |= {y, z}; assert y not in succ[x] or succ[x][y] == z; succ[x][y] = z
    tris = {frozenset((x, y, z)) for x in nodes for y in adj[x] for z in adj[x] & adj[y]}
    assert tris == {frozenset(f) for f in faces}          # every triangle is a face
    arc = {}
    for x in nodes:                                       # positions of x's known neighbours along its rotation
        s = succ[x]; starts = [y for y in s if y not in s.values()]
        if not starts: y0 = min(s, key=str); cyc = True
        else: assert len(starts) == 1; y0 = starts[0]; cyc = False
        seq = [y0]
        while seq[-1] in s and s[seq[-1]] != y0: seq.append(s[seq[-1]])
        assert set(seq) == adj[x]
        arc[x] = ({y: i for i, y in enumerate(seq)}, cyc, len(seq))
    return nodes, adj, tris, arc

def embeddings(K, w, M, let):
    """all embeddings; yields requirement dict {free slot: letter}"""
    nodes, adj, tris, arc = M; U, deg, E = K['U'], K['deg'], K['E']
    order = [max(U, key=lambda u: len(E[u]))]
    while len(order) < len(U):
        order.append(max((u for u in U if u not in order), key=lambda u: (len(E[u] & set(order)), len(E[u]))))
    phi = {}; out = []
    def okv(u, x):
        L = let.get(x)
        if L is None: return x[0] in 'tq' and deg[u] <= 8
        return L == deg[u] and L <= 8
    def rot_ok(s):
        for u in U:
            x = phi[u]; P, cyc, n = arc[x]; g = deg[u]
            if cyc: assert n == g
            assert n <= g
            off = None
            for y, pk in K['pos'][u].items():
                pm = P[phi[y]]; o = (pm - s * pk) % g
                if off is None: off = o
                elif o != off: return False
        return True
    def rec(i):
        if i == len(order):
            if not all(frozenset(phi[a] for a in t) in tris for t in K['tri']): return
            if rot_ok(1) or rot_ok(-1):
                out.append(tuple(sorted(((phi[u], deg[u]) for u in U if phi[u] not in let), key=str)))
            return
        u = order[i]; pl = [y for y in order[:i] if y in E[u]]
        cand = set.intersection(*[adj[phi[y]] for y in pl]) if pl else set(nodes)
        used = set(phi.values())
        for x in cand:
            if x in used or not okv(u, x): continue
            if any((phi[y] in adj[x]) != (y in E[u]) for y in order[:i]): continue
            phi[u] = x; rec(i + 1); del phi[u]
    rec(0); return out

def impossible_fn(w, fill):
    for k in range(5):
        tp, tn = fill.get(('t', (k - 1) % 5)), fill.get(('t', k))
        if tp is None or tn is None: continue
        if w[k] == 5 and isR5([5, w[(k + 1) % 5], tn, tp, w[(k - 1) % 5]]): return True
        if w[k] == 6 and ('q', k, 1) in fill and isR6([5, w[(k + 1) % 5], tn, fill[('q', k, 1)], tp, w[(k - 1) % 5]]):
            return True
    return False

KS_ALL = [parse(l) for l in open(os.path.join(MH, 'kills.txt')) if l.strip()]
KS = [K for K in KS_ALL if K['bic']]
MODELS = {}
def check(w, z):
    """returns (n_fillings, n_escape_K, n_escape_after_impossible, examples, which K used)"""
    if w not in MODELS: MODELS[w] = model(w)
    M = MODELS[w]; let = {'v': 5}; let.update({('a', k): w[k] for k in range(5)}); let.update(z)
    reqs = []; used = {}
    for K in KS:
        for r in embeddings(K, w, M, let):
            reqs.append(r); used.setdefault(r, K['name'])
    if () in used: return (1, 0, 0, [], {used[()]})
    slots = sorted({x for r in reqs for x, _ in r}, key=str)
    # slots needed for the R5/R6 impossibility of wheels touching these slots
    extra = set()
    for k in range(5):
        if w[k] in (5, 6):
            ws = [('t', (k - 1) % 5), ('t', k)] + ([('q', k, 1)] if w[k] == 6 else [])
            if any(s in slots for s in ws): extra |= {s for s in ws if s not in let}
    slots = slots + sorted(extra - set(slots), key=str)
    if not slots: return (1, 1, 1, [{}], set())
    ix = {s: i for i, s in enumerate(slots)}; n = len(slots)
    F = np.array(list(itertools.product(LET, repeat=n)), dtype=np.int8)
    dead = np.zeros(len(F), bool)
    for r in reqs:
        m = np.ones(len(F), bool)
        for x, L in r: m &= F[:, ix[x]] == L
        dead |= m
    escK = np.nonzero(~dead)[0]; esc2 = []
    for i in escK:
        fill = dict(let); fill.update({s: int(F[i, ix[s]]) for s in slots})
        if not impossible_fn(w, fill): esc2.append({s: int(F[i, ix[s]]) for s in slots})
    return (len(F), len(escK), len(esc2), esc2[:3], set(used.values()))

def rows():
    out = []
    for w in senders:
        x = list(w); per = []
        for k in range(5):
            if x[k] != 6: continue
            bl, br = x[(k - 1) % 5] >= 7, x[(k + 1) % 5] >= 7
            if not (bl or br): continue
            ok = {(zR if br else 0, zL if bl else 0) for zR in L for q in L for zL in L
                  if not isR6([5, x[(k + 1) % 5], zR, q, zL, x[(k - 1) % 5]])}
            per.append([dict(([(('t', k), zR)] if br else []) + ([(('t', (k - 1) % 5), zL)] if bl else [])) for zR, zL in ok])
        for combo in itertools.product(*per):
            z = {}
            for d in combo: z.update(d)
            out.append((tuple(w), tuple(sorted(z.items(), key=str))))
    return out

def fmt(w, z): return ''.join(map(str, w)) + ''.join(' t%d=%d' % (s[1], L) for s, L in sorted(z, key=lambda p: p[0][1]))

def sym_images(w, z):
    """images of row (w,z) under dihedral maps g with g(w) = w (rotation r, then optional reflection)."""
    res = []
    for refl in (False, True):
        for r in range(5):
            if refl: f = lambda k: (r - k) % 5; ft = lambda k: (r - k - 1) % 5
            else: f = lambda k: (k + r) % 5; ft = lambda k: (k + r) % 5
            w2 = [None] * 5
            for k in range(5): w2[f(k)] = w[k]
            if tuple(w2) != w: continue
            res.append((w, tuple(sorted(((('t', ft(s[1])), L) for s, L in z), key=str))))
    return res

if __name__ == '__main__':
    nsamp = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    print('configs used:', [K['name'] for K in KS], ' excluded (interior not 2-connected):', [K['name'] for K in KS_ALL if not K['bic']])
    R = rows(); print('sender rows enumerated', len(R)); Rs = set(R)
    dele = []
    for l in open(os.path.join(MH, 'deleted_rows.txt')):
        f = l.split(); w = tuple(map(int, f[0])); z = tuple(sorted(((('t', int(t[1])), int(t[3:])) for t in f[1:]), key=str))
        dele.append((w, z))
    print('deleted', len(dele), ' all are enumerated rows:', all(d in Rs for d in dele))
    D = set(dele); bad_sym = [(fmt(*d), fmt(*im)) for d in dele for im in sym_images(*d) if im not in D]
    print('reflection/rotation closure failures:', len(bad_sym), bad_sym[:5])
    conf = confK = 0; usedK = {}
    for w, z in dele:
        nF, eK, e2, ex, us = check(w, dict(z))
        for u in us: usedK[u] = usedK.get(u, 0) + 1
        if eK == 0: confK += 1
        if e2 == 0: conf += 1
        else: print('UNCONFIRMED', fmt(w, z), 'fillings', nF, 'escape', e2, 'e.g.', ex)
        if eK and not e2: print('  needs R5/R6 impossibility:', fmt(w, z), 'fillings', nF, 'K-escapes', eK)
    print('deleted rows confirmed: %d / %d (pure K, no R5/R6 impossibility used: %d)' % (conf, len(dele), confK))
    print('configs giving embeddings in deleted rows:', usedK)
    random.seed(1); keep = [r for r in R if r not in D]; samp = random.sample(keep, min(nsamp, len(keep)))
    should = [fmt(*r) for r in samp if check(r[0], dict(r[1]))[2] == 0]
    print('completeness sample: %d kept rows, %d should have been deleted %s' % (len(samp), len(should), should[:10]))
