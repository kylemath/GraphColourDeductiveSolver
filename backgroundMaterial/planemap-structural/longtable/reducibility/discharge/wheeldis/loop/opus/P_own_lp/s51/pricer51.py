# s50 refinement pricer (no solve of the main LP).  Prices radius-2 refinements of the generic families y, x, h2, g2
# against an existing dual certificate, by reduced costs of the refined columns.
#   python3 pricer50.py REG CERT TAG [REFS]       REFS = comma list of refinement names (default: all, see REFS below)
# Method (s50/REFINE_PRICE.md): every cert row is re-derived from its label with the engine's own functions; for the refined
# family its occurrences are re-derived with independent key code, and each occurrence's extra letters are either read
# from the label (pinned) or left as unseen variables with their engine domain.  A row whose letters are not pinned is
# replaced, in the refined LP, by one row per compatible completion; its old weight may be spread (convexly) over them.
# Also used: relabel freedom (other labels giving the identical old row: sender bits, cons2 apex words, single-slot
# receiver relabels).  An LP (HiGHS) picks the spread that minimises sum max(0, -rc) over the refined columns; the
# split is then rationalised, renormalised and re-evaluated exactly (Fractions).  Every completion's refined vector is
# coarsened back and must equal the engine's row coefficients for that family (assert); level-0 refinements must
# reproduce lowerR2's reduced costs exactly (control).
# Optional (s51, default off): env SPREAD51=<path.json> writes the chosen exact split of the refinement SPREAD51_REF
# (default x_outMW; relabel freedom on) per cert row / relabel mode / big position / completion, with the implied mrowX
# dual per candidate (RELAY_SPEC_s51 §51.3a).  Nothing else changes: same LP, same log lines, same price_TAG.json.
import os, sys, json, re, collections, itertools, time
from fractions import Fraction
import numpy as np
REG, CERT, TAG = sys.argv[1], sys.argv[2], sys.argv[3]
ONLY = sys.argv[4].split(',') if len(sys.argv) > 4 else None
B = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
SC = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad'
E = B + '/s50/eng'; Q = B + '/s33z/reg_' + REG; H = B + '/s39o'
M = SC + '/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
ARGS = ['xon', 'apexcls', 'filt16', 'killtab=' + Q + '/f/kill/kill6', 'hat5', 'consall', 'l3q',
        'l3qtab=' + Q + '/tab_1.json,' + Q + '/tab_-1.json', 'lqcap=3', 'rpatN=' + H + '/rpatN3.txt',
        'cert=' + CERT, 'xcap=3', 'root=' + M, 'args=' + Q + '/args_%s.txt' % REG, 'rpat=' + B + '/rpatD.txt',
        'exname=' + B + '/s40f/exname_rm128.txt', 'threads=1', 'work=' + SC + '/P/wr51_price_' + TAG]
sys.argv = [E + '/pcheck.py', 'lowerR2'] + ARGS
T0 = time.time()
src = open(E + '/pcheck.py').read(); last = src.rstrip().rsplit('\n', 1)
G = {'__file__': E + '/pcheck.py', '__name__': 'pcheck_exec'}; exec(compile(last[0], E + '/pcheck.py', 'exec'), G)
for f_, v_ in (('H5', True), ('ZH', False), ('F5', False), ('HX', False), ('FY', False), ('FB', False), ('V6', False),
               ('Q7', False), ('L6R', False), ('AC', True), ('AP', True), ('F16', True), ('L3Q', True), ('HRR', False), ('DD', False)):
    assert bool(G[f_]) == v_, (f_, G[f_])
p2 = open(E + '/prelay2.py').read()
fsrc = re.search(r'\ndef cmd_lowerR2\(\):\n(.*?)\n(?=\S)', p2, re.S).group(0)
OLD = "    if neg: log('  negative reduced costs:', len(neg), sorted(neg, key=lambda kv: kv[1])[:5])"
assert fsrc.count(OLD) == 1
fsrc = fsrc.replace(OLD, "    CAP_['tot'] = dict(tot); CAP_['tco'] = tco; CAP_['D'] = D; CAP_['Dp'] = Dp; CAP_['neg'] = list(neg)\n" + OLD)
G['CAP_'] = {}; exec(fsrc, G); G['cmd_lowerR2']()
CAP = G['CAP_']; TOT = CAP['tot']; TCO = CAP['tco']; DP = CAP['Dp']; DRAW = CAP['D'] / TCO
LET = G['LET']; CLS2 = G['CLS2']; isR6 = G['isR6']; root = G['root']; c2 = G['c2']; ap = G['ap']
recv_coef_R2 = G['recv_coef_R2']; cons2_coef = G['cons2_coef']; g2_of = G['g2_of']; h2_of = G['h2_of']
sig2_of = G['sig2_of']; sig2_keys = G['sig2_keys']; amask = G['amask']; admissible = G['admissible']
hat_sender_terms = G['hat_sender_terms']; tau = G['tau']; side = G['side']; pallow = G['pallow']
log = G['log']; XCAP = Fraction(3)
print('lowerR2 captured: tco %s, D %s = %.9f, %d columns, %d uncapped negative (%.0fs)' % (TCO, DP, float(DP), len(TOT), len(CAP['neg']), time.time() - T0), flush=True)
def nz(cf): return {k: v for k, v in cf.items() if v}
def fam(cf, f): return {k: v for k, v in cf.items() if v and k[0] == f}
def capof(k):
    if k[0] == 'x': return XCAP
    if k[0] == 'lq': return Fraction(3)
    return None
