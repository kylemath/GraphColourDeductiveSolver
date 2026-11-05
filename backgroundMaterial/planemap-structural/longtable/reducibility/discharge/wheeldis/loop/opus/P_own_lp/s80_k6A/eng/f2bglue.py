import random
# f2bglue.py (s60_f2b): outside team's full-wheel 2-ball private-letter exclusions in the Opus R6x2 engine.  exec'd by pcheck.py after prelay2.py.
# Option f2b=RULES.json switches it on (flag f2boff = load the plumbing with an empty rule set, for validation).  Without f2b nothing changes.
# Semantics (ext_f2b/f2b.py, read from the outside team's make_recv_spec_full2ball): a firing rule removes letter p_deg from
#   (w6)  the allowed-private mask am of a 6 spoke (d = 7, 8, 9): M row key ('M', sig + (am,)) -> ('M', sig + (am & ~bit,));
#   (w7)  the l3q mask m of a link-7 side (d = 7 V=7 table, d = 8 V=8 table; c = w_{i+sg} and apex in {5,6}): ('lQ', (c, ap, m)) -> (c, ap, m & ~bit).
# Masking only removes options, so every window upper bound of the DFS stays valid; the exact value is corrected at the leaf (jsepf).
F2B_ON = 'f2b' in OPT
if 'f2bx' in OPT and not F2B_ON: log('f2bx needs f2b=RULES (the extra rules ride on the f2b plumbing)'); sys.exit(8)   # s80
F2B_MV2 = [None]; F2B_EVAL = [None]; F2B_STAT = collections.Counter()
BINF = os.path.join(HERE, 'bin', 'jsepf')
if F2B_ON:
    import importlib.util as _ilu
    _sp = _ilu.spec_from_file_location('f2bmod', os.path.join(HERE, 'f2b.py')); f2bm = _ilu.module_from_spec(_sp); _sp.loader.exec_module(f2bm)
    _st = f2bm.load(OPT['f2b'], off='f2boff' in FLAGS, extra=OPT.get('f2bx'))   # s80: f2bx = extra rule files (B3 routes A' / L')
    assert F16 and AC and AP and not XO and not FY and not V6 and not W19 and not PCAM and 'ref' not in FLAGS, 'f2b: unsupported flag set'   # s67: q7 allowed (jsepf now gets the bonus file; q7m = masked payer credit)
    assert not Q7M or Q7, 'q7m needs q7'
    log('f2b: rules loaded from %s%s: %s' % (OPT['f2b'], ' (OFF: empty rule set)' if 'f2boff' in FLAGS else '', dict(_st)))
    if OPT.get('f2bx'): log('f2bx: extra rules from %s: (added, already present) per group %s' % (OPT['f2bx'], dict(f2bm.XSTATS)))
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
            raise Exception('selftest: unsupported key %s' % (k,))
        for d in (7, 8, 9):
            U = min(d, 9); W = window_table_R2(U, y, xd, MV2); arr = []
            tries = 0
            while len(arr) < N and tries < 200 * N:
                tries += 1
                if 'q7force' in FLAGS and len(arr) % 4 == 1:   # s67: arrangements with a payer slot of the key 7665557 (7 with neighbours 7, 6 | apex 6 | apex 5 | 7), both orientations
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
            _a = f2bm.ACTIVE; f2bm.ACTIVE = False
            noru = [sum(v * val(k) for k, v in recv_coef_R2(d, lk, sv, 'xon' in FLAGS).items()) for lk, sv in arr]
            f2bm.ACTIVE = _a
            nchg = sum(1 for (lk, sv), a in zip(arr, noru) if abs(a - sum(v * val(k) for k, v in recv_coef_R2(d, lk, sv, 'xon' in FLAGS).items())) > 1e-12)
            log('F2B-SELFTEST d=%d: %d arrangements, max |python exact - C++ leaf| = %.3g, %d changed by the rules (rule-fire counts %s), worst %s' % (d, len(arr), mx, nchg, nm, worst if mx > 1e-9 else '-'))
            res[d] = mx
        log('F2B-SELFTEST: %s' % ('PASS' if all(v < 1e-9 for v in res.values()) else 'FAIL'))

    # ---- s80 (Team E): self-tests for the f2bx extra rules (B3 routes A' / L'), run inside upperR2 at a solution:
    #   pcheck.py upperR2 ... f2bx=RULES.json f2bself=0 f2bxself=N [f2bxtries=3000] [f2bxkeep=40] [f2bxsub=3] [f2bxsl=56789] [f2bxlinks=L,..] [f2bxtight=1e-3]
    # (b) per extra rule: a constructed admissible row the rule matches (letter still alive before it) gets exactly the stated
    #     coefficient change (engine diff 'all rules' - 'all rules but this one' == independent expectation), and the same row
    #     with any one requirement slot changed to a disallowed letter gets the expected change (none when the rule no longer fires).
    # (c) separator vs exact: jsepf leaf (EVAL, no pruning) vs Python exact value on every test row + random rows; and at d = 7 an
    #     exhaustive check on restricted sub-spaces (link fixed by single-slot forbidden patterns, all 5^7 apex words, SYM off):
    #     the jsepf mode-0 report at a low and a mid threshold equals the Python list of admissible rows above it, value by value.
    # (t) near-tight rows of the solution on the stack WITHOUT the extra rules (jsepf mode 0, d = 7..9) and how many the rules change.
    def _f2b_rebuild_idx(g):
        idx = {}
        for p, wr, sr in f2bm._R[g]:
            sd = dict(sr); key = (sd.get(-1), sd.get(0))
            idx.setdefault(key, []).append((wr, tuple((o, v) for o, v in sr), 1 << (p - 5)))
        f2bm._IDX[g] = idx
    def _f2b_drop(drop):   # drop = {group: set of rule tuples}; returns a restore function
        saved = {g: list(f2bm._R[g]) for g in f2bm.GROUPS}
        for g, rs in drop.items():
            f2bm._R[g] = [r for r in f2bm._R[g] if r not in rs]; _f2b_rebuild_idx(g)
        def restore():
            for g in f2bm.GROUPS: f2bm._R[g] = saved[g]; _f2b_rebuild_idx(g)
        return restore
    def _fires(rule, d, w, s, i):
        p, wr, sr = rule
        return all(w[(i + o) % d] in al for o, al in wr) and all(s[(i + o) % d] == v for o, v in sr)
    def _bits(g, d, w, s, i, skip=None):
        b = 0
        for r in f2bm._R[g]:
            if r != skip and _fires(r, d, w, s, i): b |= 1 << (r[0] - 5)
        return b
    def _cdiff(a, b):
        c = collections.Counter()
        for k, v in a.items(): c[k] += v
        for k, v in b.items(): c[k] -= v
        return {k: v for k, v in c.items() if v}
    def _expect(g, r, d, w, s):
        """independent expected coefficient change (rule r on minus off) of row (d, w, s), from the stated semantics"""
        exp = collections.Counter(); U = min(d, 9); bit = 1 << (r[0] - 5); W_ = lambda k: w[k % d]; S_ = lambda k: s[k % d]
        if g.endswith('_w6'):
            for i in range(d):
                if w[i] != 6 or not _fires(r, d, w, s, i): continue
                sg = sig2_of(U, W_(i + 1), S_(i), S_(i - 1), W_(i - 1), W_(i + 2), W_(i - 2))
                am = amask(U, W_(i - 2), W_(i - 1), W_(i + 1), W_(i + 2), S_(i - 2), S_(i - 1), S_(i), S_(i + 1))
                m0 = am & ~_bits(g, d, w, s, i, skip=r); m1 = m0 & ~bit
                if m1 == m0: continue
                if sig2_keys(sg + (m0,)): exp[('M', sg + (m0,))] -= 1
                if sig2_keys(sg + (m1,)): exp[('M', sg + (m1,))] += 1
            return {k: v for k, v in exp.items() if v}
        sgn = 1 if g.endswith('_1') and not g.endswith('_-1') else -1; assert d == 7, 'f2bx test: w7 rules at d = 7 only'
        def side_mask(i, sd, with_r):
            c = W_(i + sd); a_, o = (S_(i), S_(i - 1)) if sd == 1 else (S_(i - 1), S_(i))
            if c > 6 or a_ > 6: return None
            gg = 'd7_w7_%d' % sd; ex = _bits(gg, d, w, s, i, skip=r) | (bit if (with_r and gg == g and _fires(r, d, w, s, i)) else 0)
            return c, a_, L3T[(sd, c, W_(i + 2 * sd), W_(i + 3 * sd), W_(i + 4 * sd), a_, o)] & ~ex
        for i in range(d):
            if w[i] != 7 or not _fires(r, d, w, s, i): continue
            on, off = side_mask(i, sgn, True), side_mask(i, sgn, False)
            if on is None or on == off: continue
            exp[('lQ', off)] -= 1; exp[('lQ', on)] += 1
            if Q7M:
                sg0 = q7sig(U, W_(i + 1), S_(i), S_(i - 1), W_(i - 1))
                if not q7keys(sg0): continue
                def term(with_r):
                    ms = [31, 31]
                    for k_, sd in enumerate((1, -1)):
                        x = side_mask(i, sd, with_r)
                        if x is not None: ms[k_] = x[2]
                    sgm = q7sig(U, W_(i + 1), S_(i), S_(i - 1), W_(i - 1), ms[0], ms[1])
                    return sg0 if sgm == sg0 else (sgm if q7keys(sgm) else None)
                a, b = term(True), term(False)
                if a != b:
                    if a is not None: exp[('Q', a)] += 1
                    if b is not None: exp[('Q', b)] -= 1
        return {k: v for k, v in exp.items() if v}
    def f2bx_selftest(y, xd, MV2, t, Nn):
        rng = random.Random(int(OPT.get('seed', '1'))); TR = int(OPT.get('f2bxtries', '3000'))
        XR = {g: sorted(f2bm.XRULES.get(g, ())) for g in f2bm.GROUPS}
        log('F2BX-SELFTEST: extra rules per group %s' % {g: len(v) for g, v in XR.items()})
        def val(k):
            if k[0] == 'y': return y[RIX[k[1]]]
            if k[0] == 'x': return xd.get(k[1], 0.0)
            if k[0] == 'M': v = MV2(k[1]); return 0.0 if v is None else v
            if k[0] == 'r': return RV.get(k[1], 0.0)
            if k[0] == 'rr': return RRV.get(k[1], 0.0)
            if k[0] == 'z': return ZV.get(k[1], 0.0)
            if k[0] == 'zr': return ZRV.get(k[1], 0.0)
            if k[0] == 'lq': return LQV.get(k[1], 0.0)
            if k[0] == 'q': return QV.get(k[1], 0.0)
            if k[0] == 'Q': return max([QV.get(kk, 0.0) for kk in q7keys(k[1])] or [0.0])
            if k[0] == 'lQ': return l3q_Qeff(*k[1]) if len(k[1]) == 3 else l3q_QeffV(*k[1])
            raise Exception('selftest: unsupported key %s' % (k,))
        xon = 'xon' in FLAGS; L = lambda v: ''.join(map(str, v)); EV = collections.defaultdict(list); CHL = collections.defaultdict(list)
        tot = collections.Counter(); bad = []; per = []
        # ---- (b) ----
        for g in f2bm.GROUPS:
            if not XR[g]: continue
            d = int(g[1]); par = 6 if '_w6' in g else 7
            sgn = 0 if par == 6 else (1 if g.endswith('_1') and not g.endswith('_-1') else -1)
            for r in XR[g]:
                found = None; nadm = 0; samp = []; KEEP = int(OPT.get('f2bxkeep', '40'))
                for _ in range(TR):
                    i0 = rng.randrange(d); w = [rng.choice((5, 5, 6, 6, 7, 7, 8, 9)) for _ in range(d)]; s = [rng.choice((5, 5, 6, 6, 7, 7, 8, 9)) for _ in range(d)]
                    if sgn:   # keep the l3q side readable (c, a <= 6) when the rule leaves them free
                        w[(i0 + sgn) % d] = rng.choice((5, 6)); s[i0 if sgn == 1 else (i0 - 1) % d] = rng.choice((5, 6))
                    w[i0] = par
                    for o, al in r[1]: w[(i0 + o) % d] = rng.choice(sorted(al))
                    for o, v in r[2]: s[(i0 + o) % d] = v
                    if admissible(d, L(w), L(s)) is not None: continue
                    nadm += 1; e = _expect(g, r, d, w, s)
                    if e and found is None: found = (i0, w, s, e)
                    if len(samp) < KEEP or (e and not any(x[3] for x in samp)): samp.append((i0, w, s, e))
                    if found is not None and len(samp) >= KEEP: break
                # engine diff (rule on - rule off) on every kept matched row == independent expectation (also where it is empty)
                restore = _f2b_drop({g: {r}}); off_ = [recv_coef_R2(d, L(w), L(s), xon) for i0, w, s, e in samp]; restore()
                nok = nch = 0
                for (i0, w, s, e), cf_off in zip(samp, off_):
                    dg = _cdiff(recv_coef_R2(d, L(w), L(s), xon), cf_off)
                    if dg == e: nok += 1
                    else: bad.append(('sample', g, r, L(w), L(s), dg, e))
                    nch += bool(dg)
                tot['b: sampled matched rows'] += len(samp); tot['b: sampled matched rows exact'] += nok
                EV[d] += [(L(w), L(s)) for i0, w, s, e in samp[:5]]
                if found is None:
                    per.append((g, r, 'NO CHANGE: %d admissible matched rows sampled, engine = expectation on %d/%d kept, all with no change (letter already removed by kill6 / other rules there)' % (nadm, nok, len(samp)))); tot['b: rules with no change found'] += 1; continue
                i0, w, s, e = found
                restore = _f2b_drop({g: {r}}); cf_off = recv_coef_R2(d, L(w), L(s), xon); restore()
                cf_on = recv_coef_R2(d, L(w), L(s), xon); dg = _cdiff(cf_on, cf_off)
                ok = dg == e; tot['b: rules with a change'] += 1; tot['b: match rows exact' if ok else 'b: match rows WRONG'] += 1
                if not ok: bad.append(('match', g, r, L(w), L(s), dg, e))
                EV[d] += [(L(w), L(s))]; CHL[d].append(L(w))
                # miss rows: each requirement slot set to a disallowed letter
                nm = nz = 0
                for kind, o, allowed in [('w', o, al) for o, al in r[1]] + [('s', o, {v}) for o, v in r[2]]:
                    w2, s2 = list(w), list(s); p_ = (i0 + o) % d
                    alt = [x for x in LET if x not in allowed]
                    if kind == 'w': w2[p_] = rng.choice(alt)
                    else: s2[p_] = rng.choice(alt)
                    assert not _fires(r, d, w2, s2, i0)
                    restore = _f2b_drop({g: {r}}); cf_off = recv_coef_R2(d, L(w2), L(s2), xon); restore()
                    cf_on = recv_coef_R2(d, L(w2), L(s2), xon); dg = _cdiff(cf_on, cf_off); e2 = _expect(g, r, d, w2, s2)
                    nm += 1; nz += (not dg)
                    if dg != e2: bad.append(('miss', g, r, L(w2), L(s2), dg, e2)); tot['b: miss rows WRONG'] += 1
                    else: tot['b: miss rows exact'] += 1
                    if not dg: tot['b: miss rows with no change'] += 1
                    EV[d] += [(L(w2), L(s2))]
                per.append((g, r, 'CHANGE: %d admissible matched rows sampled (%d kept: engine = expectation on %d, %d changed); match row %s/%s spoke %d: change %s exact=%s; %d miss rows (one requirement off), %d with no change' % (nadm, len(samp), nok, nch, L(w), L(s), i0, sorted(e.items(), key=str), ok, nm, nz)))
        for g, r, msg in per: log('  f2bx %s %s: %s' % (g, r, msg))
        # ---- (c1) jsepf leaf vs Python exact ----
        mx = {}
        for d in (7, 8, 9):
            arr = list(EV.get(d, []))
            while len(arr) < len(EV.get(d, [])) + Nn:
                w = [rng.choice(LET) for _ in range(d)]; s = [rng.choice(LET) for _ in range(d)]
                if admissible(d, L(w), L(s)) is None: arr.append((L(w), L(s)))
            arr = [a for a in arr if admissible(d, a[0], a[1]) is None]
            if not arr: continue
            W = window_table_R2(min(d, 9), y, xd, MV2)
            ef = os.path.join(WORK, 'f2bx_eval_d%d.txt' % d); open(ef, 'w').write(''.join('%s %s\n' % a for a in arr))
            F2B_EVAL[0] = ef; rr, dt, ni = run_sep(d, W, 1e9, 1, 0); F2B_EVAL[0] = None
            cpp = [float(r_[1]) for r_ in rr if r_[0] == 'E']; assert len(cpp) == len(arr), (len(cpp), len(arr))
            m = 0.0; worst = None
            for (lk, sv), c in zip(arr, cpp):
                pv = sum(v * val(k) for k, v in recv_coef_R2(d, lk, sv, xon).items())
                if abs(pv - c) > m: m = abs(pv - c); worst = (lk, sv, pv, c)
            mx[d] = m; tot['c1: rows d=%d' % d] = len(arr)
            log('F2BX-SELFTEST (c1) d=%d: %d rows (%d test rows + random), max |python exact - jsepf leaf| = %.3g %s' % (d, len(arr), len(EV.get(d, [])), m, worst if m > 1e-9 else ''))
        # ---- (c2) exhaustive restricted sub-spaces at d = 7 ----
        d = 7; W = window_table_R2(7, y, xd, MV2); links = []
        for lk, sv in EV.get(7, []):
            if lk not in links: links.append(lk)
        rng.shuffle(links); ch7 = []   # links of rows where an extra rule changed the row come first
        for lk in CHL.get(7, []):
            if lk not in ch7: ch7.append(lk)
        rng.shuffle(ch7); fl = [x for x in OPT.get('f2bxlinks', '').split(',') if x]   # f2bxlinks=L1,L2,..: these d = 7 links first
        links = fl + [lk for lk in ch7 if lk not in fl] + [lk for lk in links if lk not in ch7 and lk not in fl]; nsub = int(OPT.get('f2bxsub', '3')); c2ok = True
        for lk in links[:nsub]:
            Py = {}
            SL_ = tuple(int(c) for c in OPT.get('f2bxsl', '56789'))   # apex letters of the sub-space (the separator gets the same restriction)
            for sv_t in itertools.product(SL_, repeat=7):
                sv = L(sv_t)
                if admissible(7, lk, sv) is not None: continue
                Py[sv] = sum(v * val(k) for k, v in recv_coef_R2(7, lk, sv, xon).items())
            vals = sorted(Py.values())
            wl = [int(c) for c in lk]   # rows of this sub-space on which some extra d = 7 rule fires (w conditions pre-filtered per spoke)
            cand = [(r, i) for g in f2bm.GROUPS if g.startswith('d7') for r in XR[g] for i in range(7)
                    if wl[i] == (6 if '_w6' in g else 7) and all(wl[(i + o) % 7] in al for o, al in r[1])]
            FIRE = {sv for sv in Py if any(all(int(sv[(i + o) % 7]) == v for o, v in r[2]) for r, i in cand)}
            for thr in (-1e9, vals[int(0.8 * len(vals))] if vals else 0.0):
                inst = instances(7) + [((2 * i, 31 & ~(1 << LI[int(lk[i])])),) for i in range(7)]
                if len(SL_) < 5: inst += [((2 * i + 1, 31 & ~sum(1 << LI[x] for x in SL_)),) for i in range(7)]
                hdr = os.path.join(WORK, 'hdr_f2bx_sub.txt'); big = sorted(b for b in RBIG if len(b) == 7)
                with open(hdr, 'w') as f:
                    f.write('%d %.15f %d %d\n%d\n%s\n%d\n' % (7, thr, 10 ** 7, 0, len(big), '\n'.join(big), len(inst)))
                    for I in inst: f.write('%d %s\n' % (len(I), ' '.join('%d %d' % sk for sk in I)))
                wp = write_table(W, 'f2bx_sub')
                extra = ['1', '0', 'none', BONUSF[0] or 'none', L3FILE[0] or 'none', 'none', (L3VFILE[0] if (LQVX and L3VFILE[0]) else 'none'), f2b_write(7)]
                if Q7M: extra += ['none', q7m_write(7)]
                out = subprocess.run([BINF, hdr, wp] + extra, capture_output=True, text=True, check=True).stdout.split('\n')
                rep = {}
                for l_ in out:
                    f_ = l_.split()
                    if f_ and f_[0] == 'V':
                        assert f_[2] == lk, (f_, lk); rep[f_[3]] = float(f_[1])
                want = {sv: v for sv, v in Py.items() if v > thr}
                miss = [sv for sv in want if sv not in rep]; extra_ = [sv for sv in rep if sv not in want]
                dv = max([abs(rep[sv] - want[sv]) for sv in want if sv in rep] or [0.0])
                # rows at the threshold within float noise are not errors
                miss = [sv for sv in miss if want[sv] > thr + 1e-9]; extra_ = [sv for sv in extra_ if not (sv in Py and Py[sv] > thr - 1e-9)]
                nfire = sum(1 for sv in want if sv in FIRE)
                ok = not miss and not extra_ and dv < 1e-9; c2ok &= ok
                log('F2BX-SELFTEST (c2) d=7 link %s, apex words over %s: %d admissible; thr %.6f: python %d rows above (%d with an extra rule firing), jsepf reported %d; missing %d, extra %d, max |dv| %.3g -> %s' % (
                    lk, ''.join(map(str, SL_)), len(Py), thr, len(want), nfire, len(rep), len(miss), len(extra_), dv, 'OK' if ok else 'FAIL'))
                tot['c2: subspace runs'] += 1; tot['c2: subspace runs OK' if ok else 'c2: subspace runs FAIL'] += 1
        # ---- (t) near-tight rows without the extra rules ----
        if 'f2bxtight' in OPT:
            tol = float(OPT['f2bxtight']); restore = _f2b_drop({g: set(XR[g]) for g in f2bm.GROUPS})
            T_ = {}
            for d in (7, 8, 9):
                W = window_table_R2(min(d, 9), y, xd, MV2); rr, dt, ni = run_sep(d, W, d - 6 + t - tol, 500000, 0)
                T_[d] = [(r_[2], r_[3], float(r_[1])) for r_ in rr if r_[0] == 'V']
                log('  tight (slack <= %g, stack without the extra rules) d=%d: %d rows (max load %.9f, cap %.9f)%s' % (tol, d, len(T_[d]), max([x[2] for x in T_[d]] or [float('nan')]), d - 6 + t, ' TRUNCATED' if len(T_[d]) >= 500000 else ''))
            V0 = {d: [sum(v * val(k) for k, v in recv_coef_R2(d, lk, sv, xon).items()) for lk, sv, _ in T_[d]] for d in (7, 8, 9)}
            restore()
            for d in (7, 8, 9):
                nch = 0; drop = []; dsep = max([abs(a - b[2]) for a, b in zip(V0[d], T_[d])] or [0.0])
                log('  tight d=%d: max |python - jsepf| on these rows (no extra rules) %.3g' % (d, dsep))
                for (lk, sv, _), v0 in zip(T_[d], V0[d]):
                    v1 = sum(v * val(k) for k, v in recv_coef_R2(d, lk, sv, xon).items())
                    if abs(v1 - v0) > 1e-12: nch += 1; drop.append(v0 - v1)
                log('F2BX-SELFTEST (t) d=%d: %d of %d near-tight rows change with the extra rules; load drop max %.6f, mean %.6f' % (d, nch, len(T_[d]), max(drop or [0.0]), (sum(drop) / len(drop)) if drop else 0.0))
                tot['t: tight rows d=%d' % d] = len(T_[d]); tot['t: tight rows changed d=%d' % d] = nch
        for b_ in bad[:20]: log('  F2BX BAD %s' % (b_,))
        okb = not bad; okc = all(v < 1e-9 for v in mx.values()) and c2ok
        log('F2BX-SELFTEST: %s %s' % ('PASS' if okb and okc else 'FAIL', dict(tot)))
    _orig_f2b_selftest = f2b_selftest
    def f2b_selftest(y, xd, MV2, t, N):
        if 'f2bxself' in OPT: return f2bx_selftest(y, xd, MV2, t, int(OPT['f2bxself']))
        return _orig_f2b_selftest(y, xd, MV2, t, N)
