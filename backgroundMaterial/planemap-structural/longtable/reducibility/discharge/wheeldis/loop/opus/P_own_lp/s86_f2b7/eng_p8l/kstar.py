# kstar.py (s78_kstar, Team D): W6 round-3 deep key K* as an engine family.  exec'd by pcheck.py after f2bglue.py (needs f2b + l3q).
#
#   K* = EDGE(7->7)[S.L+1=B S.L-1=S S.L-2=5 S.L-3=5 S.A-1=B]   (grammar.py / gext.py positions; B = {7,8,9+}, S = {5,6})
#   A vertex u of degree exactly 7 pays ks[K1] >= 0 (cap kscap, default 3) to a neighbour v of degree exactly 7, once per oriented match:
#   in u's link read from v toward c- (the common neighbour on the S side): v, c-, S.L-2, S.L-3, ., ., c+  with c- in S, S.L-2 = 5,
#   S.L-3 = 5, c+ in B, and S.A-1 = the apex of u across (c-, S.L-2) (third vertex of that face, not u) in B.
#
#   Payer row (d = 7 centre u, link w, apexes s; s_i = apex of w_i w_{i+1}): for each link 7 at i and e1 = +-1 with c- = w_{i+e1}:
#       w_{i-e1} in B, w_{i+e1} in S, w_{i+2e1} = 5, w_{i+3e1} = 5, apex(i+e1, i+2e1) (= s_{i+1} / s_{i-2}) in B   ->  coefficient -1.
#       Every letter is in the payer's own 2-ball (link + apexes), so the payer side is exact; no second-ring row family is needed.
#   Payee row (d = 7 centre v): for each link 7 at j (the payer u) and e1 = +-1 with c- = w_k, k = j+e1, c+ = w_{j-e1}:
#       w_{j-e1} in B, w_k in S, a = apex(j, k) = 5 (S.L-2, exact), and POSSIBLY (credit semantics, as grammar.py and the engine's mrows):
#       S.L-3 = u's private next to a: 5 in L3T[(e1, w_k, w_{j+2e1}, w_{j+3e1}, w_{j+4e1}, a, o)] & ~extra7(j, e1)   (o = u's other apex);
#       S.A-1: c- = 5 -> c-'s other apex apex(k, k+e1) (exact) in B;  c- = 6 -> the 6's private, (amask & ~extra6(k)) meets B.
#       -> coefficient +1.  (Hidden letters are maximised slot by slot: the payee credits a slot whenever some allowed letter fires it.)
#   Window table (U = 7): + ks * KUB, KUB = the payee slot with L3T OR-ed over w_{j+4e1} (outside the window) and no f2b extras, in the
#   window centred at c- (k).  jsepf (argv[13]) applies the exact payer term and exact - KUB at the leaf, both <= 0 (refuses > 0).
#   Rows of every other kind (senders, cons2, d >= 8) carry no K* coefficient (both endpoints are exactly 7).
KSTAR = 'kstar' in FLAGS
KSCAP = float(OPT.get('kscap', '3'))
KSV = {}                                 # 'K1' -> amount (LP value / solution value)
KSPLANT = 'ksplant' in FLAGS             # CONTROL ONLY: the Python payee mask ignores f2b extra7 (C++ keeps it) -> the eval self-test must FAIL
KSNOWIN = 'ksnowin' in FLAGS             # CONTROL ONLY: no window bound (WIN and the file's KUB = 0) but the true amount: the payee gain would be a
                                         # positive leaf term outside WIN (the sep3r bug); jsepf must refuse it (exit 81)
_KUB = []
if KSTAR:
    assert F2B_ON and L3Q and F16 and AC and AP and not W19 and not PCAM and not XO and not FY and not V6, 'kstar: needs the s75 stack (f2b + l3q + filt16 + apexcls)'
B_MASK = 4 | 8 | 16                      # letters 7, 8, 9 (bit k = letter 5 + k)
def kstar_payee_slot(w, s, j, e1, plant=False):
    """1 iff the d = 7 centre (link w, apexes s) credits a K* slot from its link 7 at j with c- = w_{j+e1}; exact masks"""
    n = 7; k = (j + e1) % n
    if w[j] != 7 or w[(j - e1) % n] < 7 or w[k] > 6: return 0
    a = s[j] if e1 > 0 else s[(j - 1) % n]; o = s[(j - 1) % n] if e1 > 0 else s[j]
    if a != 5: return 0
    if w[k] == 5: sa = (s[k] if e1 > 0 else s[(k - 1) % n]) >= 7
    else:
        m6 = amask(7, w[(k - 2) % n], w[(k - 1) % n], w[(k + 1) % n], w[(k + 2) % n], s[(k - 2) % n], s[(k - 1) % n], s[k], s[(k + 1) % n]) & ~f2bm.extra6(7, w, s, k)
        sa = (m6 & B_MASK) != 0
    if not sa: return 0
    m7 = L3T[(e1, w[k], w[(j + 2 * e1) % n], w[(j + 3 * e1) % n], w[(j + 4 * e1) % n], a, o)]
    if not plant: m7 &= ~f2bm.extra7(7, w, s, j, e1)
    return 1 if m7 & 1 else 0
def kstar_payer_slot(w, s, i, e1):
    """1 iff the d = 7 centre pays K* to its link 7 at i with c- = w_{i+e1} (all letters in the centre's 2-ball)"""
    n = 7
    return int(w[i] == 7 and w[(i - e1) % n] >= 7 and w[(i + e1) % n] <= 6 and w[(i + 2 * e1) % n] == 5 and w[(i + 3 * e1) % n] == 5
               and (s[(i + 1) % n] if e1 > 0 else s[(i - 2) % n]) >= 7)
