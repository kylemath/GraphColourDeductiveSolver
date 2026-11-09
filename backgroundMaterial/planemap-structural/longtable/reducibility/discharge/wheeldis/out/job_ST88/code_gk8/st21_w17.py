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
# ---- W10 (swarm round 6, 4 Nov 2026): copy of the repo's out/job31/st21_check_f2b.py (md5 6f24b4a0) with three more
# column families, written from the spec text (RELAY_SPEC 15r for rr; RELAY_SPEC_s22 22.1 for z / zr; FINDINGS stage 14 +
# s67 FLAGS line for masked q7). Opt-in env flags; with all of them off the checker is the repo's (same rows, same binary).
#   HATRR=1  rr[K] >= 0 under the section-15 hat key K: sender row -rr[K] at each big hat, receiver load -rr[K] at each
#            apex five (b -> v). Needs HAT5. Folded into the existing hat tables as r - rr.
#   ZH=1     z[K] >= 0, K = zkey(n, hr, hl): sender row +z at each big spoke, receiver load +z at each link five (v -> b).
#   ZR=1     zr[K] >= 0 same key, coefficient -1 in both rows (b -> v). Needs ZH. With ZR on, z, zr, rr in [0, ZCAP].
#   Q7=1     q[K] >= 0, K = qkey(the paying 7's whole link read from a big neighbour B, reflection fixing B): the d = 7 row
#            of the payer A gets -q[K] for every big link position j (B = w_j); the row of B (any d) gets +Q at every link
#            7 (A = w_i), Q = max q over A's two hidden privates (p1 next to s_i, p2 next to s_{i-1}), completions whose
#            7-link is an RBIG wheel dropped.
#   Q7M=1    masks on p1 / p2 at d = 7 (V = 7 l3q table) and d = 8 (V = 8 table), and not f2b extra7, on a side only when
#            its c = w_{i+-1} and apex are in {5, 6}; d >= 9 unmasked. Needs Q7, F2B, L3Q, L3Q8.
#   Q7CAP=x  optional cap on q.   W10PLANT=rrflip|zdouble|q7flip|q7one|q7shift  planted errors (controls only, Python rows only).
# ---- W15 (swarm round 6, 5 Nov 2026): copy of W10's st21_w10.py (md5 fa40e97f). Changes: (1) KILLDIR may hold the
# Opus/Studio packed kill6_U{7,8,9}.npy (uint8 (5,)*8, bit b = letter 5+b killed) instead of kill_U*.npy (bool (5,)*9);
# kill6 is unpacked bit by bit, cross-checked against kill_U*.npy when both are present, md5s printed, and the killed-bit
# difference against the stock keep95p131 tables reported (patched298: U7 +298, U8/U9 +0). U8 is read from its own file
# (the stock code used KT[8] = KT[9]; identical on every stack seen). (2) defaults /tmp/swarm-W15/wd and st16.
# (3) W15PLANT=q7coef (one q value doubled in the rows) and q7flip (payer sign) for the planted-error controls.
# ---- W17 (swarm round 6, 5 Nov 2026): copy of W15's st21_w15.py (md5 fb148493). Adds K* and the generic EDGE(7->P) family
# (module ksfam.py, written from Team D's family statement and W6's grammar.py; no Opus code). Opt-in:
#   KS=1          K* = K1 EDGE(7->7)[S.L+1=B S.L-1=S S.L-2=5 S.L-3=5 S.A-1=B];   EGK=<keys file>  one 'NAME EDGE(7->P)[...]' per line.
#   Amounts: SOL['ks'] = [[NAME, value], ...] (or a dict); KSAMT='NAME=v,...' overrides (controls). Values in [0, KSCAP=3].
#   Rows: d = 7 payer -(SURE count) per key; payee +(POSSIBLE count) at every d whose centre letter is in P (exact masks).
#   Separator: SEP_KS table (window bound at each link 7, exact leaf in sep3r_w17); DP / Karp tail: the U = 9 window bound.
#   KSA10=amask|grammar: the 6-private of S.A+-1 at d >= 10 (amask as the engine's M term, default; 'grammar' = free as certpics).
#   W17PLANT=kspayflip|kspayeehalf (Python rows), SEP_KSPLANT=pay|half (C++ leaf): planted errors for the controls.
#   W17ST=1 (default with KS/EGK): KS self-test (C++ 'e' vs Python rows, planted arrangements) and window-bound check.
#   W17GRAM=N: orientation test against grammar.py on N arrangements per d (7, 8), then exit.  KSDUMP=in.tsv KSDUMP_OUT=out.tsv: row dump.
# ---- W17 round 4 (code_gk, 6 Nov 2026): W6's generic 2-ball keys (module gkfam.py, from KEYSPEC.md and the gkwin paragraph of
# DUAL_EXPORT.md; no Opus code). GK=<keys file> (one 'NAME EDGE(U->V)[POS=SYM ...]' per line; K* = KS, A1, C1, E1 are rows of it,
# so GK excludes KS=1 / EGK). Amounts SOL['ks'] (KSAMT overrides). Rows: sender OUT(sure) - IN(possible), cons2 (c6le or equality)
# IN - OUT on the class picture, receiver d = 7 IN - OUT on the KEYSPEC section 5 picture, receiver d >= 8 the gkwin IN bound;
# mrow rows have no key terms. Separator bin/sep3r_gk (SEP_GK): GKREL window bound at every link position, exact leaf; DP / Karp
# tail: GKREL at U = 9. GKST=1 (default with GK): C++ leaf vs Python rows, window-table checks. GKORACLE=N: W6's r9_rows.py oracle.
# ---- code_gk8 (W17, 9 Nov 2026, from W6b's PAYER8SPEC.md, W5 reading; no Opus code): GK keys may have payer exactly {8} or {9}
# (gkfam refuses mixed sets and S.L+-3 for them). Window rows (d >= 8): the gkwin payer gate is {5..9} and the centre's OUT slots
# (payer-8 keys at U = 8, payer-9 keys at U = 9) are subtracted on the same window, so GKREL / GKW / the DP tail may be negative.
# GKORACLE (W6's round-9 r9_rows.py) predates payer 8/9 and is not updated.
import sys, os, json, re, itertools, collections, random
from fractions import Fraction as Fr
HERE = os.environ.get('W10_HERE', '/tmp/swarm-W17/wd')
ST16 = os.environ.get('W10_ST16', '/tmp/swarm-W17/st16')
W10TAG = os.environ.get('SEPTAG', 'x') + '_' + os.path.basename(sys.argv[1]).replace('.json', '')
DIS = os.path.dirname(HERE)
SOLF, CERTF, ARGF = sys.argv[1], sys.argv[2], sys.argv[3]
SOL = json.load(open(SOLF)); CERT = json.load(open(CERTF)); ARGS = open(ARGF).read().split()
EPS = float(os.environ.get('EPS', '1e-9')); FAIL = []   # f2b041e: EPS overridable; TEXACT / SEPEPS below
V6 = os.environ.get('V6', '1') == '1'
HAT5 = os.environ.get('HAT5', '1') == '1'
# ---- W10 families (see the header) ----
HATRR = os.environ.get('HATRR', '0') == '1'; ZH = os.environ.get('ZH', '0') == '1'; ZR = os.environ.get('ZR', '0') == '1'
ZCAP = float(os.environ.get('ZCAP', '3')); Q7 = os.environ.get('Q7', '0') == '1'; Q7M = os.environ.get('Q7M', '0') == '1'
Q7CAP = float(os.environ['Q7CAP']) if os.environ.get('Q7CAP') else None; W10PLANT = os.environ.get('W10PLANT', '')
# W17 round 5 (SPEC f2b7, 6 Nov): F2B7=1 also masks q7m sides whose common neighbour c or apex is >= 7 (31 & ~extra7); needs Q7M and F2B.
# W17PLANT7=q7side (Python-only planted error) / W17PLANT_SEP7=off (separator without SEP_F2B7): controls that must FAIL.
F2B7 = os.environ.get('F2B7', '0') == '1'; W17PLANT7 = os.environ.get('W17PLANT7', '')
W10ON = HATRR or ZH or Q7
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
if os.environ.get('CKEEP'):   # s52c cover check (Opus's reading, coordinator 15:53Z): C wheels out of R5 / R6 (and RBIG below) unless kept
    _ck = {l.split()[0] for l in open(os.environ['CKEEP']) if l.strip() and not l.startswith('#')}; _dr = []
    R5, R6 = set(), set()
    for line in open(os.path.join(DIS, 'studio17', 'wheels17_verdicts.txt')):
        f = line.split()
        if not f or f[0].startswith('#'): continue
        fam, word = f[0].split('_', 1); v = f[2]
        keepC = v == 'C' and word not in UNC and fam == 'c6' and f[0] in _ck   # only the kept C 6-wheels; every c5 C dropped
        if v == 'D' or keepC: (R5 if fam == 'c5' else R6).add(canon(tuple(int(ch) for ch in word)))
        elif v == 'C' and word not in UNC: _dr.append(f[0])
    print('CKEEP: R5 = c5 D only (%d), R6 = c6 D + kept C 6-wheels (%d); C wheels dropped: %s' % (len(R5), len(R6), _dr), flush=True)
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
for fn in ([] if os.environ.get('CKEEP') else glob.glob(os.path.join(HERE, 'out', 'def_*.cfast'))):   # CKEEP: RBIG = D big wheels only
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
if os.environ.get('CKEEP'): print('CKEEP: RBIG = D big wheels only: %d (spec 104 with C)' % len(RBIG), flush=True)
elif s2(R5) != set(SPEC_R5) or s2(R6) != set(SPEC_R6) or len(FANS) != 7 or len(RBIG) != 104: fail('reducible sets differ from spec 4.4')

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
import hashlib as _hl
_KSTOCK = os.environ.get('KILLSTOCK', os.path.join(os.path.dirname(HERE), 'wd', 'loop', 'studio', 'opus_check', 'f2b041', 'keep95p131', 'tab', 'kill'))
def _kill_load(dr, U):   # W15: kill6 (packed, Opus/Studio KILL7 format) preferred; kill_U (bool) cross-checked when both exist
    f6, fb = os.path.join(dr, 'kill6_U%d.npy' % U), os.path.join(dr, 'kill_U%d.npy' % U)
    if os.path.exists(f6):
        A = _np.load(f6)
        if A.shape != (5,) * 8 or A.dtype != _np.uint8 or int(A.max()) >= 32: raise SystemExit('kill6 table %s has shape %s dtype %s max %d' % (f6, A.shape, A.dtype, A.max()))
        K = _np.zeros((5,) * 9, dtype=bool)
        for b_ in range(5): K[..., b_] = ((A >> b_) & 1).astype(bool)
        if os.path.exists(fb) and not (_np.load(fb) == K).all(): raise SystemExit('kill6 and kill_U tables disagree in %s (U%d)' % (dr, U))
        return K, 'kill6_U%d md5 %s' % (U, _hl.md5(open(f6, 'rb').read()).hexdigest())
    return _np.load(fb).astype(bool), 'kill_U%d md5 %s' % (U, _hl.md5(open(fb, 'rb').read()).hexdigest())
KT = {}
for _U in (7, 8, 9):
    KT[_U], _km = _kill_load(KILLDIR, _U)
    _ks = _kill_load(_KSTOCK, _U)[0] if os.path.isdir(_KSTOCK) else None
    print('kill table U%d: %s, %d killed (window, p)%s' % (_U, _km, int(KT[_U].sum()), '' if _ks is None else '; vs stock keep95p131: +%d new, -%d removed' % (int((KT[_U] & ~_ks).sum()), int((_ks & ~KT[_U]).sum()))), flush=True)
