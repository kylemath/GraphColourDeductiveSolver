# consdbg.py (s86): exec'd by eng/pcheck_dbg.py (ROWDBG=consdbg.py CONSL="7,7,8,9,7,9;6,7,7,7,8,9"); run upperR2 ... f2bself=1.
# For each link L in CONSL: the c6le conservation value in - out at its worst apex words, and the row's terms (column, coefficient, value).
def f2b_selftest(y, xd, MV2, t, N):
    Sj = json.load(open(OPT['sol']))
    GV = {tuple(k): v for k, v in Sj['g']}; HV2 = {tuple(k): v for k, v in Sj['h']}
    def val(k):
        f = k[0]
        if f == 'g': return GV.get(k[1], 0.0)
        if f == 'h': return HV2.get(k[1], 0.0)
        if f == 'v': return VV.get(k[1], 0.0)
        if f == 'ks': return KSV.get(k[1], 0.0)
        if f == 'fb': return FBV.get(k[1], 0.0)
        if f == 'z6': return Z6V.get(k[1], 0.0)
        if f == 'Z6': return Z6W.get(k[1], 0.0)
        raise Exception('consdbg: unsupported key %s' % (k,))
    for Ls in os.environ['CONSL'].split(';'):
        L = tuple(int(c) for c in Ls.split(','))
        D = cons2_delta(L, GV, HV2); order = np.argsort(-D)
        log('CONSDBG L=%s t=%.12f max(in-out)=%.12f excess %.3g; apex words above t: %d' % (L, t, float(D[order[0]]), float(D[order[0]]) - t, int((D > t + 1e-9).sum())))
        for idx in order[:int(os.environ.get('CONSN', '3'))]:
            s = tuple(LET[v] for v in SALL[idx]); cf = cons2_coef(L, s)
            tot = sum(c * val(k) for k, c in cf.items())
            log('  s=%s in-out %.12f (row sum %.12f)' % (''.join(map(str, s)), float(D[idx]), tot))
            for k, c in sorted(cf.items(), key=lambda kc: -abs(kc[1] * val(kc[0]))):
                v_ = val(k)
                if v_: log('    %+d x %s = %.9f' % (c, k, v_))
