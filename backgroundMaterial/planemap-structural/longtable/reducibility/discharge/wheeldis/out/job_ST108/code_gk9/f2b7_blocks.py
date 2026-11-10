# W17 round 5 test blocks (SPEC f2b7: q7m masks on 7-sides), exec'd by st21_w17.py (code_gk7) after gk_blocks.py.
# Needs: q7masks, q7sig, q7cands, qkey, recv_spec, spec_val, MASK, MASK8, F2BR, sepx, SEPX, yv, xv, T, EPS, fail, FAIL.
#   F2B7ST=1      (a) the SPEC section 4 worked example, rule counts, and (b) C++ 'e' leaf vs Python rows on random d = 7, 8 rows and on
#                 rows built from the 7-side rules (F2B7STN rows per kind, default 1500), plus an independent SPEC section 2 matcher read
#                 straight from the rule JSON (not the bit encoding f2b_extra uses). F2B7ST_ONLY=1 exits with its own verdict.
#   F2B7FIND=1    pick an admissible d = 7 row R with a fired 7-side and print K0 (a key f2b7 drops on R, in no other slot of R) and
#                 K1 (a key that survives the 7-side mask) for the planted control (c3).
#   F2B7ROWS=d:link:s[,..]  row-restricted separator search (slot masks fix every letter, then 'r thr'): FAIL if the row is reported
#                 above d - 6 + t + SEPEPS (as the full receiver check would).
import json as _j7
_F7ON = os.environ.get('F2B7ST') == '1' or os.environ.get('F2B7FIND') == '1' or bool(os.environ.get('F2B7ROWS'))
if _F7ON:
    _RJ7 = _j7.load(open(F2BR))
    _R7 = {(d_, sg_): _RJ7['d%d_w7' % d_]['1' if sg_ == 1 else '-1'] for d_ in (7, 8) for sg_ in (1, -1)}
    def _m7(rule, d, w, s, j):   # SPEC section 2, read literally: w[(j+off) % d] in allowed, s[(j+off) % d] == v
        p_, wq_, sq_ = rule
        return all(w[(j + int(o_)) % d] in set(al_) for o_, al_ in wq_) and all(s[(j + int(o_)) % d] == int(v_) for o_, v_ in sq_)
    def _x7(d, w, s, j, sg):
        e_ = 0
        for rl_ in _R7[(d, sg)]:
            if _m7(rl_, d, w, s, j): e_ |= 1 << (int(rl_[0]) - 5)
        return e_
    def _side(d, w, s, j, sg):   # SPEC section 1 table: c, ap, o of side sg
        return w[(j + sg) % d], (s[j % d] if sg == 1 else s[(j - 1) % d]), (s[(j - 1) % d] if sg == 1 else s[j % d])
    def _mask_spec(d, w, s, j, sg, f2b7):   # SPEC section 1: m_sg
        c_, ap_, o_ = _side(d, w, s, j, sg)
        if c_ <= 6 and ap_ <= 6:
            T_ = MASK if d == 7 else MASK8
            return T_[(sg, c_, ap_, w[(j + 2 * sg) % d], w[(j + 3 * sg) % d], w[(j + 4 * sg) % d], o_)] & ~_x7(d, w, s, j, sg) & 31
        return (31 & ~_x7(d, w, s, j, sg)) if f2b7 else 31
    def _cap7(rl_, d, sg):   # (c requirement, apex requirement) of a rule on side sg, None if absent; offsets 1..d, d = 0
        co_ = 1 if sg == 1 else d - 1; ao_ = 0 if sg == 1 else d - 1
        cr_ = [set(al_) for o_, al_ in rl_[1] if int(o_) % d == co_]; ar_ = [int(v_) for o_, v_ in rl_[2] if int(o_) % d == ao_]
        return (cr_[0] if cr_ else None), (ar_[0] if ar_ else None)
    def _can7(rl_, d, sg):   # the rule can fire on a 7-side (c >= 7 or apex >= 7 possible)
        cr_, ar_ = _cap7(rl_, d, sg)
        return not ((cr_ is not None and max(cr_) <= 6) and (ar_ is not None and ar_ <= 6))
    def _req7(rl_, d, sg):   # the rule requires c >= 7 or apex >= 7
        cr_, ar_ = _cap7(rl_, d, sg)
        return (cr_ is not None and min(cr_) >= 7) or (ar_ is not None and ar_ >= 7)
    def _f7val(d, lk, sv, on):   # Python row value with F2B7 on / off (module flag switched for the call)
        global F2B7
        k_ = F2B7; F2B7 = on
        try: return spec_val(d, lk, sv)
        finally: F2B7 = k_

