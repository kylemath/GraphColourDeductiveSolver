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
PMF = {f: _fg['model'](f, m) for f, m in PM.items() if not (m in ('tree', 'sel') or m.startswith('treefile:'))}
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
            if LAZYB:
                r_ = pm_bound_row(k[0], k[1])
                if r_: PMBQ.append(r_)
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
LAZYB = 'lazyb' in FLAGS; PMBSEEN = set(); PMBQ = []
SEL = {f for f, m in PM.items() if m == 'sel'}
def pm_bound_row(fam, k):
    ph = phi(fam, k)
    if not ph and fam not in SEL: return None
    sig = (fam, 'key', k) if fam in SEL else (fam, tuple(sorted(ph.items(), key=str)))   # sel: one (possibly empty) row per key, so new columns can enter it
    if sig in PMBSEEN: return None
    PMBSEEN.add(sig); hi = PMCAP[fam]() if fam in PMCAP else None
    return ({('th', fam, f): c for f, c in ph.items()}, 0.0, hi, ('pmbound', fam, repr(k)))
def pm_lazy_check(PMV):
    """lazyb: bound rows of every universe key whose modelled value is outside its bounds"""
    out = []
    for fam, V in PMV.items():
        hi = PMCAP[fam]() if fam in PMCAP else None
        for k, v in V.items():
            if v < -1e-10 or (hi is not None and v > hi + 1e-10):
                r = pm_bound_row(fam, k)
                if r: out.append(r)
    return out
def pm_bound_rows():
    """[(cf over theta, lo, hi, label)] : one row per distinct feature vector of each modelled family"""
    out = []
    if LAZYB:
        PMBSEEN.clear(); log('pm: lazy bound rows (keys in rows + violated universe keys)'); return out
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
# ---------------- s54 tree growth (pm=fam:tree): data-driven partition refinement by LP duals ----------------
# Each 'tree' family is piecewise constant on the leaves of a binary tree whose tests are "key position p == v" or
# "key position p <= v" on the raw canonical key (x: decoded to fl, tl, c1, a1, b1, c2, a2, b2).  At each converged LP
# (no violated row) the duals give every key's gradient G_k = sum_rows dual_r * a_rk; splitting leaf l into K1 / K2 gives
# new columns with reduced costs d1 = -sum_K1 G, d2 = -sum_K2 G.  The split with the largest first-order gain is taken
# (top `gk` per round, distinct leaves), the LP is rebuilt over all rows so far, and separation resumes.
PMROWS = []; PMROWIX = []
TREES = {}; NLEAF = {}
GROWMAX = int(OPT.get('growmax', '0')); GK = int(OPT.get('gk', '12')); GPF = int(OPT.get('gpf', '3')); GPAIR = int(OPT.get('gpair', '0')); GTARGET = float(OPT.get('gtarget', '-1'))
def keytup(fam, k):
    if fam == 'x':
        fl, tl, s1, s2 = _fg['x_dec'](k); return (fl, tl) + s1 + s2
    return tuple(k)
def tree_leaf(node, kt):
    while 'leaf' not in node:
        p, op, v = node['p'], node['op'], node['v']; val = kt[p] if p < len(kt) else -1
        node = node['T'] if ((val == v) if op == 'eq' else (val <= v)) else node['F']
    return node['leaf']
def _mk_tree_model(fam):
    return lambda k: {('leaf', tree_leaf(TREES[fam], keytup(fam, k))): 1}
for _f, _m in list(PM.items()):
    if _m == 'tree' or _m.startswith('treefile:'):
        TREES[_f] = json.load(open(_m[9:])) if _m.startswith('treefile:') else {'leaf': 0}
        def _nl(n): return 1 if 'leaf' in n else _nl(n['T']) + _nl(n['F'])
        def _ml(n): return n['leaf'] if 'leaf' in n else max(_ml(n['T']), _ml(n['F']))
        NLEAF[_f] = _ml(TREES[_f]) + 1; PMF[_f] = _mk_tree_model(_f)
