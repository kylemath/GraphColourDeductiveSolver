# offc2.py (s86, Opus): rotation-filtered off-centre kills, written as an rpatN-format file with one witness per line.
# exec'd by eng/pcheck_dbg.py (ROWDBG=offc2.py); replaces upperR2 by the builder.  Spec: from_opus/offc/OFFC_SPEC.md
# (= s39o/OFFC_SPEC.md sections 1, 2, 4 + section R, the disc/fan rotation filter).  The flag offc is NOT set: load_patterns
# runs as usual (u-centred registry), every entry it reads is recorded here, and the off-centre patterns are built from them.
# Options: offcout=FILE (pattern file to write), offctest=CERT (count the cert's receiver rows the new patterns kill).
exec(open(os.path.join(HERE, 'offc.py')).read(), globals())   # offc_conf, _offc_wadj, _offc_nbrs, _offc_face, _offc_canon, OFFC_EXCL
_REC = []
def addpat(nm, src, rm=None):   # load_patterns' addpat, recording every registry entry it reads
    d, P = pname(nm)
    _REC.append((src, nm, d, P) + (rm or (None, None)))
    if P not in PATS[d]: PATS[d].add(P); PSRC[src] += 1

def offc_embed_w(K, d):
    """offc_embed with the embedding phi kept: list of (pattern, phi)"""
    VV, g, A, T = K
    if not all(g[x] == d or 5 <= g[x] <= 8 for x in VV): return []
    first = max(VV, key=lambda x: (len(A[x]), g[x]))
    order = [first]
    while len(order) < len(VV):
        order.append(max((x for x in VV if x not in order), key=lambda x: (len(A[x] & set(order)), g[x], len(A[x]))))
    par = {x: next(y for y in order[:k] if y in A[x]) for k, x in enumerate(order) if k}
    out = []; phi = {}; used = set()
    def okslot(x, s_): return g[x] == d if s_ == ('u',) else 5 <= g[x] <= 8
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
            out.append((tuple(sorted(pat.items())), dict(phi))); return
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

def disc_fan(K):
    """section R: None if K's triangles form one edge-connected triangulated disc (every edge of K in 1 or 2 triangles,
    the triangles connected through shared edges, each vertex's triangles one fan through shared edges at that vertex,
    V - E + F = 1); else the reason"""
    VV, g, A, T = K
    T = [tuple(t) for t in T]
    E = {frozenset((a, b)) for a in VV for b in A[a]}
    if not T: return 'no triangle'
    et = collections.defaultdict(list)
    for i, t in enumerate(T):
        for a, b in itertools.combinations(t, 2): et[frozenset((a, b))].append(i)
    if any(not et.get(e) for e in E): return 'an edge in no triangle'
    if any(len(v) > 2 for v in et.values()): return 'an edge in 3+ triangles'
    def comps(idx, ok_edge):
        idx = list(idx); seen = {idx[0]}; st = [idx[0]]
        while st:
            i = st.pop()
            for a, b in itertools.combinations(T[i], 2):
                e = frozenset((a, b))
                if not ok_edge(e): continue
                for j in et[e]:
                    if j in idx and j not in seen: seen.add(j); st.append(j)
        return len(seen) == len(idx)
    if not comps(range(len(T)), lambda e: True): return 'triangles not edge-connected'
    for v in VV:
        tv = [i for i, t in enumerate(T) if v in t]
        if not tv: return 'a vertex in no triangle'
        if not comps(tv, lambda e, v=v: v in e): return 'a vertex with two fans'
    if len(VV) - len(E) + len(T) != 1: return 'not a disc (V - E + F = %d)' % (len(VV) - len(E) + len(T))
    return None

def _slotname(s_): return 'u' if s_ == ('u',) else '%s%d' % s_
def _patline(d, pat):
    lk = ['.'] * d; sv = ['.'] * d
    for (typ, i), S in pat:
        S = tuple(sorted(S))
        ch = 'N' if S == (6, 7, 8, 9) else str(S[0])
        assert len(S) == 1 or ch == 'N'
        if typ == 'w': lk[i] = ch
        else: assert ch != 'N'; sv[i] = ch
    return ''.join(lk), ''.join(sv)

