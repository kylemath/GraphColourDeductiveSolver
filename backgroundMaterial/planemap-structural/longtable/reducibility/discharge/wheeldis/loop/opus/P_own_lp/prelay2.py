# prelay2.py (Opus P_own_lp, stage 12): 6-centred relay R6x2 (spec in FINDINGS.md stage 12).  exec'd in pcheck.py.
AP = 'noapex' not in FLAGS          # validation V1: noapex = s10's class
AC = 'apexcls' in FLAGS             # reduced s12: apex letters read only as small (5) / big (7) witnesses
def ap(x): return (7 if x >= 7 else 5) if AC else x
ZH = 'zh' in FLAGS                   # stage 13 (R7h): big-centred split, z[five link from the big, hat classes on both sides]
ZV = {}
Q7 = 'q7' in FLAGS                   # stage 14 (R77): big -> adjacent 7 inflow q[the 7's whole link, read from the sender]
QV = {}
def qkey(m):
    m = tuple(m); return min(m, (m[0],) + tuple(reversed(m[1:])))
def q7sig(U, a, b, c, e):
    x = (U, a, b, c, e); return min(x, (U, e, c, b, a))
def q7keys(sg):
    U, a, b, c, e = sg
    return sorted({qkey((U, a, b, p1, p2, c, e)) for p1 in LET for p2 in LET if ''.join(map(str, canon((U, a, b, p1, p2, c, e)))) not in RBIG})
def q7_inflow(w):
    """coefficient dict of q keys flowing into a 7 with link w (d = 7)"""
    cf = collections.Counter()
    for j in range(7):
        if w[j] >= 7: cf[qkey(tuple(w[(j + i) % 7] for i in range(7)))] += 1
    return cf
_L7 = []
def write_bonus():
    if not _L7:
        seen = set()
        for w in itertools.product(LET, repeat=7):
            c = canon(w)
            if c not in seen: seen.add(c); _L7.append(c)
    fn = os.path.join(WORK, 'bonus7.txt'); n = 0
    with open(fn, 'w') as f:
        for c in _L7:
            v = sum(m * QV.get(k, 0.0) for k, m in q7_inflow(c).items())
            if v > 0: f.write('%s %.15f\n' % (''.join(map(str, c)), v)); n += 1
    BONUSF[0] = fn if n else None
    return n
def zkey(n, hr, hl):
    """n = (U, n1, n2, n3, n4) the five's link read from the big U (n1 = next spoke); hr = class of the hat between U and n1,
    hl = class of the hat between U and n4 (0 small / 1 big)"""
    a = tuple(n) + (hr, hl); b = (n[0], n[4], n[3], n[2], n[1], hl, hr); return min(a, b)
def g2_of(n1, n2, n3, n4, n5, ar, al):
    ar, al = ap(ar), ap(al)
    a = (n1, c2(n2), c2(n3), c2(n4), n5) + ((ar, al) if AP else ())
    b = (n5, c2(n4), c2(n3), c2(n2), n1) + ((al, ar) if AP else ())
    return min(a, b)
def h2_of(m, ar, al):
    """m = the 6's link rotated to start at the big; ar = apex beyond (m0, m1), al = apex beyond (m5, m0)"""
    ar, al = ap(ar), ap(al)
    a = tuple(m) + ((ar, al) if AP else ()); b = (m[0],) + tuple(reversed(m[1:])) + ((al, ar) if AP else ())
    return min(a, b)
def sig2_of(U, wr, sr, sl, wl, wrr, wll):
    wrr, wll = ap(wrr), ap(wll)
    a = (U, wr, sr, sl, wl) + ((wrr, wll) if AP else ()); b = (U, wl, sl, sr, wr) + ((wll, wrr) if AP else ())
    return min(a, b)
def sig2_keys(sig):
    U, wr, sr, sl, wl = sig[:5]; wrr, wll = (sig[5], sig[6]) if AP else (0, 0)
    return sorted({h2_of((U, wr, sr, p, sl, wl), wrr, wll) for p in LET if not isR6((U, wr, sr, p, sl, wl))})
