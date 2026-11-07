# p1r_test.py (s86 p1r): exec'd by eng_p1r/pcheck_dbg.py (ROWDBG=p1r_test.py) with the run family's flags + p1r; replaces lowerR2 by
# the p1_r acceptance tests (driver: p1r/p1r_test.sh).  Float / [M] where it says so; the coefficient tests are exact integers.
#   (a) every entry of W6b's test_vectors.json (md5 892f1e1f): OUT, IN max, IN min, p1_r, and the current coefficient where given;
#   (b) on cert= (k86GL2 phase-1 cert f8893e87): every (d = 7 / 8 receiver row, key) whose p1_r coefficient differs from the current one,
#       compared with W6b's p1r_changes.json (md5 2c0c1333) when the key file is r13w16; no coefficient may increase; d = 8 also against
#       the gkwin window and the KEYSPEC picture; an independent brute force (gk_slots on exact-letter pictures, every realisation of the
#       links the key reads) on every (row, key) the DP decides, up to P1R_BF realisations each;
#   (c) the restricted primal LP (min t over exactly the cert's rows, columns capped as lowerR2 prices them; scipy HiGHS, float; default
#       solve as W6b, plus dual simplex and IPM at 1e-10 tolerances) with the
#       current and with the p1_r receiver coefficients.
# Env: P1R_OUT = result JSON path; P1R_LPDUMP = dir for the LPs (npz); P1R_NEWKEYS = comma list of key-name prefixes reported separately (16f keys); P1R_BF (default 4000);
#      P1R_LP = 0 skips (c); P1R_WARM = a rows file whose d = 7 / 8 lines are timed (setup cost estimate).
import itertools as _it
from fractions import Fraction as _Fr
_KS2 = '/mnt/project-files/swarm/round6/W6-rule-grammar/round16/keyspec2'
def _rowstr(d, w, s): return '%d/%s/%s' % (d, ''.join(map(str, w)), ''.join(map(str, s)))
def _keyarr(keys):
    return (np.array([k['um'] for k in keys], dtype=np.uint8), np.array([k['vm'] for k in keys], dtype=np.uint8), np.stack([k['m'] for k in keys]).astype(np.uint8))
def _bf_inmax(d, w, s, key, dom, cap):
    """max over realisations of the exact IN count of one key, by gk_slots on exact-letter pictures; only the links whose privates some
    live slot reads at a non-wildcard position are enumerated (the others cannot change the count); None if > cap realisations"""
    A, PV = gk_recv_picture(d, w, s); _, (iu, iv, iV) = gk_slots(d, w, A, PV)
    live = [q for q in range(2 * d) if (iu[q] & key['um']) and (iv[q] & key['vm']) and all(iV[q][p_] & key['m'][p_] for p_ in _P1R_FIXCOL)]
    rd = set()
    for q in live:   # a slot's private positions (S.L+-3, S.A+-1) belong to links i - 1, i, i + 1 (whatever the reading): enumerate all three
        i = q // 2
        if any(key['m'][p_] != 31 for p_ in (2, 5, 6, 7)): rd.update(((i - 1) % d, i, (i + 1) % d))
    rd = sorted(j for j in rd if w[j] != 5)
    tot = 1
    for j in rd: tot *= len(dom[j])
    if tot > cap: return None
    fixed = {j: next(iter(sorted(dom[j]))) for j in range(d) if w[j] != 5}
    M1 = key['m'][None, :]; best = -1
    for ch in _it.product(*[sorted(dom[j]) for j in rd]):
        g = dict(fixed); g.update(zip(rd, ch))
        PVr = [None if w[j] == 5 else (1 << (g[j][1] - 5), 1 << (g[j][0] - 5)) for j in range(d)]   # (side 0 = y, side 1 = x)
        _, (ju, jv, jV) = gk_slots(d, w, A, PVr)
        c = int((((jV & M1) != 0).all(axis=1) & ((ju & key['um']) != 0) & ((jv & key['vm']) != 0)).sum())
        best = max(best, c)
    return best
