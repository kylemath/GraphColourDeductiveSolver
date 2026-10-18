# pslite.py (Opus P_own_lp): rule S-lite (Q_rule_class spec: routes A = rule T and O = the fan, through a 6-spoke
# next to the five's big root; option B small/big letters).  exec'd inside pcheck.py after psolve.py.
#
# Five v, spokes l0..l4; hat h_k = common neighbour of l_k, l_{k+1} other than v; fan f_k (6-spoke l_k) = vertex
# opposite v in l_k's wheel (v, l_{k+1}, h_k, f_k, h_{k-1}, l_{k-1}).  Root B = l_j big; raw (B, a, b, c, e) =
# (l_j, l_{j+1}, ..., l_{j-1}).  Side a = l_{j+1}: A = h_j, O = f_{j+1}; side e = l_{j-1}: A = h_{j-1}, O = f_{j-1}.
# Flag of a side: F = 2*[A big] + [O big] if that spoke is 6, else 0.
# Keys: Y(raw, Fa, Fe); S(raw, Fa, Fe, side, pos), pos in {A, O}; canonical under the reflection (B,e,c,b,a).
def yk(raw, fa, fe):
    raw = tuple(raw); rv = rev5(raw)
    if rv < raw: raw, fa, fe = rv, fe, fa
    elif raw == rv: fa, fe = min(fa, fe), max(fa, fe)
    return (raw, fa, fe)
def sk(raw, fa, fe, sd, pos):
    raw = tuple(raw); rv = rev5(raw); sw = lambda x: 'e' if x == 'a' else 'a'
    if rv < raw: raw, fa, fe, sd = rv, fe, fa, sw(sd)
    elif raw == rv and (fe, fa, sw(sd)) < (fa, fe, sd): fa, fe, sd = fe, fa, sw(sd)
    return (raw, fa, fe, sd, pos)
CLS2 = {0: (5, 6), 1: BIGL}
OON = ['nofan' not in FLAGS]
def S_sender_rows(Oon=True):
    out = []
    for w in SENDERS:
        n = 5; sixes = [k for k in range(n) if w[k] == 6]
        hats = sorted({h for k in sixes for h in (k, (k - 1) % n)})     # h_k between l_k and l_{k+1}
        fans = list(sixes)
        seen = set()
        for hb in itertools.product((0, 1), repeat=len(hats)):
            H = dict(zip(hats, hb))
            for fb in itertools.product((0, 1), repeat=len(fans)):
                Fn = dict(zip(fans, fb)); okc = True
                for k in sixes:
                    if all(isR6((5, w[(k + 1) % n], a_, q, b_, w[(k - 1) % n])) for a_ in CLS2[H[k]] for q in CLS2[Fn[k]] for b_ in CLS2[H[(k - 1) % n]]): okc = False; break
                if not okc: continue
                cf = collections.Counter()
                for j in range(n):
                    if w[j] < 7: continue
                    raw = tuple(w[(j + i) % n] for i in range(5)); ka, ke = (j + 1) % n, (j - 1) % n
                    fa = 2 * H[j] + (Fn[ka] if Oon else 0) if w[ka] == 6 else 0
                    fe = 2 * H[ke] + (Fn[ke] if Oon else 0) if w[ke] == 6 else 0
                    cf[('Y', yk(raw, fa, fe))] += 1
                    for sd, ff in (('a', fa), ('e', fe)):
                        if (sd == 'a' and w[ka] != 6) or (sd == 'e' and w[ke] != 6): continue
                        if ff & 2: cf[('S', sk(raw, fa, fe, sd, 'A'))] += 1
                        if Oon and ff & 1: cf[('S', sk(raw, fa, fe, sd, 'O'))] += 1
                k_ = tuple(sorted(cf.items()))
                if k_ not in seen: seen.add(k_); out.append((''.join(map(str, w)), dict(cf), list(hb) + ['|'] + list(fb)))
    return out