print('section 14 prime kill tables from %s (U8 == U9: %s)' % (KILLDIR, bool((KT[8] == KT[9]).all())), flush=True)
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
    for _ws in os.environ['XODBG'].split(';'):
        if _ws.startswith('row '):   # 'row d link sword': every big position of that receiver
            _, d_, lk_, sv_ = _ws.split(); d_ = int(d_); w_ = [int(x) for x in lk_]; s_ = [int(x) for x in sv_]; U_ = min(d_, 9)
            Wd = lambda k: w_[k % d_]; Sd = lambda k: s_[k % d_]
            for i_ in range(d_):
                if w_[i_] >= 7:
                    wnd = (U_, Wd(i_ - 2), Wd(i_ - 1), w_[i_], Wd(i_ + 1), Wd(i_ + 2), Sd(i_ - 2), Sd(i_ - 1), Sd(i_), Sd(i_ + 1))
                    Ap, Am = xo_window_sides(*wnd); qk = xo_q(*wnd); cs = xo_cands((U_, w_[i_], min(Ap, Am), max(Ap, Am))) if Ap[4] and Am[4] else []
                    print('XODBG row %s %s %s i=%d: masks (%d, %d), candidates %d, with in != out %d -> %s' % (d_, lk_, sv_, i_, Ap[4], Am[4], len(cs),
                          sum(i2 != o2 for _, _, i2, o2 in cs), ('+XQ%s' % (qk,)) if qk else 'no term'))
            continue
        _w = tuple(int(x) for x in _ws.split()); print('XODBG sides', xo_window_sides(*_w), 'q', xo_q(*_w))
    if os.environ.get('XOSCAN'):   # every big-centre window at the given U: reasons for 'no term' (R6)
        import random as _rs; _rs.seed(1); cnt = collections.Counter(); ex = {}
        U_ = int(os.environ['XOSCAN'])
        for _ in range(int(os.environ.get('XOSCANN', '200000'))):
            wnd = (U_, _rs.choice(LET), _rs.choice(LET), _rs.choice((7, 8, 9))) + tuple(_rs.choice(LET) for _ in range(6))
            Ap, Am = xo_window_sides(*wnd)
            if not (Ap[4] and Am[4]): why = 'mask 0'
            else:
                cs = xo_cands((U_, wnd[3], min(Ap, Am), max(Ap, Am)))
                why = 'all in = out' if all(i2 == o2 for _, _, i2, o2 in cs) else 'term'
            assert (why == 'term') == bool(xo_q(*wnd)), wnd
            cnt[why] += 1; ex.setdefault(why, wnd)
        print('XOSCAN U=%d: %s; examples %s' % (U_, dict(cnt), ex))
    if os.environ.get('XOZERO'):   # exhaustive: c = 6 visible sides with an empty domain mask, and the window gets no term
        nz = 0; tot_ = 0; ex0 = None
        for U_, c_ in itertools.product((7, 8, 9), (7, 8, 9)):
            for b_, f_, q_, r_, s_ in itertools.product(LET, repeat=5):
                tot_ += 1; wnd = (U_, 5, b_, c_, 6, f_, 5, q_, r_, s_)
                Ap, Am = xo_window_sides(*wnd)
                if Ap[4] == 0:
                    nz += 1; ex0 = ex0 or wnd
                    assert xo_q(*wnd) is None, wnd
        print('XOZERO: %d + side (c = 6) visible combinations, %d with mask 0 (each gives no term); example %s' % (tot_, nz, ex0))
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
if SOL.get('model') != 'R6x2' or not SOL.get('apexcls') or (SOL.get('zh') and not ZH) or bool(SOL.get('v6')) != V6: fail('solution mode differs from V6=%d (model/apexcls/zh/v6)' % V6)
print('v values %d; r values %d; sol hat5 %s' % (len(VV), len(RR), SOL.get('hat5')))
if bool(SOL.get('hat5')) != HAT5: fail('solution hat5 flag differs from HAT5=%d' % HAT5)
# ================= W10: rr, z / zr, q7 values, flag consistency and bounds =================
if HATRR and not HAT5: fail('HATRR needs HAT5')
if ZR and not ZH: fail('ZR needs ZH')
if ZH and not HAT5: fail('ZH is implemented only with HAT5 (every hat class enumerated on sender rows)')
if Q7M and not (Q7 and os.environ.get('F2B') and L3Q and L3Q8): fail('Q7M needs Q7, F2B, L3Q and L3Q8')
def _fam(name):
    v = SOL.get(name, [])
    if isinstance(v, (int, float)): return {}   # older files store a scalar under 'z'; never a column family
    return {tuple(k): float(x) for k, x in v}
RRR = _fam('rr'); ZV = _fam('z'); ZRV = _fam('zr'); QV = _fam('q')
for nm_, D_, on_ in (('rr', RRR, HATRR), ('z', ZV, ZH), ('zr', ZRV, ZR), ('q', QV, Q7)):
    if D_ and not on_: fail('solution has %s values but that family is off' % nm_)
if Q7 and bool(SOL.get('q7m', False)) != Q7M: fail('solution q7m flag %s differs from Q7M=%d' % (SOL.get('q7m'), Q7M))
if F2B7 and not (Q7M and os.environ.get('F2B')): fail('F2B7 needs Q7M and F2B')
if 'f2b7' in SOL and bool(SOL['f2b7']) != F2B7: fail('solution f2b7 flag %s differs from F2B7=%d' % (SOL.get('f2b7'), F2B7))
print('W17 f2b7: F2B7=%d; solution f2b7 field %s%s' % (F2B7, SOL.get('f2b7', '(absent)'), (' PLANTED %s' % W17PLANT7) if W17PLANT7 else ''), flush=True)
_cap = ZCAP if ZR else float('inf')
_bb = [(nm_, k, v) for nm_, D_ in (('rr', RRR), ('z', ZV), ('zr', ZRV)) for k, v in D_.items() if v < -1e-15 or v > _cap + 1e-9]
_bb += [('q', k, v) for k, v in QV.items() if v < -1e-15 or (Q7CAP is not None and v > Q7CAP + 1e-9)]
print('W10 families: hatrr %s zh %s zr %s (cap %s) q7 %s q7m %s (q7cap %s); values rr %d (sum %.6g), z %d (sum %.6g), zr %d (sum %.6g), q %d (sum %.6g); out of bounds %d%s' % (
    HATRR, ZH, ZR, _cap, Q7, Q7M, Q7CAP, len(RRR), sum(RRR.values()), len(ZV), sum(ZV.values()), len(ZRV), sum(ZRV.values()), len(QV), sum(QV.values()), len(_bb),
    (' PLANTED ERROR %s' % W10PLANT) if W10PLANT else ''), flush=True)
if _bb: fail('W10 family values out of bounds %s' % _bb[:3])
def zkey(n, hr, hl):   # RELAY_SPEC_s22 22.1: n = (B, n1, n2, n3, n4) = the five's link read from the big; hr, hl hat classes
    a = tuple(n) + (hr, hl); b = (n[0], n[4], n[3], n[2], n[1], hl, hr)
    if W10PLANT == 'zswap': a, b = tuple(n) + (hl, hr), (n[0], n[4], n[3], n[2], n[1], hr, hl)
    return min(a, b)
def _q7one_key():   # W15 plant q7one: the most valuable q key among the payer keys of the three W5 links (7665557, 7555667, 7575566)
    if os.environ.get('W15QKEY'): return tuple(int(x) for x in os.environ['W15QKEY'].split(','))
    ks = {qkey(tuple(L_[(j + m) % 7] for m in range(7))) for L_ in ((7, 6, 6, 5, 5, 5, 7), (7, 5, 5, 5, 6, 6, 7), (7, 5, 7, 5, 5, 6, 6)) for j in range(7) if L_[j] >= 7}
    return max(ks, key=lambda k: (QV.get(k, 0.0), k))
def qkey(m):           # FINDINGS stage 14: the 7's whole link read from B (first letter), canonical under the reflection fixing B
    m = tuple(m); return min(m, (m[0],) + tuple(reversed(m[1:])))
_Q7C = {}
def q7cands(sig):      # sig = (U, a, b, c, e, m1, m2): every key of A's link (U, a, b, p1, p2, c, e), p1 in m1, p2 in m2, not RBIG
    if sig not in _Q7C:
        U, a, b, c_, e, m1, m2 = sig
        _Q7C[sig] = sorted({qkey((U, a, b, p1, p2, c_, e)) for p1 in LET if (m1 >> (p1 - 5)) & 1 for p2 in LET if (m2 >> (p2 - 5)) & 1
                            if canon((U, a, b, p1, p2, c_, e)) not in RBIG})
    return _Q7C[sig]
def q7sig(U, a, b, c_, e, m1, m2): return min((U, a, b, c_, e, m1, m2), (U, e, c_, b, a, m2, m1))
def Q7eff(sig): return max([QV.get(k, 0.0) for k in q7cands(sig)] + [0.0])
if os.environ.get('W17Q7RAND'):   # W17 round 5, self-test runs only: every q key gets a random value, so a changed mask changes the row
    _rq7 = random.Random(int(os.environ['W17Q7RAND'])); QV = {}
    for _t7 in itertools.product((7, 8, 9), LET, LET, LET, LET, LET, LET):
        _k7 = qkey(_t7)
        if _k7 not in QV: QV[_k7] = _rq7.uniform(0.0005, 0.02)
    print('TEST MODE W17Q7RAND=%s: %d q keys set to random values in (0.0005, 0.02)' % (os.environ['W17Q7RAND'], len(QV)), flush=True)
    fail('TEST MODE W17Q7RAND: q values replaced (self-test run, not a check of the solution)')
if os.environ.get('W17QPLANT'):   # W17 round 5 control: 'k1k2..k7:delta,...' raises q[qkey(k)] by delta (both engines)
    for _pl in os.environ['W17QPLANT'].split(','):
        _kk, _dd = _pl.split(':'); _k7 = qkey(tuple(int(ch) for ch in _kk)); _o7 = QV.get(_k7, 0.0); QV[_k7] = _o7 + float(_dd)
        print('PLANTED ERROR W17QPLANT: q%s %.9g -> %.9g' % (''.join(map(str, _k7)), _o7, QV[_k7]), flush=True)
ZDOUBLE_KEY = tuple(int(x) for x in os.environ['W10ZKEY'].split(',')) if os.environ.get('W10ZKEY') else (max(ZV, key=ZV.get) if ZV else None)
LOWER_ONLY = os.environ.get('LOWER_ONLY') == '1'
NOCLAMP = os.environ.get('NOCLAMP') == '1'   # W15: positive f2b leaf deltas allowed, made safe by a pruning slack (see the f2b tables block)
Q7ONE_KEY = _q7one_key() if W10PLANT == 'q7one' else None
# ================= W17: K* / EDGE(7->P) =================
import ksfam as KF
KSON = os.environ.get('KS', '0') == '1'; EGKF = os.environ.get('EGK', ''); W17PLANT = os.environ.get('W17PLANT', '')
KSKEYS = KF.load_keys(KSON, EGKF) if (KSON or EGKF) else []
KSCAP = float(os.environ.get('KSCAP', '3'))
_ksraw = SOL.get('ks') or []
KSV = {str(k_): float(v_) for k_, v_ in (_ksraw.items() if isinstance(_ksraw, dict) else _ksraw)}
if os.environ.get('KSAMT'):
    for _t in os.environ['KSAMT'].split(','):
        if _t.strip(): _n, _v = _t.split('='); KSV[_n.strip()] = float(_v)
    print('KSAMT override: ks amounts now %s' % KSV, flush=True)
# ---- W17 round 4: generic 2-ball keys ----
import gkfam as GKF, hashlib as _hlg
GKFILE = os.environ.get('GK', '')
GKKEYS = GKF.load_keys(GKFILE) if GKFILE else []
GKENG = GKF.Engine(GKKEYS) if GKKEYS else None
GKWIN = GKF.Win(GKENG, lambda *a_: pmask(*a_)) if GKKEYS else None
_ksnames = [k_[0] for k_ in KSKEYS] + [k_[0] for k_ in GKKEYS]
_ksoff = {n_: v_ for n_, v_ in KSV.items() if n_ not in _ksnames and v_ != 0.0}
if _ksoff: fail('solution has ks values for families that are off or unknown: %s' % _ksoff)
_ksbad = {n_: v_ for n_, v_ in KSV.items() if not (0.0 <= v_ <= KSCAP + 1e-12)}
if _ksbad: fail('ks amounts out of [0, %s]: %s' % (KSCAP, _ksbad))
if KSKEYS:
    if not (L3Q and os.environ.get('F2B')): fail('KS / EGK need L3Q (the 7-private table) and F2B (the f2b extras)')
    print('W17 families: %d keys, a10 %s: %s; amounts %s%s' % (len(KSKEYS), os.environ.get('KSA10', 'amask'), ' | '.join(KF.key_str(k_) for k_ in KSKEYS),
          {n_: KSV.get(n_, 0.0) for n_ in _ksnames}, (' PLANTED ERROR %s' % W17PLANT) if W17PLANT else ''), flush=True)
_KSMEMO = {}
def _ksx(d_, w_, s_, i_, g_):   # memoised f2b extras (pure functions of the arrangement)
    k_ = (d_, tuple(w_), tuple(s_), i_, g_)
    if k_ not in _KSMEMO:
        if len(_KSMEMO) > 400000: _KSMEMO.clear()
        _KSMEMO[k_] = f2b_extra(d_, w_, s_, i_, g_, True)
    return _KSMEMO[k_]
KSCTX = KF.Ctx(l3t=lambda sg_, c_, a_, w2_, w3_, w4_, o_: MASK[(sg_, c_, a_, w2_, w3_, w4_, o_)],
               amask=lambda *a_: pmask(*a_),
               extra7=lambda d_, w_, s_, j_, sg_: _ksx(d_, w_, s_, j_, ('w7', 7, sg_)) if F2BR else 0,
               extra6=lambda d_, w_, s_, k_: _ksx(d_, w_, s_, k_, ('w6', d_)) if (F2BR and d_ <= 9) else 0,
               a10=os.environ.get('KSA10', 'amask'))
