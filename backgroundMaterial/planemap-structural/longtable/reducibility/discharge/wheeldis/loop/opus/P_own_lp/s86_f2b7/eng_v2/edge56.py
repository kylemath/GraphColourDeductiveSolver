# edge56.py (s85_edge56, Opus team): generic 2-ball EDGE keys with payer and payee letters anywhere in {5,...,9}
# (W6 rounds 6-7).  Built from KEYSPEC.md (md5 0ee6b182) only, not from W6's code.  exec'd by pcheck.py after edgefam.py.
#
# Option gkeys=<file>: one key per line "NAME EDGE(U->V)[POS=SET ...]" (trailing "# ..." ignored); SET is a letter 5..9, S = {5,6},
# B = {7,8,9}, * = all, or {...} (e.g. {567}).  POS in S.L+-1..3, S.A+-1, R.L+-2; unlisted positions are wildcards.
# Amount column ('ks', NAME) in [0, kscap] (the K* / Team D EDGE namespace; NAME must differ from K1 and from edgekeys= names).
#
# Semantics (KEYSPEC 3-5).  A row is a picture: centre letter c, link letters W[0..n-1] (exact), apex masks A[i] (the apex between
# W[i] and W[i+1]), private masks PV[i] = (private next to A[i-1], private next to A[i]) for W[i] (None for a link 5; a link 6 has
# ONE private, given as the same mask twice).  Slots, per link vertex W[i] and chirality sg = +-1:
#   OUT (c pays W[i]), sg = +1: S.L+k = W[i+k], S.L-k = W[i-k] (k = 1..3); S.A+1 = A[i+1]; S.A-1 = A[i-2]; R.L+2 = A[i];
#       R.L-2 = A[i-1].  sg = -1 is the mirror (W[i-+k], A[i-2], A[i+1], A[i-1], A[i]).
#   IN (W[i] pays c), sg = +1: S.L+1 = W[i-1], S.L-1 = W[i+1], S.L+2 = A[i-1], S.L-2 = A[i], S.L+3 = W[i]'s private next to A[i-1]
#       (= A[i] if W[i] = 5), S.L-3 = W[i]'s private next to A[i] (= A[i-1] if W[i] = 5), S.A+1 = W[i-1]'s private next to A[i-1]
#       (= A[i-2] if W[i-1] = 5), S.A-1 = W[i+1]'s private next to A[i] (= A[i+1] if W[i+1] = 5), R.L+2 = W[i-2], R.L-2 = W[i+2].
#       sg = -1 is the mirror.
#   An OUT slot counts iff it SURELY matches (payer, payee and every position set inside the key's set); an IN slot counts iff it
#   POSSIBLY matches (every one of those sets meets the key's set, position by position).
#   Coefficient: sender rows (c = 5) OUT - IN; receiver and cons2 rows (c >= 7, c = 6) IN - OUT.
# Pictures:
#   receiver d = 7 (link w, apexes s exact): a link 6 at j has one private with mask amask(7, w_{j-2}, w_{j-1}, w_{j+1}, w_{j+2},
#       s_{j-2}, s_{j-1}, s_j, s_{j+1}) & ~extra6(7, w, s, j); a link 7 at j has two privates: the one next to s_j gets
#       L3T[(+1, w_{j+1}, w_{j+2}, w_{j+3}, w_{j+4}, s_j, s_{j-1})] & ~extra7(7, w, s, j, +1) when w_{j+1}, s_j <= 6, else the wildcard;
#       the one next to s_{j-1} likewise with (-1, w_{j-1}, w_{j-2}, w_{j-3}, w_{j-4}, s_{j-1}, s_j) and extra7(..., -1); link 8+ and
#       every other private: wildcard.
#   receiver d >= 8: link 6 private amask(min(d, 9), ...) & ~extra6 (d <= 9); every other private the wildcard (only enlarges IN
#       credit; no key has a payer >= 8, so a d >= 8 centre has no OUT slot that counts).
#   sender (w, H, Fn): apex A[k] = S if H[k] = 0, B if H[k] = 1 (wildcard if k is not a hat position); a link 6 at k has one private
#       with class S (Fn[k] = 0) or B (Fn[k] = 1); link 7+ privates wildcard.
#   cons2 (L, s): apex A[k] = S if ap(s_k) = 5 else B (apexcls; the exact letter without it); every private the wildcard.
GKFILE = OPT.get('gkeys'); GKON = GKFILE is not None
GKPLANT = 'gkplant' in FLAGS          # CONTROL ONLY: IN-slot S.A+1 (sg = +1) read on the wrong side of W[i-1]; gkselftest must FAIL
GKEYS = []
_GKB = {'5': 1, '6': 2, '7': 4, '8': 8, '9': 16, 'S': 3, 'B': 28, '*': 31}
GK_POS = ('S.L+1', 'S.L+2', 'S.L+3', 'S.L-1', 'S.L-2', 'S.L-3', 'S.A+1', 'S.A-1', 'R.L+2', 'R.L-2')
def gk_set(tok):
    if tok.startswith('{'):
        assert tok.endswith('}') and len(tok) > 2, 'gkeys: bad set %r' % tok
        m = 0
        for ch in tok[1:-1]:
            assert ch in '56789', 'gkeys: bad set %r' % tok
            m |= _GKB[ch]
        return m
    assert tok in _GKB, 'gkeys: bad set %r' % tok
    return _GKB[tok]
def gk_parse(line):
    m_ = re.match(r'^\s*(\S+)\s+EDGE\(([^)]*?)->([^)]*)\)(?:\[([^\]]*)\])?\s*(?:#.*)?$', line)
    assert m_, 'gkeys: bad line %r' % line
    nm, pu, pv, body = m_.groups()
    assert re.match(r'^[A-Za-z0-9_]+$', nm) and nm != 'K1', 'gkeys: bad name %r' % nm
    conds = {}
    for tok in (body or '').split():
        p_, s_ = tok.split('=')
        assert p_ in GK_POS and p_ not in conds, 'gkeys: bad position %r in %r' % (p_, line)
        conds[p_] = gk_set(s_)
    m = np.array([conds.get(p_, 31) for p_ in GK_POS], dtype=np.uint8)
    return {'name': nm, 'um': gk_set(pu), 'vm': gk_set(pv), 'm': m, 'spec': 'EDGE(%s->%s)[%s]' % (pu, pv, body or '')}
if GKON:
    assert F2B_ON and L3Q and F16 and AC and AP and not W19 and not PCAM and not XO and not FY and not V6, 'gkeys: needs the s75 stack (f2b + l3q + filt16 + apexcls)'
    for l_ in open(GKFILE):
        if l_.strip() and not l_.lstrip().startswith('#'): GKEYS.append(gk_parse(l_))
    assert len({k['name'] for k in GKEYS}) == len(GKEYS), 'gkeys: duplicate names'
    assert not ({k['name'] for k in GKEYS} & set(EGNAMES)), 'gkeys: names clash with edgekeys='
    log('gkeys: %d keys from %s (md5 %s): payer/payee pairs %s' % (len(GKEYS), GKFILE, hashlib.md5(open(GKFILE, 'rb').read()).hexdigest()[:8],
        dict(collections.Counter('%d->%d' % (k['um'], k['vm']) for k in GKEYS))))
