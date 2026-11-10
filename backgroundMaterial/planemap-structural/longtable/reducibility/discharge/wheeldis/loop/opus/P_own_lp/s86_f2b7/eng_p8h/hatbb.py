# hatbb.py (s86 eng_p8h, Opus team, 10 Nov 2026): HATBB columns (W6b round 7, HATBB_SPEC.md md5 a36ce8d2): a big vertex (7/8/9) pays
# a big APEX across one of its link edges (diamond u, x, b, y; triangles u x y and b x y share x y).  Built from the spec only (not from
# W6b's code).  exec'd by pcheck.py after edge56.py.  Flag hatbb + option hbkeys=<file>; without them this file does nothing.
#
# Keys: "NAME HAT(u->b)[POS=SET ...]" (trailing "# ..." ignored); u, b subsets of {7,8,9} (B = {7,8,9}, or a letter / {..});
# POS in X Y U-1 U+1 XA YA V-1 V+1 (the base positions; the extended U+-2/3, UA+-2/3 are refused here); SET as gkeys (5..9, S, B, *, {..}).
# Column ('ks', NAME) in [0, kscap] with the gk keys' cost (the EDGE / K* namespace), so sol files, KSV and upperR2 carry it unchanged.
#
# Rows: receivers only (centre letter U = min(d, 9) >= 7), coefficient IN - OUT; senders, cons2 and mrows get nothing (no slot has two
# big endpoints).  Slots: per link edge (w_i, w_{i+1}) with apex b = s_i, two orientations (x, y) = (w_i, w_{i+1}) and (w_{i+1}, w_i).
#   OUT (centre pays s_i), SURE match; IN (s_i pays the centre), POSSIBLE match; position sets as HATBB_SPEC 3.1 / 3.2.
# WINDOW BOUND (as gkwin; HATBB_SPEC 3.3): every slot of edge i is read on the gk window W_i = (w_{i-2..i+2}, s_{i-2..i+1}) only:
#   a link 6's private at w_i = amask(U, window) (f2b extra6 dropped); at w_{i+1} the same OR-ed over w_{i+3}, s_{i+2};
#   a link 7's private next to the big apex s_i is the wildcard (its side has an apex >= 7); its other private at d = 7 is L3T OR-ed over
#   the letters outside the window (extra7 dropped); at d >= 8 the wildcard; 8+ privates the wildcard.
#   Every one of these only ENLARGES a position's set: OUT (sure) can only lose slots, IN (possible) can only gain them, so the window
#   coefficient >= the spec's exact coefficient (hbselftest checks both).  Rows, WIN (jsepf / jsep3 / DP + Karp tail) and the mode-2
#   class fold all use this one table, so rows and separators agree exactly (as gkwin).  U = 9 tables (every d >= 9) read a link 6's
#   private as the WILDCARD (HATBB_SPEC: d >= 10 all; Lead 06:50Z); flag hbam9 (non-default) reads amask(9) there instead.
HBON = 'hatbb' in FLAGS; HBFILE = OPT.get('hbkeys')
assert HBON == (HBFILE is not None), 'hatbb: flag hatbb and option hbkeys=<file> go together'
HB_POS = ('X', 'Y', 'U-1', 'U+1', 'XA', 'YA', 'V-1', 'V+1')
HB_EXT = ('U+2', 'U+3', 'U-2', 'U-3', 'UA+2', 'UA+3', 'UA-2', 'UA-3')
HBKEYS = []
def hb_parse(line):
    line = line.split('#')[0].strip()
    m_ = re.match(r'^(\S+)\s+HAT\(([^-]+)->([^)]+)\)\[(.*)\]$', line)
    assert m_, 'hbkeys: bad line %r' % line
    nm, u, b, body = m_.groups()
    assert re.match(r'^[A-Za-z0-9_]+$', nm) and nm != 'K1', 'hbkeys: bad name %r' % nm
    um, bm = gk_set(u), gk_set(b)
    assert um and (um & ~28) == 0 and bm and (bm & ~28) == 0, 'hbkeys: payer / payee outside {7,8,9}: %r' % line
    conds = {}
    for tok in body.split():
        p_, v_ = tok.split('=')
        assert p_ not in HB_EXT, 'hbkeys: extended position %r not supported in eng_p8h (%r)' % (p_, line)
        assert p_ in HB_POS and p_ not in conds, 'hbkeys: bad position %r in %r' % (p_, line)
        conds[p_] = gk_set(v_)
    return dict(name=nm, um=um, bm=bm, m=np.array([conds.get(p_, 31) for p_ in HB_POS], dtype=np.uint8), rule=line.split(None, 1)[1])
