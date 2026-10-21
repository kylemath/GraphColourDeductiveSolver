# s54 pmodel.py: parametric families for solveR2 (exec'd in pcheck.py after prelay2.py).
# Option pm=fam:model,... (fam in y g h x r lq; model from ../feats.py, 'free' = original columns, 'zero' = family off).
# A modelled family has no own columns: w[key] = sum_f theta[fam, f] * phi_f(key); every row's coefficient on a key is
# spread onto the theta columns.  Bounds of the family (>= 0; <= cap for x, lq) are rows over the whole key universe,
# one row per distinct feature vector.  After each LP the family is evaluated on its whole universe, so separation and
# the written sol see exactly the rule the model defines.
_fp = OPT.get('feats', os.path.join(HERE, '..', 'feats.py')); _fg = {}
exec(open(_fp).read(), _fg)
PM = {}
for _it in [s for s in OPT.get('pm', '').split(',') if s]:
    _f, _m = _it.split(':', 1)
    if _m != 'free': PM[_f] = _m
PMF = {f: _fg['model'](f, m) for f, m in PM.items()}
_phic = {}
def phi(fam, key):
    k_ = (fam, key)
    if k_ not in _phic: _phic[k_] = PMF[fam](key)
    return _phic[k_]
def pm_expand(cf):
    if not PM: return cf
    out = collections.Counter()
    for k, v in cf.items():
        if k[0] in PM:
            for f, c in phi(k[0], k[1]).items(): out[('th', k[0], f)] += v * c
        else: out[k] += v
    return {k: v for k, v in out.items() if v != 0}
UNIV = {}; _SRC = []
def _sr():
    if not _SRC: _SRC.append(R2_sender_rows())
    return _SRC[0]
def pm_universe(fam):
    if fam in UNIV: return UNIV[fam]
    U = set()
    if fam == 'y': U = set(ROOTS)
    elif fam in ('g', 'h'):
        for L in all6_words():
            for s in itertools.product((5, 7), repeat=6):
                for k, v in cons2_coef(L, s).items():
                    if k[0] == fam: U.add(k[1])
        if fam == 'g':
            for wd, cf, bits in _sr():
                for k in cf:
                    if k[0] == 'g': U.add(k[1])
    elif fam == 'x':
        for fi in range(3):
            for ti in range(3):
                for lo in range(125):
                    for hi in range(lo, 125): U.add(((fi * 3 + ti) * 125 + lo) * 125 + hi)
    elif fam == 'r':
        for b_, c_, e_, f_, q_, s2 in itertools.product(LET, repeat=6): U.add(h5_recv(b_, c_, e_, f_, q_, s2))
        for wd, cf, bits in _sr():
            for k in cf:
                if k[0] == 'r': U.add(k[1])
    elif fam == 'lq':
        for c_ in (5, 6):
            for a_ in (5, 6):
                for a2 in LET:
                    U.add((c_, a_, a2))
                    for V in LQVX: U.add((V, c_, a_, a2))
    UNIV[fam] = sorted(U, key=str); return UNIV[fam]
PMCAP = {'x': lambda: float(OPT.get('xcap', '3')), 'lq': lambda: LQCAP}
def pm_bound_rows():
    """[(cf over theta, lo, hi, label)] : one row per distinct feature vector of each modelled family"""
    out = []
    for fam in PM:
        seen = set(); hi = PMCAP[fam]() if fam in PMCAP else None
        for k in pm_universe(fam):
            ph = phi(fam, k)
            if not ph: continue
            sig = tuple(sorted(ph.items(), key=str))
            if sig in seen: continue
            seen.add(sig); out.append(({('th', fam, f): c for f, c in ph.items()}, 0.0, hi, ('pmbound', fam, repr(k))))
        log('pm: family %s model %s: %d keys in the universe, %d distinct feature vectors, %d features' % (fam, PM[fam], len(pm_universe(fam)), len(seen), len({f for k in pm_universe(fam) for f in phi(fam, k)})))
    return out
def pm_values(fam, TH):
    return {k: sum(c * TH.get((fam, f), 0.0) for f, c in phi(fam, k).items()) for k in pm_universe(fam)}
