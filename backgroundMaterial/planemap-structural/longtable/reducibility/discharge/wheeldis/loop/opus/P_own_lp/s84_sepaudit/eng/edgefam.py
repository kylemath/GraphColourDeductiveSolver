# edgefam.py (s78_kstar, Team D): generic EDGE(7->P)[slot conditions] transfer family; each key is data (file edgekeys=, one
# "NAME EDGE(7->P)[POS=SYM ...]" per line, grammar.py / gext.py position names and symbols).  exec'd by pcheck.py after kstar.py.
#   Amount column ('ks', NAME) in [0, kscap] (the K* column namespace; NAME != 'K1').  Payer: degree exactly 7.  Payee P in {7, B}
#   (or any subset of {7, 8, 9+}): the payee is the row centre, so P selects the row degrees (9 = every d >= 9).
#   Positions allowed: S.L+-1..3, S.A+-1, R.L+-2 - exactly those that are EXACT letters of the payer's own 2-ball (link + apexes), so the
#   payer side is exact in the payer's row (no second-ring row family needed).  Other positions are refused.
#   Payer row (d = 7 centre u, v = w_i, orientation e = the + direction): S.L+-k = w_{i+-k e}; S.A+1 = apex(i+e, i+2e); S.A-1 = apex(i-e,
#     i-2e); R.L+2 = apex(i, i+e); R.L-2 = apex(i-e, i); w_i in P.  Coefficient -1 per (i, e) match.  Applied at the jsepf leaf (argv[14],
#     exact, <= 0) and in recv_coef_R2.
#   Payee row (centre v of degree d with d in P, payer u = w_j = 7, orientation e): S.L+-1 = w_{j+-e}; S.L+-2 = apex(j, j+-e);
#     R.L+-2 = w_{j+-2e}; S.L+-3 = u's private next to apex(j, j+-e): L3T & m at U = 7 when (w_{j+-e}, apex) in {5,6}^2, else free;
#     S.A+-1 = the vertex across (w_k, apex(j,k)), k = j+-e: w_k = 5 -> apex(k, k+-e) (exact); w_k = 6 -> its private, amask_U(k) & m;
#     w_k >= 7 -> free.  Credit +1 per (j, e) if every condition is POSSIBLE (grammar semantics), evaluated as a WINDOW BOUND: the window
#     centred at j, every letter outside it OR-ed out per condition and the f2b extras dropped (both only enlarge the credit).  The Python
#     row coefficient IS this bound (table lookup), so WIN, the separators (all d, Karp tail through W9) and the LP rows agree exactly; the
#     payee side needs no leaf term and nothing can be positive outside WIN.
EGFILE = OPT.get('edgekeys'); EG = EGFILE is not None
EGKEYS = []                              # dicts: name, spec, vm (payee letters), conds [(pos, mask)]
EG_SYM = {'5': 1, '6': 2, '7': 4, '8': 8, '9': 16, 'S': 3, 'B': 28, '*': 31}
EG_POS = ('S.L+1', 'S.L+2', 'S.L+3', 'S.L-1', 'S.L-2', 'S.L-3', 'S.A+1', 'S.A-1', 'R.L+2', 'R.L-2')
def eg_parse(line):
    import re as _re
    m_ = _re.match(r'^\s*(\S+)\s+EDGE\(([^-]+)->([^)]+)\)(?:\[(.*)\])?\s*$', line)
    assert m_, 'edgekeys: bad line %r' % line
    nm, pu, pv, body = m_.groups(); assert nm != 'K1' and _re.match(r'^[A-Za-z0-9_]+$', nm), 'edgekeys: bad name %r' % nm
    assert pu == '7', 'edgekeys: payer must be 7 (%r)' % line
    vm = EG_SYM[pv]; assert vm and not (vm & 3), 'edgekeys: payee must be a subset of B (%r)' % line
    conds = []
    for tok in (body or '').split():
        p_, s_ = tok.split('='); assert p_ in EG_POS, 'edgekeys: position %s not supported (payer side not exact)' % p_
        assert p_ not in [c[0] for c in conds]; conds.append((p_, EG_SYM[s_]))
    return {'name': nm, 'spec': 'EDGE(%s->%s)[%s]' % (pu, pv, body or ''), 'vm': vm, 'conds': conds}
if EG:
    assert F2B_ON and L3Q and F16 and AC and AP and not W19 and not PCAM and not XO and not FY and not V6, 'edgekeys: needs the s75 stack'
    for l_ in open(EGFILE):
        if l_.strip() and not l_.startswith('#'): EGKEYS.append(eg_parse(l_))
    assert len({k['name'] for k in EGKEYS}) == len(EGKEYS), 'edgekeys: duplicate names'
    log('edgekeys: %d keys from %s: %s' % (len(EGKEYS), EGFILE, '; '.join('%s = %s' % (k['name'], k['spec']) for k in EGKEYS)))
