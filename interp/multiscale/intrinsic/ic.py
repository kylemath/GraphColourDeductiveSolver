# Intrinsic (base-point-free) boundary tilt tau_int and its exact SAT encoding.
#   odd walk  : Hol = point reflection r_p;  tau_int = max_i |H_i - p|                     (p = reflection centre)
#   even, t!=0: Hol = T_t; tau_int = half-width of the narrowest strip parallel to t containing the lifted walk
#   even, t=0 : circumradius of the closed walk (centre in the half-lattice, as in levelling/wk.tau_walk)
# Heights in half-lattice units (lev.INC); Lambda-coordinates = half-lattice coords / 2.
import sys, math, itertools, collections
sys.path.insert(0, '/mnt/project-files/multiscale/hierarchy/weak'); sys.path.insert(0, '/mnt/project-files/multiscale/hierarchy')
sys.path.insert(0, '/mnt/project-files/multiscale/levelling')
from lev import INC, n2, domain
from wk import tau_walk
S3 = math.sqrt(3)
LAM = {1: (1, 0), 2: (0, 1), 3: (-1, -1)}          # labels in Lambda coordinates

def heights(W, col):
    walk, s = W['walk'], W['s']; m = len(walk); H = [(0, 0)]
    for i in range(m):
        l = col[walk[i]] ^ col[walk[(i+1) % m]]
        if l == 0: return None
        d = INC[l]; H.append((H[-1][0]+s[i]*d[0], H[-1][1]+s[i]*d[1]))
    return H

def tvec(W, col):
    H = heights(W, col)
    if H is None or W['odd']: return None
    return (H[-1][0]-H[0][0], H[-1][1]-H[0][1])

def tau_int(W, col):
    """evaluator (brute force on the walk)."""
    H = heights(W, col)
    if H is None: return 99.0
    if W['odd'] or H[-1] == H[0]: return tau_walk(W, col)
    t = (H[-1][0]-H[0][0], H[-1][1]-H[0][1])
    E = lambda p: ((p[0]-p[1]/2)/2, p[1]*S3/4)   # n2-consistent (e_g, e_h at 120 deg)
    tx, ty = E(t); nt = math.hypot(tx, ty); nx, ny = -ty/nt, tx/nt
    pr = [E(h)[0]*nx+E(h)[1]*ny for h in H]
    return (max(pr)-min(pr))/2

def drift(W, col):
    """extent of the lap along t (Euclidean), 0 for odd / t=0."""
    H = heights(W, col)
    if H is None or W['odd'] or H[-1] == H[0]: return 0.0
    t = (H[-1][0]-H[0][0], H[-1][1]-H[0][1]); E = lambda p: ((p[0]-p[1]/2)/2, p[1]*S3/4)   # n2-consistent (e_g, e_h at 120 deg)
    tx, ty = E(t); nt = math.hypot(tx, ty)
    pr = [(E(h)[0]*tx+E(h)[1]*ty)/nt for h in H]
    return max(pr)-min(pr)

def directions(dmax):
    """primitive d=(p,q) in Lambda coords, up to sign, |d| <= dmax."""
    out = []; R = int(2*dmax)+2
    for p in range(-R, R+1):
        for q in range(-R, R+1):
            if (p, q) == (0, 0) or math.gcd(p, q) != 1: continue
            if (p, q) < (0, 0) and (-p, -q) != (p, q): continue
            if p*p+q*q-p*q <= dmax*dmax+1e-9: out.append((p, q))
    return out