def R2_sender_rows():
    out = []
    for w in SENDERS:
        n = 5; sixes = [k for k in range(n) if w[k] == 6]
        allow = {k: {(a_, q, b_) for a_ in LET for q in LET for b_ in LET if not isR6((5, w[(k + 1) % n], a_, q, b_, w[(k - 1) % n]))} for k in sixes}
        bigs = [j for j in range(n) if w[j] >= 7] if ZH else []
        hats = sorted({h for k in sixes + bigs for h in (k, (k - 1) % n)}); seen = set()
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
                for j in bigs:
                    cf[('z', zkey(tuple(w[(j + i) % n] for i in range(5)), H[j], H[(j - 1) % n]))] += 1
                for k in sixes:   # classes H, Fn are already 0/1 = c2 values; pass letters 5 / 7 as class witnesses
                    L5 = lambda c: 7 if c else 5
                    cf[('g', g2_of(w[(k + 1) % n], L5(H[k]), L5(Fn[k]), L5(H[(k - 1) % n]), w[(k - 1) % n], w[(k + 2) % n], w[(k - 2) % n]))] += 1
                k_ = tuple(sorted(cf.items()))
                if k_ not in seen: seen.add(k_); out.append((''.join(map(str, w)), dict(cf), list(hb) + ['|'] + list(fb)))
    return out
def cons2_coef(L, s):
    cf = collections.Counter()
    for i in range(6):
        if L[i] == 5: cf[('g', g2_of(L[(i + 1) % 6], L[(i + 2) % 6], L[(i + 3) % 6], L[(i + 4) % 6], L[(i + 5) % 6], s[i], s[(i - 1) % 6]))] += 1
    for j in range(6):
        if L[j] >= 7: cf[('h', h2_of(tuple(L[(j + i) % 6] for i in range(6)), s[j], s[(j - 1) % 6]))] -= 1
    return cf
SALL = np.array(list(itertools.product(range(5), repeat=6)), dtype=np.int64)   # apex words (letter indices)
def cons2_delta(L, GV, HV2):
    """Delta(s) = sum g - sum h over all 5^6 apex words for link L (vectorised); returns array"""
    D = np.zeros(len(SALL))
    for i in range(6):
        if L[i] == 5:
            T = np.array([[GV.get(g2_of(L[(i + 1) % 6], L[(i + 2) % 6], L[(i + 3) % 6], L[(i + 4) % 6], L[(i + 5) % 6], LET[a], LET[b]), 0.0) for b in range(5)] for a in range(5)])
            D += T[SALL[:, i], SALL[:, (i - 1) % 6]]
    for j in range(6):
        if L[j] >= 7:
            m = tuple(L[(j + i) % 6] for i in range(6))
            T = np.array([[HV2.get(h2_of(m, LET[a], LET[b]), 0.0) for b in range(5)] for a in range(5)])
            D -= T[SALL[:, j], SALL[:, (j - 1) % 6]]
    return D
def window_table_R2(U, y, x, MV2):
    W = window_table(U, y, x)
    if ZH:
        for a, b, e, f, q, r in itertools.product(range(5), repeat=6):
            wd = (U, LET[e], LET[r], LET[q], LET[b])
            if isR5(list(wd)): continue
            W[a, b, 0, e, f, :, q, r, :] += ZV.get(zkey(wd, c2(LET[f]), c2(LET[a])), 0.0)
    if Q7:
        for b, e, q, r in itertools.product(range(5), repeat=4):
            sg = q7sig(U, LET[e], LET[r], LET[q], LET[b]); ks = q7keys(sg)
            if ks: W[:, b, 2, e, :, :, q, r, :] += max(QV.get(k, 0.0) for k in ks)
    for a, b, e, f, q, r in itertools.product(range(5), repeat=6):
        if not AP and (a or f): continue
        sg = sig2_of(U, LET[e], LET[r], LET[q], LET[b], LET[f], LET[a])
        v = MV2(sg)
        if v is None: continue
        if AP: W[a, b, 1, e, f, :, q, r, :] += v
        else: W[:, b, 1, e, :, :, q, r, :] += v
    return W
def class_table_R2(xon):
    g = np.indices((5,) * 9, dtype=np.int64)
    a, b, c, e, f, p, q, r, s_ = g
    C = np.where(c == 0, 1 + ((b * 5 + e) * 5 + q) * 5 + r, 0)
    if ZH: C = np.where(c == 0, 1 + 100000000 + (((((a * 5 + b) * 5 + e) * 5 + f) * 5 + q) * 5 + r), C)
    C = np.where(c == 1, 1 + 625 + (((((a * 5 + b) * 5 + e) * 5 + f) * 5 + q) * 5 + r), C)
    if xon: C = np.where(c >= 2, 1 + 625 + 15625 + c * 15625 + (((((a * 5 + b) * 5 + e) * 5 + f) * 5 + q) * 5 + r), C)
    return C.astype(np.int32)
