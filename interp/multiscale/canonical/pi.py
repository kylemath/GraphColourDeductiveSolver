# Pair induction along a canonical (de Fraysseix-Pach-Pollack) ordering.
# Invariant on a coloured disc (boundary cycle b_0..b_{L-1}, gauge signs s_i, lifted walk H):
#   even #interior-odd: |t| <= 2 and tau_H = circumradius{H_i - (i/L) t : 0<=i<L} <= 1
#   odd  #interior-odd: max_i |H_i - q| <= TODD, q = (H_0 + H_L)/2 (reflection centre)
# Heights as complex numbers: label 1,2,3 -> 1, w, w^2 (unit vectors at 120 deg).
# Step: add next canonical vertex v (attachment path P on the current boundary). Free set = ball_{G_{k+1}}(v, R)
# (R = 0: only v, i.e. greedy; R = r: v plus everything within r-1 of P). Minimal R found by enumeration of the
# free boundary colours (exact pair check) + SAT extension of the free interior vertices.
import sys, math, random, itertools, collections, time
import numpy as np, networkx as nx
from scipy.spatial import ConvexHull
from pysat.solvers import Cadical153
W3 = complex(-0.5, math.sqrt(3)/2)
EV = np.array([0, 1, W3, W3*W3])          # label -> unit vector
TODD = 1.0

# ---------------- generators ----------------
sys.path.insert(0, '/mnt/project-files/multiscale'); sys.path.insert(0, '/mnt/project-files/multiscale/hierarchy')
sys.path.insert(0, '/mnt/project-files/multiscale/levelling'); sys.path.insert(0, '/mnt/project-files/multiscale/binder_maps')

def icosphere(f):
    import ms_tilt
    return [set(s) for s in ms_tilt.icosphere(f)]

def flips(adj, nflips, rng, mindeg=5, maxdeg=9):
    adj = [set(a) for a in adj]; n = len(adj); done = 0; tries = 0
    while done < nflips and tries < nflips*100:
        tries += 1; a = rng.randrange(n); b = rng.choice(sorted(adj[a])); cn = adj[a] & adj[b]
        if len(cn) != 2: continue
        c, d = cn
        if d in adj[c]: continue
        if len(adj[a])-1 < mindeg or len(adj[b])-1 < mindeg or len(adj[c])+1 > maxdeg or len(adj[d])+1 > maxdeg: continue
        adj[a].discard(b); adj[b].discard(a); adj[c].add(d); adj[d].add(c); done += 1
    return adj

def hubs(adj, nh, target, rng, mindeg=4):
    """grow nh hubs to degree ~target by flipping the edges opposite them (min degree mindeg elsewhere)."""
    adj = [set(a) for a in adj]; n = len(adj); H = rng.sample(range(n), nh)
    for h in H:
        tries = 0
        while len(adj[h]) < target and tries < 5000:
            tries += 1; a = rng.choice(sorted(adj[h])); cn = adj[h] & adj[a]
            b = rng.choice(sorted(cn))           # triangle h,a,b; flip ab to h-x
            cab = adj[a] & adj[b]
            if len(cab) != 2: continue
            x = next(iter(cab - {h}))
            if x in adj[h] or len(adj[a]) - 1 < mindeg or len(adj[b]) - 1 < mindeg or a in H or b in H: continue
            adj[a].discard(b); adj[b].discard(a); adj[h].add(x); adj[x].add(h)
    return adj, H

