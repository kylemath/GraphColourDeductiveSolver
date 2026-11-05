
    # ---- s80 (Team E): self-tests for the f2bx extra rules (B3 routes A' / L'), run inside upperR2 at a solution:
    #   pcheck.py upperR2 ... f2bx=RULES.json f2bself=0 f2bxself=1 [f2bxtries=3000] [f2bxsub=3] [f2bxtight=1e-3]
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
        xon = 'xon' in FLAGS; L = lambda v: ''.join(map(str, v)); EV = collections.defaultdict(list)
        tot = collections.Counter(); bad = []; per = []
        # ---- (b) ----
        for g in f2bm.GROUPS:
            if not XR[g]: continue
            d = int(g[1]); par = 6 if '_w6' in g else 7
            sgn = 0 if par == 6 else (1 if g.endswith('_1') and not g.endswith('_-1') else -1)
            for r in XR[g]:
                found = None; nadm = 0
                for _ in range(TR):
                    i0 = rng.randrange(d); w = [rng.choice((5, 5, 6, 6, 7, 7, 8, 9)) for _ in range(d)]; s = [rng.choice((5, 5, 6, 6, 7, 7, 8, 9)) for _ in range(d)]
                    if sgn:   # keep the l3q side readable (c, a <= 6) when the rule leaves them free
                        w[(i0 + sgn) % d] = rng.choice((5, 6)); s[i0 if sgn == 1 else (i0 - 1) % d] = rng.choice((5, 6))
                    w[i0] = par
                    for o, al in r[1]: w[(i0 + o) % d] = rng.choice(sorted(al))
                    for o, v in r[2]: s[(i0 + o) % d] = v
                    if admissible(d, L(w), L(s)) is not None: continue
                    nadm += 1
                    e = _expect(g, r, d, w, s)
                    if e: found = (i0, w, s, e); break
                if found is None:
                    per.append((g, r, 'no change in %d admissible matched rows (letter already removed by kill6 / other rules there)' % nadm)); tot['b: rule with no change found'] += 1; continue
                i0, w, s, e = found
                restore = _f2b_drop({g: {r}}); cf_off = recv_coef_R2(d, L(w), L(s), xon); restore()
                cf_on = recv_coef_R2(d, L(w), L(s), xon); dg = _cdiff(cf_on, cf_off)
                ok = dg == e; tot['b: match rows'] += 1; tot['b: match rows exact' if ok else 'b: match rows WRONG'] += 1
                if not ok: bad.append(('match', g, r, L(w), L(s), dg, e))
                EV[d] += [(L(w), L(s))]
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
                per.append((g, r, 'match row %s/%s spoke %d: change %s exact=%s; %d miss rows, %d with no change' % (L(w), L(s), i0, sorted(e.items(), key=str), ok, nm, nz)))
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
        rng.shuffle(links); nsub = int(OPT.get('f2bxsub', '3')); c2ok = True
        for lk in links[:nsub]:
            Py = {}
            for sv_t in itertools.product(LET, repeat=7):
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
                log('F2BX-SELFTEST (c2) d=7 link %s, all 5^7 apex words: %d admissible; thr %.6f: python %d rows above (%d with an extra rule firing), jsepf reported %d; missing %d, extra %d, max |dv| %.3g -> %s' % (
                    lk, len(Py), thr, len(want), nfire, len(rep), len(miss), len(extra_), dv, 'OK' if ok else 'FAIL'))
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