def tree_str(node, fam, ind=''):
    if 'leaf' in node: return '%sleaf %d\n' % (ind, node['leaf'])
    return '%sif k[%d] %s %d:\n%s%selse:\n%s' % (ind, node['p'], '==' if node['op'] == 'eq' else '<=', node['v'], tree_str(node['T'], fam, ind + '  '), ind, tree_str(node['F'], fam, ind + '  '))
def _count(n): return 1 if 'leaf' in n else _count(n['T']) + _count(n['F'])
def pm_snapshot(fn, t, xv, cols, extra=None):
    TH = {k[1:]: float(xv[i]) for k, i in cols.items() if k[0] == 'th'}
    S = {'t': float(t), 'model': 'R6x2', 'apex': AP, 'xon': 'xon' in FLAGS, 'apexcls': AC, 'hat5': H5, 'l3q': L3Q, 'zh': ZH, 'fy': FY, 'fy2': FY2}
    for fam in ('y', 'g', 'h', 'x', 'r', 'lq', 'lQ'):
        if fam in PM: V_ = pm_values(fam, TH)
        else: V_ = {k[1]: float(xv[i]) for k, i in cols.items() if k[0] == fam}
        if fam == 'y': S['y'] = {rname(k): float(v) for k, v in V_.items() if v > 0}
        elif fam == 'x': S['x'] = {str(k): float(v) for k, v in V_.items() if v > 0}
        else: S[fam] = [[list(k), float(v)] for k, v in V_.items() if v > 0]
    S['pm'] = PM; S['theta'] = [[f[0], repr(f[1]), v] for f, v in sorted(TH.items(), key=str)]
    S['trees'] = TREES
    if extra: S.update(extra)
    json.dump(S, open(fn, 'w'))
def pm_grow_step(h, cols, xv, t, info):
    """one growth round at a converged LP; returns the list of splits made (empty = stop)"""
    dual = np.array(h.getSolution().row_dual)
    G = collections.defaultdict(float)
    for (cf, lo, hi, inf_), ri in zip(PMROWS, PMROWIX):
        yv = dual[ri]
        if yv == 0.0: continue
        for k, v in cf.items():
            if k[0] in TREES: G[(k[0], k[1])] += yv * v
    TH = {k[1:]: float(xv[i]) for k, i in cols.items() if k[0] == 'th'}
    # check against HiGHS's own reduced costs of the leaf columns (bound rows add their dual)
    cd = np.array(h.getSolution().col_dual); worst = 0.0
    lg = collections.defaultdict(float)
    for (fam, k), g in G.items(): lg[(fam, tree_leaf(TREES[fam], keytup(fam, k)))] += g
    cands = []
    byleaf = collections.defaultdict(list)
    for (fam, k), g in G.items():
        if abs(g) > 1e-13: byleaf[(fam, tree_leaf(TREES[fam], keytup(fam, k)))].append((keytup(fam, k), g))
    seen_ = set()
    for (fam, lf), items in byleaf.items():
        tot = sum(g for _, g in items); th = TH.get((fam, ('leaf', lf)), 0.0)
        cap = PMCAP[fam]() if fam in PMCAP else None
        L = max(len(kt) for kt, _ in items)
        for p in range(L):
            vals = sorted({kt[p] if p < len(kt) else -1 for kt, _ in items})
            if len(vals) < 2: continue
            for op in ('eq', 'le'):
                for v in (vals if op == 'eq' else vals[:-1]):
                    if op == 'eq' and len(vals) == 2 and v == vals[1]: continue   # same split as eq vals[0]
                    K1 = frozenset(kt for kt, g in items if ((kt[p] if p < len(kt) else -1) == v if op == 'eq' else (kt[p] if p < len(kt) else -1) <= v))
                    sig_ = (fam, lf, min(K1, frozenset(kt for kt, _ in items) - K1, key=lambda z: sorted(z)))
                    if sig_ in seen_: continue
                    seen_.add(sig_)
                    s1 = sum(g for kt, g in items if kt in K1)
                    sc = 0.0
                    for d in (-s1, -(tot - s1)):   # reduced cost of each child
                        up = -d if (cap is None or th < cap - 1e-9) else 0.0
                        dn = d if th > 1e-9 else 0.0
                        sc = max(sc, up, dn)
                    if sc > 1e-12: cands.append((sc, fam, lf, p, op, v))
    cands.sort(key=lambda c: -c[0]); made = []; per = collections.Counter()
    for c in cands:   # strong-branching shortlist: the best GK candidates, at most GPF per family
        if per[c[1]] >= GPF: continue
        per[c[1]] += 1; made.append(c)
        if len(made) >= GK: break
    log('  grow: %d candidates; shortlist %s' % (len(cands), [(f, lf, p, op, v, round(sc, 4)) for sc, f, lf, p, op, v in made]))
    return made
