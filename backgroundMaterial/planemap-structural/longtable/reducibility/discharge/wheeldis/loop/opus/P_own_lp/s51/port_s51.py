# s51 port (RELAY_SPEC_s51): flag xo = x-outer.  usage: python3 port_s51.py ENGDIR   (ENGDIR = a byte copy of s47/eng)
# Every new branch is guarded by XO (flag 'xo', default off), so the default code path is s47/eng's.
import sys, os
E = sys.argv[1]
def sub(src, old, new, n=1):
    assert src.count(old) == n, (old[:80], src.count(old))
    return src.replace(old, new)
p2 = os.path.join(E, 'prelay2.py'); s = open(p2).read()

# ---------------------------------------------------------------- (1) the xo helpers (after pallow; amask / F16 defined above)
s = sub(s, "def pallow(sig): return [p for i, p in enumerate(LET) if not F16 or (sig[-1] >> i) & 1]\n",
"""def pallow(sig): return [p for i, p in enumerate(LET) if not F16 or (sig[-1] >> i) & 1]
# ---- s51 (RELAY_SPEC_s51): x-outer.  xo[tauo] = refined L2 key (sides (c, a, b, ea, eb)); receiver credit XQ[q] per big link
# position, q = (U, V, A, B), A/B = visible side tuples (c, a, b, o, mask of the unseen outer letter); mrowX rows bound XQ.
XO = 'xo' in FLAGS
assert not XO or 'xon' in FLAGS, 'xo needs xon'
XOB = OPT.get('xobroken', '')        # controls only: 'end' = in-key outer letters read at the wrong end; 'sign' = receiver gets -XQ
assert XOB in ('', 'end', 'sign')
XOV = {}                             # tauo -> value (solution / LP)
XNOMASK = [False]                    # xoselftest only
def sidex(c, a, b, ea, eb): return (((LI[c] * 5 + LI[a]) * 5 + LI[b]) * 5 + LI[ea]) * 5 + LI[eb]
def tauo(fl, tl, s1, s2):
    lo, hi = min(s1, s2), max(s1, s2); return (((LI[fl] - 2) * 3 + (LI[tl] - 2)) * 3125 + lo) * 3125 + hi
def tauo_dec(t):
    hi = t % 3125; lo = (t // 3125) % 3125; fi, ti = divmod(t // 3125 ** 2, 3)
    dg = lambda S: tuple(5 + (S // 5 ** k) % 5 for k in (4, 3, 2, 1, 0))
    return (7 + fi, 7 + ti, dg(lo), dg(hi))
_XAU = {}
def xo_au(U, sg, k1, k2, k3, k4, k5, k6):
    \"\"\"51.3: OR of the 6's amask over the two letters outside u's window. sg = +1 (6 at i+1): k = (w_{i-1}, w_i, w_{i+2},
    s_{i-1}, s_i, s_{i+1}), outside w_{i+3}, s_{i+2}; sg = -1 (6 at i-1): k = (w_{i-2}, w_i, w_{i+1}, s_{i-2}, s_{i-1}, s_i),
    outside w_{i-3}, s_{i-3}.  31 without filt16.\"\"\"
    if not F16: return 31
    kk = (U, sg, k1, k2, k3, k4, k5, k6)
    if kk not in _XAU:
        m = 0
        for x_, y_ in itertools.product(LET, repeat=2):
            m |= amask(U, k1, k2, k3, x_, k4, k5, k6, y_) if sg > 0 else amask(U, x_, k1, k2, k3, y_, k4, k5, k6)
        _XAU[kk] = m
    return _XAU[kk]
_XNR = {}
def xo_nr6(U, x1, x2, x4, x5):
    \"\"\"bitmask of p with the 6-wheel (U, x1, x2, p, x4, x5) not R6\"\"\"
    kk = (U, x1, x2, x4, x5)
    if kk not in _XNR: _XNR[kk] = sum(1 << k for k, p in enumerate(LET) if not isR6([U, x1, x2, p, x4, x5]))
    return _XNR[kk]
def xo_vis(U, V, W_, S_):
    \"\"\"51.3: credit key q of the big link vertex w_i (letter V); W_(k) = w_{i+k}, S_(k) = s_{i+k} (letters)\"\"\"
    out = []
    for sg in (1, -1):
        if sg > 0: c, a, b, o = W_(1), S_(0), W_(2), S_(1)
        else: c, a, b, o = W_(-1), S_(-1), W_(-2), S_(-2)
        if c == 5: m = 1 << LI[o]
        elif c == 6 and XNOMASK[0]: m = 31
        elif c == 6:
            if sg > 0: m = xo_au(U, 1, W_(-1), W_(0), W_(2), S_(-1), S_(0), S_(1)) & xo_nr6(U, W_(2), S_(1), S_(0), W_(0))
            else: m = xo_au(U, -1, W_(-2), W_(0), W_(1), S_(-2), S_(-1), S_(0)) & xo_nr6(U, W_(0), S_(-1), S_(-2), W_(-2))
        else: m = 31
        out.append((c, a, b, o, m))
    return (U, V, min(out), max(out))
_XC = {}
def xo_cands(q):
    \"\"\"51.3: [(eA, eB, in key, out key)] over the masks of q\"\"\"
    if q not in _XC:
        U, V, A, B = q; res = []
        for eA in LET:
            if not (A[4] >> LI[eA]) & 1: continue
            for eB in LET:
                if not (B[4] >> LI[eB]) & 1: continue
                if XOB == 'end':   # broken control: the in-key's outer letters read at the wrong end (out-key correct), so the
                    # receiver's inflow no longer matches the sender's outflow (a one-sided bug; swapping both is a relabelling)
                    ti = tauo(V, U, sidex(A[0], A[1], A[2], A[3], eA), sidex(B[0], B[1], B[2], B[3], eB))
                    to = tauo(U, V, sidex(A[0], A[2], A[1], A[3], eA), sidex(B[0], B[2], B[1], B[3], eB))
                else:
                    ti = tauo(V, U, sidex(A[0], A[1], A[2], eA, A[3]), sidex(B[0], B[1], B[2], eB, B[3]))
                    to = tauo(U, V, sidex(A[0], A[2], A[1], A[3], eA), sidex(B[0], B[2], B[1], B[3], eB))
                res.append((eA, eB, ti, to))
        _XC[q] = res
    return _XC[q]
def xo_term(q): return q[2][4] != 0 and q[3][4] != 0 and any(ti != to for _, _, ti, to in xo_cands(q))
def xo_eff(q):
    \"\"\"XQeff(q) = max over the candidates of xo[in] - xo[out] (the smallest XQ the mrowX rows allow)\"\"\"
    return max((XOV.get(ti, 0.0) - XOV.get(to, 0.0)) if ti != to else 0.0 for _, _, ti, to in xo_cands(q))
def xo_recv_terms(d, w, s):
    cf = collections.Counter(); U = min(d, 9)
    for i in range(d):
        if w[i] < 7: continue
        q = xo_vis(U, w[i], lambda k, i=i: w[(i + k) % d], lambda k, i=i: s[(i + k) % d])
        if xo_term(q): cf[('XQ', q)] += -1 if XOB == 'sign' else 1
    return cf
def xo_mrows(q):
    \"\"\"the mrowX rows of q: (coefficients, [eA, eB])\"\"\"
    for eA, eB, ti, to in xo_cands(q):
        cf = collections.Counter({('XQ', q): -1})
        if ti != to: cf[('xo', ti)] += 1; cf[('xo', to)] -= 1
        yield dict(cf), [eA, eB]
def xo_win(W, U):
    \"\"\"51.5(4): + XQeff at every big-centred window touched by a positive xo key (all other windows: XQeff = 0)\"\"\"
    if not XO: return
    touched = set()
    for t_, v in XOV.items():
        if not v > 0: continue
        fl, tl, S1, S2 = tauo_dec(t_)
        for SP, SM in ((S1, S2), (S2, S1)):
            if tl == U:   # in key at V = fl: + side (c, s_i, w_{i+2}, e+, s_{i+1}), - side (c, s_{i-1}, w_{i-2}, e-, s_{i-2})
                o = 3 if XOB == 'end' else 4
                touched.add((fl, SM[2], SM[0], SP[0], SP[2], SM[o], SM[1], SP[1], SP[o]))
            if fl == U:   # out key at V = tl: + side (c, w_{i+2}, s_i, s_{i+1}, e+)
                o = 3
                touched.add((tl, SM[1], SM[0], SP[0], SP[1], SM[o], SM[2], SP[2], SP[o]))
    for V, a, b, e, f, p, q_, r, s_ in touched:
        Wl = {-2: a, -1: b, 0: V, 1: e, 2: f}; Sl = {-2: p, -1: q_, 0: r, 1: s_}
        q = xo_vis(U, V, Wl.__getitem__, Sl.__getitem__)
        if xo_term(q): W[LI[a], LI[b], LI[V], LI[e], LI[f], LI[p], LI[q_], LI[r], LI[s_]] += (-1 if XOB == 'sign' else 1) * xo_eff(q)
def cmd_xoselftest():
    \"\"\"s51: physical consistency of the xo key from both ends of an edge u - v (independent link-list construction).\"\"\"
    rng = np.random.default_rng(int(OPT.get('seed', '1'))); N = int(OPT.get('N', '20000')); bad = 0; n = 0
    XNOMASK[0] = True; _XC.clear()   # key reading only: 6-private masks = 31 here (domains are filt16 / R6 soundness, not tested)
    def L(): return int(rng.choice(LET))
    def nb(link, x, y):   # in the cyclic list link, the neighbour of x other than y
        k = link.index(x); m = len(link); a_, b_ = link[(k - 1) % m], link[(k + 1) % m]
        assert y in (a_, b_); return b_ if a_ == y else a_
    def phys(deg, links, fl, tl, cs):
        sides = []
        for c in cs:
            lk = links[c]; a_ = nb(lk, fl, tl); b_ = nb(lk, tl, fl); ea = nb(lk, a_, fl); eb = nb(lk, b_, tl)
            sides.append(sidex(deg[c], deg[a_], deg[b_], deg[ea], deg[eb]))
        return tauo(min(deg[fl], 9), min(deg[tl], 9), sides[0], sides[1])
    for it in range(N):
        du = int(rng.integers(7, 12)); dv = int(rng.integers(7, 12)); U = min(du, 9); V = min(dv, 9)
        deg = {'u': du, 'v': dv}
        for nm in ('cp', 'cm', 'si', 'sim', 'wp2', 'wm2', 'sp1', 'sm2'): deg[nm] = L()
        links = {}
        for c, si_, w2, s1 in (('cp', 'si', 'wp2', 'sp1'), ('cm', 'sim', 'wm2', 'sm2')):
            if deg[c] == 5: links[c] = ['u', 'v', si_, s1, w2]
            else:
                mid = ['%s_x%d' % (c, k) for k in range(deg[c] - 5)]
                for x_ in mid: deg[x_] = L()
                links[c] = ['u', 'v', si_] + mid + [s1, w2]
        e_p = nb(links['cp'], 'si', 'v'); e_m = nb(links['cm'], 'sim', 'v')
        # u's arrangement: position 0 = v; w_1 = c+, w_2 = w_{+2}, s_0 = s_i, s_1 = s_{i+1}; mirror on the - side; rest random
        wu = [None] * du; su = [None] * du
        wu[0] = dv; wu[1] = deg['cp']; wu[2] = deg['wp2']; wu[-1] = deg['cm']; wu[-2] = deg['wm2']
        su[0] = deg['si']; su[1] = deg['sp1']; su[-1] = deg['sim']; su[-2] = deg['sm2']
        for k in range(du):
            if wu[k] is None: wu[k] = L()
            if su[k] is None: su[k] = L()
        wu[0] = V
        # v's arrangement: position 0 = u; w'_1 = c+, w'_2 = s_i, w'_{-1} = c-, w'_{-2} = s_{i-1}; s'_0 = w_{+2}, s'_1 = e+, s'_{-1} = w_{-2}, s'_{-2} = e-
        wv = [None] * dv; sv_ = [None] * dv
        wv[0] = U; wv[1] = deg['cp']; wv[2] = deg['si']; wv[-1] = deg['cm']; wv[-2] = deg['sim']
        sv_[0] = deg['wp2']; sv_[1] = deg[e_p]; sv_[-1] = deg['wm2']; sv_[-2] = deg[e_m]
        for k in range(dv):
            if wv[k] is None: wv[k] = L()
            if sv_[k] is None: sv_[k] = L()
        t_vu = phys(deg, links, 'v', 'u', ('cp', 'cm')); t_uv = phys(deg, links, 'u', 'v', ('cp', 'cm'))
        qu = xo_vis(U, V, lambda k: wu[k % du], lambda k: su[k % du]); qv = xo_vis(V, U, lambda k: wv[k % dv], lambda k: sv_[k % dv])
        cu = xo_cands(qu); cv = xo_cands(qv)
        okm_u = any(ti == t_vu and to == t_uv for _, _, ti, to in cu); okm_v = any(ti == t_uv and to == t_vu for _, _, ti, to in cv)
        n += 1
        if not okm_u or not okm_v:
            bad += 1
            if bad <= 3: log('  xoselftest mismatch: u %s/%s v %s/%s true v->u %s u->v %s' % (wu, su, wv, sv_, tauo_dec(t_vu), tauo_dec(t_uv)))
    XNOMASK[0] = False; _XC.clear()
    log('xoselftest%s: %d edges (both ends), %d key mismatches' % (' (BROKEN %s)' % XOB if XOB else '', n, bad))
""")