if HBON:
    assert GKON and GKWIN and F16 and AC, 'hatbb: needs the gkwin stack (gkeys + gkwin + filt16 + apexcls)'
    for l_ in open(HBFILE):
        if l_.strip() and not l_.lstrip().startswith('#'): HBKEYS.append(hb_parse(l_))
    assert len({k['name'] for k in HBKEYS}) == len(HBKEYS), 'hbkeys: duplicate names'
    assert not ({k['name'] for k in HBKEYS} & (set(GKNAMES) | set(EGNAMES))), 'hbkeys: names clash with gkeys= / edgekeys='
    HBMD5 = hashlib.md5(open(HBFILE, 'rb').read()).hexdigest()[:8]
    log('hatbb: %d HAT big->big keys from %s (md5 %s); receivers only, window bound W_i (HATBB_SPEC 3.3)' % (len(HBKEYS), HBFILE, HBMD5))
else: HBMD5 = ''
HBNAMES = [k['name'] for k in HBKEYS]
HBWPLANT = 'hbwplant' in FLAGS   # CONTROL ONLY: WIN drops the HATBB OUT side
HBAM9 = 'hbam9' in FLAGS   # NON-DEFAULT: U = 9 tables read 6-privates as amask(9) at every d >= 9 (gk-window convention; not HATBB_SPEC at d >= 10)

# ---------------- slots ----------------
def hb_edge_sets(U, w0, w1, wm1, w2, sm1, s0, s1, Px, Py, Pxo, Pyo, xp=np):
    """bit sets for the 4 slots of the edge (w_i, w_{i+1}) with apex s_i: returns list of (kind, ub, vb, V[8]); inputs are bit arrays
    (or ints) for w_i, w_{i+1}, w_{i-1}, w_{i+2}, s_{i-1}, s_i, s_{i+1} and the privates (31 = wildcard)"""
    W = lambda c, t, f: xp.where(c, t, f) if xp is np else (t if c else f)
    five_x = (w0 == 1); five_y = (w1 == 1); six_x = (w0 == 2); six_y = (w1 == 2)
    Ux = W(five_x, sm1, Px); Uy = W(five_y, s1, Py)                 # b's (= the payer's) neighbour next to x / y other than y / x
    XAx = W(five_x, wm1, W(six_x, sm1, Pxo)); XAy = W(five_y, w2, W(six_y, s1, Pyo))
    cb = 1 << (min(U, 9) - 5)
    return [('O', cb, s0, [w0, w1, wm1, w2, sm1, s1, Ux, Uy]),          # 3.1, (x, y) = (w_i, w_{i+1})
            ('O', cb, s0, [w1, w0, w2, wm1, s1, sm1, Uy, Ux]),          # 3.1 mirror
            ('I', s0, cb, [w0, w1, Ux, Uy, XAx, XAy, wm1, w2]),         # 3.2, (x, y) = (w_i, w_{i+1})
            ('I', s0, cb, [w1, w0, Uy, Ux, XAy, XAx, w2, wm1])]         # 3.2 mirror
