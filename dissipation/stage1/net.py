# Stage 1 dissipation network: index structures and the EXACT integer evaluator on the 5/6/7 world.
#
# Model (charge unit: degree-d vertex starts with 60(6-d)):
#   round 1 (push): every u of degree 5 or 6 sends P[du, dv, {x,y}, n5(u)] to each neighbour v of degree >= 6, where {x,y} is the
#           unordered pair of degrees of the two common neighbours of u and v and n5(u) the number of 5s around u.
#   round 2 (forward): every 7 u with c1(u) > theta sends c1(u) - theta to its degree-7 neighbours, split equally over the slots
#           whose integer score is within margin m of the best score (shares 1, 1/2, 1/3, ...). Scores are integer weights over
#           mirror-symmetric bits of the slot's visible context in u's own row (ring neighbours, hats, outer link, far hats).
#   Final charge of a 7 X = min(c1(X), theta) [or c1(X) if X has no 7 neighbour] + sum over 7-neighbours u of fwd(u -> X).
#
# Reach (soundness): fwd(u -> X) depends on u's own row (link + hats), one ring further than X's row. We bound it from above by
# the MAXIMUM of fwd over every ADMISSIBLE degree-7 row of u (all 14 orientations) that agrees with everything X's row shows of
# u's row ("view": u's two link neighbours beside X, u's link vertices two away = X's hats, the hats of u beside X = X's link
# vertices two away, and u's hat across (w_{i+1}, s_i) when w_{i+1} = 5 [= s_{i+1}], mirrored). Hidden letters of link 6s
# (the vertex opposite the centre) are maximised over the letters that keep that 6-link admissible. If no admissible row of u
# fits the view, X cannot occur in a kill-free map and its row is excused. Everything below is conservative: each row's value
# is an upper bound on the true final charge of that vertex in any kill-free 5/6/7 triangulation.
import numpy as np, itertools, collections
import rows as RW
LET = (5, 6, 7)
PAIR = {}
for a in LET:
    for b in LET: PAIR[(a, b)] = sorted([(x, y) for x in LET for y in LET if x <= y]).index(tuple(sorted((a, b))))
NPAR = 2 * 2 * 6 * 7; ZERO = NPAR
def pidx(du, dv, x, y, n5): return (((du - 5) * 2 + (dv - 6)) * 6 + PAIR[(x, y)]) * 7 + n5
SCALE = 420   # lcm(1..7): shares 1/k exact

def view_X(w, s, i):
    d = len(w); W = lambda k: w[k % d]; S = lambda k: s[k % d]
    return (W(i + 1), W(i - 1), S(i), S(i - 1), W(i + 2), W(i - 2), S(i + 1) if W(i + 1) == 5 else 0, S(i - 2) if W(i - 1) == 5 else 0)
def view_R(w, s, j):
    d = len(w); W = lambda k: w[k % d]; S = lambda k: s[k % d]
    return (W(j + 1), W(j - 1), W(j + 2), W(j - 2), S(j), S(j - 1), S(j + 1) if W(j + 1) == 5 else 0, S(j - 2) if W(j - 1) == 5 else 0)
def reflect(w, s):
    d = len(w); return tuple(w[(-i) % d] for i in range(d)), tuple(s[(-i - 1) % d] for i in range(d))
def sides(w, s, j):
    d = len(w); W = lambda k: w[k % d]; S = lambda k: s[k % d]
    return tuple(sorted([(W(j + 1), S(j), W(j + 2), S(j + 1)), (W(j - 1), S(j - 1), W(j - 2), S(j - 2))]))

# ---------------- attention features (mirror symmetric, per context = unordered pair of side tuples) ----------------
POSN = ['ring', 'hat', 'outer', 'farhat']
def base_bits(ctx):
    a, b = ctx; out = []
    for p in range(4):
        n5 = (a[p] == 5) + (b[p] == 5); n7 = (a[p] == 7) + (b[p] == 7)
        out += [n5 >= 1, n5 == 2, n7 >= 1, n7 == 2]
    return out
