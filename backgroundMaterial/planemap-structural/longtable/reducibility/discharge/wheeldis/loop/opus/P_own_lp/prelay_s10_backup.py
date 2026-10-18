# prelay.py (Opus P_own_lp, stage 8): 6-relay class R6x on top of L2 (spec in FINDINGS.md, stage 8).
# exec'd inside pcheck.py after psolve.py / pslite.py.
def c2(l): return 1 if l >= 7 else 0
def kg_of(n1, n2, n3, n4, n5):
    a = (n1, c2(n2), c2(n3), c2(n4), n5); return min(a, a[::-1])
def kh_of(L, j):
    a = tuple(L[(j + i) % 6] for i in range(6)); b = (a[0],) + tuple(reversed(a[1:])); return min(a, b)
def sig_of(U, wr, sr, sl, wl):
    a = (U, wr, sr, sl, wl); b = (U, wl, sl, sr, wr); return min(a, b)
def canon6(L):
    L = tuple(L); return min(min(s[k:] + s[:k] for k in range(6)) for s in (L, L[::-1]))
def relay_words():
    """canonical non-R6 6-words with at least one five"""
    out = set()
    for L in itertools.product(LET, repeat=6):
        if 5 not in L: continue
        c = canon6(L)
        if c in out: continue
        if not isR6(c): out.add(c)
    return sorted(out)
def cons_coef(L):
    cf = collections.Counter()
    for i in range(6):
        if L[i] == 5: cf[('g', kg_of(L[(i + 1) % 6], L[(i + 2) % 6], L[(i + 3) % 6], L[(i + 4) % 6], L[(i + 5) % 6]))] += 1
    for j in range(6):
        if L[j] >= 7: cf[('h', kh_of(L, j))] -= 1
    return cf
def R_sender_rows():
    out = []
    for w in SENDERS:
        n = 5; sixes = [k for k in range(n) if w[k] == 6]
        allow = {k: {(a_, q, b_) for a_ in LET for q in LET for b_ in LET if not isR6((5, w[(k + 1) % n], a_, q, b_, w[(k - 1) % n]))} for k in sixes}
        hats = sorted({h for k in sixes for h in (k, (k - 1) % n)}); seen = set()
        base = collections.Counter()
        for j in range(n):
            if w[j] >= 7: base[('y', root(list(w), j))] += 1
        for hb in itertools.product((0, 1), repeat=len(hats)):
            H = dict(zip(hats, hb))
            for fb in itertools.product((0, 1), repeat=len(sixes)):
                Fn = dict(zip(sixes, fb)); okc = True
                for k in sixes:
                    if not any((a_, q, b_) in allow[k] for a_ in CLS2[H[k]] for q in CLS2[Fn[k]] for b_ in CLS2[H[(k - 1) % n]]): okc = False; break
                if not okc: continue
                cf = collections.Counter(base)
                for k in sixes:   # (n1..n5) = (l_{k+1}, h_k, f_k, h_{k-1}, l_{k-1}); classes stand in for letters
                    a = (w[(k + 1) % n], H[k], Fn[k], H[(k - 1) % n], w[(k - 1) % n]); kg = min(a, a[::-1])
                    cf[('g', kg)] += 1
                k_ = tuple(sorted(cf.items()))
                if k_ not in seen: seen.add(k_); out.append((''.join(map(str, w)), dict(cf), list(hb) + ['|'] + list(fb)))
    return out
def relay_sigs(U, wr, sr, sl, wl):
    """candidate h keys into u through the link 6 with these window letters (p = the 6's private, free)"""
    return [kh_of((U, wr, sr, p, sl, wl), 0) for p in LET if not isR6((U, wr, sr, p, sl, wl))]