def hb_match(kind, ub, vb, V, key, xp=np):
    """OUT: sure (every set inside the key's set); IN: possible (every set meets it); masks kept non-negative for uint8 arrays"""
    m = key['m']
    if kind == 'O':
        ok = ((ub & (31 & ~key['um'])) == 0) & ((vb & (31 & ~key['bm'])) == 0)
        for p in range(8):
            if m[p] != 31: ok = ok & ((V[p] & (31 & ~int(m[p]))) == 0)
    else:
        ok = ((ub & key['um']) != 0) & ((vb & key['bm']) != 0)
        for p in range(8):
            if m[p] != 31: ok = ok & ((V[p] & int(m[p])) != 0)
    return ok

# ---------------- exact (spec) coefficient on a full label (hbselftest reference) ----------------
def hb_recv_exact(d, w, s):
    """{name: (IN, OUT)} by HATBB_SPEC 3.1 / 3.2 on the full label; privates from gk_recv_picture (link 6: amask & ~extra6 for d <= 9,
    else the wildcard; link 7 at d = 7: L3T & ~extra7 when its neighbour and apex on that side are <= 6; else the wildcard)"""
    l3q_load(); kt_load()
    A, PV = gk_recv_picture(d, w, s); n = d; U = min(d, 9)
    wb = [_gkbit(x) for x in w]
    def prv(j, side):
        p = PV[j % n]
        return 31 if p is None else p[side]
    res = {k['name']: [0, 0] for k in HBKEYS}
    for i in range(n):
        j1 = (i + 1) % n
        sl = hb_edge_sets(U, wb[i], wb[j1], wb[(i - 1) % n], wb[(i + 2) % n], A[(i - 1) % n], A[i], A[j1],
                          prv(i, 1), prv(j1, 0), prv(i, 0), prv(j1, 1), xp=None)
        for kind, ub, vb, V in sl:
            for key in HBKEYS:
                if hb_match(kind, ub, vb, V, key, xp=None): res[key['name']][0 if kind == 'I' else 1] += 1
    return res

# ---------------- window tables ----------------
_HBTAB = {}
def _hb_privs(U):
    """window privates over the 5^9 index (w_{i-2..i+2}, s_{i-2..i+1}): Px, Py (next to s_i), Pxo, Pyo (the other side), uint8"""
    kt_load(); l3q_load()
    g = np.indices((5,) * 9, dtype=np.int8).reshape(9, -1)
    lw = lambda r: g[r + 2]; la = lambda t: g[5 + t + 2]
    AM = (31 & ~np.asarray(KT[U]).astype(np.int64)).astype(np.uint8)       # amask(U, w-2, w-1, w+1, w+2, s-2, s-1, s0, s+1) - 5
    P6x = AM[g[0], g[1], g[3], g[4], g[5], g[6], g[7], g[8]]                 # the 6 at w_i (window centre): its one private
    AMp = np.bitwise_or.reduce(np.bitwise_or.reduce(AM, axis=7), axis=3)       # a 6 at j = i+1: OR over w_{j+2} = w_{i+3} and s_{j+1} = s_{i+2}
    P6y = AMp[g[1], g[2], g[4], g[6], g[7], g[8]]                            # (w_{i-1}, w_i, w_{i+2}, s_{i-1}, s_i, s_{i+1})
    full = np.full(g.shape[1], 31, dtype=np.uint8)
    if U == 9 and not HBAM9: P6x = P6y = full   # Lead 06:50Z / HATBB_SPEC 3: a link 6's private is the wildcard at d >= 10; the U = 9 table serves every d >= 9
    Px = np.where(lw(0) == 1, P6x, full).astype(np.uint8); Py = np.where(lw(1) == 1, P6y, full).astype(np.uint8)
    Pxo = full.copy(); Pyo = full.copy()
    if U == 7:   # a 7's private on the side of s_{i-1} (at w_i) / s_{i+1} (at w_{i+1}): L3T OR-ed over the letters outside the window
        L3 = {sg: np.zeros((2, 5, 5, 5, 2, 5), dtype=np.uint8) for sg in (1, -1)}
        for (sg, c, w2, w3, w4, ap_, o_), m in L3T.items():
            L3[sg][c - 5, w2 - 5, w3 - 5, w4 - 5, ap_ - 5, o_ - 5] |= np.uint8(m)
        L334 = {sg: np.bitwise_or.reduce(np.bitwise_or.reduce(L3[sg], axis=3), axis=2) for sg in (1, -1)}   # [c, w2, ap, o]
        L3all = {sg: np.bitwise_or.reduce(L334[sg], axis=1) for sg in (1, -1)}                              # [c, ap, o]
        def okv(c, ap_): return (c <= 1) & (ap_ <= 1)
        # 7 at w_i, side sg = -1: (c, w2, ap, o) = (w_{i-1}, w_{i-2}, s_{i-1}, s_i); w_{i-3}, w_{i-4} outside
        c_, a_ = lw(-1), la(-1)
        v_ = L334[-1][np.minimum(c_, 1), lw(-2), np.minimum(a_, 1), la(0)]
        Pxo = np.where((lw(0) == 2) & okv(c_, a_), v_, 31).astype(np.uint8)
        # 7 at w_{i+1}, side sg = +1: (c, ap, o) = (w_{i+2}, s_{i+1}, s_i); w_{i+3..i+5} outside
        c_, a_ = lw(2), la(1)
        v_ = L3all[1][np.minimum(c_, 1), np.minimum(a_, 1), la(0)]
        Pyo = np.where((lw(1) == 2) & okv(c_, a_), v_, 31).astype(np.uint8)
    return g, Px, Py, Pxo, Pyo