def pm_apply(c):
    sc, fam, lf, p, op, v = c
    def _split(node, lf, p, op, v, fam):
        if 'leaf' in node:
            if node['leaf'] != lf: return node
            a = NLEAF[fam]; NLEAF[fam] += 1
            return {'p': p, 'op': op, 'v': v, 'T': {'leaf': lf}, 'F': {'leaf': a}}
        return {'p': node['p'], 'op': node['op'], 'v': node['v'], 'T': _split(node['T'], lf, p, op, v, fam), 'F': _split(node['F'], lf, p, op, v, fam)}
    TREES[fam] = _split(TREES[fam], lf, p, op, v, fam)
    for kk in [kk for kk in _phic if kk[0] == fam]: del _phic[kk]
def pm_state(): return (json.loads(json.dumps(TREES)), dict(NLEAF))
def pm_restore(st):
    TREES.clear(); TREES.update(json.loads(json.dumps(st[0]))); NLEAF.clear(); NLEAF.update(st[1]); _phic.clear()

# ---------------- s54 lasso path (lasso=LAMBDA): objective t + LAMBDA * sum_f |theta_f| over every modelled feature ----------------
LASSO = float(OPT.get('lasso', '0'))
def pm_abs_rows():
    out = []
    if not LASSO: return out
    for fam in PM:
        fs = sorted({f for k in pm_universe(fam) for f in phi(fam, k)}, key=str)
        for f in fs:
            out.append(({('ab', fam, f): 1.0, ('th', fam, f): -1.0}, 0.0, None, ('pmabs', fam, repr(f), '+')))
            out.append(({('ab', fam, f): 1.0, ('th', fam, f): 1.0}, 0.0, None, ('pmabs', fam, repr(f), '-')))
    log('lasso %g: %d |theta| rows' % (LASSO, len(out)))
    return out
# ---------------- s54 forward selection (pm=fam:sel): column generation over each family's feature dictionary ----------------
# The active features of a 'sel' family are its columns.  At each converged LP every dictionary feature f is priced exactly
# (reduced cost of the new column theta_f: d_f = -sum_rows dual_r * A_rf, bound rows included); the GK best |d_f| (at most
# GPF per family) are tried by adding the column to the LP and re-solving (warm), and the one that lowers t most is kept.
# If no single column helps, pairs among the GPAIR best are tried.  Then separation resumes (lazy bounds required).
SEL = {f for f, m in PM.items() if m == 'sel'}
ACTIVE = {f: set() for f in SEL}
_DC = {}
def _dmk(f):
    base = _fg['dict2_model'](f)
    def g(k):
        kk = (f, k)
        if kk not in _DC: _DC[kk] = base(k)
        return _DC[kk]
    return g
DICTF = {f: _dmk(f) for f in SEL}   # dict2, memoised
if 'selinit' in OPT:
    for fam, fs in json.load(open(OPT['selinit'])).items():
        if fam in SEL: ACTIVE[fam].update(eval(q) for q in fs)
def _mk_sel(fam):
    return lambda k: {q: c for q, c in DICTF[fam](k).items() if q in ACTIVE[fam]}
