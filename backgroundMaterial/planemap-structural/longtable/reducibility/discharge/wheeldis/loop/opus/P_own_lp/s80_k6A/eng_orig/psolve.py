# psolve.py (Opus P_own_lp): row-generation LP with jsep3 mode 2 (K most violated distinct rows per d), highspy
# incremental warm-started re-solves.  exec'd inside pcheck.py (shares its model: ROOTS, senders, window_table, ...).
CLSFILE = [None]
def class_table(xon):
    """int32 class id per 5^9 window index (a,b,c,e,f,p,q,r,s): 0 = no coefficient; else c and the letters read."""
    g = np.indices((5,) * 9, dtype=np.int64)
    a, b, c, e, f, p, q, r, s_ = g
    five = (((b * 5 + e) * 5 + q) * 5 + r) + 1
    big = ((((((a * 5 + b) * 5 + e) * 5 + f) * 5 + q) * 5 + r) + 1) + 625 + c * 15625
    C = np.where(c == 0, five, 0)
    if xon: C = np.where(c >= 2, big, C)
    return C.astype(np.int32)
def write_cls(xon):
    p = os.path.join(WORK, 'cls_%d.bin' % int(bool(xon)))
    if not os.path.exists(p): class_table(xon).tofile(p)
    CLSFILE[0] = p