def hb_tables(U):
    """{name: (HI, HO)} uint8 over the 5^9 window index of edge i (both orientations summed): possible IN slots, sure OUT slots"""
    if U in _HBTAB: return _HBTAB[U]
    g, Px, Py, Pxo, Pyo = _hb_privs(U)
    B = lambda x: (np.uint8(1) << x.astype(np.uint8)).astype(np.uint8)
    lw = lambda r: B(g[r + 2]); la = lambda t: B(g[5 + t + 2])
    sl = hb_edge_sets(U, lw(0), lw(1), lw(-1), lw(2), la(-1), la(0), la(1), Px, Py, Pxo, Pyo)
    out = {}
    for key in HBKEYS:
        HI = np.zeros(g.shape[1], dtype=np.uint8); HO = np.zeros(g.shape[1], dtype=np.uint8)
        for kind, ub, vb, V in sl:
            ok = hb_match(kind, ub, vb, V, key)
            if kind == 'I': HI += np.broadcast_to(ok, HI.shape).astype(np.uint8)
            else: HO += np.broadcast_to(ok, HO.shape).astype(np.uint8)
        out[key['name']] = (HI, HO)
    _HBTAB[U] = out; return out
def hb_recv_win(d, w, s):
    """{name: (IN, OUT)} window-bound counts on the label (the row coefficient is IN - OUT)"""
    U = min(d, 9); T = hb_tables(U); ix = [_gk_widx(w, s, i) for i in range(d)]
    return {nm: (sum(int(T[nm][0][i_]) for i_ in ix), sum(int(T[nm][1][i_]) for i_ in ix)) for nm in HBNAMES}
def hb_recv_terms(d, w, s):
    cf = collections.Counter()
    if not HBON or d < 7: return cf
    for nm, (gi, po) in hb_recv_win(d, w, s).items():
        if gi - po: cf[('ks', nm)] = gi - po
    return cf