GKNAMES = [k['name'] for k in GKEYS]
if GKON:
    _GK_UM = np.array([k['um'] for k in GKEYS], dtype=np.uint8); _GK_VM = np.array([k['vm'] for k in GKEYS], dtype=np.uint8)
    _GK_M = np.stack([k['m'] for k in GKEYS]).astype(np.uint8)            # (nk, 10)
def _gkbit(x): return 1 << (min(int(x), 9) - 5)
def gk_slots(c, W, A, PV):
    """(OUT, IN): each an (ub, vb, V) triple: payer letter bits (2n,), payee letter bits (2n,), position masks (2n, 10) in GK_POS order"""
    n = len(W); Wb = [_gkbit(x) for x in W]
    w = lambda k: Wb[k % n]; a = lambda k: A[k % n]
    def prv(j, side):   # side 0: next to A[j-1]; 1: next to A[j]
        j %= n; p = PV[j]
        return 31 if p is None else p[side]
    def pin(j, side):   # W[j]'s neighbour next to A[j-1] (side 0) / A[j] (side 1) beyond the apex, seen from c: for a 5 the other apex
        j %= n
        if W[j] == 5: return a(j) if side == 0 else a(j - 1)
        return prv(j, side)
    out_u, out_v, out_V, in_u, in_v, in_V = [], [], [], [], [], []
    cb = _gkbit(c)
    for i in range(n):
        out_u += [cb, cb]; out_v += [w(i), w(i)]
        out_V.append([w(i + 1), w(i + 2), w(i + 3), w(i - 1), w(i - 2), w(i - 3), a(i + 1), a(i - 2), a(i), a(i - 1)])
        out_V.append([w(i - 1), w(i - 2), w(i - 3), w(i + 1), w(i + 2), w(i + 3), a(i - 2), a(i + 1), a(i - 1), a(i)])
        in_u += [w(i), w(i)]; in_v += [cb, cb]
        # sg = +1: S.L+1 = W[i-1]; S.L+3 = W[i]'s private next to A[i-1]; S.A+1 = W[i-1]'s neighbour beyond A[i-1] (its side 1)
        if GKPLANT: in_V.append([w(i - 1), a(i - 1), pin(i, 0), w(i + 1), a(i), pin(i, 1), pin(i - 1, 0), pin(i + 1, 0), w(i - 2), w(i + 2)])   # CONTROL: S.A+1 on the wrong side of W[i-1]
        else: in_V.append([w(i - 1), a(i - 1), pin(i, 0), w(i + 1), a(i), pin(i, 1), pin(i - 1, 1), pin(i + 1, 0), w(i - 2), w(i + 2)])
        in_V.append([w(i + 1), a(i), pin(i, 1), w(i - 1), a(i - 1), pin(i, 0), pin(i + 1, 0), pin(i - 1, 1), w(i + 2), w(i - 2)])
    f = lambda x: np.array(x, dtype=np.uint8)
    return (f(out_u), f(out_v), f(out_V)), (f(in_u), f(in_v), f(in_V))
def gk_counts(c, W, A, PV):
    """(pay, get): int arrays over GKEYS: OUT slots that surely match, IN slots that possibly match"""
    (ou, ov, oV), (iu, iv, iV) = gk_slots(c, W, A, PV)
    sure = ((oV[None, :, :] & ~_GK_M[:, None, :]) == 0).all(axis=2) & ((ou[None, :] & ~_GK_UM[:, None]) == 0) & ((ov[None, :] & ~_GK_VM[:, None]) == 0)
    poss = ((iV[None, :, :] & _GK_M[:, None, :]) != 0).all(axis=2) & ((iu[None, :] & _GK_UM[:, None]) != 0) & ((iv[None, :] & _GK_VM[:, None]) != 0)
    return sure.sum(axis=1), poss.sum(axis=1)
def _gk_cf(pay, get, sign):
    cf = collections.Counter()
    for k, (p_, g_) in enumerate(zip(pay, get)):
        v = int(sign * (int(p_) - int(g_)))
        if v: cf[('ks', GKNAMES[k])] = v
    return cf
def gk_recv_picture(d, w, s):
    """receiver picture (KEYSPEC 5): apex masks exact letters; privates as documented at the top"""
    n = d; U = min(d, 9); A = [_gkbit(x) for x in s]; PV = []
    for j in range(n):
        x = w[j]
        if x == 5: PV.append(None)
        elif x == 6:
            if d <= 9:
                m = amask(U, w[(j - 2) % n], w[(j - 1) % n], w[(j + 1) % n], w[(j + 2) % n], s[(j - 2) % n], s[(j - 1) % n], s[j], s[(j + 1) % n])
                m &= ~f2bm.extra6(d, w, s, j)
            else: m = 31
            PV.append((m, m))
        elif x == 7 and d == 7:
            sides = []
            for sg in (-1, 1):   # side 0 = next to s_{j-1} (sg = -1), side 1 = next to s_j (sg = +1)
                cn = w[(j + sg) % n]; ap_ = s[j] if sg > 0 else s[(j - 1) % n]; o_ = s[(j - 1) % n] if sg > 0 else s[j]
                if cn <= 6 and ap_ <= 6:
                    key = (sg, cn, w[(j + 2 * sg) % n], w[(j + 3 * sg) % n], w[(j + 4 * sg) % n], ap_, o_)
                    assert key in L3T, 'gkeys: no L3T entry %r' % (key,)
                    sides.append(L3T[key] & ~f2bm.extra7(7, w, s, j, sg))
                else: sides.append(31)
            PV.append(tuple(sides))
        else: PV.append((31, 31))
    return A, PV
def gk_recv_terms(d, w, s):
    if not GKON: return collections.Counter()
    l3q_load(); kt_load()
    A, PV = gk_recv_picture(d, w, s)
    pay, get = gk_counts(d, w, A, PV)
    return _gk_cf(pay, get, -1)
def gk_sender_terms(w, H, Fn):
    if not GKON: return collections.Counter()
    n = 5; A = [31 if H.get(k) is None else (28 if H[k] else 3) for k in range(n)]; PV = []
    for k in range(n):
        if w[k] == 5: PV.append(None)
        elif w[k] == 6:
            m = 31 if Fn.get(k) is None else (28 if Fn[k] else 3); PV.append((m, m))
        else: PV.append((31, 31))
    pay, get = gk_counts(5, w, A, PV)
    return _gk_cf(pay, get, +1)
def gk_cons2_picture(L, s):
    A = [(28 if ap(x) >= 7 else 3) if AC else _gkbit(x) for x in s]
    PV = [None if x == 5 else (31, 31) for x in L]
    return A, PV
