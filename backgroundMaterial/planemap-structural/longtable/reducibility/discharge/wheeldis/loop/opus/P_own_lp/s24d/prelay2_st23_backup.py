# prelay2.py (Opus P_own_lp, stage 12): 6-centred relay R6x2 (spec in FINDINGS.md stage 12).  exec'd in pcheck.py.
AP = 'noapex' not in FLAGS          # validation V1: noapex = s10's class
AC = 'apexcls' in FLAGS             # reduced s12: apex letters read only as small (5) / big (7) witnesses
def ap(x): return (7 if x >= 7 else 5) if AC else x
ZH = 'zh' in FLAGS                   # stage 13 (R7h): big-centred split, z[five link from the big, hat classes on both sides]
ZV = {}
Q7 = 'q7' in FLAGS                   # stage 14 (R77): big -> adjacent 7 inflow q[the 7's whole link, read from the sender]
QV = {}
V6 = 'v6' in FLAGS                   # stage 15: a 6 next to a 7 passes v[its link at u + 3-class apexes] on to the 7
VV = {}
def cv(x): return x if x < 7 else 7
W19 = 'w19' in FLAGS                 # stage 19 oracle: W (7, 5-5-5 face, face-adjacent 6 with private 5) forbidden by assumption
F16 = 'filt16' in FLAGS              # stage 16 A': allowed-private sets from the 3-ball containment filter (s16_filter.local)
KT = {}
def kt_load():
    if F16 and not KT:
        for U in (7, 8, 9): KT[U] = np.load(OPT['killtab'] + '_U%d.npy' % U)
def amask(U, a, b, e, f, s0, s1, s2, s3):
    """allowed-letter bitmask (bit i = LET[i]) for the private of a 6 at w_j: a,b,e,f = w_{j-2},w_{j-1},w_{j+1},w_{j+2};
    s0..s3 = s_{j-2..j+1}; letters 5..9"""
    kt_load(); m = 31 & ~int(KT[U][a - 5, b - 5, e - 5, f - 5, s0 - 5, s1 - 5, s2 - 5, s3 - 5])
    if W19 and U == 7 and ((e == 5 and f == 5 and s3 == 5) or (b == 5 and a == 5 and s0 == 5)): m &= ~1   # stage 19 oracle W
    return m
def pallow(sig): return [p for i, p in enumerate(LET) if not F16 or (sig[-1] >> i) & 1]
def v_of(m, ar, al):
    a = tuple(m) + (cv(ar), cv(al)); b = (m[0],) + tuple(reversed(m[1:])) + (cv(al), cv(ar)); return min(a, b)
def sigv_of(U, wr, sr, sl, wl, wrr, wll):
    a = (U, wr, sr, sl, wl, cv(wrr), cv(wll)); b = (U, wl, sl, sr, wr, cv(wll), cv(wrr)); return min(a, b)
def sigv_keys(sg):
    U, wr, sr, sl, wl, wrr, wll = sg[:7]
    return sorted({v_of((U, wr, sr, p, sl, wl), wrr, wll) for p in pallow(sg) if not isR6((U, wr, sr, p, sl, wl))})
def qkey(m):
    m = tuple(m); return min(m, (m[0],) + tuple(reversed(m[1:])))
def q7sig(U, a, b, c, e):
    x = (U, a, b, c, e); return min(x, (U, e, c, b, a))
def q7keys(sg):
    U, a, b, c, e = sg
    return sorted({qkey((U, a, b, p1, p2, c, e)) for p1 in LET for p2 in LET if ''.join(map(str, canon((U, a, b, p1, p2, c, e)))) not in RBIG})
def q7_inflow(w):
    """coefficient dict of q keys flowing into a 7 with link w (d = 7)"""
    cf = collections.Counter()
    for j in range(7):
        if w[j] >= 7: cf[qkey(tuple(w[(j + i) % 7] for i in range(7)))] += 1
    return cf
_L7 = []
def write_bonus():
    if not _L7:
        seen = set()
        for w in itertools.product(LET, repeat=7):
            c = canon(w)
            if c not in seen: seen.add(c); _L7.append(c)
    fn = os.path.join(WORK, 'bonus7.txt'); n = 0
    with open(fn, 'w') as f:
        for c in _L7:
            v = sum(m * QV.get(k, 0.0) for k, m in q7_inflow(c).items())
            if v > 0: f.write('%s %.15f\n' % (''.join(map(str, c)), v)); n += 1
    BONUSF[0] = fn if n else None
    return n
def zkey(n, hr, hl):
    """n = (U, n1, n2, n3, n4) the five's link read from the big U (n1 = next spoke); hr = class of the hat between U and n1,
    hl = class of the hat between U and n4 (0 small / 1 big)"""
    a = tuple(n) + (hr, hl); b = (n[0], n[4], n[3], n[2], n[1], hl, hr); return min(a, b)
def g2_of(n1, n2, n3, n4, n5, ar, al):
    ar, al = ap(ar), ap(al)
    a = (n1, c2(n2), c2(n3), c2(n4), n5) + ((ar, al) if AP else ())
    b = (n5, c2(n4), c2(n3), c2(n2), n1) + ((al, ar) if AP else ())
    return min(a, b)
def h2_of(m, ar, al):
    """m = the 6's link rotated to start at the big; ar = apex beyond (m0, m1), al = apex beyond (m5, m0)"""
    ar, al = ap(ar), ap(al)
    a = tuple(m) + ((ar, al) if AP else ()); b = (m[0],) + tuple(reversed(m[1:])) + ((al, ar) if AP else ())
    return min(a, b)
def sig2_of(U, wr, sr, sl, wl, wrr, wll):
    wrr, wll = ap(wrr), ap(wll)
    a = (U, wr, sr, sl, wl) + ((wrr, wll) if AP else ()); b = (U, wl, sl, sr, wr) + ((wll, wrr) if AP else ())
    return min(a, b)
def sig2_keys(sig):
    U, wr, sr, sl, wl = sig[:5]; wrr, wll = (sig[5], sig[6]) if AP else (0, 0)
    return sorted({h2_of((U, wr, sr, p, sl, wl), wrr, wll) for p in pallow(sig) if not isR6((U, wr, sr, p, sl, wl))})
F5 = 'face5' in FLAGS                # stage 17: five -> five transfer f across a 5-5-5 face (FINDINGS stage 17)
FV = {}
_m5 = {}
def mate_ok(e, hb1, hb2, o):
    """face-mate five with link (5, e, hat1, hat2, o): some completion of the two hat classes is non-R5"""
    k_ = (e, hb1, hb2, o)
    if k_ not in _m5: _m5[k_] = any(not isR5((5, e, x_, y_, o)) for x_ in CLS2[hb1] for y_ in CLS2[hb2])
    return _m5[k_]
def face_one(w, H, k, cf):
    """f terms of five v (word w, hat classes H; H[k] = class of the hat between w_k and w_{k+1}) on the 5-5-5 face
    (v, b = w_k, c = w_{k+1}).  K(x->y) = (e_xy, c k_x, c e_xz, c k_y, c e_yz, c k_z).  False if a mate is R5."""
    n = 5
    em, ka, ec = w[(k - 1) % n], w[(k - 2) % n], w[(k + 2) % n]     # e_ab, k_a, e_ca (exact)
    kb, ebc, kc = H[(k - 1) % n], H[k], H[(k + 1) % n]             # k_b, e_bc, k_c (classes)
    if not mate_ok(em, kb, ebc, 5) or not mate_ok(5, ebc, kc, ec): return False
    cf[('f', (em, c2(ka), c2(ec), kb, ebc, kc))] -= 1              # v -> b
    cf[('f', (ec, c2(ka), c2(em), kc, ebc, kb))] -= 1              # v -> c
    cf[('f', (em, kb, ebc, c2(ka), c2(ec), kc))] += 1              # b -> v
    cf[('f', (ec, kc, ebc, c2(ka), c2(em), kb))] += 1              # c -> v
    return True
def face_terms(w, H):
    cf = collections.Counter()
    for k in range(5):
        if w[k] == 5 and w[(k + 1) % 5] == 5 and not face_one(w, H, k, cf): return None
    return cf
