# code_gk9 test blocks (HATBB keys, HATBB_SPEC a36ce8d2), exec'd twice by st21_w17.py:
#   _HBSTAGE = 'vec' (right after f2b_extra is defined; needs pmask, MASK, MASK8, _ksx, hb_pic):
#       HBVEC=<json>[,<json>...]: W6b's per-row coefficient files (hbrows16x_*.json: keys -> rule, colsum, rows [[label, weight, coef]]);
#       every row label 'R<d> <link>/<apex>' that appears is recomputed for every column with this checker's rows (hb_pic + hbfam.row_counts,
#       HBPLANT applied) and compared per (row, column); also the column sums over the listed rows. HBVECKEYS=<key file> (default: the
#       HAT lines of GK). Prints a VERDICT and exits.
#   _HBSTAGE = 'st' (after gk_blocks.py; the separator is running): HBST (default on with HATBB keys): per-edge bound (exact edge term
#       <= HBREL) and C++ exact leaf ('e') vs Python rows on random + planted arrangements, d = 7..HBSTD (12) and HBSTDX (18, 26).
if _HBSTAGE == 'vec' and os.environ.get('HBVEC'):
    _vk = HBF.load_keys(os.environ['HBVECKEYS']) if os.environ.get('HBVECKEYS') else HBKEYS
    if not _vk: fail('HBVEC: no HAT keys (GK or HBVECKEYS)')
    _vkn = [k_[0] for k_ in _vk]; _tot = collections.Counter(); _vex = []
    print('HBVEC: %d HAT keys %s; plant %r; 6-private reading d <= %d' % (len(_vk), _vkn, HBPLANT, HBF.P6DMAX), flush=True)
    for _fn in os.environ['HBVEC'].split(','):
        _J = json.load(open(_fn)); _ref = collections.defaultdict(dict); _wt = {}
        _cols = sorted(_J['keys'])
        if sorted(_cols) != sorted(_vkn): fail('HBVEC %s: columns %s differ from the keys %s' % (_fn, _cols, _vkn))
        for _n, _K in _J['keys'].items():
            if HBF.key_str(HBF.parse_key(_n + ' ' + _K['rule'])) != HBF.key_str([k_ for k_ in _vk if k_[0] == _n][0]): fail('HBVEC %s: rule of %s differs from the key file' % (_fn, _n))
            if len(_K['rows']) != _K['nnz']: fail('HBVEC %s: %s nnz %d but %d rows' % (_fn, _n, _K['nnz'], len(_K['rows'])))
            for _lab, _w, _c in _K['rows']:
                _ref[_lab][_n] = _c
                if _lab in _wt and abs(_wt[_lab] - _w) > 1e-15: fail('HBVEC: row %s has two weights' % _lab)
                _wt[_lab] = _w
        _st = collections.Counter(); _rowbad = set(); _colbad = collections.Counter(); _bydeg = collections.Counter(); _cs = collections.defaultdict(float)
        for _lab in sorted(_ref):
            _R, _ws = _lab.split(); _d = int(_R[1:]); _lw, _sw = _ws.split('/')
            _w = [int(c_) for c_ in _lw]; _s = [int(c_) for c_ in _sw]
            if not (len(_w) == len(_s) == _d): fail('HBVEC: bad row label %s' % _lab); continue
            _rc = HBF.row_counts(_vk, hb_pic(_d, _w, _s), HBPLANT); _bydeg[_d] += 1; _st['rows'] += 1
            for _n in _vkn:
                _m, _r = _rc.get(_n, 0), _ref[_lab].get(_n, 0)
                _st['pairs'] += 1; _st['nonzero ref'] += _r != 0; _st['nonzero mine'] += _m != 0; _cs[_n] += _wt[_lab] * _m
                if _m != _r:
                    _st['mismatch'] += 1; _rowbad.add(_lab); _colbad[_n] += 1
                    if len(_vex) < 12: _vex.append((os.path.basename(_fn), _lab, _n, _J['keys'][_n]['rule'], _m, _r))
        _csd = max(abs(_cs[_n] - _J['keys'][_n]['colsum']) for _n in _vkn)
        print('HBVEC %s (coefj_rows %s, dual %s): rows %d (by d %s), columns %d, (row, column) pairs %d, nonzero coefficients: reference %d, mine %d; '
              'mismatches %d (rows %d, columns %d: %s); column sums over the listed rows vs the file: max |diff| %.3g' % (
              os.path.basename(_fn), _J.get('coefj_rows'), os.path.basename(_J.get('dualf', '')), _st['rows'], dict(sorted(_bydeg.items())), len(_vkn), _st['pairs'],
              _st['nonzero ref'], _st['nonzero mine'], _st['mismatch'], len(_rowbad), len(_colbad), dict(sorted(_colbad.items())), _csd), flush=True)
        _tot.update(_st); _tot['rowbad'] += len(_rowbad); _tot['colbad'] += len(_colbad)
        if _csd > 1e-9 and not _st['mismatch']: fail('HBVEC %s: column sums differ' % _fn)
    for _x in _vex: print('HBVEC MISMATCH %s row %s key %s %s: mine %d reference %d' % _x, flush=True)
    print('HBVEC total: rows %d, pairs %d, nonzero reference %d, mismatches %d (rows %d, columns %d)' % (_tot['rows'], _tot['pairs'], _tot['nonzero ref'], _tot['mismatch'], _tot['rowbad'], _tot['colbad']), flush=True)
    if _tot['mismatch']: fail('HBVEC: %d coefficient mismatches' % _tot['mismatch'])
    print('VERDICT: HBVEC %s' % ('PASS' if not FAIL else 'FAIL: ' + ' | '.join(FAIL))); sys.exit(0)

