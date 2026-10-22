# Weakened step (W1): bottom-up recursion over the top-down splitter's hierarchy (hier.split), where every node
# U must only be WEAKLY level: cut U along its internal chords into chordless pockets; require tau(P) <= 1 for
# every pocket P under ONE colouring of U.  Merge = renaming + min-R proper repair near conflicts, then
# re-level the collar N_w(dU) (+ repair zone) so that all pockets of U are level.  Final merge: repair only.
import sys, os, json, time, random, collections, itertools, math
sys.path.insert(0, '/mnt/project-files/multiscale/hierarchy'); sys.path.insert(0, '/mnt/project-files/multiscale/levelling')
import hier
from hier import G, check, split, reflex
from lev import INC, n2, domain, multi_bfs, PERMS
from pysat.solvers import Cadical153, Glucose4

class Disc:
    """near-triangulated disc on vertex set S (faces of G with all vertices in S); pockets along internal chords."""
    def __init__(self, g, S):
        self.g = g; S = set(S); self.S = S
        tris = set(i for v in S for i in g.vf[v] if all(x in S for x in g.faces[i])); self.tris = tris
        self.edges = set(); bd = {}
        for i in tris:
            f = g.faces[i]
            for j in range(3):
                u, w = f[j], f[(j+1) % 3]; self.edges.add((min(u, w), max(u, w)))
                if g.face[(w, u)] not in tris: bd[u] = w
        self.bset = set(bd)
        bedges = set((min(u, w), max(u, w)) for u, w in bd.items())
        self.chords = [e for e in self.edges if e[0] in self.bset and e[1] in self.bset and e not in bedges]
        ch = set(self.chords)
        # union-find on triangles across non-chord interior edges
        par = {i: i for i in tris}
        def find(x):
            while par[x] != x: par[x] = par[par[x]]; x = par[x]
            return x
        for i in tris:
            f = g.faces[i]
            for j in range(3):
                u, w = f[j], f[(j+1) % 3]; o = g.face[(w, u)]
                if o in tris and (min(u, w), max(u, w)) not in ch: par[find(i)] = find(o)
        comp = collections.defaultdict(set)
        for i in tris: comp[find(i)].add(i)
        self.pockets = [self.walk_of(P) for P in comp.values()]
        self.whole = self.walk_of(tris)
    def walk_of(self, P):
        g = self.g; bd = {}; cnt = collections.Counter()
        for i in P:
            f = g.faces[i]
            for j in range(3):
                u, w = f[j], f[(j+1) % 3]; cnt[u] += 1
                if g.face[(w, u)] not in P: assert u not in bd; bd[u] = w
        start = min(bd); walk = [start]
        while True:
            x = bd[walk[-1]]
            if x == start: break
            walk.append(x)
        assert len(walk) == len(bd)
        k = [cnt[b]-1 for b in walk]; s = [1]
        for i in range(1, len(walk)): s.append(s[-1]*(-1 if k[i] % 2 else 1))
        closing = s[-1]*(-1 if k[0] % 2 else 1)
        return dict(walk=walk, s=s, odd=(closing != s[0]), nv=len(set(x for i in P for x in g.faces[i])))

def tau_walk(W, col):
    walk, s = W['walk'], W['s']; m = len(walk); H = [(0, 0)]
    for i in range(m):
        l = col[walk[i]] ^ col[walk[(i+1) % m]]
        if l == 0: return 99.0
        d = INC[l]; H.append((H[-1][0]+s[i]*d[0], H[-1][1]+s[i]*d[1]))
    if W['odd']:
        q = ((H[0][0]+H[-1][0])/2, (H[0][1]+H[-1][1])/2)
        return math.sqrt(max(n2((h[0]-q[0], h[1]-q[1])) for h in H))
    As = [h[0] for h in H]; Bs = [h[1] for h in H]; best = 1e9
    for A in range(min(As)-1, max(As)+2):
        for B in range(min(Bs)-1, max(Bs)+2):
            best = min(best, max(n2((h[0]-A, h[1]-B)) for h in H))
    return math.sqrt(best)

