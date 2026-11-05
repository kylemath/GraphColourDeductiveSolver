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
    assert F16 and AC and AP and not XO and not FY and not V6 and not W19 and not PCAM and 'ref' not in FLAGS and not Q7, 'f2b: unsupported flag set'
    log('f2b: rules loaded from %s%s: %s' % (OPT['f2b'], ' (OFF: empty rule set)' if 'f2boff' in FLAGS else '', dict(_st)))
    _orig_recv_coef_R2 = recv_coef_R2
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
    def f2b_selftest(y, xd, MV2, t, N):
        """C++ leaf total (jsepf eval, f2b tables) vs the exact Python row value (recv_coef_R2 with the masks), on random arrangements and arrangements built from the rules"""
        rng = random.Random(int(OPT.get('seed', '1'))); res = {}
        def val(k):
            if k[0] == 'y': return y[RIX[k[1]]]
            if k[0] == 'x': return xd.get(k[1], 0.0)
            if k[0] == 'M': v = MV2(k[1]); return 0.0 if v is None else v
            if k[0] == 'r': return RV.get(k[1], 0.0)
            if k[0] == 'rr': return RRV.get(k[1], 0.0)
            if k[0] == 'lq': return LQV.get(k[1], 0.0)
            if k[0] == 'lQ': return l3q_Qeff(*k[1]) if len(k[1]) == 3 else l3q_QeffV(*k[1])
            raise Exception('selftest: unsupported key %s' % (k,))
        for d in (7, 8, 9):
            U = min(d, 9); W = window_table_R2(U, y, xd, MV2); arr = []
            tries = 0
            while len(arr) < N and tries < 200 * N:
                tries += 1
                if len(arr) % 2 == 0 and f2bm._R['d%d_w6' % d]:   # build from a random w6 or w7 rule
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
            _a = f2bm.ACTIVE; f2bm.ACTIVE = False
            noru = [sum(v * val(k) for k, v in recv_coef_R2(d, lk, sv, 'xon' in FLAGS).items()) for lk, sv in arr]
            f2bm.ACTIVE = _a
            nchg = sum(1 for (lk, sv), a in zip(arr, noru) if abs(a - sum(v * val(k) for k, v in recv_coef_R2(d, lk, sv, 'xon' in FLAGS).items())) > 1e-12)
            log('F2B-SELFTEST d=%d: %d arrangements, max |python exact - C++ leaf| = %.3g, %d changed by the rules (rule-fire counts %s), worst %s' % (d, len(arr), mx, nchg, nm, worst if mx > 1e-9 else '-'))
            res[d] = mx
        log('F2B-SELFTEST: %s' % ('PASS' if all(v < 1e-9 for v in res.values()) else 'FAIL'))