class Enc:
    """clause store; x(v,c) colour vars for vertex list V."""
    def __init__(self, V):
        self.V = list(V); self.ix = {v: i for i, v in enumerate(self.V)}; self.top = 4*len(self.V); self.cls = []
        for v in self.V:
            self.cls.append([self.x(v, c) for c in range(4)])
            for a, b in itertools.combinations(range(4), 2): self.cls.append([-self.x(v, a), -self.x(v, b)])
    def x(self, v, c): return 4*self.ix[v]+c+1
    def new(self): self.top += 1; return self.top
    def neq(self, u, w):
        for c in range(4): self.cls.append([-self.x(u, c), -self.x(w, c)])
    def fix(self, v, c): self.cls.append([self.x(v, c)])
    def labels(self, W):
        walk = W['walk']; m = len(walk); Ls = []
        for i in range(m):
            u, w = walk[i], walk[(i+1) % m]; L = {l: self.new() for l in (1, 2, 3)}
            for a in range(4):
                for b in range(4):
                    if a != b: self.cls.append([-self.x(u, a), -self.x(w, b), L[a ^ b]])
            Ls.append(L)
        return Ls
    def amo(self, lits, g):
        """at most one of lits, gated by literal g (clauses get -g)."""
        if len(lits) <= 4:
            for a, b in itertools.combinations(lits, 2): self.cls.append([-g, -a, -b])
            return
        prev = None
        for i, a in enumerate(lits):
            s = self.new()
            self.cls.append([-g, -a, s])
            if prev is not None:
                self.cls.append([-g, -prev, s]); self.cls.append([-g, -prev, -a])
            prev = s
    def track1(self, Ls, s, step, lo, hi, g, exact=False):
        """1-D track y_0 = 0, y_{i+1} = y_i + s_i*step[l_i], values in [lo,hi], gated by g. returns Y[i][v]."""
        m = len(Ls); vals = range(lo, hi+1)
        Y = [{v: self.new() for v in vals} for _ in range(m+1)]
        self.cls.append([-g, Y[0][0]])
        for i in range(m):
            for v in vals:
                for l in (1, 2, 3):
                    q = v + s[i]*step[l]
                    self.cls.append([-g, -Y[i][v], -Ls[i][l], Y[i+1][q]] if lo <= q <= hi else [-g, -Y[i][v], -Ls[i][l]])
        if exact:
            for i in range(m+1): self.amo([Y[i][v] for v in vals], g)
        return Y
    def track2(self, Ls, s, K2, g):
        """2-D track in the disc of radius^2 K2 (half-lattice), H_0 free, gated by g."""
        Dm = domain(K2); Ds = set(Dm); m = len(Ls)
        H = [{p: self.new() for p in Dm} for _ in range(m+1)]
        for i in range(m):
            for p in Dm:
                for l in (1, 2, 3):
                    d = INC[l]; q = (p[0]+s[i]*d[0], p[1]+s[i]*d[1])
                    self.cls.append([-g, -H[i][p], -Ls[i][l], H[i+1][q]] if q in Ds else [-g, -H[i][p], -Ls[i][l]])
        self.cls.append([-g] + [H[0][p] for p in Dm])
        for p, q in itertools.combinations(Dm, 2): self.cls.append([-g, -H[0][p], -H[0][q]])
        return H, Dm
    def walk_int(self, W, T, dmax=None, gcap=None, min_drift=None, force=None, tmax=None):
        """add 'tau_int(W) <= T'. dmax: max |d| of strip directions (default m/2: exact). gcap: range cap of the
        Lambda-coordinate tracks used to certify t != 0 (default m: exact). force: None | 'zero' | 'nonzero'.
        min_drift: (adversary) require max_i max(|a_i|,|b_i|) >= min_drift in the t != 0 branch (and forbid t = 0)."""
        m = len(W['walk']); s = W['s']; Ls = self.labels(W); K2 = T*T + 1e-9
        TRUE = self.new(); self.cls.append([TRUE])
        if W['odd']:
            H, Dm = self.track2(Ls, s, K2, TRUE)
            for p in Dm: self.cls.append([-H[m][p], H[0][(-p[0], -p[1])]] if (-p[0], -p[1]) in H[0] else [-H[m][p]])
            return
        if dmax is None: dmax = m/2
        if gcap is None: gcap = m
        z0 = self.new(); znz = self.new(); self.cls.append([z0, znz])
        if force == 'zero': self.cls.append([-znz])
        if force == 'nonzero' or min_drift: self.cls.append([-z0])
        # branch t = 0: circumradius <= T
        H, Dm = self.track2(Ls, s, K2, z0)
        for p in Dm:
            for q in Dm:
                if q != p: self.cls.append([-z0, -H[0][p], -H[m][q]])
        # branch t != 0: exact a,b tracks (Lambda coords) certify t != 0; one strip direction chosen
        G = min(gcap, m)
        A = self.track1(Ls, s, {l: LAM[l][0] for l in LAM}, -G, G, znz, exact=True)
        B = self.track1(Ls, s, {l: LAM[l][1] for l in LAM}, -G, G, znz, exact=True)
        self.cls.append([-znz, -A[m][0], -B[m][0]])
        if tmax is not None:   # |t| <= tmax (Euclidean; Lambda coords)
            for a in A[m]:
                for b in B[m]:
                    if a*a+b*b-a*b > tmax*tmax+1e-9: self.cls.append([-znz, -A[m][a], -B[m][b]])
        if min_drift:
            self.cls.append([-znz] + [Y[i][v] for Y in (A, B) for i in range(m+1) for v in Y[i] if abs(v) >= min_drift])
        zs = []
        for (p, q) in directions(dmax):
            nd = math.sqrt(p*p+q*q-p*q); Bd = int(math.floor(4*T*nd/S3 + 1e-9))
            z = self.new(); zs.append(z); self.cls.append([-z, znz])
            step = {l: p*LAM[l][1]-q*LAM[l][0] for l in LAM}
            Y = self.track1(Ls, s, step, -Bd, Bd, z)
            for v in Y[m]:
                if v != 0: self.cls.append([-z, -Y[m][v]])
            seen = {v: self.new() for v in range(-Bd, Bd+1)}
            for i in range(m+1):
                for v in Y[i]: self.cls.append([-z, -Y[i][v], seen[v]])
            for v1 in range(-Bd, Bd+1):
                for v2 in range(v1+Bd+1, Bd+1): self.cls.append([-z, -seen[v1], -seen[v2]])
        self.cls.append([-znz] + zs)