if os.environ.get('F2B7ST') == '1':
    _F7FAIL = []
    # ---- (a) SPEC section 4 worked example ----
    _w = [int(ch) for ch in '7576655']; _s = [int(ch) for ch in '7767657']
    _mon = q7masks(7, _w, _s, 0, True); _moff = q7masks(7, _w, _s, 0, False)
    _rule = [5, [[1, [5]], [4, [6]], [5, [5]], [6, [5]]], [[4, 6], [5, 5], [6, 7]]]
    def _norm(rl_): return (int(rl_[0]), tuple(sorted((int(o_) % 7, tuple(sorted(al_))) for o_, al_ in rl_[1])), tuple(sorted((int(o_) % 7, int(v_)) for o_, v_ in rl_[2])))
    _inm = _norm(_rule) in {_norm(rl_) for rl_ in _R7[(7, -1)]}
    _hitp = [rl_ for rl_ in _R7[(7, 1)] if _m7(rl_, 7, _w, _s, 0)]; _hitm = [rl_ for rl_ in _R7[(7, -1)] if _m7(rl_, 7, _w, _s, 0)]
    _sig = q7sig(7, _w[1], _s[0], _s[6], _w[6], _mon[0], _mon[1]); _sig0 = q7sig(7, _w[1], _s[0], _s[6], _w[6], 31, 31)
    _drop = sorted(set(q7cands(_sig0)) - set(q7cands(_sig)))
    _rs = recv_spec(7, '7576655', '7767657')
    print('F2B7 (a) SPEC example 7576655 / 7767657 j=0: masks F2B7=1 %s, F2B7=0 %s; side +1 c,ap = %s, matching rules %d; side -1 c,ap = %s, '
          'matching rules %d %s; SPEC rule in d7_w7 "-1": %s and matches: %s; q7sig %s (unmasked %s); dropped keys %s; 7575675 kept %s; '
          'row Q7 terms %s' % (_mon, _moff, _side(7, _w, _s, 0, 1)[:2], len(_hitp), _side(7, _w, _s, 0, -1)[:2], len(_hitm), _hitm[:3], _inm,
          _m7(_rule, 7, _w, _s, 0), _sig, _sig0, [''.join(map(str, k_)) for k_ in _drop], (7, 5, 7, 5, 6, 7, 5) in q7cands(_sig) or qkey((7, 5, 7, 5, 6, 7, 5)) in q7cands(_sig),
          sorted(k_[1] for k_ in _rs if k_[0] == 'Q7')), flush=True)
    _ok_a = (_mon == (31, 30) and _moff == (31, 31) and not _hitp and _inm and _m7(_rule, 7, _w, _s, 0) and _sig == (7, 5, 7, 7, 5, 30, 31)
             and _drop == [(7, 5, 7, 5, 5, 7, 5)] and qkey((7, 5, 7, 5, 6, 7, 5)) in q7cands(_sig) and ('Q7', (7, 5, 7, 7, 5, 30, 31)) in _rs) if F2B7 else None
    if F2B7 and not _ok_a: _F7FAIL.append('(a) SPEC worked example differs')
    print('F2B7 (a) %s' % ({True: 'PASS', False: 'FAIL', None: 'not checked (F2B7=0)'}[_ok_a]), flush=True)
    _cnt = {'d%d_w7 %+d' % k_: (len(v_), sum(1 for rl_ in v_ if _req7(rl_, k_[0], k_[1])), sum(1 for rl_ in v_ if _can7(rl_, k_[0], k_[1]))) for k_, v_ in sorted(_R7.items())}
    print('F2B7 rules per side (total, requiring c >= 7 or apex >= 7, able to fire on a 7-side): %s; SPEC: 346 (d7_w7), 135 (d8_w7) per side' % _cnt, flush=True)
    # ---- (b) C++ leaf vs Python rows ----
    _r7 = random.Random(int(os.environ.get('F2B7SEED', '57'))); _N7 = int(os.environ.get('F2B7STN', '1500'))
    _CAN = {k_: [rl_ for rl_ in v_ if _can7(rl_, k_[0], k_[1])] for k_, v_ in _R7.items()}
    def _rowrule(d):   # a row where a random 7-side-capable rule of a random side holds at a random link 7, the side made a 7-side
        for _try in range(50):
            sg = _r7.choice((1, -1)); rl_ = _r7.choice(_CAN[(d, sg)])
            w_ = [_r7.choice((5, 5, 6, 6, 7, 7, 8, 9)) for _ in range(d)]; s_ = [_r7.choice((5, 5, 6, 6, 7, 7, 8, 9)) for _ in range(d)]; j = _r7.randrange(d)
            fw = {}; fs = {}
            for o_, al_ in rl_[1]: fw[(j + int(o_)) % d] = list(al_)
            for o_, v_ in rl_[2]: fs[(j + int(o_)) % d] = int(v_)
            if j in fw and 7 not in fw[j]: continue
            for p_, al_ in fw.items(): w_[p_] = _r7.choice(al_)
            for p_, v_ in fs.items(): s_[p_] = v_
            w_[j] = 7
            cpos = (j + sg) % d; apos = j % d if sg == 1 else (j - 1) % d
            if w_[cpos] <= 6 and s_[apos] <= 6:
                opts = ([('w', cpos)] if cpos not in fw or max(fw[cpos]) >= 7 else []) + ([('s', apos)] if apos not in fs else [])
                if not opts: continue
                kd, p_ = _r7.choice(opts)
                if kd == 'w': w_[p_] = _r7.choice([l_ for l_ in fw.get(p_, (7, 8, 9)) if l_ >= 7])
                else: s_[p_] = _r7.choice((7, 8, 9))
            if not _m7(rl_, d, w_, s_, j): continue
            if _r7.random() < 0.5: w_ = w_[::-1]; s_ = s_[::-1][1:] + s_[::-1][:1]   # reflect (apex s_i between w_i and w_{i+1})
            return ''.join(map(str, w_)), ''.join(map(str, s_))
        return None
    _st7 = collections.Counter(); _mx7 = collections.defaultdict(float); _bad7 = 0; _pyd = 0; _sens = collections.Counter()
    for d in (7, 8):
        sepx(d, yv, xv, 1e9, 1)
        for kind in ('random', 'rule'):
            for n_ in range(_N7):
                if kind == 'random':
                    lk = ''.join(str(_r7.choice(LET)) for _ in range(d)); sv = ''.join(str(_r7.choice(LET)) for _ in range(d))
                    if '7' not in lk: lk = '7' + lk[1:]
                else:
                    rr_ = _rowrule(d)
                    if rr_ is None: _st7['rule rows not built d%d' % d] += 1; continue
                    lk, sv = rr_
                w_ = [int(ch) for ch in lk]; s_ = [int(ch) for ch in sv]
                fired = 0
                for j in range(d):
                    if w_[j] != 7: continue
                    mq = q7masks(d, w_, s_, j, True); ms_ = (_mask_spec(d, w_, s_, j, 1, True), _mask_spec(d, w_, s_, j, -1, True))
                    if mq != ms_:
                        _pyd += 1
                        if _pyd <= 5: print('F2B7 PYTHON MASK MISMATCH d=%d %s %s j=%d q7masks %s spec %s' % (d, lk, sv, j, mq, ms_), flush=True)
                    for sg, m_ in zip((1, -1), mq):
                        c_, ap_, _o = _side(d, w_, s_, j, sg)
                        if (c_ >= 7 or ap_ >= 7) and m_ != 31: fired += 1
                SEPX.stdin.write('e %d %s %s\n' % (d, lk, sv)); SEPX.stdin.flush(); out_ = SEPX.stdout.readline().strip()
                if out_ == 'inadm': _st7['window-inadmissible d%d %s' % (d, kind)] += 1; continue
                cv_ = float(out_); pv_ = spec_val(d, lk, sv); _st7['compared d%d %s' % (d, kind)] += 1; _mx7[d] = max(_mx7[d], abs(cv_ - pv_))
                if fired: _st7['with a fired 7-side d%d %s' % (d, kind)] += 1
                if fired and abs(pv_ - _f7val(d, lk, sv, False)) > 1e-12: _sens['value changed by f2b7 d%d %s' % (d, kind)] += 1
                if abs(cv_ - pv_) > 1e-9:
                    _bad7 += 1
                    if _bad7 <= 5: print('F2B7 SELFTEST MISMATCH d=%d %s %s python %.12f c++ %.12f (python F2B7=0 value %.12f)' % (d, lk, sv, pv_, cv_, _f7val(d, lk, sv, False)), flush=True)
    print('F2B7 (b) self-test (C++ exact leaf vs Python rows, F2B7=%d%s%s): %s; %s; max |difference| by d %s; mismatches > 1e-9: %d; Python q7masks vs the SPEC '
          'matcher on the JSON: %d differences' % (F2B7, ', W17PLANT_SEP7=off' if os.environ.get('W17PLANT_SEP7') == 'off' else '', (', W17PLANT7=' + W17PLANT7) if W17PLANT7 else '',
          dict(sorted(_st7.items())), dict(sorted(_sens.items())), {k: float('%.3g' % v) for k, v in _mx7.items()}, _bad7, _pyd), flush=True)
    if _bad7: _F7FAIL.append('(b) C++ leaf and Python rows differ on %d rows' % _bad7)
    if _pyd: _F7FAIL.append('(b) Python q7masks differ from the SPEC matcher on %d link 7s' % _pyd)
    for m_ in _F7FAIL: fail('F2B7 self-test: ' + m_)
    print('F2B7 SELFTEST %s' % ('PASS' if not _F7FAIL else 'FAIL: ' + ' | '.join(_F7FAIL)), flush=True)
    if os.environ.get('F2B7ST_ONLY') == '1': print('VERDICT: F2B7 SELFTEST %s (all FAIL lines of the run: %s)' % ('PASS' if not _F7FAIL else 'FAIL', ' | '.join(FAIL) or 'none')); sys.exit(0)