def recv_coef_R2(d, lk, sv, xon):
    cy, cx = recv_coef(d, lk, sv, xon); cf = collections.Counter()
    for r_, c in cy.items(): cf[('y', r_)] += c
    for r_, c in cx.items():
        if c: cf[('x', r_)] += c
    U = min(d, 9); w = [int(ch) for ch in lk]; s = [int(ch) for ch in sv]
    for j in range(d):
        if w[j] == 6:
            sg = sig2_of(U, w[(j + 1) % d], s[j], s[(j - 1) % d], w[(j - 1) % d], w[(j + 2) % d], w[(j - 2) % d])
            if sig2_keys(sg): cf[('M', sg)] += 1
        if w[j] == 7 and Q7:
            sg = q7sig(U, w[(j + 1) % d], s[j], s[(j - 1) % d], w[(j - 1) % d])
            if q7keys(sg): cf[('Q', sg)] += 1
        if w[j] == 5 and ZH:
            cf[('z', zkey((U, w[(j + 1) % d], s[j], s[(j - 1) % d], w[(j - 1) % d]), c2(w[(j + 2) % d]), c2(w[(j - 2) % d])))] += 1
    if Q7 and d == 7:
        for k, m in q7_inflow(w).items(): cf[('q', k)] -= m
    return cf
def cmd_orientR2():
    bad = 0; n = 0
    for a in itertools.product(LET, repeat=7):
        n += 1
        if g2_of(*a) != g2_of(a[4], a[3], a[2], a[1], a[0], a[6], a[5]): bad += 1
        if sig2_of(*a) != sig2_of(a[0], a[4], a[3], a[2], a[1], a[6], a[5]): bad += 1
    for n_ in itertools.product(LET, repeat=5):
        for hr, hl in ((0, 1), (1, 0), (1, 1), (0, 0)):
            n += 1
            if zkey(n_, hr, hl) != zkey((n_[0], n_[4], n_[3], n_[2], n_[1]), hl, hr): bad += 1
    for L in itertools.product(LET, repeat=6):
        for ar, al in ((5, 7), (8, 6), (9, 9)):
            if h2_of(L, ar, al) != h2_of((L[0],) + tuple(reversed(L[1:])), al, ar): bad += 1
    # physical: conservation coefficients invariant under rotating / reflecting the whole 6-centred arrangement
    rng = np.random.default_rng(1)
    for _ in range(20000):
        L = tuple(int(v) for v in rng.choice(LET, 6)); s = tuple(int(v) for v in rng.choice(LET, 6)); k = int(rng.integers(6))
        Lr = L[k:] + L[:k]; sr = s[k:] + s[:k]
        Lf = tuple(L[(-i) % 6] for i in range(6)); sf = tuple(s[(-i - 1) % 6] for i in range(6))
        if cons2_coef(L, s) != cons2_coef(Lr, sr) or cons2_coef(L, s) != cons2_coef(Lf, sf): bad += 1
    log('orientation test R6x2 (apex %s): %d + %d + 20000 cases, %d mismatches' % (AP, n, 3 * 5 ** 6, bad))