def solve(enc, budget=None, seed=None, solver='cadical', assumptions=()):
    from pysat.solvers import Cadical153, Glucose4
    import random
    if solver == 'cadical' and seed is None and not budget:
        s = Cadical153(bootstrap_with=enc.cls); ok = s.solve(assumptions=list(assumptions))
    else:
        s = Glucose4(bootstrap_with=enc.cls)
        if seed is not None:
            rng = random.Random(seed); s.set_phases([(4*i+c+1)*(1 if rng.random() < 0.25 else -1) for i in range(len(enc.V)) for c in range(4)])
        if budget: s.conf_budget(budget); ok = s.solve_limited(assumptions=list(assumptions))
        else: ok = s.solve(assumptions=list(assumptions))
    if ok is None: s.delete(); return 'UNK'
    res = None
    if ok:
        mod = set(l for l in s.get_model() if l > 0)
        res = {v: next(c for c in range(4) if enc.x(v, c) in mod) for v in enc.V}
    s.delete(); return res

def sat_disc(D, walks, T, fixed=None, dmax=None, gcap=None, budget=None, seed=None, force=None, min_drift=None, symbreak=True, tmax=None):
    """proper colouring of Disc D with tau_int <= T on every walk in walks."""
    enc = Enc(sorted(D.S))
    for u, w in D.edges:
        if fixed and u in fixed and w in fixed: continue
        enc.neq(u, w)
    if fixed:
        for v, c in fixed.items():
            if v in enc.ix: enc.fix(v, c)
    elif symbreak:
        f = D.g.faces[next(iter(D.tris))]
        for j in range(3): enc.fix(f[j], j)
    for W in walks: enc.walk_int(W, T, dmax=dmax, gcap=gcap, force=force, min_drift=min_drift, tmax=tmax)
    return solve(enc, budget=budget, seed=seed)

def _mec(P):
    """minimal enclosing circle radius (Welzl, iterative randomised)."""
    import random
    P = list(set(P)); random.Random(0).shuffle(P)
    def c2(a, b): return ((a[0]+b[0])/2, (a[1]+b[1])/2, math.dist(a, b)/2)
    def c3(a, b, c):
        ax, ay = a; bx, by = b; cx, cy = c; d = 2*(ax*(by-cy)+bx*(cy-ay)+cx*(ay-by))
        if abs(d) < 1e-12: return max((c2(a, b), c2(a, c), c2(b, c)), key=lambda t: t[2])
        ux = ((ax*ax+ay*ay)*(by-cy)+(bx*bx+by*by)*(cy-ay)+(cx*cx+cy*cy)*(ay-by))/d
        uy = ((ax*ax+ay*ay)*(cx-bx)+(bx*bx+by*by)*(ax-cx)+(cx*cx+cy*cy)*(bx-ax))/d
        return (ux, uy, math.dist((ux, uy), a))
    inside = lambda C, p: math.dist((C[0], C[1]), p) <= C[2]+1e-9
    C = (P[0][0], P[0][1], 0)
    for i, p in enumerate(P):
        if inside(C, p): continue
        C = (p[0], p[1], 0)
        for j, q in enumerate(P[:i]):
            if inside(C, q): continue
            C = c2(p, q)
            for r in P[:j]:
                if not inside(C, r): C = c3(p, q, r)
    return C[2]

def tau_hodge(W, col):
    """reviewer's Hodge-detrended tau for even walks: circumradius (continuous) of {H_i - (i/m) t}, i=0..m-1.
    odd walks: fixed-point radius (= tau_int)."""
    H = heights(W, col)
    if H is None: return 99.0
    if W['odd']: return tau_walk(W, col)
    m = len(W['walk']); t = (H[-1][0]-H[0][0], H[-1][1]-H[0][1])
    E = lambda p: ((p[0]-p[1]/2)/2, p[1]*S3/4)
    return _mec([E((H[i][0]-i*t[0]/m, H[i][1]-i*t[1]/m)) for i in range(m)])
