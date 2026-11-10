# p1r.py (s86 p1r, Opus team): KEYSPEC v2 receiver single-row form "p1_r" (W6b round 16e/f: KEYSPEC2_RECEIVER.md md5 d5a6734b,
# sections 1, 2, 3.3, 4.5; P1R_NOTE.md md5 f0312e8e), behind flag p1r.  exec'd by pcheck.py after edge56.py.  Without the flag this file
# only defines functions (names p1r_* / _P1R*); no row, table or separator changes.
#
# On a receiver row of degree d = 7 or 8 (centre c, link w_0..w_{d-1}, apexes s_j exact) every generic key K (gkeys=) gets
#     coef_K = max over realisations rho of IN(K; rho) - OUT(K)
# instead of edge56's "possibly" IN count (d = 7 under gkleaf) or the gkwin window bound (d = 8).  OUT is edge56's exact sure count.
# Realisation: one group G_j = (x_j, y_j) per link j, chosen independently from dom_j; x_j = w_j's private next to s_j (edge56
# pin(j, 1); W6b a_j), y_j = w_j's private next to s_{j-1} (pin(j, 0); W6b b_{j-1}):
#   w_j = 5 : {(s_{j-1}, s_j)} (the 5's rotation, exactly what gk_slots' pin reads);
#   w_j = 6 : {(p, p)}, p over the letters the row's own M term ranges over: sig = sig2_of(...) + (amask & ~extra6,) as prelay2's
#             recv_coef_R2 + f2bglue build ('M', sig); p in pallow(sig), not isR6.  Asserted: {h2_of(.., p, ..)} = sig2_keys(sig);
#   w_j = 7 : {(p1, p2)}: p1 in m1 (side +1, next to s_j), p2 in m2 (side -1, next to s_{j-1}), (U, w_{j+1}, s_j, p1, p2, s_{j-1}, w_{j-1})
#             not RBIG; m1 / m2 = the q7m masks f2bglue puts in ('Q', q7sig(.., m1, m2)): L3T (d = 7) or the l3qV = 8 table (d = 8)
#             & ~extra7 on a side with c, apex <= 6, 31 & ~extra7 otherwise (f2b7).  Asserted: {qkey(.., p1, p2, ..)} = q7keys(sig);
#   w_j >= 8: all 25 pairs.
# Checks on every row: the multiset of ('M', sig), ('Q', sig), ('lQ', key) entries these domains imply equals the row's own (recv_coef_R2
# below the gkeys wrapper), i.e. the domains are the base terms' own ranges; per link the domain's projections lie inside
# gk_recv_picture's private masks (so p1_r <= the picture IN count <= the window bound; KEYSPEC2 4.5), and max IN <= picture IN per key;
# the private columns gk_slots builds from the projections are exactly the (x, y) reads listed below.  A row with an empty domain
# (no realisation; the row cannot occur) keeps its current coefficients.
# IN slot (i, +1): S.L+3 = y_i, S.L-3 = x_i, S.A+1 = x_{i-1}, S.A-1 = y_{i+1};  (i, -1): S.L+3 = x_i, S.L-3 = y_i, S.A+1 = y_{i+1},
# S.A-1 = x_{i-1}.  With site Q_j = (x_j, y_{j+1}) slot i reads (Q_{i-1}, Q_i), and G_i = (Q_i.x, Q_{i-1}.y) must lie in dom_i, so
# max IN is a max-plus product round the d-cycle of sites (exact; states restricted to the domain projections).  Keys whose live
# slots all match on the whole domain (every private read inside the key's set for every letter of the projection) skip the DP.
# Unchanged: d >= 9 receivers, senders, cons2, mrows, and every separator (jsepf leaf 7802 / 7804, gkwin window tables, class fold):
# their key coefficients are >= p1_r, so the separators over-report (sound for a lower-bound run; see p1r/README.md).
P1R = 'p1r' in FLAGS
# eng_p8l (Lead 9 Nov 19:42Z): p1r with payer-8/9 keys.  OUT at a d = 8 centre is the exact sure count on the picture (every OUT position,
# S.L+-3 included, is an exact link or apex letter), so OUT_p1r >= the W5 OUT of the gkwin row and IN_max <= the window IN: the p1r row is
# weaker than the upper's row (a relaxation), checked key by key by cmd_p1rordtest.  P1RPLANT (CONTROL ONLY): d = 8 payer-8/9 OUT read as 0.
P1RPLANT = 'p1rplant' in FLAGS
P1R_STAT = collections.Counter()
_P1R_ALL25 = frozenset((a_, b_) for a_ in LET for b_ in LET)
_P1R_C6 = {}; _P1R_C7 = {}
_P1R_RD = {1: (6, 2, 5, 7), -1: (7, 5, 2, 6)}   # GK_POS index reading (Q_{i-1}.x, Q_{i-1}.y, Q_i.x, Q_i.y) = (x_{i-1}, y_i, x_i, y_{i+1})
_P1R_FIXCOL = [0, 1, 3, 4, 8, 9]                # IN positions reading link / apex letters only
_P1R_NEG = -(10 ** 6)
def p1r_domains(d, w, s):
    """(dom, base): dom[j] = frozenset of (x_j, y_j) letter pairs; base = Counter of the ('M' / 'Q' / 'lQ') entries the row must carry"""
    assert d in (7, 8)
    U = min(d, 9); n = d; W_ = lambda k: w[k % n]; S_ = lambda k: s[k % n]
    dom = []; base = collections.Counter()
    for j in range(n):
        x = w[j]
        if x == 5: dom.append(frozenset({(S_(j - 1), S_(j))})); continue
        if x == 6:
            sg = sig2_of(U, W_(j + 1), S_(j), S_(j - 1), W_(j - 1), W_(j + 2), W_(j - 2))
            am = amask(U, W_(j - 2), W_(j - 1), W_(j + 1), W_(j + 2), S_(j - 2), S_(j - 1), S_(j), S_(j + 1))
            sgM = sg + (am & ~f2bm.extra6(d, w, s, j),)
            ck = (U, W_(j + 1), S_(j), S_(j - 1), W_(j - 1), W_(j + 2), W_(j - 2), sgM)
            if ck not in _P1R_C6:
                P6 = [p for p in pallow(sgM) if not isR6((U, W_(j + 1), S_(j), p, S_(j - 1), W_(j - 1)))]
                ks = sig2_keys(sgM)
                assert sorted({h2_of((U, W_(j + 1), S_(j), p, S_(j - 1), W_(j - 1)), W_(j + 2), W_(j - 2)) for p in P6}) == ks, ('p1r: 6 domain vs sig2_keys', d, w, s, j)
                _P1R_C6[ck] = (frozenset((p, p) for p in P6), bool(ks))
            D, has = _P1R_C6[ck]
            if has: base[('M', sgM)] += 1
            dom.append(D); continue
        if x == 7:
            T = L3T if d == 7 else l3q_loadV(8); ms = []
            for sgn in (1, -1):
                c_ = W_(j + sgn); ap_, o_ = (S_(j), S_(j - 1)) if sgn == 1 else (S_(j - 1), S_(j)); ex = f2bm.extra7(d, w, s, j, sgn)
                if c_ <= 6 and ap_ <= 6:
                    m_ = T[(sgn, c_, W_(j + 2 * sgn), W_(j + 3 * sgn), W_(j + 4 * sgn), ap_, o_)] & ~ex
                    base[('lQ', ((c_, ap_, m_) if d == 7 else (8, c_, ap_, m_)))] += 1
                else: m_ = 31 & ~ex
                ms.append(m_)
            m1, m2 = ms
            ck = (U, W_(j + 1), S_(j), S_(j - 1), W_(j - 1), m1, m2)
            if ck not in _P1R_C7:
                sgm = q7sig(U, W_(j + 1), S_(j), S_(j - 1), W_(j - 1), m1, m2)
                pairs = [(p1, p2) for p1 in LET if (m1 >> (p1 - 5)) & 1 for p2 in LET if (m2 >> (p2 - 5)) & 1
                         if ''.join(map(str, canon((U, W_(j + 1), S_(j), p1, p2, S_(j - 1), W_(j - 1))))) not in RBIG]
                ks = q7keys(sgm)
                assert sorted({qkey((U, W_(j + 1), S_(j), p1, p2, S_(j - 1), W_(j - 1))) for p1, p2 in pairs}) == ks, ('p1r: 7 domain vs q7keys', d, w, s, j)
                _P1R_C7[ck] = (frozenset(pairs), sgm, bool(ks))
            D, sgm, has = _P1R_C7[ck]
            if has: base[('Q', sgm)] += 1
            dom.append(D); continue
        dom.append(_P1R_ALL25)
    return dom, base
