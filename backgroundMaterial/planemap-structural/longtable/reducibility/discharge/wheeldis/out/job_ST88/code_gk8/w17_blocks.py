# W17 test blocks, exec'd by st21_w17.py in its own namespace after the separator tables are built (needs KSKEYS, KSCTX, KF,
# recv_spec, spec_val, sepx, SEPX, yv, xv, KSREL_, MASK, pmask, f2b_extra, admissible, fail). Each block is opt-in by env.
def _ks_plant(rr_, d, key, role):
    """a random arrangement where key fires once as payer (d = 7, role 'pay') or payee (role 'rec') at a random slot"""
    n_, P_, cd_ = key
    w_ = [rr_.choice((5, 5, 6, 6, 7, 7, 7, 8, 9)) for _ in range(d)]; s_ = [rr_.choice((5, 5, 6, 6, 7, 7, 8, 9)) for _ in range(d)]
    pick = lambda m: rr_.choice([l for l in LET if (m >> (l - 5)) & 1])
    j = rr_.randrange(d); e = rr_.choice((1, -1))
    def setab(a, b, v):   # apex between consecutive a, b
        a %= d; b %= d
        if b == (a + 1) % d: s_[a] = v
        else: s_[b] = v
    if role == 'pay':
        w_[j] = pick(P_)
        for pi, m in cd_:
            v = pick(m)
            if pi in (0, 1, 2): w_[(j + (pi + 1) * e) % d] = v
            elif pi in (3, 4, 5): w_[(j - (pi - 2) * e) % d] = v
            elif pi == 6: setab(j + e, j + 2 * e, v)
            elif pi == 7: setab(j - e, j - 2 * e, v)
            elif pi == 8: setab(j, j + e, v)
            elif pi == 10: setab(j, j - e, v)
    else:
        w_[j] = 7
        for pi, m in cd_:
            v = pick(m)
            if pi == 0: w_[(j + e) % d] = v
            elif pi == 3: w_[(j - e) % d] = v
            elif pi == 1: setab(j, j + e, v)
            elif pi == 4: setab(j, j - e, v)
            elif pi == 8: w_[(j + 2 * e) % d] = v
            elif pi == 10: w_[(j - 2 * e) % d] = v
        for pi, m in cd_:   # far vertices after the link letters: a 5 neighbour's far apex
            if pi in (6, 7):
                sg_ = e if pi == 6 else -e; k_ = j + sg_
                if w_[k_ % d] == 5: setab(k_, k_ + sg_, pick(m))
            if pi in (2, 5) and rr_.random() < 0.5:   # a 5 / 6 neighbour so that the l3q mask is read (if that letter is free)
                sg_ = e if pi == 2 else -e
                if w_[(j + sg_) % d] > 6 and not any(q_ == (0 if sg_ == e else 3) for q_, _ in cd_): w_[(j + sg_) % d] = rr_.choice((5, 6))
        w_[j] = 7
    if rr_.random() < 0.5: k_ = rr_.randrange(d); w_ = w_[k_:] + w_[:k_]; s_ = s_[k_:] + s_[:k_]
    if rr_.random() < 0.5: w_ = w_[::-1]; s_ = s_[::-1][1:] + s_[::-1][:1]   # reflection (s_i sits between w_i and w_{i+1})
    return w_, s_
def _ks_random(rr_, d):
    return [rr_.choice((5, 5, 6, 6, 7, 7, 7, 8, 9)) for _ in range(d)], [rr_.choice((5, 5, 6, 6, 7, 7, 8, 9)) for _ in range(d)]