if GKKEYS:
    if KSKEYS: fail('GK together with KS / EGK: K* and the EDGE keys are rows of the GK list (one column each)')
    if not (L3Q and os.environ.get('F2B') and HAT5): fail('GK needs L3Q (the l3q MASK table), F2B (the f2b extras) and HAT5 (sender apex classes)')
    _gkp = collections.Counter('%s->%s' % (GKF.msym(k_[1]), GKF.msym(k_[2])) for k_ in GKKEYS)
    _gknz = {k_[0]: KSV[k_[0]] for k_ in GKKEYS if KSV.get(k_[0], 0.0) != 0.0}
    print('W17 GK keys: %d from %s (md5 %s); payer->payee %s; nonzero amounts %d (sum %.9g)%s' % (len(GKKEYS), GKFILE, _hlg.md5(open(GKFILE, 'rb').read()).hexdigest()[:8],
          dict(sorted(_gkp.items())), len(_gknz), sum(_gknz.values()), (' PLANTED ERROR %s' % W17PLANT) if W17PLANT else ''), flush=True)
    print('W17 GK amounts: %s' % ' '.join('%s=%.12g' % kv for kv in _gknz.items()), flush=True)
def gk_send_terms(w, H_, F_):   # sender row: OUT (sure) - IN (possible)
    o_, i_ = GKENG.pic_counts(GKF.sender_pic(list(w), [H_[k] for k in range(5)], [F_.get(k, 0) for k in range(5)]))
    out = collections.Counter()
    for n_, c_ in o_.items(): out[('ks', n_)] += c_
    for n_, c_ in i_.items(): out[('ks', n_)] -= c_
    return {k_: v_ for k_, v_ in out.items() if v_}
_GKCMEMO = {}
def gk_cons_terms(L, s):   # cons2 row: IN (possible) - OUT (sure) on the class picture (apex S if <= 6, B if >= 7)
    ck = (tuple(L), tuple(x >= 7 for x in s)); r = _GKCMEMO.get(ck)
    if r is None:
        o_, i_ = GKENG.pic_counts(GKF.cons2_pic(list(L), list(s)))
        r = {('ks', n_): i_[n_] - o_[n_] for n_ in set(o_) | set(i_) if i_[n_] != o_[n_]}; _GKCMEMO[ck] = r
    return r
def gk_recv_terms(d, w, s):   # receiver: d = 7 IN - OUT on the KEYSPEC picture; d >= 8 the gkwin IN bound minus the window OUT (code_gk8)
    out = collections.Counter(); w = list(w); s = list(s)
    if d == 7:
        P = GKF.recv7_pic(w, s, pmask, MASK, lambda k_: _ksx(7, w, s, k_, ('w6', 7)) if F2BR else 0, lambda k_, f_: _ksx(7, w, s, k_, ('w7', 7, f_)) if F2BR else 0)
        o_, i_ = GKENG.pic_counts(P)
        for n_, c_ in i_.items(): out[('ks', n_)] += 0.5 * c_ if W17PLANT == 'gkpayeehalf' else c_
        for n_, c_ in o_.items(): out[('ks', n_)] += c_ if W17PLANT == 'gkpayflip' else -c_
    else:
        for n_, c_ in GKWIN.row(d, w, s).items(): out[('ks', n_)] += c_
    return out
def gk_window_tables():
    """numpy gkwin, independent of gkfam.Win: [U = 7, 8, 9] x (w_{j-2}, w_{j-1}, w_j, w_{j+1}, w_{j+2}, s_{j-2}, s_{j-1}, s_j, s_{j+1}),
    the amount-weighted IN credit of the link position j (keys with amount > 0)"""
    sh = (5,) * 9; one = _np.uint8(1)
    wm2, wm1, w0, wp1, wp2, sm2, sm1, s0, sp1 = [_np.arange(5, dtype=_np.uint8).reshape([5 if a_ == i_ else 1 for a_ in range(9)]) for i_ in range(9)]
    bt = lambda a_: _np.broadcast_to(_np.left_shift(one, a_), sh)
    out = _np.zeros((3,) + sh); keys = [(k_, KSV.get(k_[0], 0.0)) for k_ in GKKEYS if KSV.get(k_[0], 0.0) > 0]
    for ui, U in enumerate((7, 8, 9)):
        PMb = ((~KT[U]).astype(_np.uint8) << _np.arange(5, dtype=_np.uint8)).sum(axis=-1).astype(_np.uint8)   # pmask over (w-2, w-1, w+1, w+2, s-2, s-1, s0, s+1)
        P6 = _np.broadcast_to(PMb[:, :, None], sh)
        ORP = _np.broadcast_to(_np.bitwise_or.reduce(_np.bitwise_or.reduce(PMb, axis=7), axis=3)[None, :, :, None, :, None, :, :, :], sh)   # 6 at j+1: OR over w_{j+3}, s_{j+2}
        ORM = _np.broadcast_to(_np.bitwise_or.reduce(_np.bitwise_or.reduce(PMb, axis=4), axis=0)[:, None, :, :, None, :, :, :, None], sh)   # 6 at j-1: OR over w_{j-3}, s_{j-3}
        pvp = _np.where(w0 == 0, bt(sm1), _np.where(w0 == 1, P6, _np.uint8(31)))   # priv(j, +1): a 5 -> s_{j-1}
        pvm = _np.where(w0 == 0, bt(s0), _np.where(w0 == 1, P6, _np.uint8(31)))    # priv(j, -1): a 5 -> s_j
        fp = _np.where(wp1 == 0, bt(sp1), _np.where(wp1 == 1, ORP, _np.uint8(31)))  # priv(j+1, -1)
        fm = _np.where(wm1 == 0, bt(sm2), _np.where(wm1 == 1, ORM, _np.uint8(31)))  # priv(j-1, +1)
        vp = {0: bt(wp1), 1: bt(s0), 2: pvp, 3: bt(wm1), 4: bt(sm1), 5: pvm, 6: fp, 7: fm, 8: bt(wp2), 10: bt(wm2)}
        vm = {0: bt(wm1), 1: bt(sm1), 2: pvm, 3: bt(wp1), 4: bt(s0), 5: pvp, 6: fm, 7: fp, 8: bt(wm2), 10: bt(wp2)}
        # code_gk8 (PAYER8SPEC 3.1): OUT vectors of the centre U -> w_j on the same window (S.L+-3 wildcard = 31), used at U >= 8 only
        op = {0: bt(wp1), 1: bt(wp2), 2: _np.uint8(31), 3: bt(wm1), 4: bt(wm2), 5: _np.uint8(31), 6: bt(sp1), 7: bt(sm2), 8: bt(s0), 10: bt(sm1)}
        om = {0: bt(wm1), 1: bt(wm2), 2: _np.uint8(31), 3: bt(wp1), 4: bt(wp2), 5: _np.uint8(31), 6: bt(sm2), 7: bt(sp1), 8: bt(sm1), 10: bt(s0)}
        acc = _np.zeros(sh)
        for (n_, Uk, Vk, cd), a_ in keys:
            if (Vk >> (U - 5)) & 1:   # IN: payer w_j (any letter 5..9; code_gk8 gate {5..9}), payee the centre U, POSSIBLE
                pay = _np.broadcast_to((_np.left_shift(one, w0) & _np.uint8(Uk)) != 0, sh)
                for vec in (vp, vm):
                    ok = pay.copy()
                    for p_, m_ in cd: ok &= (vec[p_] & _np.uint8(m_)) != 0
                    acc += a_ * ok
            if U >= 8 and not (_np.uint8(1 << (U - 5)) & ~_np.uint8(Uk)):   # OUT (code_gk8): the centre U pays w_j, SURE (payer {8} at U = 8, {9} at U = 9)
                pyee = _np.broadcast_to((_np.left_shift(one, w0) & ~_np.uint8(Vk)) == 0, sh)
                for vec in (op, om):
                    ok = pyee.copy()
                    for p_, m_ in cd: ok &= (_np.broadcast_to(vec[p_], sh) & ~_np.uint8(m_)) == 0
                    acc -= a_ * ok
        out[ui] = acc
    return out
def ks_terms(d, w, s):
    """('ks', NAME) -> coefficient: - SURE payer count (d = 7) + POSSIBLE payee count"""
    out = collections.Counter()
    if not KSKEYS: return out
    for n_, c_ in KF.payer_counts(KSKEYS, w, s).items(): out[('ks', n_)] += c_ if W17PLANT == 'kspayflip' else -c_
    for n_, c_ in KF.payee_counts(KSCTX, KSKEYS, w, s).items(): out[('ks', n_)] += 0.5 * c_ if W17PLANT == 'kspayeehalf' else c_
    return out
if Q7ONE_KEY: print('PLANTED ERROR q7one: payer coefficient of q%s (value %s) flipped to +1' % (Q7ONE_KEY, QV.get(Q7ONE_KEY)), flush=True)
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
    if key[0] == 'rr': return RRR.get(key[1], 0.0)
    if key[0] == 'z': return ZV.get(key[1], 0.0)
    if key[0] == 'zr': return ZRV.get(key[1], 0.0)
    if key[0] == 'q': return QV.get(key[1], 0.0)
    if key[0] == 'Q7': return Q7eff(key[1])
    if key[0] == 'V': return Vval(key[1])
    if key[0] == 'x': return X.get(key[1], 0.0)
    if key[0] == 'lq': return LQ.get(key[1], 0.0)
    if key[0] == 'fb': return FBV.get(key[1], 0.0)
    if key[0] == 'XQ': return XQeff(key[1])
    if key[0] == 'xo': return XOV.get(key[1], 0.0)
    if key[0] == 'lQ': return Qeff8(*key[1][1:]) if len(key[1]) == 4 else Qeff(*key[1])
    if key[0] == 'ks': return KSV.get(key[1], 0.0)
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
            if Hl[k] == 1 and HATRR: r[('rr', key_sender(list(w), Hl, Fl, k))] += 1 if W10PLANT == 'rrflip' else -1   # 15r: v gains rr
    if ZH:   # s22 22.1: at each big spoke j, n = (w_j, .., w_{j+4}), hr = H[j], hl = H[j-1]
        for j in range(5):
            if w[j] >= 7:
                zk = zkey(tuple(w[(j + m) % 5] for m in range(5)), H_[j], H_[(j - 1) % 5]); r[('z', zk)] += 1
                if ZR: r[('zr', zk)] -= 1
    if GKKEYS:   # W17 round 4
        for k_, cf_ in gk_send_terms(w, H_, F_).items(): r[k_] += cf_
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
TEXACT = Fr(os.environ['TEXACT']) if os.environ.get('TEXACT') else None
if TEXACT is not None:   # f2b041e: every sender row in exact rationals (the solution's floats read as exact binary fractions) at t = TEXACT
    _xs = []; _nf = 0
    for w in SENDERS:
        sixes = [k for k in range(5) if w[k] == 6]; hats = list(range(5)) if HAT5 else sorted({m for k in sixes for m in (k, (k - 1) % 5)}); seen = set()
        for hb in itertools.product((0, 1), repeat=len(hats)):
            for fb in itertools.product((0, 1), repeat=len(sixes)):
                H_ = dict(zip(hats, hb)); F_ = dict(zip(sixes, fb)); r = sender_row(w, H_, F_)
                if r is None: continue
                key = tuple(sorted(r.items()))
                if key in seen: continue
                seen.add(key); vf = sum(cf * val(k) for k, cf in r.items())
                if vf - (1 - T) < 1e-9: _nf += 1
                _xs.append((sum(cf * Fr(val(k)) for k, cf in r.items()) - (1 - TEXACT), ''.join(map(str, w)), H_, F_))
    _xs.sort(key=lambda z: z[0]); _neg = [z for z in _xs if z[0] < 0]
    print('TEXACT %s: senderR2 %d rows in exact rationals: float slack < 1e-9 in %d rows; exact min slack %s (= %.6g); exact violated %d' % (TEXACT, len(_xs), _nf, _xs[0][0], float(_xs[0][0]), len(_neg)), flush=True)
    for z in _xs[:3]: print('   tightest sender row %s H%s F%s exact slack %.6g' % (z[1], z[2], z[3], float(z[0])))
    if _neg: fail('senderR2 violated in exact rationals at t = %s' % TEXACT)
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
    if GKKEYS:   # W17 round 4
        for k_, cf_ in gk_cons_terms(L, s).items(): r[k_] += cf_
    return {k: v for k, v in r.items() if v != 0}