def _p1r_bits(lets):
    m = 0
    for l_ in lets: m |= 1 << (l_ - 5)
    return m
def p1r_dp(dom, X, Y, Mk, unck, sign):
    """per key (rows of Mk / unck): max over realisations of sign x (number of matching slots among the flagged ones), exact (max-plus
    product round the d-cycle of sites Q_j = (x_j, y_{j+1}), states restricted to the domain projections X_j x Y_{j+1})"""
    n = len(dom); nk = Mk.shape[0]
    xl = [[l_ for l_ in LET if (X[j] >> (l_ - 5)) & 1] for j in range(n)]; yl = [[l_ for l_ in LET if (Y[j] >> (l_ - 5)) & 1] for j in range(n)]
    sx = []; sy = []   # letter (5..9) of x_j / y_{j+1} per state of site j
    for j in range(n):
        ys_ = yl[(j + 1) % n]
        sx.append(np.array([a_ for a_ in xl[j] for _ in ys_], dtype=np.int64)); sy.append(np.array([b_ for _ in xl[j] for b_ in ys_], dtype=np.int64))
    bx = [(1 << (v - 5)).astype(np.uint8) for v in sx]; by = [(1 << (v - 5)).astype(np.uint8) for v in sy]
    F = []
    for i in range(n):
        Dm = np.zeros((10, 10), dtype=bool)
        for a_, b_ in dom[i]: Dm[a_, b_] = True
        ok = Dm[sx[i][None, :], sy[(i - 1) % n][:, None]]          # (n_{i-1}, n_i): (x_i from site i, y_i from site i-1) in dom_i
        F.append(np.repeat(np.where(ok, 0, _P1R_NEG).astype(np.int32)[None], nk, axis=0))
    for i in range(n):
        for t_, sg in ((0, 1), (1, -1)):
            kk = np.nonzero(unck[:, 2 * i + t_])[0]
            if not len(kk): continue
            r = _P1R_RD[sg]; m = Mk[kk]; im = (i - 1) % n
            lft = ((bx[im][None, :] & m[:, r[0]][:, None]) != 0) & ((by[im][None, :] & m[:, r[1]][:, None]) != 0)
            rgt = ((bx[i][None, :] & m[:, r[2]][:, None]) != 0) & ((by[i][None, :] & m[:, r[3]][:, None]) != 0)
            F[i][kk] += sign * (lft[:, :, None] & rgt[:, None, :]).astype(np.int32)
    P = F[1]
    for i in range(2, n): P = (P[:, :, :, None] + F[i][:, None, :, :]).max(axis=2)
    tot = (P + F[0].transpose(0, 2, 1)).max(axis=(1, 2))
    assert (tot > _P1R_NEG // 2).all(), 'p1r: no realisation in the DP although every domain is non-empty'
    return tot.astype(np.int64)
def p1r_core(d, w, s, UM, VM, M, want_min=False, base_cf=None):
    """p1_r data of one d = 7 / 8 receiver for the keys (UM, VM, M) (edge56 layout): pay (OUT), poss (picture IN), poss2 (IN possible
    on the domain projections), inmax (max over realisations), inmin (with want_min), empty (some dom_j empty: no realisation)"""
    n = d; A, PV = gk_recv_picture(d, w, s)
    (ou, ov, oV), (iu, iv, iV) = gk_slots(d, w, A, PV)
    pay = (((oV[None, :, :] & ~M[:, None, :]) == 0).all(axis=2) & ((ou[None, :] & ~UM[:, None]) == 0) & ((ov[None, :] & ~VM[:, None]) == 0)).sum(axis=1)
    uv = ((iu[None, :] & UM[:, None]) != 0) & ((iv[None, :] & VM[:, None]) != 0)
    poss = ((iV[None, :, :] & M[:, None, :]) != 0).all(axis=2) & uv
    dom, base = p1r_domains(d, w, s)
    if base_cf is not None:
        got = collections.Counter({k: v for k, v in base_cf.items() if k[0] in ('M', 'Q', 'lQ') and v})
        assert got == base, ('p1r: domains do not match the row base terms', d, w, s, sorted(got.items(), key=str), sorted(base.items(), key=str))
    res = {'pay': pay, 'poss': poss.sum(axis=1), 'empty': any(not D for D in dom), 'dom': dom}
    if res['empty']: return res
    X = [_p1r_bits({a_ for a_, _ in D}) for D in dom]; Y = [_p1r_bits({b_ for _, b_ in D}) for D in dom]
    for j in range(n):
        if w[j] == 5: assert (X[j], Y[j]) == (A[(j - 1) % n], A[j]), ('p1r: 5 group', d, w, s, j)
        else: assert not (X[j] & ~PV[j][1]) and not (Y[j] & ~PV[j][0]), ('p1r: domain projection outside the picture mask', d, w, s, j, X[j], Y[j], PV[j])
    PV2 = [None if w[j] == 5 else (Y[j], X[j]) for j in range(n)]
    _, (iu2, iv2, iV2) = gk_slots(d, w, A, PV2)
    assert np.array_equal(iu2, iu) and np.array_equal(iv2, iv) and np.array_equal(iV2[:, _P1R_FIXCOL], iV[:, _P1R_FIXCOL]) and not (iV2 & ~iV).any(), ('p1r: projection picture', d, w, s)
    for i in range(n):
        for t_, sg in ((0, 1), (1, -1)):
            r = _P1R_RD[sg]; v = iV2[2 * i + t_]
            assert (int(v[r[0]]), int(v[r[1]]), int(v[r[2]]), int(v[r[3]])) == (X[(i - 1) % n], Y[i], X[i], Y[(i + 1) % n]), ('p1r: slot reading differs from gk_slots', d, w, s, i, sg)
    poss2 = ((iV2[None, :, :] & M[:, None, :]) != 0).all(axis=2) & uv
    sure2 = ((iV2[None, :, :] & ~M[:, None, :]) == 0).all(axis=2) & uv
    unc = poss2 & ~sure2
    inmax = poss2.sum(axis=1).astype(np.int64); nsure = sure2.sum(axis=1).astype(np.int64)
    inmin = nsure.copy() if want_min else None
    kd = np.nonzero(unc.any(axis=1))[0]
    if len(kd):
        inmax[kd] = nsure[kd] + p1r_dp(dom, X, Y, M[kd], unc[kd], 1)
        if want_min: inmin[kd] = nsure[kd] - p1r_dp(dom, X, Y, M[kd], unc[kd], -1)
    assert (inmax <= poss2.sum(axis=1)).all() and (inmax >= nsure).all() and (poss2.sum(axis=1) <= res['poss']).all(), ('p1r: bound order', d, w, s)
    res.update(poss2=poss2.sum(axis=1), inmax=inmax, inmin=inmin, ndp=len(kd))
    return res
if P1R:
    assert GKON, 'p1r needs gkeys='
    assert F2B_ON and Q7 and Q7M and F2B7 and L3Q and 8 in LQVX and F16 and AC and AP and not V6 and not XO and not KSTAR and not EGNAMES and not GKPLANT, \
        'p1r: needs the s86 family (f2b + f2b7 + q7 q7m, l3q l3qV=7,8, filt16, apexcls; no xo / v6 / kstar / edgekeys / gkplant)'
    _p1r_gk_recv_terms_cur = gk_recv_terms   # the current key terms (gkleaf exact picture at d = 7, gkwin window at d = 8, ...)
    def p1r_recv_terms(d, w, s, base_cf=None):
        l3q_load(); kt_load()
        r = p1r_core(d, w, s, _GK_UM, _GK_VM, _GK_M, base_cf=base_cf)
        if r['empty']: P1R_STAT['empty domain (current kept)'] += 1; return _p1r_gk_recv_terms_cur(d, w, s)
        P1R_STAT['rows'] += 1; P1R_STAT['rows with DP'] += r['ndp'] > 0
        pay_ = r['pay']
        if P1RPLANT and d == 8: pay_ = np.where((_GK_UM & 24) != 0, 0, pay_)
        return _gk_cf(pay_, r['inmax'], -1)
    def gk_recv_terms(d, w, s):
        if not GKON: return collections.Counter()
        if d in (7, 8): return p1r_recv_terms(d, w, s)
        return _p1r_gk_recv_terms_cur(d, w, s)
    def recv_coef_R2(d, lk, sv, xon, tau=None):
        """edge56's wrapper, with p1_r key terms at d = 7, 8 (checked against this row's own base terms)"""
        cf = _orig_recv_coef_R2_gk(d, lk, sv, xon, tau)
        w = [int(ch) for ch in lk]; s = [int(ch) for ch in sv]
        kt = p1r_recv_terms(d, w, s, cf) if d in (7, 8) else _p1r_gk_recv_terms_cur(d, w, s)
        for k_, v_ in kt.items():
            cf[k_] += v_
            if cf[k_] == 0: del cf[k_]
        return cf
    log('p1r: KEYSPEC v2 single-row receiver keys (p1_r) on d = 7, 8 receiver rows (python rows only; separators unchanged, >= p1_r)')

def cmd_p1rordtest():
    """eng_p8l: every p1r receiver coefficient (d = 7, 8) <= the upper's coefficient (d = 7 exact picture under gkleaf, d = 8 gkwin
    window IN - W5 OUT), key by key, on random receivers with letters 5..9 (and runs rich in 8s); reports payer-8/9 coverage"""
    import random; l3q_load(); kt_load(); rng = random.Random(int(OPT.get('seed', '1'))); N_ = int(OPT.get('N', '1500')); bad = 0
    assert P1R, 'p1rordtest needs the p1r flag'
    p89 = (_GK_UM & 24) != 0; VEC = []   # test vectors for replays (payer-8/9 keys with OUT > 0 or IN_max > 0), written next to p8test/
    for d in (7, 8):
        n_ = 0; nz = 0; nzo = 0; nzi = 0; strict = 0; nb = 0; emp = 0
        while n_ < N_:
            w = [rng.choice((5, 6, 7, 8, 9)) for _ in range(d)]; s = [rng.choice((5, 6, 7, 8, 9)) for _ in range(d)]
            if n_ % 3 == 1: w = [rng.choice((5, 5, 6, 7, 8)) for _ in range(d)]
            lk = ''.join(map(str, w)); sv = ''.join(map(str, s))
            if admissible(d, lk, sv) is not None: continue
            n_ += 1
            r = p1r_core(d, w, s, _GK_UM, _GK_VM, _GK_M)
            if r['empty']: emp += 1; continue
            mine = p1r_recv_terms(d, w, s); cur = _p1r_gk_recv_terms_cur(d, w, s)
            for k, nm_ in enumerate(GKNAMES):
                a = mine.get(('ks', nm_), 0); b = cur.get(('ks', nm_), 0)
                if p89[k]:
                    nzo += int(r['pay'][k]) > 0; nzi += int(r['inmax'][k]) > 0
                    if (int(r['pay'][k]) > 0 or int(r['inmax'][k]) > 0) and len(VEC) < 400 and sum(v_['d'] == d for v_ in VEC) < 200:
                        VEC.append({'d': d, 'link': lk, 'apex': sv, 'key': nm_, 'spec': GKEYS[k]['spec'], 'OUT': int(r['pay'][k]),
                                    'IN_max': int(r['inmax'][k]), 'p1r': int(a), 'upper': int(b), 'p1rplant': bool(P1RPLANT)})
                nz += a != 0; strict += a < b
                if a > b:
                    bad += 1; nb += 1
                    if bad <= 8: log('  p1rordtest d=%d %s/%s key %s: p1r %d > upper %d' % (d, lk, sv, nm_, a, b))
        log('  p1rordtest d=%d: %d receivers (%d with an empty domain) x %d keys: %d nonzero p1r coefficients, %d strictly below the upper; payer-8/9 keys: OUT > 0 in %d, IN_max > 0 in %d; %d violations' % (d, N_, emp, len(GKEYS), nz, strict, nzo, nzi, nb))
    import json as _js, os as _os
    vp = OPT.get('vecout', _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'p8test', 'p1rord_vectors_%s.json' % ('ctl' if P1RPLANT else 'main')))
    _js.dump({'note': 'eng_p8l p1rordtest: d = 7, 8 receivers x payer-8/9 keys with OUT > 0 or IN_max > 0; OUT = exact sure count, IN_max = max over realisations, p1r = IN_max - OUT, upper = eng_p8 coefficient (gkleaf d = 7, gkwin IN - W5 OUT d = 8)', 'vectors': VEC}, open(vp, 'w'), indent=0)
    log('  p1rordtest: %d payer-8/9 vectors -> %s' % (len(VEC), vp))
    log('P1RORDTEST: %s (%d violations)' % ('PASS' if bad == 0 else 'FAIL', bad))