HV = {}
def window_table_R(U, y, x):
    W = window_table(U, y, x)          # y and x parts, R5/R6 -inf
    for b, e, q, r in itertools.product(range(5), repeat=4):
        cs = relay_sigs(U, LET[e], LET[r], LET[q], LET[b])
        if not cs: continue
        v = max(HV.get(k, 0.0) for k in cs)
        W[:, b, 1, e, :, :, q, r, :] += v
    return W
def recv_coef_R(d, lk, sv, xon):
    cy, cx = recv_coef(d, lk, sv, xon)
    cf = collections.Counter()
    for r_, c in cy.items(): cf[('y', r_)] += c
    for r_, c in cx.items():
        if c: cf[('x', r_)] += c
    U = min(d, 9); w = [int(ch) for ch in lk]; s = [int(ch) for ch in sv]
    for j in range(d):
        if w[j] == 6:
            wr, sr, sl, wl = w[(j + 1) % d], s[j], s[(j - 1) % d], w[(j - 1) % d]
            if relay_sigs(U, wr, sr, sl, wl): cf[('M', sig_of(U, wr, sr, sl, wl))] += 1
    return cf
def cmd_orientR():
    bad = 0; n = 0
    for a in itertools.product(LET, repeat=5):
        n += 1
        if kg_of(*a) != kg_of(*a[::-1]): bad += 1
        if sig_of(*a) != sig_of(a[0], a[4], a[3], a[2], a[1]): bad += 1
    for L in itertools.product(LET, repeat=6):
        for j in range(6):
            Lr = tuple(L[(j - i) % 6] for i in range(6))   # same 6, read the other way, n_j first
            if kh_of(L, j) != kh_of(Lr, 0): bad += 1
        if cons_coef(L) != cons_coef(canon6(L)): bad += 1
    log('orientation test R6x: %d + %d cases, %d mismatches' % (n, 5 ** 6, bad))