# ---------------------------------------------------------------- cert rows (rebuilt as lowerR2 does)
C = json.load(open(CERT))
SR = {(wd, tuple(map(str, b))): cf for wd, cf, b in G['R2_sender_rows']()}
ROWS = []
for ci, c in enumerate(C):
    w = Fraction(c['w']) if isinstance(c['w'], str) else Fraction(c['w']).limit_denominator(10 ** 7)
    r = c['row']; k = r[0]
    if k == 'senderR2': cf = SR[(r[1], tuple(map(str, r[2])))]; tc = 1; dc = 1
    elif k == 'cons2': cf = cons2_coef(tuple(r[1]), tuple(r[2])); tc = 0; dc = 0
    elif k == 'mrowR2': cf = {('h', tuple(r[2])): 1, ('M', tuple(r[1])): -1}; tc = 0; dc = 0
    elif k == 'mrowL': cf = {('lq', tuple(r[2])): 1, ('lQ', tuple(r[1])): -1}; tc = 0; dc = 0
    elif k == 'receiverR2': cf = recv_coef_R2(int(r[1]), r[2], r[3], True); tc = -1; dc = int(r[1]) - 6
    else: raise SystemExit('unknown row ' + str(r))
    ROWS.append(dict(ci=ci, kind=k, w=w, label=r, cf=nz(cf), tc=tc, dc=dc))
def lab(r):
    L = r['label']
    if r['kind'] == 'senderR2': return 'S %s %s' % (L[1], ''.join(map(str, L[2])))
    if r['kind'] == 'cons2': return 'C %s/%s' % (''.join(map(str, L[1])), ''.join(map(str, L[2])))
    if r['kind'] == 'receiverR2': return 'R %s %s/%s' % (L[1], L[2], L[3])
    return '%s %s/%s' % ('mR2' if r['kind'] == 'mrowR2' else 'mL', ''.join(map(str, L[1])), ''.join(map(str, L[2])))
# control 0: my ledger from the rebuilt rows = lowerR2's tot, t coefficient and D
tot0 = collections.defaultdict(Fraction); tco0 = Fraction(0); d0 = Fraction(0)
for r in ROWS:
    for k, v in r['cf'].items(): tot0[k] += r['w'] * v
    tco0 += r['w'] * r['tc']; d0 += r['w'] * r['dc']
assert tco0 == TCO and d0 == CAP['D']
assert {k: v for k, v in tot0.items() if v} == {k: v for k, v in TOT.items() if v}
RC0 = {k: -v / TCO for k, v in TOT.items()}
print('control 0: rebuilt ledger = lowerR2 ledger on all %d columns (exact)' % len(TOT), flush=True)
# ---------------------------------------------------------------- relabel freedom (other labels with the identical old row)
def sender_assign(wstr):
    """every admissible (H, Fn) of the sender word with its coefficient dict (R2_sender_rows' loop, no dedupe; hat5 flags)"""
    w = tuple(int(ch) for ch in wstr); n = 5; sixes = [k for k in range(n) if w[k] == 6]
    allow = {k: {(a_, q, b_) for a_ in LET for q in LET for b_ in LET if not isR6((5, w[(k + 1) % n], a_, q, b_, w[(k - 1) % n]))} for k in sixes}
    base = collections.Counter()
    for j in range(n):
        if w[j] >= 7: base[('y', root(list(w), j))] += 1
    for hb in itertools.product((0, 1), repeat=5):
        Hh = dict(zip(range(5), hb))
        for fb in itertools.product((0, 1), repeat=len(sixes)):
            Fn = dict(zip(sixes, fb))
            if not all(any((a_, q, b_) in allow[k] for a_ in CLS2[Hh[k]] for q in CLS2[Fn[k]] for b_ in CLS2[Hh[(k - 1) % n]]) for k in sixes): continue
            cf = collections.Counter(base)
            for k in range(n):
                if Hh[k]:
                    for k2, v2 in hat_sender_terms(w, Hh, Fn, k).items(): cf[k2] += v2
            for k in sixes:
                L5 = lambda c: 7 if c else 5
                cf[('g', g2_of(w[(k + 1) % n], L5(Hh[k]), L5(Fn[k]), L5(Hh[(k - 1) % n]), w[(k - 1) % n], w[(k + 2) % n], w[(k - 2) % n]))] += 1
            yield w, Hh, Fn, nz(cf), list(hb) + ['|'] + list(fb)
REL = {}
for r in ROWS:
    if r['kind'] == 'senderR2':
        eq = [(w, Hh, Fn, b) for w, Hh, Fn, cf, b in sender_assign(r['label'][1]) if cf == r['cf']]
        assert any(list(map(str, b)) == list(map(str, r['label'][2])) for _, _, _, b in eq)
        REL[r['ci']] = [(w, Hh, Fn) for w, Hh, Fn, b in eq]
    elif r['kind'] == 'cons2':
        L = tuple(r['label'][1])
        REL[r['ci']] = [s for s in itertools.product(LET, repeat=6) if nz(cons2_coef(L, s)) == r['cf']]
        assert tuple(r['label'][2]) in REL[r['ci']]
    elif r['kind'] == 'receiverR2':
        d, lk, sv = int(r['label'][1]), r['label'][2], r['label'][3]
        slots = [('w', i) for i in range(d)] + [('s', i) for i in range(d)]
        def put(lk_, sv_, sl, v):
            if sl[0] == 'w': return lk_[:sl[1]] + str(v) + lk_[sl[1] + 1:], sv_
            return lk_, sv_[:sl[1]] + str(v) + sv_[sl[1] + 1:]
        alt = {}
        for sl in slots:
            cur = int((lk if sl[0] == 'w' else sv)[sl[1]]); alt[sl] = [cur]
            for v in LET:
                if v == cur: continue
                l2, s2 = put(lk, sv, sl, v)
                if nz(recv_coef_R2(d, l2, s2, True)) == r['cf'] and admissible(d, l2, s2) is None: alt[sl].append(v)
        var = [sl for sl in slots if len(alt[sl]) > 1]; arr = []
        for combo in itertools.product(*[alt[sl] for sl in var]):
            l2, s2 = lk, sv
            for sl, v in zip(var, combo): l2, s2 = put(l2, s2, sl, v)
            if combo and (nz(recv_coef_R2(d, l2, s2, True)) != r['cf'] or admissible(d, l2, s2) is not None): continue
            arr.append((d, [int(ch) for ch in l2], [int(ch) for ch in s2]))
        REL[r['ci']] = arr