def cmd_solveR2():
    import highspy
    load_patterns()
    xon = 'xon' in FLAGS; XCAP = float(OPT.get('xcap', '3')); XPEN = [float(OPT.get('xpen', '0'))]
    p = os.path.join(WORK, 'clsR2_%d%s.bin' % (int(xon), 'z' if ZH else ''))
    if not os.path.exists(p): class_table_R2(xon).tofile(p)
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
    info = []; have = set(); msig = set(); conset = set(); qsig = set()
    def addrow(cf, lo, hi, inf_):
        idx = np.array([col(k) for k in cf], dtype=np.int32); val = np.array([float(v) for v in cf.values()])
        h.addRow(lo, hi, len(idx), idx, val); info.append(inf_)
    SR = R2_sender_rows()
    for wd, cf, bits in SR:
        c2_ = dict(cf); c2_[('t',)] = 1.0; addrow(c2_, 1.0, inf, ('senderR2', wd, bits))
    RW = relay_words()
    def addsig(sg):
        if sg in msig: return
        msig.add(sg)
        for k in sig2_keys(sg): addrow({('h', k): 1.0, ('M', sg): -1.0}, -inf, 0.0, ('mrowR2', list(sg), list(k)))
    def recv(d, lk, sv):
        cf = recv_coef_R2(d, lk, sv, xon)
        key = (d, tuple(sorted(cf.items(), key=str)))
        if key in have: return False
        have.add(key)
        for k in cf:
            if k[0] == 'M': addsig(k[1])
            if k[0] == 'Q' and k[1] not in qsig:
                qsig.add(k[1])
                for kk in q7keys(k[1]): addrow({('q', kk): 1.0, ('Q', k[1]): -1.0}, -inf, 0.0, ('mrowQ', list(k[1]), list(kk)))
        c2_ = dict(cf); c2_[('t',)] = -1.0
        addrow(c2_, -inf, d - 6.0, ('receiverR2', d, lk, sv)); return True
    def addcons(L, s):
        cf = {k: v for k, v in cons2_coef(L, s).items() if v}
        kk = tuple(sorted(cf.items()))
        if not cf or kk in conset: return False
        conset.add(kk); addrow(cf, 0.0, 0.0, ('cons2', list(L), list(s))); return True
    # initial conservation rows: one apex word per L (all apexes 5) -- the rest by separation
    for L in RW: addcons(L, (5,) * 6)
    if 'consbasis' in OPT:
        nb = sum(addcons(tuple(L), tuple(s_)) for L, s_ in json.load(open(OPT['consbasis'])))
        log('conservation basis rows added: %d' % nb)
    if 'warm' in OPT:
        nw = 0
        for fn in OPT['warm'].split(','):
            for line in open(fn):
                m = re.match(r'^R (\d+) (\d+) (\d+)', line)
                if m and admissible(int(m.group(1)), m.group(2), m.group(3)) is None: nw += recv(int(m.group(1)), m.group(2), m.group(3))
        log('warm rows admitted: %d' % nw)
    ng = sum(1 for k in cols if k[0] == 'g')
    log('R6x2 (apex %s): %d sender rows, %d g keys in senders, %d six-words, %d initial cons rows, %d M sigs' % (AP, len(SR), ng, len(RW), len(conset), len(msig)))
    if 'structonly' in FLAGS: return h, cols, info, conset, RW, SR
    T0 = time.time(); rowlog = open(os.path.join(HERE, 'rows_%s.txt' % OPT.get('tag', 'run')), 'w')
    for it in range(MAXIT):
        t1 = time.time()
        if 'ipm0' in FLAGS: h.setOptionValue('solver', 'ipm' if it == 0 else 'simplex')
        h.run(); xv = np.array(h.getSolution().col_value); t = xv[jt]
        y = np.array([xv[cols[('y', r_)]] for r_ in ROOTS])
        GV = {k[1]: xv[i] for k, i in cols.items() if k[0] == 'g'}; HV2 = {k[1]: xv[i] for k, i in cols.items() if k[0] == 'h'}
        ZV.clear(); ZV.update({k[1]: xv[i] for k, i in cols.items() if k[0] == 'z'})
        QV.clear(); QV.update({k[1]: xv[i] for k, i in cols.items() if k[0] == 'q'})
        if Q7: write_bonus()
        xd = {k[1]: xv[i] for k, i in cols.items() if k[0] == 'x' and xv[i] > 1e-12}
        mcache = {}
        def MV2(sg):
            if sg not in mcache:
                ks = sig2_keys(sg); mcache[sg] = max(HV2.get(k, 0.0) for k in ks) if ks else None
            return mcache[sg]
        tlp = time.time() - t1; added = 0; per = {}
        nc = 0; worst = 0.0
        for L in RW:   # conservation separation
            D = cons2_delta(L, GV, HV2)
            for idx in (int(np.argmax(D)), int(np.argmin(D))):
                if abs(D[idx]) > 1e-9:
                    worst = max(worst, abs(D[idx]))
                    if addcons(L, tuple(LET[v] for v in SALL[idx])): nc += 1
        added += nc; per['cons'] = (nc, round(worst, 6))
        Wc = {}
        for d in range(7, DMAX + 1):
            U = min(d, 9)
            if U not in Wc: Wc[U] = window_table_R2(U, y, xd, MV2)
            rr, dt, ni = run_sep(d, Wc[U], d - 6 + t + TOL, K, 2)
            n = 0; mx = None
            for r_ in rr:
                if r_[0] == 'V':
                    mx = max(mx or -1e9, float(r_[1]) - (d - 6 + t))
                    if 'dbg' in FLAGS and n == 0:
                        cf = recv_coef_R2(d, r_[2], r_[3], xon)
                        val = sum(v * (MV2(k[1]) if k[0] == 'M' else xv[cols[k]] if k in cols else 0) for k, v in cf.items())
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
    S = {'t': float(t), 'model': 'R6x2', 'apex': AP, 'xon': xon,
         'y': {rname(k[1]): float(xv[i]) for k, i in cols.items() if k[0] == 'y' and xv[i] > 0},
         'g': [[list(k[1]), float(xv[i])] for k, i in cols.items() if k[0] == 'g' and xv[i] > 0],
         'h': [[list(k[1]), float(xv[i])] for k, i in cols.items() if k[0] == 'h' and xv[i] > 0],
         'z': [[list(k[1]), float(xv[i])] for k, i in cols.items() if k[0] == 'z' and xv[i] > 0], 'zh': ZH, 'apexcls': AC,
         'q': [[list(k[1]), float(xv[i])] for k, i in cols.items() if k[0] == 'q' and xv[i] > 0], 'q7': Q7,
         'x': {str(k[1]): float(xv[i]) for k, i in cols.items() if k[0] == 'x' and xv[i] > 0}}
    json.dump(S, open(os.path.join(HERE, 'sol_%s.json' % tag), 'w'))
    cert = [{'w': float(dv), 'row': info[i]} for i, dv in enumerate(duals) if abs(dv) > 1e-11]
    json.dump(cert, open(os.path.join(HERE, 'cert_%s.json' % tag), 'w'), indent=0)
    log('LP t* = %.12f ; dual rows %d ; wrote sol_%s.json cert_%s.json' % (t, len(cert), tag, tag))
    for c in sorted(cert, key=lambda c: -abs(c['w'])):
        if c['row'][0] in ('senderR2', 'receiverR2'): log('  %+.9f %s' % (c['w'], ' '.join(map(str, c['row'][:4]))))
    log('  (+ %d cons2 / mrowR2 rows)' % sum(1 for c in cert if c['row'][0] in ('cons2', 'mrowR2')))
