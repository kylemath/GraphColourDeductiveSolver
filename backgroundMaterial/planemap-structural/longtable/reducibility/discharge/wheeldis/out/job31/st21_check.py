"""Stage 28 check (RELAY_SPEC section 21, s28q 321660a8): l3q on the st24b class (sections 12, 14', 15 hat5, v6 off),
extending st18_check.py from the spec alone; no Opus code. L3Q=1:
- receiverR2 of a d = 7 row: for each link 7 w_i and side sigma, payer -lq[(w_{i+s}, w_{i+2s}, w_{i+3s})] (c, a in {5, 6})
  and payee +lQ[(c, a, m)] with c = w_{i+s}, a = s_i (+) / s_{i-1} (-), m = Studio's mask table (l3q_masks.py) at
  (sigma, c, w_{i+2s}, w_{i+3s}, w_{i+4s}, a, o = s_{i-1} (+) / s_i (-)); lQ valued as Qeff = max(LP, max_{a2 in m} q).
- mrowL rows (lower): lq[(c, a, a2)] - lQ[(c, a, m)] <= 0, a2 in m, weight <= 0; lq with negative reduced cost priced at
  lqcap, lQ with negative reduced cost invalidates the certificate.
- Upper d = 7 via bin/sep3r_l3q (sep3r_ak + SEP_L3Q): relaxed window term UB(w_{i+1}, s_i) + UB(w_{i-1}, s_{i-1}) at a
  link 7, exact payee and payer terms at the leaf.
Stage 18 check: hat channel H5 (RELAY_SPEC section 15, 8f71209b) on the s21f base class (sections 12 + 14', no v6),
extending st16_check.py from the spec alone; no Opus code. HAT5=1:
- senderR2 enumerates all five hat classes (fans at 6-spokes only); each big hat k (H[k] = 1) adds + r[K] with K from
  the sender-row formula (st18_keys.key_sender). Admissibility as before (per six).
- receiverR2 (every d): each apex five s_i = 5 adds + r[K(w_{i-1}, w_i, w_{i+1}, w_{i+2}, s_{i-1}, s_{i+1})] to the load
  (st18_keys.key_receiver). The rows are implemented exactly as section 15 states them (the five's row gains + r, the
  big's load gains + r), so as an LP r is a five -> big transfer, although the prose says "b sends r[K] to v".
- Receivers d = 7..17 via sep3r_ak with SEP_EXACT6 (six windows) and SEP_RTAB: a relaxed r (max over the unread
  w_{i+2}, s_{i+1}) is added to the window weight, so the pruning bound stays an upper bound, and each leaf swaps in the
  exact r. Tail d = 18..30 and Karp: Studio's own max-plus matrix with the relaxed r added at s_i = 5 transitions.
Usage: L3Q=1 L3TAB=tab+1.json,tab-1.json HAT5=1 V6=0 DMAXP=17 EXPECT_T=<t> EXPECT_PAT=... python3 out/job31/st18_check.py SOL CERT ARGSFILE"""
import sys, os, json, re, itertools, collections, random
from fractions import Fraction as Fr
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
DIS = os.path.dirname(HERE)
SOLF, CERTF, ARGF = sys.argv[1], sys.argv[2], sys.argv[3]
SOL = json.load(open(SOLF)); CERT = json.load(open(CERTF)); ARGS = open(ARGF).read().split()
EPS = 1e-9; FAIL = []
V6 = os.environ.get('V6', '1') == '1'
HAT5 = os.environ.get('HAT5', '1') == '1'
L3Q = os.environ.get('L3Q', '0') == '1'; L3TAB = os.environ.get('L3TAB', '')
# RELAY_SPEC s45 / s47 (l3qV = 7,8): L3Q8=1 adds V = 8 (payer -lq[(8, c, a, a2)] at a d = 7 link 8; payee +lQ[(8, c, a, m)] at a
# d = 8 link 7, m from the V = 8 table L3TAB8 = tab+1,tab-1); BROKEN8 = a deliberate rule break, for the broken-build control only
# RELAY_SPEC s51 (flag xo): XO=1 replaces x by xo (outer-letter sides) + the per-position credit XQ (mrowX); XOBROKEN = end / sign
# (broken-build controls only); XOPRICE=1 = first-order xo pricing of a cert without mrowX rows (key check against s51.3)
XO = os.environ.get('XO', '0') == '1'; XOBROKEN = os.environ.get('XOBROKEN', ''); XOCAP = 3
L3Q8 = os.environ.get('L3Q8', '0') == '1'; L3TAB8 = os.environ.get('L3TAB8', ''); BROKEN8 = os.environ.get('BROKEN8', '')
# RELAY_SPEC s44 (fb, face-keyed big -> k-vertex transfer): FB=1, FBDIR = 6 / 7 / 67 (default 67), FBCAP optional
FB = os.environ.get('FB', '0') == '1'; FBDIR = os.environ.get('FBDIR', '67'); FBCAP = os.environ.get('FBCAP')
def fb_face(T): return T[0] == 5 and T[2] == 5 and T[3] == 5          # (c, b, e) = (5, 5, 5): c first, b third, e fourth
def fb_key(U, X, Tp, Tm):
    """44.2: sigma = (U, X, min(T+, T-), max(T+, T-)); a column iff a face side and X >= 6 (fb6: X = 6, fb7: X >= 7)"""
    if X < 6 or not (fb_face(Tp) or fb_face(Tm)): return None
    if X == 6 and '6' not in FBDIR: return None
    if X >= 7 and '7' not in FBDIR: return None
    return (U, X) + min(Tp, Tm) + max(Tp, Tm)
def fb_payer_T(W, S, j):   # u's row at j: T+ = (w_{j+1}, s_j, w_{j+2}, e+), T- = (w_{j-1}, s_{j-1}, w_{j-2}, e-)
    Tp = (W(j + 1), S(j), W(j + 2), S(j + 1) if W(j + 1) == 5 else 0)
    Tm = (W(j - 1), S(j - 1), W(j - 2), S(j - 2) if W(j - 1) == 5 else 0)
    return Tp, Tm
def fb_payee_T(L, t, k):   # X's row at u = L_k: T+ = (L_{k+1}, L_{k+2}, t_k, t_{k+1} if L_{k+1} = 5), T- mirrored
    Tp = (L(k + 1), L(k + 2), t(k), t(k + 1) if L(k + 1) == 5 else 0)
    Tm = (L(k - 1), L(k - 2), t(k - 1), t(k - 2) if L(k - 1) == 5 else 0)
    return Tp, Tm
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from st18_keys import key_sender, key_receiver   # V6=0: filtered s12r mode (section 14' mask on M only; no v, no V)
# per-solve expectations (defaults: s14r): EXPECT_T = claimed t* as a fraction, EXPECT_PAT = 'D,C,RPAT' distinct pattern counts
EXPECT_T = Fr(os.environ.get('EXPECT_T', '19/102')); EXPECT_PAT = tuple(int(v) for v in os.environ.get('EXPECT_PAT', '15497,1494,158').split(','))
def fail(msg): FAIL.append(msg); print('FAIL: ' + msg, flush=True)
LET = (5, 6, 7, 8, 9); LI = {l: l - 5 for l in LET}
def c(l): return 1 if l >= 7 else 0
CLS2 = {0: (5, 6), 1: (7, 8, 9)}

# ================= spec 4.4: reducible sets =================
def canon(w):
    w = tuple(w); n = len(w); rots = [w[k:] + w[:k] for k in range(n)]; r = w[::-1]
    return min(rots + [r[k:] + r[:k] for k in range(n)])
UNC = {'565667', '565676', '565677', '565757', '565767', '565777'}
R5, R6 = set(), set()
for line in open(os.path.join(DIS, 'studio17', 'wheels17_verdicts.txt')):
    f = line.split()
    if not f or f[0].startswith('#'): continue
    fam, word = f[0].split('_', 1); v = f[2]
    if v == 'D' or (v == 'C' and word not in UNC):
        (R5 if fam == 'c5' else R6).add(canon(tuple(int(ch) for ch in word)))
FANS = []
for line in open(os.path.join(HERE, 'out', 'fans_dfast.out')):
    if 'D=true' in line:
        nm = line.split()[0].split('_', 1)[1]; FANS.append(tuple(None if ch == 'F' else int(ch) for ch in nm))
def fanmatch(w, p):
    n = len(w)
    for r in range(n):
        for refl in (False, True):
            if all(pc is None or pc == (w[(r - i) % n] if refl else w[(r + i) % n]) for i, pc in enumerate(p)): return True
    return False
def isR5(w): return canon(w) in R5 or any(fanmatch(tuple(w), p) for p in FANS)
def isR6(w):
    w = tuple(w); return canon(w) in R6 or any(w[i] == w[(i + 1) % 6] == w[(i + 2) % 6] == 5 for i in range(6))
RBIG = set()
for line in open(os.path.join(HERE, 'out', 'bigwheels_dfast.out')):
    if 'D=true' in line: RBIG.add(canon(tuple(int(ch) for ch in line.split()[0].split('_')[1])))
import glob
for fn in [os.path.join(HERE, 'out', 'bigwheels1516_dfast_partial.out')] + glob.glob(os.path.join(HERE, 'out', 'def_*.out')):
    for line in open(fn):
        f = line.split()
        if f and re.match(r'^c[78]_\d+$', f[0]) and 'D=true' in line: RBIG.add(canon(tuple(int(ch) for ch in f[0][3:])))
for fn in glob.glob(os.path.join(HERE, 'out', 'def_*.cfast')):
    cur = None
    for line in open(fn):
        if ' r=' in line and not line.startswith(' '):
            m = re.match(r'^(?:c7_|\S*_w7_\d+_)(\d{7}) ', line); cur = m.group(1) if m else None
        elif 'C-REDUCIBLE' in line and cur: RBIG.add(canon(tuple(int(ch) for ch in cur)))
SPEC_R5 = '55555 55556 55557 55558 55566 55567 55568 55577 55578 55588 55656 55657 55658 55666 56566 56567 56568 56577 56578 56588 56657 56658 56666 66666'.split()
SPEC_R6 = ('555555 555556 555557 555566 555567 555577 555656 555657 555666 555667 555676 555677 555757 555767 555777 556556 '
           '556557 556566 556567 556576 556577 556657 556666 565656 565657 565666 566566 566567 566577 566657 566666').split()
SPEC_FANS = 'F5565 F5656 F5555 F5665 FF555 F5556 FF565'.split()
s2 = lambda S: {''.join(map(str, w)) for w in S}
print('R5 %d (spec 24, same set: %s); R6 %d (spec 31, same: %s); FANS %d (spec 7, same: %s); RBIG %d (spec 104)' % (
    len(R5), s2(R5) == set(SPEC_R5), len(R6), s2(R6) == set(SPEC_R6), len(FANS),
    {''.join('F' if x is None else str(x) for x in p) for p in FANS} == set(SPEC_FANS), len(RBIG)), flush=True)
if s2(R5) != set(SPEC_R5) or s2(R6) != set(SPEC_R6) or len(FANS) != 7 or len(RBIG) != 104: fail('reducible sets differ from spec 4.4')

# ================= spec 2 / 12.1-12.2: keys =================
def root5(a):
    a = tuple(a); return min(a, (a[0], a[4], a[3], a[2], a[1]))
