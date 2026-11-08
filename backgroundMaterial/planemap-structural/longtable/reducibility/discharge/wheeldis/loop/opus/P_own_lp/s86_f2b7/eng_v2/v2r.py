# v2r.py (s86 v2r, Opus team): KEYSPEC v2 receiver rows on d = 7 / 8 as REALISATION rows (cutting planes over rho), flag v2r.
# Spec: W6b KEYSPEC2_RECEIVER.md (md5 d5a6734b) sections 1-5 (3.1 = the exact row); P1R_NOTE.md; here the max-row
#     max over rho of value(rho; x) <= d - 6 + t
# is written as the conjunction over rho of the linear realisation rows value(rho; x) - t <= d - 6, added lazily (DP argmax at a point).
# exec'd by pcheck.py after p1r.py.  Without the flag this file only defines functions / commands (names v2r_* / _V2*); nothing changes.
#
# Realisation rho of a d = 7 / 8 receiver (centre c, link w_0..w_{d-1}, apexes s_j between w_j and w_{j+1}, all exact letters 5..9, 9 = 9+):
#   one pair (x_j, y_j) per link position j, chosen independently from dom_j (p1r_domains, = the ranges of the masked base terms):
#     x_j = w_j's neighbour next to s_j away from c (its private; W6b a_j; edge56 pin(j, 1)),
#     y_j = w_j's neighbour next to s_{j-1} away from c (W6b b_{j-1}; edge56 pin(j, 0));
#   w_j = 5: {(s_{j-1}, s_j)};  6: {(p, p)}: p in pallow(sig2 + amask & ~extra6), not R6;  7: {(p1, p2)}: q7m / f2b7 masks, not RBIG;  >= 8: all 25.
#   Written as the string rho = x_0 y_0 x_1 y_1 ... x_{d-1} y_{d-1} (2d letters 5..9).
# The realisation row ('receiverV2', d, link, apex, rho):
#   fixed  = the masked row (recv_coef_R2 below the gkeys wrapper) minus its envelope entries ('M', 'Q', 'lQ'); these are exactly the
#            entries p1r_domains says the groups own (asserted: same multiset);
#   base   = per group the copy's terms: 6 at j: h[h2_of((U, w_{j+1}, s_j, p, s_{j-1}, w_{j-1}), w_{j+2}, w_{j-2})];
#            7 at j: q[qkey((U, w_{j+1}, s_j, x_j, y_j, s_{j-1}, w_{j-1}))] + lq[(V, c, a, x_j)] on side +1 (c = w_{j+1}, a = s_j) and
#            lq[(V, c, a, y_j)] on side -1 (c = w_{j-1}, a = s_{j-1}) when c, a <= 6 (V = () at d = 7, (8,) at d = 8);
#   keys   = per generic key K: IN(K; rho) - OUT(K): gk_slots on the exact-letter picture (privates from rho), IN counted exactly, OUT as edge56.
#   Row: fixed + base + keys - t <= d - 6.  Integer coefficients; lowerR2 rebuilds it from the id alone (v2r_row).
# Soundness (KEYSPEC2 4): the real letters rho0 of any real configuration lie in the domain product, the real row = value(rho0; x), so every
# realisation row with rho = rho0 is implied; a row for another rho is a valid row of the max-row family, which implies the true constraint.
# The masked d = 7 / 8 receiver rows are STRONGER than the v2 rows (4.5), so under v2r they never enter the LP and lowerR2 rejects them.
# Separation: the masked separators (jsepf leaf, window tables) evaluate every group term as an envelope max read from the rule columns
# (M: max h over sig2_keys; Q: max q over the masked pairs; lQ: max(LP lQ column, max lq over the mask)) and the keys with the current
# coefficients (>= p1_r >= IN(K; rho), amounts >= 0), so masked value >= v2 value pointwise: they list a superset of the v2-violated
# receivers (up to their top-K cap and class collapse).  Each listed d = 7 / 8 receiver gets the DP at the point; its argmax row is added
# when it exceeds d - 6 + t + v2tol.  Every known d = 7 / 8 receiver is re-scanned by the DP each round (v2rescan=k: every k-th round, and
# always before the loop would stop), since phantoms (masked-violated, v2-satisfied) can fill the separators' top-K lists.
V2R = 'v2r' in FLAGS
V2BUG = OPT.get('v2bug', '')   # CONTROL ONLY: 'p1p2' = the row builder reads every 7's two privates swapped (base terms and IN); 'h6' = every 6's h key
# with its two outer links (w_{j+2}, w_{j-2}) swapped; a rebuild must FAIL
V2TOL = float(OPT.get('v2tol', '1e-9'))
V2STAT = collections.Counter()
_V2XON = 'xon' in FLAGS
_V2_NEG = -1.0e18
_V2_Q = np.arange(25)
_V2_QX = np.array([1 << (q // 5) for q in range(25)], dtype=np.uint8)   # state q of site j = (x_j, y_{j+1}) = (q // 5 + 5, q % 5 + 5)
_V2_QY = np.array([1 << (q % 5) for q in range(25)], dtype=np.uint8)
if V2R:
    assert GKON and GKWIN and GKLEAF, 'v2r needs gkeys= gkwin gkleaf (the s86 key family)'
    assert F2B_ON and Q7 and Q7M and F2B7 and L3Q and 8 in LQVX and F16 and AC and AP and not V6 and not XO and not KSTAR and not EGNAMES and not GKPLANT and not FY2, \
        'v2r: needs the s86 family (f2b + f2b7 + q7 q7m, l3q l3qV=7,8, filt16, apexcls; no xo / v6 / kstar / edgekeys / gkplant / fy2)'
    log('v2r: KEYSPEC v2 receiver rows on d = 7, 8 as realisation rows (receiverV2); masked d = 7, 8 receiver rows are never built%s' % (
        ' [CONTROL v2bug=%s: row builder deliberately wrong]' % V2BUG if V2BUG else ''))
_V2_GKCUR = (lambda d, w, s: _p1r_gk_recv_terms_cur(d, w, s)) if P1R else (lambda d, w, s: gk_recv_terms(d, w, s))   # current key terms (no p1r)
def v2r_rho_str(rho): return ''.join('%d%d' % (x_, y_) for x_, y_ in rho)
def v2r_rho_parse(r, d):
    assert isinstance(r, str) and len(r) == 2 * d and all(ch in '56789' for ch in r), ('v2r: bad rho', r, d)
    return [(int(r[2 * j]), int(r[2 * j + 1])) for j in range(d)]
def _v2r_parse_row(d, lk, sv):
    assert d in (7, 8), ('v2r: receiver degree must be 7 or 8', d)
    assert isinstance(lk, str) and isinstance(sv, str) and len(lk) == d and len(sv) == d and all(ch in '56789' for ch in lk + sv), ('v2r: bad label', d, lk, sv)
    return [int(ch) for ch in lk], [int(ch) for ch in sv]
def _v2r_fixed(d, lk, sv, w, s):
    """(dom, fixed, cf0): domains, the masked row minus its envelope entries, the masked row (below the gkeys wrapper, no key terms)"""
    cf0 = _orig_recv_coef_R2_gk(d, lk, sv, _V2XON)
    assert not any(k[0] == 'ks' for k in cf0), 'v2r: key terms below the gkeys wrapper'
    dom, base = p1r_domains(d, w, s)
    got = collections.Counter({k: v for k, v in cf0.items() if k[0] in ('M', 'Q', 'lQ') and v})
    assert got == base, ('v2r: domains do not match the row base terms', d, lk, sv, sorted(got.items(), key=str), sorted(base.items(), key=str))
    fixed = {k: v for k, v in cf0.items() if k[0] not in ('M', 'Q', 'lQ') and v}
    return dom, fixed, cf0
def _v2r_copy(d, w, s, j, x_, y_):
    """the base terms of group j's copy (x_, y_): list of (column, coefficient)"""
    n = d; U = d; W_ = lambda k: w[k % n]; S_ = lambda k: s[k % n]
    if w[j] == 6:
        if V2BUG == 'h6': return [(('h', h2_of((U, W_(j + 1), S_(j), x_, S_(j - 1), W_(j - 1)), W_(j - 2), W_(j + 2))), 1)]   # CONTROL: the 6's two outer links swapped
        return [(('h', h2_of((U, W_(j + 1), S_(j), x_, S_(j - 1), W_(j - 1)), W_(j + 2), W_(j - 2))), 1)]
    if w[j] == 7:
        out = collections.Counter({('q', qkey((U, W_(j + 1), S_(j), x_, y_, S_(j - 1), W_(j - 1)))): 1})
        V = () if d == 7 else (8,)
        for sgn, let in ((1, x_), (-1, y_)):
            c_ = W_(j + sgn); a_ = S_(j) if sgn == 1 else S_(j - 1)
            if c_ <= 6 and a_ <= 6: out[('lq', V + (c_, a_, let))] += 1
        return sorted(out.items(), key=str)
    return []
def v2r_keyarrays(keys=None):
    if keys is None: return _GK_UM, _GK_VM, _GK_M
    return (np.array([k['um'] for k in keys], dtype=np.uint8), np.array([k['vm'] for k in keys], dtype=np.uint8), np.stack([k['m'] for k in keys]).astype(np.uint8))
def v2r_keycounts(d, w, s, rho, KA=None):
    """(OUT, IN) per key on the exact-letter picture of realisation rho (gk_slots; every position a single letter, so IN is exact)"""
    UM, VM, M = v2r_keyarrays() if KA is None else KA
    A = [_gkbit(x) for x in s]
    PVx = [None if w[j] == 5 else (1 << (rho[j][1] - 5), 1 << (rho[j][0] - 5)) for j in range(d)]   # PV side 0 = next to s_{j-1} = y_j, side 1 = x_j
    (ou, ov, oV), (iu, iv, iV) = gk_slots(d, w, A, PVx)
    pay = (((oV[None, :, :] & ~M[:, None, :]) == 0).all(axis=2) & ((ou[None, :] & ~UM[:, None]) == 0) & ((ov[None, :] & ~VM[:, None]) == 0)).sum(axis=1)
    get = (((iV[None, :, :] & M[:, None, :]) != 0).all(axis=2) & ((iu[None, :] & UM[:, None]) != 0) & ((iv[None, :] & VM[:, None]) != 0)).sum(axis=1)
    return pay.astype(np.int64), get.astype(np.int64)
def _v2r_kconst(d, w, s, keymode, cf0):
    """key terms independent of rho (keymode 'p1r': the p1_r coefficient; 'cur': the current coefficient); restricted-LP checks only"""
    if keymode == 'cur': return dict(_V2_GKCUR(d, w, s))
    r = p1r_core(d, w, s, _GK_UM, _GK_VM, _GK_M, base_cf=cf0)
    return dict(_V2_GKCUR(d, w, s) if r['empty'] else _gk_cf(r['pay'], r['inmax'], -1))
def _v2r_assemble(d, w, s, fixed, R, keymode='exact', kconst=None):
    """fixed + the copies' base terms + the key terms of realisation R (list of (x_j, y_j)); integer coefficient dict"""
    Rb = [((y_, x_) if (V2BUG == 'p1p2' and w[j] == 7) else (x_, y_)) for j, (x_, y_) in enumerate(R)]   # CONTROL: 7's privates swapped
    cf = collections.Counter(fixed)
    for j in range(d):
        for k_, v_ in _v2r_copy(d, w, s, j, *Rb[j]): cf[k_] += v_
    if keymode == 'exact':
        pay, get = v2r_keycounts(d, w, s, Rb)
        for k, nm in enumerate(GKNAMES):
            v = int(get[k]) - int(pay[k])
            if v: cf[('ks', nm)] += v
    else:
        assert keymode in ('p1r', 'cur') and kconst is not None, keymode
        for k_, v_ in kconst.items(): cf[k_] += v_
    return {k_: int(v_) for k_, v_ in cf.items() if v_}
def v2r_row(d, lk, sv, rho, keymode='exact'):
    """the realisation row (integer coefficient dict, without t) of receiver (d, lk, sv) at rho (string or list of pairs), rebuilt from the
    label alone (lowerR2, dualexport, warm V2 lines); asserts rho in the domain product.  keymode: 'exact' (KEYSPEC v2: IN(K; rho) - OUT(K));
    'p1r' (the single-row p1_r coefficient, max IN - OUT) and 'cur' (the current coefficient) only for the restricted-LP checks."""
    w, s = _v2r_parse_row(d, lk, sv)
    R = v2r_rho_parse(rho, d) if isinstance(rho, str) else [tuple(p_) for p_ in rho]
    assert len(R) == d, ('v2r: rho length', d, R)
    dom, fixed, cf0 = _v2r_fixed(d, lk, sv, w, s)
    assert all(dom), ('v2r: empty domain (the row has no realisation)', d, lk, sv)
    for j in range(d): assert R[j] in dom[j], ('v2r: rho outside the domain', d, lk, sv, j, R[j])
    return _v2r_assemble(d, w, s, fixed, R, keymode, None if keymode == 'exact' else _v2r_kconst(d, w, s, keymode, cf0))
def v2r_struct(d, lk, sv, KA=None, keymode='exact'):
    """DP data of one receiver: dom, fixed, per group {copy: terms}, OUT per key, live IN slot entries per factor i (key index, the key's
    sets at the four private positions read (x_{i-1}, y_i, x_i, y_{i+1})); None if some domain is empty (no realisation)"""
    w, s = _v2r_parse_row(d, lk, sv)
    UM, VM, M = v2r_keyarrays() if KA is None else KA
    dom, fixed, cf0 = _v2r_fixed(d, lk, sv, w, s)
    if not all(dom): return None
    copies = [{p_: _v2r_copy(d, w, s, j, *p_) for p_ in sorted(dom[j])} for j in range(d)]
    X = [_p1r_bits({a_ for a_, _ in D}) for D in dom]; Y = [_p1r_bits({b_ for _, b_ in D}) for D in dom]
    A = [_gkbit(x) for x in s]
    PV2 = [None if w[j] == 5 else (Y[j], X[j]) for j in range(d)]
    (ou, ov, oV), (iu, iv, iV) = gk_slots(d, w, A, PV2)
    for i in range(d):   # the slot readings of the private positions are exactly (X_{i-1}, Y_i, X_i, Y_{i+1}) (p1r's layout)
        for t_, sg in ((0, 1), (1, -1)):
            r = _P1R_RD[sg]; v = iV[2 * i + t_]
            assert (int(v[r[0]]), int(v[r[1]]), int(v[r[2]]), int(v[r[3]])) == (X[(i - 1) % d], Y[i], X[i], Y[(i + 1) % d]), ('v2r: slot reading', d, lk, sv, i, sg)
    pay = (((oV[None, :, :] & ~M[:, None, :]) == 0).all(axis=2) & ((ou[None, :] & ~UM[:, None]) == 0) & ((ov[None, :] & ~VM[:, None]) == 0)).sum(axis=1)
    FX = _P1R_FIXCOL
    live = ((iV[None, :, :][:, :, FX] & M[:, None, :][:, :, FX]) != 0).all(axis=2) & ((iu[None, :] & UM[:, None]) != 0) & ((iv[None, :] & VM[:, None]) != 0)   # (nk, 2d)
    ent = []
    for i in range(d):
        ks_ = []; ms_ = []
        for t_, sg in ((0, 1), (1, -1)):
            kk = np.nonzero(live[:, 2 * i + t_])[0]
            if len(kk): ks_.append(kk); ms_.append(M[kk][:, list(_P1R_RD[sg])])
        ent.append((np.concatenate(ks_), np.concatenate(ms_)) if ks_ else (np.zeros(0, dtype=np.int64), np.zeros((0, 4), dtype=np.uint8)))
    return {'d': d, 'lk': lk, 'sv': sv, 'w': w, 's': s, 'dom': dom, 'fixed': fixed, 'copies': copies, 'pay': pay.astype(np.int64), 'ent': ent, 'keymode': keymode,
            'kconst': None if keymode == 'exact' else _v2r_kconst(d, w, s, keymode, cf0)}
def v2r_dp(st, colval, xk):
    """max over realisations of value(rho; x) - fixed(x) (the rho-dependent part incl. -OUT), and the argmax rho (deterministic: first
    maximiser in state order).  colval(col) -> float for base columns; xk = key amounts (array over the struct's keys).  Exact max-plus
    product round the d-cycle of sites Q_j = (x_j, y_{j+1}); factor i = base of group i (Q_i.x, Q_{i-1}.y), -inf off dom_i, + key slots."""
    d = st['d']; F = []
    for i in range(d):
        G = np.full((5, 5), _V2_NEG)
        for (x_, y_), terms in st['copies'][i].items(): G[x_ - 5, y_ - 5] = sum(c_ * colval(k_) for k_, c_ in terms)
        Fi = G[_V2_Q[None, :] // 5, _V2_Q[:, None] % 5]          # Fi[qp, q] = G[x_i = q.x, y_i = qp.y]
        if st['keymode'] == 'exact':
            kk, mm = st['ent'][i]
            if len(kk):
                a_ = xk[kk]; nz = a_ != 0
                if nz.any():
                    m = mm[nz]
                    L = (((_V2_QX[None, :] & m[:, 0:1]) != 0) & ((_V2_QY[None, :] & m[:, 1:2]) != 0)).astype(np.float64)
                    R = (((_V2_QX[None, :] & m[:, 2:3]) != 0) & ((_V2_QY[None, :] & m[:, 3:4]) != 0)).astype(np.float64)
                    Fi = Fi + (L * a_[nz][:, None]).T @ R
        F.append(Fi)
    P = F[1]; args = []
    for i in range(2, d):
        S_ = P[:, :, None] + F[i][None, :, :]
        a_ = S_.argmax(axis=1); args.append(a_); P = np.take_along_axis(S_, a_[:, None, :], axis=1)[:, 0, :]
    T = P + F[0].T
    fl = int(T.argmax()); c, ql = divmod(fl, 25); best = float(T[c, ql])
    if best < _V2_NEG / 2: return None
    Q = [0] * d; Q[0] = c; Q[d - 1] = ql
    for i in range(d - 1, 1, -1): Q[i - 1] = int(args[i - 2][c, Q[i]])
    rho = [(Q[j] // 5 + 5, Q[(j - 1) % d] % 5 + 5) for j in range(d)]
    if st['keymode'] == 'exact': best -= float(np.dot(xk, st['pay']))
    return best, rho
def v2r_eval(cf, colval):
    return float(sum(v_ * colval(k_) for k_, v_ in cf.items()))
def v2r_best(st, colval, xk, check=True):
    """(value of the max-row at the point, rho*, the realisation row of rho*); the row is assembled with the exact-letter picture
    (gk_slots, as lowerR2's rebuild) and its value at the point is checked against the DP max (two independent readings of the slots)"""
    r = v2r_dp(st, colval, xk)
    if r is None: return None
    dpv, rho = r
    cf = _v2r_assemble(st['d'], st['w'], st['s'], st['fixed'], rho, st['keymode'], st['kconst'])   # the row by gk_slots on the exact picture (lowerR2 rebuilds the same with v2r_row)
    val = v2r_eval(cf, colval)
    fx = v2r_eval(st['fixed'], colval) + (v2r_eval(st['kconst'], colval) if st['kconst'] else 0.0)
    if check and abs(val - (fx + dpv)) > 1e-7 * max(1.0, abs(val)):
        V2STAT['DP vs row MISMATCH'] += 1
        raise AssertionError('v2r: DP value %.12g != row value %.12g at %s/%s rho %s' % (fx + dpv, val, st['lk'], st['sv'], v2r_rho_str(rho)))
    return val, v2r_rho_str(rho), cf
def v2r_colval_dict(D):
    return lambda k_: D.get(k_, 0.0)
def v2r_xk_dict(D):
    return np.array([float(D.get(('ks', nm_), 0.0)) for nm_ in GKNAMES])

# ---------------- commands ----------------
def _v2r_cert_rows(C, mode, xon):
    """rows of a cert for the restricted LP: [(info, cf, tc, dc, sense)] with the d = 7 / 8 receivers marked for the mode's treatment"""
    SR = {(wd, tuple(map(str, b))): cf for wd, cf, b in R2_sender_rows()}
    out = []; rec = []
    for c in C:
        row = c['row']; kd = row[0]
        if kd == 'senderR2': out.append((tuple(row), dict(SR[(row[1], tuple(map(str, row[2])))]), 1.0, 1.0, 'ge'))
        elif kd == 'cons2':
            assert C6LE; out.append((('cons2', list(row[1]), list(row[2])), {k_: v_ for k_, v_ in cons2_coef(tuple(row[1]), tuple(row[2])).items() if v_}, -1.0, 0.0, 'le'))
        elif kd == 'mrowR2': out.append((tuple(row), {('h', tuple(row[2])): 1, ('M', tuple(row[1])): -1}, 0.0, 0.0, 'le'))
        elif kd == 'mrowQ': out.append((tuple(row), {('q', tuple(row[2])): 1, ('Q', tuple(row[1])): -1}, 0.0, 0.0, 'le'))
        elif kd == 'mrowL': out.append((tuple(row), {('lq', tuple(row[2])): 1, ('lQ', tuple(row[1])): -1}, 0.0, 0.0, 'le'))
        elif kd == 'receiverR2':
            d, lk, sv = int(row[1]), row[2], row[3]
            if d in (7, 8):
                if mode in ('mask', 'p1r'):
                    w = [int(ch) for ch in lk]; s = [int(ch) for ch in sv]
                    cf = collections.Counter(_orig_recv_coef_R2_gk(d, lk, sv, xon))
                    if mode == 'mask': kt = _V2_GKCUR(d, w, s)
                    else:
                        r = p1r_core(d, w, s, _GK_UM, _GK_VM, _GK_M, base_cf=dict(cf)); kt = _V2_GKCUR(d, w, s) if r['empty'] else _gk_cf(r['pay'], r['inmax'], -1)
                    for k_, v_ in kt.items(): cf[k_] += v_
                    out.append((('receiverR2', d, lk, sv), {k_: v_ for k_, v_ in cf.items() if v_}, -1.0, float(d - 6), 'le'))
                else: rec.append((d, lk, sv))
            else: out.append((('receiverR2', d, lk, sv), dict(recv_coef_R2(d, lk, sv, xon)), -1.0, float(d - 6), 'le'))
        else: raise Exception('v2restricted: row type %s not handled' % kd)
    return out, rec
def _v2r_bounds(k):
    """column bounds exactly as cmd_solveR2's col()"""
    inf = float('inf'); XC = float(OPT.get('xcap', '3'))
    lo = -inf if k[0] == 't' else -XC if k[0] == 'XQ' else 0.0
    hi = (XC if k[0] in ('x', 'xo', 'XQ') else DCAP if k[0] == 'D' else LQCAP if k[0] == 'lq' else (FBCAP if FBCAP is not None else inf) if k[0] == 'fb'
          else ZCAP if (ZR and k[0] in ('z', 'zr', 'rr')) else Z6CAP if k[0] == 'z6' else Q7CAP if (Q7CAP is not None and k[0] == 'q') else KSCAP if k[0] == 'ks' else inf)
    return lo, hi
def cmd_v2restricted():
    """restricted LP: min t over the rows of cert= only (columns bounded as solveR2), with the d = 7 / 8 receiver rows as
    v2mode = mask (current key coefficients) | p1r (p1_r coefficients) | v2 (KEYSPEC v2 realisation rows, exact keys) | v2p1rkeys / v2curkeys
    (realisation rows with the keys held at the p1_r / current coefficients).  Realisation rows are added by the DP at each LP point until no
    d = 7 / 8 receiver of the cert exceeds d - 6 + t + v2tol.  v2out= writes the final dual as a cert (receiverV2 rows) for lowerR2."""
    import highspy, time as _tm
    load_patterns(); l3q_load(); kt_load()
    xon = 'xon' in FLAGS; mode = OPT.get('v2mode', 'v2'); assert mode in ('mask', 'p1r', 'v2', 'v2p1rkeys', 'v2curkeys'), mode
    raw = open(OPT['cert'], 'rb').read(); C = json.loads(raw)
    log('v2restricted: cert %s md5 %s, %d rows %s; mode %s; keys %d (md5 %s)' % (OPT['cert'], hashlib.md5(raw).hexdigest()[:8], len(C), dict(collections.Counter(c['row'][0] for c in C)), mode, len(GKNAMES), GKMD5))
    T0 = _tm.time(); base, rec = _v2r_cert_rows(C, mode, xon)
    h = highspy.Highs(); h.setOptionValue('output_flag', False); inf = highspy.kHighsInf
    for o_ in ('primal_feasibility_tolerance', 'dual_feasibility_tolerance'): h.setOptionValue(o_, float(OPT.get('v2lptol', '1e-10')))
    cols = {}; info = []
    def col(k_):
        if k_ not in cols:
            cols[k_] = len(cols); lo, hi = _v2r_bounds(k_); h.addVar(lo, hi)
        return cols[k_]
    jt = col(('t',)); h.changeColCost(jt, 1.0)
    def addrow(cf, tc, dc, sense, inf_):
        idx = [col(k_) for k_ in cf] + [jt]; val = [float(v_) for v_ in cf.values()] + [tc]
        if sense == 'ge': h.addRow(dc, inf, len(idx), np.array(idx, dtype=np.int32), np.array(val))
        else: h.addRow(-inf, dc, len(idx), np.array(idx, dtype=np.int32), np.array(val))
        info.append(inf_)
    for inf_, cf, tc, dc, se in base: addrow(cf, tc, dc, se, inf_)
    km = {'v2': 'exact', 'v2p1rkeys': 'p1r', 'v2curkeys': 'cur'}.get(mode)
    ST = []; nempty = 0; have = set(); nreal = collections.Counter()
    for d, lk, sv in rec:
        st = v2r_struct(d, lk, sv, keymode=km)
        if st is None: nempty += 1; continue
        ST.append(st)
    log('v2restricted: %d base rows, %d d = 7 / 8 receivers (%d with an empty domain, dropped); setup %.1fs' % (len(base), len(rec), nempty, _tm.time() - T0))
    def addreal(st, rho, cf):
        key = (st['d'], tuple(sorted(cf.items(), key=str)))
        if key in have: return False
        have.add(key); nreal[(st['d'], st['lk'], st['sv'])] += 1
        addrow(cf, -1.0, float(st['d'] - 6), 'le', ('receiverV2', st['d'], st['lk'], st['sv'], rho)); return True
    # seed: every receiver's argmax at the seed point (v2seed= sol json, else 0)
    SD = load_feas_cols(OPT['v2seed']) if 'v2seed' in OPT else {}
    cv0 = v2r_colval_dict(SD); xk0 = v2r_xk_dict(SD)
    for st in ST:
        r = v2r_best(st, cv0, xk0)
        addreal(st, r[1], r[2])
    log('v2restricted: seeded %d realisation rows at %s' % (len(have), OPT.get('v2seed', 'x = 0')))
    hist = []; t = None
    for it in range(int(OPT.get('v2maxit', '500'))):
        t1 = _tm.time(); h.run(); st_ = h.modelStatusToString(h.getModelStatus())
        sol = h.getSolution(); xv = np.array(sol.col_value); t = float(xv[jt])
        nx = len(xv); colv = lambda k_: float(xv[cols[k_]]) if (k_ in cols and cols[k_] < nx) else 0.0   # columns created after this solve (new rows' terms) read 0 (feasible: every lower bound <= 0)
        xk = np.array([colv(('ks', nm_)) for nm_ in GKNAMES])
        nadd = 0; worst = -1e9; nv = 0; t2 = _tm.time()
        for st in ST:
            val, rho, cf = v2r_best(st, colv, xk)
            ex = val - (st['d'] - 6) - t; worst = max(worst, ex)
            if ex > V2TOL:
                nv += 1; nadd += addreal(st, rho, cf)
        hist.append((it, t, nv, nadd, worst))
        log('v2restricted it %d: t = %.12f (%s, %.1fs), receivers above d - 6 + t + %g: %d, rows added %d, worst excess %.3e, realisation rows %d (DP %.1fs)' % (
            it, t, st_, t2 - t1, V2TOL, nv, nadd, worst, len(have), _tm.time() - t2))
        if nv and not nadd: log('v2restricted: violated receivers whose argmax row is already in the LP (LP tolerance); stopping'); break
        if not nv: break
    xv = np.array(h.getSolution().col_value); duals = np.array(h.getSolution().row_dual)
    dist = collections.Counter(nreal.values())
    log('V2RESTRICTED %s: t = %.12f after %d LP solves; %d LP rows (%d base + %d realisation rows over %d receivers; rows per receiver %s); %.0fs' % (
        mode, t, len(hist), h.getNumRow(), len(base), len(have), len(nreal), dict(sorted(dist.items())), _tm.time() - T0))
    ku = sorted(((float(xv[i]), k_[1]) for k_, i in cols.items() if k_[0] == 'ks' and xv[i] > 1e-9), reverse=True)[:25]
    log('  key amounts (top 25): %s' % ' '.join('%s=%.6f' % (k_, v_) for v_, k_ in ku))
    # scipy linprog (W6b's solve) on the final row set, default and tight tolerances
    try:
        import scipy.sparse as _sp
        from scipy.optimize import linprog as _lp
        nr = h.getNumRow(); nc = h.getNumCol(); lp_ = h.getLp(); am = lp_.a_matrix_
        Acsc = _sp.csc_matrix((np.array(am.value_), np.array(am.index_), np.array(am.start_)), shape=(nr, nc)); Ar = Acsc.tocsr()
        rl = np.array(lp_.row_lower_); ru = np.array(lp_.row_upper_)
        Aub = _sp.vstack([Ar[np.isfinite(ru)], -Ar[np.isfinite(rl)]]).tocsr(); bub = np.concatenate([ru[np.isfinite(ru)], -rl[np.isfinite(rl)]])
        bnd = list(zip([None if not np.isfinite(v_) else v_ for v_ in lp_.col_lower_], [None if not np.isfinite(v_) else v_ for v_ in lp_.col_upper_]))
        cc = np.zeros(nc); cc[jt] = 1.0
        for meth, opt_ in (('highs', {}), ('highs-ds', {'primal_feasibility_tolerance': 1e-10, 'dual_feasibility_tolerance': 1e-10}), ('highs-ipm', {'primal_feasibility_tolerance': 1e-10, 'dual_feasibility_tolerance': 1e-10})):
            r2 = _lp(cc, A_ub=Aub, b_ub=bub, bounds=bnd, method=meth, options=opt_)
            log('  scipy linprog %-9s on the final rows: status %d t = %.12g (row viol %.2g)' % (meth, r2.status, r2.x[jt] if r2.status == 0 else float('nan'), float(max(0.0, (Aub @ r2.x - bub).max())) if r2.status == 0 else float('nan')))
    except Exception as e_: log('  scipy re-solve failed: %r' % (e_,))
    if 'v2out' in OPT:
        cert = [{'w': float(dv), 'row': list(info[i])} for i, dv in enumerate(duals) if abs(dv) > 1e-11]
        json.dump(cert, open(OPT['v2out'], 'w'), indent=0)
        log('v2restricted: dual written to %s (%d rows, %s)' % (OPT['v2out'], len(cert), dict(collections.Counter(c['row'][0] for c in cert))))
    if OPT.get('v2json'):
        json.dump({'mode': mode, 't': t, 'iterations': len(hist), 'hist': hist, 'lp_rows': h.getNumRow(), 'base_rows': len(base), 'realisation_rows': len(have),
                   'receivers': len(nreal), 'rows_per_receiver': dict(sorted(dist.items())), 'keys_top': [[k_, v_] for v_, k_ in ku], 'cert': OPT['cert']}, open(OPT['v2json'], 'w'), indent=1, default=str)
def cmd_v2rtest():
    """unit tests of the v2r row builder and DP (no LP): (a) W6b test_vectors.json: OUT, IN max / min by the DP with one key; (b) on the
    d = 7 / 8 receivers of cert=: per key DP max / min IN vs p1r_core (all keys); at v2npt random points per row: DP max = builder row value
    at the argmax (checked in v2r_best), builder value <= DP max on v2nsamp random realisations, and = the exhaustive max over the domain
    product (builder on every realisation) when the product has at most v2bf realisations; keymode cur / p1r rows carry the masked row's keys."""
    import random as _rd, time as _tm, itertools as _it
    load_patterns(); l3q_load(); kt_load(); xon = 'xon' in FLAGS; bad = 0; T0 = _tm.time()
    KS2 = '/mnt/project-files/swarm/round6/W6-rule-grammar/round16/keyspec2'
    TV = json.load(open(os.path.join(KS2, 'test_vectors.json'))); na = 0
    for e in TV:
        d, lk, sv = e['row'].split('/'); d = int(d)
        k = gk_parse('T ' + e['rule']); KA = v2r_keyarrays([k])
        st = v2r_struct(d, lk, sv, KA=KA); z = lambda k_: 0.0
        hi = v2r_dp(st, z, np.array([1.0])); lo = v2r_dp(st, z, np.array([-1.0]))
        OUT = int(st['pay'][0]); inmax = int(round(hi[0])) + OUT; inmin = OUT - int(round(lo[0]))
        pa, ge = v2r_keycounts(d, st['w'], st['s'], hi[1], KA)
        ok = (OUT, inmax, inmin, inmax - OUT) == (e['OUT'], e['IN_max'], e['IN_min'], e['v2']) and int(ge[0]) == inmax and int(pa[0]) == OUT
        na += ok; bad += not ok
        log('  (a) %-22s %-8s want OUT %d IN %d..%d v2 %d | DP OUT %d IN %d..%d v2 %d; builder IN at the argmax %d  %s' % (e['row'], e['key'], e['OUT'], e['IN_min'], e['IN_max'], e['v2'], OUT, inmin, inmax, inmax - OUT, int(ge[0]), 'ok' if ok else 'MISMATCH'))
    log('V2R-TEST (a): %d / %d test vectors reproduced' % (na, len(TV)))
    if 'cert' not in OPT: log('V2R-TEST: %s (%d failures)' % ('PASS' if bad == 0 else 'FAIL', bad)); return
    C = json.load(open(OPT['cert'])); RR = [(int(c['row'][1]), c['row'][2], c['row'][3]) for c in C if c['row'][0] == 'receiverR2' and int(c['row'][1]) in (7, 8)]
    NPT = int(OPT.get('v2npt', '2')); NS = int(OPT.get('v2nsamp', '100')); BF = int(OPT.get('v2bf', '1500')); rng = _rd.Random(int(OPT.get('seed', '1')))
    cnt = collections.Counter(); nk = len(GKNAMES); tdp = 0.0; tbf = 0.0
    def rcol(seed):
        cache = {}
        def f(k_):
            if k_ not in cache: cache[k_] = int(hashlib.md5(('%d %r' % (seed, k_)).encode()).hexdigest()[:8], 16) / 2.0 ** 32
            return cache[k_]
        return f
    for (d, lk, sv) in RR:
        w = [int(ch) for ch in lk]; s = [int(ch) for ch in sv]
        st = v2r_struct(d, lk, sv)
        if st is None: cnt['empty domain'] += 1; continue
        cnt['rows'] += 1; dom = st['dom']
        # per key max / min IN vs p1r_core
        r = p1r_core(d, w, s, _GK_UM, _GK_VM, _GK_M, want_min=True, base_cf=_orig_recv_coef_R2_gk(d, lk, sv, xon))
        z = lambda k_: 0.0; t_ = _tm.time()
        for k in range(nk):
            if not len(st['ent']) or not any((kk == k).any() for kk, _ in st['ent']):
                mx_ = mn_ = 0
            else:
                e_ = np.zeros(nk); e_[k] = 1.0; mx_ = int(round(v2r_dp(st, z, e_)[0])) + int(st['pay'][k])
                e_[k] = -1.0; mn_ = int(st['pay'][k]) - int(round(v2r_dp(st, z, e_)[0]))
            cnt['key pairs'] += 1
            if (mx_, mn_, int(st['pay'][k])) != (int(r['inmax'][k]), int(r['inmin'][k]), int(r['pay'][k])):
                bad += 1; cnt['key pair MISMATCH vs p1r'] += 1
                if cnt['key pair MISMATCH vs p1r'] <= 5: log('  (b) key %s on %d/%s/%s: DP IN %d..%d OUT %d; p1r IN %d..%d OUT %d' % (GKNAMES[k], d, lk, sv, mn_, mx_, st['pay'][k], r['inmin'][k], r['inmax'][k], r['pay'][k]))
        tdp += _tm.time() - t_
        # random points
        prod = 1
        for D in dom: prod *= len(D)
        cnt['realisations total'] += prod
        dlist = [sorted(D) for D in dom]
        dom0, fixed, cf0 = _v2r_fixed(d, lk, sv, w, s)
        def bval(R, cv, xk):
            v = v2r_eval(fixed, cv)
            for j in range(d): v += sum(c_ * cv(k_) for k_, c_ in _v2r_copy(d, w, s, j, *R[j]))
            pa, ge = v2r_keycounts(d, w, s, R)
            return v + float(np.dot(xk, ge - pa))
        for ip in range(NPT):
            cv0 = rcol(rng.randrange(1 << 30)); xk = np.array([rng.choice((0.0, 0.0, rng.uniform(0, 3), -rng.uniform(0, 1))) for _ in range(nk)])
            KIX = {nm_: i_ for i_, nm_ in enumerate(GKNAMES)}
            cv = (lambda cv0_, xk_: (lambda k_: float(xk_[KIX[k_[1]]]) if k_[0] == 'ks' else cv0_(k_)))(cv0, xk)   # key columns read the amounts xk
            val, rho, cf = v2r_best(st, cv, xk)   # raises on DP value != builder value at the argmax
            cnt['points'] += 1
            assert v2r_row(d, lk, sv, rho) == cf
            for _ in range(NS):
                R = [rng.choice(D) for D in dlist]
                if bval(R, cv, xk) > val + 1e-9: bad += 1; cnt['sample ABOVE DP max'] += 1
                cnt['samples'] += 1
            if prod <= BF:
                t_ = _tm.time(); best = max(bval(R, cv, xk) for R in _it.product(*dlist)); tbf += _tm.time() - t_
                cnt['exhaustive points'] += 1; cnt['exhaustive realisations'] += prod
                if abs(best - val) > 1e-9 * max(1.0, abs(val)): bad += 1; cnt['exhaustive MISMATCH'] += 1; log('  (b) exhaustive %d/%s/%s: brute %.12g DP %.12g' % (d, lk, sv, best, val))
        # keymode cur / p1r: the key part of a realisation row equals the masked row's key part
        for km in ('cur', 'p1r'):
            cfk = v2r_row(d, lk, sv, [D[0] for D in dlist], km)
            want = _V2_GKCUR(d, w, s) if km == 'cur' else (_V2_GKCUR(d, w, s) if r['empty'] else _gk_cf(r['pay'], r['inmax'], -1))
            if {k_: v_ for k_, v_ in cfk.items() if k_[0] == 'ks'} != {k_: v_ for k_, v_ in want.items() if v_}: bad += 1; cnt['keymode %s MISMATCH' % km] += 1
    log('V2R-TEST (b): %s; per-key DP %.1fs, exhaustive %.1fs, total %.0fs' % (dict(cnt), tdp, tbf, _tm.time() - T0))
    log('V2R-STAT %s' % dict(V2STAT))
    log('V2R-TEST: %s (%d failures)' % ('PASS' if bad == 0 else 'FAIL', bad))
def _v2r_jcol(k_):
    """a column as JSON: [type, key] with tuples as lists (key names stay strings)"""
    f = lambda v: [f(u) for u in v] if isinstance(v, (tuple, list)) else v
    return [k_[0], f(k_[1])] if len(k_) == 2 else f(k_)
def cmd_v2rshow():
    """test vectors for V2ROW_SPEC.md: for every row of v2rows= (lines 'd link apex rho') the full decomposition of the realisation row
    (domains, masked envelope entries removed, fixed terms, each group's copy terms, every key's OUT / IN / coefficient, the row) -> v2show= json"""
    load_patterns(); l3q_load(); kt_load(); out = []
    for line in open(OPT['v2rows']):
        if not line.strip() or line.lstrip().startswith('#'): continue
        d, lk, sv, rho = line.split()[:4]; d = int(d)
        w, s = _v2r_parse_row(d, lk, sv); R = v2r_rho_parse(rho, d)
        dom, fixed, cf0 = _v2r_fixed(d, lk, sv, w, s)
        cf = v2r_row(d, lk, sv, rho)
        pay, get = v2r_keycounts(d, w, s, R)
        chk = collections.Counter(fixed); grp = []
        for j in range(d):
            T = _v2r_copy(d, w, s, j, *R[j])
            for k_, v_ in T: chk[k_] += v_
            grp.append({'j': j, 'w_j': w[j], 'domain': ('all 25 pairs' if w[j] >= 8 else sorted('%d%d' % p_ for p_ in dom[j])), 'copy': '%d%d' % R[j],
                        'terms': [[_v2r_jcol(k_), int(v_)] for k_, v_ in T]})
        keys = []
        for k, nm in enumerate(GKNAMES):
            if pay[k] or get[k]:
                keys.append({'key': nm, 'spec': GKEYS[k]['spec'], 'OUT': int(pay[k]), 'IN': int(get[k]), 'coef': int(get[k]) - int(pay[k])})
                if get[k] != pay[k]: chk[('ks', nm)] += int(get[k]) - int(pay[k])
        assert {k_: v_ for k_, v_ in chk.items() if v_} == cf, ('v2rshow: decomposition != v2r_row', d, lk, sv, rho)
        e = {'id': ['receiverV2', d, lk, sv, rho], 'bound': 'row - t <= %d' % (d - 6),
             'masked_envelope_entries_removed': [[_v2r_jcol(k_), int(v_)] for k_, v_ in sorted(cf0.items(), key=str) if k_[0] in ('M', 'Q', 'lQ') and v_],
             'fixed': [[_v2r_jcol(k_), int(v_)] for k_, v_ in sorted(fixed.items(), key=str)], 'groups': grp, 'keys_nonzero_IN_or_OUT': keys,
             'row': [[_v2r_jcol(k_), int(v_)] for k_, v_ in sorted(cf.items(), key=str)], 'row_md5': hashlib.md5(json.dumps([[_v2r_jcol(k_), int(v_)] for k_, v_ in sorted(cf.items(), key=str)]).encode()).hexdigest()[:8]}
        out.append(e)
        log('V2R-SHOW %d/%s/%s rho %s: %d fixed, %d copy terms, %d keys with IN or OUT (%d nonzero coef), row %d entries md5 %s' % (
            d, lk, sv, rho, len(fixed), sum(len(g['terms']) for g in grp), len(keys), sum(1 for k_ in keys if k_['coef']), len(cf), e['row_md5']))
    json.dump(out, open(OPT['v2show'], 'w'), indent=1)
    log('V2R-SHOW: %d rows -> %s' % (len(out), OPT['v2show']))