EGNAMES = [k['name'] for k in EGKEYS]
def _eg_bit(l): return 1 << (l - 5)
def eg_payer_letter(w, s, i, e, pos):
    n = len(w); ap = lambda p: s[(i + p) % n] if e > 0 else s[(i - p - 1) % n]   # apex between orientation offsets p, p+1
    if pos[2] == 'L' and pos[0] == 'S': return w[(i + int(pos[3:]) * e) % n]
    return {'S.A+1': ap(1), 'S.A-1': ap(-2), 'R.L+2': ap(0), 'R.L-2': ap(-1)}[pos]
def eg_payer_count(key, w, s):
    """number of (i, e) at which the d = 7 centre (link w, apexes s) pays key"""
    return sum(1 for i in range(len(w)) if _eg_bit(w[i]) & key['vm'] for e in (1, -1)
               if all(_eg_bit(eg_payer_letter(w, s, i, e, p_)) & m_ for p_, m_ in key['conds']))
_EGTAB = {}
def eg_tables(key, U):
    """(T+, T-): uint8 over the 5^9 window index (w_{j-2..j+2}, s_{j-2..j+1}) centred at the payer j: payee credit bound, orientation +-1"""
    ck = (key['name'], U)
    if ck in _EGTAB: return _EGTAB[ck]
    if not (key['vm'] & _eg_bit(min(U, 9))): _EGTAB[ck] = None; return None
    kt_load(); l3q_load()
    g = np.indices((5,) * 9, dtype=np.int8)
    AM = 31 & ~np.asarray(KT[U]).astype(np.int64)
    def lw(r): return g[r + 2] if -2 <= r <= 2 else None                 # w_{j+r}
    def la(t): return g[5 + t + 2] if -2 <= t <= 1 else None             # apex(j+t, j+t+1)
    def inm(x, m): return True if x is None else ((np.int64(1) << x.astype(np.int64)) & m) != 0
    out = []
    for e in (1, -1):
        ok = (g[2] == 2)                                                    # payer letter 7
        for p_, m in key['conds']:
            sg = e if '+' in p_ else -e
            if p_ in ('S.L+1', 'S.L-1'): c_ = inm(lw(sg), m)
            elif p_ in ('S.L+2', 'S.L-2'): c_ = inm(la(0 if sg > 0 else -1), m)
            elif p_ in ('R.L+2', 'R.L-2'): c_ = inm(lw(2 * sg), m)
            elif p_ in ('S.L+3', 'S.L-3'):
                if U != 7: continue
                LB = np.zeros((2, 5, 2, 5), dtype=bool)                     # [c, w2, a, o], OR over w3, w4 (outside the window)
                for (sg_, cc, w2, w3, w4, a_, o_), mm in L3T.items():
                    if sg_ == sg: LB[cc - 5, w2 - 5, a_ - 5, o_ - 5] |= bool(mm & m)
                cw, w2_ = lw(sg), lw(2 * sg); a_ = la(0 if sg > 0 else -1); o_ = la(-1 if sg > 0 else 0)
                c_ = np.where((cw <= 1) & (a_ <= 1), LB[np.minimum(cw, 1), w2_, np.minimum(a_, 1), o_], True)
            else:                                                           # S.A+-1
                wk = lw(sg); far = la(1 if sg > 0 else -2)
                if sg > 0: AB = (AM & m).astype(bool).any(axis=(3, 7)); six = AB[g[1], g[2], g[4], g[6], g[7], g[8]]
                else: AB = (AM & m).astype(bool).any(axis=(0, 4)); six = AB[g[0], g[2], g[3], g[5], g[6], g[7]]
                c_ = np.where(wk == 0, inm(far, m), np.where(wk == 1, six, True))
            ok = ok & c_
        out.append(np.ascontiguousarray(ok, dtype=np.uint8).reshape(-1))
    del g
    _EGTAB[ck] = tuple(out); return _EGTAB[ck]
def eg_widx(w, s, j):
    n = len(w); ix = 0
    for v in [w[(j + o) % n] for o in (-2, -1, 0, 1, 2)] + [s[(j + o) % n] for o in (-2, -1, 0, 1)]: ix = ix * 5 + (v - 5)
    return ix
def eg_terms(d, w, s):
    cf = collections.Counter(); U = min(d, 9)
    for key in EGKEYS:
        T = eg_tables(key, U); v = 0
        if T is not None: v += sum(int(T[0][ix]) + int(T[1][ix]) for ix in (eg_widx(w, s, j) for j in range(d) if w[j] == 7))
        if d == 7: v -= eg_payer_count(key, w, s)
        if v: cf[('ks', key['name'])] += v
    return cf
_orig_recv_coef_R2_eg = recv_coef_R2
def recv_coef_R2(d, lk, sv, xon, tau=None):
    cf = _orig_recv_coef_R2_eg(d, lk, sv, xon, tau)
    if EG:
        for k_, v_ in eg_terms(d, [int(ch) for ch in lk], [int(ch) for ch in sv]).items():
            cf[k_] += v_
            if cf[k_] == 0: del cf[k_]
    return cf