print('relabel freedom: senders %s; cons2 %s; receivers %s (%.0fs)' % (
    sorted(collections.Counter(len(REL[r['ci']]) for r in ROWS if r['kind'] == 'senderR2').items()),
    sorted(collections.Counter(len(REL[r['ci']]) for r in ROWS if r['kind'] == 'cons2').items()),
    sorted(collections.Counter(len(REL[r['ci']]) for r in ROWS if r['kind'] == 'receiverR2').items()), time.time() - T0), flush=True)
# ---------------------------------------------------------------- refined keys (independent code; coarsened back for the check)
def ykey(n, hats):
    """n = (U, n1..n4) the five's link read from the big; hats = () | (hr, hl) [hat U-n1, hat n4-U] | (h0..h4), h_k = hat n_k-n_{k+1}"""
    n = tuple(n); a = n + tuple(hats); rn = (n[0], n[4], n[3], n[2], n[1])
    if len(hats) == 2: b = rn + (hats[1], hats[0])
    else: b = rn + tuple(reversed(hats))
    return min(a, b)
def y_coarse(K): return ('y', tuple(K[:5]))
def xkey(fl, tl, S1, S2): return (fl, tl, min(S1, S2), max(S1, S2))
def x_coarse(K): return ('x', tau(K[0], K[1], side(*K[2][:3]), side(*K[3][:3])))
def hkey(m, ext):
    """m = the 6's link from the big; ext = (ar, al) [ap classes or exact] (+ (fr, fl): apexes beyond (m2,m3), (m3,m4))"""
    m = tuple(m); a = m + tuple(ext); rm = (m[0], m[5], m[4], m[3], m[2], m[1])
    b = rm + (ext[1], ext[0]) + ((ext[3], ext[2]) if len(ext) == 4 else ())
    return min(a, b)
def h_coarse(K): return ('h', h2_of(K[:6], K[6], K[7]))
def gkey(n, ar, al):
    """n = (n1..n5) exact or with classes at 1..3; ar, al = ap classes of the apexes"""
    a = tuple(n) + (ar, al); b = tuple(reversed(n)) + (al, ar); return min(a, b)
def g_coarse(K): return ('g', g2_of(*K))
# ---------------------------------------------------------------- occurrences per row and refinement
# a row -> list of modes; mode = (const Counter, [component: list of distinct Counters]); weights spread convexly
def cls_of(c): return CLS2[c2(c)]
class CL(list):
    """a component's distinct vectors (a plain list) + .vars and .asg[j] = the letter assignments giving vector j"""
    pass
def product_vectors(occs, dom):
    """occs: list of (coef, fn(assign) -> refined key, var names); dom: var -> letters.  Returns (const, [components])"""
    const = collections.Counter(); par = {}
    def fd(x):
        while par[x] != x: x = par[x]
        return x
    for v in dom: par[v] = v
    for _, _, vs in occs:
        for v in vs[1:]: par[fd(v)] = fd(vs[0])
    groups = collections.defaultdict(list)
    for o in occs:
        if not o[2]: const[o[1]({})] += o[0]
        else: groups[fd(o[2][0])].append(o)
    comps = []
    for gk, os_ in groups.items():
        vs = sorted({v for o in os_ for v in o[2]})
        size = 1
        for v in vs: size *= len(dom[v])
        assert size <= 4 * 10 ** 6, ('component too large', vs, size)
        seen = {}; out = CL(); out.vars = vs; out.asg = []
        for combo in itertools.product(*[dom[v] for v in vs]):
            asg = dict(zip(vs, combo)); cf = collections.Counter()
            for cfv, fn, _ in os_: cf[fn(asg)] += cfv
            cf = frozenset((k, v) for k, v in cf.items() if v)
            if cf not in seen: seen[cf] = len(out); out.append(dict(cf)); out.asg.append([])
            out.asg[seen[cf]].append(combo)
        comps.append(out)
    return dict(const), comps