def cons2_block(L):
    """dense conservation block of link L over all 5^6 apex words: (matrix, local key list)"""
    terms = []
    for i in range(6):
        if L[i] == 5: terms.append((i, 1.0, [[('g', g2_of(L[(i + 1) % 6], L[(i + 2) % 6], L[(i + 3) % 6], L[(i + 4) % 6], L[(i + 5) % 6], LET[a], LET[b])) for b in range(5)] for a in range(5)]))
    for j in range(6):
        if L[j] >= 7:
            m = tuple(L[(j + i) % 6] for i in range(6))
            terms.append((j, -1.0, [[('h', h2_of(m, LET[a], LET[b])) for b in range(5)] for a in range(5)]))
    keys = {}
    for _, _, T in terms:
        for rw in T:
            for k in rw: keys.setdefault(k, len(keys))
    A = np.zeros((len(SALL), len(keys))); rid = np.arange(len(SALL))
    for i, sgn, T in terms:
        I = np.array([[keys[k] for k in rw] for rw in T])
        np.add.at(A, (rid, I[SALL[:, i], SALL[:, (i - 1) % 6]]), sgn)
    return A, list(keys)
def cmd_structR2():
    FLAGS.add('structonly')
    h, cols, info, conset, RW, SR = cmd_solveR2()
    # full conservation system over all L in RW x all 5^6 apex words. h keys are private to one L (the key fixes L),
    # so rank = sum_L rank(H_L) + rank of the stacked g-only consequences of each block.
    allg = {}; allh = set(); nrows = 0; rH = 0; Gstack = []; rL_tot = 0; gonly = set()
    for L in RW:
        A, ks = cons2_block(L)
        U_ = np.unique(A, axis=0); U_ = U_[np.abs(U_).sum(1) > 0]
        hi = [c for c, k in enumerate(ks) if k[0] == 'h']; gi = [c for c, k in enumerate(ks) if k[0] == 'g']
        for k in ks:
            if k[0] == 'g': allg.setdefault(k, len(allg))
            else: allh.add(k)
        if not hi:
            for r_ in U_: gonly.add(tuple((ks[c], r_[c]) for c in np.nonzero(r_)[0]))
        else: nrows += len(U_)
        u, sv, vt = np.linalg.svd(U_, full_matrices=False); r = int((sv > 1e-9 * max(1, sv[0])).sum()); B = vt[:r]
        rL_tot += r
        Bh = B[:, hi]
        if hi:
            u2, s2, v2 = np.linalg.svd(Bh, full_matrices=True); r2 = int((s2 > 1e-9 * max(1, s2[0] if len(s2) else 1)).sum())
            N = u2[:, r2:].T            # combos with zero h part
        else: r2 = 0; N = np.eye(r)
        rH += r2
        if len(N):
            Gp = N @ B[:, gi]; G = np.zeros((len(N), 0))
            Gstack.append((Gp, [allg[ks[c]] for c in gi]))
    nrows += len(gonly)
    Gall = np.zeros((sum(len(g) for g, _ in Gstack), len(allg))); o = 0
    for g, idx in Gstack: Gall[o:o + len(g), idx] = g; o += len(g)
    rG = np.linalg.matrix_rank(Gall) if len(Gall) else 0
    sg = set()
    for U in BIGL:
        for t7 in itertools.product(LET, repeat=6):
            wr, sr, sl, wl, wrr, wll = t7
            if not AP and (wrr != 5 or wll != 5): continue
            s_ = sig2_of(U, wr, sr, sl, wl, wrr, wll)
            if sig2_keys(s_): sg.add(s_)
    nm = sum(len(sig2_keys(s_)) for s_ in sg)
    gs = sum(1 for k in cols if k[0] == 'g')
    out = ['s12 structural summary (%s)' % ('full s12 keys' if AP else 'fallback = s10 keys'),
           'registry: %s + RSST-D + L2 (xcap 3)' % os.path.basename(OPT.get('args', '?')).replace('.txt', ''),
           'key counts by type:',
           '  y (five -> big, s1 roots): %d' % len(ROOTS),
           '  g (five -> 6): %d in conservation rows, %d of them read by sender rows' % (len(allg), gs),
           '  h (6 -> big): %d' % len(allh),
           '  M (receiver inflow signatures): %d' % len(sg),
           '  x (big-big, tau codes): lazy',
           '6-types (canonical non-R6 6-links with a five): %d' % len(RW),
           'conservation rows (distinct, all 6-types x all apex words): %d' % nrows,
           'conservation rank: %d (= %d from h-blocks + %d g-only)' % (rH + rG, rH, rG),
           '  g-only part: rank %d on %d g keys; g directions left free: %d' % (rG, len(allg), len(allg) - rG),
           'row counts at start of solve: sender %d ; conservation %d (rest by separation) ; M-rows if all used %d ; receivers by separation' % (len(SR), len(conset), nm)]
    if ZH:
        zk = set()
        for wd, cf, b in SR: zk.update(k for k in cf if k[0] == 'z')
        out.insert(4, '  z (big -> five, second split): %d' % len(zk))
    open(OPT.get('structout', os.path.join(HERE, 's12_struct%s.txt' % ('' if AP else '_noapex'))), 'w').write('\n'.join(out) + '\n')
    for l in out: log(l)