def cmd_upperR2():
    import hashlib
    t0 = time.time(); load_patterns()
    # rpat= and rpatN= entries (load_patterns records them in OFFREG only under the offc flag): parsed here as there
    for fn in [f for f in OPT.get('rpat', '').split(',') if f]:
        for line in open(fn):
            f = line.split('#')[0].split()
            if not f: continue
            d, k = int(f[0]), int(f[1]); slots = {}
            for j in range(k):
                i, m = int(f[2 + 2 * j]), int(f[3 + 2 * j])
                rd = [('w', (i + 1) % d), ('s', i), ('s', (i - 1) % d), ('w', (i - 1) % d)]
                ent = [(('w', i), frozenset((5,)))] + [(rd[t], frozenset(LET[b] for b in range(5) if (m >> (5 * t + b)) & 1)) for t in range(4)]
                for sl, S_ in ent: slots[sl] = slots.get(sl, frozenset(LET)) & S_
            _REC.append(('RPAT', line.split('#')[1].strip() if '#' in line else 'rpat', d, tuple(sorted(slots.items())), None, None))
    for fn in [f for f in OPT.get('rpatN', '').split(',') if f]:
        for ln, line in enumerate(open(fn)):
            f = line.split('#')[0].split()
            if not f: continue
            d, lk, sv = int(f[0]), f[1], f[2]
            P = tuple(sorted(((typ, i), frozenset((6, 7, 8, 9)) if ch == 'N' else frozenset((int(ch),)))
                             for typ, word in (('w', lk), ('s', sv)) for i, ch in enumerate(word) if ch != '.'))
            _REC.append(('RPATN', 'rpatN:%s:%d' % (os.path.basename(fn), ln + 1), d, P, None, None))
    # name -> source file (first file that lists it) and md5s of every source file
    fmd5 = {}; nfile = {}
    args = open(OPT['args']).read().split() if 'args' in OPT else []
    for a in args:
        if not a.startswith(('pat=', 'cpat=')): continue
        fn = a.split('=', 1)[1]; fn = fn[:-4] if fn.endswith(':all') else fn
        p = fn if os.path.isabs(fn) else os.path.join(ROOT, fn)
        if not os.path.exists(p): continue
        fmd5[fn] = hashlib.md5(open(p, 'rb').read()).hexdigest()[:8]
        for line in open(p):
            if line.strip() and not line.startswith(' ') and re.match(r'^[epf]\d+_', line): nfile.setdefault(line.split()[0], fn)
    for o in ('rpat', 'rpatN'):
        for fn in [f for f in OPT.get(o, '').split(',') if f]: fmd5[fn] = hashlib.md5(open(fn, 'rb').read()).hexdigest()[:8]
    def srcfile(src, nm):
        if src == 'RPAT': return OPT['rpat']
        if src == 'RPATN': return OPT['rpatN']
        return nfile.get(nm, '?')
    log('OFFC2: %d registry entries recorded %s (%.0fs)' % (len(_REC), dict(collections.Counter(r[0] for r in _REC)), time.time() - t0))
    # existing u-centred patterns, canonical, to skip duplicates
    have = {d: {_offc_canon(d, P) for P in PATS.get(d, ())} for d in range(7, DMAX + 1)}
    lost = set(); seenK = {}; stat = collections.Counter(); drop = collections.Counter(); found = {}; nemb = collections.Counter()
    for src, nm, d0, P, r, m in _REC:
        if nm in OFFC_EXCL: stat['excluded by name'] += 1; continue
        K, why = offc_conf(src, nm, d0, P, r, m)
        if K is None: stat['skipped: ' + why] += 1; continue
        VV, g, A, T = K
        key = (tuple(sorted((x, g[x]) for x in VV)), d0 if ('u',) in VV else 0)
        if key in seenK: stat['same K as an earlier entry'] += 1; continue
        seenK[key] = nm
        bad = disc_fan(K)
        for d in range(7, DMAX + 1):
            for pat, phi in offc_embed_w(K, d):
                uc = phi.get(('u',)) == ('u',)
                if bad:
                    drop[bad] += 1; nemb['dropped (disc/fan)%s' % (', u-centred' if uc else ', off-centre')] += 1
                    if not uc:
                        c = _offc_canon(d, pat)
                        if c not in have[d]: lost.add((d, c))
                    continue
                if uc: nemb['u-centred (entry centre on u), not off-centre: left out'] += 1; continue
                nemb['kept'] += 1
                c = _offc_canon(d, pat)
                if c in have[d]: nemb['kept, already a u-centred pattern'] += 1; continue
                if (d, c) not in found: found[(d, c)] = (src, nm, d0, pat, phi)
        stat['K disc/fan: ' + (bad or 'ok')] += 1
    for k_, v in sorted(stat.items()): log('OFFC2 K   %7d  %s' % (v, k_))
    for k_, v in sorted(nemb.items()): log('OFFC2 emb %7d  %s' % (v, k_))
    for k_, v in sorted(drop.items()): log('OFFC2 drop %6d  embeddings: %s' % (v, k_))
    lost -= set(found)
    log('OFFC2: the disc/fan filter loses %d distinct off-centre patterns that no kept embedding gives, by d %s' % (len(lost), dict(sorted(collections.Counter(d for d, _ in lost).items()))))
    log('OFFC2: %d new off-centre patterns by d %s (%.0fs)' % (len(found), dict(sorted(collections.Counter(d for d, _ in found).items())), time.time() - t0))
    out = OPT.get('offcout')
    if out:
        with open(out, 'w') as fo:
            fo.write('# offc2 (s86 Opus): rotation-filtered off-centre kills, rpatN format "d LINK SWORD"; spec from_opus/offc/OFFC_SPEC.md.\n')
            fo.write('# registry: args %s md5 %s; rpat %s; rpatN %s; exname %s; DMAX %d; %d patterns\n' % (os.path.basename(OPT.get('args', '')), hashlib.md5(open(OPT['args'], 'rb').read()).hexdigest()[:8] if 'args' in OPT else '-',
                     ' '.join('%s md5 %s' % (os.path.basename(f), fmd5[f]) for f in OPT.get('rpat', '').split(',') if f), ' '.join('%s md5 %s' % (os.path.basename(f), fmd5[f]) for f in OPT.get('rpatN', '').split(',') if f),
                     os.path.basename(OPT.get('exname', '-')), DMAX, len(found)))
            fo.write('# witness: src (D pat= / C cpat= / RPAT / RPATN), K = the entry\'s configuration (OFFC_SPEC 2), file + md5, phi = K vertex (slot of the entry\'s own degree-d0 window) > slot of this degree-d window\n')
            for (d, c), (src, nm, d0, pat, phi) in sorted(found.items(), key=lambda kv: (kv[0][0], repr(kv[0][1]))):
                lk, sv = _patline(d, pat); fn = srcfile(src, nm)
                fo.write('%d %s %s # %s %s d0=%d file=%s md5=%s phi=%s\n' % (d, lk, sv, src, nm, d0, fn, fmd5.get(fn, '?'), ','.join('%s>%s' % (_slotname(x), _slotname(s_)) for x, s_ in sorted(phi.items(), key=lambda kv: repr(kv[0])))))
        log('OFFC2: wrote %s (md5 %s)' % (out, hashlib.md5(open(out, 'rb').read()).hexdigest()[:8]))
    # tests: the new patterns as extra PATS entries
    nb = {d: len(PATS[d]) for d in PATS}
    for (d, c), (src, nm, d0, pat, phi) in found.items(): PATS[d].add(pat)
    _INST.clear(); _NPI.clear()
    for d_, lk_, sv_ in ((7, '7567675', '6666655'), (7, '8567565', '6678565')):
        log('OFFC2 TEST %d/%s/%s: %s' % (d_, lk_, sv_, admissible(d_, lk_, sv_)))
    if 'offctest' in OPT:
        C = json.load(open(OPT['offctest'])); kill = collections.Counter(); tot = collections.Counter(); wk = collections.Counter()
        for c in C:
            row = c['row']
            if row[0] != 'receiverR2': continue
            d, lk, sv = int(row[1]), row[2], row[3]; tot[d] += 1
            why = admissible(d, lk, sv)
            if why: kill[d] += 1; wk[d] += abs(float(Fraction(c['w']) if isinstance(c['w'], str) else c['w']))
        log('OFFC2 CERT %s: receiver rows killed by the new patterns, by d: %s of %s (|w| %s)' % (os.path.basename(OPT['offctest']), dict(kill), dict(tot), {d: round(v, 6) for d, v in wk.items()}))