ALL6 = sorted({canon(L) for L in itertools.product(LET, repeat=6) if not isR6(L)})
# W17 round 2 (code_c6): C6LE=1 = Opus's c6le (s83): a 6 starts at 0 and ends at 0 + in - out, and discharging only needs that to be
# <= t, so each cons2 row (same enumeration) is checked as in - out - t <= 0 instead of the equation |in - out| <= 1e-9.
C6LE = os.environ.get('C6LE') == '1'
cres = {'five': [0, 0, -float('inf') if C6LE else 0.0], 'nofive': [0, 0, -float('inf') if C6LE else 0.0]}
C6S = {'rows': 0, 'neg': 0, 'negL': 0, 'pos': 0, 'tight': 0, 'vmin': float('inf'), 'vmax': -float('inf'), 'argmin': None, 'argmax': None}
for L in ALL6:
    sub = 'five' if 5 in L else 'nofive'; cres[sub][0] += 1; _negL = False
    for s in itertools.product(CV, repeat=6):
        v = sum(cf * val(k) for k, cf in cons2_row(L, s).items())   # = in - out, the 6's final charge
        C6S['rows'] += 1
        if v < C6S['vmin']: C6S['vmin'] = v; C6S['argmin'] = (L, s)
        if v > C6S['vmax']: C6S['vmax'] = v; C6S['argmax'] = (L, s)
        if v < -1e-9: C6S['neg'] += 1; _negL = True
        if v > 1e-9: C6S['pos'] += 1
        if abs(v - T) <= 1e-9: C6S['tight'] += 1
        bad = (v - T > 1e-9) if C6LE else (abs(v) > 1e-9)
        cres[sub][2] = max(cres[sub][2], (v - T) if C6LE else abs(v))
        if bad: cres[sub][1] += 1; cres[sub][1] <= 5 and print('VIOLATED cons2%s %s s %s: in - out %.6g%s' % (' (c6le)' if C6LE else '', ''.join(map(str, L)), ''.join(map(str, s)), v, ', t %.6g' % T if C6LE else ''))
    C6S['negL'] += _negL
if C6LE: print('cons2 (c6le: the 6 ends <= t, in - out - t <= 0): %d non-R6 6-words (spec 1,424) x 729 cv class words (= all 5^6 apex words through cv and ap)' % len(ALL6))
else: print('cons2: %d non-R6 6-words (spec 1,424) x 729 cv class words (= all 5^6 apex words through cv and ap)' % len(ALL6))
for sub in ('five', 'nofive'):
    if C6LE: print('  %-7s %d words (%s): violated (in - out > t + 1e-9) %d, worst (in - out - t) %.6g' % (sub, cres[sub][0], 'spec 994' if sub == 'five' else 'spec 430', cres[sub][1], cres[sub][2]), flush=True)
    else: print('  %-7s %d words (%s): violated %d, max |sum g2 - sum h2| %.3g' % (sub, cres[sub][0], 'spec 994' if sub == 'five' else 'spec 430', cres[sub][1], cres[sub][2]), flush=True)
_fw = lambda a: '%s/%s' % (''.join(map(str, a[0])), ''.join(map(str, a[1]))) if a else '-'
print('cons2 6-balance (%s mode) over %d rows (6-word x class word): in - out min %.6g (%s), max %.6g (%s); rows with in - out < -1e-9 (the 6 ends below 0) %d in %d of %d words; rows > 1e-9 %d; rows within 1e-9 of t = %.9f (tight under c6le) %d'
      % ('c6le' if C6LE else 'equality', C6S['rows'], C6S['vmin'], _fw(C6S['argmin']), C6S['vmax'], _fw(C6S['argmax']), C6S['neg'], C6S['negL'], len(ALL6), C6S['pos'], T, C6S['tight']), flush=True)
if len(ALL6) != 1424 or cres['five'][0] != 994: fail('6-word counts')
if FB and not os.environ.get('LOWER_ONLY') == '1':   # 44.3: fb6 inflow depends on exact apex letters: all 5^6 apex words
    fbbad = 0; fbmax = 0.0
    for L in ALL6:
        base = {}
        for s5 in itertools.product(LET, repeat=6):
            a5 = tuple(ap(x) for x in s5)
            if a5 not in base: base[a5] = sum(cf * val(k) for k, cf in cons2_row(L, a5).items() if k[0] != 'fb')
            v = base[a5] + sum(cf * val(k) for k, cf in cons2_row(L, s5).items() if k[0] == 'fb')
            fbmax = max(fbmax, (v - T) if C6LE else abs(v))
            if ((v - T > 1e-9) if C6LE else (abs(v) > 1e-9)): fbbad += 1; fbbad <= 5 and print('VIOLATED cons2+fb %s s %s: %.3g' % (''.join(map(str, L)), ''.join(map(str, s5)), v))
    print('cons2 with fb over all 1,424 x 5^6 exact apex words: violated %d, max |sum| %.3g' % (fbbad, fbmax), flush=True)
    if fbbad: fail('cons2 with fb violated')
if cres['five'][1] or cres['nofive'][1]: fail('cons2 violated')
if os.environ.get('C6_ONLY') == '1':   # code_c6 controls: stop after the cons2 step
    print('CONS2 STEP (%s): %s' % ('c6le' if C6LE else 'equality', 'FAIL' if (cres['five'][1] or cres['nofive'][1]) else 'PASS'))
    print('VERDICT (C6_ONLY, checks up to cons2): %s' % ('PASS' if not FAIL else 'FAIL: ' + ' | '.join(FAIL))); sys.exit(0)
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
# W17: EXNAME=<file> = the exname hold-out list (one name per line, '#' comments): C entries (cpat=) with these names are dropped,
# D entries are kept (as Team D's log 'exname: N names held out; M C entries dropped').  Off (empty) by default.
EXNF = os.environ.get('EXNAME', ''); EXN = set(); EXDROP = collections.Counter()
if EXNF: EXN = {l.split()[0] for l in open(EXNF) if l.strip() and not l.startswith('#')}
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
            if EXN: EXDROP[fn] += sum(1 for nm in names if nm in EXN); names = [nm for nm in names if nm not in EXN]
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
if EXNF: print('exname: %d names held out (%s); %d C entries dropped, by file %s' % (len(EXN), EXNF, sum(EXDROP.values()), dict(sorted((k, v) for k, v in EXDROP.items() if v))), flush=True)
if EXNF and sum(EXDROP.values()): fail('exname: %d held-out C entries are in the args; the Studio separator builder (wlp3) has no exname, so its pattern set '
                                   'would keep them: filter the cfast files with code/exname_filter17.py and use those args' % sum(EXDROP.values()))
byd = {d: len(v) for d, v in sorted(PAT.items())}
print('patterns distinct by kind: D %d (spec 15,497), C %d (spec 1,494), RPAT %d (spec 158); by d %s; chars outside the spec table %s'
      % (KIND['D'], KIND['C'], KIND['R'], byd, dict(odd)), flush=True)
if (KIND['D'], KIND['C'], KIND['R']) != EXPECT_PAT: fail('pattern counts %s differ from expected %s' % ((KIND['D'], KIND['C'], KIND['R']), EXPECT_PAT))
PATL = {d: [tuple(P) for P in v] for d, v in PAT.items()}
ATTR = collections.defaultdict(list)   # f2b041 job 2: C patterns of ATTR_ARGS (the full args) that are not in this run's PAT
def _pm1(d, w, s, P):
    for r in range(d):
        for refl in (False, True):
            ok = True
            for kd, i, S in P:
                if kd == 'w': x_ = w[(r - i) % d] if refl else w[(i + r) % d]
                else: x_ = s[(r - i - 1) % d] if refl else s[(i + r) % d]
                if x_ not in S: ok = False; break
            if ok: return True
    return False
if os.environ.get('ATTR_ARGS'):
    for a in open(os.environ['ATTR_ARGS']).read().split():
        if not a.startswith('cpat='): continue
        fn = a[5:]; p = fn if os.path.isabs(fn) else os.path.join(HERE, fn)
        if not os.path.exists(p): continue
        lines = open(p).read().splitlines()
        for k, l in enumerate(lines):
            if ' r=' in l and not l.startswith(' '):
                for l2 in lines[k + 1:]:
                    if ' r=' in l2 and not l2.startswith(' '): break
                    if 'C-REDUCIBLE' in l2:
                        nm = l.split()[0]
                        if re.match(r'^[epf]\d+_', nm):
                            d_, P_ = parse_name(nm)
                            if P_ not in PAT[d_] and nm not in [x for x, _ in ATTR[d_]]: ATTR[d_].append((nm, P_))
                        break
    print('ATTR_ARGS: %d dropped C patterns by d %s' % (sum(len(v) for v in ATTR.values()), {k: len(v) for k, v in sorted(ATTR.items())}), flush=True)
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

# ================= f2b041 (Studio, 31 Oct): full-2-ball private-letter shrink, rules JSON as data =================
# A rule (p, w_req, s_req) at position i of a d-row kills letter p (mask bit p - 5) when every w_req (offset, allowed letters)
# and every s_req (offset, value) holds, offsets mod d from i. Groups: w6 rules shrink the 14' private mask of the link 6 at
# i (d = 7, 8, 9: groups d7_w6 / d8_w6 / d9_w6); w7 rules shrink the l3q payee mask at a link 7 (d = 7: V7 table, d = 8: V8
# table), per side (+1 / -1). F2B=<rules json> turns it on; F2BHALF=0|1 keeps only the even / odd rules of each group (control).
F2BR = os.environ.get('F2B'); F2BHALF = os.environ.get('F2BHALF'); F2BON = [bool(F2BR)]
F2BG = {}
if F2BR:
    if V6 or FB: fail('F2B is built only for V6=0, FB=0')   # f2b041e: XO=1 allowed (the xo window term is independent of the f2b leaf delta)
    _RJ = json.load(open(F2BR))
    def _f2c(rl, d_):
        out_ = []
        for n_, (p_, wq_, sq_) in enumerate(rl):
            if F2BHALF is not None and n_ % 2 != int(F2BHALF): continue
            fw_ = fs_ = 0
            for o_, al_ in wq_:
                for l_ in LET:
                    if l_ not in al_: fw_ |= 1 << (5 * (o_ % d_) + l_ - 5)
            for o_, v_ in sq_:
                for l_ in LET:
                    if l_ != v_: fs_ |= 1 << (5 * (o_ % d_) + l_ - 5)
            out_.append((fw_, fs_, 1 << (int(p_) - 5)))
        return out_
    F2BG = {('w6', 7): _f2c(_RJ['d7_w6'], 7), ('w6', 8): _f2c(_RJ['d8_w6'], 8), ('w6', 9): _f2c(_RJ['d9_w6'], 9),
            ('w7', 7, 1): _f2c(_RJ['d7_w7']['1'], 7), ('w7', 7, -1): _f2c(_RJ['d7_w7']['-1'], 7),
            ('w7', 8, 1): _f2c(_RJ['d8_w7']['1'], 8), ('w7', 8, -1): _f2c(_RJ['d8_w7']['-1'], 8)}
    print('F2B rules %s (half %s): %s' % (F2BR, F2BHALF, {k: len(v) for k, v in F2BG.items()}), flush=True)
def f2b_extra(d, w, s, i, g, always=False):   # W10: always=True for the q7m mask (part of the q7 row, not of the f2b leaf delta the 'f' self-test compares)
    if not F2BON[0] and not always: return 0
    rw = rs = 0
    for o_ in range(d): rw |= 1 << (5 * o_ + w[(i + o_) % d] - 5); rs |= 1 << (5 * o_ + s[(i + o_) % d] - 5)
    e_ = 0
    for fw_, fs_, m_ in F2BG[g]:
        if not (rw & fw_ or rs & fs_): e_ |= m_
    return e_
def q7masks(d, w, s, i, f2b7=None):   # q7m masks (m_+1, m_-1) of the link 7 at w[i]; W17 round 5: F2B7=1 (SPEC f2b7 section 1) masks a 7-side
    if f2b7 is None: f2b7 = F2B7          # (c >= 7 or apex >= 7) with 31 & ~extra7 instead of 31; c, apex <= 6 sides unchanged
    if not (Q7M and d in (7, 8)): return 31, 31
    W = lambda k: w[k % d]; S = lambda k: s[k % d]; ms = []
    for sg_ in (1, -1):
        c_, a_, o_ = W(i + sg_), (S(i) if sg_ == 1 else S(i - 1)), (S(i - 1) if sg_ == 1 else S(i))
        if c_ in (5, 6) and a_ in (5, 6):
            m_ = (MASK if d == 7 else MASK8)[(sg_, c_, a_, W(i + 2 * sg_), W(i + 3 * sg_), W(i + 4 * sg_), o_)]
            if F2BR: m_ &= ~f2b_extra(d, w, s, i, ('w7', d, sg_), True)
            ms.append(m_)
        elif f2b7:
            m_ = 31 & ~f2b_extra(d, w, s, i, ('w7', d, sg_), True)
            if W17PLANT7 == 'q7side' and m_ != 31: m_ = 31   # planted Python-only error (control): the 7-side mask dropped again
            ms.append(m_)
        else: ms.append(31)
    return ms[0], ms[1]