def cmd_lowerR2():
    """exact check from signed duals (as lowerR): senderR2 >= (w>=0), cons2 = (any sign), mrowR2 h - M <= 0 (w<=0),
    receiverR2 <= (w<=0); rows re-derived from labels; rescale so t's reduced cost is 0; x priced at its cap."""
    load_patterns()
    xon = 'xon' in FLAGS; XCAP = Fraction(OPT.get('xcap', '3')); C = json.load(open(OPT['cert']))
    SR = {(wd, tuple(map(str, b))): cf for wd, cf, b in R2_sender_rows()}
    tot = collections.defaultdict(Fraction); D = Fraction(0); ok = True; tco = Fraction(0); cnt = collections.Counter()
    for c in C:
        w = Fraction(c['w']).limit_denominator(10 ** 7); row = c['row']; cnt[row[0]] += 1
        if row[0] == 'senderR2':
            cf = SR.get((row[1], tuple(map(str, row[2]))))
            if cf is None: log('  NOT A SENDER ROW', row); ok = False; continue
            if w < 0: log('  WRONG SIGN', row); ok = False; continue
            for k, v in cf.items(): tot[k] += w * v
            tco += w; D += w
        elif row[0] == 'cons2':
            L = tuple(row[1]); s = tuple(row[2])
            if isR6(L) or len(L) != 6 or len(s) != 6 or any(v not in LET for v in L + s): log('  BAD CONS2', row); ok = False; continue
            for k, v in cons2_coef(L, s).items(): tot[k] += w * v
        elif row[0] == 'mrowR2':
            sg = tuple(row[1]); k = tuple(row[2])
            if len(sg) != (7 if AP else 5) or sg != sig2_of(*(sg if AP else sg + (5, 5))): log('  NONCANON SIG', row); ok = False; continue
            if k not in sig2_keys(sg): log('  BAD MROW', row); ok = False; continue
            if w > 0: log('  WRONG SIGN', row); ok = False; continue
            tot[('h', k)] += w; tot[('M', sg)] -= w
        elif row[0] == 'mrowQ':
            sg = tuple(row[1]); k = tuple(row[2])
            if sg != q7sig(*sg) or k not in q7keys(sg): log('  BAD MROWQ', row); ok = False; continue
            if w > 0: log('  WRONG SIGN', row); ok = False; continue
            tot[('q', k)] += w; tot[('Q', sg)] -= w
        elif row[0] == 'receiverR2':
            d, lk, sv = int(row[1]), row[2], row[3]
            why = admissible(d, lk, sv)
            if why: log('  RECEIVER NOT ADMISSIBLE', row, why); ok = False; continue
            if w > 0: log('  WRONG SIGN', row); ok = False; continue
            for k, v in recv_coef_R2(d, lk, sv, xon).items(): tot[k] += w * v
            tco -= w; D += w * (d - 6)
        else: log('  UNKNOWN', row); ok = False
    if tco <= 0: log('  t coefficient sum not positive'); ok = False; tco = Fraction(1)
    D = D / tco; neg = []
    for k, v in tot.items():
        rc = -v / tco
        if rc < 0:
            if k[0] == 'x': D += rc * XCAP
            else: neg.append((k, rc))
    if neg: log('  negative reduced costs:', len(neg), neg[:5]); ok = False
    log('rows by type: %s' % dict(cnt))
    log('LOWER-R2: %s  t >= %s = %.9f  (%d rows)' % ('VALID' if ok else 'INVALID', D, float(D), len(C)))