def gk_cons2_terms(L, s):
    if not GKON: return collections.Counter()
    A, PV = gk_cons2_picture(L, s)
    pay, get = gk_counts(6, L, A, PV)
    return _gk_cf(pay, get, -1)
_orig_recv_coef_R2_gk = recv_coef_R2
def recv_coef_R2(d, lk, sv, xon, tau=None):
    cf = _orig_recv_coef_R2_gk(d, lk, sv, xon, tau)
    if GKON:
        for k_, v_ in gk_recv_terms(d, [int(ch) for ch in lk], [int(ch) for ch in sv]).items():
            cf[k_] += v_
            if cf[k_] == 0: del cf[k_]
    return cf
_orig_cons2_coef_gk = cons2_coef
def cons2_coef(L, s):
    cf = _orig_cons2_coef_gk(L, s)
    if GKON:
        for k_, v_ in gk_cons2_terms(tuple(L), tuple(s)).items():
            cf[k_] += v_
            if cf[k_] == 0: del cf[k_]
    return cf
_orig_cons2_delta_gk = cons2_delta
def cons2_delta(L, GV, HV2):
    """with gkeys: + sum over keys of amount x coefficient, for every apex word (the coefficient depends on the apex classes only)"""
    D = _orig_cons2_delta_gk(L, GV, HV2)
    if GKON and any(KSV.get(nm_, 0.0) for nm_ in GKNAMES):
        am = np.array([KSV.get(nm_, 0.0) for nm_ in GKNAMES])
        cache = {}
        cls = np.where(SALL >= 2, 1, 0) if AC else SALL   # letter index >= 2 is 7+
        keyv = (cls * (np.array([2 ** k for k in range(6)]) if AC else np.array([5 ** k for k in range(6)]))).sum(axis=1)
        for kv in np.unique(keyv):
            idx = int(np.nonzero(keyv == kv)[0][0]); s_ = tuple(LET[v] for v in SALL[idx])
            A, PV = gk_cons2_picture(L, s_); pay, get = gk_counts(6, L, A, PV)
            cache[int(kv)] = float(np.dot(am, get - pay))
        D = D + np.array([cache[int(kv)] for kv in keyv])
    return D
def cmd_gkselftest():
    """KEYSPEC worked examples (section 6) and, with kstar data loaded, generic KS = K* (kstar_payee_slot / kstar_payer_slot) on
    random d = 7 rows"""
    l3q_load(); kt_load(); bad = 0
    ex = [('R', 7, (5, 5, 7, 5, 5, 7, 7), (5, 7, 7, 5, 7, 7, 7), {'A1': (4, 0), 'gk00_10': (2, 0), 'gk01_18': (0, 4), 'gk02_24': (0, 2), 'gk02_26': (2, 0)}),
          ('S', 5, (5, 5, 7, 7, 7), ({0: 1, 1: 1, 2: 0, 3: 1, 4: 1}, {}), {'gk01_18': (2, 0), 'gk02_26': (0, 1)}),
          ('C', 6, (5, 6, 7, 7, 6, 7), (7, 5, 5, 5, 5, 5), {'gk04_45': (1, 0), 'gk02_82': (1, 0)})]
    for kind, c, W, X, want in ex:
        if kind == 'R': A, PV = gk_recv_picture(7, list(W), list(X))
        elif kind == 'S':
            H, Fn = X; A = [28 if H[k] else 3 for k in range(5)]; PV = [None if x == 5 else (31, 31) for x in W]
        else: A, PV = gk_cons2_picture(W, X)
        pay, get = gk_counts(c, list(W), A, PV)
        for nm_, (p_, g_) in want.items():
            if nm_ not in GKNAMES: log('  gkselftest: key %s not loaded' % nm_); bad += 1; continue
            k = GKNAMES.index(nm_); ok = (int(pay[k]), int(get[k])) == (p_, g_)
            log('  gkselftest %s %s %s %s: pay %d get %d (KEYSPEC %d %d) %s' % (kind, ''.join(map(str, W)), ''.join(map(str, X)) if kind != 'S' else 'H11011', nm_, pay[k], get[k], p_, g_, 'ok' if ok else 'MISMATCH'))
            bad += not ok
    if 'KS' in GKNAMES:
        import random; rng = random.Random(int(OPT.get('seed', '1'))); k = GKNAMES.index('KS'); N = int(OPT.get('N', '20000')); nz = 0
        for _ in range(N):
            w = [rng.choice((5, 6, 7, 8, 9)) for _ in range(7)]; s = [rng.choice((5, 6, 7, 8, 9)) for _ in range(7)]
            if rng.random() < 0.7: w[rng.randrange(7)] = 7
            A, PV = gk_recv_picture(7, w, s); pay, get = gk_counts(7, w, A, PV)
            ref_get = sum(kstar_payee_slot(w, s, j, e1) for j in range(7) for e1 in (1, -1))
            ref_pay = sum(kstar_payer_slot(w, s, j, e1) for j in range(7) for e1 in (1, -1))
            if (int(pay[k]), int(get[k])) != (ref_pay, ref_get):
                bad += 1
                if bad <= 5: log('  gkselftest KS vs K*: w %s s %s: generic pay %d get %d, kstar pay %d get %d' % (w, s, pay[k], get[k], ref_pay, ref_get))
            nz += (ref_pay + ref_get) > 0
        log('  gkselftest KS vs K*: %d random d = 7 rows, %d with a K* slot' % (N, nz))
    # mirror test: K and mirror(K) (S.L+k <-> S.L-k, S.A+1 <-> S.A-1, R.L+2 <-> R.L-2) must count alike on every picture
    import random; rng = random.Random(int(OPT.get('seed', '1')) + 7); MIR = [3, 4, 5, 0, 1, 2, 7, 6, 9, 8]; nm = 0
    global _GK_M
    M0 = _GK_M.copy(); M1 = M0[:, MIR].copy()
    for _ in range(int(OPT.get('Nmir', '6000'))):
        kind = rng.choice('RSC')
        if kind == 'R':
            w = [rng.choice((5, 6, 7, 8, 9)) for _ in range(7)]; s_ = [rng.choice((5, 6, 7, 8, 9)) for _ in range(7)]; A, PV = gk_recv_picture(7, w, s_); c = 7
        elif kind == 'S':
            w = [rng.choice((5, 6, 7, 8, 9)) for _ in range(5)]; A = [rng.choice((3, 28, 31)) for _ in range(5)]
            PV = [None if x == 5 else ((lambda m: (m, m))(rng.choice((3, 28, 31))) if x == 6 else (31, 31)) for x in w]; c = 5
        else:
            w = [rng.choice((5, 6, 7, 8, 9)) for _ in range(6)]; A, PV = gk_cons2_picture(w, [rng.choice((5, 7)) for _ in range(6)]); c = 6
        _GK_M = M0; r0 = gk_counts(c, w, A, PV); _GK_M = M1; r1 = gk_counts(c, w, A, PV); _GK_M = M0
        if not (np.array_equal(r0[0], r1[0]) and np.array_equal(r0[1], r1[1])):
            nm += 1
            if nm <= 3: log('  gkselftest mirror: %s %s A %s: pay %s / %s' % (kind, w, A, list(r0[0]), list(r1[0])))
    log('  gkselftest mirror: %d pictures, %d with K != mirror(K)' % (int(OPT.get('Nmir', '6000')), nm)); bad += nm
    log('GKSELFTEST: %s (%d mismatches)' % ('PASS' if bad == 0 else 'FAIL', bad))
