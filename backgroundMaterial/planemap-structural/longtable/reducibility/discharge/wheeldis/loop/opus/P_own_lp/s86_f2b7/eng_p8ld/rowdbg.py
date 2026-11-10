# rowdbg.py (s86): exec'd by pcheck_dbg.py (ROWDBG=eng/rowdbg.py ROWS=<file of "d link sv" lines>); upperR2 ... f2bself=1 then dumps each row: python LP-row terms (recv_coef_R2) vs jsepf leaf
def f2b_selftest(y, xd, MV2, t, N):
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
        if k[0] == 'V': return min([VV.get(kk, 0.0) for kk in sigv_keys(k[1])] or [0.0])
        if k[0] == 'D': return DV.get(k[1], 0.0)
        if k[0] == 'fb': return FBV.get(k[1], 0.0)
        raise Exception('rowdbg: unsupported key %s' % (k,))
    rows = [l.split() for l in open(os.environ['ROWS']) if l.strip()]
    for d in sorted({int(r[0]) for r in rows}):
        arr = [(r[1], r[2]) for r in rows if int(r[0]) == d]
        U = min(d, 9); W = window_table_R2(U, y, xd, MV2)
        ef = os.path.join(WORK, 'rowdbg_d%d.txt' % d); open(ef, 'w').write(''.join('%s %s\n' % a for a in arr))
        F2B_EVAL[0] = ef; rr, dt, ni = run_sep(d, W, 1e9, 1, 0); F2B_EVAL[0] = None
        cpp = [float(r[1]) for r in rr if r[0] == 'E']
        for (lk, sv), c in zip(arr, cpp):
            cf = recv_coef_R2(d, lk, sv, 'xon' in FLAGS)
            pv = sum(v * val(k) for k, v in cf.items())
            log('ROWDBG d=%d %s %s: python %.9f cpp %.9f diff %.3g thr %.9f admissible=%s' % (d, lk, sv, pv, c, c - pv, d - 6 + t, admissible(d, lk, sv)))
            for k, v in sorted(cf.items(), key=str):
                if abs(v * val(k)) > 1e-12 or k[0] in ('Q', 'lQ', 'M'): log('   %+g * %.9f  %s' % (v, val(k), k))
    log('ROWDBG done')