# ================= 12.5: receiverR2 rows =================
def recv_spec(d, link, sword):
    U = min(d, 9); w = [int(ch) for ch in link]; s = [int(ch) for ch in sword]; r = collections.Counter()
    W = lambda k: w[k % d]; S = lambda k: s[k % d]
    for i in range(d):
        if HAT5 and s[i] == 5: r[('r', key_receiver(w, s, i))] += 1   # section 15: apex five s_i
        if HAT5 and HATRR and s[i] == 5: r[('rr', key_receiver(w, s, i))] += 1 if W10PLANT == 'rrflip' else -1   # 15r: b pays rr
        if ZH and w[i] == 5:   # s22 22.1: n = (B, w_{i+1}, s_i, s_{i-1}, w_{i-1}), hr = c2(w_{i+2}), hl = c2(w_{i-2})
            zk = zkey((U, W(i + 1), S(i), S(i - 1), W(i - 1)), c(W(i + 2)), c(W(i - 2)))
            r[('z', zk)] += 2 if (W10PLANT == 'zdouble' and zk == ZDOUBLE_KEY) else 1
            if ZR: r[('zr', zk)] -= 1
        if Q7 and w[i] == 7:   # q7 payee B (this centre): + Q over A = w_i's hidden privates
            m1, m2 = q7masks(d, w, s, i)
            sg7 = q7sig(U, W(i + 1), S(i), S(i - 1), W(i - 1), m1, m2)
            if q7cands(sg7): r[('Q7', sg7)] += 1
        if w[i] == 5: r[('y', root5((U, W(i + 1), S(i), S(i - 1), W(i - 1))))] += 1
        elif w[i] == 6:
            mk = pmask(U, W(i - 2), W(i - 1), W(i + 1), W(i + 2), S(i - 2), S(i - 1), S(i), S(i + 1))
            if F2BR and d <= 9: mk &= ~f2b_extra(d, w, s, i, ('w6', d))   # f2b041
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
    if Q7 and d == 7:   # q7 payer A (this centre, d = 7): - q[K] for each big neighbour B = w_j
        for j in range(d):
            if w[j] >= 7:
                _qk = qkey(tuple(w[(j + m + (1 if W10PLANT == 'q7shift' else 0)) % d] for m in range(d)))   # W15 plant q7shift: key read from B's successor, not from B
                r[('q', _qk)] += 1 if (W10PLANT == 'q7flip' or (W10PLANT == 'q7one' and _qk == Q7ONE_KEY)) else -1   # W15 q7one: one key's payer sign flipped
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
                    m7_ = MASK[(sg_, c_, a_, W(i + 2 * sg_), W(i + 3 * sg_), W(i + 4 * sg_), o_)]
                    if F2BR: m7_ &= ~f2b_extra(d, w, s, i, ('w7', 7, sg_))   # f2b041
                    r[('lQ', (c_, a_, m7_))] += 1
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
                    m8_ = MASK8[(sg_, c_, a_, W(i + 2 * sg_), W(i + 3 * sg_), W(i + 4 * sg_), o_)]
                    if F2BR: m8_ &= ~f2b_extra(d, w, s, i, ('w7', 8, sg_))   # f2b041
                    r[('lQ', (8, c_, a_, m8_))] += 1
    if KSKEYS:   # W17: K* / EDGE payer (d = 7) and payee terms
        for k_, cf_ in ks_terms(d, w, s).items(): r[k_] += cf_
    if GKKEYS:   # W17 round 4: generic keys
        for k_, cf_ in gk_recv_terms(d, w, s).items(): r[k_] += cf_
    return {k: v for k, v in r.items() if v != 0}
def spec_val(d, lk, sv): return sum(cf * val(k) for k, cf in recv_spec(d, lk, sv).items())

# ================= 12.8: exact lower check =================
SKIP_LOWER = os.environ.get('SKIP_LOWER') == '1'
if SKIP_LOWER: CERT = []; print('lower check skipped (upper-only job)')
tot = collections.defaultdict(Fr); tco = Fr(0); Dn = Fr(0); nlab = collections.Counter(); noncanon = []
C6LOW = {'rows': 0, 'pos': 0, 'sumw': Fr(0)}   # W17 round 3: cons2 cert rows (count, w > 0, sum of w)
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
        if C6LE:   # W17 round 3: c6le, the 6 ends <= t: in - out - t <= 0 is the receiver row at d = 6 (a <= row): w <= 0, t coefficient -1, constant 0
            C6LOW['rows'] += 1; C6LOW['sumw'] += w
            if w > 0: C6LOW['pos'] += 1; fail('cons2 weight > 0 under C6LE (a <= row needs w <= 0) %s w = %s' % (lab, w))
            tco -= w   # Dn += w * 0
        else: C6LOW['rows'] += 1; C6LOW['sumw'] += w; C6LOW['pos'] += w > 0   # equality: w free, no t term, constant 0
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
if C6LOW['rows']: print('cons2 cert rows (%s mode): %d, with w > 0: %d, sum of w %s (= %.6f)%s' % ('c6le' if C6LE else 'equality', C6LOW['rows'], C6LOW['pos'], C6LOW['sumw'], float(C6LOW['sumw']),
                       '; t coefficient from cons2 rows %s' % (-C6LOW['sumw']) if C6LE else '; no t term (equation rows)'), flush=True)
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
_WL = 'wlp3r6_ck.py' if os.environ.get('CKEEP') else 'wlp3r6.py'   # s52c: the CKEEP copies (frozen wlp3*.py untouched)
src = open(os.path.join(HERE, _WL)).read().replace('os.path.abspath(__file__)', repr(os.path.join(HERE, _WL)), 1)
sys.argv = ['wlp3r6', 'tag=%s' % os.environ.get('SEPTAG', 's16chk'), 'dmaxp=%s' % os.environ.get('DMAXP', '17')] + ARGS
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
EX6F = os.path.join(ST16, 'ex6_%s.bin' % W10TAG)
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
def RNET(k): return RR.get(k, 0.0) - (RRR.get(k, 0.0) if HATRR else 0.0)   # W10 15r: the window carries r - rr
def rrel(wm1, sm1, w0, wp1):
    return max(RNET(key_receiver([wm1, w0, wp1, wp2], [sm1, 5, sp1, 5], 1)) for wp2 in LET for sp1 in LET)