if os.environ.get('F2B7FIND') == '1':   # (c3) candidates: admissible d = 7 rows with a fired 7-side
    _r7 = random.Random(int(os.environ.get('F2B7SEED', '57')) + 1); _found = 0; sepx(7, yv, xv, 1e9, 1)
    _thr7 = 7 - 6 + T + float(os.environ.get('SEPEPS', str(EPS)))
    for n_ in range(int(os.environ.get('F2B7FINDN', '200000'))):
        rr_ = _rowrule(7) if os.environ.get('F2B7ST') == '1' else None
        if rr_ is None: break
        lk, sv = rr_; w_ = [int(ch) for ch in lk]; s_ = [int(ch) for ch in sv]
        SEPX.stdin.write('c 7 %s %s\n' % (lk, sv)); SEPX.stdin.flush()
        if SEPX.stdout.readline().strip() != '1': continue
        slots = [j for j in range(7) if w_[j] == 7]
        for j in slots:
            m1, m2 = q7masks(7, w_, s_, j, True)
            if (m1, m2) == (31, 31): continue
            sg = q7sig(7, w_[(j + 1) % 7], s_[j], s_[(j - 1) % 7], w_[(j - 1) % 7], m1, m2); sg0 = sg[:5] + (31, 31)
            other = set()
            for j2 in slots:   # every unmasked candidate of the other link 7s and every payer key of R
                if j2 != j: other |= set(q7cands(q7sig(7, w_[(j2 + 1) % 7], s_[j2], s_[(j2 - 1) % 7], w_[(j2 - 1) % 7], 31, 31)))
                other.add(qkey(tuple(w_[(j2 + m) % 7] for m in range(7))))
            k0 = [k_ for k_ in sorted(set(q7cands(sg0)) - set(q7cands(sg))) if k_ not in other]
            k1 = [k_ for k_ in q7cands(sg) if k_ not in other]
            if k0 and k1:
                _found += 1
                print('F2B7FIND row %s %s j=%d masks %s sig %s value F2B7=1 %.9f F2B7=0 %.9f (bound %.9f); K0 (dropped, only here) %s; K1 (kept, only here) %s' % (
                    lk, sv, j, (m1, m2), sg, _f7val(7, lk, sv, True), _f7val(7, lk, sv, False), _thr7, [''.join(map(str, k_)) for k_ in k0[:4]], [''.join(map(str, k_)) for k_ in k1[:4]]), flush=True)
                break
        if _found >= int(os.environ.get('F2B7FINDK', '3')): break
    print('F2B7FIND: %d candidate rows' % _found, flush=True)