# ---------------------------------------------------------------- (2) window term and class table
s = sub(s, "    fb_win(W, U)\n    return W\n", "    fb_win(W, U)\n    xo_win(W, U)   # s51\n    return W\n")
s = sub(s, "    if xon: C = np.where(c >= 2, 1 + 625 + 15625 + o16 + c * 15625 + (((((a * 5 + b) * 5 + e) * 5 + f) * 5 + q) * 5 + r), C)\n",
"""    if xon: C = np.where(c >= 2, 1 + 625 + 15625 + o16 + c * 15625 + (((((a * 5 + b) * 5 + e) * 5 + f) * 5 + q) * 5 + r), C)
    if XO: C = np.where(c >= 2, 1 + 625 + 390625 + (c - 2) * 390625 + (((((((a * 5 + b) * 5 + e) * 5 + f) * 5 + p) * 5 + q) * 5 + r) * 5 + s_), C)   # s51 51.7
    HS = 2000000 if XO else 500000   # s51: fold stride above the xo classes
""")
s = sub(s, "        assert int(C.max()) < 500000\n", "        assert int(C.max()) < HS\n")
s = sub(s, "        C = np.where(r == 0, C + 500000 * T[b, c, e, f, q, s_], C)\n", "        C = np.where(r == 0, C + HS * T[b, c, e, f, q, s_], C)\n")
s = sub(s, "        C = np.where(r >= 2, C + 500000 * T7[b, c, e, f, q, r, s_], C)\n", "        C = np.where(r >= 2, C + HS * T7[b, c, e, f, q, r, s_], C)\n")
s = sub(s, "'clsR2_%d%s%s%s%s%s.bin' % (int(xon), 'z' if ZH else '', 'y' if FY else '', 'f' if F16 else '', 'h' if H5 else '', 'D' if DD else '')",
           "'clsR2_%d%s%s%s%s%s%s.bin' % (int(xon), 'z' if ZH else '', 'y' if FY else '', 'f' if F16 else '', 'h' if H5 else '', 'D' if DD else '', 'o' if XO else '')", n=2)