for _f in SEL: PMF[_f] = _mk_sel(_f)
assert not SEL or LAZYB, 'sel needs lazyb'
def sel_price(h, info):
    dual = np.array(h.getSolution().row_dual)
    G = collections.defaultdict(float)
    for (cf, lo, hi, inf_), ri in zip(PMROWS, PMROWIX):
        yv = dual[ri]
        if yv == 0.0: continue
        for k, v in cf.items():
            if k[0] in SEL: G[(k[0], k[1])] += yv * v
    for ri, inf_ in enumerate(info):
        if inf_[0] == 'pmbound' and inf_[1] in SEL and dual[ri] != 0.0: G[(inf_[1], eval(inf_[2]))] += dual[ri]
    d = collections.defaultdict(float)
    for (fam, k), g in G.items():
        if abs(g) < 1e-14: continue
        for q, c in DICTF[fam](k).items():
            if q not in ACTIVE[fam]: d[(fam, q)] -= c * g
    return d
def sel_column(fam, q, info):
    """the new column theta_(fam, q) over the current LP rows: (row indices, values)"""
    A = collections.defaultdict(float)
    for (cf, lo, hi, inf_), ri in zip(PMROWS, PMROWIX):
        for k, v in cf.items():
            if k[0] == fam:
                c = DICTF[fam](k[1]).get(q)
                if c: A[ri] += v * c
    for ri, inf_ in enumerate(info):
        if inf_[0] == 'pmbound' and inf_[1] == fam:
            c = DICTF[fam](eval(inf_[2])).get(q)
            if c: A[ri] += c
    idx = np.array(sorted(A), dtype=np.int32); val = np.array([A[i] for i in idx])
    return idx, val
def sel_columns(cands, info):
    """all new columns of cands in one pass over the rows: {(fam, q): (idx, val)}"""
    want = collections.defaultdict(set)
    for fam, q in cands: want[fam].add(q)
    A = {c: collections.defaultdict(float) for c in cands}
    for (cf, lo, hi, inf_), ri in zip(PMROWS, PMROWIX):
        for k, v in cf.items():
            if k[0] in want:
                for q, c in DICTF[k[0]](k[1]).items():
                    if q in want[k[0]]: A[(k[0], q)][ri] += v * c
    for ri, inf_ in enumerate(info):
        if inf_[0] == 'pmbound' and inf_[1] in want:
            for q, c in DICTF[inf_[1]](eval(inf_[2])).items():
                if q in want[inf_[1]]: A[(inf_[1], q)][ri] += c
    out = {}
    for c_, M in A.items():
        idx = np.array(sorted(M), dtype=np.int32); out[c_] = (idx, np.array([M[i] for i in idx]))
    return out
SELCOL = {}
def sel_try(h, jt, cands, info):
    """add the columns of cands at once, solve, read t, delete them again"""
    import highspy
    n0 = h.getNumCol()
    for fam, q in cands:
        idx, val = SELCOL[(fam, q)] if (fam, q) in SELCOL else sel_column(fam, q, info); h.addCol(0.0, -highspy.kHighsInf, highspy.kHighsInf, len(idx), idx, val)
    h.run()
    ok = h.getModelStatus() == highspy.HighsModelStatus.kOptimal
    tc = h.getSolution().col_value[jt] if ok else 1e9
    h.deleteCols(len(cands), np.arange(n0, n0 + len(cands), dtype=np.int32))
    return tc
GBLOCK = int(OPT.get('gblock', '0'))
def sel_block_pool(d):
    """candidates for a block step: the GBLOCK best priced features + every non-'full' (non per-key) dictionary feature"""
    pool = [fq for fq, v in sorted(d.items(), key=lambda kv: -abs(kv[1]))[:GBLOCK]]
    seen = set(pool)
    for fam in [f for f in OPT.get('gbfam', 'y,g,h').split(',') if f in SEL]:
        fs = set()
        for k in pm_universe(fam):
            for q in DICTF[fam](k):
                if q[0] != 'K' and q not in ACTIVE[fam] and not (fam == 'x' and len(q) == 6): fs.add(q)
        for q in sorted(fs, key=str):
            if (fam, q) not in seen: seen.add((fam, q)); pool.append((fam, q))
    return pool