def face_selftest(N=200000):
    """physical test: on one 5-5-5 face (v, b, c) built from v's 2-ball letters, the f terms of the three fives' own views sum to 0"""
    rng = np.random.default_rng(7); bad = 0; n_ = 0
    for _ in range(N):
        w = [int(x_) for x_ in rng.choice(LET, 5)]; k = int(rng.integers(5)); w[k] = w[(k + 1) % 5] = 5
        h = [int(x_) for x_ in rng.choice(LET, 5)]; r = [int(x_) for x_ in rng.integers(0, 2, 4)]
        W = lambda i: w[i % 5]; Hh = lambda i: h[i % 5]
        tot = collections.Counter(); ok = []
        ok.append(face_one(w, [c2(x_) for x_ in h], k, tot))                                        # v
        wb = [5, W(k - 1), Hh(k - 1), Hh(k), 5]; Hb = [c2(W(k - 2)), r[0], r[1], c2(Hh(k + 1)), c2(W(k + 2))]
        ok.append(face_one(wb, Hb, 4, tot))                                                           # b: face (c, v) at 4, 0
        wc = [5, 5, Hh(k), Hh(k + 1), W(k + 2)]; Hc = [c2(W(k - 1)), c2(Hh(k - 1)), r[2], r[3], c2(W(k - 2))]
        ok.append(face_one(wc, Hc, 0, tot))                                                           # c: face (v, b) at 0, 1
        if not all(ok): continue
        n_ += 1
        if any(tot.values()): bad += 1
    return n_, bad
H5 = 'hat5' in FLAGS                 # stage 18 (RELAY_SPEC 15): a big b sends r[K] to a five v of which it is a hat
RV = {}
HRR = 'hatrr' in FLAGS               # stage 23 (RELAY_SPEC 15r): reverse hat channel, the big hat b sends rr[K] >= 0 to the five v
assert not HRR or H5, 'hatrr needs hat5'
RRV = {}
def hat_sender_terms(w, H, Fn, k):
    """coefficients the five v's senderR2 row gets from its big hat H[k]: r (v -> b) +1; rr (b -> v) -1"""
    K = h5_sender(w, H, Fn, k); out = {('r', K): 1}
    if HRR: out[('rr', K)] = -1
    return out
def hat_recv_terms(K, broken_sign=False):
    """coefficients the big b's receiverR2 row (load = inflow) gets at a hat position: r +1; rr -1 (b pays out)"""
    out = {('r', K): 1}
    if HRR: out[('rr', K)] = 1 if broken_sign else -1
    return out
def h5side_v(x, X1, X2):
    """one shared spoke x of the diamond (v, x, b, y), read from the five v: X1 = x's nbr adjacent to b (class),
    X2 = x=5: x's nbr adjacent to v (exact letter); x=6: x's nbr opposite y (class)"""
    if x == 5: return (5, X1, X2)
    if x == 6: return (6, X1, X2)
    return (x,)
def h5key(sa, sb): return min(sa + sb, sb + sa)
def h5_sender(w, H, Fn, k):
    """inflow key at five v (word w) from the big hat H[k] between w_k and w_{k+1}; H, Fn = class bits"""
    n = 5; x, y = w[k], w[(k + 1) % n]
    sx = (5, H[(k - 1) % n], w[(k - 1) % n]) if x == 5 else (6, Fn[k], H[(k - 1) % n]) if x == 6 else (x,)
    sy = (5, H[(k + 1) % n], w[(k + 2) % n]) if y == 5 else (6, Fn[(k + 1) % n], H[(k + 1) % n]) if y == 6 else (y,)
    return h5key(sx, sy)
def h5_recv(wm1, wi, wi1, wi2, sm1, sp1):
    """outflow key at a big centre whose apex s_i = 5 sits between w_i and w_{i+1}; wm1 = w_{i-1}, wi2 = w_{i+2},
    sm1 = s_{i-1}, sp1 = s_{i+1} (exact letters)"""
    sx = (5, c2(wm1), sm1) if wi == 5 else (6, c2(wm1), c2(sm1)) if wi == 6 else (wi,)
    sy = (5, c2(wi2), sp1) if wi1 == 5 else (6, c2(wi2), c2(sp1)) if wi1 == 6 else (wi1,)
    return h5key(sx, sy)