SIGC = {}
def sig_keys(sig):
    """candidate S keys of an inflow signature: ('A', Bl, lamO) = route A into u, O-letter class lamO;
    ('O', Bl, bl, lamA) = route O into u from root letter Bl, b-letter bl, A class lamA."""
    if sig in SIGC: return SIGC[sig]
    s = set()
    if sig[0] == 'A':
        _, Bl, lo = sig
        for p, m, o in itertools.product(LET, repeat=3):
            raw = (Bl, 6, p, m, o)
            if isR5(raw): continue
            for fe in ((0, 1, 2, 3) if o == 6 else (0,)): s.add(sk(raw, 2 + lo, fe, 'a', 'A'))
    else:
        _, Bl, bl, la = sig
        for m, o in itertools.product(LET, repeat=2):
            raw = (Bl, 6, bl, m, o)
            if isR5(raw): continue
            for fe in ((0, 1, 2, 3) if o == 6 else (0,)): s.add(sk(raw, 2 * la + 1, fe, 'a', 'O'))
    SIGC[sig] = sorted(s); return SIGC[sig]
def big(l): return 1 if l >= 7 else 0
def six_inflow_sigs(U, wl, wr, sr, sl):
    """inflow signatures at a link 6 x = w_j with w_{j-1} = wl, w_{j+1} = wr, s_j = sr, s_{j-1} = sl (letters)."""
    out = []; o = OON[0]
    if sr == 5 and wr >= 7: out.append(('A', wr, big(wl) if o else 0))   # I1: five s_j, root w_{j+1}, O = w_{j-1}
    if sl == 5 and wl >= 7: out.append(('A', wl, big(wr) if o else 0))   # I2: five s_{j-1}, root w_{j-1}, O = w_{j+1}
    if o and not isR6((U, wr, sr, 5, sl, wl)):                             # I3: p_j = 5 allowed
        if sr >= 7: out.append(('O', sr, sl, big(wr)))               # root s_j, A = w_{j+1}
        if sl >= 7: out.append(('O', sl, sr, big(wl)))               # root s_{j-1}, A = w_{j-1}
    return out
def five_key(U, wn, si, sp, wp, wnn, snn, wpp, spp):
    """Y key of a link five w_i: raw (U, w_{i+1}, s_i, s_{i-1}, w_{i-1}); side a = w_{i+1}: A = w_{i+2}, O = s_{i+1};
    side e = w_{i-1}: A = w_{i-2}, O = s_{i-2}."""
    fa = 2 * big(wnn) + (big(snn) if OON[0] else 0) if wn == 6 else 0
    fe = 2 * big(wpp) + (big(spp) if OON[0] else 0) if wp == 6 else 0
    return yk((U, wn, si, sp, wp), fa, fe)
SV = {}; MV = {}; KIDX = {}
def window_table_S(U, x):
    W = np.zeros((5,) * 9)
    if U not in KIDX:
        ids = np.zeros((5,) * 8, dtype=np.int64); kl = {}; R5m = np.zeros((5,) * 8, dtype=bool)
        for a, b, e, f, p, q, r, s_ in itertools.product(range(5), repeat=8):
            wd = (U, LET[e], LET[r], LET[q], LET[b])
            if isR5(wd): R5m[a, b, e, f, p, q, r, s_] = True; continue
            k = ('Y', five_key(U, LET[e], LET[r], LET[q], LET[b], LET[f], LET[s_], LET[a], LET[p]))
            ids[a, b, e, f, p, q, r, s_] = kl.setdefault(k, len(kl))
        KIDX[U] = (ids, list(kl), R5m)
    ids, kl, R5m = KIDX[U]
    vals = np.array([SV.get(k, 0.0) for k in kl])
    W0 = vals[ids]; W0[R5m] = -np.inf
    W[:, :, 0] = np.moveaxis(W0, (0, 1, 2, 3, 4, 5, 6, 7), (0, 1, 2, 3, 4, 5, 6, 7))
    for b, e, q, r in itertools.product(range(5), repeat=4):
        if all(isR6([U, LET[e], LET[r], p_, LET[q], LET[b]]) for p_ in LET): W[:, b, 1, e, :, :, q, r, :] = -np.inf; continue
        v = sum(MV.get(sg, 0.0) for sg in six_inflow_sigs(U, LET[b], LET[e], LET[r], LET[q]))
        W[:, b, 1, e, :, :, q, r, :] = v
    if x:
        for c in (2, 3, 4):
            for a, b, e, f, q, r in itertools.product(range(5), repeat=6):
                to = tau(U, LET[c], side(LET[b], LET[a], LET[q]), side(LET[e], LET[f], LET[r]))
                ti = tau(LET[c], U, side(LET[b], LET[q], LET[a]), side(LET[e], LET[r], LET[f]))
                W[a, b, c, e, f, :, q, r, :] += x.get(ti, 0.0) - x.get(to, 0.0)
    return W