def make(name):
    """ico<f> | flip<f>_<seed> (random min-deg-5 max-deg-9) | defect<f>_<seed> (degrees 5..9, heavy) |
       hub<f>_<seed>_<deg> | binder:<name>"""
    if name.startswith('ico'): return icosphere(int(name[3:]))
    if name.startswith('flip'):
        f, s = name[4:].split('_'); a = icosphere(int(f)); return flips(a, 3*len(a), random.Random(int(s)), 5, 9)
    if name.startswith('defect'):
        f, s = name[6:].split('_'); a = icosphere(int(f)); return flips(a, len(a)//3, random.Random(int(s)), 5, 9)
    if name.startswith('hub'):
        f, s, d = name[3:].split('_'); a = icosphere(int(f)); rng = random.Random(int(s))
        a = flips(a, len(a), rng, 5, 8); return hubs(a, 3, int(d), rng)[0]
    if name.startswith('binder:'):
        import pickle; return [set(s) for s in pickle.load(open('/mnt/project-files/multiscale/binder_maps/%s.pkl' % name[7:], 'rb'))]
    raise ValueError(name)

# ---------------- canonical ordering ----------------
def rotation(adj):
    n = len(adj); Gx = nx.Graph(); Gx.add_nodes_from(range(n))
    Gx.add_edges_from((u, w) for u in range(n) for w in adj[u] if u < w)
    ok, emb = nx.check_planarity(Gx); assert ok
    return [list(emb.neighbors_cw_order(v)) for v in range(n)], emb

def canonical(adj, rot, outer, policy='left', rng=None):
    """outer = (v1, v2, vn) a face. Returns (order, paths): order[0:3] = v1, v2, v3; for k >= 3 paths[k] is the
    attachment path of order[k] on the boundary of G_{k} (listed from the v1 side to the v2 side)."""
    v1, v2, vn = outer; n = len(adj)
    present = [True]*n; C = [v1, vn, v2]; onC = {v1, vn, v2}
    def cnb(x):
        i = C.index(x); a = C[i-1] if i > 0 else v2; b = C[i+1] if i+1 < len(C) else v1
        return a, b
    chord = collections.Counter()
    def recompute(x):
        a, b = cnb(x); chord[x] = sum(1 for y in adj[x] if present[y] and y in onC and y != a and y != b)
    for x in C: recompute(x)
    peeled = []; paths = {}; direction = None
    while sum(present) > 3:
        if policy == 'left': cand = next(x for x in C[1:-1] if chord[x] == 0)
        elif policy == 'right': cand = next(x for x in reversed(C[1:-1]) if chord[x] == 0)
        else: cand = rng.choice([x for x in C[1:-1] if chord[x] == 0])
        v = cand; j = C.index(v); pred, succ = C[j-1], C[j+1]; r = rot[v]; d = len(r)
        def arc(dr):
            i = r.index(pred); out = [pred]
            while out[-1] != succ: i = (i+dr) % d; out.append(r[i])
            return out
        if direction is None:
            a1, a2 = arc(1), arc(-1); direction = 1 if len(a1) > len(a2) else -1
        P = arc(direction)
        assert all(present[y] for y in P), 'arc contains removed vertex'
        assert set(y for y in adj[v] if present[y]) == set(P), 'neighbours not a single arc'
        present[v] = False; onC.discard(v); new = P[1:-1]
        C[j:j+1] = new; onC.update(new)
        aff = set(new) | {pred, succ}
        for u in new: aff |= set(y for y in adj[u] if present[y] and y in onC)
        for x in aff: recompute(x)
        chord.pop(v, None)
        peeled.append(v); paths[v] = P
    rest = [x for x in range(n) if present[x]]; v3 = next(x for x in rest if x not in (v1, v2))
    order = [v1, v2, v3] + peeled[::-1]
    return order, [None, None, None] + [paths[v] for v in peeled[::-1]]

# ---------------- boundary invariant ----------------
def _welzl(P):
    P = list(P); random.Random(0).shuffle(P)
    def c2(a, b): return ((a+b)/2, abs(a-b)/2)
    def c3(a, b, c):
        ax, ay, bx, by, cx, cy = a.real, a.imag, b.real, b.imag, c.real, c.imag
        d = 2*(ax*(by-cy)+bx*(cy-ay)+cx*(ay-by))
        if abs(d) < 1e-12: return max((c2(a, b), c2(a, c), c2(b, c)), key=lambda t: t[1])
        ux = ((ax*ax+ay*ay)*(by-cy)+(bx*bx+by*by)*(cy-ay)+(cx*cx+cy*cy)*(ay-by))/d
        uy = ((ax*ax+ay*ay)*(cx-bx)+(bx*bx+by*by)*(ax-cx)+(cx*cx+cy*cy)*(bx-ax))/d
        z = complex(ux, uy); return (z, abs(z-a))
    ins = lambda C, p: abs(C[0]-p) <= C[1]+1e-9
    C = (P[0], 0.0)
    for i, p in enumerate(P):
        if ins(C, p): continue
        C = (p, 0.0)
        for j, q in enumerate(P[:i]):
            if ins(C, q): continue
            C = c2(p, q)
            for r in P[:j]:
                if not ins(C, r): C = c3(p, q, r)
    return C

def mec(Z): return mecc(Z)[1]

def mecc(Z):
    Z = np.unique(np.round(Z, 9))
    if len(Z) <= 3: return _welzl(Z)
    try:
        h = ConvexHull(np.stack([Z.real, Z.imag], 1)); Z = Z[h.vertices]
    except Exception: pass
    return _welzl(Z)

def signs(B, degp):
    """gauge signs along boundary list B (cycle) given present degrees; returns (s array, odd_parity)."""
    k = np.array([degp[b] - 2 for b in B]); fl = np.where(k % 2 == 1, -1, 1)
    s = np.cumprod(np.concatenate([[1], fl[1:]]))
    closing = s[-1]*fl[0]
    return s, bool(closing != s[0])

def walk(B, s, colarr):
    lab = colarr ^ np.roll(colarr, -1)
    if (lab == 0).any(): return None
    inc = s*EV[lab]; H = np.concatenate([[0], np.cumsum(inc)]); return H

def pair(H, odd):
    """returns (ok, tau, |t|) : tau = tau_Hodge (even) or fixed-point radius (odd)."""
    L = len(H)-1
    if odd:
        q = (H[0]+H[-1])/2; r = float(np.max(np.abs(H-q))); return r <= TODD+1e-9, r, None
    t = H[-1]-H[0]; at = abs(t)
    if at > 2+1e-9: return False, None, at
    r = mec(H[:-1] - np.arange(L)/L*t); return r <= 1+1e-9, r, at

def eval_col(B, s, odd, col):
    H = walk(B, s, np.array([col[b] for b in B]))
    if H is None: return False, None, None
    return pair(H, odd)

def pair_cnf_even(enc, W, slack=0.036, delta=0.05):
    """necessary encoding of (|t|<=2 and tau_H<=1) for an even walk: H_0 = 0, H_i in Lambda one-hot (|H_i|<=4.2),
    selector over t in {0, +-2e} and centre p on a square grid of step delta: |H_i - (i/L)t - p| <= 1+slack.
    (any true solution satisfies it with slack >= delta/sqrt2; a solution of it has tau_H <= 1+slack)."""
    walk, sg = W['walk'], W['s']; m = len(walk); Ls = enc.labels(W)
    D = {1: (1, 0), 2: (0, 1), 3: (-1, -1)}; R0 = 4.2
    dom = [(a, b) for a in range(-6, 7) for b in range(-6, 7) if abs(a + b*W3) <= R0]; ds = set(dom)
    Hv = [{p: enc.new() for p in dom} for _ in range(m+1)]
    enc.cls.append([Hv[0][(0, 0)]])
    TR = enc.new(); enc.cls.append([TR])
    for i in range(m+1): enc.amo([Hv[i][p] for p in dom], TR)
    for i in range(m):
        for p in dom:
            for l in (1, 2, 3):
                q = (p[0] + sg[i]*D[l][0], p[1] + sg[i]*D[l][1])
                enc.cls.append([-Hv[i][p], -Ls[i][l], Hv[i+1][q]] if q in ds else [-Hv[i][p], -Ls[i][l]])
    zc = {p: p[0] + p[1]*W3 for p in dom}
    ts = [(0, 0), (2, 0), (-2, 0), (0, 2), (0, -2), (-2, -2), (2, 2)]
    sels = []; rr = 1 + slack; n = int(math.ceil(rr/delta))
    grid = [complex(a*delta, b*delta) for a in range(-n, n+1) for b in range(-n, n+1) if abs(complex(a*delta, b*delta)) <= rr]
    for t in ts:
        tz = t[0] + t[1]*W3
        if t not in ds: continue
        for pc in grid:
            sel = enc.new(); cl_ = []; ok = True
            for i in range(m):
                c = i/m*tz + pc
                A = [Hv[i][p] for p in dom if abs(zc[p] - c) <= rr + 1e-9]
                if not A: ok = False; break
                cl_.append([-sel] + A)
            if not ok: continue
            enc.cls.extend(cl_); enc.cls.append([-sel, Hv[m][t]]); sels.append(sel)
    enc.cls.append(sels)

# ---------------- induction ----------------
def ball(adjp, v, R):
    d = {v: 0}; q = collections.deque([v])
    while q:
        x = q.popleft()
        if d[x] >= R: continue
        for y in adjp(x):
            if y not in d: d[y] = d[x]+1; q.append(y)
    return d

class Inductor:
    def __init__(self, adj, order, paths, Rmax=6, policy='keep', seed=0, cap=300000, log=None):
        self.adj = adj; self.order = order; self.paths = paths; self.Rmax = Rmax; self.policy = policy
        self.rng = random.Random(seed); self.cap = cap
        n = len(adj); self.present = [False]*n; self.degp = [0]*n; self.col = {}
        a, b, c = order[:3]
        for x in (a, b, c): self.present[x] = True
        for x in (a, b, c): self.degp[x] = 2
        self.col = {a: 0, b: 1, c: 2}; self.B = [a, c, b]   # boundary as path v1 .. v2 (cycle)
        self.nodd = 0; self.recs = []; self.fail = None; self.verbose = False; self.dbg = None; self.enum_max = 8; self.cegar_max = 3000; self.node_cap = 400000; self.cand_cap = 20000; self.slack = 0.036; self.delta = 0.05

    def nb(self, x): return [y for y in self.adj[x] if self.present[y]]

    def score(self, r):
        ok, tau, at = r
        if self.policy == 'advtau': return -(tau or 0)
        if self.policy == 'advt': return (-(at or 0), -(tau or 0))
        return 0

    def step(self, k):
        v = self.order[k]; P = self.paths[k]; B = self.B
        ip = B.index(P[0]); iq = B.index(P[-1]); assert iq == ip + len(P) - 1, (ip, iq, len(P))
        B2 = B[:ip+1] + [v] + B[iq:]
        self.present[v] = True; self.degp[v] = len(P)
        for w in P: self.degp[w] += 1
        for w in P[1:-1]:
            assert self.degp[w] == len(self.adj[w])
            if len(self.adj[w]) % 2: self.nodd += 1
        s, odd = signs(B2, self.degp); assert odd == (self.nodd % 2 == 1), 'parity'
        pos = {b: i for i, b in enumerate(B2)}
        for R in range(0, self.Rmax+1):
            F = ball(self.nb, v, R); t0 = time.time(); res = self.solve(v, B2, pos, s, odd, F, R)
            if self.verbose: print('   R', R, '|F|', len(F), '|FB|', sum(1 for x in F if x in pos), 'ok' if res else 'no', round(time.time()-t0, 2), self.dbg, flush=True)
            if res is not None:
                newcol, (ok, tau, at), ncand, nsat = res
                nch = sum(1 for x in F if x != v and newcol[x] != self.col[x])
                self.col.update(newcol); self.B = B2
                rec = dict(k=k, n=k+1, L=len(B2), R=R, odd=odd, tau=round(tau, 4), t=None if at is None else round(at, 3),
                           degv=len(self.adj[v]), plen=len(P), nchanged=nch, ncand=ncand, nsat=nsat)
                self.recs.append(rec); return rec
        self.fail = dict(k=k, v=v, P=P, B=B2, s=s.tolist(), odd=odd, col=dict(self.col), nodd=self.nodd)
        return None

    def solve(self, v, B2, pos, s, odd, F, R):
        """exact: DFS over free boundary colours along the boundary (branch on t / reflection centre, prune by the
        pair on the partial walk), then SAT extension to free interior vertices (assumptions)."""
        col = self.col; L = len(B2); FBs = set(x for x in B2 if x in F); FI = [x for x in F if x not in pos]
        nbs = {x: self.nb(x) for x in F}
        if len(FBs) > self.enum_max: return self.solve_sat(v, B2, pos, s, odd, F, [x for x in B2 if x in FBs], nbs)
        # rotate so that index 0 is v (free); walk order b_0..b_{L-1}
        i0 = pos[v]; Bv = B2[i0:] + B2[:i0]; sv = np.concatenate([s[i0:], (-1 if odd else 1)*s[:i0]])
        # (rotation changes the gauge start; pair is base-point invariant up to the global sign of s)
        free = [x in FBs for x in Bv]
        allowed = {x: [c for c in range(4) if all(col[y] != c for y in nbs[x] if y not in F)] for x in FBs}
        for x in FBs:
            if x != v and col[x] in allowed[x]: allowed[x].remove(col[x]); allowed[x].insert(0, col[x])
        if odd: branches = [complex(a + b*W3) for a in range(-3, 4) for b in range(-3, 4) if abs(a + b*W3) <= 2+1e-9]
        else: branches = [0j] + [2*u*z for u in (1, -1) for z in (1, W3, W3*W3)]
        cands = []; nodes = [0]; ncap = self.node_cap; ccap = self.cand_cap
        assign = {}
        # suffix count of free edges (edges with a free endpoint) for reachability pruning
        fixedge = [not (free[i] or free[(i+1) % L]) for i in range(L)]
        inc = np.zeros(L, dtype=complex)
        for i in range(L):
            if fixedge[i]: inc[i] = sv[i]*EV[col[Bv[i]] ^ col[Bv[(i+1) % L]]]
        Cf = np.concatenate([[0], np.cumsum(inc)])
        runend = [0]*L; j = L
        for i in range(L-1, -1, -1):
            if not fixedge[i]: j = i
            runend[i] = j if fixedge[i] else i
        def dfs(i, H, pts, br, circ=(0j, 0.0)):
            # H = height at b_i; pts = detrended points so far (list of complex); i = next index to place (b_i coloured)
            nodes[0] += 1
            if nodes[0] > ncap or len(cands) >= ccap: return
            if i == L:
                # closing: H is H_L
                if odd:
                    if abs(H - br) > 1e-9: return
                else:
                    if abs(H - br) > 1e-9: return
                cands.append(dict(assign)); return
            x = Bv[i]; y = Bv[(i+1) % L]
            if fixedge[i]:
                j = runend[i]; ks = np.arange(i+1, j+1); Hk = H + (Cf[ks] - Cf[i])
                if odd:
                    inner = Hk[ks < L]
                    if len(inner) and np.max(np.abs(inner - br/2)) > TODD+1e-9: return
                    p2 = pts
                    c2 = circ
                else:
                    inner = (Hk - ks/L*br)[ks < L]; c2 = circ
                    if len(inner) and np.max(np.abs(inner - circ[0])) > circ[1] + 1e-9:
                        p2 = pts + list(inner)
                        if len(p2) > 6:
                            Z = np.array(p2)
                            try: h = ConvexHull(np.stack([Z.real, Z.imag], 1)); p2 = list(Z[h.vertices])
                            except Exception: pass
                        c2 = mecc(np.array(p2))
                        if c2[1] > 1+1e-9: return
                    else: p2 = pts
                dfs(j, Hk[-1], p2, br, c2); return
            if i == L-1: ys = [assign[y]]
            elif y in FBs: ys = [c for c in allowed[y] if all(assign.get(z) != c for z in nbs[y] if z in FBs)]
            else: ys = [col[y]]
            for cy in ys:
                cx = assign[x] if x in FBs else col[x]
                if cy == cx: continue
                H2 = H + sv[i]*EV[cx ^ cy]
                c2 = circ
                if i+1 < L:
                    if odd:
                        if abs(H2 - br/2) > TODD+1e-9: continue
                        p2 = pts
                    else:
                        p = H2 - (i+1)/L*br
                        if abs(p - circ[0]) > circ[1] + 1e-9:
                            p2 = pts + [p]
                            if len(p2) > 12:
                                Z = np.array(p2)
                                try: h = ConvexHull(np.stack([Z.real, Z.imag], 1)); p2 = list(Z[h.vertices])
                                except Exception: pass
                            c2 = mecc(np.array(p2))
                            if c2[1] > 1+1e-9: continue
                        else: p2 = pts
                else: p2 = pts
                newly = y in FBs and i+1 < L
                if newly: assign[y] = cy
                dfs(i+1, H2, p2, br, c2)
                if newly: del assign[y]
        for br in branches:
            for c in allowed[v]:
                assign[v] = c
                dfs(0, 0j, [] if odd else [0j], br)
                del assign[v]
        self.dbg = ('cands', len(cands), 'nodes', nodes[0])
        if nodes[0] > ncap: raise RuntimeError('node cap R=%d |FB|=%d' % (R, len(FBs)))
        if not cands: return None
        # exact evaluation, policy ordering
        ev = []
        for a in cands:
            c2 = dict(col); c2.update(a); r = eval_col(B2, s, odd, c2)
            assert r[0], ('dfs/eval mismatch', r)
            ev.append((a, r))
        if self.policy == 'keep': ev.sort(key=lambda e: sum(1 for x in FBs if x != v and e[0][x] != col[x]))
        elif self.policy == 'rand': self.rng.shuffle(ev)
        else: ev.sort(key=lambda e: self.score(e[1]))
        if not FI:
            a, r = ev[0]; return a, r, len(ev), 0
        ix = {x: i for i, x in enumerate(F)}; X = lambda x, c: 4*ix[x]+c+1; cls = []
        for x in F:
            cls.append([X(x, c) for c in range(4)])
            for a_, b_ in itertools.combinations(range(4), 2): cls.append([-X(x, a_), -X(x, b_)])
            for y in nbs[x]:
                if y in F:
                    if ix[y] > ix[x]:
                        for c in range(4): cls.append([-X(x, c), -X(y, c)])
                else: cls.append([-X(x, col[y])])
        S = Cadical153(bootstrap_with=cls); nsat = 0
        try:
            for a, r in ev:
                nsat += 1
                if S.solve(assumptions=[X(x, a[x]) for x in FBs]):
                    m = set(l for l in S.get_model() if l > 0)
                    out = {x: next(c for c in range(4) if X(x, c) in m) for x in F}
                    return out, r, len(ev), nsat
            if len(cands) >= ccap: raise RuntimeError('cand cap with no extension')
            return None
        finally: S.delete()

    def solve_sat(self, v, B2, pos, s, odd, F, FB, nbs):
        """SAT on F (all else fixed) with a necessary lattice relaxation of the pair (ic.Enc, exact in the odd
        case), CEGAR on the free boundary colours with the exact pair check."""
        sys.dont_write_bytecode = True; sys.path.insert(0, '/mnt/project-files/multiscale/intrinsic'); import ic
        col = self.col; V = sorted(set(F) | set(B2)); enc = ic.Enc(V)
        for x in V:
            if x not in F: enc.fix(x, col[x])
        X = enc.x
        for x in F:
            for y in nbs[x]:
                if y in F:
                    if y > x: enc.neq(x, y)
                else: enc.cls.append([-X(x, col[y])])
        W = dict(walk=list(B2), s=[int(z) for z in s], odd=odd)
        if odd: enc.walk_int(W, TODD)
        else: pair_cnf_even(enc, W, self.slack, self.delta)
        S = Cadical153(bootstrap_with=enc.cls); it = 0
        try:
            while it < self.cegar_max:
                it += 1
                if not S.solve(): self.dbg = ('cegar_unsat', it); return None
                m = set(l for l in S.get_model() if l > 0)
                out = {x: next(c for c in range(4) if X(x, c) in m) for x in F}
                c2 = dict(col); c2.update(out); r = eval_col(B2, s, odd, c2)
                if r[0]: self.dbg = ('cegar_ok', it); return out, r, -1, it
                if self.verbose and it < 3: print('    cegar reject', r, ic.tau_int(W, c2), ic.tau_walk(W, c2), flush=True)
                S.add_clause([-X(x, out[x]) for x in FB])
            self.dbg = ('cegar_cap', it); raise RuntimeError('cegar cap')
        finally: S.delete()

    def run(self, verbose=False):
        for k in range(3, len(self.order)):
            if self.step(k) is None: return False
        return True

def check_proper(adj, col):
    return all(col[u] != col[w] for u in range(len(adj)) for w in adj[u])
