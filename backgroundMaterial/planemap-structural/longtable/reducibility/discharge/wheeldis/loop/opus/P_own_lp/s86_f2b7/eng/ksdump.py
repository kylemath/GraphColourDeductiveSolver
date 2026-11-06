# ksdump.py (s78_kstar, Team D): row-value dump of the K* / generic EDGE terms on a fixed, seeded sample of receiver rows, for an
# independent re-implementation to compare row by row.  exec'd by pcheck.py after edgefam.py; runs inside upperR2 (option ksdump=<tsv>,
# after the solution is loaded and checked; nothing else of upperR2 runs).  Options: ksdump=<out tsv>, seed= (default 7900), n7= n8= n9=.
# Per row (TSV, one line): d, link word, apex word (s_i = apex(w_i, w_{i+1})), sample tag, mirror-pair id;
#   per family F in K1 (= K*), then each EDGE key: F_pay_n = payer slots (the centre pays, coefficient -1 each, exact),
#   F_rec_n = payee slots AS THE ENGINE ROW USES THEM (K*: exact masks; EDGE: the window bound), F_rec_x = payee slots with exact masks
#   (grammar.py semantics on W6's picture: amask & ~extra6, L3T & ~extra7 at d = 7, 7-privates free at d >= 8), F_dirs = orientations
#   firing (p+ p- r+ r-), F_term = amount * (F_rec_n - F_pay_n);
#   ks_total = sum of F_term; load_py = the exact Python row value (sum coef * value over every key of recv_coef_R2, the row LHS);
#   load_other = load_py - ks_total; leaf_cpp = jsepf EVAL leaf total for the same arrangement; thr = d - 6 + t; slack = thr - load_py.
_KSD_BITS = lambda l: 1 << (l - 5)
def _ksd_eg_rec_exact(key, d, w, s, j, e):
    """EDGE payee slot with exact masks (grammar semantics); payer at link 7 j, orientation e (the + direction)"""
    n = d; U = min(d, 9)
    if w[j] != 7 or not (key['vm'] & _KSD_BITS(min(d, 9))): return 0
    ap = lambda p: s[(j + p) % n] if e > 0 else s[(j - p - 1) % n]   # apex between orientation offsets p, p+1
    for p_, m in key['conds']:
        sg = 1 if '+' in p_ else -1; se = sg * e   # absolute direction
        if p_[2:] in ('L+1', 'L-1'): ok = _KSD_BITS(w[(j + se) % n]) & m
        elif p_[2:] in ('L+2', 'L-2') and p_[0] == 'S': ok = _KSD_BITS(ap(0 if sg > 0 else -1)) & m
        elif p_[0] == 'R': ok = _KSD_BITS(w[(j + 2 * se) % n]) & m
        elif p_[2:] in ('L+3', 'L-3'):
            c = w[(j + se) % n]; a = s[j] if se > 0 else s[(j - 1) % n]; o = s[(j - 1) % n] if se > 0 else s[j]
            if d == 7 and c <= 6 and a <= 6:
                mm = L3T[(se, c, w[(j + 2 * se) % n], w[(j + 3 * se) % n], w[(j + 4 * se) % n], a, o)] & ~f2bm.extra7(7, w, s, j, se)
                ok = mm & m
            else: ok = True
        else:   # S.A+-1
            k = (j + se) % n
            if w[k] == 5: ok = _KSD_BITS(ap(1 if sg > 0 else -2)) & m
            elif w[k] == 6:
                am = amask(U, w[(k - 2) % n], w[(k - 1) % n], w[(k + 1) % n], w[(k + 2) % n], s[(k - 2) % n], s[(k - 1) % n], s[k], s[(k + 1) % n]) & ~f2bm.extra6(d, w, s, k)
                ok = am & m
            else: ok = True
        if not ok: return 0
    return 1
def _ksd_fams():
    F = []
    if KSTAR: F.append('K1')
    return F + [k['name'] for k in EGKEYS]
def _ksd_terms(d, w, s):
    """per family: (pay_n, rec_n engine, rec_x exact, dirs)"""
    out = {}; U = min(d, 9)
    if KSTAR:
        pay = [(i, e) for i in range(d) for e in (1, -1) if d == 7 and kstar_payer_slot(w, s, i, e)]
        rec = [(j, e) for j in range(d) for e in (1, -1) if d == 7 and kstar_payee_slot(w, s, j, e)]
        out['K1'] = (len(pay), len(rec), len(rec), ''.join(sorted({'p%s' % '+-'[e < 0] for _, e in pay} | {'r%s' % '+-'[e < 0] for _, e in rec})))
    for key in EGKEYS:
        pay = [(i, e) for i in range(d) for e in (1, -1) if d == 7 and _KSD_BITS(w[i]) & key['vm']
               and all(_KSD_BITS(eg_payer_letter(w, s, i, e, p_)) & m_ for p_, m_ in key['conds'])]
        T = eg_tables(key, U); rec = []
        if T is not None: rec = [(j, e) for j in range(d) if w[j] == 7 for ei, e in ((0, 1), (1, -1)) if T[ei][eg_widx(w, s, j)]]
        recx = [(j, e) for j in range(d) for e in (1, -1) if _ksd_eg_rec_exact(key, d, w, s, j, e)]
        out[key['name']] = (len(pay), len(rec), len(recx), ''.join(sorted({'p%s' % '+-'[e < 0] for _, e in pay} | {'r%s' % '+-'[e < 0] for _, e in rec})))
    return out
