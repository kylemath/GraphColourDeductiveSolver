import random
# f2bglue.py (s60_f2b): outside team's full-wheel 2-ball private-letter exclusions in the Opus R6x2 engine.  exec'd by pcheck.py after prelay2.py.
# Option f2b=RULES.json switches it on (flag f2boff = load the plumbing with an empty rule set, for validation).  Without f2b nothing changes.
# Semantics (ext_f2b/f2b.py, read from the outside team's make_recv_spec_full2ball): a firing rule removes letter p_deg from
#   (w6)  the allowed-private mask am of a 6 spoke (d = 7, 8, 9): M row key ('M', sig + (am,)) -> ('M', sig + (am & ~bit,));
#   (w7)  the l3q mask m of a link-7 side (d = 7 V=7 table, d = 8 V=8 table; c = w_{i+sg} and apex in {5,6}): ('lQ', (c, ap, m)) -> (c, ap, m & ~bit).
# Masking only removes options, so every window upper bound of the DFS stays valid; the exact value is corrected at the leaf (jsepf).
F2B_ON = 'f2b' in OPT
F2B_MV2 = [None]; F2B_EVAL = [None]; F2B_STAT = collections.Counter()
BINF = os.path.join(HERE, 'bin', 'jsepf')
if F2B_ON:
    import importlib.util as _ilu
    _sp = _ilu.spec_from_file_location('f2bmod', os.path.join(HERE, 'f2b.py')); f2bm = _ilu.module_from_spec(_sp); _sp.loader.exec_module(f2bm)
    _st = f2bm.load(OPT['f2b'], off='f2boff' in FLAGS)
    assert F16 and AC and AP and not XO and not FY and not V6 and not W19 and not PCAM and 'ref' not in FLAGS, 'f2b: unsupported flag set'   # s67: q7 allowed (jsepf now gets the bonus file; q7m = masked payer credit)
    assert not Q7M or Q7, 'q7m needs q7'
    F2B7 = 'f2b7' in FLAGS   # s86: q7m masks on 7-sides from the (already loaded, ungated) f2b d7_w7 / d8_w7 rules; jsepf reads JSEPF_F2B7
    assert not F2B7 or Q7M, 'f2b7 needs q7m'
    if F2B7 and 'f2b7ctl' in FLAGS: log('f2b7ctl: NEGATIVE CONTROL, python rows use f2b7 but jsepf does not (selftest must fail)')
    elif F2B7: os.environ['JSEPF_F2B7'] = '1'; log('f2b7: q7m masks on sides with c or apex >= 7 = 31 & ~extra7 (python rows + jsepf JSEPF_F2B7=1)')
    log('f2b: rules loaded from %s%s: %s' % (OPT['f2b'], ' (OFF: empty rule set)' if 'f2boff' in FLAGS else '', dict(_st)))
    _orig_recv_coef_R2 = recv_coef_R2
    Q7PLANT = 'q7plant' in FLAGS; Q7PKEY = (7, 6, 6, 5, 5, 5, 7)
    def _clean(cf):
        for k in [k for k, v in cf.items() if v == 0]: del cf[k]
        return cf
    def recv_coef_R2(d, lk, sv, xon, tau=None):
        cf = _orig_recv_coef_R2(d, lk, sv, xon, tau)
        if d > 9: return cf
        U = min(d, 9); w = [int(ch) for ch in lk]; s = [int(ch) for ch in sv]
        for j in range(d):
            if w[j] != 6: continue
            ex = f2bm.extra6(d, w, s, j)
            if not ex: continue
            sg = sig2_of(U, w[(j + 1) % d], s[j], s[(j - 1) % d], w[(j - 1) % d], w[(j + 2) % d], w[(j - 2) % d])
            am = amask(U, w[(j - 2) % d], w[(j - 1) % d], w[(j + 1) % d], w[(j + 2) % d], s[(j - 2) % d], s[(j - 1) % d], s[j], s[(j + 1) % d])
            if not (ex & am): continue
            s0 = sg + (am,); s1 = sg + (am & ~ex,); F2B_STAT['w6'] += 1
            if sig2_keys(s0): cf[('M', s0)] -= 1
            if sig2_keys(s1): cf[('M', s1)] += 1
        if Q7M and d in (7, 8):   # s67: masked q7 -- the 7 neighbour A's hidden privates p1 (next to s_j) / p2 (next to s_{j-1}) are restricted by L3T (d=7) or the V=8 table (d=8) & ~extra7
            T = L3T if d == 7 else (l3q_loadV(8) if 8 in LQVX else None)
            if T is not None:
                for j in range(d):
                    if w[j] != 7: continue
                    sg0 = q7sig(U, w[(j + 1) % d], s[j], s[(j - 1) % d], w[(j - 1) % d])
                    if not q7keys(sg0): continue
                    ms = []
                    for sgn in (1, -1):
                        c = w[(j + sgn) % d]; ap_, o = (s[j], s[(j - 1) % d]) if sgn == 1 else (s[(j - 1) % d], s[j])
                        if c <= 6 and ap_ <= 6:
                            ms.append(T[(sgn, c, w[(j + 2 * sgn) % d], w[(j + 3 * sgn) % d], w[(j + 4 * sgn) % d], ap_, o)] & ~f2bm.extra7(d, w, s, j, sgn))
                        elif F2B7: ms.append(31 & ~f2bm.extra7(d, w, s, j, sgn)); F2B_STAT['f2b7'] += 1   # s86: 7-side (c or ap >= 7): no L3T mask, the f2b d7_w7/d8_w7 rules still apply
                        else: ms.append(31)
                    sgm = q7sig(U, w[(j + 1) % d], s[j], s[(j - 1) % d], w[(j - 1) % d], ms[0], ms[1])
                    if Q7PLANT and Q7PKEY in q7keys(sgm): cf[('Q', sgm)] += 1   # PLANTED ERROR (control): payer coefficient of the column q(7665557) doubled, python side only
                    if sgm != sg0:
                        cf[('Q', sg0)] -= 1; F2B_STAT['q7m'] += 1
                        if q7keys(sgm): cf[('Q', sgm)] += 1
        return _clean(cf)
    _orig_l3q_terms = l3q_terms
    def l3q_terms(d, w, s):
        cf = _orig_l3q_terms(d, w, s)
        if not L3Q or d != 7: return cf
        n = 7
        for i in range(n):
            if w[i] != 7: continue
            for sg in (1, -1):
                c, a, a2 = w[(i + sg) % n], w[(i + 2 * sg) % n], w[(i + 3 * sg) % n]
                ap_, o = (s[i], s[(i - 1) % n]) if sg == 1 else (s[(i - 1) % n], s[i])
                if c <= 6 and ap_ <= 6:
                    m = L3T[(sg, c, a, a2, w[(i + 4 * sg) % n], ap_, o)]; ex = f2bm.extra7(7, w, s, i, sg)
                    if ex & m: cf[('lQ', (c, ap_, m))] -= 1; cf[('lQ', (c, ap_, m & ~ex))] += 1; F2B_STAT['w7d7'] += 1
        return _clean(cf)
    _orig_l3q_terms_payeeV = l3q_terms_payeeV
    def l3q_terms_payeeV(d, w, s):
        cf = _orig_l3q_terms_payeeV(d, w, s); V = min(d, 9)
        if V not in LQVX or d not in (7, 8): return cf
        T = l3q_loadV(V); n = d
        for i in range(n):
            if w[i] != 7: continue
            for sg in (1, -1):
                c, w2, w3, w4 = (w[(i + k * sg) % n] for k in (1, 2, 3, 4))
                ap_, o = (s[i], s[(i - 1) % n]) if sg == 1 else (s[(i - 1) % n], s[i])
                if c <= 6 and ap_ <= 6:
                    m = T[(sg, c, w2, w3, w4, ap_, o)]; ex = f2bm.extra7(d, w, s, i, sg)
                    if ex & m: cf[('lQ', (V, c, ap_, m))] -= 1; cf[('lQ', (V, c, ap_, m & ~ex))] += 1; F2B_STAT['w7d8'] += 1
        return _clean(cf)

    def f2b_buckets(g, dval):
        buckets = [dict() for _ in range(25)]
        for p, wr, sr in f2bm._R[g]:
            fw = 0
            for o, al in wr:
                bits = sum(1 << (x - 5) for x in al); fw |= ((~bits) & 31) << (5 * (o % dval))
            fs = 0; sd = dict(sr)
            for o, v in sr: fs |= ((~(1 << (v - 5))) & 31) << (5 * (o % dval))
            sm1s = [sd[-1] - 5] if -1 in sd else range(5); s0s = [sd[0] - 5] if 0 in sd else range(5)
            for a in sm1s:
                for b in s0s:
                    k = (fw, fs); buckets[a * 5 + b][k] = buckets[a * 5 + b].get(k, 0) | (1 << (p - 5))
        o = bytearray()
        for b in range(25):
            items = sorted(buckets[b].items()); o += np.array([len(items)], dtype='<u4').tobytes()
            if items: o += np.array([(fw, fs, kb) for (fw, fs), kb in items], dtype='<u8').tobytes()
        return bytes(o)
    def f2b_write(d):
        """per-d table file for jsepf (layout in jsepf.cpp); built from the current M / Q values (F2B_MV2, LQQ, LQV)"""
        kt_load(); U = min(d, 9); MV2 = F2B_MV2[0]; assert MV2 is not None
        out = bytearray(np.array([d], dtype='<i4').tobytes())
        km = (31 & ~np.asarray(KT[U]).astype(np.int64)).astype(np.uint8); assert km.shape == (5,) * 8
        out += np.ascontiguousarray(km).tobytes()
        V6 = np.zeros((5, 5, 5, 5, 2, 2, 32))
        for b, e, q, r in itertools.product(range(5), repeat=4):
            for ca, cf_ in itertools.product((0, 1), repeat=2):
                sg = sig2_of(U, LET[e], LET[r], LET[q], LET[b], 7 if cf_ else 5, 7 if ca else 5)
                for m in range(32):
                    v = MV2(sg + (m,)); V6[b, e, q, r, ca, cf_, m] = 0.0 if v is None else v
        out += V6.astype('<f8').tobytes()
        QM = np.zeros((5, 5, 32))
        if d in (7, 8) and L3Q:
            for c_, a_ in itertools.product((5, 6), repeat=2):
                for m in range(32): QM[c_ - 5, a_ - 5, m] = l3q_Qeff(c_, a_, m) if d == 7 else l3q_QeffV(8, c_, a_, m)
        out += QM.astype('<f8').tobytes()
        out += f2b_buckets('d%d_w6' % d, d) if d <= 9 else b''.join(np.array([0], dtype='<u4').tobytes() for _ in range(25))
        for g in ('d%d_w7_1', 'd%d_w7_-1'):
            if d in (7, 8): out += f2b_buckets(g % d, d)
            else: out += b''.join(np.array([0], dtype='<u4').tobytes() for _ in range(25))
        fn = os.path.join(WORK, 'f2b_d%d.bin' % d); open(fn, 'wb').write(bytes(out)); return fn
    _Q7KEY = {}
    def q7m_write(d):
        """s67: jsepf argv[12] table for masked q7: doubles QT[((b*5+e)*5+q)*5+r][m1][m2] (shape 625 x 32 x 32) = max over p1 in m1, p2 in m2 of QV[key(U, e, r, p1, p2, q, b)] (0 if no key); b,e = w_{j-1}, w_{j+1}, q,r = s_{j-1}, s_j"""
        U = min(d, 9)
        if U not in _Q7KEY:
            kk = {}
            for b, e, q, r, p1, p2 in itertools.product(range(5), repeat=6):
                wd = (U, LET[e], LET[r], LET[p1], LET[p2], LET[q], LET[b])
                kk[(b, e, q, r, p1, p2)] = None if ''.join(map(str, canon(wd))) in RBIG else qkey(wd)
            _Q7KEY[U] = kk
        kk = _Q7KEY[U]; A = np.full((5, 5, 5, 5, 5, 5), -1.0)
        for ix, k in kk.items():
            if k is not None: A[ix] = QV.get(k, 0.0)
        A = A.reshape(625, 5, 5)
        R = np.zeros((625, 5, 32))   # over p2 for each m2
        for m2 in range(1, 32):
            sel = [k for k in range(5) if (m2 >> k) & 1]; R[:, :, m2] = A[:, :, sel].max(axis=2)
        T = np.zeros((625, 32, 32))
        for m1 in range(1, 32):
            sel = [k for k in range(5) if (m1 >> k) & 1]; T[:, m1, :] = R[:, sel, :].max(axis=1)
        T = np.maximum(T, 0.0)
        fn = os.path.join(WORK, 'q7m_d%d.bin' % d); open(fn, 'wb').write(T.astype('<f8').tobytes()); return fn
    def f2b_selftest(y, xd, MV2, t, N):
        """C++ leaf total (jsepf eval, f2b tables) vs the exact Python row value (recv_coef_R2 with the masks), on random arrangements and arrangements built from the rules"""
        rng = random.Random(int(OPT.get('seed', '1'))); res = {}
        def val(k):
            if k[0] == 'y': return y[RIX[k[1]]]
            if k[0] == 'x': return xd.get(k[1], 0.0)
            if k[0] == 'M': v = MV2(k[1]); return 0.0 if v is None else v
            if k[0] == 'r': return RV.get(k[1], 0.0)
            if k[0] == 'rr': return RRV.get(k[1], 0.0)
            if k[0] == 'z': return ZV.get(k[1], 0.0)   # s69: z / zr keys in the selftest value map (were missing: 'unsupported key')
            if k[0] == 'zr': return ZRV.get(k[1], 0.0)
            if k[0] == 'lq': return LQV.get(k[1], 0.0)
            if k[0] == 'q': return QV.get(k[1], 0.0)
            if k[0] == 'Q': return max([QV.get(kk, 0.0) for kk in q7keys(k[1])] or [0.0])
            if k[0] == 'lQ': return l3q_Qeff(*k[1]) if len(k[1]) == 3 else l3q_QeffV(*k[1])
            if k[0] == 'ks': return KSV.get(k[1], 0.0)   # s78 K*
            raise Exception('selftest: unsupported key %s' % (k,))
        for d in (7, 8, 9):
            U = min(d, 9); W = window_table_R2(U, y, xd, MV2); arr = []
            tries = 0
            while len(arr) < N and tries < 200 * N:
                tries += 1
                if 'egforce' in FLAGS and EG and len(arr) % 3 == 2:   # s78: planted generic EDGE payer (d = 7) or payee pattern
                    w, s = eg_force(rng, d)
                elif 'ksforce' in FLAGS and d == 7 and len(arr) % 3 == 1:   # s78: arrangements with a planted K* payer or payee pattern
                    w, s = kstar_force(rng, d)
                elif 'q7force' in FLAGS and len(arr) % 4 == 1:   # s67: arrangements with a payer slot of the key 7665557 (7 with neighbours 7, 6 | apex 6 | apex 5 | 7), both orientations
                    i0 = rng.randrange(d); w = [rng.choice((5, 6, 7, 8, 9)) for _ in range(d)]; s = [rng.choice((5, 6, 7, 8, 9)) for _ in range(d)]
                    w[i0] = 7; w[(i0 + 1) % d] = 6; s[i0] = 6; s[(i0 - 1) % d] = 5; w[(i0 - 1) % d] = 7
                    if rng.random() < 0.5: w = [w[(i0 - k) % d] for k in range(d)]; s = [s[(i0 - k - 1) % d] for k in range(d)]
                elif len(arr) % 2 == 0 and f2bm._R['d%d_w6' % d]:   # build from a random w6 or w7 rule
                    g = rng.choice(['d%d_w6' % d] + (['d%d_w7_1' % d, 'd%d_w7_-1' % d] if d in (7, 8) else []))
                    p, wr, sr = rng.choice(f2bm._R[g]); i0 = rng.randrange(d)
                    w = [rng.choice((5, 6, 7, 8, 9)) for _ in range(d)]; s = [rng.choice((5, 6, 7, 8, 9)) for _ in range(d)]
                    w[i0] = 6 if 'w6' in g else 7
                    for o, al in wr: w[(i0 + o) % d] = rng.choice(sorted(al))
                    for o, v in sr: s[(i0 + o) % d] = v
                else:
                    w = [rng.choice((5, 6, 7, 8, 9)) for _ in range(d)]; s = [rng.choice((5, 6, 7, 8, 9)) for _ in range(d)]
                lk = ''.join(map(str, w)); sv = ''.join(map(str, s))
                if admissible(d, lk, sv) is not None: continue
                arr.append((lk, sv))
            ef = os.path.join(WORK, 'f2b_eval_d%d.txt' % d); open(ef, 'w').write(''.join('%s %s\n' % a for a in arr))
            F2B_EVAL[0] = ef; rr, dt, ni = run_sep(d, W, 1e9, 1, 0); F2B_EVAL[0] = None
            cpp = [float(r[1]) for r in rr if r[0] == 'E']
            assert len(cpp) == len(arr), (len(cpp), len(arr))
            F2B_STAT.clear(); mx = 0.0; nchg = 0; worst = None
            for (lk, sv), c in zip(arr, cpp):
                cf = recv_coef_R2(d, lk, sv, 'xon' in FLAGS)
                pv = sum(v * val(k) for k, v in cf.items())
                if abs(pv - c) > mx: mx = abs(pv - c); worst = (lk, sv, pv, c)
            nm = dict(F2B_STAT); F2B_STAT.clear()
            nQ = sum(1 for lk, sv in arr if any(k[0] == 'Q' for k in recv_coef_R2(d, lk, sv, 'xon' in FLAGS))); nq = sum(1 for lk, sv in arr if d == 7 and any(k[0] == 'q' and QV.get(k[1], 0.0) > 0 for k in recv_coef_R2(d, lk, sv, 'xon' in FLAGS))) if Q7 else 0
            if Q7: log('  q7 coverage d=%d: %d arrangements with a Q payer coefficient, %d with a q payee coefficient of positive value' % (d, nQ, nq))
            if EG:   # s78: generic EDGE coverage of the self-test arrangements
                for key_ in EGKEYS:
                    _c = [recv_coef_R2(d, lk, sv, 'xon' in FLAGS).get(('ks', key_['name']), 0) for lk, sv in arr]
                    _p = sum(1 for lk, sv in arr if d == 7 and eg_payer_count(key_, [int(c_) for c_ in lk], [int(c_) for c_ in sv]))
                    log('  edge coverage d=%d %s: amount %.9f; %d arrangements with a payer slot, %d with a nonzero coefficient (min %d max %d)' % (d, key_['name'], KSV.get(key_['name'], 0.0), _p, sum(1 for v_ in _c if v_), min(_c), max(_c)))
            if KSTAR and d == 7:   # s78: K* coverage of the self-test arrangements
                _kc = [recv_coef_R2(d, lk, sv, 'xon' in FLAGS).get(('ks', 'K1'), 0) for lk, sv in arr]
                _kp = sum(1 for lk, sv in arr if any(kstar_payer_slot([int(c_) for c_ in lk], [int(c_) for c_ in sv], i_, e_) for i_ in range(7) for e_ in (1, -1)))
                _ke = sum(1 for lk, sv in arr if any(kstar_payee_slot([int(c_) for c_ in lk], [int(c_) for c_ in sv], i_, e_) for i_ in range(7) for e_ in (1, -1)))
                _k0, _k1 = kstar_kub(); _gap = 0
                for lk, sv in arr:
                    w_ = [int(c_) - 5 for c_ in lk]; s_ = [int(c_) - 5 for c_ in sv]
                    ub_ = sum(int(_k0[np.ravel_multi_index(tuple(w_[(k_ + o_) % 7] for o_ in (-2, -1, 0, 1, 2)) + tuple(s_[(k_ + o_) % 7] for o_ in (-2, -1, 0, 1)), (5,) * 9)]) + int(_k1[np.ravel_multi_index(tuple(w_[(k_ + o_) % 7] for o_ in (-2, -1, 0, 1, 2)) + tuple(s_[(k_ + o_) % 7] for o_ in (-2, -1, 0, 1)), (5,) * 9)]) for k_ in range(7))
                    ex_ = sum(kstar_payee_slot([int(c_) for c_ in lk], [int(c_) for c_ in sv], i_, e_) for i_ in range(7) for e_ in (1, -1))
                    assert ex_ <= ub_, (lk, sv, ex_, ub_)
                    _gap += ub_ > ex_
                log('  kstar coverage d=7: K1 = %.9f; %d arrangements with a payer slot, %d with an exact payee slot, %d with a nonzero K1 coefficient (min %d max %d); %d with a window bound above the exact payee count (leaf correction < 0)' % (KSV.get('K1', 0.0), _kp, _ke, sum(1 for c_ in _kc if c_), min(_kc), max(_kc), _gap))
            _a = f2bm.ACTIVE; f2bm.ACTIVE = False
            noru = [sum(v * val(k) for k, v in recv_coef_R2(d, lk, sv, 'xon' in FLAGS).items()) for lk, sv in arr]
            f2bm.ACTIVE = _a
            nchg = sum(1 for (lk, sv), a in zip(arr, noru) if abs(a - sum(v * val(k) for k, v in recv_coef_R2(d, lk, sv, 'xon' in FLAGS).items())) > 1e-12)
            log('F2B-SELFTEST d=%d: %d arrangements, max |python exact - C++ leaf| = %.3g, %d changed by the rules (rule-fire counts %s), worst %s' % (d, len(arr), mx, nchg, nm, worst if mx > 1e-9 else '-'))
            res[d] = mx
        log('F2B-SELFTEST: %s' % ('PASS' if all(v < 1e-9 for v in res.values()) else 'FAIL'))