def _hb_plant(rr_, d, key, role):
    """a random degree-d arrangement with key's OUT slot (role 'out': the centre pays the apex s_i) or IN slot (role 'in': s_i pays
    the centre) set up on a random edge and orientation from the key's own sets (privates are not forced; other letters random)"""
    n_, U_, V_, cd_ = key
    w_ = [rr_.choice((5, 5, 6, 6, 7, 7, 8, 9)) for _ in range(d)]; s_ = [rr_.choice((5, 6, 7, 7, 8, 9)) for _ in range(d)]
    i = rr_.randrange(d); o = rr_.choice((1, -1)); a = i if o == 1 else i + 1; b = a + o
    def setA(p, q, v):
        p %= d; q %= d
        if q == (p + 1) % d: s_[p] = v
        else: s_[q] = v
    def setW(k, v): w_[k % d] = v
    cdd = dict(cd_); pk = lambda p_: _gk_pick(rr_, cdd[p_])
    if 0 in cdd: setW(a, pk(0))
    if 1 in cdd: setW(b, pk(1))
    if role == 'out':
        sb = _gk_pick(rr_, V_)
        for p_, (kind, x, y) in {2: ('w', a - o, 0), 3: ('w', b + o, 0), 4: ('a', a, a - o), 5: ('a', b, b + o), 8: ('w', b + 2 * o, 0), 9: ('w', b + 3 * o, 0),
                                  10: ('w', a - 2 * o, 0), 11: ('w', a - 3 * o, 0), 12: ('a', b + o, b + 2 * o), 13: ('a', b + 2 * o, b + 3 * o),
                                  14: ('a', a - o, a - 2 * o), 15: ('a', a - 2 * o, a - 3 * o)}.items():
            if p_ in cdd: (setW(x, pk(p_)) if kind == 'w' else setA(x, y, pk(p_)))
        if 6 in cdd and w_[a % d] == 5: setA(a, a - o, _gk_pick(rr_, cdd[6] & cdd.get(4, 31) or cdd[6]))
        if 7 in cdd and w_[b % d] == 5: setA(b, b + o, _gk_pick(rr_, cdd[7] & cdd.get(5, 31) or cdd[7]))
    else:
        sb = _gk_pick(rr_, U_)
        if 6 in cdd: setW(a - o, pk(6))
        if 7 in cdd: setW(b + o, pk(7))
        for p_, x, f in ((2, a, o), (3, b, -o)):   # U-1 / U+1: a 5's other apex
            if p_ in cdd and w_[x % d] == 5: setA(x, x - f, pk(p_))
        for p_, x, f in ((4, a, o), (5, b, -o)):   # XA / YA: a 5's far link, a 6's other apex
            if p_ in cdd and w_[x % d] == 5: setW(x - f, pk(p_))
            elif p_ in cdd and w_[x % d] == 6: setA(x, x - f, pk(p_))
    s_[i % d] = sb
    if rr_.random() < 0.5: k_ = rr_.randrange(d); w_ = w_[k_:] + w_[:k_]; s_ = s_[k_:] + s_[:k_]
    if rr_.random() < 0.5: w_ = w_[::-1]; s_ = s_[::-1][1:] + s_[::-1][:1]
    return w_, s_