def recv_occ(ref, d, w, s):
    """refined-family occurrences in a receiver row (d, link w, apexes s): list of (coef, fn, vars), domains"""
    U = min(d, 9); W_ = lambda k: w[k % d]; S_ = lambda k: s[k % d]; occs = []; dom = {}
    def pdom(m):   # allowed privates of the link 6 at m (engine: non-R6 wheel and the filt16 mask)
        sg = sig2_of(U, W_(m + 1), S_(m), S_(m - 1), W_(m - 1), W_(m + 2), W_(m - 2))
        am = amask(U, W_(m - 2), W_(m - 1), W_(m + 1), W_(m + 2), S_(m - 2), S_(m - 1), S_(m), S_(m + 1))
        return [p for p in pallow(sg + (am,)) if not isR6((U, W_(m + 1), S_(m), p, S_(m - 1), W_(m - 1)))]
    def hatvar(m, sd):
        """the unseen vertex next to link vertex w_m on the side of s_{m-1} (sd = -1) or s_m (sd = +1) (not adjacent to u):
        a 6's private (shared by both sides), or a big's own unseen neighbour; None if w_m is a five (then visible)"""
        m %= d
        if w[m] == 5: return None
        if w[m] == 6:
            nm = ('p', m); dom[nm] = pdom(m); return nm
        nm = ('X', m, sd); dom[nm] = list(LET); return nm
    if ref[0] == 'y':
        for i in range(d):
            if w[i] != 5: continue
            n = (U, W_(i + 1), S_(i), S_(i - 1), W_(i - 1))
            if ref == 'y0': occs.append((1, (lambda n: lambda a: ykey(n, ()))(n), [])); continue
            if ref == 'y_ap': occs.append((1, (lambda n, hr, hl: lambda a: ykey(n, (hr, hl)))(n, W_(i + 2), W_(i - 2)), [])); continue
            # y_hats: h0 = w_{i+2}; h1 = s_{i+1} if w_{i+1} = 5 else unseen; h2 = t_i unseen; h3 = s_{i-2} if w_{i-1} = 5; h4 = w_{i-2}
            v1 = hatvar(i + 1, -1); v3 = hatvar(i - 1, +1); vt = ('t', i); dom[vt] = list(LET)
            vs = [v for v in (v1, vt, v3) if v]
            def fn(a, n=n, i=i, v1=v1, v3=v3, vt=vt):
                return ykey(n, (W_(i + 2), S_(i + 1) if v1 is None else a[v1], a[vt], S_(i - 2) if v3 is None else a[v3], W_(i - 2)))
            occs.append((1, fn, vs))
    elif ref[0] == 'x':
        for i in range(d):
            if w[i] < 7: continue
            # + side c = w_{i+1}: a/b as the engine; outer letters: next to w_{i+2} is s_{i+1} (seen); next to s_i is
            # s_{i+1} if c = 5, else the unseen vertex hatvar(i+1, -1).   - side mirrored with s_{i-2}, hatvar(i-1, +1).
            vp = None if ref == 'x0' else hatvar(i + 1, -1); vm = None if ref == 'x0' else hatvar(i - 1, +1)
            if ref in ('x_outM', 'x_outMW'):   # s51: M-style, one unseen pair per x term (not shared with other terms)
                def own(v, m, side_):
                    if v is None: return None
                    nm = ('T', i) + v
                    if ref == 'x_outMW' and v[0] == 'p':   # window-local domain: amask union over the 2 slots outside the window at i
                        mm = v[1]; dd = set()
                        for o1, o2 in itertools.product(LET, repeat=2):
                            if side_ > 0: am = amask(U, W_(mm - 2), W_(mm - 1), W_(mm + 1), o1, S_(mm - 2), S_(mm - 1), S_(mm), o2)
                            else: am = amask(U, o1, W_(mm - 1), W_(mm + 1), W_(mm + 2), o2, S_(mm - 1), S_(mm), S_(mm + 1))
                            dd |= {p_ for k_, p_ in enumerate(LET) if (am >> k_) & 1}
                        dom[nm] = [p_ for p_ in LET if p_ in dd and not isR6((U, W_(mm + 1), S_(mm), p_, S_(mm - 1), W_(mm - 1)))]
                    else: dom[nm] = list(dom[v])
                    return nm
                vp = own(vp, i + 1, +1); vm = own(vm, i - 1, -1)
            vs = [v for v in (vp, vm) if v]
            def ex(a, v, sval): return sval if v is None else a[v]
            def fin(a, i=i, vp=vp, vm=vm):
                if ref == 'x0': return xkey(W_(i), U, (W_(i - 1), S_(i - 1), W_(i - 2)), (W_(i + 1), S_(i), W_(i + 2)))
                Sp = (W_(i + 1), S_(i), W_(i + 2), ex(a, vp, S_(i + 1)), S_(i + 1))
                Sm = (W_(i - 1), S_(i - 1), W_(i - 2), ex(a, vm, S_(i - 2)), S_(i - 2))
                return xkey(W_(i), U, Sm, Sp)
            def fout(a, i=i, vp=vp, vm=vm):
                if ref == 'x0': return xkey(U, W_(i), (W_(i - 1), W_(i - 2), S_(i - 1)), (W_(i + 1), W_(i + 2), S_(i)))
                Sp = (W_(i + 1), W_(i + 2), S_(i), S_(i + 1), ex(a, vp, S_(i + 1)))
                Sm = (W_(i - 1), W_(i - 2), S_(i - 1), S_(i - 2), ex(a, vm, S_(i - 2)))
                return xkey(U, W_(i), Sm, Sp)
            occs.append((1, fin, vs)); occs.append((-1, fout, vs))
    return occs, dom