def cmd_solve2():
    import highspy
    load_patterns()
    xon = 'xon' in FLAGS; XCAP = float(OPT.get('xcap', '3')); XPEN = [float(OPT.get('xpen', '0'))]
    write_cls(xon)
    K = int(OPT.get('K', '300')); MAXIT = int(OPT.get('maxit', '200')); TOL = float(OPT.get('tol', '1e-9'))
    h = highspy.Highs(); h.setOptionValue('output_flag', False)
    inf = highspy.kHighsInf
    cols = {}; names = []
    def col(key, lo, hi):
        if key not in cols:
            cols[key] = len(names); names.append(key); h.addVar(lo, hi)
            if key[0] == 'x' and XPEN[0]: h.changeColCost(cols[key], XPEN[0])
        return cols[key]
    jt = col(('t',), -inf, inf); h.changeColCost(jt, 1.0)
    for r in ROOTS: col(('y', r), 0.0, inf)
    info = []; have = set()
    def addrow(coef, lo, hi, inf_):
        idx = np.array([col(k, 0.0, (XCAP if k[0] == 'x' else inf)) for k in coef], dtype=np.int32)
        val = np.array(list(coef.values()), dtype=np.float64)
        h.addRow(lo, hi, len(idx), idx, val); info.append(inf_)
    for w in SENDERS:   # sum y + t >= 1
        cf = {('t',): 1.0}
        for r, c in sender_coef(w).items(): cf[('y', r)] = float(c)
        addrow(cf, 1.0, inf, ('sender', ''.join(map(str, w))))
    def recv(d, lk, sv):
        cy, cx = recv_coef(d, lk, sv, xon)
        key = (d, tuple(sorted(cy.items())), tuple(sorted((k, v) for k, v in cx.items() if v)))
        if key in have: return False
        have.add(key); cf = {('t',): -1.0}
        for r, c in cy.items(): cf[('y', r)] = float(c)
        for r, c in cx.items():
            if c: cf[('x', r)] = float(c)
        addrow(cf, -inf, d - 6.0, ('receiver', d, lk, sv)); return True
    nw = 0
    if 'warm' in OPT:
        for fn in OPT['warm'].split(','):
            for line in open(fn):
                m = re.search(r'receiver d=(\d+) link (\d+) s (\d+)', line) or re.match(r'^R (\d+) (\d+) (\d+)', line)
                if m and int(m.group(1)) <= DTAIL and admissible(int(m.group(1)), m.group(2), m.group(3)) is None:
                    nw += recv(int(m.group(1)), m.group(2), m.group(3))
        log('warm rows admitted: %d' % nw)
    T0 = time.time(); hist = []
    rowlog = open(os.path.join(HERE, 'rows_%s.txt' % OPT.get('tag', 'run')), 'w')
    for it in range(MAXIT):
        t1 = time.time(); h.run()
        sol = h.getSolution(); xv = np.array(sol.col_value); t = xv[jt]
        y = np.array([xv[cols[('y', r)]] for r in ROOTS])
        xd = {k[1]: xv[i] for k, i in cols.items() if k[0] == 'x' and xv[i] > 1e-12}
        tlp = time.time() - t1; added = 0; per = {}
        Wc = {}
        for d in range(7, DMAX + 1):
            U = min(d, 9)
            if U not in Wc: Wc[U] = window_table(U, y, xd)
            rr, dt, ni = run_sep(d, Wc[U], d - 6 + t + TOL, K, 2)
            n = 0; mx = None
            for r_ in rr:
                if r_[0] == 'V':
                    mx = max(mx or -1e9, float(r_[1]) - (d - 6 + t))
                    if recv(d, r_[2], r_[3]): n += 1; rowlog.write('R %d %s %s\n' % (d, r_[2], r_[3]))
            added += n; per[d] = (n, mx, round(dt, 1))
        if not added or 'tailall' in FLAGS:   # d > DMAX: relaxed DP, exact pattern-free separation where it fails
            W9 = Wc.get(9); Mr = relaxed_M(W9)
            for d in range(DMAX + 1, DTAIL + 1):
                if closed_max(Mr, d) <= d - 6 + t + TOL: continue
                rr, dt, ni = run_sep(d, W9, d - 6 + t + TOL, K, 2, pats=False); n = 0
                for r_ in rr:
                    if r_[0] == 'V' and recv(d, r_[2], r_[3]): n += 1; rowlog.write('R %d %s %s\n' % (d, r_[2], r_[3]))
                added += n; per[d] = (n, 'tail', round(dt, 1))
            lam = karp(Mr); log('  Karp lambda %.6f d0 %.2f' % (lam, (6 - t) / (1 - lam) if lam < 1 else 1e9))
        rowlog.flush()
        log('iter %d t=%.12f rows %d cols %d added %d  lp %.1fs sep %.1fs total %.0fs  %s' % (
            it, t, h.getNumRow(), h.getNumCol(), added, tlp, time.time() - t1 - tlp, time.time() - T0,
            {d: v for d, v in per.items() if v[0]}))
        if not added and XPEN[0]:
            XPEN[0] = 0.0
            for k, i in cols.items():
                if k[0] == 'x': h.changeColCost(i, 0.0)
            log('  converged with x penalty; penalty removed, continuing'); continue
        if not added: break
    sol = h.getSolution(); xv = np.array(sol.col_value); t = xv[jt]; duals = np.array(sol.row_dual)
    tag = OPT.get('tag', 'run')
    S = {'t': float(t), 'z9': 0.0, 'y': {rname(k[1]): float(xv[i]) for k, i in cols.items() if k[0] == 'y' and xv[i] > 0},
         'x': {str(k[1]): float(xv[i]) for k, i in cols.items() if k[0] == 'x' and xv[i] > 0}}
    json.dump(S, open(os.path.join(HERE, 'sol_%s.json' % tag), 'w'))
    cert = []
    for i, dv in enumerate(duals):
        if abs(dv) > 1e-10: cert.append({'w': float(abs(dv)), 'row': list(info[i])})
    cd = np.array(sol.col_dual)
    for i in range(len(names)):
        if names[i][0] == 'x' and abs(cd[i]) > 1e-10: cert.append({'w': float(abs(cd[i])), 'row': ['xcap', names[i][1]]})
    json.dump(cert, open(os.path.join(HERE, 'cert_%s.json' % tag), 'w'), indent=0); bnd = [(names[i], cd[i]) for i in range(len(names)) if abs(cd[i]) > 1e-10 and names[i][0] != 't']
    log('LP t* = %.12f ; dual rows %d ; bound duals %d %s ; wrote sol_%s.json cert_%s.json' % (t, len(cert), len(bnd), bnd[:8], tag, tag))
    for c in sorted(cert, key=lambda c: -c['w']): log('  %.9f %s' % (c['w'], ' '.join(map(str, c['row']))))

# ---------------- rule T (option B, side fixed with tkey) ----------------
def class_table_T(xon):
    g = np.indices((5,) * 9, dtype=np.int64)
    a, b, c, e, f, p, q, r, s_ = g
    full = (((((a * 5 + b) * 5 + e) * 5 + f) * 5 + q) * 5 + r)
    C = np.where(c == 0, 1 + full, 0)
    infl = (r == 0) & (((c == 1) & (e >= 2)) | ((c >= 2) & (e == 1)))
    if xon: C = np.where(c >= 2, 1 + 15625 * c + full, C); C = np.where((c == 1) & infl, 1 + 15625 + e * 5 + r, C)
    else: C = np.where((c >= 1) & infl, 1 + 15625 * c + e * 5 + r, C)
    return C.astype(np.int32)