def all6_words():
    out = set()
    for L in itertools.product(LET, repeat=6):
        c = canon6(L)
        if c not in out and not isR6(c): out.add(c)
    return sorted(out)
def cmd_upperR2():
    load_patterns()
    xon = 'xon' in FLAGS
    p = os.path.join(WORK, 'clsR2_%d%s.bin' % (int(xon), 'z' if ZH else ''))
    if not os.path.exists(p): class_table_R2(xon).tofile(p)
    CLSFILE[0] = p
    Sj = json.load(open(OPT['sol'])); t = Sj['t']
    y = np.zeros(len(ROOTS))
    for k, v in Sj['y'].items():
        u, rest = k.split('|'); r_ = root(list((int(u),) + tuple(int(c) for c in rest)), 0); y[RIX[r_]] = v
    GV = {tuple(k): v for k, v in Sj['g']}; HV2 = {tuple(k): v for k, v in Sj['h']}
    ZV.clear(); ZV.update({tuple(k): v for k, v in Sj.get('z', [])})
    if Sj.get('z') and not ZH: log('SOLUTION HAS z BUT zh FLAG OFF'); return
    QV.clear(); QV.update({tuple(k): v for k, v in Sj.get('q', [])})
    if Sj.get('q') and not Q7: log('SOLUTION HAS q BUT q7 FLAG OFF'); return
    if Q7: log('bonus links: %d' % write_bonus())
    xd = {int(k): v for k, v in Sj.get('x', {}).items()}
    if any(v < 0 for v in list(GV.values()) + list(HV2.values()) + list(y)): log('NEGATIVE VALUE'); 
    bad = 0
    for wd, cf, bits in R2_sender_rows():
        v = sum(c * (y[RIX[k[1]]] if k[0] == 'y' else ZV.get(k[1], 0.0) if k[0] == 'z' else GV.get(k[1], 0.0)) for k, c in cf.items())
        if v < 1 - t - EPS: bad += 1
    log('sender rows violated: %d' % bad)
    nc = 0; worst = 0.0; A6 = all6_words()
    for L in A6:   # every non-R6 6-arrangement, with or without a five, every apex word
        Dl = cons2_delta(L, GV, HV2); m = float(np.abs(Dl).max()); worst = max(worst, m)
        if m > 1e-9: nc += 1
    log('conservation: %d canonical non-R6 links x 5^6 apex words; links with |in - out| > 1e-9: %d (worst %.3g)' % (len(A6), nc, worst)); bad += nc
    mcache = {}
    def MV2(sg):
        if sg not in mcache:
            ks = sig2_keys(sg); mcache[sg] = max(HV2.get(k, 0.0) for k in ks) if ks else None
        return mcache[sg]
    for d in range(7, DMAX + 1):
        W = window_table_R2(min(d, 9), y, xd, MV2)
        res, dt, ni = run_sep(d, W, d - 6 + t + EPS, 20, 0)
        v = [r for r in res if r[0] == 'V']; bad += len(v)
        log('d=%d: %d violated (exhaustive, %.1fs)' % (d, len(v), dt))
    W9 = window_table_R2(9, y, xd, MV2); M = relaxed_M(W9)
    for d in range(DMAX + 1, DTAIL + 1):
        v = closed_max(M, d)
        if v > d - 6 + t + EPS:
            res, dt, ni = run_sep(d, W9, d - 6 + t + EPS, 20, 0, pats=False); nv = sum(1 for r in res if r[0] == 'V'); bad += nv
            log('d=%d relaxed %.6f > cap; exact pattern-free: %d violated' % (d, v, nv))
    lam = karp(M); d0 = (6 - t) / (1 - lam) if lam < 1 else 1e9
    log('Karp lambda %.9f d0 %.3f' % (lam, d0))
    if d0 > DTAIL + 1: bad += 1
    log('UPPER-R2: %s at t = %.12f' % ('FEASIBLE' if bad == 0 else 'INFEASIBLE (%d)' % bad, t))