RREL_ = _np.zeros((125, 25)); REX_ = _np.zeros(15625)
ZREL_ = _np.zeros((3, 125, 25)); ZEX_ = _np.zeros((3, 15625)); QREL_ = _np.zeros((3, 125, 25)); QPAIR_ = _np.zeros((3, 625, 25)); QPAY_ = _np.zeros(78125)
def ZNET(k): return ZV.get(k, 0.0) - (ZRV.get(k, 0.0) if ZR else 0.0)
if HAT5:
    for wm1, sm1, w0, wp1 in itertools.product(LET, repeat=4):
        RREL_[(wm1 - 5) * 25 + (sm1 - 5) * 5 + (w0 - 5), wp1 - 5] = rrel(wm1, sm1, w0, wp1)
    for wm1, w0, wp1, wp2, sm1, sp1 in itertools.product(LET, repeat=6):
        REX_[(((((wm1 - 5) * 5 + w0 - 5) * 5 + wp1 - 5) * 5 + wp2 - 5) * 25) + (sm1 - 5) * 5 + sp1 - 5] = RNET(key_receiver([wm1, w0, wp1, wp2], [sm1, 5, sp1, 5], 1))
    RTF = os.path.join(ST16, 'rtab_%s.bin' % W10TAG)
    with open(RTF, 'wb') as _f: _f.write(RREL_.astype('<f8').tobytes()); _f.write(REX_.astype('<f8').tobytes())
    SEPX.stdin.close(); SEPX.wait()
    SEPENV = dict(os.environ, SEP_NODELIMIT='0', SEP_ARRKEY='1', SEP_EXACT6=EX6F, SEP_RTAB=RTF)
    if ZH:   # W10 s22 22.1: z - zr at a link five; exact over (w_{i-2}, w_{i-1}, w_{i+1}, w_{i+2}, s_{i-1}, s_i), relaxed over the two hat classes
        for _ui, _U in enumerate((7, 8, 9)):
            for wm2, wm1, wp1, wp2, sm1, s0 in itertools.product(LET, repeat=6):
                zk = zkey((_U, wp1, s0, sm1, wm1), c(wp2), c(wm2))
                ZEX_[_ui, ((((wm2 - 5) * 5 + wm1 - 5) * 5 + wp1 - 5) * 5 + wp2 - 5) * 25 + (sm1 - 5) * 5 + s0 - 5] = ZNET(zk)
            for wm1, sm1, s0, wp1 in itertools.product(LET, repeat=4):
                ZREL_[_ui, (wm1 - 5) * 25 + (sm1 - 5) * 5 + 0, (s0 - 5) * 5 + wp1 - 5] = max(ZNET(zkey((_U, wp1, s0, sm1, wm1), hr, hl)) for hr in (0, 1) for hl in (0, 1))
        ZTF = os.path.join(ST16, 'ztab_%s.bin' % W10TAG)
        with open(ZTF, 'wb') as _f: _f.write(ZREL_.astype('<f8').tobytes()); _f.write(ZEX_.astype('<f8').tobytes())
        SEPENV['SEP_ZTAB'] = ZTF
        print('W10 z separator tables: exact min %.6f max %.6f; relaxed max %.6f (%s)' % (ZEX_.min(), ZEX_.max(), ZREL_.max(), os.path.basename(ZTF)), flush=True)
    if Q7:   # W10 q7: payee pair table, unmasked relaxed window term at a link 7, payer total per raw d = 7 link
        for _ui, _U in enumerate((7, 8, 9)):
            for a_, b_, c_, e_ in itertools.product(LET, repeat=4):
                vals = []
                for p1, p2 in itertools.product(LET, LET):
                    m_ = (_U, a_, b_, p1, p2, c_, e_)
                    v_ = -1.0 if canon(m_) in RBIG else QV.get(qkey(m_), 0.0)
                    QPAIR_[_ui, (((a_ - 5) * 5 + b_ - 5) * 5 + c_ - 5) * 5 + e_ - 5, (p1 - 5) * 5 + p2 - 5] = v_; vals.append(v_)
                QREL_[_ui, (e_ - 5) * 25 + (c_ - 5) * 5 + 2, (b_ - 5) * 5 + a_ - 5] = max(vals + [0.0])   # state (w_{i-1}, s_{i-1}, 7), choice (s_i, w_{i+1})
        for _ix, lk7 in enumerate(itertools.product(LET, repeat=7)):
            QPAY_[_ix] = sum(QV.get(qkey(tuple(lk7[(j + m) % 7] for m in range(7))), 0.0) for j in range(7) if lk7[j] >= 7)
        if os.environ.get('W15PLANT_SEP') == 'q7pay': QPAY_ = -QPAY_; print('PLANTED ERROR (separator only) q7pay: payer table sign flipped', flush=True)   # W15 control
        if os.environ.get('W15PLANT_SEP') == 'q7pair': QPAIR_[QPAIR_ > 0] *= 0.5; print('PLANTED ERROR (separator only) q7pair: payee pair values halved', flush=True)   # W15 control
        Q7F = os.path.join(ST16, 'q7_%s.bin' % W10TAG)
        with open(Q7F, 'wb') as _f: _f.write(QREL_.astype('<f8').tobytes()); _f.write(QPAIR_.astype('<f8').tobytes()); _f.write(QPAY_.astype('<f8').tobytes())
        SEPENV['SEP_Q7'] = Q7F
        if Q7M: SEPENV['SEP_Q7M'] = '1'
        if F2B7 and os.environ.get('W17PLANT_SEP7') != 'off': SEPENV['SEP_F2B7'] = '1'   # W17 round 5
        elif F2B7: print('PLANTED ERROR (separator only) W17PLANT_SEP7=off: the separator runs without SEP_F2B7', flush=True)
        print('W10 q7 separator tables: relaxed (unmasked) max %.6f, payer total max %.6f, masks %s (%s)' % (QREL_.max(), QPAY_.max(), 'on (d = 7, 8)' if Q7M else 'off', os.path.basename(Q7F)), flush=True)
    if RPATN:
        FXF = os.path.join(ST16, 'fullx_%s.txt' % W10TAG)
        open(FXF, 'w').write('\n'.join(FULLX) + '\n'); SEPENV['SEP_FULLX'] = FXF
    if L3Q:   # section 21.6: relaxed window term at a d = 7 link 7, exact payee / payer terms at the leaf
        L3R = _np.zeros((125, 25)); L3X = _np.zeros(31250); L3P = _np.zeros(125)
        for wm1, sm1, s0, wp1 in itertools.product(LET, repeat=4):
            L3R[(wm1 - 5) * 25 + (sm1 - 5) * 5 + 2, (s0 - 5) * 5 + (wp1 - 5)] = UB(wp1, s0) + UB(wm1, sm1)
        for (sg_, c_, a_, w2_, w3_, w4_, o_), m_ in MASK.items():
            L3X[((((((0 if sg_ == 1 else 1) * 5 + c_ - 5) * 5 + a_ - 5) * 5 + w2_ - 5) * 5 + w3_ - 5) * 5 + w4_ - 5) * 5 + o_ - 5] = Qeff(c_, a_, m_)
        for k_, v_ in LQ.items():   # s47 R8: the V = 7 payer table PQ from 3-tuple keys only
            if len(k_) == 3: c_, a_, a2 = k_; L3P[((c_ - 5) * 5 + a_ - 5) * 5 + a2 - 5] = v_
        L3F = os.path.join(ST16, 'l3q_%s.bin' % W10TAG)
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
        L8F = os.path.join(ST16, 'l3q8_%s.bin' % W10TAG)
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
        FBF = os.path.join(ST16, 'fb_%s.bin' % W10TAG)
        with open(FBF, 'wb') as _f: _f.write(FBREL_.astype('<f8').tobytes()); _f.write(FBX_.astype('<f8').tobytes())
        SEPENV['SEP_FB6'] = FBF
        print('fb separator tables: %d fb values; exact min %.6f max %.6f; relaxed max %.6f (%s)' % (len(FBV), FBX_.min(), FBX_.max(), FBREL_.max(), os.path.basename(FBF)), flush=True)
    if F2BR:   # f2b041: leaf tables for bin/sep3r_f2bS (SEP_F2BS)
        _MT = _np.zeros((3, 5, 5, 5, 5, 2, 2, 32)); _PM = _np.zeros((3,) + (5,) * 8, dtype=_np.uint8)
        for _ui, _U in enumerate((7, 8, 9)):
            for wp1, s0, sm1, wm1 in itertools.product(LET, repeat=4):
                for apP, apM in itertools.product((0, 1), repeat=2):
                    for m_ in range(32):
                        sg = sig2_of(_U, wp1, s0, sm1, wm1, (5, 7)[apP], (5, 7)[apM]) + (m_,)
                        _MT[_ui, wp1 - 5, s0 - 5, sm1 - 5, wm1 - 5, apP, apM, m_] = Mval(sg) if cand2(sg) else 0.0
            for _ix in itertools.product(range(5), repeat=8):
                _PM[(_ui,) + _ix] = pmask(_U, *(q + 5 for q in _ix))
        # consistency with SEP_EXACT6 (V6 off: EX6 = M at the unreduced mask) and monotonicity (every delta <= 0)
        _exb = 0
        for _ui in range(3):
            for _ix in itertools.product(range(5), repeat=8):
                wm2, wm1, wp1, wp2, sm2, sm1, s0, sp1 = _ix
                if abs(_MT[_ui, wp1, s0, sm1, wm1, int(wp2 >= 2), int(wm2 >= 2), _PM[(_ui,) + _ix]] - _EX[(_ui,) + _ix]) > 1e-15: _exb += 1
        _mono = sum(1 for m_ in range(32) for b_ in range(5) if (m_ >> b_) & 1 and (_MT[..., m_ & ~(1 << b_)] > _MT[..., m_] + 1e-15).any())
        _QF7 = _np.zeros((5, 5, 32)); _QF8 = _np.zeros((5, 5, 32))
        for c_, a_, m_ in itertools.product((5, 6), (5, 6), range(32)):
            _QF7[c_ - 5, a_ - 5, m_] = Qeff(c_, a_, m_) if L3Q else 0.0; _QF8[c_ - 5, a_ - 5, m_] = Qeff8(c_, a_, m_) if L3Q8 else 0.0
        _mono += sum(1 for Q_ in (_QF7, _QF8) for m_ in range(32) for b_ in range(5) if (m_ >> b_) & 1 and (Q_[..., m_ & ~(1 << b_)] > Q_[..., m_] + 1e-15).any())
        _MK7 = _np.zeros(31250, dtype=_np.uint8); _MK8 = _np.zeros(31250, dtype=_np.uint8)
        for MM_, KK_ in ((MASK, _MK7), (MASK8, _MK8)):
            for (sg_, c_, a_, w2_, w3_, w4_, o_), m_ in MM_.items():
                KK_[((((((0 if sg_ == 1 else 1) * 5 + c_ - 5) * 5 + a_ - 5) * 5 + w2_ - 5) * 5 + w3_ - 5) * 5 + w4_ - 5) * 5 + o_ - 5] = m_
        print('f2b tables: M table vs EX6 mismatches %d; monotonicity violations (M, Qeff, Qeff8) %d' % (_exb, _mono), flush=True)
        if _mono:   # W15: list every offending entry (as /tmp/swarm-W10/dbg/mono.py), then FAIL as before (no clamping)
            for m_ in range(32):
                for b_ in range(5):
                    if not ((m_ >> b_) & 1): continue
                    D_ = _MT[..., m_ & ~(1 << b_)] - _MT[..., m_]
                    for _ixm in zip(*_np.nonzero(D_ > 1e-15)):
                        print('MONO-M U=%d (wp1,s0,sm1,wm1)=%s (apP,apM)=%s mask %s -> %s: %.9g > %.9g' % ((7, 8, 9)[_ixm[0]], [int(v) + 5 for v in _ixm[1:5]], tuple(int(v) for v in _ixm[5:7]), bin(m_), bin(m_ & ~(1 << b_)), _MT[_ixm + (m_ & ~(1 << b_),)], _MT[_ixm + (m_,)]), flush=True)
            for nm_, Q_, UBf_ in (('Qeff7', _QF7, UB), ('Qeff8', _QF8, UB8)):
                for m_ in range(32):
                    for b_ in range(5):
                        if not ((m_ >> b_) & 1): continue
                        D_ = Q_[..., m_ & ~(1 << b_)] - Q_[..., m_]
                        for _ixm in zip(*_np.nonzero(D_ > 1e-15)):
                            c_, a_ = int(_ixm[0]) + 5, int(_ixm[1]) + 5; ub_ = UBf_(c_, a_); qs_ = Q_[_ixm + (m_ & ~(1 << b_),)]
                            print('MONO-%s (c,a)=(%d,%d) mask %s -> %s: %.9g > %.9g; stored lQ at the smaller mask %s, at the larger %s; window bound UB(c,a) = %.9g (%s)' % (
                                nm_, c_, a_, bin(m_), bin(m_ & ~(1 << b_)), qs_, Q_[_ixm + (m_,)],
                                (LQQ.get((c_, a_, m_ & ~(1 << b_))) if nm_ == 'Qeff7' else LQQ.get((8, c_, a_, m_ & ~(1 << b_)))),
                                (LQQ.get((c_, a_, m_)) if nm_ == 'Qeff7' else LQQ.get((8, c_, a_, m_))), ub_,
                                'the window term still covers it' if qs_ <= ub_ + 1e-15 else 'NOT covered by the window term'), flush=True)
            print('MONO note: %s' % ('NOCLAMP=1: not failed; slack mode below' if NOCLAMP else 'the gate is a hard FAIL (W15, coordinator 5 Nov): the separator leaf assumes every f2b delta <= 0; no clamping; NOCLAMP=1 gives the slack mode'), flush=True)
        # W15: the largest positive leaf delta over every (mask, sub-mask) pair: M per U, Qeff7 (d = 7) and Qeff8 (d = 8)
        _SUB = [(m_, m2_) for m_ in range(32) for m2_ in range(32) if m2_ & ~m_ == 0 and m2_ != m_]
        _dM = [max([float((_MT[_ui][..., m2_] - _MT[_ui][..., m_]).max()) for m_, m2_ in _SUB] + [0.0]) for _ui in range(3)]
        _dQ7 = max([float((_QF7[..., m2_] - _QF7[..., m_]).max()) for m_, m2_ in _SUB] + [0.0])
        _dQ8 = max([float((_QF8[..., m2_] - _QF8[..., m_]).max()) for m_, m2_ in _SUB] + [0.0])
        SLACKD = {d_: d_ * _dM[min(d_, 9) - 7] + (2 * d_ * _dQ7 if d_ == 7 else 0.0) + (2 * d_ * _dQ8 if d_ == 8 else 0.0) for d_ in (7, 8, 9)}
        print('f2b positive leaf deltas (max over every mask / sub-mask pair): dM+ U7/U8/U9 %s, dQeff7+ %.9g, dQeff8+ %.9g; pruning slack d*dM+ + 2d*dQ+ = %s' % (
            ['%.9g' % v for v in _dM], _dQ7, _dQ8, {d_: float('%.9g' % v) for d_, v in SLACKD.items()}), flush=True)
        if _mono and NOCLAMP:
            if _exb: fail('f2b leaf tables inconsistent (M table vs EX6)')
            SEPENV['SEP_SLACKD'] = ','.join('%d:%.12g' % (d_, v) for d_, v in SLACKD.items())
            print('NOCLAMP MODE: the monotonicity gate found %d non-monotone pairs; NOT failed: every leaf keeps its exact (unclamped) value and the separator adds slack(d) %s to every pruning test (SEP_SLACKD=%s)' % (_mono, {d_: float('%.9g' % v) for d_, v in SLACKD.items()}, SEPENV['SEP_SLACKD']), flush=True)
        elif _exb or _mono: fail('f2b leaf tables inconsistent or not monotone (delta could be > 0)%s' % ('' if _mono == 0 else '; rerun with NOCLAMP=1 for the slack mode'))
        F2F = os.path.join(ST16, 'f2bS_%s_%s.bin' % (os.environ.get('SEPTAG', 'x'), W10TAG))
        import struct as _st
        with open(F2F, 'wb') as _f:
            _f.write(_MT.astype('<f8').tobytes()); _f.write(_QF7.astype('<f8').tobytes()); _f.write(_QF8.astype('<f8').tobytes())
            _f.write(_PM.tobytes()); _f.write(_MK7.tobytes()); _f.write(_MK8.tobytes())
            for g_ in (('w6', 7), ('w6', 8), ('w6', 9), ('w7', 7, 1), ('w7', 7, -1), ('w7', 8, 1), ('w7', 8, -1)):
                _f.write(_st.pack('<I', len(F2BG[g_])))
                for fw_, fs_, m_ in F2BG[g_]: _f.write(_st.pack('<QQQ', fw_, fs_, m_))
        SEPENV['SEP_F2BS'] = F2F
        print('f2b leaf table file %s' % os.path.basename(F2F), flush=True)
    KSREL_ = _np.zeros((3, 125, 25))
    if KSKEYS:   # W17: payee window bound at a link 7 (per centre class U = 7, 8, 9+), exact payee / payer at the sep3r_w17 leaf
        # numpy unions of the 6-private masks over the letters outside the window (the loop version in ksfam is checked below)
        _KSOR = {}
        for _U in (7, 8, 9):
            _nk = ~KT[_U]   # allowed[wm2, wm1, wp1, wp2, sm2, sm1, s0, sp1, p]
            _KSOR[(_U, 1)] = _nk[:, 2, :, :, :, :, :, :, :].any(axis=(1, 2, 5, 6))      # k = j+1: [w_{j-1}, s_{j-1}, s_j, p]
            _KSOR[(_U, -1)] = _nk[:, :, 2, :, :, :, :, :, :].any(axis=(0, 1, 3, 4))     # k = j-1: [w_{j+1}, s_{j-1}, s_j, p]
        def _amask_or(U_, sg_, wm1_, sm1_, sp0_, wp1_):
            A_ = _KSOR[(U_, sg_)][(wm1_ if sg_ == 1 else wp1_) - 5, sm1_ - 5, sp0_ - 5]
            return sum(1 << b_ for b_ in range(5) if A_[b_])
        KSCTX.amask_or = _amask_or
        _kc = {}
        for _ui, _U in enumerate((7, 8, 9)):
            for wm1, sm1, s0, wp1 in itertools.product(LET, repeat=4):
                KSREL_[_ui, (wm1 - 5) * 25 + (sm1 - 5) * 5 + 2, (s0 - 5) * 5 + wp1 - 5] = sum(KSV.get(k_[0], 0.0) * KF.bound_count(KSCTX, k_, _U, wm1, sm1, s0, wp1, _kc) for k_ in KSKEYS)
        _kschk = 0; _rk = random.Random(17)   # the numpy unions vs the plain loop over pmask, on 300 random windows per side
        for _ in range(300):
            _U = _rk.choice((7, 8, 9)); wm1, sm1, s0, wp1 = (_rk.choice(LET) for _ in range(4))
            for sg_ in (1, -1):
                m_ = 0
                for x1, x2, y1, y2 in itertools.product(LET, repeat=4):
                    m_ |= pmask(_U, wm1, 7, x1, x2, sm1, s0, y1, y2) if sg_ == 1 else pmask(_U, x2, x1, 7, wp1, y2, y1, sm1, s0)
                _kschk += m_ != _amask_or(_U, sg_, wm1, sm1, s0, wp1)
        if _kschk: fail('W17 6-private window unions differ between numpy and the loop (%d)' % _kschk)
        import struct as _stk
        KSF = os.path.join(ST16, 'ks_%s.bin' % W10TAG)
        with open(KSF, 'wb') as _f:
            _f.write(_stk.pack('<ii', len(KSKEYS), 1 if os.environ.get('KSA10', 'amask') == 'grammar' else 0))
            for n_, P_, cd_ in KSKEYS:
                _f.write(_stk.pack('<idi', P_, KSV.get(n_, 0.0), len(cd_)))
                for pi_, m_ in cd_: _f.write(_stk.pack('<ii', pi_, m_))
            _f.write(KSREL_.astype('<f8').tobytes())
        SEPENV['SEP_KS'] = KSF
        if os.environ.get('W17PLANT_SEP'): SEPENV['SEP_KSPLANT'] = os.environ['W17PLANT_SEP']; print('PLANTED ERROR (separator only) %s' % os.environ['W17PLANT_SEP'], flush=True)
        print('W17 KS separator table: window max U7/U8/U9 %s, windows > 0 %s; 6-private union check %d mismatches (%s)' % (
            ['%.6g' % KSREL_[u_].max() for u_ in range(3)], [int((KSREL_[u_] > 0).sum()) for u_ in range(3)], _kschk, os.path.basename(KSF)), flush=True)
    GKREL_ = _np.zeros((3, 125, 25)); GKWNP = None
    if GKKEYS:   # W17 round 4: numpy gkwin per U over the 5^9 windows; DP window bound = its max over (w_{j-2}, w_{j+2}, s_{j-2}, s_{j+1})
        import time as _tmg; _tg = _tmg.time()
        GKWNP = gk_window_tables()
        print('W17 GK numpy window tables built in %.0fs' % (_tmg.time() - _tg), flush=True)
        for _ui in range(3): GKREL_[_ui] = GKWNP[_ui].max(axis=(0, 4, 5, 8)).transpose(0, 3, 1, 4, 2).reshape(125, 25)
        import struct as _stg
        GKF_ = os.path.join(ST16, 'gk_%s.bin' % W10TAG)
        with open(GKF_, 'wb') as _f:
            _f.write(_stg.pack('<i', len(GKKEYS)))
            for n_, U_, V_, cd_ in GKKEYS:
                _f.write(_stg.pack('<iidi', U_, V_, KSV.get(n_, 0.0), len(cd_)))
                for pi_, m_ in cd_: _f.write(_stg.pack('<ii', pi_, m_))
            _f.write(GKREL_.astype('<f8').tobytes())
        SEPENV['SEP_GK'] = GKF_
        if os.environ.get('W17PLANT_SEP'): SEPENV['SEP_GKPLANT'] = os.environ['W17PLANT_SEP']; print('PLANTED ERROR (separator only) %s' % os.environ['W17PLANT_SEP'], flush=True)
        print('W17 GK separator table: window max U7/U8/U9 %s, cells > 0 %s, windows > 0 per U %s (%s)' % (['%.6g' % GKREL_[u_].max() for u_ in range(3)],
              [int((GKREL_[u_] > 0).sum()) for u_ in range(3)], [int((GKWNP[u_] > 0).sum()) for u_ in range(3)], os.path.basename(GKF_)), flush=True)
    _BIN = os.environ.get('SEPBIN') or ('sep3r_w10' if W10ON else 'sep3r_f2bS' if F2BR else ('sep3r_l3q' if L3Q else 'sep3r_ak'))
    print('separator binary: %s' % _BIN, flush=True)
    SEPX = _sp.Popen([os.path.join(HERE, 'bin', _BIN), NS_['SF']], stdin=_sp.PIPE, stdout=_sp.PIPE, text=True, env=SEPENV)
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
def w10rel_row(d, lk, sv):   # W10: relaxed z (max over the hat classes) at link fives, unmasked Q at link 7s; the payer term (<= 0) is dropped
    w = [int(c_) for c_ in lk]; s_ = [int(c_) for c_ in sv]; ui_ = min(d, 9) - 7; v_ = 0.0
    for i in range(d):
        st_ = (w[(i - 1) % d] - 5) * 25 + (s_[(i - 1) % d] - 5) * 5 + w[i] - 5; ch_ = (s_[i] - 5) * 5 + w[(i + 1) % d] - 5
        if ZH and w[i] == 5: v_ += ZREL_[ui_, st_, ch_]
        if Q7 and w[i] == 7: v_ += QREL_[ui_, st_, ch_]
    return v_