# ---------------- full-stack receivers: window bound of the IN (payee) side, flag gkwin ----------------
# For the separators (jsepf / jsep3 / Karp tail all read WIN) the payee credit of a d >= 7 centre is a WINDOW BOUND: per IN slot, the
# window centred at the payer w_j (w_{j-2..j+2}, s_{j-2..j+1}) is fixed and every letter outside it is OR-ed out position by position;
# f2b extras are dropped.  Both only enlarge each position's set, so the bound >= the exact (KEYSPEC) IN count.  With gkwin the Python
# receiver row uses the same bound (so rows, WIN and every separator agree exactly, as Team D's EDGE does); without it the row is exact.
# The OUT (payer) side of a d = 7 centre is exact and is applied at the jsepf leaf (argv[14], Team D's 7802 format; payer-7 keys only).
GKWIN = 'gkwin' in FLAGS
GKMD5 = hashlib.md5(open(GKFILE, 'rb').read()).hexdigest()[:8] if GKON else ''
_GKPOS = {}
def _gk_posmasks(U):
    """{(payer letter, sg): (10, 5^9) uint8 position masks} for the IN slot of the window centred at the payer (window bound)"""
    if U in _GKPOS: return _GKPOS[U]
    kt_load(); l3q_load()
    g = np.indices((5,) * 9, dtype=np.int8).reshape(9, -1)
    B = lambda x: (np.uint8(1) << x.astype(np.uint8)).astype(np.uint8)
    lw = lambda r: g[r + 2]; la = lambda t: g[5 + t + 2]
    AM = (31 & ~np.asarray(KT[U]).astype(np.int64)).astype(np.uint8)          # amask(U, w-2, w-1, w+1, w+2, s-2, s-1, s0, s+1) - 5
    P6 = AM[g[0], g[1], g[3], g[4], g[5], g[6], g[7], g[8]]                   # the payer 6's private
    AMm = np.bitwise_or.reduce(np.bitwise_or.reduce(AM, axis=4), axis=0)        # six at j-1: (w_{j-2}, w_j, w_{j+1}, s_{j-2}, s_{j-1}, s_j)
    AMp = np.bitwise_or.reduce(np.bitwise_or.reduce(AM, axis=7), axis=3)        # six at j+1: (w_{j-1}, w_j, w_{j+2}, s_{j-1}, s_j, s_{j+1})
    six_m = AMm[g[0], g[2], g[3], g[5], g[6], g[7]]; six_p = AMp[g[1], g[2], g[4], g[6], g[7], g[8]]
    full = np.full(g.shape[1], 31, dtype=np.uint8)
    if U == 7:
        # L3T[(sg, c, w2, w3, w4, ap, o)] for c, ap <= 6; OR over the letters outside the window
        L3 = {sg: np.zeros((2, 5, 5, 5, 2, 5), dtype=np.uint8) for sg in (1, -1)}
        for (sg, c, w2, w3, w4, ap_, o_), m in L3T.items():
            assert c <= 6 and ap_ <= 6
            L3[sg][c - 5, w2 - 5, w3 - 5, w4 - 5, ap_ - 5, o_ - 5] |= np.uint8(m)
        L34 = {sg: np.bitwise_or.reduce(L3[sg], axis=3) for sg in (1, -1)}             # OR over w4: [c, w2, w3, ap, o]
        L334 = {sg: np.bitwise_or.reduce(L34[sg], axis=2) for sg in (1, -1)}           # OR over w3, w4: [c, w2, ap, o]
        def l3(sg, c, w2, ap_, o_, w3=None):   # c, ap as letter indices; wildcard unless both <= 6
            ok = (c <= 1) & (ap_ <= 1); c1 = np.minimum(c, 1); a1 = np.minimum(ap_, 1)
            v = L334[sg][c1, w2, a1, o_] if w3 is None else L34[sg][c1, w2, w3, a1, o_]
            return np.where(ok, v, 31).astype(np.uint8)
        P7m = l3(-1, lw(-1), lw(-2), la(-1), la(0))                                 # payer 7: private next to s_{j-1}
        P7p = l3(1, lw(1), lw(2), la(0), la(-1))                                    # payer 7: private next to s_j
        sev_m = l3(1, lw(0), lw(1), la(-1), la(-2), w3=lw(2))                       # 7 at j-1: its private next to s_{j-1}
        sev_p = l3(-1, lw(0), lw(-1), la(0), la(1), w3=lw(-2))                      # 7 at j+1: its private next to s_j
    else: P7m = P7p = sev_m = sev_p = full
    def nb(r, five, six, sev):   # the neighbour W[j+r] (r = -1 / +1)'s vertex beyond its apex next to w_j
        x = lw(r)
        return np.where(x == 0, five, np.where(x == 1, six, np.where(x == 2, sev, 31))).astype(np.uint8)
    SAm = nb(-1, B(la(-2)), six_m, sev_m)                                         # pin(j-1, 1)
    SAp = nb(1, B(la(1)), six_p, sev_p)                                           # pin(j+1, 0)
    out = {}
    for u, (p0, p1) in ((5, (B(la(0)), B(la(-1)))), (6, (P6, P6)), (7, (P7m, P7p))):   # pin(j, 0), pin(j, 1)
        out[(u, 1)] = np.stack([B(lw(-1)), B(la(-1)), p0, B(lw(1)), B(la(0)), p1, SAm, SAp, B(lw(-2)), B(lw(2))])
        out[(u, -1)] = np.stack([B(lw(1)), B(la(0)), p1, B(lw(-1)), B(la(-1)), p0, SAp, SAm, B(lw(2)), B(lw(-2))])
        out[(u, 'payer')] = (g[2] == u - 5)
    _GKPOS[U] = out; return out
_GKTAB = {}
def gk_tables(k, U):
    """(T+, T-) uint8 over the 5^9 window index centred at the payer: window bound of key k's IN slot at a centre of degree U; None
    if the key cannot pay a degree-U centre"""
    ck = (k, U)
    if ck in _GKTAB: return _GKTAB[ck]
    key = GKEYS[k]
    if not (key['vm'] & _gkbit(U)) or not (key['um'] & 7): _GKTAB[ck] = None; return None
    res = []
    for sg in (1, -1):
        tot = np.zeros(5 ** 9, dtype=np.uint8)
        for u in (5, 6, 7):
            if not (key['um'] & _gkbit(u)): continue
            PM = _gk_posmasks(U); ok = PM[(u, 'payer')].copy(); V = PM[(u, sg)]
            for p in range(10):
                if key['m'][p] != 31: ok &= (V[p] & key['m'][p]) != 0
            tot += ok.astype(np.uint8)
        res.append(tot)
    _GKTAB[ck] = tuple(res); return _GKTAB[ck]