_orig_window_table_R2_eg = window_table_R2
def window_table_R2(U, y, x, MV2):
    W = _orig_window_table_R2_eg(U, y, x, MV2)
    if EG:
        for key in EGKEYS:
            v = KSV.get(key['name'], 0.0); T = eg_tables(key, U)
            if v != 0.0 and T is not None: W += v * (T[0].astype(np.float64) + T[1].astype(np.float64)).reshape((5,) * 9)
    return W
EG_KIND = {'S.L+1': (0, 1), 'S.L+2': (0, 2), 'S.L+3': (0, 3), 'S.L-1': (0, -1), 'S.L-2': (0, -2), 'S.L-3': (0, -3),
           'S.A+1': (1, 1), 'S.A-1': (1, -2), 'R.L+2': (1, 0), 'R.L-2': (1, -1)}   # payer frame: (0, r) = w_{i+r e}; (1, p) = apex(offsets p, p+1)
def eg_write():
    """argv[14] for jsepf at d = 7: int32 7802, int32 nkeys; per key: double amount (>= 0), int32 payee mask, int32 ncond,
    ncond x (int32 kind, int32 off, int32 mask)"""
    fn = os.path.join(WORK, 'edge_d7.bin'); b_ = [np.array([7802, len(EGKEYS)], dtype='<i4').tobytes()]
    for key in EGKEYS:
        v = float(KSV.get(key['name'], 0.0)); assert v >= -1e-12, 'edgekeys: negative amount %s %r' % (key['name'], v)
        b_.append(np.array([max(v, 0.0)], dtype='<f8').tobytes())
        cl_ = [(p_, 31 if ('egplant' in FLAGS and n_ == 0) else m_) for n_, (p_, m_) in enumerate(key['conds'])]   # CONTROL egplant: C++ payer cond 1 widened
        b_.append(np.array([key['vm'], len(cl_)] + [z for p_, m_ in cl_ for z in EG_KIND[p_] + (m_,)], dtype='<i4').tobytes())
    open(fn, 'wb').write(b''.join(b_)); return fn
def eg_force(rng, d):
    """a random arrangement with a planted payer (d = 7) or payee pattern of a random key"""
    w = [rng.choice((5, 6, 7, 8, 9)) for _ in range(d)]; s = [rng.choice((5, 6, 7, 8, 9)) for _ in range(d)]
    key = rng.choice(EGKEYS); i = rng.randrange(d); e = rng.choice((1, -1)); n = d
    pick = lambda m: rng.choice([l for l in LET if _eg_bit(l) & m])
    def setap(p, l):
        if e > 0: s[(i + p) % n] = l
        else: s[(i - p - 1) % n] = l
    if d == 7 and rng.random() < 0.5:   # payer
        w[i] = pick(key['vm'])
        for p_, m_ in key['conds']:
            kd, off = EG_KIND[p_]
            if kd == 0: w[(i + off * e) % n] = pick(m_)
            else: setap(off, pick(m_))
    else:                               # payee: centre is the payee, w_i = 7 the payer
        w[i] = 7
        for p_, m_ in key['conds']:
            sg = 1 if '+' in p_ else -1
            if p_[:3] == 'S.L' and p_[-1] == '1': w[(i + sg * e) % n] = pick(m_)
            elif p_[:3] == 'S.L' and p_[-1] == '2': setap(0 if sg > 0 else -1, pick(m_))
            elif p_[:3] == 'R.L': w[(i + 2 * sg * e) % n] = pick(m_)
            elif p_[:3] == 'S.A' and w[(i + sg * e) % n] == 5: setap(1 if sg > 0 else -2, pick(m_))
    return w, s
_orig_class_table_R2_eg = class_table_R2
def class_table_R2(xon):
    """mode-2 classes: fold the generic payee bounds (all keys, U, orientations) into the class of every window (the base class of a
    c >= 2 window lacks p and s, which the bounds read)"""
    C = _orig_class_table_R2_eg(xon)
    if not EG: return C
    sig = np.zeros(5 ** 9, dtype=np.int64); b_ = 0
    for key in EGKEYS:
        for U in (7, 8, 9):
            T = eg_tables(key, U)
            if T is None: continue
            for t_ in T: sig |= t_.astype(np.int64) << b_; b_ += 1
    assert b_ < 62
    u_, inv = np.unique(sig, return_inverse=True)
    C = C.reshape(-1).astype(np.int64); stride = int(C.max()) + 1
    C = np.where(C != 0, C + stride * inv.astype(np.int64), C); assert int(C.max()) < 2 ** 31 - 1, 'edgekeys: class fold overflow'
    log('edgekeys: mode-2 class fold: %d distinct payee-bound signatures' % len(u_))
    return C.astype(np.int32).reshape((5,) * 9)
