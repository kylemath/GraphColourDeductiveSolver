# offc.py (Opus P_own_lp, round s39o): off-centre matching, spec in ../OFFC_SPEC.md.  exec'd by pcheck.load_patterns() under the
# offc flag only (flag off: this file is never read).  Every registry entry recorded in OFFREG is turned into its configuration K
# (OFFC_SPEC 2), every embedding of K anywhere in the known 1.5-ball of a degree-d row (OFFC_SPEC 1, 4) is enumerated for
# d = 7..DMAX, and each embedding becomes one more whole-window pattern in PATS[d] (slot -> letter set), so the separator DFS,
# admissible(), lowerR2 and upperR2 all skip the killed arrangements exactly as they skip u-centred pattern hits.
OFFC_LOG = collections.Counter(); OFFC_SKIP = collections.Counter()
OFFC_BROKEN = 'offcbroken' in FLAGS   # physical-test control only

def offc_conf(src, nm, d0, P, r, m):
    """registry entry -> K = (vertices, degree, adjacency, triangles) or (None, reason).  OFFC_SPEC 2."""
    ex = {sl: next(iter(S)) for sl, S in P if len(S) == 1 and 5 <= next(iter(S)) <= 8}
    V = [('u',)] + sorted(ex)
    deg = {('u',): d0}; deg.update(ex)
    wl = {sl[1]: L for sl, L in ex.items() if sl[0] == 'w'}
    for sl in ex:   # s_{i-1}, s_i both in K and w_i not in K: the cut window's s-s adjacency is not determined by the name
        if sl[0] == 's' and ('s', (sl[1] + 1) % d0) in ex and ('w', (sl[1] + 1) % d0) not in ex: return None, 'ambiguous s-s pair'
    def adj(x, y):
        r_ = _offc_wadj(d0, x, y, wl); assert not isinstance(r_, tuple); return r_
    def mk(VV):
        A = {x: {y for y in VV if y != x and adj(x, y)} for x in VV}
        T = {frozenset((a, b, c)) for a in VV for b in A[a] for c in A[a] & A[b] if len({a, b, c}) == 3}
        return VV, {x: deg[x] for x in VV}, A, T
    def ring(K):
        VV, g, A, T = K; E = sum(len(A[x]) for x in VV) // 2
        return sum(g.values()) - E - 3 * len(VV) + 3
    def conn(K):
        VV, g, A, T = K; seen = {VV[0]}; st = [VV[0]]
        while st:
            x = st.pop()
            for y in A[x]:
                if y not in seen: seen.add(y); st.append(y)
        return len(seen) == len(VV)
    Ku = mk(V)
    if src in ('RPATN',): return (Ku, 'u in K (rpatN: u-centred by construction)') if conn(Ku) else (None, 'disconnected')
    if r is None or m is None:   # nf, rpat/rpatD: no (r, m) on record -> K with u (a superset of the verified interior)
        return (Ku, 'u in K (no r/m on record)') if conn(Ku) else (None, 'disconnected')
    if m == len(V) and conn(Ku) and ring(Ku) == r: return Ku, 'u in K, (r, m) confirmed'
    K0 = mk(V[1:])
    if m == len(V) - 1 and len(V) > 1 and conn(K0) and ring(K0) == r: return K0, 'u not in K, (r, m) confirmed'
    return None, '(r, m) = (%d, %d) not reproduced (|exact| = %d)' % (r, m, len(V) - 1)