def T_sender_rows():
    """option-B sender rows: list of (word, {('Y',key) or ('T',key): coef}) over admissible flag assignments"""
    out = []
    for w in SENDERS:
        n = 5; sixes = [k for k in range(n) if w[k] == 6]; zs = {}
        for k in sixes:
            for dr in (1, -1):
                if w[(k + dr) % n] >= 7: zs[(k, dr)] = None
        keys = sorted(zs); seen = set()
        for bits in itertools.product((0, 1), repeat=len(keys)):
            Z = dict(zip(keys, bits)); okc = True
            for k in sixes:
                zr = Z.get((k, 1)); zl = Z.get((k, -1))
                cand = lambda f: LET if f is None else (BIGL if f else (5, 6))
                if all(isR6((5, w[(k + 1) % n], a_, q, b_, w[(k - 1) % n])) for a_ in cand(zr) for b_ in cand(zl) for q in LET): okc = False; break
            if not okc: continue
            cf = collections.Counter()
            for j in range(n):
                if w[j] < 7: continue
                raw = tuple(w[(j + i) % n] for i in range(5)); ka, ke = (j + 1) % n, (j - 1) % n
                fa = Z.get((ka, -1), 0) if w[ka] == 6 else 0; fe = Z.get((ke, 1), 0) if w[ke] == 6 else 0
                cf[('Y', ykey(raw, fa, fe))] += 1
                if fa: cf[('T', tkey(raw, fa, fe, 'a'))] += 1
                if fe: cf[('T', tkey(raw, fa, fe, 'e'))] += 1
            k_ = tuple(sorted(cf.items()))
            if k_ not in seen: seen.add(k_); out.append((''.join(map(str, w)), dict(cf), bits))
    return out
TCAND = {}
def tcands(b):
    if b not in TCAND:
        s = []
        for p, m, o in itertools.product(LET, repeat=3):
            if isR5((b, 6, p, m, o)): continue
            for fe in ((0, 1) if o == 6 else (0,)):
                k = tkey((b, 6, p, m, o), 1, fe, 'a')
                if k not in s: s.append(k)
        TCAND[b] = s
    return TCAND[b]
def recv_coef_T(d, lk, sv, xon, TV):
    U = min(d, 9); w = [int(c) for c in lk]; s = [int(c) for c in sv]
    cf = collections.Counter()
    for i in range(d):
        if w[i] == 5:
            wd = (U, w[(i + 1) % d], s[i], s[(i - 1) % d], w[(i - 1) % d])
            fa = int(w[(i + 1) % d] == 6 and w[(i + 2) % d] >= 7); fe = int(w[(i - 1) % d] == 6 and w[(i - 2) % d] >= 7)
            cf[('Y', ykey(wd, fa, fe))] += 1
        if s[i] == 5:
            p_, q_ = w[i], w[(i + 1) % d]; b = p_ if (p_ >= 7 and q_ == 6) else (q_ if (p_ == 6 and q_ >= 7) else None)
            if b is not None and any(('T', k) in TV for k in tcands(b)): cf[('M', b)] += 1
    if xon:
        _, cx = recv_coef(d, lk, sv, True)
        for k, v in cx.items():
            if v: cf[('x', k)] += v
    return cf
