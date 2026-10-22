# Independent exact checker for one merge (my code; only lat.py/msat underneath).
#   min_R(g, A, B, colA, colB, w, level) = least R such that for SOME of the 24 renamings pi, recolouring
#   F = N_R(conflicts) cup N_w(dU) (distances inside U; w = -1 means no collar) gives a proper colouring of U
#   (and, if level=True, one in which every pocket of U has tau <= 1), everything outside F unchanged.
import itertools, collections, math
from lat import solve, bfs, disc_info, INC, n2, PERMS

def pockets(g, S, info=None):
    """pockets of disc S cut along its internal chords: list of dict(walk, s, odd)"""
    info = info or disc_info(g, S); tris = info['tris']; ch = set(info['chords'])
    par = {t: t for t in tris}
    def find(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for t in tris:
        f = g.faces[t]
        for a in range(3):
            u, w = f[a], f[(a+1) % 3]; o = g.face[(w, u)]
            if o in tris and (min(u, w), max(u, w)) not in ch: par[find(t)] = find(o)
    comp = collections.defaultdict(set)
    for t in tris: comp[find(t)].add(t)
    out = []
    for P in comp.values():
        bd = {}; cnt = collections.Counter()
        for t in P:
            f = g.faces[t]
            for a in range(3):
                u, w = f[a], f[(a+1) % 3]; cnt[u] += 1
                if g.face[(w, u)] not in P: bd[u] = w
        s0 = min(bd); walk = [s0]
        while bd[walk[-1]] != s0: walk.append(bd[walk[-1]])
        k = [cnt[b]-1 for b in walk]; s = [1]
        for i in range(1, len(walk)): s.append(s[-1]*(-1 if k[i] % 2 else 1))
        odd = (s[-1]*(-1 if k[0] % 2 else 1)) != s[0]
        out.append(dict(walk=walk, s=s, odd=odd, tris=P))
    return out

def tau(W, col):
    walk, s = W['walk'], W['s']; m = len(walk); H = [(0, 0)]
    for i in range(m):
        l = col[walk[i]] ^ col[walk[(i+1) % m]]
        if l == 0: return float('inf')
        d = INC[l]; H.append((H[-1][0]+s[i]*d[0], H[-1][1]+s[i]*d[1]))
    if W['odd']:
        q = ((H[0][0]+H[-1][0])/2, (H[0][1]+H[-1][1])/2)
        return math.sqrt(max(n2((h[0]-q[0], h[1]-q[1])) for h in H))
    As = [h[0] for h in H]; Bs = [h[1] for h in H]
    return math.sqrt(min(max(n2((h[0]-a, h[1]-b)) for h in H)
                         for a in range(min(As)-1, max(As)+2) for b in range(min(Bs)-1, max(Bs)+2)))

def weak_tau(g, S, col, P=None):
    P = P or pockets(g, S); return max(tau(W, col) for W in P)

def _domain(K2):
    R = int(2*math.sqrt(K2)) + 3
    return [(a, b) for a in range(-2*R, 2*R+1) for b in range(-2*R, 2*R+1) if n2((a, b)) <= K2 + 1e-9]

def sat_extend(g, Uset, col, free, walks=(), K2=1.0, budget=None):
    """proper colouring of the induced graph on Uset, = col outside `free`, each walk tau^2<=K2. dict or None/'UNK'"""
    fl = sorted(free); ix = {v: i for i, v in enumerate(fl)}
    x = lambda v, c: 4*ix[v] + c + 1; top = [4*len(fl)]; cls = []
    def new(): top[0] += 1; return top[0]
    # literal for "v has colour c" (constant for fixed vertices: returns True/False)
    def L(v, c):
        if v in ix: return x(v, c)
        return col[v] == c
    for v in fl:
        cls.append([x(v, c) for c in range(4)])
        for a, b in itertools.combinations(range(4), 2): cls.append([-x(v, a), -x(v, b)])
        for w in g.adj[v]:
            if w not in Uset: continue
            if w in ix:
                if w > v:
                    for c in range(4): cls.append([-x(v, c), -x(w, c)])
            else: cls.append([-x(v, col[w])])
    for v in Uset:            # fixed-fixed edges must already be proper
        if v in ix: continue
        for w in g.adj[v]:
            if w in Uset and w not in ix and col[v] == col[w]: return None
    Dm = _domain(K2); Ds = set(Dm)
    for W in walks:
        walk, s = W['walk'], W['s']; m = len(walk)
        H = [{p: new() for p in Dm} for _ in range(m+1)]
        for i in range(m):
            u, w = walk[i], walk[(i+1) % m]
            lab = {}
            if u not in ix and w not in ix:
                lab = {col[u] ^ col[w]: None}
                if 0 in lab: return None
            else:
                Lv = {l: new() for l in (1, 2, 3)}
                for a in range(4):
                    for b in range(4):
                        if a == b: continue
                        la, lb = L(u, a), L(w, b)
                        if la is False or lb is False: continue
                        c = [Lv[a ^ b]]
                        if la is not True: c.append(-la)
                        if lb is not True: c.append(-lb)
                        cls.append(c)
                lab = Lv
            for p in Dm:
                for l in (1, 2, 3):
                    if l not in lab: continue
                    d = INC[l]; q = (p[0]+s[i]*d[0], p[1]+s[i]*d[1])
                    c = [-H[i][p]] + ([] if lab[l] is None else [-lab[l]])
                    if q in Ds: c.append(H[i+1][q])
                    cls.append(c)
        cls.append([H[0][p] for p in Dm])
        for p, q in itertools.combinations(Dm, 2): cls.append([-H[0][p], -H[0][q]])
        if W['odd']:
            for p in Dm: cls.append([-H[m][p], H[0][(-p[0], -p[1])]])
    r = solve(top[0], cls, budget)
    if r is None or r == 'UNK': return r
    out = dict(col)
    for v in fl: out[v] = next(c for c in range(4) if x(v, c) in r)
    return out

def glue(A, B, colA, colB, p):
    c = {v: colA[v] for v in A}; c.update({v: p[colB[v]] for v in B}); return c

def conflicts(g, A, B, c):
    return set(x for u in A for w in g.adj[u] if w in B and c[u] == c[w] for x in (u, w))

def min_R(g, A, B, colA, colB, w=-1, level=False, Rmax=12, perms=PERMS, budget=None, verbose=False):
    U = set(A) | set(B); info = disc_info(g, U)
    dB = bfs(g.adj, list(info['bset']), U)
    coll = set(v for v in U if dB[v] <= w)
    P = pockets(g, U, info) if level else ()
    data = []
    for p in perms:
        c = glue(A, B, colA, colB, p); K = conflicts(g, A, B, c)
        data.append((len(K), p, c, K, bfs(g.adj, list(K), U) if K else {}))
    data.sort(key=lambda t: t[0])
    unk = 0
    for R in range(0, Rmax+1):
        for nk, p, c, K, dK in data:
            free = set(v for v in U if dK.get(v, 99) <= R) | coll
            if not free:
                if not level or weak_tau(g, U, c, P) <= 1 + 1e-9: return dict(R=R, perm=p, col=c, nK=nk, unk=unk)
                continue
            r = sat_extend(g, U, c, free, P, 1.0, budget)
            if r == 'UNK': unk += 1; continue
            if r is not None:
                assert all(r[a] != r[b] for a in U for b in g.adj[a] if b in U)
                if level: assert weak_tau(g, U, r, P) <= 1 + 1e-9
                return dict(R=R, perm=p, col=r, nK=nk, unk=unk, nfree=len(free))
        if verbose: print('  R=%d infeasible for all %d renamings' % (R, len(data)), flush=True)
    return dict(R=None, unk=unk)