def row_modes(ref, r, relabel=True):
    """modes for the refined family of ref in row r, or None if the row has no such column"""
    f = ref[0]; k = r['kind']; L_ = r['label']
    if not fam(r['cf'], f): return None
    if k == 'receiverR2':
        assert f in 'yx', (ref, lab(r))
        modes = []
        for d, w, s in (REL[r['ci']] if relabel else [(int(L_[1]), [int(ch) for ch in L_[2]], [int(ch) for ch in L_[3]])]):
            occs, dom = recv_occ(ref, d, w, s); modes.append(product_vectors(occs, dom))
        return modes
    if k == 'senderR2':
        assert f in 'yg', (ref, lab(r))
        out = []; seen = set()
        cand = REL[r['ci']] if relabel else [x for x in REL[r['ci']] if [x[1][m] for m in range(5)] + ['|'] + [x[2][kk] for kk in sorted(x[2])] == list(L_[2])]
        assert cand
        for w, Hh, Fn in cand:
            sixes = [kk for kk in range(5) if w[kk] == 6]
            if f == 'y':
                hsets = [cls_of(7 if Hh[m] else 5) if ref != 'y0' else (5 if not Hh[m] else 7,) for m in range(5)]
                for hx in itertools.product(*hsets):
                    if ref != 'y0' and not all(any(not isR6((5, w[(kk + 1) % 5], hx[kk], q, hx[(kk - 1) % 5], w[(kk - 1) % 5])) for q in CLS2[Fn[kk]]) for kk in sixes): continue
                    cf = collections.Counter()
                    for j in range(5):
                        if w[j] >= 7:
                            n = tuple(w[(j + t) % 5] for t in range(5))
                            hh = () if ref == 'y0' else (hx[j], hx[(j - 1) % 5]) if ref == 'y_ap' else tuple(hx[(j + t) % 5] for t in range(5))
                            cf[ykey(n, hh)] += 1
                    fz = frozenset(cf.items())
                    if fz not in seen: seen.add(fz); out.append(dict(cf))
            else:
                hsets = [cls_of(7 if Hh[m] else 5) for m in range(5)]; fsets = [cls_of(7 if Fn[kk] else 5) for kk in sixes]
                if ref == 'g0': hsets = [(7 if Hh[m] else 5,) for m in range(5)]; fsets = [(7 if Fn[kk] else 5,) for kk in sixes]
                for hx in itertools.product(*hsets):
                    for fx in itertools.product(*fsets):
                        F_ = dict(zip(sixes, fx))
                        if ref != 'g0' and any(isR6((5, w[(kk + 1) % 5], hx[kk], F_[kk], hx[(kk - 1) % 5], w[(kk - 1) % 5])) for kk in sixes): continue
                        cf = collections.Counter()
                        for kk in sixes:
                            n = (w[(kk + 1) % 5], hx[kk], F_[kk], hx[(kk - 1) % 5], w[(kk - 1) % 5])
                            cf[gkey(n, ap(w[(kk + 2) % 5]), ap(w[(kk - 2) % 5]))] += 1
                        fz = frozenset(cf.items())
                        if fz not in seen: seen.add(fz); out.append(dict(cf))
        return [({}, [out])]
    if k == 'cons2':
        assert f in 'hg', (ref, lab(r))
        Lw = tuple(L_[1]); out = []; seen = set()
        for s in (REL[r['ci']] if relabel else [tuple(L_[2])]):
            cf = collections.Counter()
            if f == 'g':
                for i in range(6):
                    if Lw[i] == 5:
                        n = tuple(Lw[(i + t) % 6] for t in range(1, 6))
                        if ref == 'g0': n = (n[0], ap(n[1]), ap(n[2]), ap(n[3]), n[4])   # class witnesses 5/7
                        cf[gkey(n, ap(s[i]), ap(s[(i - 1) % 6]))] += 1
            else:
                for j in range(6):
                    if Lw[j] >= 7:
                        m = tuple(Lw[(j + t) % 6] for t in range(6))
                        ext = (ap(s[j]), ap(s[(j - 1) % 6])) if ref == 'h0' else (s[j], s[(j - 1) % 6])
                        if ref == 'h_apf': ext = ext + (s[(j + 2) % 6], s[(j + 3) % 6])
                        cf[hkey(m, ext)] -= 1
            fz = frozenset((kk, v) for kk, v in cf.items() if v)
            if fz not in seen: seen.add(fz); out.append(dict(fz))
        return [({}, [out])]
    if k == 'mrowR2':
        assert f == 'h'
        K = tuple(L_[2]); m = K[:6]; out = []
        if ref == 'h0': return [({hkey(m, (K[6], K[7])): 1}, [])]
        for ar in cls_of(K[6]):
            for al in cls_of(K[7]):
                for fr in (LET if ref == 'h_apf' else (None,)):
                    for fl_ in (LET if ref == 'h_apf' else (None,)):
                        ext = (ar, al) + ((fr, fl_) if ref == 'h_apf' else ())
                        out.append({hkey(m, ext): 1})
        return [({}, [out])]
    raise AssertionError((ref, k))
COARSE = {'y': y_coarse, 'x': x_coarse, 'h': h_coarse, 'g': g_coarse}
REFS = [('y0', 'y, level 0 (control)'), ('x0', 'x, level 0 (control)'), ('h0', 'h2, level 0 (control)'), ('g0', 'g2, level 0 (control)'),
        ('y_ap', 'y + both apex letters exact (hats U-n1, n4-U)'), ('y_hats', "y + the five's 5 hats exact"),
        ('x_out', 'x sides + outer (second-ring) letters'), ('x_outM', 'x_out, M-style: unseen letters per x term'), ('x_outMW', 'x_outM with window-local 6-private domain'), ('h_ap', 'h2 apexes exact'),
        ('h_apf', "h2 apexes exact + the two apexes at the 6's opposite private"), ('g_hf', 'g2 hats and fan exact')]