def _ksd_plant(rng, w, s, fam, role, i, e):
    """plant family fam as payer (role 'p', d = 7 centre pays its link vertex i) or payee (role 'r', link 7 at i pays the centre), orientation e"""
    n = len(w); pick = lambda m: rng.choice([l for l in LET if _KSD_BITS(l) & m])
    def setap(p, l):   # apex between orientation offsets p, p+1 around i
        if e > 0: s[(i + p) % n] = l
        else: s[(i - p - 1) % n] = l
    if fam == 'K1':   # K* in its own convention: e1 = e points to c-
        w[i] = 7
        w[(i - e) % n] = pick(28); w[(i + e) % n] = pick(3)
        if role == 'p': w[(i + 2 * e) % n] = 5; w[(i + 3 * e) % n] = 5; setap(1, pick(28))
        else:
            setap(0, 5)
            if w[(i + e) % n] == 5: setap(1, pick(28))
        return
    key = [k for k in EGKEYS if k['name'] == fam][0]
    if role == 'p':
        w[i] = pick(key['vm'])
        for p_, m_ in key['conds']:
            kd, off = EG_KIND[p_]
            if kd == 0: w[(i + off * e) % n] = pick(m_)
            else: setap(off, pick(m_))
    else:
        w[i] = 7
        for p_, m_ in key['conds']:
            sg = 1 if '+' in p_ else -1
            if p_[:3] == 'S.L' and p_[-1] == '1': w[(i + sg * e) % n] = pick(m_)
            elif p_[:3] == 'S.L' and p_[-1] == '2': setap(0 if sg > 0 else -1, pick(m_))
            elif p_[:3] == 'R.L': w[(i + 2 * sg * e) % n] = pick(m_)
            elif p_[:3] == 'S.A' and w[(i + sg * e) % n] == 5: setap(1 if sg > 0 else -2, pick(m_))
def _ksd_mirror(w, s):
    d = len(w); return [w[(-k) % d] for k in range(d)], [s[(-k - 1) % d] for k in range(d)]