def _offc_wadj(d, x, y, wl):
    """adjacency of slots x, y in the degree-d window, w letters wl {i: letter} for w slots that are vertices of the embedding;
    ('w', i) when it is s_{i-1}-s_i with w_i not a vertex of the embedding (adjacent iff w_i = 5).  OFFC_SPEC 1."""
    if x == y: return False
    if x == ('u',) or y == ('u',):
        o = y if x == ('u',) else x
        return o[0] == 'w'
    if x[0] == 'w' and y[0] == 'w': return (x[1] - y[1]) % d in (1, d - 1)
    if x[0] == 's' and y[0] == 's':
        if (x[1] - y[1]) % d == 1: i = x[1]
        elif (y[1] - x[1]) % d == 1: i = y[1]
        else: return False
        if OFFC_BROKEN: return True   # BROKEN CONTROL (offcbroken): s_{i-1}-s_i taken adjacent whatever w_i is
        L = wl.get(i)
        return ('w', i) if L is None else (L == 5)
    w, s = (x, y) if x[0] == 'w' else (y, x)
    return s[1] in (w[1], (w[1] - 1) % d)

def _offc_nbrs(d, x):
    if x == ('u',): return [('w', i) for i in range(d)]
    i = x[1]
    if x[0] == 'w': return [('u',), ('w', (i + 1) % d), ('w', (i - 1) % d), ('s', i), ('s', (i - 1) % d)]
    return [('w', i), ('w', (i + 1) % d), ('s', (i + 1) % d), ('s', (i - 1) % d)]

def offc_embed(K, d):
    """every embedding of K into the degree-d window up to the window's rotations -> list of patterns {slot: frozenset}.
    Injective; u's image needs degree d; every other image is exact (degree 5..8); induced; triangles onto faces."""
    VV, g, A, T = K
    if not all(g[x] == d or 5 <= g[x] <= 8 for x in VV): return []
    first = max(VV, key=lambda x: (len(A[x]), g[x]))
    order = [first]
    while len(order) < len(VV):
        order.append(max((x for x in VV if x not in order), key=lambda x: (len(A[x] & set(order)), g[x], len(A[x]))))
    par = {x: next(y for y in order[:k] if y in A[x]) for k, x in enumerate(order) if k}
    out = []; phi = {}; used = set()
    def okslot(x, s_):
        return g[x] == d if s_ == ('u',) else 5 <= g[x] <= 8
    def rec(k):
        if k == len(order):
            wl = {s_[1]: g[x] for x, s_ in phi.items() if s_[0] == 'w'}; cons = {}
            for a, b in itertools.combinations(order, 2):
                r_ = _offc_wadj(d, phi[a], phi[b], wl); want = b in A[a]
                if isinstance(r_, tuple): cons[r_[1]] = (5,) if want else (6, 7, 8, 9)
                elif r_ != want: return
            for t in T:
                if not _offc_face(d, [phi[x] for x in t], wl): return
            pat = {s_: frozenset((g[x],)) for x, s_ in phi.items() if s_ != ('u',)}
            for i, S in cons.items(): pat[('w', i)] = frozenset(S)
            out.append(tuple(sorted(pat.items()))); return
        x = order[k]
        cands = [('u',), ('w', 0), ('s', 0)] if k == 0 else _offc_nbrs(d, phi[par[x]])
        wl = {s_[1]: g[y] for y, s_ in phi.items() if s_[0] == 'w'}
        for s_ in cands:
            if s_ in used or not okslot(x, s_): continue
            wl2 = dict(wl)
            if s_[0] == 'w': wl2[s_[1]] = g[x]
            bad = False
            for y in order[:k]:
                r_ = _offc_wadj(d, s_, phi[y], wl2)
                if isinstance(r_, tuple): continue
                if r_ != (y in A[x]): bad = True; break
            if bad: continue
            phi[x] = s_; used.add(s_); rec(k + 1); used.discard(s_); del phi[x]
    rec(0)
    return out

def _offc_face(d, im, wl):
    S = set(im)
    if len(S) != 3: return False
    if ('u',) in S:
        ws = sorted(x[1] for x in S if x[0] == 'w')
        return len(ws) == 2 and (ws[0] - ws[1]) % d in (1, d - 1)
    ws = [x[1] for x in S if x[0] == 'w']; ss = [x[1] for x in S if x[0] == 's']
    if len(ws) == 2:
        a, b = ws
        if (b - a) % d != 1: a, b = b, a
        return (b - a) % d == 1 and ss == [a]
    if len(ws) == 1: i = ws[0]; return set(ss) == {(i - 1) % d, i} and wl.get(i) == 5
    return False