def sel_block(h, jt, t, d, info):
    """plateau: lasso over a candidate pool (penalty only on new columns); the first lambda that lowers t gives the block"""
    import highspy
    inf = highspy.kHighsInf; pool = sel_block_pool(d); t_ = time.time()
    n0 = h.getNumCol(); m0 = h.getNumRow()
    CC = sel_columns(pool, info); log('    block: %d columns built in %.0fs' % (len(CC), time.time() - t_))
    for fam, q in pool:
        idx, val = CC[(fam, q)]; h.addCol(0.0, -inf, inf, len(idx), idx, val)
    nn = len(pool)
    for i in range(nn): h.addCol(1.0, 0.0, inf, 0, np.array([], dtype=np.int32), np.array([]))   # u_i >= |theta_i|
    for i in range(nn):
        h.addRow(0.0, inf, 2, np.array([n0 + nn + i, n0 + i], dtype=np.int32), np.array([1.0, -1.0]))
        h.addRow(0.0, inf, 2, np.array([n0 + nn + i, n0 + i], dtype=np.int32), np.array([1.0, 1.0]))
    out = ([], 1e9)
    h.setOptionValue('solver', 'ipm')
    for lam in [float(x) for x in OPT.get('gblam', '1e-3,1e-4').split(',')]:
        for i in range(nn): h.changeColCost(n0 + nn + i, lam)
        h.run()
        if h.getModelStatus() != highspy.HighsModelStatus.kOptimal: continue
        xv_ = np.array(h.getSolution().col_value); th = xv_[n0:n0 + nn]
        sel_ = [pool[i] for i in range(nn) if abs(th[i]) > 1e-9]
        log('    block lambda %g: t %.9f with %d new columns' % (lam, xv_[jt], len(sel_)))
        if xv_[jt] < t - 1e-6 and sel_: out = (sel_, xv_[jt]); break
    h.setOptionValue('solver', 'simplex')
    h.deleteRows(2 * nn, np.arange(m0, m0 + 2 * nn, dtype=np.int32)); h.deleteCols(2 * nn, np.arange(n0, n0 + 2 * nn, dtype=np.int32))
    log('    block over %d candidates (%.0fs): %s' % (nn, time.time() - t_, out[0][:20]))
    return out
def sel_step(h, jt, t, info):
    t_ = time.time(); d = sel_price(h, info)
    ranked = sorted(d.items(), key=lambda kv: -abs(kv[1]))
    short = []; per = collections.Counter()
    for (fam, q), v in ranked:
        if abs(v) < 1e-10: break
        if per[fam] >= GPF: continue
        per[fam] += 1; short.append(((fam, q), v))
        if len(short) >= GK: break
    log('  sel: %d priced features with |d| > 0; shortlist %s' % (sum(1 for v in d.values() if abs(v) > 1e-10), [(f, q, round(v, 4)) for (f, q), v in short[:12]]))
    res = []; SELCOL.clear(); SELCOL.update(sel_columns([c for c, _ in short], info))
    for (fam, q), v in short:
        tc = sel_try(h, jt, [(fam, q)], info); res.append((tc, (fam, q)))
        log('    try %s %s (d %.4g): t = %.9f' % (fam, q, v, tc))
    res.sort(key=lambda r: r[0]); pick = [res[0][1]] if res else []; tb = res[0][0] if res else 1e9
    if (not res or tb > t - 1e-9) and GPAIR:
        top = [c for c, _ in short[:GPAIR]]; bp = (tb, None)
        for i_ in range(len(top)):
            for j_ in range(i_ + 1, len(top)):
                tc = sel_try(h, jt, [top[i_], top[j_]], info)
                if tc < bp[0] - 1e-9: bp = (tc, [top[i_], top[j_]])
        log('    pair lookahead over %d: best t %.9f %s' % (len(top), bp[0], bp[1]))
        if bp[1]: pick = bp[1]; tb = bp[0]
    if (not pick or tb > t - 1e-9) and GBLOCK:
        pick, tb = sel_block(h, jt, t, d, info)
    elif tb > t - 1e-9: pick = []
    for fam, q in pick:
        ACTIVE[fam].add(q)
        for kk in [kk for kk in _phic if kk[0] == fam]: del _phic[kk]
    log('  sel: added %s (LP t %.9f, was %.9f; %.0fs); active %s' % (pick, tb, t, time.time() - t_, {f: len(ACTIVE[f]) for f in SEL}))
    return pick