# ---------------------------------------------------------------- (3) receiver coefficients
s = sub(s, "    cy, cx = recv_coef(d, lk, sv, xon); cf = collections.Counter()\n", "    cy, cx = recv_coef(d, lk, sv, xon and not XO); cf = collections.Counter()   # s51: no old x under xo\n")
s = sub(s, "        for _, k in fb_payee_keys(d, w, s, min(d, 9)) if min(d, 9) >= 7 else []: cf[('fb', k)] += 1\n    return cf\n",
           "        for _, k in fb_payee_keys(d, w, s, min(d, 9)) if min(d, 9) >= 7 else []: cf[('fb', k)] += 1\n    if XO: cf.update(xo_recv_terms(d, w, s))   # s51\n    return cf\n")

# ---------------------------------------------------------------- (4) solveR2
s = sub(s, "            h.addVar(-inf if key[0] == 't' else 0.0, XCAP if key[0] == 'x' else DCAP",
           "            h.addVar(-inf if key[0] == 't' else -XCAP if key[0] == 'XQ' else 0.0, XCAP if key[0] in ('x', 'xo', 'XQ') else DCAP")
s = sub(s, "            if key[0] == 'x' and XPEN[0]: h.changeColCost(cols[key], XPEN[0])\n",
           "            if key[0] in ('x', 'xo') and XPEN[0]: h.changeColCost(cols[key], XPEN[0])   # s51: xo carries the x penalty\n")