def ksrel_row(d, lk, sv):   # W17: payee window bound at every link 7 (the payer debit, <= 0, is dropped)
    if not KSKEYS: return 0.0
    w = [int(c_) for c_ in lk]; s_ = [int(c_) for c_ in sv]; ui_ = min(d, 9) - 7
    return sum(KSREL_[ui_, (w[(i - 1) % d] - 5) * 25 + (s_[(i - 1) % d] - 5) * 5 + 2, (s_[i] - 5) * 5 + w[(i + 1) % d] - 5] for i in range(d) if w[i] == 7)
def gkrel_row(d, lk, sv):   # W17 round 4: GKREL at every link position
    if not GKKEYS: return 0.0
    w = [int(c_) for c_ in lk]; s_ = [int(c_) for c_ in sv]; ui_ = min(d, 9) - 7
    return sum(GKREL_[ui_, (w[(i - 1) % d] - 5) * 25 + (s_[(i - 1) % d] - 5) * 5 + w[i] - 5, (s_[i] - 5) * 5 + w[(i + 1) % d] - 5] for i in range(d))
def studio_val(d, lk, sv):
    r_ = recv_row(d, lk, sv)
    return gkrel_row(d, lk, sv) + ksrel_row(d, lk, sv) + w10rel_row(d, lk, sv) + fbrel_row(d, lk, sv) + l3rel_row(d, lk, sv) + rrel_row(d, lk, sv) + sum(cf * (yv[k[1]] if k[0] == 'y' else xv.get(k[1], 0.0) if k[0] == 'x' else V6B[k[1]] if k[0] == 'y6b' else 0.0) for k, cf in r_.items() if k[0] != 't')
def xk(rr): return collections.Counter({k[1]: cf for k, cf in rr.items() if k[0] == 'x'})
tests = [(e['row'][1], e['row'][2], e['row'][3]) for e in CERT if e['row'][0] == 'receiverR2']
if os.environ.get('REPLAY'):   # f2b041 job 2: per-arrangement admissibility, row value and row terms for the violators in REPLAY files
    with open(os.environ['REPLAY_OUT'], 'w') as _ro:
        for _fn in os.environ['REPLAY'].split(','):
            for _l in open(_fn):
                _f = _l.split(); d, lk, sv = int(_f[0]), _f[2], _f[3]; _w = [int(c) for c in lk]; _s = [int(c) for c in sv]
                _rs = recv_spec(d, lk, sv); _ro.write(json.dumps([d, lk, sv, bool(admissible(d, _w, _s)), spec_val(d, lk, sv), sorted([repr(k), v] for k, v in _rs.items())]) + '\n')
    print('REPLAY written %s' % os.environ['REPLAY_OUT'], flush=True); sys.exit(0)
def fam_of(k): return 'ks:' + k[1] if k[0] == 'ks' else {'Q7': 'q7Q', 'q': 'q7q', 'lQ': 'lq', 'g': 'g'}.get(k[0], k[0])
if os.environ.get('W10_ROWS'):   # W10 control (c): per-arrangement receiver rows and every sender context, by family, for the Opus comparison
    with open(os.environ['W10_ROWS_OUT'], 'w') as _ro:
        for _l in open(os.environ['W10_ROWS']):
            _f = _l.split(); d, lk, sv = int(_f[0]), _f[1], _f[2]; fam = collections.defaultdict(float)
            for k_, cf_ in recv_spec(d, lk, sv).items(): fam[fam_of(k_)] += cf_ * val(k_)
            _ro.write(json.dumps(['R', d, lk, sv, sum(fam.values()), fam, bool(admissible(d, [int(c_) for c_ in lk], [int(c_) for c_ in sv]))]) + '\n')   # + spec admissibility (control e)
        for w in SENDERS:
            sixes = [k for k in range(5) if w[k] == 6]
            for hb in itertools.product((0, 1), repeat=5):
                for fb in itertools.product((0, 1), repeat=len(sixes)):
                    H_ = dict(zip(range(5), hb)); F_ = dict(zip(sixes, fb)); r = sender_row(w, H_, F_)
                    if r is None: continue
                    fam = collections.defaultdict(float)
                    for k_, cf_ in r.items(): fam[fam_of(k_)] += cf_ * val(k_)
                    _ro.write(json.dumps(['S', ''.join(map(str, w)), list(hb), list(fb), sum(fam.values()), fam]) + '\n')
    print('W10_ROWS written %s' % os.environ['W10_ROWS_OUT'], flush=True); sys.exit(0)
if W10ON and os.environ.get('W10ST', '1') != '0':   # W10 self-test: C++ exact row value ("e") vs the Python spec row, random + forced arrangements
    _rr = random.Random(int(os.environ.get('W10SEED', '10'))); _st = collections.Counter(); _mx = collections.defaultdict(float); _bad = 0
    def _w10arr(d, kind):
        w_ = [_rr.choice(LET) for _ in range(d)]; s_ = [_rr.choice(LET) for _ in range(d)]; i0 = _rr.randrange(d)
        if kind == 1: s_[i0] = 5; w_[i0] = _rr.choice((5, 6, 7)); w_[(i0 + 1) % d] = _rr.choice((5, 6, 7))     # a diamond: apex five
        elif kind == 2: w_[i0] = 5; w_[(i0 + 1) % d] = _rr.choice((7, 8, 9, 5, 6)); w_[(i0 - 1) % d] = _rr.choice((7, 8, 9, 5, 6))   # a link five
        elif kind == 3:   # q7 payee slot: A = w_i0 = 7 with the W5 key 7665557 visible (w+ = 6, s_i = 6, s_{i-1} = 5, w- = 7)
            w_[i0] = 7; w_[(i0 + 1) % d] = 6; s_[i0] = 6; s_[(i0 - 1) % d] = 5; w_[(i0 - 1) % d] = 7
            for o_ in (2, 3, 4, -2, -3): w_[(i0 + o_) % d] = _rr.choice((5, 6))   # small c / a so that the l3q masks are read
        elif kind == 4 and d == 7: w_ = list(_rr.choice(((7, 6, 6, 5, 5, 5, 7), (7, 5, 5, 5, 6, 6, 7), (7, 5, 7, 5, 5, 6, 6)))); k_ = _rr.randrange(7); w_ = w_[k_:] + w_[:k_]   # payer slot
        elif kind == 4: w_[i0] = 7
        if _rr.random() < 0.5: w_ = w_[::-1]; s_ = s_[::-1][1:] + s_[::-1][:1]   # reflect (apex s_i sits between w_i and w_{i+1})
        return ''.join(map(str, w_)), ''.join(map(str, s_))
    for d in range(7, int(os.environ.get('W10STD', '12')) + 1):
        sepx(d, yv, xv, 1e9, 1)   # load this d's weights into the separator (no search: threshold 1e9)
        for n_ in range(int(os.environ.get('W10STN', '2500'))):
            lk, sv = _w10arr(d, n_ % 5)
            SEPX.stdin.write('e %d %s %s\n' % (d, lk, sv)); SEPX.stdin.flush(); out_ = SEPX.stdout.readline().strip()
            if out_ == 'inadm': _st['window-inadmissible'] += 1; continue
            cv_ = float(out_); pv_ = spec_val(d, lk, sv); _st['compared'] += 1; _mx[d] = max(_mx[d], abs(cv_ - pv_))
            rs_ = recv_spec(d, lk, sv)
            for f_ in ('rr', 'z', 'zr', 'Q7', 'q'):
                if any(k_[0] == f_ and abs(val(k_)) > 0 for k_ in rs_): _st['with ' + f_] += 1
            if abs(cv_ - pv_) > 1e-9:
                _bad += 1
                if _bad <= 5: print('W10 SELFTEST MISMATCH d=%d %s %s python %.12f c++ %.12f' % (d, lk, sv, pv_, cv_), flush=True)
    print('W10 self-test (C++ exact leaf vs Python spec rows): %s; max |difference| by d %s; mismatches > 1e-9: %d' % (dict(_st), {k: float('%.3g' % v) for k, v in _mx.items()}, _bad), flush=True)
    if _bad: fail('W10 self-test: C++ leaf and Python rows differ')
    if os.environ.get('W10ST_ONLY') == '1': print('VERDICT: W10 SELFTEST %s' % ('PASS' if not FAIL else 'FAIL: ' + ' | '.join(FAIL))); sys.exit(0)
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'w17_blocks.py')).read())   # W17 tests (KSDUMP, W17GRAM, W17ST)
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gk_blocks.py')).read())    # W17 round 4 tests (GKST, GKORACLE)
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'f2b7_blocks.py')).read())  # W17 round 5 tests (F2B7ST, F2B7ROWS)
if F2BR:   # f2b041 self-test: spec delta (rules on minus rules off, spec_val) vs the C++ leaf delta ("f" command)
    def _cdelta(d, lk, sv):
        SEPX.stdin.write('f %d %s %s\n' % (d, lk, sv)); SEPX.stdin.flush(); return float(SEPX.stdout.readline())
    def _pdelta(d, lk, sv):
        v1 = spec_val(d, lk, sv); F2BON[0] = False; v0 = spec_val(d, lk, sv); F2BON[0] = True; return v1 - v0
    _rr = random.Random(int(os.environ.get('F2BSEED', '41'))); _ft = []
    _gl = [(g_, r_) for g_, L_ in F2BG.items() for r_ in L_]
    for _ in range(int(os.environ.get('F2BNT', '6000'))):
        g_, (fw_, fs_, m_) = _gl[_rr.randrange(len(_gl))] if _gl and _rr.random() < 0.85 else (None, (0, 0, 0))
        d = g_[1] if g_ else _rr.choice((7, 8, 9))
        while True:   # a word satisfying the rule at position 0 (centre letter set by the group), random elsewhere
            w_ = [_rr.choice([l_ for l_ in LET if not (fw_ >> (5 * o_ + l_ - 5)) & 1]) for o_ in range(d)]
            s_ = [_rr.choice([l_ for l_ in LET if not (fs_ >> (5 * o_ + l_ - 5)) & 1]) for o_ in range(d)]
            if g_: w_[0] = 6 if g_[0] == 'w6' else 7
            if _rr.random() < 0.3: w_[_rr.randrange(1, d)] = _rr.choice(LET)   # sometimes break the rule
            break
        k_ = _rr.randrange(d); w_ = w_[k_:] + w_[:k_]; s_ = s_[k_:] + s_[:k_]   # rotate
        _ft.append((d, ''.join(map(str, w_)), ''.join(map(str, s_))))
    _fb = 0; _nz = 0; _pos = 0
    for d, lk, sv in _ft:
        pd_, cd_ = _pdelta(d, lk, sv), _cdelta(d, lk, sv)
        _nz += abs(pd_) > 1e-12; _pos += pd_ > 1e-12
        if abs(pd_ - cd_) > 1e-9: _fb += 1; _fb <= 5 and print('F2B SELFTEST MISMATCH d=%d %s %s python %.12f c++ %.12f' % (d, lk, sv, pd_, cd_))
    print('f2b self-test: %d arrangements (seed %s), %d with a nonzero delta, %d positive; Python vs C++ mismatches %d' % (len(_ft), os.environ.get('F2BSEED', '41'), _nz, _pos, _fb), flush=True)
    if NOCLAMP and _pos and not _fb: print('NOCLAMP MODE: f2b self-test has %d positive deltas, all equal in Python and C++ (the leaf is unclamped); not failed' % _pos, flush=True)
    if _fb or (_pos and not NOCLAMP): fail('f2b self-test: Python rows and C++ leaf differ, or a delta is positive')