def _gk_widx(w, s, j):
    n = len(w); ix = 0
    for v in [w[(j + o) % n] for o in (-2, -1, 0, 1, 2)] + [s[(j + o) % n] for o in (-2, -1, 0, 1)]: ix = ix * 5 + (min(v, 9) - 5)
    return ix
def gk_recv_terms_win(d, w, s):
    """receiver key terms with the window-bound IN side and the exact OUT side"""
    U = min(d, 9); A, PV = gk_recv_picture(d, w, s); pay, _ = gk_counts(d, w, A, PV); cf = collections.Counter()
    ix = [_gk_widx(w, s, j) for j in range(d)]
    for k, nm_ in enumerate(GKNAMES):
        T = gk_tables(k, U); get = 0
        if T is not None: get = sum(int(T[0][i_]) + int(T[1][i_]) for i_ in ix)
        v = get - int(pay[k])
        if v: cf[('ks', nm_)] = v
    return cf
GKLEAF = 'gkleaf' in FLAGS   # with gkwin: d = 7 rows exact (jsepf_gk corrects the window bound at the leaf, argv[15]); d >= 8 rows window bound
assert GKWIN or not GKLEAF, 'gkleaf needs gkwin'
if GKWIN:
    _gk_recv_terms_exact = gk_recv_terms
    def gk_recv_terms(d, w, s):
        if not GKON: return collections.Counter()
        l3q_load(); kt_load()
        if GKLEAF and d == 7: return _gk_recv_terms_exact(d, w, s)
        return gk_recv_terms_win(d, w, s)
if GKLEAF: BINF = os.path.join(HERE, 'bin', 'jsepf_gk')
GK_NPAY7 = sum(1 for k in GKEYS if k['um'] & 4); GK_PAY7MAX = 64   # s86 p1r copy: jsepf_gk refuses > 64 payer-7 keys (7802 header check)
if GKLEAF and GK_NPAY7 > 64:   # s86 p1r copy: same source with the limit raised to 192 (ids 1800000100 + k stay below the gkin ids 1800000300 + k)
    BINF = os.path.join(HERE, 'bin', 'jsepf_gk_k192'); GK_PAY7MAX = 192; log('gkeys: %d payer-7 keys > 64: leaf binary %s (7802 limit 192)' % (GK_NPAY7, BINF))
_GK_INPOS = {p_: i for i, p_ in enumerate(GK_POS)}
def gkin_write():
    """argv[15] for jsepf_gk at d = 7 (magic 7804): the keys whose payee set contains 7 (IN slots of the d = 7 centre, exact at the leaf),
    then UBW[5^9] = sum over those keys of amount x (T+ + T-) at U = 7 (the window bound window_table_R2 added to WIN)"""
    fn = os.path.join(WORK, 'gkin_d7.bin'); ks = [k for k in range(len(GKEYS)) if gk_tables(k, 7) is not None]
    b_ = [np.array([7804, len(ks)], dtype='<i4').tobytes()]; UBW = np.zeros(5 ** 9)
    for k in ks:
        key = GKEYS[k]; v = float(KSV.get(key['name'], 0.0)); assert v >= -1e-12, 'gkeys: negative amount %s %r' % (key['name'], v); v = max(v, 0.0)
        assert 0 < (int(key['um']) & 7) and not (int(key['um']) & 24)
        cl_ = [(i, int(key['m'][i])) for i in range(10) if key['m'][i] != 31]
        b_.append(np.array([v], dtype='<f8').tobytes()); b_.append(np.array([int(key['um']) & 7, len(cl_)] + [z for c_ in cl_ for z in c_], dtype='<i4').tobytes())
        if v != 0.0: T = gk_tables(k, 7); UBW += v * (T[0].astype(np.float64) + T[1].astype(np.float64))
    b_.append(UBW.astype('<f8').tobytes()); open(fn, 'wb').write(b''.join(b_)); return fn
GKWPLANT = 'gkwplant' in FLAGS
_orig_window_table_R2_gk = window_table_R2
def window_table_R2(U, y, x, MV2):
    W = _orig_window_table_R2_gk(U, y, x, MV2)
    if GKON:
        assert GKWIN, 'gkeys: separators need gkwin (window-bound receiver rows)'
        for k, nm_ in enumerate(GKNAMES):
            v = KSV.get(nm_, 0.0); T = gk_tables(k, U)
            if v != 0.0 and T is not None: W += v * (T[0].astype(np.float64) + (0 if GKWPLANT else T[1].astype(np.float64))).reshape((5,) * 9)   # GKWPLANT: CONTROL ONLY (F2B-SELFTEST must FAIL)
    return W