def rootw(w, j): return root5(tuple(w[(j + k) % 5] for k in range(5)))
def ap(l): return 7 if l >= 7 else 5
def kh_of(L, j):
    a = tuple(L[(j + k) % 6] for k in range(6)); return min(a, (a[0], a[5], a[4], a[3], a[2], a[1]))
def h2_of(m, ar, al):
    """h2 of a 6 with link m rooted at the big m0; ar = apex beyond edge (m0, m1), al = apex beyond (m5, m0)."""
    m = tuple(m); return min(m + (ap(ar), ap(al)), (m[0], m[5], m[4], m[3], m[2], m[1]) + (ap(al), ap(ar)))
def g2_raw(n1, c2, c3, c4, n5, ar, al):
    """g2 from letters n1, n5, classes c2..c4 and apex classes (already ap-ed)."""
    a = (n1, c2, c3, c4, n5, ar, al); b = (n5, c4, c3, c2, n1, al, ar); return min(a, b)
def sig2_of(U, wr, sr, sl, wl, ar, al): return min((U, wr, sr, sl, wl, ar, al), (U, wl, sl, sr, wr, al, ar))
def cand2(sig):   # sig may carry the 14' allowed-p mask as an 8th element
    U, wr, sr, sl, wl, ar, al = sig[:7]; m = sig[7] if len(sig) == 8 else 31
    return {h2_of((U, wr, sr, p, sl, wl), ar, al) for p in LET if not isR6((U, wr, sr, p, sl, wl)) and (m >> (p - 5)) & 1}
def side(cc, a, b): return LI[cc] * 25 + LI[a] * 5 + LI[b]
def tau(fl, tl, s1, s2_): return (((LI[fl] - 2) * 3 + (LI[tl] - 2)) * 125 + min(s1, s2_)) * 125 + max(s1, s2_)
# apex classes enter only through ap(): the witnesses 5 and 7 stand for them (ap(5) = 5, ap(7) = 7)
AP = (5, 7)
# ---- section 13.1: cv, v, sigV, candV ----
def cv(l): return l if l < 7 else 7
CV = (5, 6, 7)
def v_of(m, ar, al):
    m = tuple(m); return min(m + (cv(ar), cv(al)), (m[0], m[5], m[4], m[3], m[2], m[1]) + (cv(al), cv(ar)))
def sigV_of(U, wr, sr, sl, wl, ar, al): return min((U, wr, sr, sl, wl, ar, al), (U, wl, sl, sr, wr, al, ar))
def candV(sig):
    U, wr, sr, sl, wl, ar, al = sig[:7]; m = sig[7] if len(sig) == 8 else 31
    return {v_of((U, wr, sr, p, sl, wl), ar, al) for p in LET if not isR6((U, wr, sr, p, sl, wl)) and (m >> (p - 5)) & 1}
import numpy as _np
KILLDIR = os.environ.get('KILLDIR', os.path.join(HERE, 'out', 'job31', 'st16'))   # section 14' tables of the solve's registry
KT = {7: _np.load(os.path.join(KILLDIR, 'kill_U7.npy')), 9: _np.load(os.path.join(KILLDIR, 'kill_U9.npy'))}
print('section 14 prime kill tables from %s' % KILLDIR)
KT[8] = KT[9]
def pmask(U, wm2, wm1, wp1, wp2, sm2, sm1, s0, sp1):
    K = KT[U][wm2 - 5, wm1 - 5, wp1 - 5, wp2 - 5, sm2 - 5, sm1 - 5, s0 - 5, sp1 - 5]
    return sum(1 << b for b in range(5) if not K[b])