def cmd_solveT():
    import highspy
    global TMODE
    load_patterns()
    xon = 'xon' in FLAGS; XCAP = float(OPT.get('xcap', '3')); XPEN = [float(OPT.get('xpen', '0'))]
    p = os.path.join(WORK, 'clsT_%d.bin' % int(xon))
    if not os.path.exists(p): class_table_T(xon).tofile(p)
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
    info = []; have = set()
    def addrow(cf, lo, hi, inf_):
        idx = np.array([col(k) for k in cf], dtype=np.int32); val = np.array([float(v) for v in cf.values()])
        h.addRow(lo, hi, len(idx), idx, val); info.append(inf_)
    SR = T_sender_rows()
    for wd, cf, bits in SR:
        c2 = dict(cf); c2[('t',)] = 1.0; addrow(c2, 1.0, inf, ('senderT', wd, list(bits)))
    nY = sum(1 for k in cols if k[0] == 'Y'); nT = sum(1 for k in cols if k[0] == 'T')
    log('rule T: %d sender rows, %d Y, %d T' % (len(SR), nY, nT))
    TV = {k: 0.0 for k in cols if k[0] == 'T'}
    nm = 0
    for b in BIGL:
        for k in tcands(b):
            if ('T', k) in TV: addrow({('T', k): 1.0, ('M', b): -1.0}, -inf, 0.0, ('mrow', b, [list(k[0])] + list(k[1:]))); nm += 1
    log('M rows (T[k] <= M_b, b = 7, 8, 9): %d' % nm)
    def recv(d, lk, sv):
        cf = recv_coef_T(d, lk, sv, xon, TV)
        key = (d, tuple(sorted(cf.items())))
        if key in have: return False
        have.add(key); c2 = dict(cf); c2[('t',)] = -1.0
        addrow(c2, -inf, d - 6.0, ('receiverT', d, lk, sv)); return True
    if 'warm' in OPT:
        nw = 0
        for fn in OPT['warm'].split(','):
            for line in open(fn):
                m = re.search(r'receiver d=(\d+) link (\d+) s (\d+)', line) or re.match(r'^R (\d+) (\d+) (\d+)', line)
                if m and int(m.group(1)) <= DTAIL and admissible(int(m.group(1)), m.group(2), m.group(3)) is None:
                    nw += recv(int(m.group(1)), m.group(2), m.group(3))
        log('warm rows admitted: %d' % nw)
    TMODE = True; T0 = time.time()
    rowlog = open(os.path.join(HERE, 'rows_%s.txt' % OPT.get('tag', 'run')), 'w')
    def current():
        sol = h.getSolution(); xv = np.array(sol.col_value)
        YT.clear(); TT.clear()
        for k, i in cols.items():
            if k[0] == 'Y': YT[k[1]] = xv[i]
            elif k[0] == 'T': TT[k[1]] = xv[i]; TV[k] = xv[i]
        xd = {k[1]: xv[i] for k, i in cols.items() if k[0] == 'x' and xv[i] > 1e-12}
        return xv[jt], xd, xv
    for it in range(MAXIT):
        t1 = time.time(); h.run(); t, xd, xv = current(); tlp = time.time() - t1
        added = 0; per = {}; Wc = {}
        for d in range(7, DMAX + 1):
            U = min(d, 9)
            if U not in Wc: Wc[U] = window_table(U, None, xd)
            rr, dt, ni = run_sep(d, Wc[U], d - 6 + t + TOL, K, 2)
            n = 0; mx = None
            for r_ in rr:
                if r_[0] == 'V':
                    mx = max(mx or -1e9, float(r_[1]) - (d - 6 + t))
                    if 'dbg' in FLAGS and n == 0 and d == 7:
                        cf = recv_coef_T(d, r_[2], r_[3], xon, TV)
                        val = sum(v * xv[cols[k]] for k, v in cf.items() if k in cols)
                        log('  DBG sep %s row %.9f %s %s %s' % (r_[1], val, r_[2], r_[3], sorted((k, v, round(xv[cols[k]], 4) if k in cols else None) for k, v in cf.items())))
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
    fmtY = lambda k: '%s|%d%d' % (''.join(map(str, k[0])), k[1], k[2])
    fmtT = lambda k: '%s|%d%d%s' % (''.join(map(str, k[0])), k[1], k[2], k[3])
    S = {'t': float(t), 'z9': 0.0, 'y': {},
         'yT': {fmtY(k[1]): float(xv[i]) for k, i in cols.items() if k[0] == 'Y' and xv[i] > 0},
         'tau': {fmtT(k[1]): float(xv[i]) for k, i in cols.items() if k[0] == 'T' and xv[i] > 0},
         'x': {str(k[1]): float(xv[i]) for k, i in cols.items() if k[0] == 'x' and xv[i] > 0}}
    json.dump(S, open(os.path.join(HERE, 'sol_%s.json' % tag), 'w'))
    cert = []
    for i, dv in enumerate(duals):
        if abs(dv) > 1e-10: cert.append({'w': float(abs(dv)), 'row': info[i]})
    cd = np.array(sol.col_dual)
    for i in range(len(names)):
        if names[i][0] == 'x' and abs(cd[i]) > 1e-10: cert.append({'w': float(abs(cd[i])), 'row': ['xcap', names[i][1]]})
        elif names[i][0] in 'YT' and cd[i] < -1e-10: log('  WARNING upper-bound dual on', names[i])
    json.dump(cert, open(os.path.join(HERE, 'cert_%s.json' % tag), 'w'), indent=0)
    log('LP t* = %.12f ; dual rows %d ; wrote sol_%s.json cert_%s.json' % (t, len(cert), tag, tag))
    for c in sorted(cert, key=lambda c: -c['w']): log('  %.9f %s' % (c['w'], ' '.join(map(str, c['row'][:4]))))

