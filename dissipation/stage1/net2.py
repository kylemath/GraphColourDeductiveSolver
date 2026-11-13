# Stage 1 (c): three-round dissipation network on the 5/6/7 world, with hat-aware pushes.
#   R1 push : u of degree 5 or 6 sends P[key] to each neighbour v of degree >= 6. key = (deg u, deg v, unordered pair of the two
#             "sides" (x, h_x), (y, h_y)) [+ o = the vertex opposite v, if deg u = 6]. x, y = common neighbours of u, v; h_x = u's
#             other neighbour next to x. For a 5 this is its whole link; for a 6 its whole link. (Strictly richer than the n5 table.)
#   R2 fwd  : a 7 with c1 > th7 sends c1 - th7 to its neighbours of degree 6 or 7, equal split over the slots whose integer score
#             is within margin m2 of the best.
#   R3 fwd  : a 6 with c2 > th6 sends c2 - th6 to its 7-neighbours, equal split over the top slots (margin m3).
#   finals  : 7: min(c1, th7) + in2 + in3 [c1 + in2 + in3 if no target]; 6: min(c2, th6) [c2 if no 7 nbr]; 5: 60 - out.
# Rows: 7-rows = W16 pickle (link + hats), 6-rows = every 6 (link + hats) whose link is not R6 and whose link 5s / 6s pass R5 / R6,
# 5-rows = admissible 5-links. Reach: whatever a row receives by forwarding is bounded by the max over every admissible row of the
# sender (all orientations) that agrees with what the receiver sees of it ("view"); hidden letters maximised over admissible choices.
import numpy as np, itertools, collections
import rows as RW
LET = (5, 6, 7)
SIDES = [(a, b) for a in LET for b in LET]
SPAIR = sorted({tuple(sorted([x, y])) for x in SIDES for y in SIDES})
SPI = {p: i for i, p in enumerate(SPAIR)}           # 45
N5 = 2 * len(SPAIR); NPAR = N5 + 2 * len(SPAIR) * 3; ZERO = NPAR
def pkey(du, dv, sa, sb, o=None):
    p = SPI[tuple(sorted([sa, sb]))]
    if du == 5: return (dv - 6) * len(SPAIR) + p
    return N5 + ((dv - 6) * len(SPAIR) + p) * 3 + (o - 5)
def pname(i):
    if i < N5: dv, p = divmod(i, len(SPAIR)); return '5->%d %s' % (dv + 6, SPAIR[p])
    j = i - N5; q, o = divmod(j, 3); dv, p = divmod(q, len(SPAIR)); return '6->%d %s o=%d' % (dv + 6, SPAIR[p], o + 5)
SCALE = 25200   # 420 * 60: R2 shares 1/k (k <= 7) and R3 shares 1/k (k <= 6) of R2-sums stay integral

def view_recv(w, s, i):
    d = len(w); W = lambda k: w[k % d]; S = lambda k: s[k % d]
    return (W(i + 1), W(i - 1), S(i), S(i - 1), W(i + 2), W(i - 2), S(i + 1) if W(i + 1) == 5 else 0, S(i - 2) if W(i - 1) == 5 else 0)
def view_send(w, s, j):
    d = len(w); W = lambda k: w[k % d]; S = lambda k: s[k % d]
    return (W(j + 1), W(j - 1), W(j + 2), W(j - 2), S(j), S(j - 1), S(j + 1) if W(j + 1) == 5 else 0, S(j - 2) if W(j - 1) == 5 else 0)
def reflect(w, s):
    d = len(w); return tuple(w[(-i) % d] for i in range(d)), tuple(s[(-i - 1) % d] for i in range(d))
def sides(w, s, j):
    d = len(w); W = lambda k: w[k % d]; S = lambda k: s[k % d]
    return tuple(sorted([(W(j + 1), S(j), W(j + 2), S(j + 1)), (W(j - 1), S(j - 1), W(j - 2), S(j - 2))]))

BASE = ['%s:%s' % (p, q) for p in ('ring', 'hat', 'outer', 'farhat') for q in ('5>=1', '5=2', '7>=1', '7=2')]
SIDE2 = sorted({tuple(sorted([x, y])) for x in itertools.product(LET, LET) for y in itertools.product(LET, LET)})
SIDE3 = sorted({tuple(sorted([x, y])) for x in itertools.product(LET, LET, LET) for y in itertools.product(LET, LET, LET)})
def feat_names():
    n = ['tgt7'] + BASE + ['tgt7&' + b for b in BASE]
    n += ['%s&%s' % (BASE[i], BASE[j]) for i in range(16) for j in range(i + 1, 16)]
    return n + ['side2=%s' % (t,) for t in SIDE2] + ['side3=%s' % (t,) for t in SIDE3]