def cmd_lowerR2():
    import scipy.sparse as _sp, time as _tm
    from scipy.optimize import linprog as _lp
    load_patterns(); l3q_load(); kt_load()
    assert P1R and GKWIN and GKLEAF, 'p1r_test: run with gkwin gkleaf p1r'
    xon = 'xon' in FLAGS; OUTJ = {'gkeys': GKFILE, 'gkeys_md5': GKMD5, 'nkeys': len(GKEYS), 'flags': sorted(FLAGS)}; bad = 0
    NEWP = [p for p in os.environ.get('P1R_NEWKEYS', '').split(',') if p]
    isnew = lambda nm: any(nm.startswith(p) for p in NEWP)
    # ---------------- (a) test vectors ----------------
    TV = json.load(open(os.path.join(_KS2, 'test_vectors.json'))); na = 0; ra = []
    for e in TV:
        d, lk, sv = e['row'].split('/'); d = int(d); w = [int(c) for c in lk]; s = [int(c) for c in sv]
        k = gk_parse('T ' + e['rule']); UM, VM, M = _keyarr([k])
        r = p1r_core(d, w, s, UM, VM, M, want_min=True, base_cf=_orig_recv_coef_R2_gk(d, lk, sv, xon))
        assert not r['empty']
        got = {'OUT': int(r['pay'][0]), 'IN_max': int(r['inmax'][0]), 'IN_min': int(r['inmin'][0]), 'v2': int(r['inmax'][0] - r['pay'][0])}
        cur = None
        if e['key'] in GKNAMES:
            kk = GKEYS[GKNAMES.index(e['key'])]
            assert (int(kk['um']), int(kk['vm']), list(map(int, kk['m']))) == (int(k['um']), int(k['vm']), list(map(int, k['m']))), ('test vector rule differs from the loaded key', e['key'])
            cur = int(_p1r_gk_recv_terms_cur(d, w, s).get(('ks', e['key']), 0)); got['cur'] = cur
        ok = all(got[f] == e[f] for f in ('OUT', 'IN_max', 'IN_min', 'v2')) and (e['cur'] is None or cur == e['cur'])
        na += ok; bad += not ok
        ra.append(dict(row=e['row'], key=e['key'], want={f: e[f] for f in ('OUT', 'IN_max', 'IN_min', 'v2', 'cur')}, got=got, ok=ok))
        log('  (a) %-22s %-10s want OUT %d IN %d..%d v2 %d cur %s | got OUT %d IN %d..%d v2 %d cur %s  %s' % (e['row'], e['key'], e['OUT'], e['IN_min'], e['IN_max'], e['v2'], e['cur'],
            got['OUT'], got['IN_min'], got['IN_max'], got['v2'], cur, 'ok' if ok else 'MISMATCH'))
    log('P1R-TEST (a): %d / %d test vectors reproduced' % (na, len(TV))); OUTJ['a'] = {'n': len(TV), 'ok': na, 'entries': ra}
    # ---------------- (b) cert rows ----------------
    C = json.load(open(OPT['cert'])); OUTJ['cert'] = OPT['cert']; OUTJ['cert_md5'] = hashlib.md5(open(OPT['cert'], 'rb').read()).hexdigest()
    RR = [(c, int(c['row'][1]), c['row'][2], c['row'][3]) for c in C if c['row'][0] == 'receiverR2' and int(c['row'][1]) in (7, 8)]
    chg = []; up = 0; nempty = 0; npairs = 0; nwin = 0; ndp = 0; bfn = 0; bfskip = 0; bfbad = 0; T0 = _tm.time(); tp1 = 0.0
    BFCAP = int(os.environ.get('P1R_BF', '4000')); newst = collections.Counter(); win_lt = 0
    for c, d, lk, sv in RR:
        w = [int(ch) for ch in lk]; s = [int(ch) for ch in sv]
        base = _orig_recv_coef_R2_gk(d, lk, sv, xon)
        cur = _p1r_gk_recv_terms_cur(d, w, s)
        t_ = _tm.time(); r = p1r_core(d, w, s, _GK_UM, _GK_VM, _GK_M, base_cf=base); tp1 += _tm.time() - t_
        new = p1r_recv_terms(d, w, s, base)
        if r['empty']: nempty += 1; assert new == cur; continue
        ndp += r['ndp'] > 0
        pic = r['poss'] - r['pay']
        for k, nm in enumerate(GKNAMES):
            npairs += 1
            cv = int(cur.get(('ks', nm), 0)); pv = int(r['inmax'][k] - r['pay'][k]); assert int(new.get(('ks', nm), 0)) == pv
            if d == 8:   # current = gkwin window bound; also the KEYSPEC picture
                nwin += 1; win_lt += cv < int(pic[k])
                if pv > int(pic[k]): bad += 1; log('  (b) p1r ABOVE the d = 8 picture %s %s' % (_rowstr(d, w, s), nm))
            else: assert cv == int(pic[k])
            if pv > cv: up += 1; bad += 1; log('  (b) p1r ABOVE current %s %s: %d > %d' % (_rowstr(d, w, s), nm, pv, cv))
            if isnew(nm): newst['pairs'] += 1; newst['changed'] += pv != cv; newst['above'] += pv > cv
            if pv != cv:
                chg.append(dict(row=_rowstr(d, w, s), w=c['w'], key=nm, current=cv, p1_r=pv, OUT=int(r['pay'][k]), IN_max=int(r['inmax'][k])))
            # brute force on every pair whose live slots read some private at a non-wildcard position (DP or sure-skip both checked)
            if r['poss'][k] and any(GKEYS[k]['m'][p_] != 31 for p_ in (2, 5, 6, 7)):
                b_ = _bf_inmax(d, w, s, GKEYS[k], r['dom'], BFCAP)
                if b_ is None: bfskip += 1
                else:
                    bfn += 1
                    if b_ != int(r['inmax'][k]):
                        bfbad += 1; bad += 1
                        if bfbad <= 5: log('  (b) BRUTE FORCE %s %s: brute %d, p1r %d' % (_rowstr(d, w, s), nm, b_, r['inmax'][k]))
    log('P1R-TEST (b): %d d = 7 / 8 receiver rows x %d keys = %d pairs (%d rows with an empty domain kept as is; %d rows needed the DP; p1r core %.2fs, %.2f ms/row)' % (
        len(RR), len(GKEYS), npairs, nempty, ndp, tp1, 1000 * tp1 / max(1, len(RR))))
    log('P1R-TEST (b): changed %d pairs by key %s; above current %d; d = 8 pairs %d (window < picture: %d)' % (len(chg), dict(collections.Counter(x['key'] for x in chg).most_common()), up, nwin, win_lt))
    log('P1R-TEST (b): brute force (gk_slots on exact pictures) %d pairs checked, %d mismatches, %d skipped (> %d realisations)' % (bfn, bfbad, bfskip, BFCAP))
    OUTJ['b'] = {'rows': len(RR), 'pairs': npairs, 'empty_rows': nempty, 'dp_rows': ndp, 'changed': len(chg), 'above_current': up, 'by_key': dict(collections.Counter(x['key'] for x in chg)),
                 'brute_force': {'checked': bfn, 'mismatch': bfbad, 'skipped': bfskip, 'cap': BFCAP}, 'changes': chg, 'ms_per_row': 1000 * tp1 / max(1, len(RR))}
    if NEWP: log('P1R-TEST (b) new keys %s: %s' % (NEWP, dict(newst))); OUTJ['b']['new_keys'] = dict(newst)
    ref = json.load(open(os.path.join(_KS2, 'p1r_changes.json')))
    R0 = {(x['row'], x['key']): (x['current'], x['p1_r'], x['OUT'], x['IN_max']) for x in ref['changes']}
    R1 = {(x['row'], x['key']): (x['current'], x['p1_r'], x['OUT'], x['IN_max']) for x in chg if not isnew(x['key'])}
    only0 = sorted(set(R0) - set(R1)); only1 = sorted(set(R1) - set(R0)); diffv = sorted(k_ for k_ in set(R0) & set(R1) if R0[k_] != R1[k_])
    same = not only0 and not only1 and not diffv
    log('P1R-TEST (b) vs p1r_changes.json (%d changes, md5 %s): %s; only W6b %d %s; only ours %d %s; values differ %d %s' % (len(R0), hashlib.md5(open(os.path.join(_KS2, 'p1r_changes.json'), 'rb').read()).hexdigest()[:8],
        'IDENTICAL' if same else 'DIFFERENT', len(only0), only0[:5], len(only1), only1[:5], len(diffv), diffv[:5]))
    bad += not same; OUTJ['b']['vs_w6b'] = {'identical': same, 'only_w6b': only0, 'only_ours': only1, 'values_differ': diffv}
    # optional: setup cost on a warm rows file
    if os.environ.get('P1R_WARM'):
        nw = 0; tw = 0.0; tc = 0.0; ndw = 0; seen = set()
        for line in open(os.environ['P1R_WARM']):
            m_ = re.match(r'^R ([78]) (\d+) (\d+)', line)
            if not m_ or (m_.group(2), m_.group(3)) in seen or admissible(int(m_.group(1)), m_.group(2), m_.group(3)) is not None: continue
            seen.add((m_.group(2), m_.group(3))); d = int(m_.group(1)); lk, sv = m_.group(2), m_.group(3); w = [int(ch) for ch in lk]; s = [int(ch) for ch in sv]
            t_ = _tm.time(); b0 = _orig_recv_coef_R2_gk(d, lk, sv, xon); c0 = _p1r_gk_recv_terms_cur(d, w, s); tc += _tm.time() - t_
            t_ = _tm.time(); r = p1r_core(d, w, s, _GK_UM, _GK_VM, _GK_M, base_cf=b0); tw += _tm.time() - t_; nw += 1; ndw += (not r['empty']) and r['ndp'] > 0
            if not r['empty']:
                for k, nm in enumerate(GKNAMES):
                    if int(r['inmax'][k] - r['pay'][k]) > int(c0.get(('ks', nm), 0)): bad += 1; log('  warm: p1r ABOVE current %s %s' % (_rowstr(d, w, s), nm))
            if nw >= int(os.environ.get('P1R_WARMN', '3000')): break
        log('P1R-TEST warm %s: %d distinct admissible d = 7 / 8 rows: base row + current keys %.2f ms/row, p1r core %.2f ms/row (%d with DP); no p1r coefficient above current' % (
            os.environ['P1R_WARM'], nw, 1000 * tc / max(1, nw), 1000 * tw / max(1, nw), ndw))
        OUTJ['warm'] = {'file': os.environ['P1R_WARM'], 'rows': nw, 'ms_base_cur': 1000 * tc / max(1, nw), 'ms_p1r': 1000 * tw / max(1, nw), 'dp_rows': ndw}
    # ---------------- (c) restricted primal LP ----------------
    if os.environ.get('P1R_LP', '1') != '0':
        SR = {(wd, tuple(map(str, b))): cf for wd, cf, b in R2_sender_rows()}
        def caps(k):
            if k[0] in ('x', 'xo'): return float(OPT.get('xcap', '3'))
            if k[0] == 'D': return float(OPT.get('dcap', '3'))
            if k[0] == 'fb' and FBCAP is not None: return float(OPT['fbcap'])
            if k[0] == 'lq': return float(OPT.get('lqcap', '3'))
            if ZR and k[0] in ('z', 'zr', 'rr'): return float(OPT.get('zcap', '3'))
            if k[0] == 'z6': return float(OPT.get('z6cap', '3'))
            if k[0] == 'q' and Q7CAP is not None: return float(OPT['q7cap'])
            if k[0] == 'ks': return float(OPT.get('kscap', '3'))
            return None
        def rows_of(p1):
            out = []
            for c in C:
                row = c['row']; kd = row[0]
                if kd == 'senderR2': out.append((dict(SR[(row[1], tuple(map(str, row[2])))]), 1, 1, 'ge'))
                elif kd == 'cons2': out.append((dict(cons2_coef(tuple(row[1]), tuple(row[2]))), -1, 0, 'le'))
                elif kd == 'mrowR2': out.append(({('h', tuple(row[2])): 1, ('M', tuple(row[1])): -1}, 0, 0, 'le'))
                elif kd == 'mrowQ': out.append(({('q', tuple(row[2])): 1, ('Q', tuple(row[1])): -1}, 0, 0, 'le'))
                elif kd == 'mrowL': out.append(({('lq', tuple(row[2])): 1, ('lQ', tuple(row[1])): -1}, 0, 0, 'le'))
                elif kd == 'receiverR2':
                    d, lk, sv = int(row[1]), row[2], row[3]
                    if p1: cf = dict(recv_coef_R2(d, lk, sv, xon))   # the p1r engine path
                    else:
                        cf = collections.Counter(_orig_recv_coef_R2_gk(d, lk, sv, xon))
                        for k_, v_ in _p1r_gk_recv_terms_cur(d, [int(ch) for ch in lk], [int(ch) for ch in sv]).items(): cf[k_] += v_
                        cf = {k_: v_ for k_, v_ in cf.items() if v_}
                    out.append((cf, -1, d - 6, 'le'))
                else: raise Exception('p1r_test: row type %s not handled' % kd)
            return out
        def solve(rs, name):
            cols = {('t',): 0}
            for r in rs:
                for k in r[0]: cols.setdefault(k, len(cols))
            I, J, V, b = [], [], [], []
            for i, (cf, tc, dc, se) in enumerate(rs):
                sg = -1.0 if se == 'ge' else 1.0
                for k, v in cf.items():
                    if v: I.append(i); J.append(cols[k]); V.append(sg * v)
                if tc: I.append(i); J.append(0); V.append(sg * tc)
                b.append(sg * dc)
            A_ = _sp.csr_matrix((V, (I, J)), shape=(len(rs), len(cols)))
            bnd = [(None, None)] + [(0, caps(k)) for k in list(cols)[1:]]
            c_ = np.zeros(len(cols)); c_[0] = 1.0
            res = _lp(c_, A_ub=A_, b_ub=np.array(b), bounds=bnd, method='highs')
            tv = float(res.x[0]) if res.status == 0 else float('nan')
            if os.environ.get('P1R_LPDUMP'):   # the LP itself, for re-solves with other HiGHS settings
                lb_ = np.array([-np.inf if l_ is None else l_ for l_, u_ in bnd]); ub_ = np.array([np.inf if u_ is None else u_ for l_, u_ in bnd])
                _sp.save_npz(os.path.join(os.environ['P1R_LPDUMP'], 'lp_%s_A.npz' % name), A_.tocsr()); np.savez(os.path.join(os.environ['P1R_LPDUMP'], 'lp_%s_b.npz' % name), b=np.array(b), lb=lb_, ub=ub_, cols=np.array([repr(k) for k in cols]))
            ku = sorted(((float(res.x[i]), k[1]) for k, i in cols.items() if k[0] == 'ks' and res.status == 0 and res.x[i] > 1e-9), reverse=True)[:12]
            log('P1R-TEST (c) %-8s rows %d cols %d: status %d (%s) t = %.12g; top key amounts %s' % (name, len(rs), len(cols), res.status, res.message[:40], tv, ' '.join('%s=%.4g' % (k, v) for v, k in ku)))
            # the default HiGHS solve stops within its 1e-7 tolerances; the p1r LP (t ~ 1e-4, keys at their cap) is sensitive to that, so
            # re-solve with dual simplex and IPM at 1e-10 tolerances and report the worst row violation of each point
            alt = {}
            for meth in ('highs-ds', 'highs-ipm'):
                r2 = _lp(c_, A_ub=A_, b_ub=np.array(b), bounds=bnd, method=meth, options={'primal_feasibility_tolerance': 1e-10, 'dual_feasibility_tolerance': 1e-10})
                alt[meth] = {'status': int(r2.status), 't': float(r2.x[0]) if r2.status == 0 else float('nan'), 'max_row_violation': float(max(0.0, (A_ @ r2.x - np.array(b)).max())) if r2.status == 0 else None}
            log('P1R-TEST (c) %-8s tight tolerances (1e-10): dual simplex t = %.12g (row viol %.2g), IPM t = %.12g (row viol %.2g); default-solve row viol %.2g' % (name,
                alt['highs-ds']['t'], alt['highs-ds']['max_row_violation'], alt['highs-ipm']['t'], alt['highs-ipm']['max_row_violation'], float(max(0.0, (A_ @ res.x - np.array(b)).max()))))
            return {'t': tv, 'status': int(res.status), 'rows': len(rs), 'cols': len(cols), 'top_keys': [[k, v] for v, k in ku], 'tight': alt}
        OUTJ['c'] = {'current': solve(rows_of(False), 'current'), 'p1r': solve(rows_of(True), 'p1r')}
    log('P1R-STAT %s' % dict(P1R_STAT))
    log('P1R-TEST: %s (%d failures)' % ('PASS' if bad == 0 else 'FAIL', bad)); OUTJ['failures'] = bad
    if os.environ.get('P1R_OUT'): json.dump(OUTJ, open(os.environ['P1R_OUT'], 'w'), indent=1, default=str)