_orig_class_table_R2_gk = class_table_R2
def class_table_R2(xon):
    """mode-2 classes: fold every key's payee bound signature (all U, both chiralities) into the class of every window"""
    C = _orig_class_table_R2_gk(xon)
    if not GKON: return C
    tabs = [(k, U) for k in range(len(GKEYS)) for U in (7, 8, 9) if gk_tables(k, U) is not None]
    nb_ = 2 * len(tabs); P = np.zeros((5 ** 9, max(1, (2 * nb_ + 7) // 8)), dtype=np.uint8); b_ = 0
    for k, U in tabs:
        for T in gk_tables(k, U):
            for bit in (1, 2):   # the table value is 0..2 (two payer letters can share a chirality only if um has several letters)
                P[:, b_ // 8] |= (((T & bit) != 0).astype(np.uint8) << np.uint8(b_ % 8)); b_ += 1
    u_, inv = np.unique(P, axis=0, return_inverse=True); inv = inv.reshape(-1)
    C = C.reshape(-1).astype(np.int64); stride = int(C.max()) + 1; nz = C != 0
    pair = C * np.int64(len(u_)) + inv.astype(np.int64); _, rn = np.unique(pair[nz], return_inverse=True)   # renumber (class, signature) pairs densely; 0 stays 0
    C2 = np.zeros_like(C); C2[nz] = rn.reshape(-1).astype(np.int64) + 1; C = C2; assert int(C.max()) < 2 ** 31 - 1, 'gkeys: class fold overflow'
    log('gkeys: mode-2 class fold: %d distinct payee-bound signatures over %d tables' % (len(u_), len(tabs)))
    return C.astype(np.int32).reshape((5,) * 9)
_GK_KIND = {'S.L+1': (0, 1), 'S.L+2': (0, 2), 'S.L+3': (0, 3), 'S.L-1': (0, -1), 'S.L-2': (0, -2), 'S.L-3': (0, -3),
            'S.A+1': (1, 1), 'S.A-1': (1, -2), 'R.L+2': (1, 0), 'R.L-2': (1, -1)}   # OUT slot of a d = 7 centre (payer frame), as edgefam
def gk_write():
    """argv[14] for jsepf at d = 7 (Team D's 7802 format): the keys whose payer set contains 7 (the centre's OUT slots, exact);
    a key with a payer set beyond {7} is written with its full payee mask: the leaf only ever sees the d = 7 centre as payer"""
    fn = os.path.join(WORK, 'gkedge_d7.bin'); ks = [k for k, key in enumerate(GKEYS) if key['um'] & 4]
    assert len(ks) <= GK_PAY7MAX, 'gkeys: more than %d payer-7 keys (jsepf limit)' % GK_PAY7MAX
    b_ = [np.array([7802, len(ks)], dtype='<i4').tobytes()]
    for k in ks:
        key = GKEYS[k]; v = float(KSV.get(key['name'], 0.0)); assert v >= -1e-12, 'gkeys: negative amount %s %r' % (key['name'], v)
        b_.append(np.array([max(v, 0.0)], dtype='<f8').tobytes())
        cl_ = [(p_, int(key['m'][i])) for i, p_ in enumerate(GK_POS) if key['m'][i] != 31]
        b_.append(np.array([int(key['vm']), len(cl_)] + [z for p_, m_ in cl_ for z in _GK_KIND[p_] + (m_,)], dtype='<i4').tobytes())
    open(fn, 'wb').write(b''.join(b_)); return fn
if GKWIN and GKON:
    assert all(not (k['um'] & 24) for k in GKEYS), 'gkwin: a payer set beyond {5, 6, 7} (the OUT side of a d >= 8 centre has no jsepf leaf)'
def cmd_gkwintest():
    """gkwin: the window-bound IN count >= the exact (KEYSPEC) IN count, key by key, on random receivers d = 7, 8, 9 (and with planted
    payer letters); the OUT side identical; reports how often the bound is strict"""
    import random; l3q_load(); kt_load(); rng = random.Random(int(OPT.get('seed', '1'))); N = int(OPT.get('N', '4000')); bad = 0
    for d in (7, 8, 9):
        U = min(d, 9); strict = 0; nzx = 0; nzw = 0
        for it in range(N):
            w = [rng.choice((5, 6, 7, 8, 9)) for _ in range(d)]; s = [rng.choice((5, 6, 7, 8, 9)) for _ in range(d)]
            if it % 2: w = [rng.choice((5, 6, 7)) for _ in range(d)]; s = [rng.choice((5, 6, 7)) for _ in range(d)]
            lk = ''.join(map(str, w)); sv = ''.join(map(str, s))
            if admissible(d, lk, sv) is not None: continue
            A, PV = gk_recv_picture(d, w, s); pay, get = gk_counts(d, w, A, PV)
            ix = [_gk_widx(w, s, j) for j in range(d)]
            for k in range(len(GKEYS)):
                T = gk_tables(k, U); gw = 0 if T is None else sum(int(T[0][i_]) + int(T[1][i_]) for i_ in ix)
                if gw < int(get[k]):
                    bad += 1
                    if bad <= 5: log('  gkwintest d=%d %s %s key %s: window %d < exact %d' % (d, lk, sv, GKNAMES[k], gw, get[k]))
                strict += gw > int(get[k]); nzx += int(get[k]) > 0; nzw += gw > 0
            cw = gk_recv_terms_win(d, w, s)
            for k, nm_ in enumerate(GKNAMES):
                T = gk_tables(k, U); gw = 0 if T is None else sum(int(T[0][i_]) + int(T[1][i_]) for i_ in ix)
                if cw.get(('ks', nm_), 0) != gw - int(pay[k]): bad += 1
        log('  gkwintest d=%d: %d random receivers x %d keys: exact IN > 0 in %d, window IN > 0 in %d, window strictly above exact in %d' % (d, N, len(GKEYS), nzx, nzw, strict))
    log('GKWINTEST: %s (%d failures)' % ('PASS' if bad == 0 else 'FAIL', bad))
# ---------------- s85: exact check of a t = 0 point (W6's JSON) on the 5/6/7 world, our engine's rows ----------------
def cmd_world0():
    """exact (Fractions) check, at the point's t, of a W6-format point ({'t', 'rules', 'variables': [{var, key, value}]}) on our rows:
    every receiver of rows= (our admissibility; load <= d - 6 + t), every sender row of R2_sender_rows (>= 1 - t), every cons2 class row
    (all6_words x {5,7}^6 apex words; c6le: in - out <= t, else = 0), every bound (>= 0, caps 3).  M, Q are our engine's derived
    values (max h over sig2_keys, max q over q7keys); lQ = max(LP lQ, max lq over the mask) as upperR2; W6's M, Q7 variables are only
    reported (mrow closure: ours is the smallest admissible choice)"""
    from fractions import Fraction as Fr
    load_patterns(); xon = 'xon' in FLAGS; l3q_load(); kt_load(); assert AC, 'world0: needs apexcls ({5,7}^6 apex words are the classes)'
    raw = open(OPT['w6sol'], 'rb').read(); P = json.loads(raw); t = Fr(P['t'])
    log('world0: %s md5 %s, t = %s, %d variables; c6le %s' % (OPT['w6sol'], hashlib.md5(raw).hexdigest(), t, len(P['variables']), C6LE))
    mine = {k['name']: (int(k['um']), int(k['vm']), tuple(int(z) for z in k['m'])) for k in GKEYS}; diff = []
    for nm_, r_ in P.get('rules', []):
        k_ = gk_parse('%s %s' % (nm_, r_)); th = (int(k_['um']), int(k_['vm']), tuple(int(z) for z in k_['m']))
        if mine.get(nm_) != th: diff.append(nm_)
    log('world0: rules in the point %d, gkeys loaded %d, differing or missing %d %s' % (len(P.get('rules', [])), len(GKEYS), len(diff), diff[:5]))
    V = collections.defaultdict(dict); unk = collections.Counter()
    for v in P['variables']:
        q = Fr(v['value']); var = v['var']; key = v['key']
        if var == 'y':
            r_ = root(list(key), 0)
            if r_ not in RIX: unk['y'] += 1; continue
            V['y'][r_] = q
        elif var == 'x': V['x'][int(key)] = q
        elif var == 'E': V['ks'][str(key)] = q
        else: V[var][tuple(key)] = q
    log('world0: variables by kind %s; y keys not among our roots %d' % (dict((k, len(d_)) for k, d_ in V.items()), unk['y']))
    caps = {'x': 3, 'lq': 3, 'z': 3, 'zr': 3, 'rr': 3, 'q': 3, 'ks': 3}; nb = 0
    for var, d_ in V.items():
        for k, q in d_.items():
            if q < 0 or (var in caps and q > caps[var]): nb += 1; log('  bound violated %s %s = %s' % (var, k, q)) if nb <= 5 else None
    log('world0: bound violations %d' % nb)
    LQV.clear(); LQV.update(V['lq']); LQQ.clear(); LQQ.update(V['lQ'])
    YV, XV, HV, GV_, KV = V['y'], V['x'], V['h'], V['g'], V['ks']
    QVx = V['q']; RVx, RRx, ZVx, ZRx = V['r'], V['rr'], V['z'], V['zr']; mc = {}
    def Mv(sg):
        if sg not in mc:
            ks = sig2_keys(sg); mc[sg] = max([HV.get(k, Fr(0)) for k in ks] or [Fr(0)])
        return mc[sg]
    bad_keys = collections.Counter()
    def val(k):
        a = k[0]
        if a == 'y': return YV.get(k[1], Fr(0))
        if a == 'x': return XV.get(k[1], Fr(0))
        if a == 'M': return Mv(k[1])
        if a == 'r': return RVx.get(k[1], Fr(0))
        if a == 'rr': return RRx.get(k[1], Fr(0))
        if a == 'z': return ZVx.get(k[1], Fr(0))
        if a == 'zr': return ZRx.get(k[1], Fr(0))
        if a == 'lq': return LQV.get(k[1], Fr(0))
        if a == 'q': return QVx.get(k[1], Fr(0))
        if a == 'Q': return max([QVx.get(kk, Fr(0)) for kk in q7keys(k[1])] or [Fr(0)])
        if a == 'lQ': return Fr(l3q_Qeff(*k[1]) if len(k[1]) == 3 else l3q_QeffV(*k[1]))
        if a == 'ks': return KV.get(k[1], Fr(0))
        if a == 'g': return GV_.get(k[1], Fr(0))
        if a == 'h': return HV.get(k[1], Fr(0))
        bad_keys[a] += 1; return Fr(0)
    def row(cf): return sum((Fr(c) * val(k) for k, c in cf.items() if c), Fr(0))
    res = {}
    # receivers
    nr = nadm = 0; bad = 0; mn = None; seen = set()
    for l in open(OPT['rows']):
        f = l.split()
        if len(f) != 4 or f[0] != 'R': continue
        d = int(f[1]); lk, sv = f[2], f[3]; nr += 1
        if admissible(d, lk, sv) is not None: nadm += 1; continue
        sl = Fr(d - 6) + t - row(recv_coef_R2(d, lk, sv, xon))
        if mn is None or sl < mn[0]: mn = (sl, lk, sv)
        if sl < 0:
            bad += 1
            if bad <= 5: log('  receiver violated d=%d %s/%s slack %s (%.3g)' % (d, lk, sv, sl, float(sl)))
        if nr % 20000 == 0: log('  receivers checked %d' % nr)
    log('world0: receivers %d listed, %d not admissible in our engine (skipped), %d checked: violated %d; min slack %s (%.3g) at %s/%s' % (nr, nadm, nr - nadm, bad, mn[0], float(mn[0]), mn[1], mn[2]))
    res['receiver'] = bad
    # senders
    ns = bad = 0; mn = None
    for wd, cf, bits in R2_sender_rows():
        ns += 1; sl = row(cf) - (1 - t)
        if mn is None or sl < mn[0]: mn = (sl, wd, bits)
        if sl < 0:
            bad += 1
            if bad <= 5: log('  sender violated %s %s slack %s' % (wd, bits, sl))
    log('world0: sender rows %d: violated %d; min slack %s (%.3g) at %s %s' % (ns, bad, mn[0], float(mn[0]), mn[1], mn[2]))
    res['sender'] = bad
    # cons2
    nc = bad = 0; mn = None; A6 = all6_words(); hi = None
    for L in A6:
        for s_ in itertools.product((5, 7), repeat=6):
            v = row(cons2_coef(tuple(L), s_)); nc += 1
            sl = (t - v) if C6LE else -abs(v)
            if mn is None or sl < mn[0]: mn = (sl, L, s_)
            if hi is None or v < hi[0]: hi = (v, L, s_)
            if sl < 0:
                bad += 1
                if bad <= 5: log('  cons2 violated L=%s s=%s in-out %s' % (L, s_, v))
    log('world0: cons2 rows %d (%d links x 64 class words): violated %d; min slack %s (%.3g) at %s %s; lowest in - out %s (%.3g)' % (nc, len(A6), bad, mn[0], float(mn[0]), mn[1], mn[2], hi[0], float(hi[0])))
    res['cons2'] = bad
    # W6's own mrow variables vs our derived values (information only)
    gM = sum(1 for k, q in V['M'].items() if q < Mv(k)); gQ = sum(1 for k, q in V['Q7'].items() if q < max([QVx.get(kk, Fr(0)) for kk in q7keys(k)] or [Fr(0)]))
    log('world0: W6 M variables %d (below our max h: %d), Q7 variables %d (below our max q: %d); unsupported coefficient kinds %s' % (len(V['M']), gM, len(V['Q7']), gQ, dict(bad_keys)))
    ok = nb == 0 and not diff and not any(res.values()) and not bad_keys and unk['y'] == 0
    log('WORLD0: %s at t = %s (receivers %d, senders %d, cons2 %d violated; bounds %d)' % ('HOLDS EXACTLY' if ok else 'FAILS', t, res['receiver'], res['sender'], res['cons2'], nb))
def cmd_gkdbg():
    """debug: one d = 7 arrangement (lk=, sv=) at sol=: python exact and window-bound key credit per payer position, and jsepf_gk's
    leaf (GKDBG lines) on the same arrangement"""
    load_patterns(); xon = 'xon' in FLAGS; l3q_load(); kt_load()
    Sj = json.load(open(OPT['sol'])); KSV.clear(); KSV.update({str(k): float(v) for k, v in Sj.get('ks', [])})
    lk = OPT['lk']; sv = OPT['sv']; d = len(lk); w = [int(c) for c in lk]; s = [int(c) for c in sv]
    A, PV = gk_recv_picture(d, w, s); log('gkdbg %s/%s: A %s PV %s' % (lk, sv, A, PV))
    (ou, ov, oV), (iu, iv, iV) = gk_slots(d, w, A, PV)
    for k, key in enumerate(GKEYS):
        amt = KSV.get(key['name'], 0.0); T = gk_tables(k, 7)
        if not amt or T is None: continue
        for slot in range(2 * d):
            j = slot // 2; sg = 1 if slot % 2 == 0 else -1
            poss = bool(((iV[slot] & key['m']) != 0).all() and (iu[slot] & key['um']) and (iv[slot] & key['vm']))
            ub = int(T[0 if sg == 1 else 1][_gk_widx(w, s, j)])
            if poss or ub: log('  key %s amt %.6f j=%d sg=%+d exact %d bound %d  V %s m %s' % (key['name'], amt, j, sg, poss, ub, list(iV[slot]), list(key['m'])))
    os.environ['GKDBG'] = '1'
    ef = os.path.join(WORK, 'gkdbg_eval.txt'); open(ef, 'w').write('%s %s\n' % (lk, sv))
    y = np.zeros(len(ROOTS)); MV2 = lambda sg: None
    write_l3q(); F2B_EVAL[0] = ef; W = window_table_R2(7, y, {}, MV2); rr, dt, ni = run_sep(7, W, 1e9, 1, 0); F2B_EVAL[0] = None
    log('gkdbg: jsepf eval %s' % rr)
def cmd_dualexport():
    """s85: every dual-support row of cert= with its labels and its generic-key coefficients (W6 pricing input) -> out= (JSON).
    Receivers: credit 'exact' (d = 7 under gkleaf: KEYSPEC picture) or 'window' (gkwin window bound, d >= 8); window rows also carry
    ks_exact_picture (the KEYSPEC-picture coefficients) for comparison.  Senders: apex classes H (S = {5,6}, B = {7,8,9}) and the
    class of each link 6's private.  cons2: apex classes (apexcls).  colsum[key] = sum over rows of w x coefficient (cert signs)."""
    from fractions import Fraction as Fr
    load_patterns(); l3q_load(); kt_load()
    raw = open(OPT['cert'], 'rb').read(); C = json.loads(raw)
    SR = {(wd, tuple(map(str, b))): cf for wd, cf, b in R2_sender_rows()}
    rows = []; colsum = collections.Counter(); kinds = collections.Counter(); wk = collections.Counter(); nwin_diff = 0
    for c in C:
        r = c['row']; w = float(Fr(c['w'])) if isinstance(c['w'], str) else float(c['w'])
        e = {'w': w}
        if isinstance(c['w'], str): e['w_exact'] = c['w']
        k = r[0]; ks = {}
        if k == 'receiverR2':
            d = int(r[1]); lk = [int(ch) for ch in r[2]]; sv = [int(ch) for ch in r[3]]
            mode = 'exact' if (not GKWIN or (GKLEAF and d == 7)) else 'window'
            if P1R and d in (7, 8): mode = 'p1r'   # s86 p1r copy: KEYSPEC v2 single-row coefficient (max over realisations of IN - OUT)
            e.update(type='receiver', d=d, link=r[2], apex=r[3], credit=mode,
                     link_has_8plus=any(x >= 8 for x in lk), apex_has_8plus=any(x >= 8 for x in sv))
            ks = {nm[1]: v for nm, v in gk_recv_terms(d, lk, sv).items()}
            if mode == 'window':
                ex = {nm[1]: int(v) for nm, v in _gk_recv_terms_exact(d, lk, sv).items()}
                e['ks_exact_picture'] = ex
                if ex != {n: int(v) for n, v in ks.items()}: nwin_diff += 1
            if mode == 'p1r':
                e['ks_current'] = {nm[1]: int(v) for nm, v in _p1r_gk_recv_terms_cur(d, lk, sv).items()}   # s86 p1r copy: the coefficients without p1r
                if e['ks_current'] != {n: int(v) for n, v in ks.items()}: nwin_diff += 1
        elif k == 'receiverV2':   # s86 v2r: KEYSPEC v2 realisation row; ks = IN(K; rho) - OUT(K) exactly (the same reading prices any new key exactly on this row)
            d = int(r[1]); lk = [int(ch) for ch in r[2]]; sv = [int(ch) for ch in r[3]]
            e.update(type='receiverV2', d=d, link=r[2], apex=r[3], rho=r[4], credit='v2', privates={str(j): r[4][2 * j:2 * j + 2] for j in range(d) if lk[j] != 5},
                     link_has_8plus=any(x >= 8 for x in lk), apex_has_8plus=any(x >= 8 for x in sv))
            ks = {nm[1]: v for nm, v in v2r_row(d, r[2], r[3], r[4]).items() if nm[0] == 'ks'}
        elif k == 'senderR2':
            cf = SR[(r[1], tuple(map(str, r[2])))]
            b = list(r[2]); i = b.index('|'); H = b[:i]; Fb = b[i + 1:]; assert len(H) == 5, 'dualexport: needs hat5'
            w5 = [int(ch) for ch in r[1]]; sixes = [j for j in range(5) if w5[j] == 6]
            e.update(type='sender', link=r[1], apex_classes=''.join('B' if int(x) else 'S' for x in H),
                     six_private_classes={str(j): ('B' if int(x) else 'S') for j, x in zip(sixes, Fb)}, label_bits=[str(x) for x in r[2]])
            ks = {nm[1]: v for nm, v in cf.items() if nm[0] == 'ks'}
        elif k == 'cons2':
            L = tuple(int(x) for x in r[1]); s = tuple(int(x) for x in r[2])
            e.update(type='cons2', link=''.join(map(str, L)), apex=''.join(map(str, s)))
            if AC: e['apex_classes'] = ''.join('B' if ap(x) >= 7 else 'S' for x in s)
            ks = {nm[1]: v for nm, v in gk_cons2_terms(L, s).items()}
        else:
            e.update(type=k, sig=r[1], key=r[2])
        e['ks'] = {n: int(v) for n, v in ks.items() if v}
        for n, v in e['ks'].items(): colsum[n] += w * v
        kinds[e['type']] += 1; wk[e['type']] += abs(w); rows.append(e)
    rows.sort(key=lambda e: -abs(e['w']))
    meta = {'cert': OPT['cert'], 'cert_md5': hashlib.md5(raw).hexdigest(), 'gkeys': GKFILE, 'gkeys_md5': GKMD5, 'flags': sorted(FLAGS),
            'sign_convention': 'receiver w <= 0 (load <= d - 6 + t), sender w >= 0 (sum >= 1 - t), cons2 w <= 0 (c6le: in - out <= t), mrow* w <= 0 (h - M <= 0 etc.)',
            'coef_convention': 'ks coefficient: receiver / cons2 IN - OUT, sender OUT - IN (IN counts possible matches, OUT sure matches)',
            'rows_by_type': dict(kinds), 'abs_w_by_type': {k_: round(v, 9) for k_, v in wk.items()},
            'window_rows_where_window_differs_from_picture': nwin_diff, 'keys': GKNAMES}
    if V2R: meta['v2r'] = 'receiverV2 rows (d = 7 / 8): KEYSPEC v2 realisation rows, rho = x_0 y_0 ... x_{d-1} y_{d-1} (x_j = w_j private next to s_j, y_j = next to s_{j-1}); ks = IN(K; rho) - OUT(K) exact (v2r/V2ROW_SPEC.md)'
    if P1R: meta['p1r'] = 'receiver d = 7 / 8 rows: credit p1r = max over realisations of IN - OUT (KEYSPEC2_RECEIVER 3.3), ks_current = the coefficients without p1r; window_rows_where_window_differs_from_picture also counts p1r rows that differ from ks_current'
    json.dump({'meta': meta, 'colsum': {n: colsum.get(n, 0.0) for n in GKNAMES}, 'rows': rows}, open(OPT['out'], 'w'), separators=(',', ':'))
    log('DUALEXPORT: %d rows %s -> %s; window rows differing from the KEYSPEC picture %d' % (len(rows), dict(kinds), OPT['out'], nwin_diff))