def cmd_ctxR2():
    """sender rows of the listed words in the context 'all hats and fans big' (bits all 1): value breakdown"""
    Sj = json.load(open(OPT['sol'])); t = Sj['t']
    GV = {tuple(k): v for k, v in Sj['g']}; YV = Sj['y']; GV.update({tuple(k): v for k, v in Sj.get('z', [])})
    def yv(r_): return YV.get(rname(r_), 0.0)
    for wd, cf, bits in R2_sender_rows():
        if wd not in OPT.get('words', '55677,56687').split(',') : continue
        b = [x for x in bits if x != '|']
        if not all(x == 1 for x in b): continue
        parts = ['%s%s=%.5f' % (k[0], ''.join(map(str, k[1])) if k[0] in 'gz' else rname(k[1]), (yv(k[1]) if k[0] == 'y' else GV.get(k[1], 0.0))) for k in cf]
        tot = sum(c * (yv(k[1]) if k[0] == 'y' else GV.get(k[1], 0.0)) for k, c in cf.items())
        log('%s all-big ring: total %.5f vs 1-t %.5f  %s' % (wd, tot, 1 - t, ' '.join(parts)))
def cmd_consbasisR2():
    """per 6-type L: a maximal independent set of actual conservation rows (L, s) (QR with column pivoting on A_L^T);
    together they imply every (L, s) row. Written as JSON [[L, s], ...]."""
    import scipy.linalg as sla
    out = []; tot = 0
    for L in relay_words():
        A, ks = cons2_block(L)
        U_, idx = np.unique(A, axis=0, return_index=True)
        keep = np.abs(U_).sum(1) > 0; U_ = U_[keep]; idx = idx[keep]
        if not len(U_): continue
        R, P = sla.qr(U_.T, mode='r', pivoting=True)
        dg = np.abs(np.diag(R)); r = int((dg > 1e-9 * max(1.0, dg[0])).sum())
        for q in P[:r]: out.append([list(L), [LET[v] for v in SALL[idx[q]]]])
        tot += r
    json.dump(out, open(OPT.get('out', os.path.join(HERE, 'cons2basis.json')), 'w'))
    log('conservation basis: %d rows over %d 6-types' % (tot, len(relay_words())))
def cmd_rowR2():
    """one receiver row at a solution: each term's value, load vs cap, slack, and its dual weight in cert"""
    load_patterns(); xon = 'xon' in FLAGS
    Sj = json.load(open(OPT['sol'])); t = Sj['t']; d = int(OPT['d']); lk = OPT['lk']; sv = OPT['sv']
    YV = Sj['y']; HV2 = {tuple(k): v for k, v in Sj['h']}; ZV.clear(); ZV.update({tuple(k): v for k, v in Sj.get('z', [])})
    XV = {int(k): v for k, v in Sj.get('x', {}).items()}; QV.clear(); QV.update({tuple(k): v for k, v in Sj.get('q', [])})
    def MV2(sg):
        ks = sig2_keys(sg); return max(HV2.get(k, 0.0) for k in ks) if ks else 0.0
    tot = 0.0; parts = []
    for k, c in sorted(recv_coef_R2(d, lk, sv, xon).items(), key=str):
        v = YV.get(rname(k[1]), 0.0) if k[0] == 'y' else ZV.get(k[1], 0.0) if k[0] == 'z' else XV.get(k[1], 0.0) if k[0] == 'x' else QV.get(k[1], 0.0) if k[0] == 'q' else max([QV.get(kk, 0.0) for kk in q7keys(k[1])] or [0.0]) if k[0] == 'Q' else MV2(k[1])
        tot += c * v
        if abs(c * v) > 1e-12: parts.append('%s%s:%+g*%.5f' % (k[0], rname(k[1]) if k[0] == 'y' else ''.join(map(str, k[1])) if k[0] != 'x' else k[1], c, v))
    w = 0.0
    if 'cert' in OPT:
        for c in json.load(open(OPT['cert'])):
            if c['row'][0] == 'receiverR2' and int(c['row'][1]) == d and c['row'][2] == lk and c['row'][3] == sv: w = c['w']
    log('row d=%d %s/%s: load %.9f cap %.9f slack %.3g dual %.9f admissible=%s' % (d, lk, sv, tot, d - 6 + t, d - 6 + t - tot, w, admissible(d, lk, sv)))
    log('  terms: ' + ' '.join(parts))