def ctx_feats(ctx):
    tgt, (a, b) = ctx; bb = []
    for p in range(4):
        n5 = (a[p] == 5) + (b[p] == 5); n7 = (a[p] == 7) + (b[p] == 7); bb += [n5 >= 1, n5 == 2, n7 >= 1, n7 == 2]
    t7 = tgt == 7
    f = [t7] + bb + [t7 and x for x in bb] + [bb[i] and bb[j] for i in range(16) for j in range(i + 1, 16)]
    s2 = tuple(sorted([a[:2], b[:2]])); s3 = tuple(sorted([a[:3], b[:3]]))
    return np.array(f + [s2 == t for t in SIDE2] + [s3 == t for t in SIDE3], dtype=bool)

def rows6(W6):
    out = set()
    for L in W6:
        for t in itertools.product(LET, repeat=6):
            ok = True
            for k in range(6):
                a, b = L[(k + 1) % 6], L[(k - 1) % 6]
                if L[k] == 5 and RW.isR5((6, a, t[k], t[(k - 1) % 6], b)): ok = False; break
                if L[k] == 6 and all(RW.isR6((6, a, t[k], p, t[(k - 1) % 6], b)) for p in LET): ok = False; break
            if ok: out.add(canon_ws(L, t))
    return sorted(out)
def canon_ws(w, s):
    d = len(w); best = None
    for r in range(d):
        c1 = (tuple(w[(i + r) % d] for i in range(d)), tuple(s[(i + r) % d] for i in range(d)))
        c2 = (tuple(w[(r - i) % d] for i in range(d)), tuple(s[(r - i - 1) % d] for i in range(d)))
        for c in (c1, c2):
            if best is None or c < best: best = c
    return best

class Ix:
    def __init__(self): self.d = {}
    def __call__(self, k):
        if k not in self.d: self.d[k] = len(self.d)
        return self.d[k]
    def list(self):
        L = [None] * len(self.d)
        for k, i in self.d.items(): L[i] = k
        return L

def build(R7, R6, W5, adm=True):
    ok6 = (lambda l: not RW.isR6(l)) if adm else (lambda l: True)
    ok5 = (lambda l: not RW.isR5(l)) if adm else (lambda l: True)
    V2, V3, C2, C3 = Ix(), Ix(), Ix(), Ix()
    def centre(rowlist, d):
        n = len(rowlist); K = 9 if d == 6 else 3
        IN = np.full((n, d, K), ZERO, np.int32); OUT = np.full((n, d), ZERO, np.int32)
        r2v = np.full((n, d), -1, np.int64); r3v = np.full((n, d), -1, np.int64)   # receive views (R2 from 7s, R3 from 6s)
        tgt2 = np.full((n, d), -1, np.int64); tgt3 = np.full((n, d), -1, np.int64)  # send contexts
        src = []   # (row, slot, view) for sending
        for r, (w, s) in enumerate(rowlist):
            W = lambda k: w[k % d]; S = lambda k: s[k % d]
            for k in range(d):
                sa, sb = (W(k - 1), S(k - 1)), (W(k + 1), S(k))
                if w[k] == 5:
                    IN[r, k, :] = pkey(5, d, sa, sb)
                elif w[k] == 6:
                    c = sorted({pkey(6, d, sa, sb, p) for p in LET if ok6((d, W(k + 1), S(k), p, S(k - 1), W(k - 1)))}) or [ZERO]
                    IN[r, k, :] = (c * K)[:K]
                if d == 6 and w[k] >= 6:
                    OUT[r, k] = pkey(6, w[k], (W(k - 1), W(k - 2)), (W(k + 1), W(k + 2)), W(k + 3))
                if w[k] == 7: r2v[r, k] = V2((d,) + view_recv(w, s, k))
                if w[k] == 6 and d == 7: r3v[r, k] = V3(view_recv(w, s, k))
                if d == 7 and w[k] >= 6: tgt2[r, k] = C2((w[k], sides(w, s, k)))
                if d == 6 and w[k] == 7: tgt3[r, k] = C3((7, sides(w, s, k)))
            for (ww, ss), refl in (((w, s), False), (reflect(w, s), True)):
                for j in range(d):
                    jj = (-j) % d if refl else j
                    if d == 7 and ww[j] >= 6: src.append((r, jj, V2((ww[j],) + view_send(ww, ss, j))))
                    if d == 6 and ww[j] == 7: src.append((r, jj, V3(view_send(ww, ss, j))))
        src = np.array(src, np.int64).reshape(-1, 3)
        src = src[np.argsort(src[:, 2], kind='stable')]
        return dict(n=n, IN=IN, OUT=OUT, r2v=r2v, r3v=r3v, tgt2=tgt2, tgt3=tgt3, src=src)
    A7 = centre(R7, 7); A6 = centre(R6, 6)
    # 5-rows (6 cases for a 6 neighbour: its push depends on nothing hidden here since it is the 5's own push)
    P5 = np.full((len(W5), 5), ZERO, np.int32)
    for r, w in enumerate(W5):
        for k in range(5):
            if w[k] >= 6: P5[r, k] = pkey(5, w[k], (w[(k - 1) % 5], w[(k - 2) % 5]), (w[(k + 1) % 5], w[(k + 2) % 5]))
    F2 = np.stack([ctx_feats(c) for c in C2.list()]); F3 = np.stack([ctx_feats(c) for c in C3.list()])
    nV2, nV3 = len(V2.d), len(V3.d)
    cnt2 = np.bincount(A7['src'][:, 2], minlength=nV2); cnt3 = np.bincount(A6['src'][:, 2], minlength=nV3)
    B = dict(A7=A7, A6=A6, P5=P5, F2=F2, F3=F3, nV2=nV2, nV3=nV3, R7=R7, R6=R6, W5=W5, V2=V2.list(), V3=V3.list())
    # excuse receivers with a view that no admissible sender row matches (cannot occur in a kill-free map)
    for A in (A7, A6):
        bad = ((A['r2v'] >= 0) & (cnt2[np.maximum(A['r2v'], 0)] == 0)).any(1)
        bad |= ((A['r3v'] >= 0) & (cnt3[np.maximum(A['r3v'], 0)] == 0)).any(1)
        A['excused'] = bad
    return B