s = sub(s, "    info = []; have = set(); msig = set(); conset = set(); qsig = set(); vsig = set(); lsig = set()\n",
           "    info = []; have = set(); msig = set(); conset = set(); qsig = set(); vsig = set(); lsig = set(); xqsig = set()\n")
s = sub(s, "            if k[0] == 'Q' and k[1] not in qsig:\n",
"""            if k[0] == 'XQ' and k[1] not in xqsig:   # s51: all mrowX rows of q at first use
                xqsig.add(k[1])
                for cfx, ee in xo_mrows(k[1]): addrow(cfx, -inf, 0.0, ('mrowX', [k[1][0], k[1][1], list(k[1][2]), list(k[1][3])], ee))
            if k[0] == 'Q' and k[1] not in qsig:
""")
s = sub(s, "        xd = {k[1]: xv[i] for k, i in cols.items() if k[0] == 'x' and xv[i] > 1e-12}\n        mcache = {}\n",
           "        xd = {k[1]: xv[i] for k, i in cols.items() if k[0] == 'x' and xv[i] > 1e-12}\n        XOV.clear(); XOV.update({k[1]: xv[i] for k, i in cols.items() if k[0] == 'xo' and xv[i] > 0})   # s51\n        mcache = {}\n")
s = sub(s, "                if k[0] in ('x', 'D', 'lq', 'z6', 'fb') or (ZR and k[0] in ('z', 'zr', 'rr')): h.changeColCost(i, 0.0)\n",
           "                if k[0] in ('x', 'xo', 'D', 'lq', 'z6', 'fb') or (ZR and k[0] in ('z', 'zr', 'rr')): h.changeColCost(i, 0.0)\n")