def cmd_lowerT():
    """exact check of a rule-T (+x) dual certificate: senderT rows re-derived from (word, flag bits); receiverT rows:
    admissible, Y/x coefficients re-derived, each listed T key a valid inflow candidate of a distinct inflow slot."""
    load_patterns()
    xon = 'xon' in FLAGS; XCAP = Fraction(OPT.get('xcap', '3'))
    C = json.load(open(OPT['cert'])); SR = {}; TVALL = {}
    for wd, cf, bits in T_sender_rows():
        SR[(wd, tuple(bits))] = cf
        for k in cf:
            if k[0] == 'T': TVALL[k] = 1
    tot = collections.defaultdict(Fraction); sw = Fraction(0); rhs = Fraction(0); ok = True
    for c in C:
        w = Fraction(c['w']).limit_denominator(10 ** 6); row = c['row']
        if row[0] == 'xcap':
            tot[('x', row[1])] += w; rhs += w * XCAP; continue
        if row[0] == 'sender':
            wd = tuple(int(ch) for ch in row[1])
            if wd not in SENDERS: log('  NOT A SENDER', row); ok = False; continue
            for r, k in sender_coef(wd).items(): tot[('y', r)] -= w * k
            rhs -= w; sw += w; continue
        if row[0] == 'receiver':
            d, lk, sv = int(row[1]), row[2], row[3]
            why = admissible(d, lk, sv)
            if why: log('  RECEIVER NOT ADMISSIBLE', row, why); ok = False; continue
            cy, cx = recv_coef(d, lk, sv, xon)
            for r, k in cy.items(): tot[('y', r)] += w * k
            for r, k in cx.items(): tot[('x', r)] += w * k
            rhs += w * (d - 6); sw += w; continue
        if row[0] == 'senderT':
            cf = SR.get((row[1], tuple(row[2])))
            if cf is None: log('  NOT A SENDER ROW', row); ok = False; continue
            for k, v in cf.items(): tot[k] -= w * v
            rhs -= w; sw += w; continue
        if row[0] == 'mrow':
            b = int(row[1]); k = (tuple(row[2][0]), row[2][1], row[2][2], row[2][3])
            if k not in tcands(b): log('  MROW KEY NOT A CANDIDATE', row); ok = False; continue
            tot[('T', k)] += w; tot[('M', b)] -= w; continue
        d, lk, sv = int(row[1]), row[2], row[3]
        why = admissible(d, lk, sv)
        if why: log('  RECEIVER NOT ADMISSIBLE', row[:4], why); ok = False; continue
        cf = recv_coef_T(d, lk, sv, xon, TVALL)
        for k, v in cf.items(): tot[k] += w * v
        rhs += w * (d - 6); sw += w
        continue
        tl = []
        why = admissible(d, lk, sv)
        if why: log('  RECEIVER NOT ADMISSIBLE', row[:4], why); ok = False; continue
        cf = recv_coef_T(d, lk, sv, xon, {})          # Y and x part (no T var known -> no T)
        U = min(d, 9); wv = [int(ch) for ch in lk]; svv = [int(ch) for ch in sv]
        slots = collections.Counter()
        for i in range(d):
            if svv[i] == 5:
                p_, q_ = wv[i], wv[(i + 1) % d]
                b = p_ if (p_ >= 7 and q_ == 6) else (q_ if (p_ == 6 and q_ >= 7) else None)
                if b is not None: slots[b] += 1
        used = collections.Counter()
        for e in tl:
            k = (tuple(e[0]), e[1], e[2], e[3]); n = e[4]
            bs = [b for b in slots if k in tcands(b)]
            if len(bs) != 1: log('  T KEY NOT A CANDIDATE', row[:4], k); ok = False
            else: used[bs[0]] += n
            tot[('T', k)] += w * n
        if any(used[b] > slots[b] for b in used): log('  TOO MANY T KEYS', row[:4]); ok = False
        for k, v in cf.items(): tot[k] += w * v
        rhs += w * (d - 6); sw += w
    neg = {k: v for k, v in tot.items() if v < 0}
    if neg: log('  negative combined coefficients:', len(neg), list(neg.items())[:5]); ok = False
    t0 = -rhs / sw
    log('LOWER-T: %s  t >= %s = %.9f  (%d rows, sum of weights %s)' % ('VALID' if ok else 'INVALID', t0, float(t0), len(C), sw))