REFN = dict(REFS)
# ---------------------------------------------------------------- the spread LP and its exact evaluation
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
def price(ref, relabel=True, cfree=False, dump=None):
    f = ref[0]
    RM = []
    for r in ROWS:
        md = row_modes(ref, r, relabel)
        if md is None: continue
        # coarsening check: every completion of every mode coarsens to the engine's coefficients for the family
        oldf = fam(r['cf'], f)
        for const, comps in md:
            bases = [const]
            for comp in comps:
                for v in comp:
                    tot_ = collections.Counter()
                    for kk, cv in const.items(): tot_[COARSE[f](kk)] += cv
                    for c2_ in comps:
                        for kk, cv in (v if c2_ is comp else c2_[0]).items(): tot_[COARSE[f](kk)] += cv
                    assert nz(tot_) == oldf, (ref, lab(r), dict(tot_), oldf)
            if not comps:
                tot_ = collections.Counter()
                for kk, cv in const.items(): tot_[COARSE[f](kk)] += cv
                assert nz(tot_) == oldf, (ref, lab(r), dict(tot_), oldf)
        RM.append((r, md))
        if os.environ.get('DEBUG50') == ref:
            for const, comps in md: print('  DEBUG', lab(r), 'w', r['w'], 'const', const, 'comps', [c if len(c) <= 6 else (len(c), c[:6]) for c in comps])
    # LP variables: alpha per (row, mode) when > 1 mode; mu per component vector; z per refined key
    keys = {}; cst = collections.defaultdict(float)
    def kid(kk):
        if kk not in keys: keys[kk] = len(keys)
        return keys[kk]
    var = []; Arow = []; Acol = []; Aval = []; eqr = []; eqc = []; eqv = []; beq = []; bnd = []
    struct = []
    pinned = 0
    for r, md in RM:
        wf = float(r['w']); one = len(md) == 1
        if one and all(len(c) == 1 for c in md[0][1]): pinned += 1
        ri = len(beq)
        if not one: beq.append(1.0)
        st = []
        for const, comps in md:
            if one:
                for kk, cv in const.items(): cst[kid(kk)] += wf * cv
                ai = None
            else:
                ai = len(var); var.append(('a', r['ci'])); bnd.append((0, None))
                eqr.append(ri); eqc.append(ai); eqv.append(1.0)
                for kk, cv in const.items(): Arow.append(kid(kk)); Acol.append(ai); Aval.append(wf * cv)
            cs = []
            for comp in comps:
                ei = len(beq); beq.append(1.0 if one else 0.0)
                if not one: eqr.append(ei); eqc.append(ai); eqv.append(-1.0)
                mus = []
                for v in comp:
                    vi = len(var); var.append(('m', r['ci'])); mus.append(vi)
                    bnd.append((None, None) if (cfree and r['kind'] == 'cons2') else (0, None))
                    eqr.append(ei); eqc.append(vi); eqv.append(1.0)
                    for kk, cv in v.items(): Arow.append(kid(kk)); Acol.append(vi); Aval.append(wf * cv)
                cs.append(mus)
            st.append((ai, const, comps, cs))
        struct.append((r, one, st))
    nk = len(keys); nv = len(var)
    zoff = nv
    for kk in range(nk): Arow.append(kk); Acol.append(zoff + kk); Aval.append(-1.0); bnd.append((0, None))
    cvec = np.zeros(nv + nk); cvec[zoff:] = 1.0 / float(TCO)
    Aub = coo_matrix((Aval, (Arow, Acol)), shape=(nk, nv + nk)).tocsr()
    bub = -np.array([cst.get(kk, 0.0) for kk in range(nk)])
    Aeq = coo_matrix((eqv, (eqr, eqc)), shape=(len(beq), nv + nk)).tocsr()
    t1 = time.time()
    res = linprog(cvec, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=np.array(beq), bounds=bnd, method='highs-ds' if not cfree else 'highs')
    assert res.status == 0, res.message
    x = res.x
    # exact evaluation of the (rationalised, renormalised) split
    def fr(v): return Fraction(max(v, 0.0) if not cfree else v).limit_denominator(10 ** 9)
    totR = collections.defaultdict(Fraction); contrib = collections.defaultdict(list)
    for r, one, st in struct:
        w = r['w']
        al = [Fraction(1)] if one else [fr(x[ai]) for ai, _, _, _ in st]
        sa = sum(al)
        if sa == 0: al = [Fraction(1)] + [Fraction(0)] * (len(al) - 1); sa = Fraction(1)
        al = [a / sa for a in al]
        if dump is not None: dump[r['ci']] = dict(al=al, mu=[])
        for (ai, const, comps, cs), a in zip(st, al):
            if dump is not None: dump[r['ci']]['mu'].append([])
            if a == 0: continue
            for kk, cv in const.items(): totR[kk] += w * a * cv; contrib[kk].append((w * a * cv, r))
            for comp, mus in zip(comps, cs):
                mu = [fr(x[vi]) for vi in mus]; sm = sum(mu)
                if sm == 0: mu = [Fraction(1)] + [Fraction(0)] * (len(mu) - 1); sm = Fraction(1)
                if dump is not None: dump[r['ci']]['mu'][-1].append([m_ / sm for m_ in mu])
                for v, m_ in zip(comp, mu):
                    if m_ == 0: continue
                    for kk, cv in v.items(): totR[kk] += w * a * (m_ / sm) * cv; contrib[kk].append((w * a * (m_ / sm) * cv, r))
    # coarsened ledger must be lowerR2's ledger for the family (spreading never changes the old columns)
    co = collections.defaultdict(Fraction)
    for kk, v in totR.items(): co[COARSE[f](kk)] += v
    oldk = {k: v for k, v in TOT.items() if k[0] == f and v}
    assert {k: v for k, v in co.items() if v} == oldk, 'coarsened ledger differs'
    rcR = {kk: -v / TCO for kk, v in totR.items()}
    neg = sorted([(rc, kk) for kk, rc in rcR.items() if rc < 0], key=lambda t: t[0])
    oldneg = sum((rc for k, rc in RC0.items() if k[0] == f and rc < 0), Fraction(0))
    S = -sum((rc for rc, _ in neg), Fraction(0))
    SB = -sum((rc for rc, kk in neg if any(r['kind'] == 'receiverR2' and v for v, r in contrib[kk])), Fraction(0))
    NB = sum(1 for rc, kk in neg if any(r['kind'] == 'receiverR2' and v for v, r in contrib[kk]))
    pin = collections.Counter((r['kind'], len(md) == 1 and all(len(c) == 1 for c in md[0][1])) for r, md in RM)
    out = dict(ref=ref, rows=len(RM), pinned=pinned, ncol=len(keys), nold=len({COARSE[f](kk) for kk in keys}), nneg=len(neg),
               minrc=neg[0][0] if neg else Fraction(0), S=S, SB=SB, NB=NB, pin=dict(pin), lp=res.fun, nvar=nv, oldneg=-oldneg, neg=neg, contrib=contrib, rcR=rcR,
               t=time.time() - t1)
    if f == 'x': out['Dcap3'] = DP + XCAP * oldneg * -1 + XCAP * -S   # D with x priced at its real cap 3 after the split
    if dump is not None: out['struct'] = struct; out['totR'] = totR
    return out