def sat(D, walks, K2, fixed=None, budget=3*10**6):
    """proper 4-colouring of disc D, every walk in `walks` with tau^2 <= K2. None=UNSAT, 'UNK', or dict."""
    V = sorted(D.S); ix = {v: i for i, v in enumerate(V)}
    x = lambda v, c: 4*ix[v]+c+1; top = [4*len(V)]
    def new(): top[0] += 1; return top[0]
    cls = []
    for v in V:
        if fixed and v in fixed: cls.append([x(v, fixed[v])]); continue
        cls.append([x(v, c) for c in range(4)])
        for a, b in itertools.combinations(range(4), 2): cls.append([-x(v, a), -x(v, b)])
    for u, w in D.edges:
        if fixed and u in fixed and w in fixed: continue
        for c in range(4): cls.append([-x(u, c), -x(w, c)])
    if not fixed:
        f = D.g.faces[next(iter(D.tris))]
        for j in range(3): cls.append([x(f[j], j)])
    Dm = domain(K2); Ds = set(Dm)
    for W in walks:
        walk, s = W['walk'], W['s']; m = len(walk)
        H = [{p: new() for p in Dm} for _ in range(m+1)]
        for i in range(m):
            u, w = walk[i], walk[(i+1) % m]; L = {l: new() for l in (1, 2, 3)}
            for a in range(4):
                for b in range(4):
                    if a != b: cls.append([-x(u, a), -x(w, b), L[a ^ b]])
            for p in Dm:
                for l in (1, 2, 3):
                    d = INC[l]; q = (p[0]+s[i]*d[0], p[1]+s[i]*d[1])
                    cls.append([-H[i][p], -L[l], H[i+1][q]] if q in Ds else [-H[i][p], -L[l]])
        cls.append([H[0][p] for p in Dm])
        for p, q in itertools.combinations(Dm, 2): cls.append([-H[0][p], -H[0][q]])
        if W['odd']:
            for p in Dm: cls.append([-H[m][p], H[0][(-p[0], -p[1])]])
        else:   # even: closed one lap must end at same centre-relative position modulo t -- centre is free; nothing
            pass
    s_ = Glucose4(bootstrap_with=cls)
    if budget: s_.conf_budget(budget); ok = s_.solve_limited()
    else: ok = s_.solve()
    if ok is None: s_.delete(); return 'UNK'
    res = None
    if ok:
        mod = set(l for l in s_.get_model() if l > 0)
        res = {v: next(c for c in range(4) if x(v, c) in mod) for v in V}
    s_.delete(); return res

def proper_repair(g, Sset, edges, col, K, Rmax):
    """min R: recolour N_R(K) within Sset (rest fixed) to a proper colouring of the induced edges."""
    for R in range(Rmax+1):
        d = multi_bfs(g.adj, list(K), Sset)
        free = set(v for v in Sset if d.get(v, 99) <= R)
        x = lambda v, c: 4*v+c+1; cls = []
        for v in free:
            cls.append([x(v, c) for c in range(4)])
            for a, b in itertools.combinations(range(4), 2): cls.append([-x(v, a), -x(v, b)])
            for w in g.adj[v]:
                if w not in Sset: continue
                if w in free:
                    if w > v:
                        for c in range(4): cls.append([-x(v, c), -x(w, c)])
                else: cls.append([-x(v, col[w])])
        s = Cadical153(bootstrap_with=cls); ok = s.solve()
        if ok:
            mod = set(l for l in s.get_model() if l > 0); s.delete()
            c2 = dict(col)
            for v in free: c2[v] = next(c for c in range(4) if x(v, c) in mod)
            return R, c2
        s.delete()
    return None, None