BASE_NAMES = ['%s:%s' % (p, q) for p in POSN for q in ('5>=1', '5=2', '7>=1', '7=2')]
SIDE2 = sorted({tuple(sorted([x, y])) for x in itertools.product(LET, LET) for y in itertools.product(LET, LET)})   # (ring, hat) side types
SIDE3 = sorted({tuple(sorted([x, y])) for x in itertools.product(LET, LET, LET) for y in itertools.product(LET, LET, LET)})
def feat_names():
    n = list(BASE_NAMES)
    n += ['%s&%s' % (BASE_NAMES[i], BASE_NAMES[j]) for i in range(16) for j in range(i + 1, 16)]
    n += ['side2=%s' % (t,) for t in SIDE2] + ['side3=%s' % (t,) for t in SIDE3]
    return n
def ctx_feats(ctx):
    b = base_bits(ctx); f = list(b)
    f += [b[i] and b[j] for i in range(16) for j in range(i + 1, 16)]
    s2 = tuple(sorted([ctx[0][:2], ctx[1][:2]])); s3 = tuple(sorted([ctx[0][:3], ctx[1][:3]]))
    f += [s2 == t for t in SIDE2] + [s3 == t for t in SIDE3]
    return np.array(f, dtype=bool)

def build(R7, W5, W6, adm=True):
    """R7: list of (w, s) degree-7 rows (canonical); W5 / W6: admissible 5- / 6-links (canonical).
    adm=False: no admissibility filtering of hidden letters (used by the torus self-test)."""
    W5set = {RW.canon(w) for w in W5} if adm else None; W6set = {RW.canon(w) for w in W6} if adm else None
    ok5 = (lambda l: RW.canon(l) in W5set) if adm else (lambda l: True)
    ok6 = (lambda l: RW.canon(l) in W6set) if adm else (lambda l: True)
    N = len(R7)
    P7 = np.full((N, 7, 4), ZERO, dtype=np.int32); is7 = np.zeros((N, 7), bool)
    vX = np.full((N, 7), -1, dtype=np.int64); cX = np.full((N, 7), -1, dtype=np.int64)
    views = {}; ctxs = {}; srow, sslot, sview = [], [], []
    def vid(v):
        if v not in views: views[v] = len(views)
        return views[v]
    def cid(c):
        if c not in ctxs: ctxs[c] = len(ctxs)
        return ctxs[c]
    for r, (w, s) in enumerate(R7):
        d = 7; W = lambda k: w[k % d]; S = lambda k: s[k % d]
        for k in range(7):
            if w[k] == 5:
                n5 = sum(x == 5 for x in (W(k + 1), S(k), S(k - 1), W(k - 1)))
                P7[r, k, :] = pidx(5, 7, W(k - 1), W(k + 1), n5)
            elif w[k] == 6:
                n5b = sum(x == 5 for x in (W(k + 1), S(k), S(k - 1), W(k - 1)))
                c = sorted({pidx(6, 7, W(k - 1), W(k + 1), n5b + (p == 5)) for p in LET if ok6((7, W(k + 1), S(k), p, S(k - 1), W(k - 1)))})
                if not c: c = [ZERO]   # cannot happen for admissible rows
                P7[r, k, :] = (c * 4)[:4]
            else:
                is7[r, k] = True; vX[r, k] = vid(view_X(w, s, k)); cX[r, k] = cid(sides(w, s, k))
        for (ww, ss), refl in (((w, s), False), (reflect(w, s), True)):
            for j in range(7):
                if ww[j] != 7: continue
                srow.append(r); sslot.append((-j) % 7 if refl else j); sview.append(vid(view_R(ww, ss, j)))
    # 5-rows
    P5 = np.full((len(W5), 5), ZERO, dtype=np.int32)
    for r, w in enumerate(W5):
        n5 = sum(x == 5 for x in w)
        for k in range(5):
            if w[k] >= 6: P5[r, k] = pidx(5, w[k], w[(k - 1) % 5], w[(k + 1) % 5], n5)
    # 6-rows: out pushes exact, in pushes maximised over admissible links of the pushing neighbour
    O6 = np.full((len(W6), 6), ZERO, dtype=np.int32); I6 = np.full((len(W6), 6, 4), ZERO, dtype=np.int32)
    for r, L in enumerate(W6):
        n5 = sum(x == 5 for x in L); Lk = lambda k: L[k % 6]
        for k in range(6):
            a, b = Lk(k - 1), Lk(k + 1)
            if L[k] >= 6: O6[r, k] = pidx(6, L[k], a, b, n5)
            if L[k] == 5:
                c = sorted({pidx(5, 6, a, b, sum(x == 5 for x in (a, b, p, q))) for p in LET for q in LET if ok5((6, b, p, q, a))})
            elif L[k] == 6:
                c = sorted({pidx(6, 6, a, b, sum(x == 5 for x in (a, b, p, q, t))) for p in LET for q in LET for t in LET if ok6((6, b, p, q, t, a))})
            else: continue
            if not c: c = [ZERO]
            I6[r, k, :] = (c * 4)[:4]
    cl = [None] * len(ctxs)
    for c, i in ctxs.items(): cl[i] = c
    F = np.stack([ctx_feats(c) for c in cl]) if cl else np.zeros((0, len(feat_names())), bool)
    srow = np.array(srow, dtype=np.int64); sslot = np.array(sslot, dtype=np.int64); sview = np.array(sview, dtype=np.int64)
    nview = len(views)
    vcount = np.bincount(sview, minlength=nview)
    order = np.argsort(sview, kind='stable')
    return dict(N=N, P7=P7, is7=is7, vX=vX, cX=cX, srow=srow[order], sslot=sslot[order], sview=sview[order], nview=nview,
                vcount=vcount, F=F, ctxs=cl, P5=P5, O6=O6, I6=I6, views=views, has7=is7.any(1))