def write_spread(o, dump, path):
    """per cert row / relabel mode / big position / completion: outer letters and exact weight; implied mrowX duals"""
    ref = o['ref']; assert ref in ('x_outM', 'x_outMW'), ref
    F = lambda q: str(q)
    def side_letter(v, d, i):   # var ('T', i, 'p', m) or ('T', i, 'X', m, sd) -> '+' / '-'
        if v[2] == 'p': return '+' if v[3] == (i + 1) % d else '-'
        return '+' if v[4] == -1 else '-'
    rows_out = []; QD = {}; chk = collections.defaultdict(Fraction)
    for r, one, st in o['struct']:
        if r['kind'] != 'receiverR2': continue
        ex = dump[r['ci']]; md_lab = REL[r['ci']]
        assert len(md_lab) == len(st) == len(ex['al'])
        modes = []
        for (d, w, s), (ai, const, comps, cs), a, mus in zip(md_lab, st, ex['al'], ex['mu']):
            occs, dom = recv_occ(ref, d, w, s); U = min(d, 9); W_ = lambda k: w[k % d]; S_ = lambda k: s[k % d]
            bigs = [i for i in range(d) if w[i] >= 7]; assert len(occs) == 2 * len(bigs)
            byvars = {tuple(c.vars): (c, mu) for c, mu in zip(comps, mus)}
            used = set(); pos = []
            for k_, i in enumerate(bigs):
                (_, fin, vs), (_, fout, vs2) = occs[2 * k_], occs[2 * k_ + 1]; assert vs == vs2
                vp = next((v for v in vs if side_letter(v, d, i) == '+'), None); vm = next((v for v in vs if side_letter(v, d, i) == '-'), None)
                def mask(v, seen):
                    return sum(1 << (l_ - 5) for l_ in (dom[v] if v is not None else [seen]))
                Ap = (W_(i + 1), S_(i), W_(i + 2), S_(i + 1), mask(vp, S_(i + 1)))
                Am = (W_(i - 1), S_(i - 1), W_(i - 2), S_(i - 2), mask(vm, S_(i - 2)))
                swap = Am < Ap; q = (U, W_(i), min(Ap, Am), max(Ap, Am))
                if vs:
                    key = tuple(sorted({v for v in vs}))
                    comp, mu = byvars[key]; used.add(key)
                    cand = []
                    for j, (vec, m_) in enumerate(zip(comp, mu)):
                        asgs = [dict(zip(comp.vars, cb)) for cb in comp.asg[j]]
                        lets = [(a_.get(vp, S_(i + 1)) if vp else S_(i + 1), a_.get(vm, S_(i - 2)) if vm else S_(i - 2)) for a_ in asgs]
                        cand.append((lets, vec, r['w'] * a * m_))
                else:
                    vec = collections.Counter(); vec[fin({})] += 1; vec[fout({})] -= 1
                    cand = [([(S_(i + 1), S_(i - 2))], {k2: v2 for k2, v2 in vec.items() if v2}, r['w'] * a)]
                comp_out = []
                for lets, vec, wt in cand:
                    eA, eB = (lets[0][1], lets[0][0]) if swap else lets[0]
                    for kk, cv in vec.items(): chk[kk] += wt * cv
                    if a != 0:
                        qd = QD.setdefault(q, dict(recv=Fraction(0), cand=collections.defaultdict(Fraction)))
                        qd['cand'][(eA, eB)] += wt
                    comp_out.append({'outer_letters': [{'e+': ep, 'e-': em} for ep, em in lets], 'weight': F(wt),
                                     'mrowX_candidate': [eA, eB], 'mrowX_dual': F(wt),
                                     'vector': [[list(kk[:2]) + [list(kk[2]), list(kk[3])], cv] for kk, cv in sorted(vec.items())]})
                if a != 0: QD[q]['recv'] += r['w'] * a
                pos.append({'i': i, 'V': W_(i), 'q': [q[0], q[1], list(q[2]), list(q[3])], 'A_is_plus_side': not swap,
                            'unseen': {'e+': vp is not None, 'e-': vm is not None},
                            'domain': {'e+': (dom[vp] if vp else [S_(i + 1)]), 'e-': (dom[vm] if vm else [S_(i - 2)])},
                            'completions': comp_out})
            assert used == set(byvars), (lab(r), used, set(byvars))
            for kk, cv in const.items(): pass   # const = the pinned positions, already written per position above
            modes.append({'relabel': [d, ''.join(map(str, w)), ''.join(map(str, s))], 'alpha': F(a), 'row_weight_share': F(r['w'] * a), 'positions': pos})
        rows_out.append({'ci': r['ci'], 'label': r['label'], 'w': F(r['w']), 'modes': modes})
    # the written split reproduces the pricer's exact refined ledger, hence its rc and sum max(0, -rc)
    assert {k: v for k, v in chk.items() if v} == {k: v for k, v in o['totR'].items() if v}, 'spread ledger differs'
    mrowx = []
    for q, qd in sorted(QD.items()):
        sy = sum(qd['cand'].values(), Fraction(0)); assert sy == qd['recv'], (q, sy, qd['recv'])   # XQ[q] column balances
        mrowx.append({'q': [q[0], q[1], list(q[2]), list(q[3])], 'sum_receiver_weight': F(qd['recv']),
                      'duals': [{'cand': [eA, eB], 'w': F(v)} for (eA, eB), v in sorted(qd['cand'].items()) if v]})
    json.dump({'ref': ref, 'tag': TAG, 'cert': CERT, 'tco': F(TCO), 'S': F(o['S']), 'nneg': o['nneg'], 'minrc': F(o['minrc']),
               'neg': [[F(rc), [kk[0], kk[1], list(kk[2]), list(kk[3])]] for rc, kk in o['neg']],
               'note': 'weights exact (Fractions as strings); receiver and mrowX duals are <= 0; rc(key) = -sum(weight*coef)/tco',
               'rows': rows_out, 'mrowX': mrowx}, open(path, 'w'), indent=1)
    print('    spread written: %s (%d receiver rows, %d credit keys q, %d mrowX duals != 0); ledger and XQ balances checked' % (
        path, len(rows_out), len(mrowx), sum(len(m['duals']) for m in mrowx)), flush=True)