NPERM = 6
def proper_repair_at(g, Sset, col, K, R):
    d = multi_bfs(g.adj, list(K), Sset)
    free = set(v for v in Sset if d.get(v, 99) <= R)
    x = lambda v, c: 4*v+c+1; cls = []
    for v in free:
        cls.append([x(v, c) for c in range(4)])
        for w in g.adj[v]:
            if w not in Sset: continue
            if w in free:
                if w > v:
                    for c in range(4): cls.append([-x(v, c), -x(w, c)])
            else: cls.append([-x(v, col[w])])
    s = Cadical153(bootstrap_with=cls); ok = s.solve()
    if not ok: s.delete(); return None, None
    mod = set(l for l in s.get_model() if l > 0); s.delete(); c2 = dict(col)
    for v in free: c2[v] = next(c for c in range(4) if x(v, c) in mod)
    return R, c2

def build_tree(g, L=40, seed=0, exh=16, tries=8):
    """hier.build, but returns the tree: nodes = dict(S, kids, bad, dep)."""
    rng = random.Random(seed); nodes = []
    stack = [(set(range(g.n)), None, 0, None)]
    while stack:
        U, walk, dep, parent = stack.pop()
        nid = len(nodes); nodes.append(dict(S=U, kids=[], bad=False, dep=dep))
        if parent is not None: nodes[parent]['kids'].append(nid)
        if walk is not None and len(U) <= L: continue
        r = split(g, U, walk, rng, tries=(tries if len(U) > 300 else 3*tries), L=L)
        if (r is None or r[0] is None) and walk is not None and len(U) <= exh:
            e = hier.exhaustive_split(g, U)
            if e: r = (e[0], e[1], {})
            else: continue
        if r is None: raise RuntimeError('nothing')
        if r[0] is None:
            sc, A, B = r[1]; sa, sb = check(g, A), check(g, B)
            nodes[nid]['bad'] = True
            if sa[0] == 'nodisc' or sb[0] == 'nodisc': continue
        else:
            A, B, info = r; sa, sb = check(g, A), check(g, B)
        stack.append((A, sa[1], dep+1, nid)); stack.append((B, sb[1], dep+1, nid))
    return nodes

def do_merge(g, D, A, B, col, wmax=6, Rmax=8, bad=False, dep=0):
    tm = time.time()
    seam = [(u, w) for (u, w) in D.edges if (u in A) != (w in A)]
    best = []
    for p in PERMS:
        cc = {v: col[v] for v in A}; cc.update({v: p[col[v]] for v in B})
        K = set(x for e in seam if cc[e[0]] == cc[e[1]] for x in e)
        best.append((len(K), p, cc, K))
    best.sort(key=lambda t: t[0])
    # min R over renamings (try the 6 fewest-conflict renamings)
    R = None; cR = None; glued = None
    if NPERM <= 6:
        for nk, p, cc, K in best[:NPERM]:
            if not K: R, cR, glued = 0, cc, cc; break
            r, c2 = proper_repair(g, D.S, D.edges, cc, K, Rmax)
            if r is not None and (R is None or r < R): R, cR, glued = r, c2, cc
            if R == 0: break
    else:   # R outer, all renamings inner (as levelling/lev.merge)
        for RR in range(Rmax+1):
            for nk, p, cc, K in best:
                if not K: R, cR, glued = 0, cc, cc; break
                r, c2 = proper_repair_at(g, D.S, cc, K, RR)
                if r is not None: R, cR, glued = RR, c2, cc; break
            if R is not None: break
    zone = set(v for v in D.S if cR[v] != glued[v])
    ptau_before = max(tau_walk(W, cR) for W in D.pockets)
    dB = multi_bfs(g.adj, list(D.bset), D.S)
    w = None; c3 = None
    for ww in range(0, wmax+1):
        if ww == 0 and ptau_before <= 1+1e-9: w, c3 = 0, cR; break
        fixed = {v: cR[v] for v in D.S if dB[v] > ww and v not in zone}
        r = sat(D, D.pockets, 1.0, fixed=fixed)
        if r not in (None, 'UNK'): w, c3 = ww, r; break
    fallback = None
    if c3 is None:
        r = sat(D, D.pockets, 1.0, fixed=None, budget=2*10**7)
        if r not in (None, 'UNK'):
            fallback = 'full_relevel'; c3 = r
        else:
            fallback = 'not_weak_levelable' if r is None else 'unknown'; c3 = cR
    col.update(c3)
    DA_, DB_ = Disc(g, A), Disc(g, B)
    kidch = len(DA_.chords)+len(DB_.chords)
    def spock(DX):   # pockets of X having a boundary edge on the seam arc (outside face lies in U)
        k = 0
        for W in DX.pockets:
            wl = W['walk']; m = len(wl)
            if any(g.face[(wl[(i+1) % m], wl[i])] in D.tris and g.face[(wl[(i+1) % m], wl[i])] not in DX.tris for i in range(m)): k += 1
        return k
    sA, sB = spock(DA_), spock(DB_)
    seamP = len(set(j for j, W in enumerate(D.pockets) for e in seam if e[0] in W['walk'] and e[1] in W['walk']))
    rec = dict(dep=dep, nA=len(A), nB=len(B), nU=len(D.S), mU=len(D.whole['walk']), chords=len(D.chords),
               pockets=len(D.pockets), maxpocket=max(W['nv'] for W in D.pockets), bad_split=bad, kid_chords=kidch, seam_pockets=seamP, sA=sA, sB=sB, minpocket_m=min(len(W['walk']) for W in D.pockets),
               nconf=best[0][0], R=R, w=w, ptau_before=round(ptau_before, 3),
               ptau_after=round(max(tau_walk(W, c3) for W in D.pockets), 3), strict_tau_after=round(tau_walk(D.whole, c3), 3),
               fallback=fallback, sec=round(time.time()-tm, 1))
    return rec

