# s44 control (b): physical test of the fb key (RELAY_SPEC_s44 44.1-44.2).  Explicit rotation systems around u (s43's
# builder: link, apexes, privates, apex rotations with shared fresh vertices).  For every link vertex X of degree >= 6:
#   (I) an INDEPENDENT key from vertex identities: c = common nbr of u, X; a = common nbr of X, c other than u;
#       b = common nbr of u, c other than X; e = common nbr of c, a other than X (only if deg c = 5) -- each read from any
#       rotation holding the pair (all such readings must agree);
#   (P) the engine's payer key fb_payer_keys(d, w, s) on u's row in a random rotation / orientation;
#   (Q) the engine's payee key fb_payee_at on X's own row (L = X's rotation, t = its apexes from rotations, unknown
#       apexes random), in a random rotation / orientation; for X = 6 also cons2_coef(L, t) must carry it.
# Broken control: the payee read with the payer's slot map (a and b swapped) must mismatch.
import sys, random, collections
NARG = int(sys.argv[1]) if len(sys.argv) > 1 else 50000
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
M = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
E = B + '/s44/eng'
sys.argv = [E + '/pcheck.py', 'none', 'apexcls', 'hat5', 'fb', 'root=' + M]
src = open(E + '/pcheck.py').read(); last = src.rstrip().rsplit('\n', 1)
G = {'__file__': E + '/pcheck.py', '__name__': 'pcheck_exec'}; exec(compile(last[0], E + '/pcheck.py', 'exec'), G)
assert G['FB'] and G['FBDIR'] == '67'
def build(rng, d):
    L = lambda: rng.choice((5, 6, 7, 8, 9))
    deg = {}; rot = {}
    U = min(d, 9); deg['u'] = U
    w = [rng.choice((5, 5, 5, 6, 6, 7, 8)) for _ in range(d)]
    s = [rng.choice((5, 5, 6, 7, 8, 9)) for _ in range(d)]
    for _ in range(rng.choice((0, 1, 1, 2))):   # plant faces
        i = rng.randrange(d); w[i] = w[(i + 1) % d] = 5; s[i] = 5
    W_ = ['w%d' % i for i in range(d)]; S_ = ['s%d' % i for i in range(d)]
    for i in range(d): deg[W_[i]] = w[i]; deg[S_[i]] = s[i]
    rot['u'] = list(W_)
    # w_i: u, w_{i+1}, s_i, [privates], s_{i-1}, w_{i-1}
    for i in range(d):
        pv = ['p%d_%d' % (i, k) for k in range(w[i] - 5)]
        for z in pv: deg[z] = L()
        rot[W_[i]] = ['u', W_[(i + 1) % d], S_[i]] + pv + [S_[(i - 1) % d], W_[(i - 1) % d]]
    # s_i: w_i, w_{i+1}, a, fresh..., b ; a = the nbr of w_{i+1} before s_i (s_{i+1} or w_{i+1}'s last private),
    # b = the nbr of w_i after s_i (s_{i-1} or w_i's first private)
    for i in range(d):
        a = rot[W_[(i + 1) % d]][-3]; b = rot[W_[i]][3]
        fr = ['f%d_%d' % (i, k) for k in range(s[i] - 4)]
        for z in fr: deg[z] = L()
        rot[S_[i]] = [W_[i], W_[(i + 1) % d], a] + fr + [b]
    # faces of the edges s_i s_{i+1} (present iff w_{i+1} = 5): the vertex after s_{i+1} in s_i's rotation is the vertex
    # before s_i in s_{i+1}'s rotation -> identify (union-find over fresh names)
    par = {}
    def fd(x):
        while par.get(x, x) != x: x = par[x]
        return x
    for i in range(d):
        if w[(i + 1) % d] == 5:
            x, y = fd(rot[S_[i]][3]), fd(rot[S_[(i + 1) % d]][-2])
            if x != y: par[y] = x
    for k in list(rot): rot[k] = [fd(z) for z in rot[k]]
    return d, w, s, deg, rot


def common(rot, x, y, excl):
    hs = set()
    for a, b in ((x, y), (y, x)):
        if a in rot and b in rot[a]:
            r = rot[a]; j = r.index(b); c1, c2_ = r[(j - 1) % len(r)], r[(j + 1) % len(r)]
            assert excl in (c1, c2_), (a, b, excl); hs.add(c2_ if c1 == excl else c1)
    assert len(hs) <= 1, hs
    return hs.pop() if hs else None
