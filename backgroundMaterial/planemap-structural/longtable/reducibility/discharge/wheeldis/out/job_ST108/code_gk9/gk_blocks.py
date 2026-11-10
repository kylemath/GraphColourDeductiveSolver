# W17 round 4 test blocks, exec'd by st21_w17.py (code_gk) after the separator tables are built (needs GKKEYS, GKENG, GKWIN, GKF,
# gk_recv_terms, gk_send_terms, gk_cons_terms, GKREL_, GKWNP, recv_spec, spec_val, sepx, SEPX, yv, xv, KSV, pmask, MASK, f2b_extra).
# code_gk9: with HATBB keys loaded, GKST_ONLY=1 does not exit here: hb_blocks.py (HBST) runs next and prints the verdict.
def _gk_pick(rr_, m, lets=LET):
    c_ = [l for l in lets if (m >> (l - 5)) & 1]
    return rr_.choice(c_) if c_ else rr_.choice(lets)
def _gk_plant(rr_, d, key, role):
    """a random degree-d arrangement where key's IN slot (role 'in', payer = a link vertex) or OUT slot (role 'out', the centre pays
    a link vertex: d = 7 payer 7, code_gk8: d = 8 payer 8, d >= 9 payer 9) is set up at a random position and chirality from the
    key's own sets (other letters random)"""
    n_, U_, V_, cd_ = key
    w_ = [rr_.choice((5, 5, 6, 6, 7, 7, 7, 8, 9)) for _ in range(d)]; s_ = [rr_.choice((5, 5, 6, 6, 7, 7, 8, 9)) for _ in range(d)]
    j = rr_.randrange(d); e = rr_.choice((1, -1))
    def setab(a, b, v):
        a %= d; b %= d
        if b == (a + 1) % d: s_[a] = v
        else: s_[b] = v
    if role == 'out':
        w_[j] = _gk_pick(rr_, V_)
        for pi, m in cd_:
            v = _gk_pick(rr_, m)
            if pi in (0, 1, 2): w_[(j + (pi + 1) * e) % d] = v
            elif pi in (3, 4, 5): w_[(j - (pi - 2) * e) % d] = v
            elif pi == 6: setab(j + e, j + 2 * e, v)
            elif pi == 7: setab(j - e, j - 2 * e, v)
            elif pi == 8: setab(j, j + e, v)
            elif pi == 10: setab(j, j - e, v)
    else:
        p_ = _gk_pick(rr_, U_); w_[j] = p_   # code_gk8: payer letters 5..9
        cdd = dict(cd_)
        for pi, m in cd_:
            v = _gk_pick(rr_, m)
            if pi == 0: w_[(j + e) % d] = v if v <= 9 else 9
            elif pi == 3: w_[(j - e) % d] = v
            elif pi == 1: setab(j, j + e, v)
            elif pi == 4: setab(j, j - e, v)
            elif pi == 8: w_[(j + 2 * e) % d] = v
            elif pi == 10: w_[(j - 2 * e) % d] = v
        if p_ == 5:   # the payer 5's S.L+-3 are its apexes: pick them inside both sets where possible
            for pi, sd in ((2, -e), (5, e)):
                if pi in cdd: setab(j, j + sd, _gk_pick(rr_, cdd[pi] & cdd.get(1 if sd == e else 4, 31) or cdd[pi]))
        for pi, sd in ((6, e), (7, -e)):   # a 5 neighbour: its far apex
            if pi in cdd and w_[(j + sd) % d] == 5: setab(j + sd, j + 2 * sd, _gk_pick(rr_, cdd[pi]))
        w_[j] = p_
    if rr_.random() < 0.5: k_ = rr_.randrange(d); w_ = w_[k_:] + w_[:k_]; s_ = s_[k_:] + s_[:k_]
    if rr_.random() < 0.5: w_ = w_[::-1]; s_ = s_[::-1][1:] + s_[::-1][:1]   # reflection (s_i sits between w_i and w_{i+1})
    return w_, s_