def run(name, adj, seed=0, L=40, wmax=6, Rmax=8, log=None):
    g = G(adj); t0 = time.time()
    nodes = build_tree(g, L=L, seed=seed)
    tbuild = time.time()-t0
    col = {}; recs = []; leafinfo = []
    order = []
    st = [0]
    while st:     # post-order
        i = st.pop(); order.append(i); st.extend(nodes[i]['kids'])
    order.reverse()
    for i in order:
        nd = nodes[i]
        if i == 0: continue
        D = Disc(g, nd['S'])
        if not nd['kids']:
            c = sat(D, D.pockets, 1.0, budget=None)
            ok = c is not None
            if not ok: c = sat(D, [], 1.0, budget=None)   # fallback: any proper colouring
            col.update(c)
            leafinfo.append(dict(n=len(D.S), chords=len(D.chords), pockets=len(D.pockets), weak_level=ok,
                                 strict_tau=round(tau_walk(D.whole, c), 3)))
            continue
        a, b = nd['kids']; A, B = nodes[a]['S'], nodes[b]['S']
        rec = do_merge(g, D, A, B, col, wmax, Rmax, nd['bad'], nd['dep'])
        recs.append(rec)
        if log: log.write(json.dumps(rec)+'\n'); log.flush()
    # root: final closing merge
    a, b = nodes[0]['kids']; A, B = nodes[a]['S'], nodes[b]['S']
    allS = set(range(g.n)); E = set((u, w) for u in range(g.n) for w in g.adj[u] if u < w)
    best = None
    for p in PERMS:
        cc = {v: col[v] for v in A}; cc.update({v: p[col[v]] for v in B})
        K = set(x for (u, w) in E if cc[u] == cc[w] for x in (u, w))
        if best is None or len(K) < len(best[0]): best = (K, cc)
    K, cc = best
    if K: Rf, cf = proper_repair(g, allS, E, cc, K, 14)
    else: Rf, cf = 0, cc
    proper = cf is not None and all(cf[u] != cf[w] for (u, w) in E)
    DA, DB = Disc(g, A), Disc(g, B)
    fin = dict(R_final=Rf, nconf_final=len(K), sizes=[len(A), len(B)], chords_final=[len(DA.chords), len(DB.chords)],
               pockets_final=[len(DA.pockets), len(DB.pockets)], proper=proper)
    return dict(n=g.n, nodes=len(nodes), tbuild=round(tbuild), sec=round(time.time()-t0), recs=recs, leaves=leafinfo, **fin)