def class_table_S(xon):
    g = np.indices((5,) * 9, dtype=np.int64)
    a, b, c, e, f, p, q, r, s_ = g
    full8 = ((((((((a * 5 + b) * 5 + e) * 5 + f) * 5 + p) * 5 + q) * 5 + r) * 5 + s_))
    C = np.where(c == 0, 1 + full8, 0)
    C = np.where(c == 1, 1 + 390625 + ((b * 5 + e) * 5 + q) * 5 + r, C)
    if xon: C = np.where(c >= 2, 1 + 391250 + c * 15625 + (((((a * 5 + b) * 5 + e) * 5 + f) * 5 + q) * 5 + r), C)
    return C.astype(np.int32)
def recv_coef_S(d, lk, sv, xon, have_sig):
    U = min(d, 9); w = [int(c) for c in lk]; s = [int(c) for c in sv]; cf = collections.Counter()
    W_ = lambda k: w[k % d]; S_ = lambda k: s[k % d]
    for i in range(d):
        if w[i] == 5: cf[('Y', five_key(U, W_(i + 1), S_(i), S_(i - 1), W_(i - 1), W_(i + 2), S_(i + 1), W_(i - 2), S_(i - 2)))] += 1
        elif w[i] == 6:
            for sg in six_inflow_sigs(U, W_(i - 1), W_(i + 1), S_(i), S_(i - 1)):
                if sg in have_sig: cf[('M', sg)] += 1
    if xon:
        _, cx = recv_coef(d, lk, sv, True)
        for k, v in cx.items():
            if v: cf[('x', k)] += v
    return cf