def _offc_canon(d, P):
    """P up to the 2d rotations / reflections (as instances(): w_i -> w_{r-i}, s_i -> s_{r-i-1})"""
    best = None
    for r in range(d):
        for refl in (False, True):
            Q = []
            for (typ, i), S in P:
                j = (i + r) % d if not refl else ((r - i) % d if typ == 'w' else (r - i - 1) % d)
                Q.append(((typ, j), S))
            Q = tuple(sorted(Q, key=lambda z: (z[0], sorted(z[1]))))
            k = tuple((a, tuple(sorted(b))) for a, b in Q)
            if best is None or k < best[0]: best = (k, Q)
    return best[1]

def offc_extend():
    """adds the off-centre patterns to PATS.  The result is cached (pickle keyed by the md5 of OFFREG, this file and DMAX) in
    OPT offccache (default: the scratchpad's P/offc_cache)."""
    import hashlib, pickle
    t0 = time.time()
    src_ = open(os.path.join(HERE, 'offc.py')).read()
    hk = hashlib.md5(repr((sorted(map(repr, OFFREG)), src_, DMAX, 'offcbroken' in FLAGS)).encode()).hexdigest()
    cd = OPT.get('offccache', '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/offc_cache'); os.makedirs(cd, exist_ok=True)
    cf = os.path.join(cd, 'offc_%s.pkl' % hk)
    hit = os.path.exists(cf)
    if hit:
        add, msgs = pickle.load(open(cf, 'rb'))
    else:
        add, msgs = _offc_build()
        tmp = cf + '.%d' % os.getpid(); pickle.dump((add, msgs), open(tmp, 'wb')); os.replace(tmp, cf)
    for d, c in add:
        if c not in PATS[d]: PATS[d].add(c); PSRC['OFFC'] += 1
    for m_ in msgs: log(m_)
    log('  offc cache %s (%s, %.1fs)' % (os.path.basename(cf), 'read' if hit else 'built', time.time() - t0))
def _offc_build():
    t0 = time.time(); seenK = {}; nK = 0; nadd = collections.Counter(); add = []; msgs = []; seenP = set()
    for src, nm, d0, P, r, m in OFFREG:
        if nm in OFFC_EXCL: OFFC_SKIP['excluded by name'] += 1; continue
        K, why = offc_conf(src, nm, d0, P, r, m)
        OFFC_LOG[(src, why if K else 'skipped: ' + why)] += 1
        if K is None: continue
        VV, g, A, T = K
        key = (tuple(sorted((x, g[x]) for x in VV)), d0 if ('u',) in VV else 0)
        if key in seenK: continue
        seenK[key] = nm; nK += 1
        for d in range(7, DMAX + 1):
            for pat in offc_embed(K, d):
                c = _offc_canon(d, pat)
                if (d, c) not in seenP: seenP.add((d, c)); add.append((d, c)); nadd[d] += 1
    msgs.append('offc: %d registry entries -> %d distinct configurations K; distinct off-centre patterns by d %s (built in %.1fs)' % (len(OFFREG), nK, dict(sorted(nadd.items())), time.time() - t0))
    for (src, why), n in sorted(OFFC_LOG.items()): msgs.append('  offc %-6s %6d  %s' % (src, n, why))
    for why, n in OFFC_SKIP.items(): msgs.append('  offc        %6d  %s' % (n, why))
    return add, msgs
# RSST 2.126 and 8406.123 are kept out of every solve (Long Table): any entry with that name is skipped here as well.
OFFC_EXCL = {'2.126', '8406.123', 'rsst 2.126', 'RSST 2.126', 'RSST 8406.123'}