BIG = np.iinfo(np.int64).min // 4
def shares_int(tgt, F, W, m):
    """integer share numerators: inS (bool) and k per row, from integer weights."""
    sc_ctx = F.astype(np.int64) @ np.asarray(W, np.int64)
    sc = np.where(tgt >= 0, sc_ctx[np.maximum(tgt, 0)], BIG)
    mx = sc.max(1, keepdims=True); inS = (tgt >= 0) & (sc >= mx - m)
    return inS, np.maximum(inS.sum(1), 1)
def segmax(src, vals, n):
    M = np.zeros(n, np.int64)
    if len(vals):
        v = src[:, 2]; st = np.flatnonzero(np.r_[True, v[1:] != v[:-1]])
        M[v[st]] = np.maximum(np.maximum.reduceat(vals, st), 0)
    return M

def exact(B, P, th7, th6, W2, m2, W3, m3, U=1):
    """U: charge sub-unit (P, th7, th6 given in units of 1/U of a charge unit; finals in units of 1/(U*SCALE))."""
    """exact integer evaluation; returns finals in units of 1/SCALE."""
    Pf = np.concatenate([np.asarray(P, np.int64), [0]]); S = SCALE
    A7, A6 = B['A7'], B['A6']
    c1_7 = -60 * U + Pf[A7['IN']].max(2).sum(1)
    c1_6 = Pf[A6['IN']].max(2).sum(1) - Pf[A6['OUT']].sum(1)
    has2 = (A7['tgt2'] >= 0).any(1)
    inS, k = shares_int(A7['tgt2'], B['F2'], W2, m2)
    sur2 = np.where(has2, np.maximum(c1_7 - th7, 0), 0)
    f2 = sur2[:, None] * (S // k)[:, None] * inS
    M2 = segmax(A7['src'], f2[A7['src'][:, 0], A7['src'][:, 1]], B['nV2'])
    in2_7 = np.where(A7['r2v'] >= 0, M2[np.maximum(A7['r2v'], 0)], 0).sum(1)
    in2_6 = np.where(A6['r2v'] >= 0, M2[np.maximum(A6['r2v'], 0)], 0).sum(1)
    c2_6 = c1_6 * S + in2_6
    has3 = (A6['tgt3'] >= 0).any(1)
    inS3, k3 = shares_int(A6['tgt3'], B['F3'], W3, m3)
    sur3 = np.where(has3, np.maximum(c2_6 - th6 * S, 0), 0)
    assert (sur3 % 60 == 0).all()
    f3 = (sur3 // k3)[:, None] * inS3
    assert ((sur3 % k3) == 0).all()
    M3 = segmax(A6['src'], f3[A6['src'][:, 0], A6['src'][:, 1]], B['nV3'])
    in3_7 = np.where(A7['r3v'] >= 0, M3[np.maximum(A7['r3v'], 0)], 0).sum(1)
    f7 = np.where(has2, np.minimum(c1_7, th7), c1_7) * S + in2_7 + in3_7
    f6 = np.where(has3, np.minimum(c2_6, th6 * S), c2_6)
    f5 = (60 * U - Pf[B['P5']].sum(1)) * S
    return dict(f7=f7, f6=f6, f5=f5, c1_7=c1_7, c1_6=c1_6, c2_6=c2_6, M2=M2, M3=M3, sur2=sur2, sur3=sur3)

def maxfinal(B, E):
    return max(E['f7'][~B['A7']['excused']].max(), E['f6'][~B['A6']['excused']].max(), E['f5'].max())