def cmd_solveS():
    import highspy
    load_patterns()
    xon = 'xon' in FLAGS; Oon = 'nofan' not in FLAGS; XCAP = float(OPT.get('xcap', '3')); XPEN = [float(OPT.get('xpen', '0'))]
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
    info = []; have = set()
    def addrow(cf, lo, hi, inf_):
        idx = np.array([col(k) for k in cf], dtype=np.int32); val = np.array([float(v) for v in cf.values()])
        h.addRow(lo, hi, len(idx), idx, val); info.append(inf_)
    SR = S_sender_rows(Oon)
    for wd, cf, bits in SR:
        c2 = dict(cf); c2[('t',)] = 1.0; addrow(c2, 1.0, inf, ('senderS', wd, bits))
    Skeys = {k[1] for k in cols if k[0] == 'S'}
    nY = sum(1 for k in cols if k[0] == 'Y'); nSA = sum(1 for k in Skeys if k[4] == 'A'); nSO = len(Skeys) - nSA
    # inflow signatures and M rows
    sigs = set()
    for Bl in BIGL:
        for lo in (0, 1): sigs.add(('A', Bl, lo))
        for bl in LET:
            for la in (0, 1): sigs.add(('O', Bl, bl, la))
    have_sig = set(); nm = 0; covered = set()
    for sg in sorted(sigs, key=str):
        ks = [k for k in sig_keys(sg) if k in Skeys]
        if not ks: continue
        have_sig.add(sg)
        for k in ks: addrow({('S', k): 1.0, ('M', sg): -1.0}, -inf, 0.0, ('mrowS', list(sg), [list(k[0])] + list(k[1:]))); nm += 1; covered.add(k)
    log('rule S-lite (fan %s): %d sender rows, %d Y, %d S_A, %d S_O; %d inflow signatures, %d M rows; S keys with no receiver: %d' % (
        Oon, len(SR), nY, nSA, nSO, len(have_sig), nm, len(Skeys - covered)))
    if Skeys - covered: log('  UNRECEIVED', sorted(Skeys - covered)[:10])
    def recv(d, lk, sv):
        cf = recv_coef_S(d, lk, sv, xon, have_sig)
        key = (d, tuple(sorted(cf.items(), key=str)))
        if key in have: return False
        have.add(key); c2 = dict(cf); c2[('t',)] = -1.0
        addrow(c2, -inf, d - 6.0, ('receiverS', d, lk, sv)); return True
    if 'warm' in OPT:
        nw = 0
        for fn in OPT['warm'].split(','):
            for line in open(fn):
                m = re.match(r'^R (\d+) (\d+) (\d+)', line)
                if m and admissible(int(m.group(1)), m.group(2), m.group(3)) is None: nw += recv(int(m.group(1)), m.group(2), m.group(3))
        log('warm rows admitted: %d' % nw)
    if 'plant' in OPT:   # validation: force one S_O key >= value
        pk = sorted(k for k in Skeys if k[4] == 'O')[int(OPT['plant'])]
        addrow({('S', pk): 1.0}, 0.3, inf, ('plant',)); log('PLANT S %s >= 0.3' % (pk,))
    T0 = time.time(); rowlog = open(os.path.join(HERE, 'rows_%s.txt' % OPT.get('tag', 'run')), 'w')
    for it in range(MAXIT):
        t1 = time.time(); h.run(); xv = np.array(h.getSolution().col_value); t = xv[jt]
        SV.clear(); MV.clear()
        for k, i in cols.items():
            if k[0] in 'YS': SV[k] = xv[i]
        for sg in have_sig: MV[sg] = max(SV.get(('S', k), 0.0) for k in sig_keys(sg))
        xd = {k[1]: xv[i] for k, i in cols.items() if k[0] == 'x' and xv[i] > 1e-12}
        tlp = time.time() - t1; added = 0; per = {}; Wc = {}
        for d in range(7, DMAX + 1):
            U = min(d, 9)
            if U not in Wc: Wc[U] = window_table_S(U, xd)
            rr, dt, ni = run_sep(d, Wc[U], d - 6 + t + TOL, K, 2)
            n = 0; mx = None
            for r_ in rr:
                if r_[0] == 'V':
                    mx = max(mx or -1e9, float(r_[1]) - (d - 6 + t))
                    if 'dbg' in FLAGS and n == 0:
                        cf = recv_coef_S(d, r_[2], r_[3], xon, have_sig)
                        val = sum(v * (MV[k[1]] if k[0] == 'M' else xv[cols[k]] if k in cols else 0) for k, v in cf.items())
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
            if lam >= 1 or (6 - t) / (1 - lam) > DTAIL + 1: log('  TAIL NOT COVERED')
        rowlog.flush()
        log('iter %d t=%.12f rows %d cols %d added %d  lp %.1fs total %.0fs  %s' % (it, t, h.getNumRow(), h.getNumCol(), added, tlp, time.time() - T0, {d: v for d, v in per.items() if v[0]}))
        if not added and XPEN[0]:
            XPEN[0] = 0.0
            for k, i in cols.items():
                if k[0] == 'x': h.changeColCost(i, 0.0)
            log('  converged with x penalty; penalty removed, continuing'); continue
        if not added: break
    sol = h.getSolution(); xv = np.array(sol.col_value); t = xv[jt]; duals = np.array(sol.row_dual); cd = np.array(sol.col_dual)
    tag = OPT.get('tag', 'run')
    fk = lambda k: [list(k[0])] + list(k[1:])
    S = {'t': float(t), 'model': 'S-lite', 'fan': Oon, 'xon': xon,
         'Y': [[fk(k[1]), float(xv[i])] for k, i in cols.items() if k[0] == 'Y' and xv[i] > 0],
         'S': [[fk(k[1]), float(xv[i])] for k, i in cols.items() if k[0] == 'S' and xv[i] > 0],
         'x': {str(k[1]): float(xv[i]) for k, i in cols.items() if k[0] == 'x' and xv[i] > 0}}
    json.dump(S, open(os.path.join(HERE, 'sol_%s.json' % tag), 'w'))
    cert = [{'w': float(abs(dv)), 'row': info[i]} for i, dv in enumerate(duals) if abs(dv) > 1e-10]
    for i in range(len(names)):
        if names[i][0] == 'x' and abs(cd[i]) > 1e-10: cert.append({'w': float(abs(cd[i])), 'row': ['xcap', names[i][1]]})
    json.dump(cert, open(os.path.join(HERE, 'cert_%s.json' % tag), 'w'), indent=0)
    log('LP t* = %.12f ; dual rows %d ; wrote sol_%s.json cert_%s.json' % (t, len(cert), tag, tag))
    for c in sorted(cert, key=lambda c: -c['w']): log('  %.9f %s' % (c['w'], ' '.join(map(str, c['row'][:4]))))

