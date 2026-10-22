# "Twist" construction.  For a renaming pi = (Q, T mod 2L) (Q in D3 permuting e_g, e_h, e_{g+h}; T a translation),
# a seam stretch S is pi-conflict-free with offset T when, on every seam edge b->a of S (b in B, a in A),
#     h_A(a) - (Q h_B(b) + T)  is the height increment of the glued colouring, i.e. lies in sgn(b->a) * {e_1,e_2,e_3}.
# Two such stretches S_L, S_R with offsets T_L != T_R (same class mod 2L) that stay connected through A \ Z and
# through B \ Z give a loop with height monodromy T_R - T_L != 0 in a flat disc: no repair avoiding that loop exists.
import itertools, random
from lat import INC, n2, solve, bfs, col_of_height, PERMS
from heights import ball_pts

E = [INC[1], INC[2], INC[3]]
def Qmat(sig):
    """linear map with Q e_l = e_sig(l) (sig a permutation of (1,2,3) given as tuple of images)."""
    a, b = INC[sig[0]], INC[sig[1]]
    return lambda p: ((p[0]*a[0] + p[1]*b[0])//2, (p[0]*a[1] + p[1]*b[1])//2)
QS = list(itertools.permutations((1, 2, 3)))
CLASSES = [(0, 0), (2, 0), (0, 2), (2, 2)]           # Lambda / 2Lambda representatives (half units)

def renaming(sig, T):
    Q = Qmat(sig); pi = [None]*4
    for c in CLASSES:
        pi[col_of_height(c)] = col_of_height(tuple(x+y for x, y in zip(Q(c), T)))
    return tuple(pi)

ALL = {}
for sig in QS:
    for T in CLASSES:
        ALL[renaming(sig, T)] = (sig, T)
assert len(ALL) == 24 and set(ALL) == set(PERMS)

def mod2(T): return ((T[0] // 2) % 2 * 2, (T[1] // 2) % 2 * 2)

def build(g, A, B, consA, consB, stretches, seed=0, slack=0, budget=None, tcands=3.0, cap=None, pocket_opts=None):
    """Heights for A and B jointly.  consA/consB: v -> allowed heights (pocket balls).  stretches: list of
       (edges [(a,b)...], sig, Tclass, group) ; stretches sharing a group get pairwise DIFFERENT offsets T (all in Tclass).
       Offsets are chosen by the solver among class members within distance tcands of the origin."""
    rng = random.Random(seed)
    S = set(A) | set(B); cons = dict(consA); cons.update(consB)
    # pocket_opts: list of (vertex list, [centre options]); vertex domains = union of option balls (intersected)
    if pocket_opts:
        for vs, opts in pocket_opts:
            U_ = set(p for c in opts for p in ball_pts(c, 1.0))
            for x in vs: cons[x] = cons[x] & U_ if x in cons else set(U_)
    d0 = bfs(g.adj, list(cons), S)
    allp = set(p for c in cons for p in cons[c]); cache = {}
    dom = {}
    for v in S:
        if v in cons: dom[v] = sorted(cons[v]); continue
        r = d0[v] + slack
        if cap is not None: r = min(r, cap)
        if r not in cache:
            R = int(r) + 1
            offs = [(2*a, 2*b) for a in range(-R, R+1) for b in range(-R, R+1) if n2((2*a, 2*b)) <= r*r + 1e-9]
            cache[r] = sorted(set((p[0]+o[0], p[1]+o[1]) for p in allp for o in offs))
        dom[v] = cache[r]
    var = {}; top = [0]
    def new(): top[0] += 1; return top[0]
    for v in sorted(S):
        for p in dom[v]: var[(v, p)] = new()
    cls = []
    for v in sorted(S):
        lits = [var[(v, p)] for p in dom[v]]; cls.append(lits); prev = None
        for i, x in enumerate(lits):
            if i == len(lits)-1:
                if prev: cls.append([-x, -prev])
                break
            s = new(); cls.append([-x, s])
            if prev: cls.append([-prev, s]); cls.append([-x, -prev])
            prev = s
    Aset = set(A); Bset = set(B)
    for u in sorted(S):
        for w in g.adj[u]:
            if w not in S or w < u: continue
            if (u in Aset) != (w in Aset): continue        # seam edges are not height edges
            sg = g.sgn(u, w)
            for (x, y, s_) in ((u, w, sg), (w, u, -sg)):
                for p in dom[x]:
                    nb = [var[(y, (p[0]+s_*e[0], p[1]+s_*e[1]))] for e in E if (y, (p[0]+s_*e[0], p[1]+s_*e[1])) in var]
                    cls.append([-var[(x, p)]] + nb)
    cvars = []
    for vs, opts in (pocket_opts or []):
        cv = {c: new() for c in opts}; cvars.append(cv); cls.append(list(cv.values()))
        for c1, c2 in itertools.combinations(opts, 2): cls.append([-cv[c1], -cv[c2]])
        for c, t in cv.items():
            bp = set(ball_pts(c, 1.0))
            for x in vs: cls.append([-t] + [var[(x, p)] for p in dom[x] if p in bp])
    groups = {}
    tvars = []
    for si, (edges, sig, Tc, grp) in enumerate(stretches):
        Q = Qmat(sig)
        R = int(tcands) + 2
        cands = [(Tc[0]+4*a, Tc[1]+4*b) for a in range(-R, R+1) for b in range(-R, R+1)
                 if n2((Tc[0]+4*a, Tc[1]+4*b)) <= tcands*tcands + 1e-9]
        tv = {T: new() for T in cands}; tvars.append(tv)
        cls.append(list(tv.values()))
        for T1, T2 in itertools.combinations(cands, 2): cls.append([-tv[T1], -tv[T2]])
        groups.setdefault(grp, []).append(si)
        for (a, b) in edges:
            sg = g.sgn(b, a)
            for T, t in tv.items():
                for q in dom[b]:
                    Qq = Q(q)
                    ok = [var[(a, (Qq[0]+T[0]+sg*e[0], Qq[1]+T[1]+sg*e[1]))] for e in E
                          if (a, (Qq[0]+T[0]+sg*e[0], Qq[1]+T[1]+sg*e[1])) in var]
                    cls.append([-t, -var[(b, q)]] + ok)
    for grp, sis in groups.items():
        for s1, s2 in itertools.combinations(sis, 2):
            for T in tvars[s1]:
                if T in tvars[s2]: cls.append([-tvars[s1][T], -tvars[s2][T]])
    perm = list(range(1, top[0]+1)); rng.shuffle(perm)
    cls2 = [[perm[abs(l)-1]*(1 if l > 0 else -1) for l in c] for c in cls]; rng.shuffle(cls2)
    r = solve(top[0], cls2, budget)
    if r is None or r == 'UNK': return r, None
    inv = {perm[i]: i+1 for i in range(top[0])}; tv_ = set(inv[x] for x in r)
    h = {v: next(p for p in dom[v] if var[(v, p)] in tv_) for v in S}
    Ts = [next(T for T, t in tvars[i].items() if t in tv_) for i in range(len(stretches))]
    build.centres = [next(c for c, t in cv.items() if t in tv_) for cv in cvars]
    return h, Ts

# ---------------------------------------------------------------- solver-free lower-bound certificate
def monodromy_obstruction(g, U, col, Z):
    """True iff the colouring col restricted to U \\ Z (which must be proper there) has a non-single-valued height
       on some connected component; then no recolouring of Z alone can make U properly coloured (U flat)."""
    rest = set(U) - set(Z); h = {}
    for s in rest:
        if s in h: continue
        h[s] = (0, 0); st = [s]
        while st:
            u = st.pop()
            for w in g.adj[u]:
                if w not in rest: continue
                l = col[u] ^ col[w]
                if l == 0: raise ValueError('improper edge outside Z')
                d = INC[l]; sg = g.sgn(u, w); hw = (h[u][0]+sg*d[0], h[u][1]+sg*d[1])
                if w in h:
                    if h[w] != hw: return True
                else: h[w] = hw; st.append(w)
    return False