def cmd_solveR():
    import highspy
    load_patterns()
    xon = 'xon' in FLAGS; XCAP = float(OPT.get('xcap', '3')); XPEN = [float(OPT.get('xpen', '0'))]
    p = os.path.join(WORK, 'clsS_%d.bin' % int(xon))
    if not os.path.exists(p): class_table_S(xon).tofile(p)
    CLSFILE[0] = p
    K = int(OPT.get('K', '300')); MAXIT = int(OPT.get('maxit', '300')); TOL = float(OPT.get('tol', '1e-9'))
    h = highspy.Highs(); h.setOptionValue('output_flag', False); inf = highspy.kHighsInf
    cols = {}; names = []
    def col(key):
        if key not in cols:
            cols[key] = len(names); names.append(key)
            h.addVar(-inf if key[0] == 't' else 0.0, XCAP if key[0] == 'x' else inf)
            if key[0] == 'x' and XPEN[0]: h.changeColCost(cols[key], XPEN[0])
        return cols[key]
    jt = col(('t',)); h.changeColCost(jt, 1.0)
    for r_ in ROOTS: col(('y', r_))
    info = []; lo_, hi_ = [], []; have = set()
    def addrow(cf, lo, hi, inf_):
        idx = np.array([col(k) for k in cf], dtype=np.int32); val = np.array([float(v) for v in cf.values()])
        h.addRow(lo, hi, len(idx), idx, val); info.append(inf_); lo_.append(lo); hi_.append(hi)
    SR = R_sender_rows()
    for wd, cf, bits in SR:
        c2_ = dict(cf); c2_[('t',)] = 1.0; addrow(c2_, 1.0, inf, ('senderR', wd, bits))
    RW = relay_words(); ncons = 0
    for L in RW:
        cf = {k: v for k, v in cons_coef(L).items() if v}
        if any(k[0] == 'g' for k in cf): addrow(cf, 0.0, 0.0, ('cons', list(L))); ncons += 1
    sigs = set()
    for U in BIGL:
        for wr, sr, sl, wl in itertools.product(LET, repeat=4):
            cs = relay_sigs(U, wr, sr, sl, wl)
            if cs: sigs.add((sig_of(U, wr, sr, sl, wl), tuple(sorted(set(cs)))))
    nm = 0; SIGK = {}
    for sg, cs in sorted(sigs):
        SIGK[sg] = cs
        for k in cs: addrow({('h', k): 1.0, ('M', sg): -1.0}, -inf, 0.0, ('mrowR', list(sg), list(k))); nm += 1
    ng = sum(1 for k in cols if k[0] == 'g'); nh = sum(1 for k in cols if k[0] == 'h')
    log('R6x: %d sender rows, %d g, %d h, %d conservation rows (of %d non-R6 words), %d signatures, %d M rows' % (len(SR), ng, nh, ncons, len(RW), len(SIGK), nm))
    def recv(d, lk, sv):
        cf = recv_coef_R(d, lk, sv, xon)
        key = (d, tuple(sorted(cf.items(), key=str)))
        if key in have: return False
        have.add(key); c2_ = dict(cf); c2_[('t',)] = -1.0
        addrow(c2_, -inf, d - 6.0, ('receiverR', d, lk, sv)); return True
    if 'warm' in OPT:
        nw = 0
        for fn in OPT['warm'].split(','):
            for line in open(fn):
                m = re.match(r'^R (\d+) (\d+) (\d+)', line)
                if m and admissible(int(m.group(1)), m.group(2), m.group(3)) is None: nw += recv(int(m.group(1)), m.group(2), m.group(3))
        log('warm rows admitted: %d' % nw)
    T0 = time.time(); rowlog = open(os.path.join(HERE, 'rows_%s.txt' % OPT.get('tag', 'run')), 'w')
    for it in range(MAXIT):
        t1 = time.time(); h.run(); xv = np.array(h.getSolution().col_value); t = xv[jt]
        y = np.array([xv[cols[('y', r_)]] for r_ in ROOTS])
        HV.clear()
        for k, i in cols.items():
            if k[0] == 'h': HV[k[1]] = xv[i]
        xd = {k[1]: xv[i] for k, i in cols.items() if k[0] == 'x' and xv[i] > 1e-12}
        tlp = time.time() - t1; added = 0; per = {}; Wc = {}
        for d in range(7, DMAX + 1):
            U = min(d, 9)
            if U not in Wc: Wc[U] = window_table_R(U, y, xd)
            rr, dt, ni = run_sep(d, Wc[U], d - 6 + t + TOL, K, 2)
            n = 0; mx = None
            for r_ in rr:
                if r_[0] == 'V':
                    mx = max(mx or -1e9, float(r_[1]) - (d - 6 + t))
                    if 'dbg' in FLAGS and n == 0:
                        cf = recv_coef_R(d, r_[2], r_[3], xon)
                        val = sum(v * (max(HV.get(kk, 0.0) for kk in SIGK[k[1]]) if k[0] == 'M' else xv[cols[k]] if k in cols else 0) for k, v in cf.items())
                        log('  DBG d=%d sep %s row %.9f' % (d, r_[1], val))
                    if recv(d, r_[2], r_[3]): n += 1; rowlog.write('R %d %s %s\n' % (d, r_[2], r_[3]))
            added += n; per[d] = (n, None if mx is None else round(mx, 6), round(dt, 1))
        if not added:
            W9 = Wc.get(9); Mr = relaxed_M(W9)
            for d in range(DMAX + 1, DTAIL + 1):
                if closed_max(Mr, d) <= d - 6 + t + TOL: continue
                rr, dt, ni = run_sep(d, W9, d - 6 + t + TOL, K, 2, pats=False); n = 0
                for r_ in rr:
                    if r_[0] == 'V' and recv(d, r_[2], r_[3]): n += 1; rowlog.write('R %d %s %s\n' % (d, r_[2], r_[3]))
                added += n; per[d] = (n, 'tail', round(dt, 1))
            lam = karp(Mr); log('  Karp lambda %.6f d0 %.2f' % (lam, (6 - t) / (1 - lam) if lam < 1 else 1e9))
        rowlog.flush()
        log('iter %d t=%.12f rows %d cols %d added %d  lp %.1fs total %.0fs  %s' % (it, t, h.getNumRow(), h.getNumCol(), added, tlp, time.time() - T0, {d: v for d, v in per.items() if v[0]}))
        if not added and XPEN[0]:
            XPEN[0] = 0.0
            for k, i in cols.items():
                if k[0] == 'x': h.changeColCost(i, 0.0)
            log('  converged with x penalty; penalty removed, continuing'); continue
        if not added: break
    sol = h.getSolution(); xv = np.array(sol.col_value); t = xv[jt]; duals = np.array(sol.row_dual)
    tag = OPT.get('tag', 'run')
    S = {'t': float(t), 'model': 'R6x', 'xon': xon,
         'y': {rname(k[1]): float(xv[i]) for k, i in cols.items() if k[0] == 'y' and xv[i] > 0},
         'g': [[list(k[1]), float(xv[i])] for k, i in cols.items() if k[0] == 'g' and xv[i] > 0],
         'h': [[list(k[1]), float(xv[i])] for k, i in cols.items() if k[0] == 'h' and xv[i] > 0],
         'x': {str(k[1]): float(xv[i]) for k, i in cols.items() if k[0] == 'x' and xv[i] > 0}}
    json.dump(S, open(os.path.join(HERE, 'sol_%s.json' % tag), 'w'))
    cert = [{'w': float(dv), 'row': info[i]} for i, dv in enumerate(duals) if abs(dv) > 1e-11]
    json.dump(cert, open(os.path.join(HERE, 'cert_%s.json' % tag), 'w'), indent=0)
    log('LP t* = %.12f ; dual rows %d ; wrote sol_%s.json cert_%s.json' % (t, len(cert), tag, tag))
    for c in sorted(cert, key=lambda c: -abs(c['w'])):
        if c['row'][0] in ('senderR', 'receiverR'): log('  %+.9f %s' % (c['w'], ' '.join(map(str, c['row'][:4]))))
    log('  (+ %d cons / mrow rows)' % sum(1 for c in cert if c['row'][0] in ('cons', 'mrowR')))

