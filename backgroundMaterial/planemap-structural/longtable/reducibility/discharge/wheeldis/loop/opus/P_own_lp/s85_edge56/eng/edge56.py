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