# ---- RELAY_SPEC s51: xo keys, the visible side tuples, domain masks, the credit key q and its candidates ----
def sidex(cc, a, b, ea, eb): return (((LI[cc] * 5 + LI[a]) * 5 + LI[b]) * 5 + LI[ea]) * 5 + LI[eb]
def tauo(fl, tl, S1, S2): return (((LI[fl] - 2) * 3 + (LI[tl] - 2)) * 3125 + min(S1, S2)) * 3125 + max(S1, S2)
def tauo_dec(t):
    hi = t % 3125; lo = (t // 3125) % 3125; fi, ti = divmod(t // 3125 ** 2, 3)
    dg = lambda S: tuple(int(ch) + 5 for ch in _np.base_repr(S, 5).zfill(5))
    return 7 + fi, 7 + ti, dg(lo), dg(hi)
_AUC = {}
def xo_au(U, args8):   # OR over the two letters outside the window of the 14' private mask of that 6 (s51.3, window-local)
    k = (U, args8)
    if k not in _AUC:
        m = 0
        for x_, y_ in itertools.product(LET, LET):
            a = [x_ if v == 'x' else y_ if v == 'y' else v for v in args8]; m |= pmask(U, *a)
        _AUC[k] = m
    return _AUC[k]
def xo_window_sides(U, a, b, c, e, f, p, q, r, s_):
    """window (a, b, c, e, f; p, q, r, s) = (w_{i-2..i+2}; s_{i-2..i+1}) with a big centre c: the two visible tuples (c, a, b, o, m)"""
    if e == 5: mp = 1 << LI[s_]
    elif e == 6: mp = sum(1 << LI[x_] for x_ in LET if not isR6((U, f, s_, x_, r, c))) & xo_au(U, (b, c, f, 'x', q, r, s_, 'y'))
    else: mp = 31
    if b == 5: mm = 1 << LI[p]
    elif b == 6: mm = sum(1 << LI[x_] for x_ in LET if not isR6((U, c, q, x_, p, a))) & xo_au(U, ('x', a, c, e, 'y', p, q, r))
    else: mm = 31
    return (e, r, f, s_, mp), (b, q, a, p, mm)
def xo_sides_in_out(T, e_):   # T = (c, a, b, o, m): the in-side and out-side sidex codes for unseen letter e_
    cc, a, b, o, m = T
    if XOBROKEN == 'end': return sidex(cc, a, b, o, e_), sidex(cc, b, a, e_, o)   # broken control: u reads the far outer letter
    return sidex(cc, a, b, e_, o), sidex(cc, b, a, o, e_)
def xo_cands(qk):
    U, V, A, B = qk; out = []
    for eA in LET:
        if not (A[4] >> LI[eA]) & 1: continue
        ia, oa = xo_sides_in_out(A, eA)
        for eB in LET:
            if not (B[4] >> LI[eB]) & 1: continue
            ib, ob = xo_sides_in_out(B, eB); out.append((eA, eB, tauo(V, U, ia, ib), tauo(U, V, oa, ob)))
    return out
_XQK = {}
def xo_q(U, a, b, c, e, f, p, q, r, s_):   # the credit key of a big-centre window, or None (R6: empty mask, or in = out always)
    k = (U, a, b, c, e, f, p, q, r, s_)
    if k not in _XQK:
        Ap, Am = xo_window_sides(U, a, b, c, e, f, p, q, r, s_); qk = (U, c, min(Ap, Am), max(Ap, Am))
        cs = xo_cands(qk) if Ap[4] and Am[4] else []
        _XQK[k] = qk if cs and any(i_ != o_ for _, _, i_, o_ in cs) else None
    return _XQK[k]
def XQeff(qk): return max(XOV.get(i_, 0.0) - XOV.get(o_, 0.0) for _, _, i_, o_ in xo_cands(qk))
if os.environ.get('XODBG'):   # debug: XODBG='U a b c e f p q r s'
    _w = tuple(int(x) for x in os.environ['XODBG'].split()); print('XODBG sides', xo_window_sides(*_w), 'q', xo_q(*_w))
    if xo_q(*_w):
        for c_ in xo_cands(xo_q(*_w)): print('  cand', c_[:2], 'in', tauo_dec(c_[2]), 'out', tauo_dec(c_[3]))
    sys.exit(0)
def xo_windows_of(t_):   # every (U, window) at which key t_ is an in- or an out-key of some candidate (s51.5 (5)), forward-verified
    fl, tl, S1, S2 = tauo_dec(t_); out = set()
    for role, (V_, U_) in (('in', (fl, tl)), ('out', (tl, fl))):
        for P_, M_ in ((S1, S2), (S2, S1)):
            # sidex layout (c, x2, x3, x4, x5): in = (c, s_adj, w_adj, unseen, seen); out = (c, w_adj, s_adj, seen, unseen) (swapped for 'end')
            def rd(Tt):
                cc, x2, x3, x4, x5 = Tt
                if role == 'in': s_adj, w_adj, uns, seen = x2, x3, (x5 if XOBROKEN == 'end' else x4), (x4 if XOBROKEN == 'end' else x5)
                else: w_adj, s_adj, seen, uns = x2, x3, (x5 if XOBROKEN == 'end' else x4), (x4 if XOBROKEN == 'end' else x5)
                return cc, s_adj, w_adj, seen
            ep, rp, fp, sp = rd(P_); bm, qm, am, pm = rd(M_)
            wnd = (U_, am, bm, V_, ep, fp, pm, qm, rp, sp)
            qk = xo_q(*wnd)
            if qk and any(t_ in (i_, o_) for _, _, i_, o_ in xo_cands(qk)): out.add(wnd)
    return out

# ================= solution values =================
Y = {}
for k, v in SOL['y'].items():
    u, rest = k.split('|'); Y[(int(u),) + tuple(int(ch) for ch in rest)] = v
G = {tuple(k): v for k, v in SOL['g']}; H = {tuple(k): v for k, v in SOL['h']}; X = {int(k): v for k, v in SOL['x'].items()}
VV = {tuple(k): v for k, v in SOL.get('v', [])}
RR = {tuple(k): v for k, v in SOL.get('r', [])}
T = SOL['t']
if os.environ.get('TCHECK'): T = float(Fr(os.environ['TCHECK'])); print('TCHECK: every row checked at t = %s = %.15f (solution t %.15f)' % (os.environ['TCHECK'], T, SOL['t']), flush=True)
FBV = {tuple(k): v for k, v in SOL.get('fb', [])}
XOV = {int(k): v for k, v in (SOL.get('xo') or {}).items()}
if XO and os.environ.get('XORAND'): XOV = {}   # filled after the key functions (self-test only)
if not XO and XOV: fail('solution has xo values but xo is off (s51.5)')
if XO:
    if X: fail('xo on but the solution has old x values (s51.5: no mixing, R8)')
    if not os.environ.get('XORAND') and not SOL.get('xoflag'): fail('xo on but the solution has no xoflag')
    if os.environ.get('XORAND'):   # self-test only: random xo on every in / out key of 4000 random big-centre windows
        import random as _rx; _rx.seed(int(os.environ['XORAND'])); _n = 0
        while _n < 4000:
            U_, c_ = _rx.choice((7, 8, 9)), _rx.choice((7, 8, 9)); wnd = [_rx.choice(LET) for _ in range(8)]
            qk = xo_q(U_, wnd[0], wnd[1], c_, *wnd[2:])
            if not qk: continue
            _n += 1
            for _, _, i_, o_ in xo_cands(qk):
                for t_ in (i_, o_): XOV.setdefault(t_, _rx.random() * 0.05)
        print('XORAND: random xo on %d keys of 4000 windows' % len(XOV), flush=True)
    _xb = [(k, v) for k, v in XOV.items() if v < -1e-15 or v > XOCAP + 1e-9]
    print('xo: %d values, max %.3g; out of [0, xcap] %d' % (len(XOV), max(XOV.values(), default=0.0), len(_xb)), flush=True)
    if _xb: fail('xo values out of bounds %s' % _xb[:3])
if not FB and FBV: print('fb family OFF: %d fb values in the solution ignored (max %.3g)' % (len(FBV), max(FBV.values())), flush=True)
if FB and not os.environ.get('FBRAND') and FBV:   # s44A83: bounds [0, fbcap] and keys in the switched-on family (fbdir)
    _fbb = [(k, v) for k, v in FBV.items() if v < -1e-15 or (FBCAP and v > float(FBCAP) + 1e-12)]
    _fbk = [k for k in FBV if not ((k[1] == 6 and '6' in FBDIR) or (k[1] >= 7 and '7' in FBDIR)) or k[0] < 7]
    print('fb: %d values, min %.3g, max %.3g; out of bounds %d; keys outside fbdir=%s %d' % (len(FBV), min(FBV.values()), max(FBV.values()), len(_fbb), FBDIR, len(_fbk)), flush=True)
    if _fbb or _fbk: fail('fb values out of bounds or keys outside the family %s %s' % (_fbb[:3], _fbk[:3]))
if os.environ.get('FBPERTURB'):   # self-test only: FBPERTURB=value sets the largest-key fb amount (or a new key) to value
    _k = max(FBV, key=FBV.get); FBV[_k] = float(os.environ['FBPERTURB']); print('FBPERTURB: fb%s set to %s' % (_k, FBV[_k]), flush=True)
if FB and os.environ.get('FBRAND'):   # self-test only: random fb values on every possible key
    import random as _rnd; _rnd.seed(int(os.environ['FBRAND']))
    for U_ in LET:
        for X_ in LET:
            for Tp_ in itertools.product(LET, LET, LET, LET + (0,)):
                for Tm_ in itertools.product(LET, LET, LET, LET + (0,)):
                    k_ = fb_key(U_, X_, Tp_, Tm_) if (Tp_[3] == 0) == (Tp_[0] != 5) and (Tm_[3] == 0) == (Tm_[0] != 5) else None
                    if k_ and k_ not in FBV: FBV[k_] = _rnd.random() * 0.05
    print('FBRAND: %d random fb values' % len(FBV), flush=True)
LQ = {tuple(k): v for k, v in SOL.get('lq', [])}; LQQ = {tuple(k): v for k, v in SOL.get('lQ', [])}; LQCAP = float(SOL.get('lqcap', 3))
if L3Q8 and os.environ.get('L8RAND'):   # self-test only (s47 (3)): random V = 8 q on all 20 payer keys and random Q on every (c, a, m)
    import random as _r8; _r8.seed(int(os.environ['L8RAND']))
    for c_, a_, a2 in itertools.product((5, 6), (5, 6), LET): LQ[(8, c_, a_, a2)] = _r8.random() * 0.05
    for c_, a_, m_ in itertools.product((5, 6), (5, 6), (30, 31)): LQQ[(8, c_, a_, m_)] = _r8.random() * 0.08
    print('L8RAND: random V = 8 values on %d lq and %d lQ keys' % (20, 8), flush=True)
MASK = {}
if L3Q:
    for sg_, fn_ in zip((1, -1), L3TAB.split(',')):
        for r_ in json.load(open(fn_)): MASK[(sg_,) + tuple(r_[:6])] = r_[6]
    print('l3q: lq %d values %s, lQ %d values %s, lqcap %s; Studio mask table %d entries, masks %s' % (len(LQ), LQ, len(LQQ), LQQ, LQCAP,
          len(MASK), dict(collections.Counter(MASK.values()))), flush=True)
    if len(MASK) != 5000: fail('l3q mask table size %d != 5,000' % len(MASK))
MASK8 = {}
if L3Q8:
    for sg_, fn_ in zip((1, -1), L3TAB8.split(',')):
        for r_ in json.load(open(fn_)): MASK8[(sg_,) + tuple(r_[:6])] = r_[6]
    print('l3qV8: V = 8 mask table %d entries, masks %s' % (len(MASK8), dict(collections.Counter(MASK8.values()))), flush=True)
    if len(MASK8) != 5000: fail('V = 8 mask table size %d != 5,000' % len(MASK8))
def Qeff8(c_, a_, m_): return max([LQQ.get((8, c_, a_, m_), 0.0)] + [LQ.get((8, c_, a_, a2), 0.0) for a2 in LET if (m_ >> (a2 - 5)) & 1])
UBQ8 = {}
for (sg_, c_, a_, w2_, w3_, w4_, o_), m_ in MASK8.items(): UBQ8[(c_, a_)] = max(UBQ8.get((c_, a_), 0.0), Qeff8(c_, a_, m_))
def UB8(c_, a_): return UBQ8.get((c_, a_), 0.0) if c_ in (5, 6) and a_ in (5, 6) else 0.0
def Qeff(c_, a_, m_): return max([LQQ.get((c_, a_, m_), 0.0)] + [LQ.get((c_, a_, a2), 0.0) for a2 in LET if (m_ >> (a2 - 5)) & 1])
UBQ = {}
for (sg_, c_, a_, w2_, w3_, w4_, o_), m_ in MASK.items(): UBQ[(c_, a_)] = max(UBQ.get((c_, a_), 0.0), Qeff(c_, a_, m_))
def UB(c_, a_): return UBQ.get((c_, a_), 0.0) if c_ in (5, 6) and a_ in (5, 6) else 0.0
if L3Q:
    print('l3q UB(c, a) over the table masks: %s' % {k: round(v, 12) for k, v in sorted(UBQ.items())}, flush=True)
    ok8 = lambda k, last: len(k) == 4 and L3Q8 and k[0] == 8 and k[1] in (5, 6) and k[2] in (5, 6) and last(k[3])   # s47.3 (v)
    lqbad = [k for k in LQ if not ((len(k) == 3 and k[0] in (5, 6) and k[1] in (5, 6) and k[2] in LET) or ok8(k, lambda x: x in LET))] + \
            [k for k in LQQ if not ((len(k) == 3 and k[0] in (5, 6) and k[1] in (5, 6) and 0 < k[2] < 32) or ok8(k, lambda x: 0 <= x < 32))]
    if lqbad: fail('SOLUTION HAS lq / lQ KEYS OF A FAMILY THAT IS OFF OR MALFORMED (l3qV=%s): %s' % ('7,8' if L3Q8 else '7', lqbad[:5]))
    if L3Q8:
        print('l3qV8: lq8 %s, lQ8 %s; UB8(c, a) %s' % ({k: v for k, v in LQ.items() if len(k) == 4}, {k: v for k, v in LQQ.items() if len(k) == 4}, {k: round(v, 12) for k, v in sorted(UBQ8.items())}), flush=True)
        mlb8 = sum(1 for (sg_, c_, a_, w2_, w3_, w4_, o_), m_ in MASK8.items() for a2 in LET if (m_ >> (a2 - 5)) & 1 and LQ.get((8, c_, a_, a2), 0.0) > Qeff8(c_, a_, m_) + 1e-12)
        print('V = 8 mrowL over every table mask and every a2 in it, at Qeff8: violated %d' % mlb8)
        if mlb8: fail('V = 8 mrowL violated')
    if any(v < 0 or v > LQCAP + EPS for v in LQ.values()) or any(v < 0 for v in LQQ.values()): fail('l3q bounds')
    if not SOL.get('l3q'): fail('solution has no l3q flag')
    # mrowL under Qeff: lq[(c, a, a2)] <= Qeff(c, a, m) for every table mask m containing a2 (holds by construction; checked)
    mlb = sum(1 for (sg_, c_, a_, w2_, w3_, w4_, o_), m_ in MASK.items() for a2 in LET if (m_ >> (a2 - 5)) & 1 and LQ.get((c_, a_, a2), 0.0) > Qeff(c_, a_, m_) + 1e-12)
    print('mrowL over every table mask and every a2 in it, at Qeff: violated %d' % mlb)
    if mlb: fail('mrowL violated')
print('solution t = %.15f (claimed %s = %.15f), model %s apex %s apexcls %s zh %s: %d y, %d g, %d h, %d x, z %s' % (
    T, EXPECT_T, float(EXPECT_T), SOL.get('model'), SOL.get('apex'), SOL.get('apexcls'), SOL.get('zh'), len(Y), len(G), len(H), len(X), SOL.get('z')), flush=True)
if SOL.get('model') != 'R6x2' or not SOL.get('apexcls') or SOL.get('zh') or bool(SOL.get('v6')) != V6: fail('solution mode differs from V6=%d (model/apexcls/zh/v6)' % V6)
print('v values %d; r values %d; sol hat5 %s' % (len(VV), len(RR), SOL.get('hat5')))
if bool(SOL.get('hat5')) != HAT5: fail('solution hat5 flag differs from HAT5=%d' % HAT5)
LOWER_ONLY = os.environ.get('LOWER_ONLY') == '1'
if abs(T - float(EXPECT_T)) > 1e-12 and not LOWER_ONLY: fail('solution t differs from the claimed value')
badlen = [k for k in G if len(k) != 7] + [k for k in H if len(k) != 8] + [k for k in VV if len(k) != 8]
if badlen: fail('%d g/h keys of the wrong length' % len(badlen))
neg = [v for v in list(Y.values()) + list(G.values()) + list(H.values()) + list(X.values()) + list(VV.values()) + list(RR.values()) if v < 0]
xmax = max(X.values()) if X else 0.0
print('bounds: %d negative values; max x = %.6f (cap 3)' % (len(neg), xmax))
if neg or xmax > 3 + EPS: fail('bounds')
def Mval(sig): return max([H.get(k, 0.0) for k in cand2(sig)] + [0.0])
def Vval(sig): return min([VV.get(k, 0.0) for k in candV(sig)])   # missing v counts as 0 (spec 13, answer to Studio)
# stored V (from st15 on): [sigV, LP value, min over candV of v]; the rebuild must equal the stored min, LP value <= min
SV_ = SOL.get('V', []); vbad = vlp = 0
for ent in SV_:
    sg, lpv, mn = tuple(ent[0]), ent[1], ent[2]
    if sg[:7] != sigV_of(*sg[:7]) or not candV(sg): vbad += 1; vbad <= 5 and print('STORED V signature not canonical/admissible %s' % (sg,)); continue
    vmax_ = max(globals().get('vmax_', 0.0), abs(Vval(sg) - mn))
    if abs(Vval(sg) - mn) > 1e-9: vbad += 1; vbad <= 5 and print('STORED V min %s differs from rebuild %.12f: %s' % (mn, Vval(sg), ent))
    if lpv > mn + 1e-9: vlp += 1
print('stored V entries %d: rebuilt min differs (> 1e-9) %d, max |difference| %.3g; LP value above the min %d (allowed only <= min)' % (len(SV_), vbad, globals().get('vmax_', 0.0), vlp))
if vbad or vlp: fail('stored V entries disagree with the rebuild')
def val(key):
    if key[0] == 'y': return Y.get(key[1], 0.0)
    if key[0] == 'g': return G.get(key[1], 0.0)
    if key[0] == 'h': return H.get(key[1], 0.0)
    if key[0] == 'M': return Mval(key[1])
    if key[0] == 'v': return VV.get(key[1], 0.0)
    if key[0] == 'r': return RR.get(key[1], 0.0)
    if key[0] == 'V': return Vval(key[1])
    if key[0] == 'x': return X.get(key[1], 0.0)
    if key[0] == 'lq': return LQ.get(key[1], 0.0)
    if key[0] == 'fb': return FBV.get(key[1], 0.0)
    if key[0] == 'XQ': return XQeff(key[1])
    if key[0] == 'xo': return XOV.get(key[1], 0.0)
    if key[0] == 'lQ': return Qeff8(*key[1][1:]) if len(key[1]) == 4 else Qeff(*key[1])
    raise KeyError(key)

# ================= 12.3: senderR2 =================
W5 = sorted({canon(w) for w in itertools.product(LET, repeat=5)})
SENDERS = [w for w in W5 if not isR5(w) and max(w) >= 7]
print('sender words %d (spec 342)' % len(SENDERS))
if len(SENDERS) != 342: fail('sender count')
def sender_row(w, H_, F_):
    sixes = [k for k in range(5) if w[k] == 6]
    for k in sixes:
        if not any(not isR6((5, w[(k + 1) % 5], a, q, b, w[(k - 1) % 5]))
                   for a in CLS2[H_[k]] for q in CLS2[F_[k]] for b in CLS2[H_[(k - 1) % 5]]): return None
    r = collections.Counter()
    for j in range(5):
        if w[j] >= 7: r[('y', rootw(w, j))] += 1
    for k in sixes:
        r[('g', g2_raw(w[(k + 1) % 5], H_[k], F_[k], H_[(k - 1) % 5], w[(k - 1) % 5], ap(w[(k + 2) % 5]), ap(w[(k - 2) % 5])))] += 1
    if HAT5:   # section 15: every big hat k sends through the diamond: + r[K]
        Hl = [H_[m] for m in range(5)]; Fl = [F_.get(m) for m in range(5)]
        for k in range(5):
            if Hl[k] == 1: r[('r', key_sender(list(w), Hl, Fl, k))] += 1
    return r
nrows = nbad = 0; worst = 1e9; GSEND = set()
for w in SENDERS:
    sixes = [k for k in range(5) if w[k] == 6]; hats = list(range(5)) if HAT5 else sorted({m for k in sixes for m in (k, (k - 1) % 5)})
    seen = set()
    for hb in itertools.product((0, 1), repeat=len(hats)):
        for fb in itertools.product((0, 1), repeat=len(sixes)):
            H_ = dict(zip(hats, hb)); F_ = dict(zip(sixes, fb)); r = sender_row(w, H_, F_)
            if r is None: continue
            key = tuple(sorted(r.items()))
            if key in seen: continue
            seen.add(key); nrows += 1; GSEND.update(k[1] for k in r if k[0] == 'g')
            v = sum(cf * val(k) for k, cf in r.items()); worst = min(worst, v - (1 - T))
            if v < 1 - T - EPS: nbad += 1; nbad <= 5 and print('VIOLATED senderR2 %s H%s F%s: %.12f < %.12f' % (''.join(map(str, w)), H_, F_, v, 1 - T))
print('senderR2 rows %d (spec 7,074), violated %d, min slack %.3g; g2 keys in sender rows %d (spec 393)' % (nrows, nbad, worst, len(GSEND)), flush=True)
if nbad: fail('senderR2 violated')
if nrows != 7074 and not HAT5: fail('senderR2 row count differs from spec 12.3')
if HAT5: print('senderR2 rows with all five hat classes enumerated (section 15): %d (section 15 states no count)' % nrows)
if len(GSEND) != 393: print('WARN: %d g2 keys in sender rows, spec 12.3 says 393 (a descriptive count: neither a violation nor a rebuild mismatch; see README ambiguities)' % len(GSEND))

# ================= 12.4 / 12.7.2: cons2 over all non-R6 6-words x all apex class words =================
def cons2_row(L, s):
    r = collections.Counter()
    for i in range(6):
        if L[i] == 5:
            r[('g', g2_raw(L[(i + 1) % 6], c(L[(i + 2) % 6]), c(L[(i + 3) % 6]), c(L[(i + 4) % 6]), L[(i + 5) % 6], ap(s[i]), ap(s[(i - 1) % 6])))] += 1
        elif L[i] >= 7:
            m = tuple(L[(i + k) % 6] for k in range(6)); r[('h', h2_of(m, s[i], s[(i - 1) % 6]))] -= 1
            if V6 and L[i] == 7: r[('v', v_of(m, s[i], s[(i - 1) % 6]))] += 1
    if FB:   # 44.3: cons2 (L, s) of a 6 X: +1 for each k with L_k >= 7 and a face side
        Lf = lambda q: L[q % 6]; sf = lambda q: s[q % 6]
        for k in range(6):
            if L[k] >= 7:
                Tp, Tm = fb_payee_T(Lf, sf, k); key = fb_key(L[k], 6, Tp, Tm)
                if key: r[('fb', key)] += 1
    return {k: v for k, v in r.items() if v != 0}
ALL6 = sorted({canon(L) for L in itertools.product(LET, repeat=6) if not isR6(L)})
cres = {'five': [0, 0, 0.0], 'nofive': [0, 0, 0.0]}
for L in ALL6:
    sub = 'five' if 5 in L else 'nofive'; cres[sub][0] += 1
    for s in itertools.product(CV, repeat=6):
        v = sum(cf * val(k) for k, cf in cons2_row(L, s).items())
        cres[sub][2] = max(cres[sub][2], abs(v))
        if abs(v) > 1e-9: cres[sub][1] += 1; cres[sub][1] <= 5 and print('VIOLATED cons2 %s s %s: %.3g' % (''.join(map(str, L)), ''.join(map(str, s)), v))
print('cons2: %d non-R6 6-words (spec 1,424) x 729 cv class words (= all 5^6 apex words through cv and ap)' % len(ALL6))
for sub in ('five', 'nofive'):
    print('  %-7s %d words (%s): violated %d, max |sum g2 - sum h2| %.3g' % (sub, cres[sub][0], 'spec 994' if sub == 'five' else 'spec 430', cres[sub][1], cres[sub][2]), flush=True)
if len(ALL6) != 1424 or cres['five'][0] != 994: fail('6-word counts')
if FB and not os.environ.get('LOWER_ONLY') == '1':   # 44.3: fb6 inflow depends on exact apex letters: all 5^6 apex words
    fbbad = 0; fbmax = 0.0
    for L in ALL6:
        base = {}
        for s5 in itertools.product(LET, repeat=6):
            a5 = tuple(ap(x) for x in s5)
            if a5 not in base: base[a5] = sum(cf * val(k) for k, cf in cons2_row(L, a5).items() if k[0] != 'fb')
            v = base[a5] + sum(cf * val(k) for k, cf in cons2_row(L, s5).items() if k[0] == 'fb')
            fbmax = max(fbmax, abs(v))
            if abs(v) > 1e-9: fbbad += 1; fbbad <= 5 and print('VIOLATED cons2+fb %s s %s: %.3g' % (''.join(map(str, L)), ''.join(map(str, s5)), v))
    print('cons2 with fb over all 1,424 x 5^6 exact apex words: violated %d, max |sum| %.3g' % (fbbad, fbmax), flush=True)
    if fbbad: fail('cons2 with fb violated')
if cres['five'][1] or cres['nofive'][1]: fail('cons2 violated')
hcan = [k for k in H if k != min(k, (k[0], k[5], k[4], k[3], k[2], k[1], k[7], k[6]))]
gcan = [k for k in G if k != g2_raw(*k)]
if hcan or gcan: fail('%d h2 / %d g2 solution keys not canonical' % (len(hcan), len(gcan)))

# ================= spec 4.5: pattern loader and matcher =================
CH = {'.': None, '5': {5}, '6': {6}, '7': {7}, '8': {8}, 'B': {7, 8, 9}}
odd = collections.Counter()
def parse_name(nm):
    f = nm.split('_'); K, d = f[0][0], int(f[0][1:]); lk, sw = f[1], f[2]; P = []
    for kind, word in (('w', lk), ('s', sw)):
        for i, ch in enumerate(word):
            if K == 'p' and ((kind == 'w' and ch == '9') or (kind == 's' and ch == '0')): continue
            if ch not in CH: odd[ch] += 1; S = {int(ch)}   # not in spec 4.5's table; read as the exact letter
            else: S = CH[ch]
            if S is not None: P.append((kind, i, frozenset(S)))
    return d, frozenset(P)
PAT = collections.defaultdict(set); KIND = collections.Counter(); seenp = {'D': set(), 'C': set(), 'R': set()}
for a in ARGS:
    if a.startswith(('pat=', 'cpat=')):
        fn = a.split('=', 1)[1]; allf = fn.endswith(':all'); fn = fn[:-4] if allf else fn
        p = fn if os.path.isabs(fn) else os.path.join(HERE, fn)
        if not os.path.exists(p): print('missing pattern file (skipped as in the run): %s' % fn); continue
        lines = open(p).read().splitlines()
        if a.startswith('pat='):
            names = [l.split()[0] for l in lines if l.strip() and (allf or 'D=true' in l)]; kind = 'D'
        else:
            names = []; kind = 'C'
            for k, l in enumerate(lines):
                if ' r=' in l and not l.startswith(' '):
                    for l2 in lines[k + 1:]:
                        if ' r=' in l2 and not l2.startswith(' '): break
                        if 'C-REDUCIBLE' in l2: names.append(l.split()[0]); break
        for nm in names:
            if not re.match(r'^[epf]\d+_', nm): continue
            d, P = parse_name(nm)
            if (d, P) not in seenp[kind]: seenp[kind].add((d, P)); KIND[kind] += 1
            PAT[d].add(P)
    elif a.startswith('rpat='):
        fn = a[5:]; p = fn if os.path.isabs(fn) else os.path.join(HERE, fn)
        for line in open(p):
            f = line.split('#')[0].split()
            if not f: continue
            d, k = int(f[0]), int(f[1]); slots = {}
            for e in range(k):
                i, m = int(f[2 + 2 * e]), int(f[3 + 2 * e])
                for sl, S in ((('w', i), {5}),) + tuple(((nm_, (ix_ % d)), {LET[b] for b in range(5) if (m >> (5 * t_)) >> b & 1})
                                                        for t_, (nm_, ix_) in enumerate((('w', i + 1), ('s', i), ('s', i - 1), ('w', i - 1)))):
                    slots[sl] = slots.get(sl, set(LET)) & S
            P = frozenset((kd, ix_, frozenset(S)) for (kd, ix_), S in slots.items() if S != set(LET))
            if (d, P) not in seenp['R']: seenp['R'].add((d, P)); KIND['R'] += 1
            PAT[d].add(P)
RPATN = os.environ.get('RPATN')   # RELAY_SPEC_s39o 39.2: whole-window raw patterns 'd LINK SWORD', 5-8 exact, N = {6,7,8,9}, . free
NRPATN = collections.Counter(); FULLX = []
if RPATN:
    NSET = {'5': {5}, '6': {6}, '7': {7}, '8': {8}, 'N': {6, 7, 8, 9}}
    for line in open(RPATN):
        if line.startswith('#') or not line.strip(): continue
        f = line.split('#')[0].split(); d = int(f[0]); lk, sw = f[1], f[2]
        P = frozenset([('w', i, frozenset(NSET[ch])) for i, ch in enumerate(lk) if ch != '.'] + [('s', i, frozenset(NSET[ch])) for i, ch in enumerate(sw) if ch != '.'])
        PAT[d].add(P); NRPATN[d] += 1
        FULLX.append('%d %d %s' % (d, len(P), ' '.join('%d %d' % ((i if kd == 'w' else d + i), sum(1 << (x - 5) for x in S)) for kd, i, S in sorted(P))))
    print('rpatN patterns from %s: %d, by d %s' % (os.path.basename(RPATN), sum(NRPATN.values()), dict(sorted(NRPATN.items()))), flush=True)
byd = {d: len(v) for d, v in sorted(PAT.items())}
print('patterns distinct by kind: D %d (spec 15,497), C %d (spec 1,494), RPAT %d (spec 158); by d %s; chars outside the spec table %s'
      % (KIND['D'], KIND['C'], KIND['R'], byd, dict(odd)), flush=True)
if (KIND['D'], KIND['C'], KIND['R']) != EXPECT_PAT: fail('pattern counts %s differ from expected %s' % ((KIND['D'], KIND['C'], KIND['R']), EXPECT_PAT))
PATL = {d: [tuple(P) for P in v] for d, v in PAT.items()}
def patmatch(d, w, s):
    for P in PATL.get(d, ()):
        for r in range(d):
            for refl in (False, True):
                ok = True
                for kd, i, S in P:
                    if kd == 'w': x_ = w[(r - i) % d] if refl else w[(i + r) % d]
                    else: x_ = s[(r - i - 1) % d] if refl else s[(i + r) % d]
                    if x_ not in S: ok = False; break
                if ok: return True
    return False
def admissible(d, w, s):
    U = min(d, 9)
    for i in range(d):
        if w[i] == 5 and isR5((U, w[(i + 1) % d], s[i], s[(i - 1) % d], w[(i - 1) % d])): return False
        if w[i] == 6 and all(isR6((U, w[(i + 1) % d], s[i], p, s[(i - 1) % d], w[(i - 1) % d])) for p in LET): return False
    if d in (7, 8) and canon(w) in RBIG: return False
    return not patmatch(d, w, s)

# ================= 12.5: receiverR2 rows =================
def recv_spec(d, link, sword):
    U = min(d, 9); w = [int(ch) for ch in link]; s = [int(ch) for ch in sword]; r = collections.Counter()
    W = lambda k: w[k % d]; S = lambda k: s[k % d]
    for i in range(d):
        if HAT5 and s[i] == 5: r[('r', key_receiver(w, s, i))] += 1   # section 15: apex five s_i
        if w[i] == 5: r[('y', root5((U, W(i + 1), S(i), S(i - 1), W(i - 1))))] += 1
        elif w[i] == 6:
            mk = pmask(U, W(i - 2), W(i - 1), W(i + 1), W(i + 2), S(i - 2), S(i - 1), S(i), S(i + 1))
            sg = sig2_of(U, W(i + 1), S(i), S(i - 1), W(i - 1), ap(W(i + 2)), ap(W(i - 2))) + (mk,)
            if cand2(sg): r[('M', sg)] += 1
            if V6 and U == 7:
                sv_ = sigV_of(U, W(i + 1), S(i), S(i - 1), W(i - 1), cv(W(i + 2)), cv(W(i - 2))) + (mk,)
                if candV(sv_): r[('V', sv_)] -= 1
        elif XO:   # s51.3: one M-style credit per big position, no old x term
            qk = xo_q(U, W(i - 2), W(i - 1), w[i], W(i + 1), W(i + 2), S(i - 2), S(i - 1), S(i), S(i + 1))
            if qk: r[('XQ', qk)] += -1 if XOBROKEN == 'sign' else 1
        else:
            ti = tau(w[i], U, side(W(i - 1), S(i - 1), W(i - 2)), side(W(i + 1), S(i), W(i + 2)))
            to = tau(U, w[i], side(W(i - 1), W(i - 2), S(i - 1)), side(W(i + 1), W(i + 2), S(i)))
            r[('x', ti)] += 1; r[('x', to)] -= 1
    if FB:   # 44.3: payer (any d) -1 at w_j >= 6; fb7 payee +1 at w_k >= 7 when the centre is >= 7
        for j in range(d):
            if w[j] >= 6:
                Tp, Tm = fb_payer_T(W, S, j); key = fb_key(U, w[j], Tp, Tm)
                if key: r[('fb', key)] -= 1
            if w[j] >= 7 and U >= 7:
                Tp, Tm = fb_payee_T(W, S, j); key = fb_key(w[j], U, Tp, Tm)
                if key: r[('fb', key)] += 1
    if L3Q and d == 7:   # section 21.3: payer and payee terms at each link 7, both sides
        for i in range(d):
            if w[i] != 7: continue
            for sg_ in (1, -1):
                key = (W(i + sg_), W(i + 2 * sg_), W(i + 3 * sg_))
                if key[0] in (5, 6) and key[1] in (5, 6): r[('lq', key)] -= 1
                c_, a_, o_ = W(i + sg_), (S(i) if sg_ == 1 else S(i - 1)), (S(i - 1) if sg_ == 1 else S(i))
                if c_ in (5, 6) and a_ in (5, 6):
                    r[('lQ', (c_, a_, MASK[(sg_, c_, a_, W(i + 2 * sg_), W(i + 3 * sg_), W(i + 4 * sg_), o_)]))] += 1
    if L3Q8 and d == 7:   # s45.2 / s47.2: payer -lq[(8, c, a, a2)] at every link 8, both sides, c, a <= 6
        for i in range(d):
            if w[i] != 8: continue
            for sg_ in (1, -1):
                key = (8, W(i + sg_), W(i + 2 * sg_), W(i + 3 * sg_))
                if key[1] in (5, 6) and key[2] in (5, 6): r[('lq', key)] += 1 if BROKEN8 == 'payersign' else -1
    if L3Q8 and d == 8:   # s45.2 / s47.2: payee +lQ[(8, c, a, m)] at every link 7, both sides; indices mod 8 (w4 = antipode)
        for i in range(d):
            if w[i] != 7: continue
            for sg_ in (1, -1):
                c_, a_, o_ = W(i + sg_), (S(i) if sg_ == 1 else S(i - 1)), (S(i - 1) if sg_ == 1 else S(i))
                if BROKEN8 == 'apex': a_, o_ = o_, a_
                if c_ in (5, 6) and a_ in (5, 6):
                    r[('lQ', (8, c_, a_, MASK8[(sg_, c_, a_, W(i + 2 * sg_), W(i + 3 * sg_), W(i + 4 * sg_), o_)]))] += 1
    return {k: v for k, v in r.items() if v != 0}
def spec_val(d, lk, sv): return sum(cf * val(k) for k, cf in recv_spec(d, lk, sv).items())

# ================= 12.8: exact lower check =================
SKIP_LOWER = os.environ.get('SKIP_LOWER') == '1'
if SKIP_LOWER: CERT = []; print('lower check skipped (upper-only job)')
tot = collections.defaultdict(Fr); tco = Fr(0); Dn = Fr(0); nlab = collections.Counter(); noncanon = []
for e in CERT:
    w = Fr(e['w']) if isinstance(e['w'], str) or os.environ.get('WEXACT') == '1' else Fr(e['w']).limit_denominator(10 ** 7); lab = e['row']; kind = lab[0]; nlab[kind] += 1   # 44.8: 'p/q' weights exact
    if kind == 'senderR2':
        word = tuple(int(ch) for ch in lab[1]); bits = lab[2]; cut = bits.index('|')
        sixes = [k for k in range(5) if word[k] == 6]; hats = list(range(5)) if HAT5 else sorted({m for k in sixes for m in (k, (k - 1) % 5)})
        if word not in SENDERS or len(bits[:cut]) != len(hats) or len(bits[cut + 1:]) != len(sixes): fail('bad senderR2 label %s' % lab); continue
        r = sender_row(word, dict(zip(hats, bits[:cut])), dict(zip(sixes, bits[cut + 1:])))
        if r is None: fail('senderR2 assignment inadmissible %s' % lab); continue
        if w < 0: fail('senderR2 weight < 0 %s' % lab)
        tco += w; Dn += w
    elif kind == 'receiverR2':
        d, lk, sv = lab[1], lab[2], lab[3]
        if not admissible(d, [int(ch) for ch in lk], [int(ch) for ch in sv]): fail('receiverR2 label not admissible %s' % lab)
        r = recv_spec(d, lk, sv)
        if w > 0: fail('receiverR2 weight > 0 %s' % lab)
        tco -= w; Dn += w * (d - 6)
    elif kind == 'cons2':
        L, s = tuple(lab[1]), tuple(lab[2])
        if isR6(L) or not all(x in LET for x in L + s): fail('cons2 label not admissible %s' % lab)
        r = cons2_row(L, s)
    elif kind == 'mrowR2':
        sg, hk = tuple(lab[1]), tuple(lab[2])
        if sg[:7] != sig2_of(*sg[:7]): noncanon.append(lab)
        if hk not in cand2(sg): fail('mrowR2 key not in cand2 (stored orientation) %s' % lab)
        r = {('h', hk): 1, ('M', sg): -1}
        if w > 0: fail('mrowR2 weight > 0 %s' % lab)
    elif kind == 'mrowL':   # section 21.3: lq[(c, a, a2)] - lQ[(c, a, m)] <= 0 for a2 in m
        # label order (not fixed by section 21.3; the s33z certs use it): ['mrowL', [c, a, m] (lQ), [c, a, a2] (lq)]
        Qk, qk = tuple(lab[1]), tuple(lab[2])
        if len(Qk) == 4 and len(qk) == 4 and L3Q8 and Qk[0] == qk[0] == 8: Qs, qs = Qk[1:], qk[1:]   # s45.2: ['mrowL', [8, c, a, m], [8, c, a, a2]]
        elif len(Qk) == 3 and len(qk) == 3: Qs, qs = Qk, qk
        else: Qs, qs = (0, 0, 0), (1, 1, 5); fail('mrowL label of a family that is off or malformed %s' % lab)
        if not (qs[:2] == Qs[:2] and qs[0] in (5, 6) and qs[1] in (5, 6) and (Qs[2] >> (qs[2] - 5)) & 1): fail('mrowL label invalid %s' % lab)
        r = {('lq', qk): 1, ('lQ', Qk): -1}
        if w > 0: fail('mrowL weight > 0 %s' % lab)
    elif kind == 'mrowX':   # s51.6: xo[in] - xo[out] - XQ[q] <= 0, label ['mrowX', [U, V, A, B], [eA, eB]], w <= 0
        (U_, V_, A_, B_), (eA, eB) = lab[1], lab[2]; A_, B_ = tuple(A_), tuple(B_)
        okl = XO and U_ in (7, 8, 9) and V_ in (7, 8, 9) and all(len(T) == 5 and all(x in LET for x in T[:4]) and 1 <= T[4] <= 31 for T in (A_, B_)) \
              and A_ <= B_ and (A_[4] >> LI[eA]) & 1 and (B_[4] >> LI[eB]) & 1 if eA in LET and eB in LET else False
        if not okl: fail('mrowX label invalid %s' % lab); continue
        qk = (U_, V_, A_, B_); ia_, oa_ = xo_sides_in_out(A_, eA); ib_, ob_ = xo_sides_in_out(B_, eB)
        ti_, to_ = tauo(V_, U_, ia_, ib_), tauo(U_, V_, oa_, ob_)
        r = collections.Counter({('XQ', qk): -1}); r[('xo', ti_)] += 1; r[('xo', to_)] -= 1; r = {k: v for k, v in r.items() if v}
        if w > 0: fail('mrowX weight > 0 %s' % lab)
    elif kind == 'mrowV':
        sg, vk = tuple(lab[1]), tuple(lab[2])
        if sg != sigV_of(*sg): noncanon.append(lab)
        if vk not in candV(sg): fail('mrowV key not in candV %s' % lab)
        r = {('V', sg): 1, ('v', vk): -1}
        if w > 0: fail('mrowV weight > 0 %s' % lab)
    else:
        fail('unknown label %s' % lab); continue
    for k, cf in r.items(): tot[k] += w * cf
print('cert rows %d: %s; mrowR2/mrowV not in canonical orientation: %d %s' % (len(CERT), dict(nlab), len(noncanon), noncanon[:3]))
if noncanon: fail('%d mrowR2/mrowV rows not in canonical orientation' % len(noncanon))
if tco <= 0 and not SKIP_LOWER: fail('t coefficient %s <= 0' % tco)
D = Dn / tco if tco else Fr(0); rc = {k: -v / tco for k, v in tot.items() if v != 0}
for k, v in list(rc.items()):
    if k[0] == 'x' and v < 0: D += v * 3
    if k[0] == 'xo' and v < 0: D += v * XOCAP   # s51.6: xo at xcap
    if k[0] == 'XQ' and v != 0: D -= XOCAP * abs(v)   # s51.6: XQ in [-xcap, xcap] priced at its box
    if k[0] == 'lq' and v < 0: D += v * Fr(LQCAP).limit_denominator(1000)   # section 21.3: priced at its cap
if FB and FBCAP:
    for k, v in list(rc.items()):
        if k[0] == 'fb' and v < 0: D += v * Fr(FBCAP)
if L3Q8:   # s45.6: raw rc of every V = 8 column the rows touch, and the bundle rc(lq k) + sum of rc(lQ (8, c, a, m)) over cert-row keys with a2 in m
    _l8 = sorted((k[1], v) for k, v in rc.items() if k[0] == 'lq' and len(k[1]) == 4); _Q8 = sorted((k[1], v) for k, v in rc.items() if k[0] == 'lQ' and len(k[1]) == 4)
    _all8 = sorted({k[1] for k in tot if k[0] == 'lq' and len(k[1]) == 4}); _allQ8 = sorted({k[1] for k in tot if k[0] == 'lQ' and len(k[1]) == 4})
    print('l3qV8 lower: lq8 columns in rows %d, nonzero rc %s; lQ8 columns in rows %d, nonzero rc %s' % (len(_all8), _l8, len(_allQ8), _Q8), flush=True)
    for c_, a_, a2 in itertools.product((5, 6), (5, 6), LET):
        k_ = (8, c_, a_, a2); r_ = rc.get(('lq', k_), Fr(0)); b_ = r_ + sum(v for kk, v in _Q8 if kk[1:3] == (c_, a_) and (kk[3] >> (a2 - 5)) & 1)
        if r_ or b_: print('  lq%s raw rc %s, bundle rc %s' % (k_, r_, b_))
    if any(v < 0 for _, v in _Q8): print('l3qV8 lower: NEGATIVE lQ8 columns %s' % [kv for kv in _Q8 if kv[1] < 0])
FBNEG = sorted(((v, k[1]) for k, v in rc.items() if k[0] == 'fb' and v < 0))
if FB: print('fb columns with rc < 0: %d %s' % (len(FBNEG), ['%s rc=%s' % (''.join(map(str, kk[:2])) + ' ' + ''.join(map(str, kk[2:6])) + ' ' + ''.join(map(str, kk[6:])), vv) for vv, kk in FBNEG]), flush=True)
if XO:
    _xq = {k[1]: v for k, v in rc.items() if k[0] == 'XQ'}; _xon = sorted((v, k[1]) for k, v in rc.items() if k[0] == 'xo' and v < 0)
    print('xo lower: XQ columns with rc != 0: %d (box charge %s); xo columns rc < 0: %d (cap charge %s); mrowX rows %d' % (len(_xq), sum(XOCAP * abs(v) for v in _xq.values()),
          len(_xon), sum(-XOCAP * v for v, _ in _xon), nlab['mrowX']), flush=True)
    if os.environ.get('XOPRICE') == '1':   # first-order: d XQeff / d xo[t] at xo = 0 is max over candidates of [in = t] - [out = t]
        _fo = collections.defaultdict(Fr)
        for qk, v in _xq.items():
            cs = xo_cands(qk); ks = {i_ for _, _, i_, _ in cs} | {o_ for _, _, _, o_ in cs}
            for t_ in ks:
                dv = max((1 if i_ == t_ else 0) - (1 if o_ == t_ else 0) for _, _, i_, o_ in cs)
                if dv: _fo[t_] += v * dv
        if os.environ.get('XOPRICEMODE') in ('one', 'spread'):   # dual extension: mrowX duals mu_c <= 0 with sum mu_c = rc(XQ q) * tco, so rc(XQ q) = 0;
            _fo = collections.defaultdict(Fr)                   # rc(xo in_c) += -mu_c / tco, rc(xo out_c) += mu_c / tco ('one': all on the first (eA, eB); 'spread': equal)
            for qk, v in _xq.items():
                cs = xo_cands(qk); share = [(cs[0], Fr(1))] if os.environ['XOPRICEMODE'] == 'one' else [(c_, Fr(1, len(cs))) for c_ in cs]
                for (eA, eB, i_, o_), f_ in share:
                    if i_ != o_: _fo[i_] += v * f_; _fo[o_] -= v * f_
        if os.environ.get('XOPRICEMODE') == 'json':   # s51.3a: Opus's chosen spread (data file SPREADJSON), duals fed into Studio's own key formulas
            SJ = json.load(open(os.environ['SPREADJSON'])); _fo = collections.defaultdict(Fr); bad_q = bad_bal = bad_c = 0; nd = 0
            for ent in SJ['mrowX']:
                U_, V_, A_, B_ = ent['q']; qk = (U_, V_, tuple(A_), tuple(B_))
                ys = [(tuple(dd['cand']), Fr(dd['w'])) for dd in ent['duals']]
                if qk not in _xq and Fr(ent['sum_receiver_weight']) != 0: bad_q += 1
                # balance of the free column XQ[q]: my ledger tot[XQ q] (receiver rows) = sum of its mrowX duals (= the file's receiver sum)
                if -_xq.get(qk, Fr(0)) * tco != sum(y for _, y in ys) or Fr(ent['sum_receiver_weight']) != sum(y for _, y in ys): bad_bal += 1
                for (eA, eB), y in ys:
                    if y > 0 or not ((A_[4] >> LI[eA]) & 1 and (B_[4] >> LI[eB]) & 1): bad_c += 1; continue
                    ia_, oa_ = xo_sides_in_out(tuple(A_), eA); ib_, ob_ = xo_sides_in_out(tuple(B_), eB)
                    ti_, to_ = tauo(V_, U_, ia_, ib_), tauo(U_, V_, oa_, ob_); nd += 1
                    if ti_ != to_: _fo[ti_] -= y / tco; _fo[to_] += y / tco
            mine_q = [qk for qk, v in _xq.items() if v]; inj = {(e['q'][0], e['q'][1], tuple(e['q'][2]), tuple(e['q'][3])) for e in SJ['mrowX']}
            print('SPREADJSON %s: %d credit keys (Studio XQ ledger: %d nonzero, %d not in the file), %d duals; q not in Studio ledger %d, '
                  'XQ balance mismatches %d, bad candidates / signs %d' % (os.path.basename(os.environ['SPREADJSON']), len(SJ['mrowX']), len(mine_q),
                  len([q_ for q_ in mine_q if q_ not in inj]), nd, bad_q, bad_bal, bad_c), flush=True)
            for q_ in [q_ for q_ in mine_q if q_ not in inj]:
                cs = xo_cands(q_); print('  Studio-only credit key %s: rc %s, %d candidates, distinct (in, out) pairs %d' % (q_, _xq[q_], len(cs), len({(i_, o_) for _, _, i_, o_ in cs})))
            # rows: one mode each, alpha 1, completion weights a convex split of the row weight (same sign, summing to w per position)
            nm_ = sum(len(rw['modes']) != 1 for rw in SJ['rows']); split_bad = 0; npos = 0
            for rw in SJ['rows']:
                wr = Fr(rw['w'])
                for md in rw['modes']:
                    if Fr(md['alpha']) != 1: split_bad += 1
                    for ps in md['positions']:
                        npos += 1; ws = [Fr(cp['weight']) for cp in ps['completions']]
                        if sum(ws) != wr * Fr(md['alpha']) or any(x * wr < 0 for x in ws if x): split_bad += 1
            print('SPREADJSON rows: %d receiver rows, %d with more than one mode (relabel), %d positions, convex-split violations %d' % (len(SJ['rows']), nm_, npos, split_bad), flush=True)
            _negJ = {tuple([n[1][0], n[1][1], tuple(n[1][2]), tuple(n[1][3])]): Fr(n[0]) for n in SJ['neg']}
            _negS = {tauo_dec(t_): v for t_, v in _fo.items() if v < 0}
            print('SPREADJSON vs the file: stated S %s, nneg %s, min %s; negative keys equal (same rc): %s' % (SJ['S'], SJ['nneg'], SJ['minrc'], _negJ == _negS), flush=True)
        _neg = sorted((v, t_) for t_, v in _fo.items() if v < 0)
        print('XOPRICE first-order xo: %d keys with rc != 0; negative %d, sum max(0, -rc) = %s; most negative %s' % (len([1 for v in _fo.values() if v]), len(_neg), sum(-v for v, _ in _neg), _neg[0][0] if _neg else 0), flush=True)
        for v, t_ in _neg[:12]: print('  xo %s rc %s' % (tauo_dec(t_), v))
negrc = {k: v for k, v in rc.items() if k[0] not in ('x', 'lq', 'xo', 'XQ') and not (k[0] == 'fb' and FBCAP) and v < 0}
print('lower: tco = %s, D = %s; nonzero reduced costs: %s; negative (non-x) %d' % (
    tco, D, ', '.join('%s[%s] = %s' % (k[0], ''.join(map(str, k[1])) if isinstance(k[1], tuple) else k[1], v) for k, v in sorted(rc.items(), key=str)), len(negrc)))
if negrc: fail('negative reduced costs %s' % negrc)
if SKIP_LOWER: pass
elif os.environ.get('LOWER_TOL') and abs(D - EXPECT_T) <= Fr(os.environ['LOWER_TOL']): print('LOWER: D = %.15f (exact, denominator %d digits), within %s of the claimed %s' % (float(D), len(str(D.denominator)), os.environ['LOWER_TOL'], float(EXPECT_T))); print('LOWER: VALID t >= %s' % D) if not negrc else print('LOWER: NOT ESTABLISHED (negative reduced costs)')
elif D != EXPECT_T: fail('lower bound %s != claimed %s' % (D, EXPECT_T))
elif negrc: print('LOWER: NOT ESTABLISHED (D = %s but negative reduced costs)' % D)
else: print('LOWER: VALID t >= %s' % D)

if LOWER_ONLY:
    print('VERDICT (lower only): %s' % ('PASS (lower VALID %s)' % EXPECT_T if not FAIL else 'FAIL: ' + ' | '.join(FAIL))); sys.exit(0)
# ================= receivers: Studio sep3r on the apex relaxation, exact re-check of what it reports =================
os.environ['SEP_NODELIMIT'] = '0'
src = open(os.path.join(HERE, 'wlp3r6.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(HERE, 'wlp3r6.py')), 1)
sys.argv = ['wlp3r6', 'tag=s16chk', 'dmaxp=%s' % os.environ.get('DMAXP', '17')] + ARGS
NS_ = {'__name__': 'studio_wlp3r6'}
exec(src[:src.index('DS, DSF = list(range(7, 13))')], NS_)
import numpy as np
NY, ix, V56, V6B, I6B, recv_row, sepx, check, dp9, DMAXP = (NS_[k] for k in ('NY', 'ix', 'V56', 'V6B', 'I6B', 'recv_row', 'sepx', 'check', 'dp9', 'DMAXP'))
NS, TRI, states, BIGSTATE, best6, SEPX = (NS_[k] for k in ('NS', 'TRI', 'states', 'BIGSTATE', 'best6', 'SEPX'))
# results keyed by arrangement (bin/sep3r_ak, SEP_ARRKEY=1): under the apex relaxation two arrangements with one Studio
# row can differ in their exact value, so sep3r's row-keyed dedupe could hide an exact violator
SEPX.stdin.close(); SEPX.wait()
import subprocess as _sp
# exact six-window table for sep3r_ak's leaf correction (SEP_EXACT6): M[sig2 + mask] - (U = 7) V[sigV + mask], per spec
# 12.5 / 13.2 / 14', over the full window (w_{i-2}, w_{i-1}, w_{i+1}, w_{i+2}, s_{i-2}, s_{i-1}, s_i, s_{i+1}); the search
# still prunes on the relaxed bound, so it stays exhaustive, and only exact violators are reported
_EX = _np.zeros((3,) + (5,) * 8)
_mcM, _mcV = {}, {}   # separate caches: a sig2 and a sigV can be the same tuple
for _ui, _U in enumerate((7, 8, 9)):
    for _ix in itertools.product(range(5), repeat=8):
        wm2, wm1, wp1, wp2, sm2, sm1, s0, sp1 = (q + 5 for q in _ix)
        mk = pmask(_U, wm2, wm1, wp1, wp2, sm2, sm1, s0, sp1)
        sg = sig2_of(_U, wp1, s0, sm1, wm1, ap(wp2), ap(wm2)) + (mk,)
        if sg not in _mcM: _mcM[sg] = Mval(sg) if cand2(sg) else 0.0
        v_ = _mcM[sg]
        if V6 and _U == 7:
            sv_ = sigV_of(_U, wp1, s0, sm1, wm1, cv(wp2), cv(wm2)) + (mk,)
            if sv_ not in _mcV: _mcV[sv_] = Vval(sv_) if candV(sv_) else 0.0
            v_ -= _mcV[sv_]
        _EX[(_ui,) + _ix] = v_
EX6F = os.path.join(HERE, 'out', 'job31', 'st16', 'ex6_%s.bin' % os.path.basename(SOLF).replace('.json', ''))
_EX.astype('<f8').tofile(EX6F)
print('exact six-window table: %d entries written (%s); min %.6f, max %.6f' % (_EX.size, os.path.basename(EX6F), _EX.min(), _EX.max()), flush=True)
SEPX = _sp.Popen([os.path.join(HERE, 'bin', 'sep3r_ak'), NS_['SF']], stdin=_sp.PIPE, stdout=_sp.PIPE, text=True,
                 env=dict(os.environ, SEP_NODELIMIT='0', SEP_ARRKEY='1', SEP_EXACT6=EX6F))
NS_['SEPX'] = SEPX
yv = np.zeros(NY)
for k, v in Y.items(): yv[ix[k]] = v
V56[:] = 0.0; V6B[:] = 0.0
def Vlow(k6):   # the least v over the private and the cv apex pairs, for the 5-signature of this rooted 6-link
    U, a1, b1, _, d1, e1 = k6
    if U != 7 or not V6: return 0.0
    lst = [VV.get(v_of((U, a1, b1, p, d1, e1), ar, al), 0.0) for p in LET if not isR6((U, a1, b1, p, d1, e1)) for ar in CV for al in CV]
    return min(lst) if lst else 0.0
for k6, i6 in I6B.items():   # relaxation: the largest h2 over the apex pairs, minus (at a 7) the least possible V
    V6B[i6] = max(H.get(h2_of(k6, a, b), 0.0) for a in AP for b in AP) - Vlow(k6)
xv = dict(X)
def rrel(wm1, sm1, w0, wp1):
    return max(RR.get(key_receiver([wm1, w0, wp1, wp2], [sm1, 5, sp1, 5], 1), 0.0) for wp2 in LET for sp1 in LET)
RREL_ = _np.zeros((125, 25)); REX_ = _np.zeros(15625)
if HAT5:
    for wm1, sm1, w0, wp1 in itertools.product(LET, repeat=4):
        RREL_[(wm1 - 5) * 25 + (sm1 - 5) * 5 + (w0 - 5), wp1 - 5] = rrel(wm1, sm1, w0, wp1)
    for wm1, w0, wp1, wp2, sm1, sp1 in itertools.product(LET, repeat=6):
        REX_[(((((wm1 - 5) * 5 + w0 - 5) * 5 + wp1 - 5) * 5 + wp2 - 5) * 25) + (sm1 - 5) * 5 + sp1 - 5] = RR.get(key_receiver([wm1, w0, wp1, wp2], [sm1, 5, sp1, 5], 1), 0.0)
    RTF = os.path.join(HERE, 'out', 'job31', 'st16', 'rtab_%s.bin' % os.path.basename(SOLF).replace('.json', ''))
    with open(RTF, 'wb') as _f: _f.write(RREL_.astype('<f8').tobytes()); _f.write(REX_.astype('<f8').tobytes())
    SEPX.stdin.close(); SEPX.wait()
    SEPENV = dict(os.environ, SEP_NODELIMIT='0', SEP_ARRKEY='1', SEP_EXACT6=EX6F, SEP_RTAB=RTF)
    if RPATN:
        FXF = os.path.join(HERE, 'out', 'job31', 'st16', 'fullx_%s.txt' % os.path.basename(SOLF).replace('.json', ''))
        open(FXF, 'w').write('\n'.join(FULLX) + '\n'); SEPENV['SEP_FULLX'] = FXF
    if L3Q:   # section 21.6: relaxed window term at a d = 7 link 7, exact payee / payer terms at the leaf
        L3R = _np.zeros((125, 25)); L3X = _np.zeros(31250); L3P = _np.zeros(125)
        for wm1, sm1, s0, wp1 in itertools.product(LET, repeat=4):
            L3R[(wm1 - 5) * 25 + (sm1 - 5) * 5 + 2, (s0 - 5) * 5 + (wp1 - 5)] = UB(wp1, s0) + UB(wm1, sm1)
        for (sg_, c_, a_, w2_, w3_, w4_, o_), m_ in MASK.items():
            L3X[((((((0 if sg_ == 1 else 1) * 5 + c_ - 5) * 5 + a_ - 5) * 5 + w2_ - 5) * 5 + w3_ - 5) * 5 + w4_ - 5) * 5 + o_ - 5] = Qeff(c_, a_, m_)
        for k_, v_ in LQ.items():   # s47 R8: the V = 7 payer table PQ from 3-tuple keys only
            if len(k_) == 3: c_, a_, a2 = k_; L3P[((c_ - 5) * 5 + a_ - 5) * 5 + a2 - 5] = v_
        L3F = os.path.join(HERE, 'out', 'job31', 'st16', 'l3q_%s.bin' % os.path.basename(SOLF).replace('.json', ''))
        with open(L3F, 'wb') as _f: _f.write(L3R.astype('<f8').tobytes()); _f.write(L3X.astype('<f8').tobytes()); _f.write(L3P.astype('<f8').tobytes())
        SEPENV['SEP_L3Q'] = L3F
        print('l3q separator tables: relaxed max %.6f, exact payee max %.6f, payer max %.6f (%s)' % (L3R.max(), L3X.max(), L3P.max(), os.path.basename(L3F)), flush=True)
    if L3Q8:   # s47.3: relaxed UB8 window term at a d = 8 link 7, exact Qeff8 payee terms at the d = 8 leaf, payer q8 at a d = 7 link 8 (leaf)
        L8R = _np.zeros((125, 25)); L8X = _np.zeros(31250); L8P = _np.zeros(125)
        for wm1, sm1, s0, wp1 in itertools.product(LET, repeat=4):
            L8R[(wm1 - 5) * 25 + (sm1 - 5) * 5 + 2, (s0 - 5) * 5 + (wp1 - 5)] = UB8(wp1, s0) + UB8(wm1, sm1)
        for (sg_, c_, a_, w2_, w3_, w4_, o_), m_ in MASK8.items():
            if BROKEN8 == 'sep_payee0': continue   # broken separator control: no exact V = 8 payee credit
            L8X[((((((0 if sg_ == 1 else 1) * 5 + c_ - 5) * 5 + a_ - 5) * 5 + w2_ - 5) * 5 + w3_ - 5) * 5 + w4_ - 5) * 5 + o_ - 5] = Qeff8(c_, a_, m_)
        for k_, v_ in LQ.items():
            if len(k_) == 4 and k_[0] == 8: L8P[((k_[1] - 5) * 5 + k_[2] - 5) * 5 + k_[3] - 5] = -v_ if BROKEN8 in ('sep_payersign', 'payersign') else v_   # 'payersign': rows and separator both mis-signed (a consistent broken engine)
        L8F = os.path.join(HERE, 'out', 'job31', 'st16', 'l3q8_%s.bin' % os.path.basename(SOLF).replace('.json', ''))
        with open(L8F, 'wb') as _f: _f.write(L8R.astype('<f8').tobytes()); _f.write(L8X.astype('<f8').tobytes()); _f.write(L8P.astype('<f8').tobytes())
        SEPENV['SEP_L3Q8'] = L8F
        print('l3qV8 separator tables: relaxed max %.6f, exact payee max %.6f, payer max %.6f (%s)' % (L8R.max(), L8X.max(), L8P.max(), os.path.basename(L8F)), flush=True)
    if FB or XO:   # s44 window term: payer at c >= 6, fb7 payee at c >= 7 when U >= 7; exact table + relaxed max over (a, f, p, s)
        FBX_ = _np.zeros((3,) + (5,) * 9); FBREL_ = _np.full((3, 125, 25), 0.0)
        if XO:   # s51.5 (4)-(5): + XQeff at every big-centre window touched by a positive xo key (all others have XQeff = 0)
            _xw = set()
            for t_, v_ in XOV.items():
                if v_ > 0: _xw |= xo_windows_of(t_)
            for wnd in (_xw if XOBROKEN != 'sep0' else ()):   # 'sep0': broken separator control (no xo term in the window table)
                U_, a_, b_, c_, e_, f_, p_, q_, r_, s_ = wnd; v_ = XQeff(xo_q(*wnd)) * (-1 if XOBROKEN == 'sign' else 1)
                FBX_[U_ - 7, a_ - 5, b_ - 5, c_ - 5, e_ - 5, f_ - 5, p_ - 5, q_ - 5, r_ - 5, s_ - 5] += v_
            print('xo separator windows: %d touched by a positive xo key; XQeff min %.6f max %.6f' % (len(_xw), FBX_.min(), FBX_.max()), flush=True)
        for ui_, U_ in enumerate((7, 8, 9)):
            for a_, b_, c_, e_, f_, p_, q_, r_, s_ in (itertools.product(LET, repeat=9) if FB else ()):
                v_ = 0.0
                if c_ >= 6:
                    k_ = fb_key(U_, c_, (e_, r_, f_, s_ if e_ == 5 else 0), (b_, q_, a_, p_ if b_ == 5 else 0))
                    if k_: v_ -= FBV.get(k_, 0.0)
                if c_ >= 7 and U_ >= 7:
                    k_ = fb_key(c_, U_, (e_, f_, r_, s_ if e_ == 5 else 0), (b_, a_, q_, p_ if b_ == 5 else 0))
                    if k_: v_ += FBV.get(k_, 0.0)
                FBX_[ui_, a_ - 5, b_ - 5, c_ - 5, e_ - 5, f_ - 5, p_ - 5, q_ - 5, r_ - 5, s_ - 5] += v_
            # relaxed: state (b, q, c) and choice (r, e): max over a, f, p, s
            R_ = FBX_[ui_].max(axis=(0, 4, 5, 8))   # dims left: b, c, e, q, r
            for b_, c_, e_, q_, r_ in itertools.product(range(5), repeat=5):
                FBREL_[ui_, b_ * 25 + q_ * 5 + c_, r_ * 5 + e_] = R_[b_, c_, e_, q_, r_]
        FBF = os.path.join(HERE, 'out', 'job31', 'st16', 'fb_%s.bin' % os.path.basename(SOLF).replace('.json', ''))
        with open(FBF, 'wb') as _f: _f.write(FBREL_.astype('<f8').tobytes()); _f.write(FBX_.astype('<f8').tobytes())
        SEPENV['SEP_FB6'] = FBF
        print('fb separator tables: %d fb values; exact min %.6f max %.6f; relaxed max %.6f (%s)' % (len(FBV), FBX_.min(), FBX_.max(), FBREL_.max(), os.path.basename(FBF)), flush=True)
    SEPX = _sp.Popen([os.path.join(HERE, 'bin', 'sep3r_l3q' if L3Q else 'sep3r_ak'), NS_['SF']], stdin=_sp.PIPE, stdout=_sp.PIPE, text=True, env=SEPENV)
    NS_['SEPX'] = SEPX
    print('hat-channel tables: relaxed max %.6f, exact max %.6f (%s)' % (RREL_.max(), REX_.max(), os.path.basename(RTF)), flush=True)
def rrel_row(d, lk, sv):
    w = [int(c) for c in lk]; s_ = [int(c) for c in sv]
    return sum(RREL_[(w[(i - 1) % d] - 5) * 25 + (s_[(i - 1) % d] - 5) * 5 + w[i] - 5, w[(i + 1) % d] - 5] for i in range(d) if s_[i] == 5) if HAT5 else 0.0
def l3rel_row(d, lk, sv):
    w = [int(c) for c in lk]; s_ = [int(c) for c in sv]
    if L3Q8 and d == 8: return sum(UB8(w[(i + 1) % d], s_[i]) + UB8(w[(i - 1) % d], s_[(i - 1) % d]) for i in range(d) if w[i] == 7)
    if not (L3Q and d == 7): return 0.0
    return sum(UB(w[(i + 1) % d], s_[i]) + UB(w[(i - 1) % d], s_[(i - 1) % d]) for i in range(d) if w[i] == 7)
def fbrel_row(d, lk, sv):
    if not (FB or XO): return 0.0
    w = [int(c) for c in lk]; s_ = [int(c) for c in sv]; ui_ = min(d, 9) - 7
    return sum(FBREL_[ui_, (w[(i - 1) % d] - 5) * 25 + (s_[(i - 1) % d] - 5) * 5 + w[i] - 5, (s_[i] - 5) * 5 + w[(i + 1) % d] - 5] for i in range(d))
def studio_val(d, lk, sv):
    r_ = recv_row(d, lk, sv)
    return fbrel_row(d, lk, sv) + l3rel_row(d, lk, sv) + rrel_row(d, lk, sv) + sum(cf * (yv[k[1]] if k[0] == 'y' else xv.get(k[1], 0.0) if k[0] == 'x' else V6B[k[1]] if k[0] == 'y6b' else 0.0) for k, cf in r_.items() if k[0] != 't')
def xk(rr): return collections.Counter({k[1]: cf for k, cf in rr.items() if k[0] == 'x'})
tests = [(e['row'][1], e['row'][2], e['row'][3]) for e in CERT if e['row'][0] == 'receiverR2']
_devs = []
CALD = min(DMAXP, int(os.environ.get('CALD', str(DMAXP))))   # calibration degrees (a validation step only)
for d in range(7, CALD + 1):
    _o = sepx(d, yv, xv, -1e9, int(os.environ.get('CALN', '20')) if d == 7 else 20); tests += [(d, lk, sv) for _, lk, sv in _o]
    _devs += [abs(wq - spec_val(d, lk, sv)) for wq, lk, sv in _o]
    _nl3 = sum(1 for _, lk, sv in _o if any(k[0] in ('lq', 'lQ') for k in recv_spec(d, lk, sv)))
    print('  calibration d=%d: %d heaviest compared (%d with l3q terms), max |difference| %.3g' % (d, len(_o), _nl3, max([abs(wq - spec_val(d, lk, sv)) for wq, lk, sv in _o] + [0.0])), flush=True)
print('sep3r_ak exact leaf weights vs spec rows on the heaviest 20 per d (d = 7..%d): %d compared, max |difference| %.3g' % (CALD, len(_devs), max(_devs + [0.0])), flush=True)
if max(_devs + [0.0]) > 1e-9: fail('sep3r_ak exact leaf weights differ from the spec rows')
random.seed(7)
for d in (7, 8, 9, 10):
    for _ in range(150): tests.append((d, ''.join(random.choice('5666777889') for _ in range(d)), ''.join(random.choice('5566677889') for _ in range(d))))
adm_bad = low = xbad = ncmp = 0
for d, lk, sv in tests:
    a1 = admissible(d, [int(ch) for ch in lk], [int(ch) for ch in sv]); a2 = check(d, lk, sv)
    if a1 != a2: adm_bad += 1; adm_bad <= 5 and print('ADMISSIBILITY MISMATCH d=%d %s %s spec %s studio %s' % (d, lk, sv, a1, a2))
    if a1 and a2:
        ncmp += 1; v1, v2 = spec_val(d, lk, sv), studio_val(d, lk, sv)
        if v2 < v1 - 1e-12: low += 1; low <= 5 and print('RELAXATION BELOW EXACT d=%d %s %s spec %.12f studio %.12f' % (d, lk, sv, v1, v2))
        if not XO and xk(recv_spec(d, lk, sv)) != xk(recv_row(d, lk, sv)): xbad += 1   # under xo the old x keys are off (R8)
print('spec rows vs Studio relaxed rows: %d arrangements, admissibility mismatches %d; %d compared: relaxed below exact %d, x-key mismatches %d'
      % (len(tests), adm_bad, ncmp, low, xbad), flush=True)
if adm_bad or low or xbad: fail('Studio relaxed receiver rows are not an upper bound on the spec rows')
rbad = 0; CAP = int(os.environ.get('CAP', '5000')); import time as _tm
for d in range(7, DMAXP + 1):
    _t0 = _tm.time(); out = sepx(d, yv, xv, d - 6 + T + EPS, CAP)
    exact_bad = [(spec_val(d, lk, sv), lk, sv) for _, lk, sv in out if spec_val(d, lk, sv) > d - 6 + T + EPS]
    dev = max([abs(wq - spec_val(d, lk, sv)) for wq, lk, sv in out] + [0.0])
    if dev > 1e-9: fail('d=%d: sep3r_ak exact weight differs from the spec row by %.3g' % (d, dev))
    for v_, lk, sv in exact_bad[:5]: print('VIOLATED receiverR2 d=%d exact load %.12f link %s s %s' % (d, v_, lk, sv))
    full = len(out) < CAP
    if not full: fail('d=%d: relaxation reports >= %d arrangements; exact check incomplete' % (d, CAP))
    rbad += len(exact_bad)
    print('receivers d=%d: relaxation reports %d above threshold%s; exact violated %d (%.0fs)' % (d, len(out), '' if full else ' (CAP hit)', len(exact_bad), _tm.time() - _t0), flush=True)
z9 = max([v for tq, v in X.items() if (tq // 15625) % 3 == 2] + [0.0])
Mk = np.full((NS, NS), -np.inf)
for a_, b_, rr in TRI[9]:
    (wp, sp, wc), (_, sc, wn) = states[a_], states[b_]
    v_ = (yv[ix[rr]] if rr is not None else 0.0) + z9 * BIGSTATE[a_]
    if wc == 6: v_ += best6(9, wn, sc, sp, wp)[0]
    if HAT5 and sc == 5: v_ += RREL_[(wp - 5) * 25 + (sp - 5) * 5 + wc - 5, wn - 5]   # section 15 r at the apex five
    if FB or XO: v_ += FBREL_[2, (wp - 5) * 25 + (sp - 5) * 5 + wc - 5, (sc - 5) * 5 + wn - 5]   # s44 relaxed fb at U = 9
    Mk[a_, b_] = max(Mk[a_, b_], v_)
Pk = Mk.copy(); dpbad = 0
for k_ in range(2, 31):
    Pk = (Pk[:, :, None] + Mk[None, :, :]).max(axis=1)
    if k_ >= DMAXP + 1:
        v_ = np.diag(Pk).max()
        if v_ > k_ - 6 + T + EPS: dpbad += 1; print('DP d=%d relaxed closed-walk bound %.12f > %.12f (not decided)' % (k_, v_, k_ - 6 + T))
rbad += dpbad
print('DP d=%d..30 (Studio max-plus with the relaxed r, z9 = %.6f): %s' % (DMAXP + 1, z9, 'clean' if dpbad == 0 else '%d undecided' % dpbad))
n_ = NS; Dk = np.full((n_ + 1, n_), -np.inf); Dk[0, :] = 0.0
for k in range(1, n_ + 1): Dk[k] = (Dk[k - 1][:, None] + Mk).max(axis=0)
with np.errstate(invalid='ignore'):
    q = np.where(np.isfinite(Dk[n_]), np.min(np.where(np.isfinite(Dk[:n_]), (Dk[n_] - Dk[:n_]) / (n_ - np.arange(n_))[:, None], np.inf), axis=0), -np.inf)
lam = q.max(); d0 = (6 - T) / (1 - lam) if lam < 1 else float('inf')
print('Karp tail (apex relaxation): lambda = %.9f, covered for d >= %.3f (needs <= 31)' % (lam, d0))
if d0 > 31: rbad += 1
if rbad: fail('receiver side violated or undecided')
SEPX.stdin.close(); SEPX.wait()
print('UPPER: %s' % ('FEASIBLE at t = %.12f' % T if rbad == 0 and not [f for f in FAIL if 'violated' in f or 'bounds' in f or 'incomplete' in f] else 'NOT ESTABLISHED'))
print('VERDICT: %s' % (('PASS (upper FEASIBLE at %s; lower not checked)' if SKIP_LOWER else 'PASS (upper FEASIBLE, lower VALID %s)') % EXPECT_T if not FAIL else 'FAIL: ' + ' | '.join(FAIL)))