def cmd_lowerR():
    """exact check from signed duals: rows re-derived from labels; y rationalised, rescaled so t's reduced cost is 0;
    every other reduced cost >= 0 (vars >= 0), x priced at its cap if negative; bound = dual objective."""
    load_patterns()
    xon = 'xon' in FLAGS; XCAP = Fraction(OPT.get('xcap', '3')); C = json.load(open(OPT['cert']))
    SR = {(wd, tuple(map(str, b))): cf for wd, cf, b in R_sender_rows()}
    tot = collections.defaultdict(Fraction); D = Fraction(0); ok = True; tco = Fraction(0)
    for c in C:
        w = Fraction(c['w']).limit_denominator(10 ** 7); row = c['row']
        if row[0] == 'senderR':
            cf = SR.get((row[1], tuple(map(str, row[2]))))
            if cf is None: log('  NOT A SENDER ROW', row); ok = False; continue
            if w < 0: log('  WRONG SIGN', row); ok = False; continue
            for k, v in cf.items(): tot[k] += w * v
            tco += w; D += w * 1
        elif row[0] == 'cons':
            L = tuple(row[1])
            if isR6(L) or canon6(L) != L: log('  BAD CONS', row); ok = False; continue
            for k, v in cons_coef(L).items(): tot[k] += w * v
        elif row[0] == 'mrowR':
            sg = tuple(row[1]); k = tuple(row[2])
            U, wr, sr, sl, wl = sg
            if k not in relay_sigs(U, wr, sr, sl, wl) and k not in relay_sigs(U, wl, sl, sr, wr): log('  BAD MROW', row); ok = False; continue
            if w > 0: log('  WRONG SIGN', row); ok = False; continue
            tot[('h', k)] += w; tot[('M', sg)] -= w
        elif row[0] == 'receiverR':
            d, lk, sv = int(row[1]), row[2], row[3]
            why = admissible(d, lk, sv)
            if why: log('  RECEIVER NOT ADMISSIBLE', row, why); ok = False; continue
            if w > 0: log('  WRONG SIGN', row); ok = False; continue
            for k, v in recv_coef_R(d, lk, sv, xon).items(): tot[k] += w * v
            tco -= w; D += w * (d - 6)
        else: log('  UNKNOWN', row); ok = False
    # reduced cost of var j: c_j - sum_i w_i A_ij ; t: 1 - tco must be 0 after rescale
    if tco <= 0: log('  t coefficient sum not positive'); ok = False; tco = Fraction(1)
    D = D / tco; neg = []
    for k, v in tot.items():
        rc = -v / tco
        if rc < 0:
            if k[0] == 'x': D += rc * XCAP
            else: neg.append((k, rc))
    if neg: log('  negative reduced costs:', len(neg), neg[:5]); ok = False
    log('LOWER-R: %s  t >= %s = %.9f  (%d rows)' % ('VALID' if ok else 'INVALID', D, float(D), len(C)))

