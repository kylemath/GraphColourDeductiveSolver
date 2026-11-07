# unmask.py (s86): exec'd by eng/pcheck_dbg.py (ROWDBG=unmask.py); replaces lowerR2 by a float diagnostic on a phase-1 cert's rows.
# The restricted primal LP (min t over exactly the cert's rows, columns capped as lowerR2 prices them) is solved as is (baseline,
# which must give the cert's t1), then with chosen l3q signatures unmasked: every receiver row holding ('lQ', sg) for sg in the set
# is replaced by one copy per hidden letter l of sg's mask, with lQ(sg) -> lq(sg[:2] + (l,)) (all combinations if several), and
# the mrowL rows of those signatures are dropped.  A restricted LP is a valid lower bound for its own model, so t > 0 after
# unmasking means a receiver that sees the letter still cannot reach 0 on these rows.
# Env UNMASK: comma list of variants: none | pair66 (lQ (6,6,30), (6,6,31)) | L (every 3-letter lQ signature) | a;b;mask (one sig).
import itertools as _it
def cmd_lowerR2():
    import scipy.sparse as _sp
    from scipy.optimize import linprog as _lp
    load_patterns()
    xon = 'xon' in FLAGS; C = json.load(open(OPT['cert']))
    SR = {(wd, tuple(map(str, b))): cf for wd, cf, b in R2_sender_rows()}
    rows = []   # (kind, cf dict, tc, dc, sense) ; sense 'ge' for senders (cf + t >= 1), 'le' otherwise (cf + tc t <= dc)
    for c in C:
        row = c['row']; kd = row[0]
        if kd == 'senderR2': rows.append((kd, None, dict(SR[(row[1], tuple(map(str, row[2])))]), 1, 1, 'ge'))
        elif kd == 'cons2': rows.append((kd, None, dict(cons2_coef(tuple(row[1]), tuple(row[2]))), -1, 0, 'le'))
        elif kd == 'mrowR2': rows.append((kd, None, {('h', tuple(row[2])): 1, ('M', tuple(row[1])): -1}, 0, 0, 'le'))
        elif kd == 'mrowQ': rows.append((kd, None, {('q', tuple(row[2])): 1, ('Q', tuple(row[1])): -1}, 0, 0, 'le'))
        elif kd == 'mrowL': rows.append((kd, tuple(row[1]), {('lq', tuple(row[2])): 1, ('lQ', tuple(row[1])): -1}, 0, 0, 'le'))
        elif kd == 'receiverR2':
            d, lk, sv = int(row[1]), row[2], row[3]; tau = None
            if FY2: tau = dict(fy2_cells(d, [int(ch) for ch in lk], [int(ch) for ch in sv]))[row[4]]
            rows.append((kd, None, dict(recv_coef_R2(d, lk, sv, xon, tau)), -1, d - 6, 'le'))
        else: raise Exception('unmask: row type %s not handled' % kd)
    lqsigs = sorted({k[1] for r in rows for k in r[2] if k[0] == 'lQ' and len(k[1]) == 3})
    log('UNMASK: %d cert rows %s; 3-letter lQ signatures in receiver rows: %d' % (len(rows), dict(collections.Counter(r[0] for r in rows)), len(lqsigs)))
    sgn = collections.Counter((r[0], 'pos' if v > 0 else 'neg') for r in rows for k, v in r[2].items() if k[0] == 'lQ')
    log('UNMASK: lQ coefficient signs by row type: %s' % dict(sgn))
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
    def solve(rs, name):
        cols = {('t',): 0}
        for r in rs:
            for k in r[2]: cols.setdefault(k, len(cols))
        I, J, V, b = [], [], [], []
        for i, (kd, _, cf, tc, dc, se) in enumerate(rs):
            sg = -1.0 if se == 'ge' else 1.0   # cf + tc t >= dc  ->  -cf - tc t <= -dc
            for k, v in cf.items():
                if v: I.append(i); J.append(cols[k]); V.append(sg * v)
            if tc: I.append(i); J.append(0); V.append(sg * tc)
            b.append(sg * dc)
        A = _sp.csr_matrix((V, (I, J)), shape=(len(rs), len(cols)))
        bnd = [(None, None)] + [(0, caps(k)) for k in list(cols)[1:]]
        c_ = np.zeros(len(cols)); c_[0] = 1.0
        res = _lp(c_, A_ub=A, b_ub=np.array(b), bounds=bnd, method='highs')
        tv = res.x[0] if res.status == 0 else float('nan')
        log('UNMASK %-12s rows %6d cols %6d: status %d (%s) t = %.12f' % (name, len(rs), len(cols), res.status, res.message[:40], tv))
        return tv
    for var in os.environ.get('UNMASK', 'none,pair66,L').split(','):
        if var == 'none': S = set()
        elif var == 'pair66': S = {(6, 6, 30), (6, 6, 31)}
        elif var == 'L': S = set(lqsigs)
        else: S = {tuple(int(v) for v in var.split(';'))}
        out = []; nsplit = 0
        for r in rows:
            kd, msg, cf, tc, dc, se = r
            if kd == 'mrowL' and msg in S: continue
            hid = [k for k in cf if k[0] == 'lQ' and k[1] in S]
            if hid and kd != 'receiverR2': log('UNMASK WARNING: %s row holds unmasked %s' % (kd, hid))
            if kd != 'receiverR2' or not hid: out.append(r); continue
            nsplit += 1
            for lets in _it.product(*[l3q_mask_letters(k[1][2]) for k in hid]):
                cf2 = dict(cf)
                for k, l in zip(hid, lets):
                    v = cf2.pop(k); kk = ('lq', k[1][:2] + (l,)); cf2[kk] = cf2.get(kk, 0) + v
                out.append((kd, None, cf2, tc, dc, se))
        log('UNMASK %s: %d signatures unmasked, %d receiver rows split, %d mrowL rows dropped' % (var, len(S), nsplit, sum(1 for r in rows if r[0] == 'mrowL' and r[1] in S)))
        solve(out, var)