s = sub(s, "         'x': {str(k[1]): float(xv[i]) for k, i in cols.items() if k[0] == 'x' and xv[i] > 0}}\n",
           "         'x': {str(k[1]): float(xv[i]) for k, i in cols.items() if k[0] == 'x' and xv[i] > 0},\n         'xo': {str(k[1]): float(xv[i]) for k, i in cols.items() if k[0] == 'xo' and xv[i] > 0}, 'xoflag': XO}   # s51\n")
s = sub(s, "    log('  (+ %d cons2 / mrowR2 rows)' % sum(1 for c in cert if c['row'][0] in ('cons2', 'mrowR2')))\n",
           "    log('  (+ %d cons2 / mrowR2 rows)' % sum(1 for c in cert if c['row'][0] in ('cons2', 'mrowR2')))\n"
           "    if XO: log('  xo: %d xo > 0 (total %.9f, max %.9f); %d XQ columns, %d mrowX rows in the LP, %d in the cert' % (sum(1 for k, i in cols.items() if k[0] == 'xo' and xv[i] > 1e-12), sum(float(xv[i]) for k, i in cols.items() if k[0] == 'xo'), max([float(xv[i]) for k, i in cols.items() if k[0] == 'xo'] or [0.0]), len(xqsig), sum(1 for r_ in info if r_[0] == 'mrowX'), sum(1 for c in cert if c['row'][0] == 'mrowX')))\n")

# ---------------------------------------------------------------- (5) lowerR2
s = sub(s, "        elif row[0] == 'mrowV':\n",
"""        elif row[0] == 'mrowX':   # s51 51.6
            qq = row[1]; ee = row[2]
            try:
                good = (XO and len(qq) == 4 and qq[0] in (7, 8, 9) and qq[1] in (7, 8, 9) and all(len(z) == 5 and all(v in LET for v in z[:4]) and isinstance(z[4], int) and 1 <= z[4] <= 31 for z in qq[2:])
                        and tuple(qq[2]) <= tuple(qq[3]) and len(ee) == 2 and ee[0] in LET and ee[1] in LET and (qq[2][4] >> LI[ee[0]]) & 1 and (qq[3][4] >> LI[ee[1]]) & 1)
            except TypeError: good = False
            if not good: log('  BAD MROWX', row); ok = False; continue
            if w > 0: log('  WRONG SIGN', row); ok = False; continue
            q = (qq[0], qq[1], tuple(qq[2]), tuple(qq[3]))
            cf = [c_ for c_, e_ in xo_mrows(q) if e_ == list(ee)][0]
        elif row[0] == 'mrowV':
""")
s = sub(s, "        if k[0] == 'x': return XCAP\n        if k[0] == 'D': return Fraction(OPT.get('dcap', '3'))",
           "        if k[0] in ('x', 'xo'): return XCAP   # s51: xo priced at xcap as x\n        if k[0] == 'D': return Fraction(OPT.get('dcap', '3'))")