if HBON:
    _orig_recv_coef_R2_hb = recv_coef_R2
    def recv_coef_R2(d, lk, sv, xon, tau=None):
        cf = _orig_recv_coef_R2_hb(d, lk, sv, xon, tau)
        for k_, v_ in hb_recv_terms(d, [int(ch) for ch in lk], [int(ch) for ch in sv]).items():
            cf[k_] += v_
            if cf[k_] == 0: del cf[k_]
        return cf
    _orig_window_table_R2_hb = window_table_R2
    def window_table_R2(U, y, x, MV2):
        W = _orig_window_table_R2_hb(U, y, x, MV2)
        if U >= 7:
            T = hb_tables(min(U, 9))
            for nm in HBNAMES:
                v = KSV.get(nm, 0.0)
                if v != 0.0: W += v * (T[nm][0].astype(np.float64) - (0 if HBWPLANT else T[nm][1].astype(np.float64))).reshape((5,) * 9)   # HBWPLANT: CONTROL ONLY (F2B-SELFTEST must FAIL)
        return W
    _orig_class_table_R2_hb = class_table_R2
    def class_table_R2(xon):
        """mode-2 classes: fold every HATBB table (IN and OUT, U = 7, 8, 9; values 0..2) into the class of every window"""
        C = _orig_class_table_R2_hb(xon)
        tabs = [T for U in (7, 8, 9) for nm in HBNAMES for T in hb_tables(U)[nm] if T.any()]
        nb_ = 2 * len(tabs); P = np.zeros((5 ** 9, max(1, (nb_ + 7) // 8)), dtype=np.uint8); b_ = 0
        for T in tabs:
            for bit in (1, 2):
                P[:, b_ // 8] |= (((T & bit) != 0).astype(np.uint8) << np.uint8(b_ % 8)); b_ += 1
        u_, inv = np.unique(P, axis=0, return_inverse=True); inv = inv.reshape(-1)
        C = C.reshape(-1).astype(np.int64); nz = C != 0
        pair = C * np.int64(len(u_)) + inv.astype(np.int64); _, rn = np.unique(pair[nz], return_inverse=True)
        C2 = np.zeros_like(C); C2[nz] = rn.reshape(-1).astype(np.int64) + 1; assert int(C2.max()) < 2 ** 31 - 1, 'hatbb: class fold overflow'
        log('hatbb: mode-2 class fold: %d distinct HATBB signatures over %d tables' % (len(u_), len(tabs)))
        return C2.astype(np.int32).reshape((5,) * 9)

def cmd_hbselftest():
    """(1) spec worked examples (HATBB_SPEC 5); (2) exact coefficient = W6b's results/hbrows16x_*.json on every receiver row of the eval
    certs (hbcert=<c1,c2> hbref=<r1,r2>, paired); (3) window bound vs exact on those rows and on random receivers d = 7, 8, 9:
    IN_win >= IN_exact and OUT_win <= OUT_exact, key by key"""
    assert HBON; l3q_load(); kt_load(); bad = 0
    ex = [(8, '55556859', '58576556', 'HB03', (0, 1)), (8, '55556776', '58576658', 'HB03', (0, 1)), (7, '7657567', '6755765', 'HB03', (2, 0))]
    for d, lk, sv, nm, want in ex:
        if nm not in HBNAMES: continue
        got = tuple(hb_recv_exact(d, [int(c) for c in lk], [int(c) for c in sv])[nm])
        log('  hbselftest spec 5: R%d %s/%s %s exact (IN, OUT) = %s, spec %s %s' % (d, lk, sv, nm, got, want, 'ok' if got == want else 'FAIL'))
        bad += got != want
    certs = [c for c in OPT.get('hbcert', '').split(',') if c]; refs = [r for r in OPT.get('hbref', '').split(',') if r]
    assert len(certs) == len(refs)
    STAT = collections.Counter(); DIFF = []
    for cf_, rf_ in zip(certs, refs):
        R = json.load(open(rf_)); ref = {}
        for nm, v in R['keys'].items():
            for lab, w_, c_ in v['rows']: ref[(nm, lab)] = c_
        rows = {(r['row'][1], r['row'][2], r['row'][3]) for r in json.load(open(cf_)) if r['row'][0] == 'receiverR2'}
        seen = set()
        for d, lk, sv in sorted(rows):
            w = [int(c) for c in lk]; s = [int(c) for c in sv]; lab = 'R%d %s/%s' % (d, lk, sv)
            ex_ = hb_recv_exact(d, w, s); wn_ = hb_recv_win(d, w, s)
            for nm in HBNAMES:
                e_ = ex_[nm][0] - ex_[nm][1]; r_ = ref.get((nm, lab), 0); seen.add((nm, lab))
                STAT['pairs'] += 1
                if e_ == r_: STAT['exact=W6b'] += 1
                else:
                    STAT['exact!=W6b d%d' % d] += 1
                    if len(DIFF) < 12: DIFF.append('%s %s exact %d (IN %d OUT %d) W6b %d' % (nm, lab, e_, ex_[nm][0], ex_[nm][1], r_))
                wi, wo = wn_[nm]
                if HBAM9 and d >= 10 and (wi < ex_[nm][0] or wo > ex_[nm][1]):   # hbam9 only: amask(9) window vs the spec's wildcard private
                    STAT['window amask9 vs wildcard d%d' % d] += 1
                    if len(DIFF) < 24: DIFF.append('INFO d>=10 %s %s window (IN %d OUT %d) exact (IN %d OUT %d)' % (nm, lab, wi, wo, *ex_[nm]))
                elif wi < ex_[nm][0] or wo > ex_[nm][1]:
                    STAT['WINDOW-BOUND-VIOLATION d%d' % d] += 1; bad += 1
                    if len(DIFF) < 24: DIFF.append('BOUND %s %s window (IN %d OUT %d) exact (IN %d OUT %d)' % (nm, lab, wi, wo, *ex_[nm]))
                elif (wi, wo) != tuple(ex_[nm]): STAT['window>exact d%d' % d] += 1
        miss = [k for k in ref if k not in seen]
        if miss: log('  hbselftest: %d W6b entries not among the cert receiver rows, e.g. %s' % (len(miss), miss[:3]))
    for l_ in DIFF: log('   ', l_)
    log('  hbselftest rows: %s' % dict(sorted(STAT.items())))
    rng = np.random.default_rng(int(OPT.get('seed', '7'))); N = int(OPT.get('hbN', '3000')); RS = collections.Counter()
    for d in (7, 8, 9, 10, 11):
        for _ in range(N):
            w = list(rng.choice([5, 6, 7, 8, 9], size=d, p=[.35, .35, .2, .05, .05])); s = list(rng.choice([5, 6, 7, 8, 9], size=d, p=[.3, .3, .25, .1, .05]))
            if admissible(d, ''.join(map(str, w)), ''.join(map(str, s))) is not None: continue
            ex_ = hb_recv_exact(d, w, s); wn_ = hb_recv_win(d, w, s); RS['rows d%d' % d] += 1
            for nm in HBNAMES:
                wi, wo = wn_[nm]; ei, eo = ex_[nm]
                if (d <= 9 or not HBAM9) and (wi < ei or wo > eo):
                    bad += 1; RS['BOUND-VIOLATION d%d' % d] += 1
                    if RS['BOUND-VIOLATION d%d' % d] <= 3: log('   random BOUND %s R%d %s/%s window (%d, %d) exact (%d, %d)' % (nm, d, ''.join(map(str, w)), ''.join(map(str, s)), wi, wo, ei, eo))
                if (wi, wo) != (ei, eo): RS['window!=exact d%d' % d] += 1
                if ei or eo: RS['exact nonzero d%d' % d] += 1
    log('  hbselftest random (bound checked at every d%s): %s' % (' <= 9; hbam9: d >= 10 info only' if HBAM9 else '', dict(sorted(RS.items()))))
    log('HBSELFTEST: %s (%d failures)' % ('PASS' if bad == 0 else 'FAIL', bad))