def _gk_gen(rr_, d, n, keys):
    out = []
    for q_ in range(n):
        if q_ % 3 == 0 or not keys:
            out.append(([rr_.choice((5, 5, 5, 6, 6, 7, 7, 8, 9)) for _ in range(d)], [rr_.choice((5, 5, 6, 6, 7, 7, 8, 9)) for _ in range(d)])); continue
        key = keys[(q_ // 3) % len(keys)]
        role = 'out' if (q_ % 3 == 2 and ((d == 7 and (key[1] >> 2) & 1) or (d == 8 and (key[1] >> 3) & 1) or (d >= 9 and (key[1] >> 4) & 1))) else 'in'   # code_gk8
        out.append(_gk_plant(rr_, d, key, role))
    return out
def _gk_win_of(d, w_, s_, j):
    W_ = lambda k: min(w_[k % d], 9); S_ = lambda k: min(s_[k % d], 9)
    return (W_(j - 2), W_(j - 1), W_(j), W_(j + 1), W_(j + 2), S_(j - 2), S_(j - 1), S_(j), S_(j + 1))
# ---------------- GKST: window tables (numpy vs scalar), per-position bound, C++ leaf vs Python rows -------------------------------
if GKKEYS and os.environ.get('GKST', '1') != '0':
    _rr = random.Random(int(os.environ.get('GKSEED', '4004'))); _amt = {k_[0]: KSV.get(k_[0], 0.0) for k_ in GKKEYS}
    _nzk = [k_ for k_ in GKKEYS if _amt[k_[0]] > 0]
    # (1) numpy gkwin table vs gkfam.Win on random windows (and windows read from planted arrangements)
    _wb = 0; _wn = 0; _wpos = 0; _wneg = 0
    for _ in range(int(os.environ.get('GKSTW', '30000'))):
        U_ = _rr.choice((7, 8, 9))
        if _rr.random() < 0.5 and _nzk:
            k_ = _rr.choice(_nzk); ro_ = 'in'
            if k_[1] in (8, 16) and _rr.random() < 0.5: ro_ = 'out'; U_ = 8 if k_[1] == 8 else 9   # code_gk8: plant a payer-8/9 OUT slot
            d_ = U_ if U_ < 9 else _rr.choice((9, 10, 11)); w_, s_ = _gk_plant(_rr, d_, k_, ro_)
            j_ = _rr.randrange(d_); win = _gk_win_of(d_, w_, s_, j_)
        else: win = tuple(_rr.choice(LET) for _ in range(9))
        a_ = sum(_amt[GKENG.names[q]] for q in GKWIN.counts(U_, *win)) - sum(_amt[GKENG.names[q]] for q in GKWIN.out_counts(U_, *win))   # code_gk8: IN - OUT
        b_ = GKWNP[U_ - 7][tuple(x - 5 for x in win)]
        _wn += 1; _wpos += a_ > 0; _wneg += a_ < 0
        if abs(a_ - b_) > 1e-12: _wb += 1; _wb <= 5 and print('GK WINDOW TABLE MISMATCH U=%d %s scalar %.15g numpy %.15g' % (U_, win, a_, b_))
    print('W17 GK window tables: %d windows, %d with credit > 0, %d with credit < 0 (payer-8/9 OUT); numpy vs gkfam.Win mismatches %d' % (_wn, _wpos, _wneg, _wb), flush=True)
    if _wb: fail('W17 GK numpy window table differs from gkfam.Win')
    # (2) C++ exact leaf ('e') vs Python rows, d = 7..GKSTD, random + planted; (3) per-position credit <= GKREL
    _mx = {}; _bad = 0; _cmp = 0; _inadm = 0; _nz = collections.Counter(); _pb = 0; _ptot = 0; _ptight = 0
    for d in range(7, int(os.environ.get('GKSTD', '12')) + 1):
        sepx(d, yv, xv, 1e9, 1)
        n_ = int(os.environ.get('GKSTN', '3000')) if d <= 9 else int(os.environ.get('GKSTN2', '600'))
        for w_, s_ in _gk_gen(_rr, d, n_, _nzk):
            lk, sv = ''.join(map(str, w_)), ''.join(map(str, s_))
            rs_ = recv_spec(d, lk, sv); gk_ = {k_[1]: cf_ for k_, cf_ in rs_.items() if k_[0] == 'ks' and _amt.get(k_[1], 0.0) > 0}
            if d == 7:
                P_ = GKF.recv7_pic(w_, s_, pmask, MASK, lambda k_: _ksx(7, w_, s_, k_, ('w6', 7)), lambda k_, f_: _ksx(7, w_, s_, k_, ('w7', 7, f_)))
                o_, i_ = GKENG.pic_counts(P_)
                _nz[(d, 'out>0')] += any(o_[n] and _amt[n] > 0 for n in o_); _nz[(d, 'in>0')] += any(i_[n] and _amt[n] > 0 for n in i_)
                for j_ in range(d):   # per-position IN credit (exact picture) <= GKREL at that position (code_gk8: link 8 / 9 payers too)
                    ex_ = sum(_amt[GKENG.names[q]] for e_ in (1, -1) for q in GKENG.in_hits(GKF.bit(w_[j_]), GKF.bit(7), P_.in_vec(j_, e_)))
                    rel_ = GKREL_[0, (w_[(j_ - 1) % d] - 5) * 25 + (s_[(j_ - 1) % d] - 5) * 5 + w_[j_] - 5, (s_[j_] - 5) * 5 + w_[(j_ + 1) % d] - 5]
                    _ptot += 1; _ptight += abs(ex_ - rel_) < 1e-15
                    if ex_ > rel_ + 1e-12: _pb += 1; _pb <= 5 and print('GK BOUND BELOW EXACT d=7 %s %s j=%d exact %.12g window %.12g' % (lk, sv, j_, ex_, rel_))
            else:
                _nz[(d, 'in>0')] += bool(gk_)
                _nz[(d, 'coef<0')] += any(v_ < 0 for v_ in gk_.values())   # code_gk8: rows where a payer-8/9 OUT wins
                for j_ in range(d):   # code_gk8: every position (payer 8 / 9 IN, centre OUT)
                    win = _gk_win_of(d, w_, s_, j_); ex_ = GKWNP[min(d, 9) - 7][tuple(x - 5 for x in win)]
                    rel_ = GKREL_[min(d, 9) - 7, (win[1] - 5) * 25 + (win[6] - 5) * 5 + win[2] - 5, (win[7] - 5) * 5 + win[3] - 5]
                    _ptot += 1; _ptight += abs(ex_ - rel_) < 1e-15
                    if ex_ > rel_ + 1e-12: _pb += 1
            SEPX.stdin.write('e %d %s %s\n' % (d, lk, sv)); SEPX.stdin.flush(); out_ = SEPX.stdout.readline().strip()
            if out_ == 'inadm': _inadm += 1; continue
            cv_ = float(out_); pv_ = sum(cf * val(k) for k, cf in rs_.items()); _cmp += 1
            _mx[d] = max(_mx.get(d, 0.0), abs(cv_ - pv_)); _nz[(d, 'compared with gk')] += bool(gk_)
            if abs(cv_ - pv_) > 1e-9:
                _bad += 1
                if _bad <= 5: print('GK SELFTEST MISMATCH d=%d %s %s python %.12f c++ %.12f (gk terms %s)' % (d, lk, sv, pv_, cv_, gk_), flush=True)
    print('W17 GK self-test (C++ leaf vs Python rows, all families on): %d compared, %d window-inadmissible; max |difference| by d %s; mismatches > 1e-9: %d' % (
        _cmp, _inadm, {k_: float('%.3g' % v_) for k_, v_ in sorted(_mx.items())}, _bad), flush=True)
    print('W17 GK self-test rows with a nonzero key term (amount > 0): %s' % ', '.join('d%d %s %d' % (k_[0], k_[1], v_) for k_, v_ in sorted(_nz.items())), flush=True)
    print('W17 GK per-position bound check: %d positions, window bound == exact on %d, exact above bound %d' % (_ptot, _ptight, _pb), flush=True)
    if _bad: fail('W17 GK self-test: C++ leaf and Python rows differ')
    if _pb: fail('W17 GK window bound below the exact per-position credit')
    if os.environ.get('GKST_ONLY') == '1' and not HBKEYS: print('VERDICT: W17 GK SELFTEST %s' % ('PASS' if not FAIL else 'FAIL: ' + ' | '.join(FAIL))); sys.exit(0)
# ---------------- GKORACLE=N: W6's r9_rows.py (round 9) as an independent oracle (copied to ORACLEDIR, shim r5lib with this
# checker's pmask / MASK / f2b_extra) on N random + planted receivers per d = 7..10, every sender label, and GKORC cons2 labels ----
if GKKEYS and os.environ.get('GKORACLE'):
    sys.path.insert(0, os.environ.get('ORACLEDIR', '/tmp/swarm-W17/oracle'))
    import r5lib as _R5S
    _R5S.W.NS = {'pmask': pmask, 'MASK': MASK, 'MASK8': MASK8, 'f2b_extra': f2b_extra, 'F2BR': F2BR}
    import grammar as GR, r9_rows as R9
    _rr = random.Random(int(os.environ.get('GKORSEED', '909'))); _N = int(os.environ['GKORACLE'])
    def _orc_coef(pics_or_slots, sign_in, sign_out, nrows):
        """per key: coefficient arrays from a SlotTable over (rid, slot) items"""
        TB = GR.SlotTable(pics_or_slots).G['EDGE']; res = {}
        for n_, U_, V_, cd_ in GKKEYS:
            sure, poss = GR.match(TB, U_, V_, dict(cd_))
            co = _np.bincount(TB['rid'][TB['out'] & sure], minlength=nrows); ci = _np.bincount(TB['rid'][~TB['out'] & poss], minlength=nrows)
            res[n_] = (co, ci)
        return res
    _rep = collections.Counter(); _ex = []
    def _cmp(tag, mine, orc, nrows, labels):
        for n_, U_, V_, cd_ in GKKEYS:
            co, ci = orc[n_]
            for r_ in range(nrows):
                mo, mi = mine[r_][0][n_], mine[r_][1][n_]
                _rep[(tag, 'slots')] += 1; _rep[(tag, 'nonzero')] += (mo or mi) > 0
                if (mo, mi) != (int(co[r_]), int(ci[r_])):
                    _rep[(tag, 'mismatch')] += 1
                    if len(_ex) < 12: _ex.append((tag, n_, labels[r_], mo, int(co[r_]), mi, int(ci[r_])))
    # receivers d = 7: KEYSPEC picture (r9_rows.recv_pic) vs mine (out, in)
    for d in (7, 8, 9, 10):
        arrs = _gk_gen(_rr, d, _N, GKKEYS)
        if d == 7:
            items = []; mine = []
            for r_, (w_, s_) in enumerate(arrs):
                for sl_ in GR.slots(R9.recv_pic(7, w_, s_)):
                    if sl_[0] == 'EDGE': items.append((r_, sl_))
                P_ = GKF.recv7_pic(w_, s_, pmask, MASK, lambda k_, w_=w_, s_=s_: _ksx(7, w_, s_, k_, ('w6', 7)), lambda k_, f_, w_=w_, s_=s_: _ksx(7, w_, s_, k_, ('w7', 7, f_)))
                mine.append(GKENG.pic_counts(P_))
            _cmp('recv d=7 (recv_pic)', mine, _orc_coef(items, 1, -1, len(arrs)), len(arrs), [(''.join(map(str, w_)), ''.join(map(str, s_))) for w_, s_ in arrs])
        else:   # d >= 8: Opus's gkwin (r9_rows.win_vecs) vs mine; recv_pic differences counted (expected)
            mine = []; orc = {n_: (_np.zeros(len(arrs), int), _np.zeros(len(arrs), int)) for n_ in [k_[0] for k_ in GKKEYS]}; picdiff = 0
            for r_, (w_, s_) in enumerate(arrs):
                mine.append((collections.Counter(), GKWIN.row(d, w_, s_)))
                U_ = min(d, 9); vv = R9.win_vecs(d, w_, s_)
                for n_, Uk, Vk, cd_ in GKKEYS:
                    if not (Vk >> (U_ - 5)) & 1: continue
                    orc[n_][1][r_] = sum(1 for ub, v14 in vv if ub & Uk and all(v14[p_] & m_ for p_, m_ in cd_))
                pc = collections.Counter()   # the KEYSPEC picture at this d (recv_pic, a different object): IN possible counts
                for sl_ in GR.slots(R9.recv_pic(d, w_, s_)):
                    if sl_[0] != 'EDGE' or sl_[1] != 'in': continue
                    for n_, Uk, Vk, cd_ in GKKEYS:
                        if sl_[2] & Uk and sl_[3] & Vk and all(sl_[4][p_] & m_ for p_, m_ in cd_): pc[n_] += 1
                picdiff += any(pc[n_] != mine[-1][1][n_] for n_ in [k_[0] for k_ in GKKEYS])
            _cmp('recv d=%d (win_vecs)' % d, mine, orc, len(arrs), [(''.join(map(str, w_)), ''.join(map(str, s_))) for w_, s_ in arrs])
            _rep[('recv d=%d' % d, 'rows where recv_pic differs from gkwin (expected)')] = picdiff
    # senders: every admissible label (w, H, F) of the sender loop (one per distinct row), generic_pic as r5lib.send_pic
    labs = []
    for w in SENDERS:
        sixes = [k for k in range(5) if w[k] == 6]
        for hb in itertools.product((0, 1), repeat=5):
            for fb in itertools.product((0, 1), repeat=len(sixes)):
                H_ = dict(zip(range(5), hb)); F_ = dict(zip(sixes, fb))
                if sender_row(w, H_, F_) is None: continue
                labs.append((w, H_, F_))
    if os.environ.get('GKORSEND'): _rr.shuffle(labs); labs = labs[:int(os.environ['GKORSEND'])]
    items = []; mine = []
    for r_, (w, H_, F_) in enumerate(labs):
        pv = [[GR.CLS[F_[i]]] if w[i] == 6 else [GR.ALL] * (w[i] - 5) for i in range(5)]
        for sl_ in GR.slots(R9.generic_pic('S', 5, list(w), [GR.CLS[H_[k]] for k in range(5)], pv, 'S')):
            if sl_[0] == 'EDGE': items.append((r_, sl_))
        mine.append(GKENG.pic_counts(GKF.sender_pic(list(w), [H_[k] for k in range(5)], [F_.get(k, 0) for k in range(5)])))
    _cmp('sender', mine, _orc_coef(items, -1, 1, len(labs)), len(labs), [(''.join(map(str, w)), ''.join(str(H_[k]) for k in range(5)), str(F_)) for w, H_, F_ in labs])
    # cons2: GKORC labels (L, class word) over the 1,424 non-R6 6-links x 2^6 apex classes (r5lib.cons_pic 'ap' mode)
    cl = [(L, s) for L in ALL6 for s in itertools.product((5, 7), repeat=6)]
    _rr.shuffle(cl); cl = cl[:int(os.environ.get('GKORC', '20000'))]
    items = []; mine = []
    for r_, (L, s) in enumerate(cl):
        for sl_ in GR.slots(R9.generic_pic('C', 6, list(L), [GR.SYM['B'] if x >= 7 else GR.SYM['S'] for x in s], [[GR.ALL] * (x - 5) for x in L], 'C')):
            if sl_[0] == 'EDGE': items.append((r_, sl_))
        mine.append(GKENG.pic_counts(GKF.cons2_pic(list(L), list(s))))
    _cmp('cons2', mine, _orc_coef(items, 1, -1, len(cl)), len(cl), [(''.join(map(str, L)), ''.join(map(str, s))) for L, s in cl])
    # the row functions used by the checker equal the counts compared above (sign conventions)
    _sg = 0
    for w, H_, F_ in labs[:3000]:
        o_, i_ = GKENG.pic_counts(GKF.sender_pic(list(w), [H_[k] for k in range(5)], [F_.get(k, 0) for k in range(5)])); t_ = gk_send_terms(w, H_, F_)
        _sg += any(t_.get(('ks', n_), 0) != o_[n_] - i_[n_] for n_ in GKENG.names)
    for L, s in cl[:3000]:
        o_, i_ = GKENG.pic_counts(GKF.cons2_pic(list(L), list(s))); t_ = gk_cons_terms(L, s)
        _sg += any(t_.get(('ks', n_), 0) != i_[n_] - o_[n_] for n_ in GKENG.names)
    for tag in sorted({k_[0] for k_ in _rep}):
        print('GKORACLE %s: %s' % (tag, ', '.join('%s %d' % (k_[1], v_) for k_, v_ in sorted(_rep.items()) if k_[0] == tag)), flush=True)
    for x_ in _ex: print('GKORACLE MISMATCH %s key %s row %s: mine out %d oracle out %d, mine in %d oracle in %d' % x_, flush=True)
    print('GKORACLE row-function sign check: %d rows differ' % _sg, flush=True)
    _ob = sum(v_ for k_, v_ in _rep.items() if k_[1] == 'mismatch') + _sg
    print('VERDICT: GKORACLE %s (mismatches %d; oracle fallbacks %s)' % ('PASS' if _ob == 0 else 'FAIL', _ob, dict(R9.FALLBACK)), flush=True)
    sys.exit(0)
# ---------------- GKPLANTFIND=1: candidates for the planted controls (c), then exit ----------------
#   (c1) the tightest sender row with a positive key coefficient (amount > 0): lowering that key by (slack + 1e-6) / coefficient
#        must give 'senderR2 violated'.  (c2) d = 7 (c3) d = 8: an admissible receiver (random + planted arrangements) with an IN
#        coefficient > 0 for a key that touches no 5 / 6 row as payee or as an OUT-free payer (c2: payer {5}, payee {7}; c3: payer
#        {7}, payee B): raising it by (slack + 1e-6) / coefficient overloads that receiver.
if GKKEYS and os.environ.get('GKPLANTFIND') == '1':
    best = None
    for w in SENDERS:
        sixes = [k for k in range(5) if w[k] == 6]
        for hb in itertools.product((0, 1), repeat=5):
            for fb in itertools.product((0, 1), repeat=len(sixes)):
                H_ = dict(zip(range(5), hb)); F_ = dict(zip(sixes, fb)); r = sender_row(w, H_, F_)
                if r is None: continue
                v = sum(cf * val(k) for k, cf in r.items()); sl_ = v - (1 - T)
                for k_, cf_ in r.items():
                    if k_[0] == 'ks' and cf_ > 0 and KSV.get(k_[1], 0.0) > 0:
                        need = (sl_ + 1e-6) / cf_
                        if need < KSV[k_[1]] and (best is None or sl_ < best[0]): best = (sl_, ''.join(map(str, w)), dict(H_), dict(F_), k_[1], cf_, KSV[k_[1]], KSV[k_[1]] - need)
    print('GKPLANT c1 sender: slack %.6g row %s H%s F%s key %s coefficient %d amount %.12g -> lower to %.12g' % best if best else 'GKPLANT c1: none', flush=True)
    _rr = random.Random(77)
    for d, sel in ((7, lambda k_: k_[1] == 1 and k_[2] == 4), (8, lambda k_: k_[1] == 4 and k_[2] & 8)):
        sepx(d, yv, xv, 1e9, 1); cands = [k_ for k_ in GKKEYS if sel(k_)]; best = None
        for q_ in range(4000):
            w_, s_ = _gk_plant(_rr, d, cands[q_ % len(cands)], 'in')
            lk, sv = ''.join(map(str, w_)), ''.join(map(str, s_))
            if not admissible(d, w_, s_) or not check(d, lk, sv): continue
            SEPX.stdin.write('e %d %s %s\n' % (d, lk, sv)); SEPX.stdin.flush(); out_ = SEPX.stdout.readline().strip()
            if out_ == 'inadm': continue
            ld = spec_val(d, lk, sv); sl_ = d - 6 + T - ld
            for k_, cf_ in recv_spec(d, lk, sv).items():
                if k_[0] == 'ks' and cf_ > 0 and k_[1] in [c_[0] for c_ in cands]:
                    newa = KSV.get(k_[1], 0.0) + (sl_ + 1e-6) / cf_
                    if newa < 2.9 and (best is None or newa - KSV.get(k_[1], 0.0) < best[-1] - best[-2]): best = (d, lk, sv, ld, sl_, k_[1], cf_, KSV.get(k_[1], 0.0), newa)
        print('GKPLANT c%d receiver d=%d %s %s load %.12f slack %.6g key %s IN coefficient %s amount %.12g -> raise to %.12g' % ((2 if d == 7 else 3,) + best) if best else 'GKPLANT d=%d: none' % d, flush=True)
    print('VERDICT: GKPLANTFIND done'); sys.exit(0)