def _hb_gen(rr_, d, n, keys):
    out = []; U_ = min(d, 9)
    for q_ in range(n):
        if q_ % 4 == 0 or not keys:
            out.append(([rr_.choice((5, 5, 6, 6, 7, 7, 8, 9)) for _ in range(d)], [rr_.choice((5, 6, 7, 7, 8, 9)) for _ in range(d)])); continue
        cand = [(k_, r_) for k_ in keys for r_ in ('out', 'in') if (k_[1] if r_ == 'out' else k_[2]) & HBF.bit(U_)]
        if not cand: out.append(([rr_.choice((5, 6, 7, 8, 9)) for _ in range(d)], [rr_.choice((5, 6, 7, 8, 9)) for _ in range(d)])); continue
        k_, r_ = cand[(q_ // 4 + q_) % len(cand)]
        out.append(_hb_plant(rr_, d, k_, r_))
    return out
if _HBSTAGE == 'st' and HBKEYS and os.environ.get('HBST', '1') != '0':
    _rr = random.Random(int(os.environ.get('HBSEED', '9009'))); _amh = {k_[0]: KSV.get(k_[0], 0.0) for k_ in HBKEYS}
    _nzh = [k_ for k_ in HBKEYS if _amh[k_[0]] > 0]
    if not _nzh: print('W17 HATBB self-test: no HATBB key has a nonzero amount (every HATBB term is 0); the C++ / Python comparison below still runs', flush=True)
    _mx = {}; _bad = 0; _cmp = 0; _inadm = 0; _nz = collections.Counter(); _pb = 0; _ptot = 0; _ptight = 0; _pnz = 0
    _dl = list(range(7, int(os.environ.get('HBSTD', '12')) + 1)) + [int(x_) for x_ in os.environ.get('HBSTDX', '18,26').split(',') if x_]
    for d in _dl:
        sepx(d, yv, xv, 1e9, 1)
        n_ = int(os.environ.get('HBSTN', '3000')) if d <= 9 else int(os.environ.get('HBSTN2', '600'))
        ui_ = min(d, 9) - 7
        for w_, s_ in _hb_gen(_rr, d, n_, _nzh):
            lk, sv = ''.join(map(str, w_)), ''.join(map(str, s_))
            P_ = hb_pic(d, w_, s_); rc_ = HBF.row_counts(HBKEYS, P_, HBPLANT)
            hb_ = {n_: c_ for n_, c_ in rc_.items() if c_ and _amh[n_] > 0}
            _nz[(d, 'hb terms')] += bool(hb_); _nz[(d, 'hb coef<0')] += any(v_ < 0 for v_ in hb_.values()); _nz[(d, 'hb coef>0')] += any(v_ > 0 for v_ in hb_.values())
            for i_ in range(d):   # per-edge bound: exact amount-weighted edge term <= HBREL
                o_, in_ = HBF.edge_counts(HBKEYS, P_, i_, HBPLANT)
                ex_ = sum(_amh[n_] * c_ for n_, c_ in in_.items()) - sum(_amh[n_] * c_ for n_, c_ in o_.items())
                rel_ = HBREL_[ui_, (w_[(i_ - 1) % d] - 5) * 25 + (s_[(i_ - 1) % d] - 5) * 5 + w_[i_] - 5, (s_[i_] - 5) * 5 + w_[(i_ + 1) % d] - 5]
                _ptot += 1; _ptight += abs(ex_ - rel_) < 1e-15; _pnz += abs(ex_) > 0
                if ex_ > rel_ + 1e-12: _pb += 1; _pb <= 5 and print('HB BOUND BELOW EXACT d=%d %s %s i=%d exact %.12g bound %.12g' % (d, lk, sv, i_, ex_, rel_))
            rs_ = recv_spec(d, lk, sv)
            if any(rs_.get(('ks', n_), 0) != rc_.get(n_, 0) for n_ in _amh): fail('HBST: recv_spec HATBB terms differ from hbfam.row_counts')
            SEPX.stdin.write('e %d %s %s\n' % (d, lk, sv)); SEPX.stdin.flush(); out_ = SEPX.stdout.readline().strip()
            if out_ == 'inadm': _inadm += 1; continue
            cv_ = float(out_); pv_ = sum(cf * val(k) for k, cf in rs_.items()); _cmp += 1
            _mx[d] = max(_mx.get(d, 0.0), abs(cv_ - pv_)); _nz[(d, 'compared with hb')] += bool(hb_)
            if abs(cv_ - pv_) > 1e-9:
                _bad += 1
                if _bad <= 5: print('HB SELFTEST MISMATCH d=%d %s %s python %.12f c++ %.12f (hb terms %s)' % (d, lk, sv, pv_, cv_, hb_), flush=True)
    print('W17 HATBB self-test (C++ leaf vs Python rows, all families on, %d HATBB keys with amount > 0): %d compared, %d window-inadmissible; max |difference| by d %s; mismatches > 1e-9: %d' % (
        len(_nzh), _cmp, _inadm, {k_: float('%.3g' % v_) for k_, v_ in sorted(_mx.items())}, _bad), flush=True)
    print('W17 HATBB self-test rows with a nonzero HATBB term (amount > 0): %s' % ', '.join('d%d %s %d' % (k_[0], k_[1], v_) for k_, v_ in sorted(_nz.items())), flush=True)
    print('W17 HATBB per-edge bound check: %d edges (%d with a nonzero exact term), bound == exact on %d, exact above bound %d' % (_ptot, _pnz, _ptight, _pb), flush=True)
    if _bad: fail('W17 HATBB self-test: C++ leaf and Python rows differ')
    if _pb: fail('W17 HATBB edge bound below the exact edge term')
if _HBSTAGE == 'st' and HBKEYS and (os.environ.get('GKST_ONLY') == '1' or os.environ.get('HBST_ONLY') == '1'):
    print('VERDICT: W17 GK+HATBB SELFTEST %s' % ('PASS' if not FAIL else 'FAIL: ' + ' | '.join(FAIL))); sys.exit(0)