def kstar_terms(d, w, s):
    cf = collections.Counter()
    if not KSTAR or d != 7: return cf
    l3q_load(); kt_load()
    for i in range(7):
        for e1 in (1, -1):
            cf[('ks', 'K1')] += kstar_payee_slot(w, s, i, e1, KSPLANT) - kstar_payer_slot(w, s, i, e1)
    return cf
_orig_recv_coef_R2_ks = recv_coef_R2
def recv_coef_R2(d, lk, sv, xon, tau=None):
    cf = _orig_recv_coef_R2_ks(d, lk, sv, xon, tau)
    if KSTAR and d == 7:
        for k_, v_ in kstar_terms(7, [int(ch) for ch in lk], [int(ch) for ch in sv]).items():
            cf[k_] += v_
            if cf[k_] == 0: del cf[k_]
    return cf
def kstar_kub():
    """(KUB0, KUB1) uint8 arrays over the 5^9 window index (a,b,c,e,f,p,q,r,s) = (w_{k-2..k+2}, s_{k-2..k+1}): window upper bound of a K*
    payee slot with c- = w_k and the payer at k-1 (KUB0; c+ = w_{k-2}) or at k+1 (KUB1; c+ = w_{k+2})"""
    if not _KUB:
        kt_load(); l3q_load()
        a, b, c, e, f, p, q, r, s_ = np.indices((5,) * 9, dtype=np.int16)
        AM = 31 & ~np.asarray(KT[7]).astype(np.int64)            # amask(7, ...) index (w-2, w-1, w+1, w+2, s-2, s-1, s0, s+1) - 5
        am = AM[a, b, e, f, p, q, r, s_]
        six_b = (am & B_MASK) != 0
        L3p = np.zeros((5,) * 5, dtype=bool); L3m = np.zeros((5,) * 5, dtype=bool)   # OR over w4 of (5 in mask): [c, w2, w3, ap, o]
        for (sg, cc, w2, w3, w4, ap_, o_), m in L3T.items():
            T_ = L3p if sg == 1 else L3m
            T_[cc - 5, w2 - 5, w3 - 5, ap_ - 5, o_ - 5] |= bool(m & 1)
        cl = np.minimum(c, 1)
        k0 = (b == 2) & (a >= 2) & (c <= 1) & (q == 0) & np.where(c == 0, r >= 2, six_b) & L3p[cl, e, f, q, p]
        k1 = (e == 2) & (f >= 2) & (c <= 1) & (r == 0) & np.where(c == 0, q >= 2, six_b) & L3m[cl, b, a, r, s_]
        del a, b, c, e, f, p, q, r, s_, am, six_b, cl
        _KUB.extend([k0.astype(np.uint8).reshape(-1), k1.astype(np.uint8).reshape(-1)])
        log('kstar: window bounds: %d windows with a payer-at-k-1 slot, %d with a payer-at-k+1 slot' % (int(_KUB[0].sum()), int(_KUB[1].sum())))
    return _KUB
_orig_window_table_R2_ks = window_table_R2
def window_table_R2(U, y, x, MV2):
    W = _orig_window_table_R2_ks(U, y, x, MV2)
    v = KSV.get('K1', 0.0)
    if KSTAR and U == 7 and v != 0.0 and not KSNOWIN:
        k0, k1 = kstar_kub()
        W += v * (k0.astype(np.float64) + k1.astype(np.float64)).reshape((5,) * 9)
    return W
def kstar_write(d):
    """argv[13] file for jsepf at d = 7 (layout in jsepf.cpp)"""
    assert d == 7
    v = float(KSV.get('K1', 0.0))
    assert v >= -1e-12, 'kstar: negative amount %r' % v
    v = max(v, 0.0)
    k0, k1 = kstar_kub()
    if KSNOWIN: k0 = np.zeros_like(k0); k1 = np.zeros_like(k1)   # control: bound missing from the file as from WIN
    fn = os.path.join(WORK, 'kstar_d7.bin')
    with open(fn, 'wb') as fh:
        fh.write(np.array([7801, 7], dtype='<i4').tobytes()); fh.write(np.array([v], dtype='<f8').tobytes())
        fh.write(k0.tobytes()); fh.write(k1.tobytes())
    return fn
def kstar_force(rng, d):
    """a random d = 7 arrangement with a planted K* payer slot (mode 0) or payee slot pattern (mode 1, masks random)"""
    w = [rng.choice((5, 6, 7, 8, 9)) for _ in range(d)]; s = [rng.choice((5, 6, 7, 8, 9)) for _ in range(d)]
    i = rng.randrange(d); e1 = rng.choice((1, -1)); n = d
    w[i] = 7; w[(i - e1) % n] = rng.choice((7, 8, 9)); w[(i + e1) % n] = rng.choice((5, 6))
    if rng.random() < 0.5:   # payer: S.L-2 = S.L-3 = 5, S.A-1 big
        w[(i + 2 * e1) % n] = 5; w[(i + 3 * e1) % n] = 5
        if e1 > 0: s[(i + 1) % n] = rng.choice((7, 8, 9))
        else: s[(i - 2) % n] = rng.choice((7, 8, 9))
    else:                    # payee: apex(i, i+e1) = 5, c-'s other apex big when c- = 5
        if e1 > 0: s[i] = 5
        else: s[(i - 1) % n] = 5
        k = (i + e1) % n
        if w[k] == 5:
            if e1 > 0: s[k] = rng.choice((7, 8, 9))
            else: s[(k - 1) % n] = rng.choice((7, 8, 9))
    return w, s