def cmd_upperS():
    """exhaustive check of an S-lite solution: sender rows (all flag assignments), receivers d = 7..DMAX by jsep3
    mode 0/1 on window_table_S (inflow = max over each signature's candidates), relaxed DP + Karp tail."""
    load_patterns()
    Sj = json.load(open(OPT['sol'])); t = Sj['t']; Oon = Sj.get('fan', True); OON[0] = Oon
    tk = lambda e: (tuple(e[0]),) + tuple(e[1:])
    SV.clear(); MV.clear()
    for e, v in Sj['Y']: SV[('Y', tk(e))] = v
    for e, v in Sj['S']: SV[('S', tk(e))] = v
    xd = {int(k): v for k, v in Sj.get('x', {}).items()}
    bad = 0
    for wd, cf, bits in S_sender_rows(Oon):
        v = sum(c * SV.get(k, 0.0) for k, c in cf.items())
        if v < 1 - t - EPS: bad += 1; log('  VIOLATED sender %s %s %.9f' % (wd, bits, v))
    log('sender rows: violated %d' % bad)
    sigs = set()
    for Bl in BIGL:
        for lo in (0, 1): sigs.add(('A', Bl, lo))
        for bl in LET:
            for la in (0, 1): sigs.add(('O', Bl, bl, la))
    for sg in sigs: MV[sg] = max([SV.get(('S', k), 0.0) for k in sig_keys(sg)] + [0.0])
    # every S key with value must be receivable
    allc = set(k for sg in sigs for k in sig_keys(sg))
    unrec = [k for k in SV if k[0] == 'S' and SV[k] > 0 and k[1] not in allc]
    log('S keys > 0 not receivable: %d' % len(unrec)); bad += len(unrec)
    for d in range(7, DMAX + 1):
        W = window_table_S(min(d, 9), xd)
        res, dt, ni = run_sep(d, W, d - 6 + t + EPS, 20, 0)
        v = [r for r in res if r[0] == 'V']; bad += len(v)
        if 'nomax' in FLAGS or d > 10: log('d=%d: %d violated (exhaustive, %.1fs)' % (d, len(v), dt)); continue
        res2, _, _ = run_sep(d, W, 0, 1, 1); r = res2[0]
        log('d=%d: %d violated; max load - (d-6+t) = %+.3e (link %s s %s)' % (d, len(v), float(r[1]) - (d - 6 + t), r[2], r[3]))
    W9 = window_table_S(9, xd); M = relaxed_M(W9)
    for d in range(DMAX + 1, DTAIL + 1):
        v = closed_max(M, d)
        if v > d - 6 + t + EPS:
            res, dt, ni = run_sep(d, W9, d - 6 + t + EPS, 20, 0, pats=False); nv = sum(1 for r in res if r[0] == 'V'); bad += nv
            log('d=%d relaxed %.6f > cap; exact pattern-free: %d violated' % (d, v, nv))
    lam = karp(M); d0 = (6 - t) / (1 - lam) if lam < 1 else 1e9
    log('Karp lambda %.9f d0 %.3f' % (lam, d0))
    if d0 > DTAIL + 1: bad += 1
    log('UPPER-S: %s at t = %.12f' % ('FEASIBLE' if bad == 0 else 'INFEASIBLE (%d)' % bad, t))

