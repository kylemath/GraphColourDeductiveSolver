# Adversarial merges for step (a_W): hand-built pairs (A,B), several weakly level colourings per side
# (random phases, forced |t|=2 where possible), ALL 24 renamings, exact min R, then exact min collar width w.
import sys, os, json, time, random, collections, itertools, math
sys.path.insert(0, '/mnt/project-files/multiscale/hierarchy/weak'); sys.path.insert(0, '/mnt/project-files/multiscale/hierarchy')
sys.path.insert(0, '/mnt/project-files/multiscale/levelling')
from wk import Disc, tau_walk, proper_repair_at, G, check
from lev import INC, n2, domain, multi_bfs, PERMS, bfs
from e1_hier import make
from pysat.solvers import Cadical153, Glucose4

def sat2(D, walks, K2, fixed=None, budget=3*10**6, phases=None, force_t=None, seed=None, big_walk=None):
    """big_walk=(W, K2big, minT2): also track walk W in a domain of radius^2 K2big and require |H_m-H_0|^2 >= minT2."""
    """as wk.sat, plus: phases (random seed), force_t: 'zero' | 'nonzero' applied to every EVEN walk."""
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
        elif force_t == 'zero':
            for p in Dm: cls.append([-H[0][p], H[m][p]])
        elif force_t == 'nonzero':
            for p in Dm: cls.append([-H[0][p], -H[m][p]])
    if big_walk:
        W, Kb, mT = big_walk; Db = domain(Kb); Dbs = set(Db); walk, s = W['walk'], W['s']; m = len(walk)
        H = [{p: new() for p in Db} for _ in range(m+1)]
        for i in range(m):
            u, w = walk[i], walk[(i+1) % m]; L = {l: new() for l in (1, 2, 3)}
            for a in range(4):
                for b in range(4):
                    if a != b: cls.append([-x(u, a), -x(w, b), L[a ^ b]])
            for p in Db:
                for l in (1, 2, 3):
                    d = INC[l]; q = (p[0]+s[i]*d[0], p[1]+s[i]*d[1])
                    cls.append([-H[i][p], -L[l], H[i+1][q]] if q in Dbs else [-H[i][p], -L[l]])
        cls.append([H[0][(0, 0)]])
        for q in Db:
            if n2(q) < mT - 1e-9: cls.append([-H[m][q]])
    s_ = Glucose4(bootstrap_with=cls)
    if seed is not None:
        rng = random.Random(seed); s_.set_phases([(4*i+c+1)*(1 if rng.random() < 0.25 else -1) for i in range(len(V)) for c in range(4)])
    if budget: s_.conf_budget(budget); ok = s_.solve_limited()
    else: ok = s_.solve()
    if ok is None: s_.delete(); return 'UNK'
    res = None
    if ok:
        mod = set(l for l in s_.get_model() if l > 0)
        res = {v: next(c for c in range(4) if x(v, c) in mod) for v in V}
    s_.delete(); return res

def tvec(W, col):
    walk, s = W['walk'], W['s']; m = len(walk); H = (0, 0)
    for i in range(m):
        l = col[walk[i]] ^ col[walk[(i+1) % m]]
        if l == 0: return None
        d = INC[l]; H = (H[0]+s[i]*d[0], H[1]+s[i]*d[1])
    return None if W['odd'] else math.sqrt(n2(H))

def merge_all24(g, D, A, B, colA, colB, Rmax=6, wmax=6):
    seam = [(u, w) for (u, w) in D.edges if (u in A) != (w in A)]
    data = []
    for p in PERMS:
        cc = {v: colA[v] for v in A}; cc.update({v: p[colB[v]] for v in B})
        K = set(x for e in seam if cc[e[0]] == cc[e[1]] for x in e)
        data.append((len(K), p, cc, K))
    data.sort(key=lambda t: t[0])
    R = None; nR = 0
    for RR in range(Rmax+1):
        for nk, p, cc, K in data:
            if not K: r, c2 = 0, cc
            else: r, c2 = proper_repair_at(g, D.S, cc, K, RR)
            if r is not None:
                if R is None: R, cR, glued = RR, c2, cc
                nR += 1
        if R is not None: break
    if R is None: return dict(R=None)
    zone = set(v for v in D.S if cR[v] != glued[v])
    ptau_before = max(tau_walk(W, cR) for W in D.pockets)
    dB = multi_bfs(g.adj, list(D.bset), D.S)
    w = None; wc = None   # w: collar + repair zone free (wk convention);  wc: collar only
    for ww in range(wmax+1):
        if ww == 0 and ptau_before <= 1+1e-9: w = 0; wc = 0; break
        if wc is None:
            fx = {v: cR[v] for v in D.S if dB[v] > ww}
            r = sat2(D, D.pockets, 1.0, fixed=fx)
            if r not in (None, 'UNK'): wc = ww; c3 = r
            elif r == 'UNK': wc = 'UNK%d' % ww
        if w is None:
            fx = {v: cR[v] for v in D.S if dB[v] > ww and v not in zone}
            r = sat2(D, D.pockets, 1.0, fixed=fx)
            if r not in (None, 'UNK'): w = ww; c3 = r
            elif r == 'UNK': w = 'UNK%d' % ww
        if w is not None and wc is not None: break
    seamP = len(set(j for j, W in enumerate(D.pockets) for e in seam if e[0] in W['walk'] and e[1] in W['walk']))
    return dict(R=R, nR=nR, nconf=data[0][0], w=w, wc=wc, ptau_before=round(ptau_before, 3), strict_tau_before=round(tau_walk(D.whole, cR), 3),
                seam_len=len(seam), seam_pockets=seamP, chords=len(D.chords), pockets=len(D.pockets), mU=len(D.whole['walk']),
                tA=[tvec(W, colA) for W in Disc(g, A).pockets], tB=[tvec(W, colB) for W in Disc(g, B).pockets])

def ball(g, c, r): return set(bfs(g.adj, c, r))

def level_cols(g, S, k, force=None, seed0=0, budget=5*10**6):
    D = Disc(g, S); out = []
    for s in range(k):
        r = sat2(D, D.pockets, 1.0, force_t=force, seed=seed0+s, budget=budget)
        if r not in (None, 'UNK'): out.append(r)
        elif r is None: break
    return out