def cmd_upperR():
    load_patterns()
    Sj = json.load(open(OPT['sol'])); t = Sj['t']
    y = np.zeros(len(ROOTS))
    for k, v in Sj['y'].items():
        u, rest = k.split('|'); r_ = root(list((int(u),) + tuple(int(c) for c in rest)), 0); y[RIX[r_]] = v
    G = {tuple(k): v for k, v in Sj['g']}; HV.clear(); HV.update({tuple(k): v for k, v in Sj['h']})
    xd = {int(k): v for k, v in Sj.get('x', {}).items()}
    bad = 0
    for wd, cf, bits in R_sender_rows():
        v = sum(c * (y[RIX[k[1]]] if k[0] == 'y' else G.get(k[1], 0.0)) for k, c in cf.items())
        if v < 1 - t - EPS: bad += 1
    log('sender rows violated: %d' % bad)
    nc = 0
    for L in relay_words():
        cf = cons_coef(L); v = sum(c * (G.get(k[1], 0.0) if k[0] == 'g' else HV.get(k[1], 0.0)) for k, c in cf.items())
        if v > 1e-9: nc += 1          # receives more than it passes on (passing more is impossible: h >= 0 only cancels g)
        if v < -1e-9: nc += 1
    log('conservation violated (|in - out| > 1e-9): %d' % nc); bad += nc
    for d in range(7, DMAX + 1):
        W = window_table_R(min(d, 9), y, xd)
        res, dt, ni = run_sep(d, W, d - 6 + t + EPS, 20, 0)
        v = [r for r in res if r[0] == 'V']; bad += len(v)
        log('d=%d: %d violated (exhaustive, %.1fs)' % (d, len(v), dt))
    W9 = window_table_R(9, y, xd); M = relaxed_M(W9)
    for d in range(DMAX + 1, DTAIL + 1):
        v = closed_max(M, d)
        if v > d - 6 + t + EPS:
            res, dt, ni = run_sep(d, W9, d - 6 + t + EPS, 20, 0, pats=False); nv = sum(1 for r in res if r[0] == 'V'); bad += nv
            log('d=%d relaxed %.6f > cap; exact pattern-free: %d violated' % (d, v, nv))
    lam = karp(M); d0 = (6 - t) / (1 - lam) if lam < 1 else 1e9
    log('Karp lambda %.9f d0 %.3f' % (lam, d0))
    if d0 > DTAIL + 1: bad += 1
    log('UPPER-R: %s at t = %.12f' % ('FEASIBLE' if bad == 0 else 'INFEASIBLE (%d)' % bad, t))