if os.environ.get('F2B7ROWS'):   # (c3) row-restricted separator search
    for _it in os.environ['F2B7ROWS'].split(','):
        d_, lk, sv = _it.split(':'); d_ = int(d_)
        _thr = d_ - 6 + T + float(os.environ.get('SEPEPS', str(EPS)))
        sepx(d_, yv, xv, 1e9, 1)
        SEPX.stdin.write('M %d %s\n' % (2 * d_, ' '.join(str(1 << (int(ch) - 5)) for ch in lk + sv))); SEPX.stdin.write('r %.12f 20\n' % _thr); SEPX.stdin.flush()
        rep = []
        while True:
            l_ = SEPX.stdout.readline().strip()
            if l_.startswith('END'): break
            if l_.startswith('A '): f_ = l_.split(); rep.append((float(f_[1]), f_[2], f_[3]))
        SEPX.stdin.write('M 0\n'); SEPX.stdin.flush()
        pv_ = spec_val(d_, lk, sv)
        print('F2B7ROWS d=%d %s %s (F2B7=%d): Python row value %.9f, bound %.9f; separator search restricted to this arrangement reported %s [%s]' % (
            d_, lk, sv, F2B7, pv_, _thr, rep, l_), flush=True)
        if rep: fail('F2B7ROWS: receiver d=%d %s %s reported above the bound (load %.9f)' % (d_, lk, sv, rep[0][0]))
        elif pv_ > _thr: fail('F2B7ROWS: Python row above the bound but the separator search did not report it')
    if os.environ.get('F2B7ROWS_ONLY') == '1' or os.environ.get('W17QPLANT'):   # a planted control needs nothing after this
        print('VERDICT: F2B7ROWS %s (all FAIL lines: %s)' % ('PASS' if not FAIL else 'FAIL', ' | '.join(FAIL) or 'none')); sys.exit(0)