def _ks_gen(rr_, d, n):
    out = []
    for q_ in range(n):
        if q_ % 2 == 0 or not KSKEYS: out.append(_ks_random(rr_, d)); continue
        key = KSKEYS[(q_ // 2) % len(KSKEYS)]; role = 'pay' if (d == 7 and (q_ // 2 // len(KSKEYS)) % 2 == 0) else 'rec'
        out.append(_ks_plant(rr_, d, key, role))
    return out
def _ks_payee_by_j(w_, s_):   # per link 7 j: {name: exact count}
    out = collections.defaultdict(collections.Counter)
    for n_, lst in KF.payee_dirs(KSCTX, KSKEYS, w_, s_).items():
        for j_, e_ in lst: out[j_][n_] += 1
    return out
def _ks_bound_check(arrs):
    """per link 7 and per key: exact payee count <= window bound count; and the amount-weighted sum <= KSREL_"""
    bad = tight = tot = 0
    for d, w_, s_ in arrs:
        U_ = min(d, 9); byj = _ks_payee_by_j(w_, s_)
        for j_ in range(d):
            if w_[j_] != 7: continue
            wm1, sm1, s0, wp1 = w_[(j_ - 1) % d], s_[(j_ - 1) % d], s_[j_], w_[(j_ + 1) % d]
            for k_ in KSKEYS:
                b_ = KF.bound_count(KSCTX, k_, U_, wm1, sm1, s0, wp1); x_ = byj[j_][k_[0]]; tot += 1; tight += b_ == x_
                if x_ > b_: bad += 1; bad <= 5 and print('KS BOUND BELOW EXACT d=%d %s %s j=%d key %s exact %d bound %d' % (d, ''.join(map(str, w_)), ''.join(map(str, s_)), j_, k_[0], x_, b_))
            ex_ = sum(KSV.get(n_, 0.0) * c_ for n_, c_ in byj[j_].items())
            if ex_ > KSREL_[U_ - 7, (wm1 - 5) * 25 + (sm1 - 5) * 5 + 2, (s0 - 5) * 5 + wp1 - 5] + 1e-12: bad += 1
    return bad, tight, tot
# ---------------- KSDUMP: my row values for a list of arrangements (TSV with columns d, link, apex), for the Opus comparison ----
if os.environ.get('KSDUMP'):
    _rows = []
    for _l in open(os.environ['KSDUMP']):
        if not _l.strip() or _l.startswith('#'): continue
        _f = _l.rstrip('\n').split('\t')
        if _f[0] == 'd': _hdr = _f; continue
        _rows.append(_f)
    _ci = {c_: i_ for i_, c_ in enumerate(_hdr)}
    _out = open(os.environ['KSDUMP_OUT'], 'w')
    _nm = [k_[0] for k_ in KSKEYS]
    _out.write('\t'.join(['d', 'link', 'apex'] + ['%s_%s' % (n_, c_) for n_ in _nm for c_ in ('pay_n', 'rec_x', 'rec_win')] + ['ks_total', 'load_py', 'leaf_cpp', 'thr', 'slack', 'admissible']) + '\n')
    _curd = None
    for _f in sorted(_rows, key=lambda f_: int(f_[_ci['d']])):
        d = int(_f[_ci['d']]); lk, sv = _f[_ci['link']], _f[_ci['apex']]; w_ = [int(c_) for c_ in lk]; s_ = [int(c_) for c_ in sv]
        if d != _curd: sepx(d, yv, xv, 1e9, 1); _curd = d
        pc = KF.payer_counts(KSKEYS, w_, s_); qc = KF.payee_counts(KSCTX, KSKEYS, w_, s_)
        qb = collections.Counter()
        for j_ in range(d):
            if w_[j_] == 7:
                for k_ in KSKEYS: qb[k_[0]] += KF.bound_count(KSCTX, k_, min(d, 9), w_[(j_ - 1) % d], s_[(j_ - 1) % d], s_[j_], w_[(j_ + 1) % d])
        kt = sum(KSV.get(n_, 0.0) * (qc[n_] - pc[n_]) for n_ in _nm); ld = spec_val(d, lk, sv)
        SEPX.stdin.write('e %d %s %s\n' % (d, lk, sv)); SEPX.stdin.flush(); ce = SEPX.stdout.readline().strip()
        _out.write('\t'.join([str(d), lk, sv] + ['%d\t%d\t%d' % (pc[n_], qc[n_], qb[n_]) for n_ in _nm] + ['%.12f' % kt, '%.12f' % ld, ce, '%.12f' % (d - 6 + T), '%.12f' % (d - 6 + T - ld), str(bool(admissible(d, w_, s_)))]) + '\n')
    _out.close(); print('KSDUMP written %s (%d rows)' % (os.environ['KSDUMP_OUT'], len(_rows)), flush=True)
    if os.environ.get('KSDUMP_ONLY', '1') == '1': print('VERDICT: KSDUMP done'); sys.exit(0)
# ---------------- W17GRAM: orientation test against W6's grammar.py on recv_pic-style pictures built from this checker's masks ----
if os.environ.get('W17GRAM'):
    sys.path.insert(0, os.environ.get('W17GRAMDIR', '/tmp/swarm-W17/grammar')); import grammar as GR
    def _pic(d, w_, s_):   # certpics.recv_pic with this checker's masks: 6-privates amask & ~extra6 (d <= 9); 7-privates L3T & ~extra7 at d = 7
        priv = []
        for j in range(d):
            pv = [GR.ALL] * (w_[j] - 5)
            if w_[j] == 6 and d <= 9:
                am = pmask(min(d, 9), w_[(j - 2) % d], w_[(j - 1) % d], w_[(j + 1) % d], w_[(j + 2) % d], s_[(j - 2) % d], s_[(j - 1) % d], s_[j], s_[(j + 1) % d])
                pv = [am & ~f2b_extra(d, w_, s_, j, ('w6', d), True)]
            if w_[j] == 7 and d == 7:
                for sg, slot in ((1, 1), (-1, 0)):
                    c_ = w_[(j + sg) % d]; ap_, o_ = (s_[j], s_[(j - 1) % d]) if sg == 1 else (s_[(j - 1) % d], s_[j])
                    if c_ <= 6 and ap_ <= 6:
                        pv[slot] = MASK[(sg, c_, ap_, w_[(j + 2 * sg) % d], w_[(j + 3 * sg) % d], w_[(j + 4 * sg) % d], o_)] & ~f2b_extra(7, w_, s_, j, ('w7', 7, sg), True)
            priv.append(pv)
        return GR.build('R', '%d' % d, d, w_, [GR.BIT[x] for x in s_], priv)
    _rr = random.Random(int(os.environ.get('W17GRAMSEED', '1717'))); _N = int(os.environ['W17GRAM'])
    def _swapA(k_):   # deliberately mis-oriented control: S.A+1 <-> S.A-1 only (or R.L+-2, or S.L+-3, if the key has no S.A)
        n_, P_, cd_ = k_; ps = {p for p, _ in cd_}
        for a, b in ((6, 7), (8, 10), (2, 5)):
            if a in ps or b in ps: return (n_ + 'x', P_, tuple(sorted(({a: b, b: a}.get(p, p), m) for p, m in cd_)))
        return (n_ + 'x', P_, cd_)
    _mir = [KF.mirror_key(k_) for k_ in KSKEYS]; _xk = [_swapA(k_) for k_ in KSKEYS]
    _st = collections.Counter(); _ex = []
    for d in (7, 8):
        arrs = _ks_gen(_rr, d, _N)
        items = []; rid = 0
        for w_, s_ in arrs:
            for sl_ in GR.slots(_pic(d, w_, s_)):
                if sl_[0] == 'EDGE': items.append((rid, sl_))
            rid += 1
        TB = GR.SlotTable(items).G['EDGE']
        for key, mk, xk in zip(KSKEYS, _mir, _xk):
            n_, P_, cd_ = key
            sure, poss = GR.match(TB, GR.BIT[7], P_, dict(cd_))
            gpay = np.bincount(TB['rid'][TB['out'] & sure], minlength=len(arrs)); grec = np.bincount(TB['rid'][~TB['out'] & poss], minlength=len(arrs))
            msure, mposs = GR.match(TB, GR.BIT[7], P_, dict(mk[2]))
            gpaym = np.bincount(TB['rid'][TB['out'] & msure], minlength=len(arrs)); grecm = np.bincount(TB['rid'][~TB['out'] & mposs], minlength=len(arrs))
            for r_, (w_, s_) in enumerate(arrs):
                mp = KF.payer_counts([key], w_, s_)[n_]; mq = KF.payee_counts(KSCTX, [key], w_, s_)[n_]
                mpm = KF.payer_counts([mk], w_, s_)[mk[0]]; mqm = KF.payee_counts(KSCTX, [mk], w_, s_)[mk[0]]
                xp = KF.payer_counts([xk], w_, s_)[xk[0]]; xq = KF.payee_counts(KSCTX, [xk], w_, s_)[xk[0]]
                g_ = (d, n_)
                _st[g_ + ('rows',)] += 1; _st[g_ + ('pay>0',)] += mp > 0; _st[g_ + ('rec>0',)] += mq > 0
                _st[g_ + ('pay mismatch',)] += mp != gpay[r_]; _st[g_ + ('rec below grammar',)] += mq < grec[r_]; _st[g_ + ('rec equal',)] += mq == grec[r_]
                _st[g_ + ('mirror differs',)] += (mpm, mqm) != (mp, mq) or (gpaym[r_], grecm[r_]) != (gpay[r_], grec[r_])
                _st[g_ + ('misoriented differs',)] += (xp, xq) != (gpay[r_], grec[r_])
                if (mp != gpay[r_] or mq < grec[r_]) and len(_ex) < 8: _ex.append((d, n_, ''.join(map(str, w_)), ''.join(map(str, s_)), mp, int(gpay[r_]), mq, int(grec[r_])))
        print('W17GRAM d=%d: %d arrangements (half planted), %d EDGE slots' % (d, len(arrs), len(items)), flush=True)
    for (d, n_) in sorted({(k_[0], k_[1]) for k_ in _st}):
        g_ = (d, n_)
        print('W17GRAM d=%d %s: rows %d, payer>0 %d, payee>0 %d; payer mismatches vs grammar SURE %d; payee below grammar POSSIBLE %d, equal %d; mirror key differs %d; mis-oriented control differs %d' % (
            d, n_, _st[g_ + ('rows',)], _st[g_ + ('pay>0',)], _st[g_ + ('rec>0',)], _st[g_ + ('pay mismatch',)], _st[g_ + ('rec below grammar',)], _st[g_ + ('rec equal',)],
            _st[g_ + ('mirror differs',)], _st[g_ + ('misoriented differs',)]), flush=True)
    for x_ in _ex: print('W17GRAM MISMATCH d=%d %s %s %s: mine payer %d grammar %d, mine payee %d grammar %d' % x_)
    _gb = sum(v_ for k_, v_ in _st.items() if k_[2] in ('pay mismatch', 'rec below grammar', 'mirror differs'))
    _gx = all(_st[(d, k_[0], 'misoriented differs')] > 0 for d in (7, 8) for k_ in KSKEYS if (d == 7 or (k_[1] >> 3) & 1))
    print('VERDICT: W17GRAM %s (payer mismatches + payee below grammar + mirror differences = %d; every mis-oriented control differs: %s)' % ('PASS' if _gb == 0 and _gx else 'FAIL', _gb, _gx), flush=True)
    sys.exit(0)
# ---------------- W17ST: C++ leaf ('e') vs Python rows with the families on, planted arrangements; window-bound check ----------
if KSKEYS and os.environ.get('W17ST', '1') != '0':
    _rr = random.Random(int(os.environ.get('W17SEED', '17'))); _mx = {}; _bad = 0; _nz = collections.Counter(); _arrs = []; _cmp = 0; _inadm = 0
    for d in range(7, int(os.environ.get('W17STD', '12')) + 1):
        sepx(d, yv, xv, 1e9, 1)
        n_ = int(os.environ.get('W17STN', '3000')) if d <= 9 else int(os.environ.get('W17STN2', '500'))
        for w_, s_ in _ks_gen(_rr, d, n_):
            _arrs.append((d, w_, s_)); lk, sv = ''.join(map(str, w_)), ''.join(map(str, s_))
            SEPX.stdin.write('e %d %s %s\n' % (d, lk, sv)); SEPX.stdin.flush(); out_ = SEPX.stdout.readline().strip()
            if out_ == 'inadm': _inadm += 1; continue
            cv_ = float(out_); rs_ = recv_spec(d, lk, sv); pv_ = sum(cf * val(k) for k, cf in rs_.items()); _cmp += 1
            _mx[d] = max(_mx.get(d, 0.0), abs(cv_ - pv_))
            for k_, cf_ in rs_.items():
                if k_[0] == 'ks' and KSV.get(k_[1], 0.0) > 0:
                    pc_ = KF.payer_counts([kk for kk in KSKEYS if kk[0] == k_[1]], w_, s_)[k_[1]]
                    _nz[(d, k_[1], 'payer')] += pc_ > 0; _nz[(d, k_[1], 'payee')] += cf_ + pc_ > 0
            if abs(cv_ - pv_) > 1e-9:
                _bad += 1
                if _bad <= 5: print('W17 SELFTEST MISMATCH d=%d %s %s python %.12f c++ %.12f (ks terms %s)' % (d, lk, sv, pv_, cv_, {k_: cf_ for k_, cf_ in rs_.items() if k_[0] == 'ks'}), flush=True)
    print('W17 self-test (C++ leaf vs Python rows, families on): %d compared, %d window-inadmissible; max |difference| by d %s; mismatches > 1e-9: %d' % (
        _cmp, _inadm, {k_: float('%.3g' % v_) for k_, v_ in sorted(_mx.items())}, _bad), flush=True)
    print('W17 self-test rows with a nonzero term (amount > 0): %s' % ', '.join('d%d %s %s %d' % (k_[0], k_[1], k_[2], v_) for k_, v_ in sorted(_nz.items())), flush=True)
    if _bad: fail('W17 self-test: C++ leaf and Python rows differ')
    _bb, _bt, _btot = _ks_bound_check(_arrs)
    print('W17 window bound check: %d (link 7, key) slots, bound == exact on %d (%.1f%%), exact above bound %d' % (_btot, _bt, 100.0 * _bt / max(_btot, 1), _bb), flush=True)
    if _bb: fail('W17 window bound below the exact payee credit')
    if os.environ.get('W17ST_ONLY') == '1': print('VERDICT: W17 SELFTEST %s' % ('PASS' if not FAIL else 'FAIL: ' + ' | '.join(FAIL))); sys.exit(0)