s = sub(s, "        for k, v in tot.items():\n            rc = -v / tco\n            if rc < 0:\n",
           "        for k, v in tot.items():\n            rc = -v / tco\n            if k[0] == 'XQ':   # s51: XQ in [-xcap, xcap], priced at its box\n                D -= XCAP * abs(rc); continue\n            if rc < 0:\n")

# ---------------------------------------------------------------- (6) upperR2
s = sub(s, "    xd = {int(k): v for k, v in Sj.get('x', {}).items()}\n    if any(v < 0 for v in list(GV.values())",
"""    xd = {int(k): v for k, v in Sj.get('x', {}).items()}
    XOV.clear(); XOV.update({int(k): v for k, v in Sj.get('xo', {}).items()})   # s51 51.5
    if XOV and not XO: log('SOLUTION HAS xo BUT xo FLAG OFF'); return
    if XO and xd: log('SOLUTION HAS OLD x BUT xo FLAG ON'); return
    if XO and not Sj.get('xoflag'): log('SOLUTION WAS NOT SOLVED WITH xo'); return
    if any(v < 0 or v > float(OPT.get('xcap', '3')) + 1e-9 for v in XOV.values()): log('xo VALUE OUTSIDE [0, xcap]'); return
    if XO: log('xo: %d xo > 0 (total %.9f, max %.9f); XQ taken as max over the candidates%s' % (len(XOV), sum(XOV.values()), max(XOV.values() or [0.0]), ' (BROKEN %s CONTROL)' % XOB if XOB else ''))
    if any(v < 0 for v in list(GV.values())""")

# ---------------------------------------------------------------- (7) binderR2 / rowR2 read XQ
s = sub(s, "    for k, v in Sj.get('x', {}).items(): VAL[('x', int(k))] = v\n    HV2 = {tuple(k): v for k, v in Sj['h']}\n",
           "    for k, v in Sj.get('x', {}).items(): VAL[('x', int(k))] = v\n    XOV.clear(); XOV.update({int(k): v for k, v in Sj.get('xo', {}).items()})   # s51\n    HV2 = {tuple(k): v for k, v in Sj['h']}\n")
s = sub(s, "        if k[0] == 'M': return max([HV2.get(tuple(h), 0.0) for h in sig2_keys(k[1])] or [0.0])\n        return VAL.get(k, 0.0)\n",
           "        if k[0] == 'M': return max([HV2.get(tuple(h), 0.0) for h in sig2_keys(k[1])] or [0.0])\n        if k[0] == 'XQ': return xo_eff(k[1])   # s51\n        return VAL.get(k, 0.0)\n")
s = sub(s, "    GRP = {'y': 'base y', 'x': 'base x',", "    GRP = {'XQ': 'xo XQ', 'y': 'base y', 'x': 'base x',")
s = sub(s, "    XV = {int(k): v for k, v in Sj.get('x', {}).items()}; QV.clear();", "    XOV.clear(); XOV.update({int(k): v for k, v in Sj.get('xo', {}).items()})   # s51\n    XV = {int(k): v for k, v in Sj.get('x', {}).items()}; QV.clear();")
s = sub(s, "        v = YV.get(rname(k[1]), 0.0) if k[0] == 'y' else dict(", "        v = xo_eff(k[1]) if k[0] == 'XQ' else YV.get(rname(k[1]), 0.0) if k[0] == 'y' else dict(")
open(p2, 'w').write(s)

pc = os.path.join(E, 'pcheck.py'); t = open(pc).read()
t = sub(t, "{'pcellcheck': cmd_pcellcheck,", "{'xoselftest': cmd_xoselftest, 'pcellcheck': cmd_pcellcheck,")
open(pc, 'w').write(t)
print('port_s51: done')