def ks_dump(y, xd, MV2, t):
    out = OPT['ksdump']; seed = int(OPT.get('seed', '7900')); rng = random.Random(seed)
    NS = {7: int(OPT.get('n7', '400')), 8: int(OPT.get('n8', '100')), 9: int(OPT.get('n9', '100'))}
    fams = _ksd_fams(); assert fams, 'ksdump: no K* / EDGE family on'
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
        if k[0] == 'ks': return KSV.get(k[1], 0.0)
        raise Exception('ksdump: unsupported key %s' % (k,))
    rows = []; seen = set(); pid = [0]
    def take(d, w, s, tag, need=None, mir=False):
        lk = ''.join(map(str, w)); sv = ''.join(map(str, s))
        if (lk, sv) in seen or admissible(d, lk, sv) is not None: return False
        tm = _ksd_terms(d, w, s)
        if need is not None:
            f_, r_ = need; v_ = tm[f_]
            if (r_ == 'p' and v_[0] == 0) or (r_ == 'r' and v_[1] == 0) or (r_ == 'b' and not (('p+' in v_[3] or 'r+' in v_[3]) and ('p-' in v_[3] or 'r-' in v_[3]))): return False
        seen.add((lk, sv)); rows.append([d, lk, sv, tag, '', tm])
        if mir:
            w2, s2 = _ksd_mirror(w, s); lk2 = ''.join(map(str, w2)); sv2 = ''.join(map(str, s2))
            if (lk2, sv2) not in seen and admissible(d, lk2, sv2) is None:
                pid[0] += 1; rows[-1][4] = 'm%d' % pid[0]; seen.add((lk2, sv2)); rows.append([d, lk2, sv2, tag + '|mirror', 'm%d' % pid[0], _ksd_terms(d, w2, s2)])
        return True
    rnd = lambda d: ([rng.choice(LET) for _ in range(d)], [rng.choice(LET) for _ in range(d)])
    for d in (7, 8, 9):
        target = NS[d]; start = len(rows)
        roles = [(f_, r_) for f_ in fams for r_ in (('p', 'r') if d == 7 else ('r',)) if d == 7 or f_ in [k['name'] for k in EGKEYS if k['vm'] & 24]]
        per = int(OPT.get('per%d' % d, '44' if d == 7 else '30')); nb = int(OPT.get('nboth', '8'))   # planted rows per (family, role); both-orientation rows per family
        plan = [(f_, r_, 'one') for f_, r_ in roles for _ in range(per)] + [(f_, 'b', 'both') for f_, r_ in roles if r_ == 'r' for _ in range(nb)]
        for n_, (f_, r_, how) in enumerate(plan):
            for _ in range(4000):
                w, s = rnd(d); i = rng.randrange(d)
                if how == 'one': _ksd_plant(rng, w, s, f_, r_, i, rng.choice((1, -1)))
                else:   # both orientations: plant +1 at i and -1 at i (EDGE payee) or at a second position
                    ro = 'r' if d > 7 or rng.random() < 0.5 else 'p'
                    _ksd_plant(rng, w, s, f_, ro, i, 1); _ksd_plant(rng, w, s, f_, ro, (i + rng.choice((0, 3, 4))) % d if d >= 7 else i, -1)
                if take(d, w, s, 'plant:%s:%s' % (f_, {'p': 'payer', 'r': 'payee', 'b': 'both-e'}[r_]), (f_, r_), mir=(n_ % 7 == 0)): break
        while len(rows) - start < target:
            w, s = rnd(d); take(d, w, s, 'random', None, mir=(rng.random() < 0.05))
    # C++ leaf values (jsepf EVAL, the same tables as the separator) and the exact Python row values
    leaf = {}
    for d in (7, 8, 9):
        arr = [(r[1], r[2]) for r in rows if r[0] == d]
        W = window_table_R2(min(d, 9), y, xd, MV2)
        ef = os.path.join(WORK, 'ksdump_eval_d%d.txt' % d); open(ef, 'w').write(''.join('%s %s\n' % a for a in arr))
        F2B_EVAL[0] = ef; rr, dt, ni = run_sep(d, W, 1e9, 1, 0); F2B_EVAL[0] = None
        cpp = [float(r[1]) for r in rr if r[0] == 'E']; assert len(cpp) == len(arr), (len(cpp), len(arr))
        for a, c in zip(arr, cpp): leaf[(d,) + a] = c
    am = {f_: KSV.get(f_, 0.0) for f_ in fams}
    hdr = ['d', 'link', 'apex', 'tag', 'mirror_pair'] + [c % f_ for f_ in fams for c in ('%s_pay_n', '%s_rec_n', '%s_rec_x', '%s_dirs', '%s_term')] + ['ks_total', 'load_py', 'load_other', 'leaf_cpp', 'thr', 'slack']
    L = ['# ksdump (s78_kstar Team D): sol=%s t=%.12f seed=%d amounts %s; stack flags: %s' % (OPT['sol'], t, seed, ' '.join('%s=%.12g' % kv for kv in am.items()),
         ' '.join(a for a in sys.argv[2:] if not a.startswith(('sol=', 'ksdump=', 'work=')))),
         '# EDGE keys: ' + '; '.join('%s = %s' % (k['name'], k['spec']) for k in EGKEYS) + ('; K1 = K* = EDGE(7->7)[S.L+1=B S.L-1=S S.L-2=5 S.L-3=5 S.A-1=B]' if KSTAR else ''),
         '\t'.join(hdr)]
    mx = 0.0; C = collections.Counter()
    for d, lk, sv, tag, mp, tm in rows:
        cf = recv_coef_R2(d, lk, sv, 'xon' in FLAGS); pv = sum(v * val(k) for k, v in cf.items())
        cols = []; tot = 0.0
        for f_ in fams:
            pn, rn, rx, dirs = tm[f_]; term = am[f_] * (rn - pn); tot += term
            assert cf.get(('ks', f_), 0) == rn - pn, ('ksdump: coefficient mismatch', d, lk, sv, f_, cf.get(('ks', f_), 0), rn, pn)
            cols += [str(pn), str(rn), str(rx), dirs or '-', '%.12f' % term]
            C[f_, 'pay'] += pn > 0; C[f_, 'rec'] += rn > 0; C[f_, 'recx'] += rx > 0; C[f_, 'both'] += ('+' in dirs and '-' in dirs); C[f_, 'gap'] += rn != rx
        c = leaf[(d, lk, sv)]; mx = max(mx, abs(c - pv)); thr = d - 6 + t
        L.append('\t'.join([str(d), lk, sv, tag, mp or '-'] + cols + ['%.12f' % tot, '%.12f' % pv, '%.12f' % (pv - tot), '%.12f' % c, '%.12f' % thr, '%.12f' % (thr - pv)]))
        C['d%d' % d] += 1; C['viol'] += pv > thr + 1e-9
    open(out, 'w').write('\n'.join(L) + '\n')
    log('ksdump: %d rows (d=7 %d, d=8 %d, d=9 %d; %d mirror pairs; %d above thr) -> %s; max |load_py - leaf_cpp| = %.3g'
        % (len(rows), C['d7'], C['d8'], C['d9'], pid[0], C['viol'], out, mx))
    for f_ in fams:
        log('ksdump: %s: rows with payer slots %d, payee slots (engine) %d, payee slots (exact) %d, both orientations %d, engine != exact payee %d'
            % (f_, C[f_, 'pay'], C[f_, 'rec'], C[f_, 'recx'], C[f_, 'both'], C[f_, 'gap']))
    log('KSDUMP: %s (max |py - C++| %.3g)' % ('OK' if mx < 1e-9 else 'LEAF MISMATCH', mx))