if os.environ.get('W15FIXROWS'):   # W15: fixed test rows "d:link:s,..." -> Python spec value, C++ exact leaf ("e"), f2b delta (Python / C++ "f"), lQ terms
    for _fr in os.environ['W15FIXROWS'].split(','):
        _d, _lk, _sv = _fr.split(':'); _d = int(_d)
        sepx(_d, yv, xv, 1e9, 1)
        SEPX.stdin.write('e %d %s %s\n' % (_d, _lk, _sv)); SEPX.stdin.flush(); _ce = SEPX.stdout.readline().strip()
        _cf = _cdelta(_d, _lk, _sv) if F2BR else float('nan'); _pf = _pdelta(_d, _lk, _sv) if F2BR else float('nan')
        _lqt = {repr(k_): (cf_, val(k_)) for k_, cf_ in recv_spec(_d, _lk, _sv).items() if k_[0] in ('lQ', 'lq')}
        print('FIXED ROW d=%d %s/%s: python exact %.12f, C++ exact %s, threshold %.12f; f2b delta python %.9g C++ %.9g; l3q terms %s' % (
            _d, _lk, _sv, spec_val(_d, _lk, _sv), _ce, _d - 6 + T, _pf, _cf, _lqt), flush=True)
    if os.environ.get('F2B_SELFTEST_ONLY') == '1': print('VERDICT: SELFTEST %s' % ('PASS' if not FAIL else 'FAIL: ' + ' | '.join(FAIL))); sys.exit(0)
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
        _sl = SLACKD.get(d, 0.0) if (NOCLAMP and 'SEP_SLACKD' in SEPENV) else 0.0   # W15 NOCLAMP: the separator's bound is relaxed + slack(d)
        if v2 + _sl < v1 - 1e-12: low += 1; low <= 5 and print('RELAXATION BELOW EXACT d=%d %s %s spec %.12f studio %.12f (slack %.3g)' % (d, lk, sv, v1, v2, _sl))
        if not XO and xk(recv_spec(d, lk, sv)) != xk(recv_row(d, lk, sv)): xbad += 1   # under xo the old x keys are off (R8)
print('spec rows vs Studio relaxed rows: %d arrangements, admissibility mismatches %d; %d compared: relaxed below exact %d, x-key mismatches %d'
      % (len(tests), adm_bad, ncmp, low, xbad), flush=True)
if adm_bad or low or xbad: fail('Studio relaxed receiver rows are not an upper bound on the spec rows')
rbad = 0; CAP = int(os.environ.get('CAP', '5000')); import time as _tm
_DL = [] if os.environ.get('DLIST') == 'none' else [int(x) for x in os.environ['DLIST'].split(',')] if os.environ.get('DLIST') else list(range(7, DMAXP + 1))   # f2b041: degrees split over processes
print('receiver degrees this process: %s' % _DL, flush=True)
_QD = os.environ.get('SEPQDUMP')   # W15: dump each degree's separator query (+ the tables' env and the SF file) for replays (drive15.py)
if _QD:
    import shutil as _shq
    os.makedirs(_QD, exist_ok=True); _shq.copy(NS_['SF'], os.path.join(_QD, 'sf.in'))
    _envq = {k_: v_ for k_, v_ in SEPENV.items() if k_.startswith('SEP_')}
    for k_ in [k_ for k_, v_ in _envq.items() if isinstance(v_, str) and v_.startswith(ST16 + '/')]:   # copy the table files next to the query
        _shq.copy(_envq[k_], os.path.join(_QD, os.path.basename(_envq[k_]))); _envq[k_] = os.path.join(_QD, os.path.basename(_envq[k_]))
    json.dump(dict(_envq, SEPBIN=os.path.join(HERE, 'bin', _BIN), T=repr(T), EPS=repr(EPS)), open(os.path.join(_QD, 'env.json'), 'w'), indent=1)
def _qtext(d, thr, many):
    xs_ = [(tau_, v_) for tau_, v_ in xv.items() if v_ > 1e-12]
    return 'q %d %.12f %d %d\n%s\nX %d %s\nR %d %s\n' % (d, thr, many, NS_['OMAX'], ' '.join('%.12f' % x_ for x_ in yv), len(xs_), ' '.join('%d %.12f' % kv for kv in xs_), NS_['N6B'], ' '.join('%.12f' % x_ for x_ in V6B))
for d in _DL:
    _thr = d - 6 + T + float(os.environ.get('SEPEPS', str(EPS)))
    if _QD: open(os.path.join(_QD, 'q_d%d.txt' % d), 'w').write(_qtext(d, _thr, CAP))
    if os.environ.get('QDUMP_ONLY') == '1':
        print('receivers d=%d: QUERY DUMPED to %s (not searched here)' % (d, _QD), flush=True); continue
    _t0 = _tm.time(); out = sepx(d, yv, xv, _thr, CAP)
    exact_bad = [(spec_val(d, lk, sv), lk, sv) for _, lk, sv in out if spec_val(d, lk, sv) > d - 6 + T + EPS]
    if TEXACT is not None:   # f2b041e: every reported row (all within SEPEPS of the bound) re-checked in exact rationals at t = TEXACT
        _ex = sorted((sum(cf * Fr(val(k)) for k, cf in recv_spec(d, lk, sv).items()) - (d - 6 + TEXACT), lk, sv) for _, lk, sv in out)
        exact_bad = [(float(e_) + d - 6 + T, lk, sv) for e_, lk, sv in _ex if e_ > 0]
        print('TEXACT d=%d: %d rows reported within SEPEPS %s of the bound; exact max excess %s; exact violated %d' % (d, len(_ex), os.environ.get('SEPEPS', str(EPS)), ('%.6g' % float(_ex[-1][0])) if _ex else '-', len(exact_bad)), flush=True)
    dev = max([abs(wq - spec_val(d, lk, sv)) for wq, lk, sv in out] + [0.0])
    if dev > 1e-9: fail('d=%d: sep3r_ak exact weight differs from the spec row by %.3g' % (d, dev))
    for v_, lk, sv in exact_bad[:5]: print('VIOLATED receiverR2 d=%d exact load %.12f link %s s %s' % (d, v_, lk, sv))
    full = len(out) < CAP
    if not full: fail('d=%d: relaxation reports >= %d arrangements; exact check incomplete' % (d, CAP))
    if os.environ.get('VIOLDUMP') and exact_bad:   # f2b041 job 2: every exact violator, with the dropped C patterns (ATTR_ARGS) that forbid it
        with open(os.environ['VIOLDUMP'] + '_d%d.txt' % d, 'w') as _vf:
            _na = collections.Counter()
            for v_, lk, sv in sorted(exact_bad, reverse=True):
                _w = [int(c) for c in lk]; _s = [int(c) for c in sv]; _hit = [nm for nm, P in ATTR.get(d, ()) if _pm1(d, _w, _s, P)]
                _na[len(_hit) > 0] += 1; _vf.write('%d %.12f %s %s %s\n' % (d, v_, lk, sv, ' '.join(_hit) or '-'))
        print('VIOLDUMP d=%d: %d violators; forbidden by a dropped C pattern %d, by none %d' % (d, len(exact_bad), _na[True], _na[False]), flush=True)
    rbad += len(exact_bad)
    print('receivers d=%d: relaxation reports %d above threshold%s; exact violated %d (%.0fs)' % (d, len(out), '' if full else ' (CAP hit)', len(exact_bad), _tm.time() - _t0), flush=True)
z9 = max([v for tq, v in X.items() if (tq // 15625) % 3 == 2] + [0.0])
Mk = np.full((NS, NS), -np.inf)
for a_, b_, rr in TRI[9]:
    (wp, sp, wc), (_, sc, wn) = states[a_], states[b_]
    v_ = (yv[ix[rr]] if rr is not None else 0.0) + z9 * BIGSTATE[a_]
    if wc == 6: v_ += best6(9, wn, sc, sp, wp)[0]
    if HAT5 and sc == 5: v_ += RREL_[(wp - 5) * 25 + (sp - 5) * 5 + wc - 5, wn - 5]   # section 15 r at the apex five
    if ZH and wc == 5: v_ += ZREL_[2, (wp - 5) * 25 + (sp - 5) * 5 + wc - 5, (sc - 5) * 5 + wn - 5]   # W10: relaxed z - zr at a link five, U = 9
    if Q7 and wc == 7: v_ += QREL_[2, (wp - 5) * 25 + (sp - 5) * 5 + wc - 5, (sc - 5) * 5 + wn - 5]   # W10: unmasked Q at a link 7, U = 9 (no payer at d >= 18)
    if KSKEYS and wc == 7: v_ += KSREL_[2, (wp - 5) * 25 + (sp - 5) * 5 + wc - 5, (sc - 5) * 5 + wn - 5]   # W17: K* / EDGE payee window bound, U = 9
    if GKKEYS: v_ += GKREL_[2, (wp - 5) * 25 + (sp - 5) * 5 + wc - 5, (sc - 5) * 5 + wn - 5]   # W17 round 4: generic-key window bound, U = 9, every position
    if FB or XO: v_ += FBREL_[2, (wp - 5) * 25 + (sp - 5) * 5 + wc - 5, (sc - 5) * 5 + wn - 5]   # s44 relaxed fb at U = 9
    Mk[a_, b_] = max(Mk[a_, b_], v_)
Pk = Mk.copy(); dpbad = 0
for k_ in range(2, 31):
    Pk = (Pk[:, :, None] + Mk[None, :, :]).max(axis=1)
    if k_ >= DMAXP + 1:
        v_ = np.diag(Pk).max()
        _dpm = max(globals().get('_dpm', -1e18), v_ - (k_ - 6 + T))   # f2b041e: largest (bound - threshold) over d = 18..30
        if v_ > k_ - 6 + T + EPS: dpbad += 1; print('DP d=%d relaxed closed-walk bound %.12f > %.12f (not decided)' % (k_, v_, k_ - 6 + T))
rbad += dpbad
print('DP margin: max over d of (closed-walk bound - (d - 6 + t)) = %.6g' % globals().get('_dpm', float('nan')), flush=True)
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
if os.environ.get('QDUMP_ONLY') == '1': print('VERDICT (python part; receivers d = %s were NOT searched here, only dumped): %s' % (','.join(map(str, _DL)), 'PASS' if not FAIL else 'FAIL: ' + ' | '.join(FAIL)))   # W15
else: print('VERDICT: %s' % (('PASS (upper FEASIBLE at %s; lower not checked)' if SKIP_LOWER else 'PASS (upper FEASIBLE, lower VALID %s)') % EXPECT_T if not FAIL else 'FAIL: ' + ' | '.join(FAIL)))