def hat5_selftest(N=100000, broken=False):
    """physical test on random local triangulations around a diamond (v five; x, y consecutive spokes of v; b the other
    apex of edge xy, big).  Each vertex gets a random letter; x and y get explicit rotations (cyclic neighbour lists),
    and every hat / apex / fan is read off them by the generic rule apex(c; p, q) = the common neighbour of p and q
    other than c.  The sender reads v's 2-ball, the receiver reads b's 2-ball; both keys must agree, in both
    orientations of b's link.  broken = the receiver reads s_{i-1} from the wrong side (control)."""
    rng = np.random.default_rng(18); bad = 0
    for _ in range(N):
        deg = {}; rot = {}
        L = lambda: int(rng.choice(LET))
        dx, dy = int(rng.choice((5, 6, 7))), int(rng.choice((5, 6, 7)))
        names = ['v', 'x', 'y', 'b', 'w2', 'w3', 'wm1']
        # x's rotation starting at v towards y: v, y, b, then its free nbrs, ending at wm1 (v's other link nbr of x)
        rot['x'] = ['v', 'y', 'b'] + ['x%d' % i for i in range(dx - 4)] + ['wm1']
        rot['y'] = ['v', 'x', 'b'] + ['y%d' % i for i in range(dy - 4)] + ['w2']
        rot['v'] = ['x', 'y', 'w2', 'w3', 'wm1']
        for nm in names + rot['x'] + rot['y']: deg.setdefault(nm, L())
        deg['v'] = 5; deg['x'] = dx; deg['y'] = dy; deg['b'] = int(rng.choice(BIGL))
        def nb_after(c, p, other):   # in c's rotation, the neighbour of p that is not `other`
            r = rot[c]; i = r.index(p); a1, a2 = r[(i - 1) % len(r)], r[(i + 1) % len(r)]
            return a2 if a1 == other else a1
        # v's view: link (x, y, w2, w3, wm1); hats H[k] between link k, k+1
        hk_m1 = nb_after('x', 'wm1', 'v')      # common nbr of wm1 and x other than v
        hk_p1 = nb_after('y', 'w2', 'v')
        wv = [deg['x'], deg['y'], deg['w2'], deg['w3'], deg['wm1']]
        H = {4: c2(deg[hk_m1]), 0: c2(deg['b']), 1: c2(deg[hk_p1]), 2: 0, 3: 0}
        fan = lambda c: rot[c][len(rot[c]) // 2] if len(rot[c]) == 6 else None   # a 6's private = opposite v
        Fn = {0: c2(deg[fan('x')]) if dx == 6 else 0, 1: c2(deg[fan('y')]) if dy == 6 else 0}
        ks = h5_sender(wv, H, Fn, 0)
        # b's view: b's link contains X1, x, y, Y1 consecutively (X1 = x's nbr after b, Y1 = y's nbr after b)
        X1 = nb_after('x', 'b', 'y'); Y1 = nb_after('y', 'b', 'x')
        sm1 = nb_after('x', X1, 'b') if not broken else nb_after('x', 'v', 'y')   # apex of (X1, x) other than b
        sp1 = nb_after('y', Y1, 'b')
        assert nb_after('x', 'y', 'b') == 'v'                                       # apex of (x, y) other than b is v
        kr = h5_recv(deg[X1], dx, dy, deg[Y1], deg[sm1], deg[sp1])
        kr2 = h5_recv(deg[Y1], dy, dx, deg[X1], deg[sp1], deg[sm1])
        if not (ks == kr == kr2): bad += 1; continue
        if HRR:   # stage 23: the rr terms the two rows actually get must conserve charge and point b -> v
            ts = hat_sender_terms(wv, H, Fn, 0); tr = hat_recv_terms(kr, 'brokensign' in FLAGS)
            # v's charge changes by -cs * value (cs = coefficient in v's 'sends' row); b's by +cr * value (load = inflow)
            for fam_ in ('r', 'rr'):
                cs = ts.get((fam_, ks)); cr = tr.get((fam_, kr))
                if cs is None or cr is None or cs != cr: bad += 1; break
            else:
                if ts[('rr', ks)] != -1 or ts[('r', ks)] != 1: bad += 1   # rr: v gains (b -> v); r: v loses (v -> b)
    return N, bad
HX = 'hatx' in FLAGS
assert not HX or 'hat5' in FLAGS, 'hatx needs hat5 (all hats enumerated)'
HX = HX                 # stage 20 (RELAY_SPEC 16): exact hat letters in sender admissibility (joint over shared hats)
_r6c = {}
def isR6c(w):
    if w not in _r6c: _r6c[w] = isR6(w)
    return _r6c[w]
def hx_ok(w, H, Fn):
    """some exact letter per hat (in its class) makes every 6-spoke wheel non-R6 (fan letter in its class) and every
    five-spoke link non-R5, with each hat's single letter shared by the two spokes it touches"""
    n = 5; sixes = [k for k in range(n) if w[k] == 6]; fives = [k for k in range(n) if w[k] == 5]
    for h in itertools.product(*[CLS2[H[k]] for k in range(n)]):
        if any(isR5((5, w[(k - 1) % n], h[(k - 1) % n], h[k], w[(k + 1) % n])) for k in fives): continue
        if all(any(not isR6c((5, w[(k + 1) % n], h[k], q, h[(k - 1) % n], w[(k - 1) % n])) for q in CLS2[Fn[k]]) for k in sixes): return True
    return False
def hatx_selftest(N=100000, broken=False):
    """physical test around a five v: random letters on v's link w, its hats h (h_k = common nbr of w_k, w_{k+1} other than v)
    and the 6-spokes' privates; each spoke gets an explicit rotation list and its OWN wheel is read from that list.
    Checks: (a) a five-spoke's own link = the sender's reading (5, w_{k-1}, h_{k-1}, h_k, w_{k+1}) (canonical);
    (b) a 6-spoke's own wheel = the sender's reading (5, w_{k+1}, h_k, F_k, h_{k-1}, w_{k-1}) (canonical);
    (c) the g2 key the 6-spoke computes from its own arrangement (link from v, apexes from v's rotation) = the sender's g2.
    broken = the sender reads the five-spoke link with h_{k+1} in place of h_{k-1} (control)."""
    rng = np.random.default_rng(20); bad = 0; n_ = 0
    for _ in range(N):
        L = lambda: int(rng.choice(LET))
        w = [L() for _ in range(5)]; h = [L() for _ in range(5)]; f = [L() for _ in range(5)]
        vrot = list(range(5))                     # v's rotation: spokes 0..4
        for k in range(5):
            if w[k] not in (5, 6): continue
            # spoke k's rotation, starting at v towards w_{k+1}: v, w_{k+1}, h_k, [f_k if 6], h_{k-1}, w_{k-1}
            rot = [('v', 5), ('w', w[(k + 1) % 5]), ('h', h[k])] + ([('f', f[k])] if w[k] == 6 else []) + [('h', h[(k - 1) % 5]), ('w', w[(k - 1) % 5])]
            own = tuple(x[1] for x in rot)
            n_ += 1
            if w[k] == 5:
                rd = (5, w[(k - 1) % 5], h[(k + 1) % 5] if broken else h[(k - 1) % 5], h[k], w[(k + 1) % 5])
                if canon(own) != canon(rd): bad += 1
            else:
                rd = (5, w[(k + 1) % 5], h[k], f[k], h[(k - 1) % 5], w[(k - 1) % 5])
                if canon(own) != canon(rd): bad += 1
                # g2 from the 6's arrangement: L = own (L_i = v first); apex beyond (v, w_{k+1}) = v's next spoke w_{k+2};
                # apex beyond (w_{k-1}, v) = w_{k-2}
                k6 = g2_of(own[1], own[2], own[3], own[4], own[5], w[(vrot[(k + 2) % 5])], w[vrot[(k - 2) % 5]])
                L5 = lambda c: 7 if c else 5
                ks = g2_of(w[(k + 1) % 5], L5(c2(h[k])), L5(c2(f[k])), L5(c2(h[(k - 1) % 5])), w[(k - 1) % 5], w[(k + 2) % 5], w[(k - 2) % 5])
                if k6 != ks: bad += 1
    return n_, bad
WF19 = set()
if 'wf19' in FLAGS:   # stage 19b oracle: forbidden sender contexts (word, bits), FINDINGS stage 19b
    for line in open(OPT['wf']):
        if line.strip() and not line.startswith('#'):
            wd_, bt = line.split(); h_, f_ = bt.split('|')
            WF19.add((wd_, tuple(int(c) for c in h_.split(',')) + ('|',) + tuple(int(c) for c in f_.split(',') if c != '')))
def R2_sender_rows():
    out = []; nwf = [0]; nhx = [0]
    for w in SENDERS:
        n = 5; sixes = [k for k in range(n) if w[k] == 6]
        allow = {k: {(a_, q, b_) for a_ in LET for q in LET for b_ in LET if not isR6((5, w[(k + 1) % n], a_, q, b_, w[(k - 1) % n]))} for k in sixes}
        bigs = [j for j in range(n) if w[j] >= 7] if ZH else []
        faces = [k for k in range(n) if F5 and w[k] == 5 and w[(k + 1) % n] == 5]
        hats = sorted({h for k in sixes + bigs for h in (k, (k - 1) % n)} | {h for k in faces for h in ((k - 1) % n, k, (k + 1) % n)} | (set(range(n)) if H5 else set())); seen = set()
        base = collections.Counter()
        for j in range(n):
            if w[j] >= 7: base[('y', root(list(w), j))] += 1
        for hb in itertools.product((0, 1), repeat=len(hats)):
            H = dict(zip(hats, hb))
            for fb in itertools.product((0, 1), repeat=len(sixes)):
                Fn = dict(zip(sixes, fb)); okc = True
                for k in sixes:
                    if not any((a_, q, b_) in allow[k] for a_ in CLS2[H[k]] for q in CLS2[Fn[k]] for b_ in CLS2[H[(k - 1) % n]]): okc = False; break
                if not okc: continue
                if HX and not hx_ok(w, H, Fn): nhx[0] += 1; continue
                if WF19 and (''.join(map(str, w)), tuple(hb) + ('|',) + tuple(fb)) in WF19: nwf[0] += 1; continue
                cf = collections.Counter(base)
                if H5:
                    for k in range(n):
                        if H[k]:
                            for k2, c2v in hat_sender_terms(w, H, Fn, k).items(): cf[k2] += c2v
                if faces:
                    ft = face_terms(w, H)
                    if ft is None: continue
                    for k_, c_ in ft.items():
                        if c_: cf[k_] += c_
                for j in bigs:
                    cf[('z', zkey(tuple(w[(j + i) % n] for i in range(5)), H[j], H[(j - 1) % n]))] += 1
                for k in sixes:   # classes H, Fn are already 0/1 = c2 values; pass letters 5 / 7 as class witnesses
                    L5 = lambda c: 7 if c else 5
                    cf[('g', g2_of(w[(k + 1) % n], L5(H[k]), L5(Fn[k]), L5(H[(k - 1) % n]), w[(k - 1) % n], w[(k + 2) % n], w[(k - 2) % n]))] += 1
                k_ = tuple(sorted(cf.items()))
                if k_ not in seen: seen.add(k_); out.append((''.join(map(str, w)), dict(cf), list(hb) + ['|'] + list(fb)))
    if WF19: log('wf19: %d of %d forbidden sender contexts skipped' % (nwf[0], len(WF19)))
    if HX: log('hatx: %d sender contexts have no jointly admissible exact hat letters (dropped)' % nhx[0])
    return out
def cons2_coef(L, s):
    cf = collections.Counter()
    for i in range(6):
        if L[i] == 5: cf[('g', g2_of(L[(i + 1) % 6], L[(i + 2) % 6], L[(i + 3) % 6], L[(i + 4) % 6], L[(i + 5) % 6], s[i], s[(i - 1) % 6]))] += 1
    for j in range(6):
        if L[j] >= 7: cf[('h', h2_of(tuple(L[(j + i) % 6] for i in range(6)), s[j], s[(j - 1) % 6]))] -= 1
        if V6 and L[j] == 7: cf[('v', v_of(tuple(L[(j + i) % 6] for i in range(6)), s[j], s[(j - 1) % 6]))] += 1
    return cf
SALL = np.array(list(itertools.product(range(5), repeat=6)), dtype=np.int64)   # apex words (letter indices)
def cons2_delta(L, GV, HV2):
    """Delta(s) = sum g - sum h over all 5^6 apex words for link L (vectorised); returns array"""
    D = np.zeros(len(SALL))
    for i in range(6):
        if L[i] == 5:
            T = np.array([[GV.get(g2_of(L[(i + 1) % 6], L[(i + 2) % 6], L[(i + 3) % 6], L[(i + 4) % 6], L[(i + 5) % 6], LET[a], LET[b]), 0.0) for b in range(5)] for a in range(5)])
            D += T[SALL[:, i], SALL[:, (i - 1) % 6]]
    for j in range(6):
        if L[j] >= 7:
            m = tuple(L[(j + i) % 6] for i in range(6))
            T = np.array([[HV2.get(h2_of(m, LET[a], LET[b]), 0.0) for b in range(5)] for a in range(5)])
            D -= T[SALL[:, j], SALL[:, (j - 1) % 6]]
        if V6 and L[j] == 7:
            m = tuple(L[(j + i) % 6] for i in range(6))
            T = np.array([[VV.get(v_of(m, LET[a], LET[b]), 0.0) for b in range(5)] for a in range(5)])
            D += T[SALL[:, j], SALL[:, (j - 1) % 6]]
    return D
def window_table_R2(U, y, x, MV2):
    W = window_table(U, y, x)
    if ZH:
        for a, b, e, f, q, r in itertools.product(range(5), repeat=6):
            wd = (U, LET[e], LET[r], LET[q], LET[b])
            if isR5(list(wd)): continue
            W[a, b, 0, e, f, :, q, r, :] += ZV.get(zkey(wd, c2(LET[f]), c2(LET[a])), 0.0)
    if V6 and U == 7:
        for a, b, e, f, q, r in itertools.product(range(5), repeat=6):
            sv0 = sigv_of(U, LET[e], LET[r], LET[q], LET[b], LET[f], LET[a])
            if not F16:
                ks = sigv_keys(sv0)
                if ks: W[a, b, 1, e, f, :, q, r, :] -= min(VV.get(k, 0.0) for k in ks)
                continue
            for p_, s_ in itertools.product(range(5), repeat=2):
                ks = sigv_keys(sv0 + (amask(U, LET[a], LET[b], LET[e], LET[f], LET[p_], LET[q], LET[r], LET[s_]),))
                if ks: W[a, b, 1, e, f, p_, q, r, s_] -= min(VV.get(k, 0.0) for k in ks)
    if Q7:
        for b, e, q, r in itertools.product(range(5), repeat=4):
            sg = q7sig(U, LET[e], LET[r], LET[q], LET[b]); ks = q7keys(sg)
            if ks: W[:, b, 2, e, :, :, q, r, :] += max(QV.get(k, 0.0) for k in ks)
    if H5:
        for b, c, e, f, q, s_ in itertools.product(range(5), repeat=6):
            K_ = h5_recv(LET[b], LET[c], LET[e], LET[f], LET[q], LET[s_])
            W[:, b, c, e, f, :, q, 0, s_] += RV.get(K_, 0.0) - RRV.get(K_, 0.0)
    for a, b, e, f, q, r in itertools.product(range(5), repeat=6):
        if not AP and (a or f): continue
        sg = sig2_of(U, LET[e], LET[r], LET[q], LET[b], LET[f], LET[a])
        if F16:
            for p_, s_ in itertools.product(range(5), repeat=2):
                v = MV2(sg + (amask(U, LET[a], LET[b], LET[e], LET[f], LET[p_], LET[q], LET[r], LET[s_]),))
                if v is not None: W[a, b, 1, e, f, p_, q, r, s_] += v
            continue
        v = MV2(sg)
        if v is None: continue
        if AP: W[a, b, 1, e, f, :, q, r, :] += v
        else: W[:, b, 1, e, :, :, q, r, :] += v
    return W
def class_table_R2(xon):
    g = np.indices((5,) * 9, dtype=np.int64)
    a, b, c, e, f, p, q, r, s_ = g
    C = np.where(c == 0, 1 + ((b * 5 + e) * 5 + q) * 5 + r, 0)
    if ZH: C = np.where(c == 0, 1 + 100000000 + (((((a * 5 + b) * 5 + e) * 5 + f) * 5 + q) * 5 + r), C)
    C = np.where(c == 1, 1 + 625 + (((((a * 5 + b) * 5 + e) * 5 + f) * 5 + q) * 5 + r), C)
    if F16: C = np.where(c == 1, 1 + 625 + (((((((a * 5 + b) * 5 + e) * 5 + f) * 5 + q) * 5 + r) * 5 + p) * 5 + s_), C)
    o16 = 390625 - 15625 if F16 else 0
    if xon: C = np.where(c >= 2, 1 + 625 + 15625 + o16 + c * 15625 + (((((a * 5 + b) * 5 + e) * 5 + f) * 5 + q) * 5 + r), C)
    if H5:   # the hat-channel outflow at a position with s_i = 5 depends on (b, c, e, f, q, s): fold its key id into the class
        assert int(C.max()) < 500000
        ids = {}; T = np.zeros((5,) * 6, dtype=np.int64)
        for b_, c_, e_, f_, q_, s2 in itertools.product(range(5), repeat=6):
            T[b_, c_, e_, f_, q_, s2] = ids.setdefault(h5_recv(LET[b_], LET[c_], LET[e_], LET[f_], LET[q_], LET[s2]), len(ids)) + 1
        C = np.where(r == 0, C + 500000 * T[b, c, e, f, q, s_], C)
        assert int(C.max()) < 2 ** 31 - 1
    return C.astype(np.int32)
def recv_coef_R2(d, lk, sv, xon):
    cy, cx = recv_coef(d, lk, sv, xon); cf = collections.Counter()
    for r_, c in cy.items(): cf[('y', r_)] += c
    for r_, c in cx.items():
        if c: cf[('x', r_)] += c
    U = min(d, 9); w = [int(ch) for ch in lk]; s = [int(ch) for ch in sv]
    for j in range(d):
        if w[j] == 6:
            sg = sig2_of(U, w[(j + 1) % d], s[j], s[(j - 1) % d], w[(j - 1) % d], w[(j + 2) % d], w[(j - 2) % d])
            if F16: am = amask(U, w[(j - 2) % d], w[(j - 1) % d], w[(j + 1) % d], w[(j + 2) % d], s[(j - 2) % d], s[(j - 1) % d], s[j], s[(j + 1) % d]); sg = sg + (am,)
            if sig2_keys(sg): cf[('M', sg)] += 1
        if w[j] == 6 and V6 and U == 7 and d == 7:
            sv_ = sigv_of(U, w[(j + 1) % d], s[j], s[(j - 1) % d], w[(j - 1) % d], w[(j + 2) % d], w[(j - 2) % d])
            if F16: sv_ = sv_ + (am,)
            if sigv_keys(sv_): cf[('V', sv_)] -= 1
        if w[j] == 7 and Q7:
            sg = q7sig(U, w[(j + 1) % d], s[j], s[(j - 1) % d], w[(j - 1) % d])
            if q7keys(sg): cf[('Q', sg)] += 1
        if w[j] == 5 and ZH:
            cf[('z', zkey((U, w[(j + 1) % d], s[j], s[(j - 1) % d], w[(j - 1) % d]), c2(w[(j + 2) % d]), c2(w[(j - 2) % d])))] += 1
    if H5:
        for i in range(d):
            if s[i] == 5:
                for k2, c2v in hat_recv_terms(h5_recv(w[(i - 1) % d], w[i], w[(i + 1) % d], w[(i + 2) % d], s[(i - 1) % d], s[(i + 1) % d])).items(): cf[k2] += c2v
    if Q7 and d == 7:
        for k, m in q7_inflow(w).items(): cf[('q', k)] -= m
    return cf
def cmd_orientR2():
    bad = 0; n = 0
    for a in itertools.product(LET, repeat=7):
        n += 1
        if g2_of(*a) != g2_of(a[4], a[3], a[2], a[1], a[0], a[6], a[5]): bad += 1
        if sig2_of(*a) != sig2_of(a[0], a[4], a[3], a[2], a[1], a[6], a[5]): bad += 1
    for n_ in itertools.product(LET, repeat=5):
        for hr, hl in ((0, 1), (1, 0), (1, 1), (0, 0)):
            n += 1
            if zkey(n_, hr, hl) != zkey((n_[0], n_[4], n_[3], n_[2], n_[1]), hl, hr): bad += 1
    for L in itertools.product(LET, repeat=6):
        for ar, al in ((5, 7), (8, 6), (9, 9)):
            if h2_of(L, ar, al) != h2_of((L[0],) + tuple(reversed(L[1:])), al, ar): bad += 1
    # physical: conservation coefficients invariant under rotating / reflecting the whole 6-centred arrangement
    rng = np.random.default_rng(1)
    for _ in range(20000):
        L = tuple(int(v) for v in rng.choice(LET, 6)); s = tuple(int(v) for v in rng.choice(LET, 6)); k = int(rng.integers(6))
        Lr = L[k:] + L[:k]; sr = s[k:] + s[:k]
        Lf = tuple(L[(-i) % 6] for i in range(6)); sf = tuple(s[(-i - 1) % 6] for i in range(6))
        if cons2_coef(L, s) != cons2_coef(Lr, sr) or cons2_coef(L, s) != cons2_coef(Lf, sf): bad += 1
    if V6:
        for a in itertools.product(LET, repeat=7):
            n += 1
            if sigv_of(*a) != sigv_of(a[0], a[4], a[3], a[2], a[1], a[6], a[5]): bad += 1
        for L in itertools.product(LET, repeat=6):
            for ar, al in ((5, 6), (6, 9), (8, 5)):
                if v_of(L, ar, al) != v_of((L[0],) + tuple(reversed(L[1:])), al, ar): bad += 1
    if Q7:
        for _ in range(20000):
            w = tuple(int(v) for v in rng.choice(LET, 7)); j = int(rng.integers(7))
            if w[j] < 7 or ''.join(map(str, canon(w))) in RBIG: continue
            n += 1; kin = qkey(tuple(w[(j + i) % 7] for i in range(7)))
            W_ = lambda k: w[k % 7]
            for sg in (q7sig(w[j], W_(j + 1), W_(j + 2), W_(j - 2), W_(j - 1)), q7sig(w[j], W_(j - 1), W_(j - 2), W_(j + 2), W_(j + 1))):
                if kin not in q7keys(sg): bad += 1
            if q7_inflow(w) != q7_inflow(canon(w)): bad += 1
    if HX:
        nx_, bx_ = hatx_selftest(int(OPT.get('ntest', '100000')), 'brokenkey' in FLAGS); log('hatx physical test: %d spoke readings, %d mismatches%s' % (nx_, bx_, ' (BROKEN-KEY CONTROL)' if 'brokenkey' in FLAGS else '')); bad += bx_
    if H5:
        nh_, bh_ = hat5_selftest(int(OPT.get('ntest', '100000')), 'brokenkey' in FLAGS); log('hat5 physical test: %d random diamonds, %d with sender key != receiver key%s%s' % (nh_, bh_, ' or r/rr coefficients not conserving / rr not b -> v' if HRR else '', ''.join(t_ for f_, t_ in (('brokenkey', ' (BROKEN-KEY CONTROL)'), ('brokensign', ' (BROKEN-SIGN CONTROL)')) if f_ in FLAGS))); bad += bh_
    if F5:
        nf_, bf_ = face_selftest(); log('face5 physical test: %d faces, %d with nonzero net f' % (nf_, bf_)); bad += bf_
    log('orientation test R6x2 (apex %s): %d + %d + 20000 cases, %d mismatches' % (AP, n, 3 * 5 ** 6, bad))
def cmd_solveR2():
    import highspy
    load_patterns()
    xon = 'xon' in FLAGS; XCAP = float(OPT.get('xcap', '3')); XPEN = [float(OPT.get('xpen', '0'))]
    p = os.path.join(WORK, 'clsR2_%d%s%s.bin' % (int(xon), 'z' if ZH else '', 'f' if F16 else ''))
    if not os.path.exists(p): class_table_R2(xon).tofile(p)
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
    for r_ in ROOTS: col(('y', r_))
    info = []; have = set(); msig = set(); conset = set(); qsig = set(); vsig = set()
    def addrow(cf, lo, hi, inf_):
        idx = np.array([col(k) for k in cf], dtype=np.int32); val = np.array([float(v) for v in cf.values()])
        h.addRow(lo, hi, len(idx), idx, val); info.append(inf_)
    SR = R2_sender_rows()
    for wd, cf, bits in SR:
        c2_ = dict(cf); c2_[('t',)] = 1.0; addrow(c2_, 1.0, inf, ('senderR2', wd, bits))
    RW = all6_words() if V6 else relay_words()   # v6: no-five 6-types must conserve too (v out = h in)
    def addsig(sg):
        if sg in msig: return
        msig.add(sg)
        for k in sig2_keys(sg): addrow({('h', k): 1.0, ('M', sg): -1.0}, -inf, 0.0, ('mrowR2', list(sg), list(k)))
    def recv(d, lk, sv):
        cf = recv_coef_R2(d, lk, sv, xon)
        key = (d, tuple(sorted(cf.items(), key=str)))
        if key in have: return False
        have.add(key)
        for k in cf:
            if k[0] == 'M': addsig(k[1])
            if k[0] == 'V' and k[1] not in vsig:
                vsig.add(k[1])
                for kk in sigv_keys(k[1]): addrow({('V', k[1]): 1.0, ('v', kk): -1.0}, -inf, 0.0, ('mrowV', list(k[1]), list(kk)))
            if k[0] == 'Q' and k[1] not in qsig:
                qsig.add(k[1])
                for kk in q7keys(k[1]): addrow({('q', kk): 1.0, ('Q', k[1]): -1.0}, -inf, 0.0, ('mrowQ', list(k[1]), list(kk)))
        c2_ = dict(cf); c2_[('t',)] = -1.0
        addrow(c2_, -inf, d - 6.0, ('receiverR2', d, lk, sv)); return True
    def addcons(L, s):
        cf = {k: v for k, v in cons2_coef(L, s).items() if v}
        kk = tuple(sorted(cf.items()))
        if not cf or kk in conset: return False
        conset.add(kk); addrow(cf, 0.0, 0.0, ('cons2', list(L), list(s))); return True
    # initial conservation rows: one apex word per L (all apexes 5) -- the rest by separation
    for L in RW: addcons(L, (5,) * 6)
    if 'consbasis' in OPT:
        nb = sum(addcons(tuple(L), tuple(s_)) for L, s_ in json.load(open(OPT['consbasis'])))
        log('conservation basis rows added: %d' % nb)
    if 'warm' in OPT:
        nw = 0
        for fn in OPT['warm'].split(','):
            for line in open(fn):
                m = re.match(r'^R (\d+) (\d+) (\d+)', line)
                if m and admissible(int(m.group(1)), m.group(2), m.group(3)) is None: nw += recv(int(m.group(1)), m.group(2), m.group(3))
        log('warm rows admitted: %d' % nw)
    ng = sum(1 for k in cols if k[0] == 'g')
    log('R6x2 (apex %s): %d sender rows, %d g keys in senders, %d six-words, %d initial cons rows, %d M sigs' % (AP, len(SR), ng, len(RW), len(conset), len(msig)))
    if 'structonly' in FLAGS: return h, cols, info, conset, RW, SR
    T0 = time.time(); rowlog = open(os.path.join(HERE, 'rows_%s.txt' % OPT.get('tag', 'run')), 'w')
    for it in range(MAXIT):
        t1 = time.time()
        if 'ipm0' in FLAGS: h.setOptionValue('solver', 'ipm' if it == 0 else 'simplex')
        h.run(); xv = np.array(h.getSolution().col_value); t = xv[jt]
        y = np.array([xv[cols[('y', r_)]] for r_ in ROOTS])
        GV = {k[1]: xv[i] for k, i in cols.items() if k[0] == 'g'}; HV2 = {k[1]: xv[i] for k, i in cols.items() if k[0] == 'h'}
        ZV.clear(); ZV.update({k[1]: xv[i] for k, i in cols.items() if k[0] == 'z'})
        QV.clear(); QV.update({k[1]: xv[i] for k, i in cols.items() if k[0] == 'q'})
        VV.clear(); VV.update({k[1]: xv[i] for k, i in cols.items() if k[0] == 'v'})
        RV.clear(); RV.update({k[1]: xv[i] for k, i in cols.items() if k[0] == 'r'})
        RRV.clear(); RRV.update({k[1]: xv[i] for k, i in cols.items() if k[0] == 'rr'})
        if Q7: write_bonus()
        xd = {k[1]: xv[i] for k, i in cols.items() if k[0] == 'x' and xv[i] > 1e-12}
        mcache = {}
        def MV2(sg):
            if sg not in mcache:
                ks = sig2_keys(sg); mcache[sg] = max(HV2.get(k, 0.0) for k in ks) if ks else None
            return mcache[sg]
        tlp = time.time() - t1; added = 0; per = {}
        if 'nosep' in FLAGS: log('nosep: LP over the warm rows only, t = %.12f (a lower bound once lowerR2 checks the cert)' % t); break
        nc = 0; worst = 0.0
        for L in RW:   # conservation separation
            D = cons2_delta(L, GV, HV2)
            for idx in (int(np.argmax(D)), int(np.argmin(D))):
                if abs(D[idx]) > 1e-9:
                    worst = max(worst, abs(D[idx]))
                    if addcons(L, tuple(LET[v] for v in SALL[idx])): nc += 1
        added += nc; per['cons'] = (nc, round(worst, 6))
        Wc = {}
        for d in range(7, DMAX + 1):
            U = min(d, 9)
            if U not in Wc: Wc[U] = window_table_R2(U, y, xd, MV2)
            rr, dt, ni = run_sep(d, Wc[U], d - 6 + t + TOL, K, 2)
            n = 0; mx = None
            for r_ in rr:
                if r_[0] == 'V':
                    mx = max(mx or -1e9, float(r_[1]) - (d - 6 + t))
                    if 'dbg' in FLAGS and n == 0:
                        cf = recv_coef_R2(d, r_[2], r_[3], xon)
                        val = sum(v * (MV2(k[1]) if k[0] == 'M' else max([QV.get(kk, 0.0) for kk in q7keys(k[1])] or [0.0]) if k[0] == 'Q' else min([VV.get(kk, 0.0) for kk in sigv_keys(k[1])] or [0.0]) if k[0] == 'V' else xv[cols[k]] if k in cols and cols[k] < len(xv) else 0) for k, v in cf.items())
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
        rowlog.flush()
        log('iter %d t=%.12f rows %d cols %d added %d  lp %.1fs total %.0fs  %s' % (it, t, h.getNumRow(), h.getNumCol(), added, tlp, time.time() - T0, {d: v for d, v in per.items() if v[0]}))
        if not added and XPEN[0] and 'keeppen' in FLAGS:
            log('  converged with x penalty; keeppen: stopping here (no violated row at this solution; sol = this solution)'); break
        if not added and XPEN[0]:
            XPEN[0] = 0.0
            for k, i in cols.items():
                if k[0] == 'x': h.changeColCost(i, 0.0)
            log('  converged with x penalty; penalty removed, continuing'); continue
        if not added: break
    sol = h.getSolution(); xv = np.array(sol.col_value); t = xv[jt]; duals = np.array(sol.row_dual)
    tag = OPT.get('tag', 'run')
    S = {'t': float(t), 'model': 'R6x2', 'apex': AP, 'xon': xon,
         'y': {rname(k[1]): float(xv[i]) for k, i in cols.items() if k[0] == 'y' and xv[i] > 0},
         'g': [[list(k[1]), float(xv[i])] for k, i in cols.items() if k[0] == 'g' and xv[i] > 0],
         'h': [[list(k[1]), float(xv[i])] for k, i in cols.items() if k[0] == 'h' and xv[i] > 0],
         'z': [[list(k[1]), float(xv[i])] for k, i in cols.items() if k[0] == 'z' and xv[i] > 0], 'zh': ZH, 'apexcls': AC,
         'q': [[list(k[1]), float(xv[i])] for k, i in cols.items() if k[0] == 'q' and xv[i] > 0], 'q7': Q7,
         'v': [[list(k[1]), float(xv[i])] for k, i in cols.items() if k[0] == 'v' and xv[i] > 0], 'v6': V6,
         'f': [[list(k[1]), float(xv[i])] for k, i in cols.items() if k[0] == 'f' and xv[i] > 0], 'face5': F5,
         'r': [[list(k[1]), float(xv[i])] for k, i in cols.items() if k[0] == 'r' and xv[i] > 0], 'hat5': H5,
         'rr': [[list(k[1]), float(xv[i])] for k, i in cols.items() if k[0] == 'rr' and xv[i] > 0], 'hatrr': HRR,
         'V': [[list(k[1]), float(xv[i]), min([float(xv[cols[('v', kk)]]) if ('v', kk) in cols else 0.0 for kk in sigv_keys(k[1])] or [0.0])] for k, i in cols.items() if k[0] == 'V'],
         'x': {str(k[1]): float(xv[i]) for k, i in cols.items() if k[0] == 'x' and xv[i] > 0}}
    json.dump(S, open(os.path.join(HERE, 'sol_%s.json' % tag), 'w'))
    cert = [{'w': float(dv), 'row': info[i]} for i, dv in enumerate(duals) if abs(dv) > 1e-11]
    json.dump(cert, open(os.path.join(HERE, 'cert_%s.json' % tag), 'w'), indent=0)
    log('LP t* = %.12f ; dual rows %d ; wrote sol_%s.json cert_%s.json' % (t, len(cert), tag, tag))
    for c in sorted(cert, key=lambda c: -abs(c['w'])):
        if c['row'][0] in ('senderR2', 'receiverR2'): log('  %+.9f %s' % (c['w'], ' '.join(map(str, c['row'][:4]))))
    log('  (+ %d cons2 / mrowR2 rows)' % sum(1 for c in cert if c['row'][0] in ('cons2', 'mrowR2')))
def cons2_block(L):
    """dense conservation block of link L over all 5^6 apex words: (matrix, local key list)"""
    terms = []
    for i in range(6):
        if L[i] == 5: terms.append((i, 1.0, [[('g', g2_of(L[(i + 1) % 6], L[(i + 2) % 6], L[(i + 3) % 6], L[(i + 4) % 6], L[(i + 5) % 6], LET[a], LET[b])) for b in range(5)] for a in range(5)]))
    for j in range(6):
        if L[j] >= 7:
            m = tuple(L[(j + i) % 6] for i in range(6))
            terms.append((j, -1.0, [[('h', h2_of(m, LET[a], LET[b])) for b in range(5)] for a in range(5)]))
            if V6 and L[j] == 7: terms.append((j, 1.0, [[('v', v_of(m, LET[a], LET[b])) for b in range(5)] for a in range(5)]))
    keys = {}
    for _, _, T in terms:
        for rw in T:
            for k in rw: keys.setdefault(k, len(keys))
    A = np.zeros((len(SALL), len(keys))); rid = np.arange(len(SALL))
    for i, sgn, T in terms:
        I = np.array([[keys[k] for k in rw] for rw in T])
        np.add.at(A, (rid, I[SALL[:, i], SALL[:, (i - 1) % 6]]), sgn)
    return A, list(keys)
def cmd_structR2():
    FLAGS.add('structonly')
    h, cols, info, conset, RW, SR = cmd_solveR2()
    # full conservation system over all L in RW x all 5^6 apex words. h keys are private to one L (the key fixes L),
    # so rank = sum_L rank(H_L) + rank of the stacked g-only consequences of each block.
    allg = {}; allh = set(); allv = set(); nrows = 0; rH = 0; Gstack = []; rL_tot = 0; gonly = set()
    for L in RW:
        A, ks = cons2_block(L)
        U_ = np.unique(A, axis=0); U_ = U_[np.abs(U_).sum(1) > 0]
        hi = [c for c, k in enumerate(ks) if k[0] != 'g']; gi = [c for c, k in enumerate(ks) if k[0] == 'g']
        for k in ks:
            if k[0] == 'g': allg.setdefault(k, len(allg))
            elif k[0] == 'h': allh.add(k)
            else: allv.add(k)
        if not hi:
            for r_ in U_: gonly.add(tuple((ks[c], r_[c]) for c in np.nonzero(r_)[0]))
        else: nrows += len(U_)
        if not len(U_) or not len(ks): continue
        u, sv, vt = np.linalg.svd(U_, full_matrices=False); r = int((sv > 1e-9 * max(1, sv[0])).sum()); B = vt[:r]
        rL_tot += r
        Bh = B[:, hi]
        if hi:
            u2, s2, v2 = np.linalg.svd(Bh, full_matrices=True); r2 = int((s2 > 1e-9 * max(1, s2[0] if len(s2) else 1)).sum())
            N = u2[:, r2:].T            # combos with zero h part
        else: r2 = 0; N = np.eye(r)
        rH += r2
        if len(N):
            Gp = N @ B[:, gi]; G = np.zeros((len(N), 0))
            Gstack.append((Gp, [allg[ks[c]] for c in gi]))
    nrows += len(gonly)
    Gall = np.zeros((sum(len(g) for g, _ in Gstack), len(allg))); o = 0
    for g, idx in Gstack: Gall[o:o + len(g), idx] = g; o += len(g)
    rG = np.linalg.matrix_rank(Gall) if len(Gall) else 0
    sg = set()
    for U in BIGL:
        for t7 in itertools.product(LET, repeat=6):
            wr, sr, sl, wl, wrr, wll = t7
            if not AP and (wrr != 5 or wll != 5): continue
            s_ = sig2_of(U, wr, sr, sl, wl, wrr, wll)
            if F16:   # one signature per allowed-private set seen in some window (s_{j-2}, s_{j+1} free)
                for s0, s3 in itertools.product(LET, repeat=2):
                    x_ = s_ + (amask(U, wll, wl, wr, wrr, s0, sl, sr, s3),)
                    if sig2_keys(x_): sg.add(x_)
                continue
            if sig2_keys(s_): sg.add(s_)
    nm = sum(len(sig2_keys(s_)) for s_ in sg)
    gs = sum(1 for k in cols if k[0] == 'g')
    out = ['s12 structural summary (%s)' % ('full s12 keys' if AP else 'fallback = s10 keys'),
           'registry: %s + RSST-D + L2 (xcap 3)' % os.path.basename(OPT.get('args', '?')).replace('.txt', ''),
           'key counts by type:',
           '  y (five -> big, s1 roots): %d' % len(ROOTS),
           '  g (five -> 6): %d in conservation rows, %d of them read by sender rows' % (len(allg), gs),
           '  h (6 -> big): %d' % len(allh),
           '  M (receiver inflow signatures): %d' % len(sg),
           '  x (big-big, tau codes): lazy',
           '6-types (canonical non-R6 6-links%s): %d' % ('' if V6 else ' with a five', len(RW)),
           'conservation rows (distinct, all 6-types x all apex words): %d' % nrows,
           'conservation rank: %d (= %d from h-blocks + %d g-only)' % (rH + rG, rH, rG),
           '  g-only part: rank %d on %d g keys; g directions left free: %d' % (rG, len(allg), len(allg) - rG),
           'row counts at start of solve: sender %d ; conservation %d (rest by separation) ; M-rows if all used %d ; receivers by separation' % (len(SR), len(conset), nm)]
    if V6:
        vs = set()
        for t7 in itertools.product(LET, repeat=6):
            s_ = sigv_of(7, *t7)
            if F16:
                wr, sr, sl, wl, wrr, wll = t7
                for s0, s3 in itertools.product(LET, repeat=2):
                    x_ = s_ + (amask(7, wll, wl, wr, wrr, s0, sl, sr, s3),)
                    if sigv_keys(x_): vs.add(x_)
                continue
            if sigv_keys(s_): vs.add(s_)
        out.insert(6, '  v (new in s16): %d' % len(allv)); out.insert(7, '  V (new in s16, signatures): %d; V-rows if all used %d' % (len(vs), sum(len(sigv_keys(x)) for x in vs)))
        out[0] = 's16 structural summary (stage 15 class on the reduced 6-centred relay)'
        out = [l.replace('from h-blocks', 'from private blocks') for l in out]
    if ZH:
        zk = set()
        for wd, cf, b in SR: zk.update(k for k in cf if k[0] == 'z')
        out.insert(4, '  z (big -> five, second split): %d' % len(zk))
    open(OPT.get('structout', os.path.join(HERE, 's12_struct%s.txt' % ('' if AP else '_noapex'))), 'w').write('\n'.join(out) + '\n')
    for l in out: log(l)
def cmd_lowerR2():
    """exact check from signed duals (as lowerR): senderR2 >= (w>=0), cons2 = (any sign), mrowR2 h - M <= 0 (w<=0),
    receiverR2 <= (w<=0); rows re-derived from labels; rescale so t's reduced cost is 0; x priced at its cap."""
    load_patterns()
    xon = 'xon' in FLAGS; XCAP = Fraction(OPT.get('xcap', '3')); C = json.load(open(OPT['cert']))
    SR = {(wd, tuple(map(str, b))): cf for wd, cf, b in R2_sender_rows()}
    tot = collections.defaultdict(Fraction); D = Fraction(0); ok = True; tco = Fraction(0); cnt = collections.Counter()
    for c in C:
        w = Fraction(c['w']).limit_denominator(10 ** 7); row = c['row']; cnt[row[0]] += 1
        if row[0] == 'senderR2':
            cf = SR.get((row[1], tuple(map(str, row[2]))))
            if cf is None: log('  NOT A SENDER ROW', row); ok = False; continue
            if w < 0: log('  WRONG SIGN', row); ok = False; continue
            for k, v in cf.items(): tot[k] += w * v
            tco += w; D += w
        elif row[0] == 'cons2':
            L = tuple(row[1]); s = tuple(row[2])
            if isR6(L) or len(L) != 6 or len(s) != 6 or any(v not in LET for v in L + s): log('  BAD CONS2', row); ok = False; continue
            for k, v in cons2_coef(L, s).items(): tot[k] += w * v
        elif row[0] == 'mrowR2':
            sg = tuple(row[1]); k = tuple(row[2])
            g0 = sg[:-1] if F16 else sg
            if F16 and not (0 <= sg[-1] < 32): log('  BAD MASK', row); ok = False; continue
            if len(g0) != (7 if AP else 5) or g0 != sig2_of(*(g0 if AP else g0 + (5, 5))): log('  NONCANON SIG', row); ok = False; continue
            if k not in sig2_keys(sg): log('  BAD MROW', row); ok = False; continue
            if w > 0: log('  WRONG SIGN', row); ok = False; continue
            tot[('h', k)] += w; tot[('M', sg)] -= w
        elif row[0] == 'mrowV':
            sg = tuple(row[1]); k = tuple(row[2])
            g0 = sg[:7]
            if g0 != sigv_of(*g0) or len(sg) != (8 if F16 else 7) or k not in sigv_keys(sg): log('  BAD MROWV', row); ok = False; continue
            if w > 0: log('  WRONG SIGN', row); ok = False; continue
            tot[('V', sg)] += w; tot[('v', k)] -= w
        elif row[0] == 'mrowQ':
            sg = tuple(row[1]); k = tuple(row[2])
            if sg != q7sig(*sg) or k not in q7keys(sg): log('  BAD MROWQ', row); ok = False; continue
            if w > 0: log('  WRONG SIGN', row); ok = False; continue
            tot[('q', k)] += w; tot[('Q', sg)] -= w
        elif row[0] == 'receiverR2':
            d, lk, sv = int(row[1]), row[2], row[3]
            why = admissible(d, lk, sv)
            if why: log('  RECEIVER NOT ADMISSIBLE', row, why); ok = False; continue
            if w > 0: log('  WRONG SIGN', row); ok = False; continue
            for k, v in recv_coef_R2(d, lk, sv, xon).items(): tot[k] += w * v
            tco -= w; D += w * (d - 6)
        else: log('  UNKNOWN', row); ok = False
    if tco <= 0: log('  t coefficient sum not positive'); ok = False; tco = Fraction(1)
    D = D / tco; neg = []
    for k, v in tot.items():
        rc = -v / tco
        if rc < 0:
            if k[0] == 'x': D += rc * XCAP
            else: neg.append((k, rc))
    if neg: log('  negative reduced costs:', len(neg), neg[:5]); ok = False
    log('rows by type: %s' % dict(cnt))
    log('LOWER-R2: %s  t >= %s = %.9f  (%d rows)' % ('VALID' if ok else 'INVALID', D, float(D), len(C)))
def all6_words():
    out = set()
    for L in itertools.product(LET, repeat=6):
        c = canon6(L)
        if c not in out and not isR6(c): out.add(c)
    return sorted(out)
def cmd_upperR2():
    load_patterns()
    xon = 'xon' in FLAGS
    p = os.path.join(WORK, 'clsR2_%d%s%s.bin' % (int(xon), 'z' if ZH else '', 'f' if F16 else ''))
    if not os.path.exists(p): class_table_R2(xon).tofile(p)
    CLSFILE[0] = p
    Sj = json.load(open(OPT['sol'])); t = Sj['t']
    y = np.zeros(len(ROOTS))
    for k, v in Sj['y'].items():
        u, rest = k.split('|'); r_ = root(list((int(u),) + tuple(int(c) for c in rest)), 0); y[RIX[r_]] = v
    GV = {tuple(k): v for k, v in Sj['g']}; HV2 = {tuple(k): v for k, v in Sj['h']}
    ZV.clear(); ZV.update({tuple(k): v for k, v in Sj.get('z', [])})
    if Sj.get('z') and not ZH: log('SOLUTION HAS z BUT zh FLAG OFF'); return
    QV.clear(); QV.update({tuple(k): v for k, v in Sj.get('q', [])})
    if Sj.get('q') and not Q7: log('SOLUTION HAS q BUT q7 FLAG OFF'); return
    if Q7: log('bonus links: %d' % write_bonus())
    VV.clear(); VV.update({tuple(k): v for k, v in Sj.get('v', [])})
    if Sj.get('v') and not V6: log('SOLUTION HAS v BUT v6 FLAG OFF'); return
    RV.clear(); RV.update({tuple(k): v for k, v in Sj.get('r', [])})
    if Sj.get('r') and not H5: log('SOLUTION HAS r BUT hat5 FLAG OFF'); return
    RRV.clear(); RRV.update({tuple(k): v for k, v in Sj.get('rr', [])})
    if Sj.get('rr') and not HRR: log('SOLUTION HAS rr BUT hatrr FLAG OFF'); return
    FV.clear(); FV.update({tuple(k): v for k, v in Sj.get('f', [])})
    if Sj.get('f') and not F5: log('SOLUTION HAS f BUT face5 FLAG OFF'); return
    xd = {int(k): v for k, v in Sj.get('x', {}).items()}
    if any(v < 0 for v in list(GV.values()) + list(HV2.values()) + list(y) + list(FV.values()) + list(RV.values()) + list(RRV.values())): log('NEGATIVE VALUE'); 
    bad = 0
    for wd, cf, bits in R2_sender_rows():
        v = sum(c * (y[RIX[k[1]]] if k[0] == 'y' else ZV.get(k[1], 0.0) if k[0] == 'z' else FV.get(k[1], 0.0) if k[0] == 'f' else RV.get(k[1], 0.0) if k[0] == 'r' else RRV.get(k[1], 0.0) if k[0] == 'rr' else GV.get(k[1], 0.0)) for k, c in cf.items())
        if v < 1 - t - EPS: bad += 1
    log('sender rows violated: %d' % bad)
    nc = 0; worst = 0.0; A6 = all6_words()
    for L in A6:   # every non-R6 6-arrangement, with or without a five, every apex word
        Dl = cons2_delta(L, GV, HV2); m = float(np.abs(Dl).max()); worst = max(worst, m)
        if m > 1e-9:
            nc += 1
            if nc <= 8: log("  cons off: L=%s five=%s worst %.4g" % (L, 5 in L, m))
    log('conservation: %d canonical non-R6 links x 5^6 apex words; links with |in - out| > 1e-9: %d (worst %.3g)' % (len(A6), nc, worst)); bad += nc
    mcache = {}
    def MV2(sg):
        if sg not in mcache:
            ks = sig2_keys(sg); mcache[sg] = max(HV2.get(k, 0.0) for k in ks) if ks else None
        return mcache[sg]
    for d in range(7, DMAX + 1):
        W = window_table_R2(min(d, 9), y, xd, MV2)
        res, dt, ni = run_sep(d, W, d - 6 + t + EPS, 20, 0)
        v = [r for r in res if r[0] == 'V']; bad += len(v)
        log('d=%d: %d violated (exhaustive, %.1fs)' % (d, len(v), dt))
    W9 = window_table_R2(9, y, xd, MV2); M = relaxed_M(W9)
    for d in range(DMAX + 1, DTAIL + 1):
        v = closed_max(M, d)
        if v > d - 6 + t + EPS:
            res, dt, ni = run_sep(d, W9, d - 6 + t + EPS, 20, 0, pats=False); nv = sum(1 for r in res if r[0] == 'V'); bad += nv
            log('d=%d relaxed %.6f > cap; exact pattern-free: %d violated' % (d, v, nv))
    lam = karp(M); d0 = (6 - t) / (1 - lam) if lam < 1 else 1e9
    log('Karp lambda %.9f d0 %.3f' % (lam, d0))
    if d0 > DTAIL + 1: bad += 1
    log('UPPER-R2: %s at t = %.12f' % ('FEASIBLE' if bad == 0 else 'INFEASIBLE (%d)' % bad, t))
def cmd_ctxR2():
    """sender rows of the listed words in the context 'all hats and fans big' (bits all 1): value breakdown"""
    Sj = json.load(open(OPT['sol'])); t = Sj['t']
    GV = {tuple(k): v for k, v in Sj['g']}; YV = Sj['y']; GV.update({tuple(k): v for k, v in Sj.get('z', [])})
    def yv(r_): return YV.get(rname(r_), 0.0)
    for wd, cf, bits in R2_sender_rows():
        if wd not in OPT.get('words', '55677,56687').split(',') : continue
        b = [x for x in bits if x != '|']
        if not all(x == 1 for x in b): continue
        parts = ['%s%s=%.5f' % (k[0], ''.join(map(str, k[1])) if k[0] in 'gz' else rname(k[1]), (yv(k[1]) if k[0] == 'y' else GV.get(k[1], 0.0))) for k in cf]
        tot = sum(c * (yv(k[1]) if k[0] == 'y' else GV.get(k[1], 0.0)) for k, c in cf.items())
        log('%s all-big ring: total %.5f vs 1-t %.5f  %s' % (wd, tot, 1 - t, ' '.join(parts)))
def cmd_consbasisR2():
    """per 6-type L: a maximal independent set of actual conservation rows (L, s) (QR with column pivoting on A_L^T);
    together they imply every (L, s) row. Written as JSON [[L, s], ...]."""
    import scipy.linalg as sla
    out = []; tot = 0
    for L in (all6_words() if V6 else relay_words()):
        A, ks = cons2_block(L)
        U_, idx = np.unique(A, axis=0, return_index=True)
        keep = np.abs(U_).sum(1) > 0; U_ = U_[keep]; idx = idx[keep]
        if not len(U_): continue
        R, P = sla.qr(U_.T, mode='r', pivoting=True)
        dg = np.abs(np.diag(R)); r = int((dg > 1e-9 * max(1.0, dg[0])).sum())
        for q in P[:r]: out.append([list(L), [LET[v] for v in SALL[idx[q]]]])
        tot += r
    json.dump(out, open(OPT.get('out', os.path.join(HERE, 'cons2basis.json')), 'w'))
    log('conservation basis: %d rows over %d 6-types' % (tot, len(all6_words() if V6 else relay_words())))
def cmd_rowR2():
    """one receiver row at a solution: each term's value, load vs cap, slack, and its dual weight in cert"""
    load_patterns(); xon = 'xon' in FLAGS
    Sj = json.load(open(OPT['sol'])); t = Sj['t']; d = int(OPT['d']); lk = OPT['lk']; sv = OPT['sv']
    YV = Sj['y']; HV2 = {tuple(k): v for k, v in Sj['h']}; ZV.clear(); ZV.update({tuple(k): v for k, v in Sj.get('z', [])})
    XV = {int(k): v for k, v in Sj.get('x', {}).items()}; QV.clear(); QV.update({tuple(k): v for k, v in Sj.get('q', [])}); VV.clear(); VV.update({tuple(k): v for k, v in Sj.get('v', [])})
    def MV2(sg):
        ks = sig2_keys(sg); return max(HV2.get(k, 0.0) for k in ks) if ks else 0.0
    tot = 0.0; parts = []
    for k, c in sorted(recv_coef_R2(d, lk, sv, xon).items(), key=str):
        v = YV.get(rname(k[1]), 0.0) if k[0] == 'y' else dict((tuple(a), b) for a, b in Sj.get('r', [])).get(k[1], 0.0) if k[0] == 'r' else dict((tuple(a), b) for a, b in Sj.get('rr', [])).get(k[1], 0.0) if k[0] == 'rr' else ZV.get(k[1], 0.0) if k[0] == 'z' else XV.get(k[1], 0.0) if k[0] == 'x' else QV.get(k[1], 0.0) if k[0] == 'q' else VV.get(k[1], 0.0) if k[0] == 'v' else min([VV.get(kk, 0.0) for kk in sigv_keys(k[1])] or [0.0]) if k[0] == 'V' else max([QV.get(kk, 0.0) for kk in q7keys(k[1])] or [0.0]) if k[0] == 'Q' else MV2(k[1])
        tot += c * v
        if abs(c * v) > 1e-12: parts.append('%s%s:%+g*%.5f' % (k[0], rname(k[1]) if k[0] == 'y' else ''.join(map(str, k[1])) if k[0] != 'x' else k[1], c, v))
    w = 0.0
    if 'cert' in OPT:
        for c in json.load(open(OPT['cert'])):
            if c['row'][0] == 'receiverR2' and int(c['row'][1]) == d and c['row'][2] == lk and c['row'][3] == sv: w = c['w']
    log('row d=%d %s/%s: load %.9f cap %.9f slack %.3g dual %.9f admissible=%s' % (d, lk, sv, tot, d - 6 + t, d - 6 + t - tot, w, admissible(d, lk, sv)))
    log('  terms: ' + ' '.join(parts))