# ---- GK8EX=N (round 5, coordinator: the 140-key file has payee 8 / 9 keys): at d = 8..10 the row's IN credit is the gkwin window count
# of each link position; check per key that it is >= the count on the row's exact picture (apexes exact, link 6 private = pmask of its
# own window, 7+ privates free), on N random + N planted rows per d (planted = an IN slot of a key whose payee set holds min(d, 9)). ----
if GKKEYS and os.environ.get('GK8EX'):
    _r8 = random.Random(int(os.environ.get('GK8SEED', '808'))); _N8 = int(os.environ['GK8EX']); _st8 = collections.Counter(); _bad8 = 0
    for d in (8, 9, 10):
        U_ = min(d, 9); _kd = [k_ for k_ in GKKEYS if (k_[2] >> (U_ - 5)) & 1]
        for n_ in range(2 * _N8):
            if n_ % 2 == 0: w_ = [_r8.choice((5, 5, 5, 6, 6, 7, 7, 8, 9)) for _ in range(d)]; s_ = [_r8.choice((5, 5, 6, 6, 7, 7, 8, 9)) for _ in range(d)]
            else: w_, s_ = _gk_plant(_r8, d, _r8.choice(_kd), 'in')
            W_ = lambda k: w_[k % d]; S_ = lambda k: s_[k % d]
            P6 = {k: pmask(U_, W_(k - 2), W_(k - 1), W_(k + 1), W_(k + 2), S_(k - 2), S_(k - 1), S_(k), S_(k + 1)) & 31 for k in range(d) if w_[k] == 6}
            P_ = GKF.Pic(d, GKF.bit(U_), w_, [GKF.bit(x) for x in s_], P6)
            _o, ex_ = GKENG.pic_counts(P_, out_on=False)
            wn_ = collections.Counter()
            for j_ in range(d):
                for q in GKWIN.counts(U_, *_gk_win_of(d, w_, s_, j_)): wn_[GKENG.names[q]] += 1
            for nm_ in set(ex_) | set(wn_):
                k_ = GKKEYS[GKENG.names.index(nm_)]; tg_ = 'payee %s' % GKF.msym(k_[2])
                if ex_[nm_] > 0: _st8['d%d exact>0 %s' % (d, tg_)] += 1
                if wn_[nm_] > ex_[nm_]: _st8['d%d window>exact %s' % (d, tg_)] += 1
                if ex_[nm_] > wn_[nm_]:
                    _bad8 += 1
                    if _bad8 <= 5: print('GK8EX WINDOW BELOW EXACT d=%d %s %s key %s exact %d window %d' % (d, ''.join(map(str, w_)), ''.join(map(str, s_)), nm_, ex_[nm_], wn_[nm_]), flush=True)
    print('GK8EX (d = 8..10, %d random + %d planted rows per d): window count below the exact-picture count for %d (row, key) pairs; %s' % (_N8, _N8, _bad8,
          ', '.join('%s %d' % kv for kv in sorted(_st8.items()) if ('8' in kv[0].split('payee ')[1] or '9' in kv[0].split('payee ')[1] or 'B' in kv[0].split('payee ')[1]))), flush=True)
    if _bad8: fail('GK8EX: d >= 8 window credit below the exact picture count')
    if os.environ.get('GK8EX_ONLY') == '1': print('VERDICT: GK8EX %s (all FAIL lines: %s)' % ('PASS' if not _bad8 else 'FAIL', ' | '.join(FAIL) or 'none')); sys.exit(0)