def excused_rows(B):
    """7-rows with a 7-slot whose view no admissible row of the neighbour matches (cannot occur in a kill-free map)."""
    bad = np.zeros(B['N'], bool)
    m = B['is7']; vv = np.where(m, B['vX'], 0)
    bad |= (m & (B['vcount'][vv] == 0)).any(1)
    return bad

# ---------------- exact integer evaluation ----------------
def exact(B, P, theta, Wt, margin, live=None):
    """P: int array (NPAR,), multiples of 3 not required; theta int; Wt int array (nfeat,); margin int >= 0.
    Returns dict with final charges (as Fractions-scaled integers, unit 1/SCALE) for 7-, 5- and 6-rows."""
    Pf = np.concatenate([np.asarray(P, dtype=np.int64), [0]])
    c1 = -60 + Pf[B['P7']].max(2).sum(1)                                     # (N,) upper bound on round-1 charge
    sc_ctx = B['F'].astype(np.int64) @ np.asarray(Wt, dtype=np.int64)        # (nctx,)
    sc = np.where(B['is7'], sc_ctx[np.where(B['is7'], B['cX'], 0)], np.iinfo(np.int64).min // 4)
    mx = sc.max(1, keepdims=True); inS = B['is7'] & (sc >= mx - margin); k = np.maximum(inS.sum(1), 1)
    sur = np.where(B['has7'], np.maximum(c1 - theta, 0), 0)
    fwd = sur[:, None] * (SCALE // k)[:, None] * inS                          # (N,7) unit 1/SCALE
    vals = fwd[B['srow'], B['sslot']]
    M = np.zeros(B['nview'], dtype=np.int64)
    if len(vals):
        starts = np.flatnonzero(np.r_[True, B['sview'][1:] != B['sview'][:-1]])
        M[B['sview'][starts]] = np.maximum.reduceat(vals, starts)
    own = np.where(B['has7'], np.minimum(c1, theta), c1) * SCALE
    inc = np.where(B['is7'], M[np.where(B['is7'], B['vX'], 0)], 0).sum(1)
    f7 = own + inc
    f5 = (60 - Pf[B['P5']].sum(1)) * SCALE
    f6 = (-Pf[B['O6']].sum(1) + Pf[B['I6']].max(2).sum(1)) * SCALE
    return dict(f7=f7, f5=f5, f6=f6, c1=c1, sur=sur, M=M, inS=inS)