def show(o, top=10):
    caps = ('0.05', '0.1', '0.3')
    print('\n=== %s [%s]: rows touched %d (fully pinned %d), refined columns %d (old %d), LP vars %d, LP min sum max(0,-rc) %.6g (%.1fs)' % (
        o['ref'], REFN.get(o['ref'], o['ref']), o['rows'], o['pinned'], o['ncol'], o['nold'], o['nvar'], o['lp'], o['t']))
    print('    exact split: rc<0 %d, most negative %s = %.6f, sum max(0,-rc) = %s = %.6f; x 3 cap priced old neg sum %.6f' % (
        o['nneg'], o['minrc'], float(o['minrc']), o['S'], float(o['S']), float(o['oldneg'])))
    print('    pinned by label (kind, pinned): %s; negative keys touching a receiverR2 (binder) row: %d, their sum max(0,-rc) %s = %.6f' % (
        sorted(o['pin'].items()), o['NB'], o['SB'], float(o['SB'])))
    print('    gain sum max(0,-rc)*cap: ' + ', '.join('cap %s %.6f' % (c, float(o['S'] * Fraction(c))) for c in caps))
    if 'Dcap3' in o: print('    x at its real cap 3: valid bound after the split D = %s = %.9f (old %.9f)' % (o['Dcap3'], float(o['Dcap3']), float(DP)))
    for rc, kk in o['neg'][:top]:
        cs = sorted(o['contrib'][kk], key=lambda t: -abs(t[0]))
        agg = collections.defaultdict(Fraction)
        for v, r in cs: agg[lab(r)] += v
        print('    rc %s = %+.6f  key %s | %s' % (rc, float(rc), kk, '; '.join('%s %+.5f' % (l_, float(v / TCO)) for l_, v in sorted(agg.items(), key=lambda t: -abs(t[1]))[:6])))
    sys.stdout.flush()
RES = {}
for ref, nm in REFS:
    if ONLY and ref not in ONLY: continue
    SPD = {} if (os.environ.get('SPREAD51') and ref == os.environ.get('SPREAD51_REF', 'x_outMW')) else None
    o = price(ref, dump=SPD); RES[ref] = o; show(o)
    if SPD is not None: write_spread(o, SPD, os.environ['SPREAD51'])
    if ref.endswith('0'):   # control: level 0 = lowerR2's rc on every column of the family, exactly
        f = ref[0]; mine = {COARSE[f](kk): rc for kk, rc in o['rcR'].items()}
        eng = {k: rc for k, rc in RC0.items() if k[0] == f}
        assert all(mine.get(k, 0) == v for k, v in eng.items()) and all(eng.get(k, 0) == v for k, v in mine.items()), 'CONTROL FAIL ' + ref
        print('    CONTROL %s: %d columns (%d touched), every rc equals lowerR2 rc exactly; negative uncapped %d (lowerR2 lists %d)' % (
            ref, len(eng), len(mine), sum(1 for v in mine.values() if v < 0 and f != 'x'), len([1 for k, _ in CAP['neg'] if k[0] == f])))
    elif ref not in ('x_out', 'x_outM', 'x_outMW'):
        o2 = price(ref, relabel=False); RES[ref + ':asis'] = o2
        print('    as-labelled (no relabel freedom): rc<0 %d, most negative %.6f, sum max(0,-rc) %.6f' % (o2['nneg'], float(o2['minrc']), float(o2['S'])))
        if ref.startswith('h'):
            o3 = price(ref, cfree=True); RES[ref + ':cfree'] = o3
            print('    cons2 weights free-sign split: rc<0 %d, sum max(0,-rc) %.6f' % (o3['nneg'], float(o3['S'])))
    else:
        o2 = price(ref, relabel=False); RES[ref + ':asis'] = o2
        print('    as-labelled (no relabel freedom): rc<0 %d, most negative %.6f, sum max(0,-rc) %.6f; Dcap3 %.9f' % (o2['nneg'], float(o2['minrc']), float(o2['S']), float(o2['Dcap3'])))
json.dump({k: dict(SB=str(o['SB']), NB=o['NB'], pin=str(o['pin']), nneg=o['nneg'], minrc=str(o['minrc']), S=str(o['S']), ncol=o['ncol'], nold=o['nold'], rows=o['rows'], pinned=o['pinned'],
                   Dcap3=str(o.get('Dcap3')), neg=[[str(rc), str(kk)] for rc, kk in o['neg'][:40]]) for k, o in RES.items()},
          open(os.path.join(B, 's51', 'price_%s.json' % TAG), 'w'), indent=1)
print('\nDONE %s (%.0fs)' % (TAG, time.time() - T0))