def ind_key(st, X):
    d, w, s, deg, rot = st
    Us = min(deg['u'], 9); sides = []
    for c in (rot['u'][(rot['u'].index(X) + 1) % d], rot['u'][(rot['u'].index(X) - 1) % d]):
        a = common(rot, X, c, 'u'); b = common(rot, 'u', c, X)
        e = common(rot, c, a, X) if deg[c] == 5 else None
        sides.append((deg[c], deg[a], deg[b], deg[e] if deg[c] == 5 else 0))
    if not any(T[0] == 5 and T[2] == 5 and T[3] == 5 for T in sides): return None
    return (Us, deg[X]) + min(sides) + max(sides)
def orient(L, t, rng):
    n = len(L); r = rng.randrange(n); refl = rng.random() < 0.5
    L2 = [None] * n; t2 = [None] * n
    for i in range(n):
        j = (i + r) % n if not refl else (r - i) % n; L2[j] = L[i]
        j2 = (i + r) % n if not refl else (r - i - 1) % n; t2[j2] = t[i]
    return L2, t2
def run(N, seed=44):
    rng = random.Random(seed); st_ = collections.Counter()
    for _ in range(N):
        d = rng.choice((7, 7, 8, 9)); st = build(rng, d); d, w, s, deg, rot = st
        # u's row in a random orientation, tracking which index is which X
        ids = ['w%d' % i for i in range(d)]; sl_ = list(s)
        wl, sl = orient(w, s, rng); idl, _ = orient(ids, s, random.Random(0))
        rr = rng.randrange(d); refl = rng.random() < 0.5
        Wx = [None] * d; Sx = [None] * d; Ix = [None] * d
        for i in range(d):
            j = (i + rr) % d if not refl else (rr - i) % d; Wx[j] = w[i]; Ix[j] = ids[i]
            j2 = (i + rr) % d if not refl else (rr - i - 1) % d; Sx[j2] = s[i]
        pay = dict(G['fb_payer_keys'](d, Wx, Sx))
        for j in range(d):
            X = Ix[j]
            if deg[X] < 6: continue
            K = ind_key(st, X); st_['pairs'] += 1; st_['face pairs'] += K is not None
            if pay.get(j) != K: st_['PAYER MISMATCH'] += 1
            # X's own row: link = rot[X], apexes from rotations (unknown -> random letter)
            L = [deg[z] for z in rot[X]]; n = len(L); t = []
            for m in range(n):
                a_ = common(rot, rot[X][m], rot[X][(m + 1) % n], X)
                t.append(deg[a_] if a_ is not None else rng.choice((5, 6, 7, 8, 9)))
            # orient and locate u
            r2 = rng.randrange(n); rf2 = rng.random() < 0.5; L2 = [None] * n; t2 = [None] * n; ku = None
            for i in range(n):
                jj = (i + r2) % n if not rf2 else (r2 - i) % n; L2[jj] = L[i]
                if rot[X][i] == 'u': ku = jj
                j2 = (i + r2) % n if not rf2 else (r2 - i - 1) % n; t2[j2] = t[i]
            Xl = min(deg[X], 9)
            Q = G['fb_payee_at'](n, L2, t2, Xl, ku) if Xl >= 6 else None
            if Q != K: st_['PAYEE MISMATCH'] += 1
            if Xl == 6 and K is not None:
                cf = G['cons2_coef'](tuple(L2), tuple(t2))
                if cf.get(('fb', K), 0) < 1: st_['CONS2 MISSING'] += 1
                st_['six payees'] += 1
            if Xl >= 7 and K is not None: st_['big payees'] += 1
            # broken: payee with the payer's slot map (a <-> b)
            e1, e2 = L2[(ku + 1) % n], L2[(ku - 1) % n]
            Tp = (e1, t2[ku], L2[(ku + 2) % n], t2[(ku + 1) % n] if e1 == 5 else 0); Tm = (e2, t2[(ku - 1) % n], L2[(ku - 2) % n], t2[(ku - 2) % n] if e2 == 5 else 0)
            Kb = G['fb_key'](L2[ku], Xl, Tp, Tm)
            if K is not None: st_['broken checked'] += 1; st_['broken mismatches'] += Kb != K
    return st_
st = run(NARG)
for k in sorted(st): print('%-20s %d' % (k, st[k]))
ok = not (st['PAYER MISMATCH'] or st['PAYEE MISMATCH'] or st['CONS2 MISSING'])
print('PHYS44:', 'PASS' if ok else 'FAIL', '(broken payee slot map: %d of %d face pairs mismatch)' % (st['broken mismatches'], st['broken checked']))