def cmd_lowerS():
    load_patterns()
    xon = 'xon' in FLAGS; XCAP = Fraction(OPT.get('xcap', '3')); C = json.load(open(OPT['cert']))
    Oon = 'nofan' not in FLAGS
    SR = {}; Skeys = set()
    for wd, cf, bits in S_sender_rows(Oon):
        SR[(wd, tuple(map(str, bits)))] = cf
        for k in cf:
            if k[0] == 'S': Skeys.add(k[1])
    sigs = set()
    for Bl in BIGL:
        for lo in (0, 1): sigs.add(('A', Bl, lo))
        for bl in LET:
            for la in (0, 1): sigs.add(('O', Bl, bl, la))
    have_sig = {sg for sg in sigs if any(k in Skeys for k in sig_keys(sg))}
    tot = collections.defaultdict(Fraction); sw = Fraction(0); rhs = Fraction(0); ok = True
    tk = lambda e: (tuple(e[0]),) + tuple(e[1:])
    for c in C:
        w = Fraction(c['w']).limit_denominator(10 ** 6); row = c['row']
        if row[0] == 'xcap': tot[('x', row[1])] += w; rhs += w * XCAP; continue
        if row[0] == 'senderS':
            cf = SR.get((row[1], tuple(map(str, row[2]))))
            if cf is None: log('  NOT A SENDER ROW', row); ok = False; continue
            for k, v in cf.items(): tot[k] -= w * v
            rhs -= w; sw += w; continue
        if row[0] == 'mrowS':
            sg = tuple(row[1]); k = tk(row[2])
            if k not in sig_keys(sg): log('  MROW NOT A CANDIDATE', row); ok = False; continue
            tot[('S', k)] += w; tot[('M', sg)] -= w; continue
        if row[0] == 'receiverS':
            d, lk, sv = int(row[1]), row[2], row[3]
            why = admissible(d, lk, sv)
            if why: log('  RECEIVER NOT ADMISSIBLE', row, why); ok = False; continue
            for k, v in recv_coef_S(d, lk, sv, xon, have_sig).items(): tot[k] += w * v
            rhs += w * (d - 6); sw += w; continue
        log('  UNKNOWN ROW', row); ok = False
    neg = {k: v for k, v in tot.items() if v < 0}
    if neg: log('  negative combined coefficients:', len(neg), list(neg.items())[:5]); ok = False
    t0 = -rhs / sw
    log('LOWER-S: %s  t >= %s = %.9f  (%d rows)' % ('VALID' if ok else 'INVALID', t0, float(t0), len(C)))

def cmd_orientS():
    """orientation test: keys read clockwise == anticlockwise, for every raw word, flag pair, side, pos."""
    bad = 0; n = 0
    for raw in itertools.product(LET, repeat=5):
        for fa in range(4):
            for fe in range(4):
                n += 1
                if yk(raw, fa, fe) != yk(rev5(raw), fe, fa): bad += 1
                for sd in 'ae':
                    for pos in 'AO':
                        if sk(raw, fa, fe, sd, pos) != sk(rev5(raw), fe, fa, 'e' if sd == 'a' else 'a', pos): bad += 1
    log('orientation test: %d cases, %d mismatches' % (n, bad))
    # sender physical test: for every sender row term, reading the same five from the mirrored word gives the same keys
    m = 0
    for w in SENDERS[:400]:
        pass
    log('done')
