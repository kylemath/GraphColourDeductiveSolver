"""EXPLORE round 20 (H-L2, exploratory): big-big transfers in the wlp3 LP.  Restricted LP, not a bound.
Senders, rooted variables y and the pattern set are wlp3_j28_12's (j28_12.args; sep3).  Rows are whole arrangements
(d, link, s).  A transfer variable x[tau] >= 0 per oriented edge type tau = (deg from, deg to, two sides unordered),
side = (common neighbour c, vertex at 'from' and c, vertex at 'to' and c); degrees as letters 7, 8, 9 (9 = >= 9).
A row with a big link vertex k gets  -x[out tau] + x[in tau]  (out: this centre -> k; in: k -> this centre).
Separation: y-only sep3 (d = 7..14) for rows without in-transfers; for every tau with x > 0, the heaviest arrangement
at the receiving end showing tau (DP over 6-letter states, own transfer terms included, best-first enumeration,
then sep3 'c' for patterns and RBIG).
Usage: python3 l2.py [notx] [maxit=N] [tmax=SECONDS]"""
import sys, os, re, time, heapq, collections
import numpy as np
import scipy.sparse as sps
from scipy.optimize import linprog
L2D = os.path.dirname(os.path.abspath(__file__)); WD = os.path.dirname(os.path.dirname(L2D))
OPTS = sys.argv[1:]
NOTX = 'notx' in OPTS
MAXIT = int(next((a[6:] for a in OPTS if a.startswith('maxit=')), '60'))
TMAX = float(next((a[5:] for a in OPTS if a.startswith('tmax=')), '2400'))
T0 = time.time()
jargs = [a.strip() for a in open(os.path.join(L2D, 'j28_12.args')) if a.strip()]
jargs = [a for a in jargs if os.path.exists(os.path.join(WD, a.split('=', 1)[-1].replace(':all', ''))) or a == 'w7plus']
src = open(os.path.join(WD, 'wlp3.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(WD, 'wlp3.py')), 1)
sys.argv = ['wlp3'] + jargs + ['tag=l2' + ('x' if not NOTX else '0')]
exec(src[:src.index('A_ub, b_ub = [], []')])
NY = len(roots)
def check(d, lk, sv):
    SEP.stdin.write('c %d %s %s\n' % (d, lk, sv)); SEP.stdin.flush(); return SEP.stdout.readline().strip() == '1'
LT = (5, 6, 7, 8, 9)
def li(c): return int(c) - 5

# ---- edge types
def tkey(f, t, s1, s2):
    """f, t letter indices (2..4), sides = (c, a_from, a_to) letter indices"""
    a = s1[0] * 25 + s1[1] * 5 + s1[2]; b = s2[0] * 25 + s2[1] * 5 + s2[2]
    if a > b: a, b = b, a
    return (((f - 2) * 3 + (t - 2)) * 125 + a) * 125 + b
def tdec(k):
    b = k % 125; k //= 125; a = k % 125; k //= 125; t = k % 3 + 2; f = k // 3 + 2
    tri = lambda z: (z // 25, z // 5 % 5, z % 5)
    return f, t, tri(a), tri(b)
def tname(k):
    f, t, a, b = tdec(k); s = lambda z: ''.join(str(LT[q]) for q in z)
    return '%d->%d [%s|%s]' % (LT[f], LT[t], s(a), s(b))
NK = 9 * 125 * 125

# ---- rows
def canon_arr(lk, sv):
    d = len(lk); best = None
    for refl in (0, 1):
        if refl: l2 = [lk[(-i) % d] for i in range(d)]; s2 = [sv[(-i - 1) % d] for i in range(d)]
        else: l2, s2 = list(lk), list(sv)
        for r in range(d):
            c = ''.join(l2[r:] + l2[:r]) + ' ' + ''.join(s2[r:] + s2[:r])
            if best is None or c < best: best = c
    return best
def row_terms(d, lk, sv):
    """(y index list, {tau: coef}) of the arrangement; None if it has an R5 five"""
    U = min(d, 9); Ui = U - 5; w = [li(c) for c in lk]; s = [li(c) for c in sv]; ys = []; xs = collections.Counter()
    for i in range(d):
        if w[i] == 0:
            ww = [U, LT[w[(i + 1) % d]], LT[s[i]], LT[s[(i - 1) % d]], LT[w[(i - 1) % d]]]
            if isR5(ww): return None
            ys.append(ix[root(ww, 0)])
        elif w[i] >= 2:
            lm1, lm2, lp1, lp2 = w[(i - 1) % d], w[(i - 2) % d], w[(i + 1) % d], w[(i + 2) % d]
            sm, sp_ = s[(i - 1) % d], s[i]
            xs[tkey(Ui, w[i], (lm1, lm2, sm), (lp1, lp2, sp_))] -= 1
            xs[tkey(w[i], Ui, (lm1, sm, lm2), (lp1, sp_, lp2))] += 1
    return ys, {k: v for k, v in xs.items() if v}
ROWS = []; RKEY = {}; RSRC = []
def add_row(d, lk, sv, srcname):
    key = (d, canon_arr(lk, sv))
    if key in RKEY: return False
    rt = row_terms(d, lk, sv)
    if rt is None: return False
    RKEY[key] = len(ROWS); ROWS.append((d, lk, sv, rt[0], rt[1])); RSRC.append(srcname); return True
def rows_from(fn, srcname, pat):
    n = m = 0
    for line in open(fn):
        mm = re.search(pat, line)
        if not mm: continue
        d, lk, sv = (int(mm.group(1)), mm.group(2), mm.group(3)) if mm.lastindex == 3 else (7, mm.group(1), mm.group(2))
        if d > 15 or not check(d, lk, sv): m += 1; continue
        n += add_row(d, lk, sv, srcname)
    print('rows from %s: +%d (forbidden by the j28_12 patterns: %d)' % (os.path.basename(fn), n, m), flush=True)
rows_from(os.path.join(WD, 'out', 'job28', 'tight_12.txt'), 'tight12', r'receiver d=(\d+) link (\d+) s (\d+)')
rows_from(os.path.join(WD, 'loop', 'w2', 'cov2.txt'), 'fam617', r'^(\d{7}) (\d{7}) ')
HARD = []
for line in open(os.path.join(WD, 'loop', 'lf', 'seeds.txt')):
    f = line.split(); HARD.append((7, canon_arr(f[0], f[1]), f[2]))

# ---- LP
XCOL = {}   # tau -> column offset
def solve():
    for d, lk, sv, ys, xs in ROWS:
        for k in xs:
            if k not in XCOL and not NOTX: XCOL[k] = len(XCOL)
    nx = len(XCOL); ncol = NY + 1 + nx; it = NY
    ri, ci, vv, b = [], [], [], []; r = 0
    for w in senders:
        for j in range(5):
            if w[j] >= 7: ri.append(r); ci.append(ix[root(list(w), j)]); vv.append(-1.0)
        ri.append(r); ci.append(it); vv.append(-1.0); b.append(-1.0); r += 1
    for d, lk, sv, ys, xs in ROWS:
        for q in ys: ri.append(r); ci.append(q); vv.append(1.0)
        ri.append(r); ci.append(it); vv.append(-1.0)
        if not NOTX:
            for k, c in xs.items(): ri.append(r); ci.append(NY + 1 + XCOL[k]); vv.append(float(c))
        b.append(d - 6.0); r += 1
    A = sps.csr_matrix((vv, (ri, ci)), shape=(r, ncol))
    cvec = np.zeros(ncol); cvec[it] = 1.0
    res = linprog(cvec, A_ub=A, b_ub=np.array(b), bounds=[(0, 1)] * NY + [(None, None)] + [(0, 3)] * nx, method='highs')
    assert res.status == 0, res.message
    yv = res.x[:NY]; t = res.x[NY]; xfull = np.zeros(NK + 1)
    for k, c in XCOL.items(): xfull[k] = res.x[NY + 1 + c]
    duals = -res.ineqlin.marginals; slack = np.array(b) - A @ res.x
    return t, yv, xfull, duals[len(senders):], slack[len(senders):]
def row_value(ys, xs, yv, xfull):
    return sum(yv[q] for q in ys) + sum(c * xfull[k] for k, c in xs.items())

# ---- v-side DP tables: state (L[i-3], L[i-2], S[i-2], L[i-1], S[i-1], L[i]), choice (S[i], L[i+1])
NS6 = 5 ** 6
st = np.arange(NS6); A_, B_, C_, E_, F_, G_ = [(st // 5 ** (5 - p)) % 5 for p in range(6)]
NX = np.empty((NS6, 25), dtype=np.int64); YI = {}; XIN = {}; XOUT = {}
for ch in range(25):
    h, j = ch // 5, ch % 5
    NX[:, ch] = ((((B_ * 5 + E_) * 5 + F_) * 5 + G_) * 5 + h) * 5 + j
for U in (7, 8, 9):
    Ui = U - 5
    y5 = np.full(5 ** 5, -1, dtype=np.int64)   # (e, f, g, h, j) -> -2 forbidden, -1 zero, >= 0 y index
    for z in range(5 ** 5):
        e, f, g, h, j = [(z // 5 ** (4 - p)) % 5 for p in range(5)]
        if g == 0:
            ww = [U, LT[j], LT[h], LT[f], LT[e]]
            y5[z] = -2 if isR5(ww) else ix[root(ww, 0)]
        elif g == 1:
            if all(isR6([U, LT[j], LT[h], p, LT[f], LT[e]]) for p in LT): y5[z] = -2
    yi = np.empty((NS6, 25), dtype=np.int64); xin = np.full((NS6, 25), NK, dtype=np.int64); xout = xin.copy()
    for ch in range(25):
        h, j = ch // 5, ch % 5
        yi[:, ch] = y5[(((E_ * 5 + F_) * 5 + G_) * 5 + h) * 5 + j]
        big = E_ >= 2
        a = np.minimum(B_ * 25 + C_ * 5 + A_, G_ * 25 + F_ * 5 + j); b2 = np.maximum(B_ * 25 + C_ * 5 + A_, G_ * 25 + F_ * 5 + j)
        kin = (((np.clip(E_ - 2, 0, 2)) * 3 + (Ui - 2)) * 125 + a) * 125 + b2
        a = np.minimum(B_ * 25 + A_ * 5 + C_, G_ * 25 + j * 5 + F_); b2 = np.maximum(B_ * 25 + A_ * 5 + C_, G_ * 25 + j * 5 + F_)
        kout = (((Ui - 2) * 3 + np.clip(E_ - 2, 0, 2)) * 125 + a) * 125 + b2
        xin[:, ch] = np.where(big, kin, NK); xout[:, ch] = np.where(big, kout, NK)
    YI[U], XIN[U], XOUT[U] = yi, xin, xout
print('DP tables ready (%.0fs)' % (time.time() - T0), flush=True)
def gains(yv, xfull):
    yfull = np.concatenate([yv, [0.0, -np.inf]])
    return {U: yfull[np.where(YI[U] >= 0, YI[U], np.where(YI[U] == -1, NY, NY + 1))] + xfull[XIN[U]] - xfull[XOUT[U]]
            for U in (7, 8, 9)}
def vside(k, d, G, thr, cap=400):
    """allowed arrangements of degree d showing tau = k at position 0 (k -> centre), value > thr, best first"""
    f, t, s1, s2 = tdec(k); U = min(d, 9); Gu = G[U]
    Lf = {0: f, d - 1: s1[0], d - 2: s1[2], 1: s2[0], 2: s2[2]}; Sf = {d - 1: s1[1], 0: s2[1]}
    start = ((((Lf[d - 2] * 5 + Lf[d - 1]) * 5 + Sf[d - 1]) * 5 + Lf[0]) * 5 + Sf[0]) * 5 + Lf[1]
    masks = {}
    for i in range(1, d + 1):
        m = np.ones(25, dtype=bool)
        if i % d in Sf: m &= (np.arange(25) // 5) == Sf[i % d]
        if (i + 1) % d in Lf: m &= (np.arange(25) % 5) == Lf[(i + 1) % d]
        masks[i] = np.nonzero(m)[0]
    B = [None] * (d + 2); B[d + 1] = np.full(NS6, -np.inf); B[d + 1][start] = 0.0
    for i in range(d, 0, -1):
        cs = masks[i]; B[i] = (Gu[:, cs] + B[i + 1][NX[:, cs]]).max(axis=1)
    if B[1][start] <= thr: return [], B[1][start], 0
    heap = [(-B[1][start], 0.0, 1, start, ())]; out = []; leaves = 0
    while heap and leaves < cap:
        nb, acc, i, s, chs = heapq.heappop(heap)
        if i == d + 1:
            leaves += 1
            lk = [None] * d; sv = [None] * d
            for p, q in Lf.items(): lk[p] = q
            for p, q in Sf.items(): sv[p] = q
            for ii, ch in zip(range(1, d + 1), chs): sv[ii % d] = ch // 5; lk[(ii + 1) % d] = ch % 5
            lks = ''.join(str(LT[q]) for q in lk); svs = ''.join(str(LT[q]) for q in sv)
            if (d, canon_arr(lks, svs)) in RKEY: continue
            if d <= 15 and not check(d, lks, svs): continue
            out.append((acc, lks, svs))
            if len(out) >= 3: break
            continue
        for ch in masks[i]:
            g = Gu[s, ch]
            if g == -np.inf: continue
            ns = NX[s, ch]; v = acc + g + B[i + 1][ns]
            if v > thr: heapq.heappush(heap, (-v, acc + g, i + 1, ns, chs + (int(ch),)))
    return out, B[1][start], leaves

# ---- main loop
hist = []
for it_ in range(MAXIT):
    t, yv, xfull, duals, slack = solve()
    added = collections.Counter(); masked = 0
    # y-only separation
    for d in range(7, 15):
        thr = d - 6 + t + 1e-7
        res_, nodes = sep(d, yv, thr, 200)
        for v, lk, sv, p in res_:
            rt = row_terms(d, lk, sv)
            if rt is None: continue
            if row_value(rt[0], rt[1], yv, xfull) > thr:
                if add_row(d, lk, sv, 'sep3'): added['sep3_d%d' % d] += 1
            else: masked += 1
    # v-side separation
    G = gains(yv, xfull); nt = 0; vmax = collections.Counter()
    if not NOTX:
        for k in np.nonzero(xfull[:NK] > 1e-9)[0]:
            f, tt, s1, s2 = tdec(int(k)); nt += 1
            for d in ((7,) if tt == 2 else (8,) if tt == 3 else (9, 10, 11, 12)):
                out, best, leaves = vside(int(k), d, G, d - 6 + t + 1e-7)
                for v, lk, sv in out:
                    if add_row(d, lk, sv, 'vside'): added['vside_d%d' % d] += 1
                if leaves >= 400 and not out: vmax['capped'] += 1
            if time.time() - T0 > TMAX: break
    nadd = sum(added.values())
    print('iter %d t=%.6f rows %d xcols %d tau>0 %d added %s masked %d capped %d (%.0fs)' % (
        it_, t, len(ROWS), len(XCOL), nt, dict(added), masked, vmax['capped'], time.time() - T0), flush=True)
    hist.append((it_, t, len(ROWS), dict(added)))
    if not nadd or time.time() - T0 > TMAX: break

# ---- report
t, yv, xfull, duals, slack = solve()
tag = 'notx' if NOTX else 'x'
out = ['# l2.py %s: t* = %.6f (13/49 = %.6f); %d rows, %d transfer columns, converged=%s (%d iterations, %.0fs)' % (
    ' '.join(OPTS), t, 13 / 49, len(ROWS), len(XCOL), 'yes' if not nadd else 'NO', len(hist), time.time() - T0)]
out.append('rows by source: %s' % dict(collections.Counter(RSRC)))
bind = collections.Counter(); bindw = collections.Counter()
for q, dv in enumerate(duals):
    if dv > 1e-9: bind[(RSRC[q], ROWS[q][0])] += 1; bindw[(RSRC[q], ROWS[q][0])] += dv
out.append('binding rows (positive dual) by source, degree: count / total dual weight')
for kk in sorted(bind): out.append('  %s d=%d: %d / %.4f' % (kk[0], kk[1], bind[kk], bindw[kk]))
tight = collections.Counter((RSRC[q], ROWS[q][0]) for q in range(len(ROWS)) if slack[q] < 1e-7)
out.append('tight rows by source, degree: %s' % dict(sorted(tight.items())))
out.append('HARD28-like rows (49): slack at t*')
nsl = 0
for d, ck, lab in HARD:
    q = RKEY.get((d, ck))
    if q is None: out.append('  %s %s: not in the LP (forbidden by the j28_12 patterns)' % (ck, lab)); continue
    out.append('  %s %s: slack %.4f dual %.4f' % (ck, lab, slack[q], duals[q])); nsl += slack[q] > 1e-7
out.append('HARD28-like rows slack: %d of %d in the LP' % (nsl, sum(1 for d, ck, lab in HARD if (d, ck) in RKEY)))
xs = sorted(((xfull[k], k) for k in XCOL if xfull[k] > 1e-9), reverse=True)
out.append('transfers x > 0: %d; largest:' % len(xs))
for v, k in xs[:25]: out.append('  %.4f  %s' % (v, tname(k)))
out.append('binding rows (largest dual first):')
for q in np.argsort(-duals)[:40]:
    if duals[q] <= 1e-9: break
    d, lk, sv, ys, xx = ROWS[q]
    out.append('  %.4f  %s d=%d link %s s %s  y=%.4f x=%+.4f' % (duals[q], RSRC[q], d, lk, sv, sum(yv[z] for z in ys),
                                                           sum(c * xfull[k] for k, c in xx.items())))
out.append('iterations: ' + ' '.join('%d:%.4f' % (h[0], h[1]) for h in hist))
open(os.path.join(L2D, 'l2_%s.txt' % tag), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
