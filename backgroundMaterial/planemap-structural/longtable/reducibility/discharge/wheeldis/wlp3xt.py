"""Job 30 part B (exploratory): wlp3x.py (L2) + Rule T, a sender-2-ball rule.
Rule T: a five v with a big neighbour u' and a 6-neighbour x adjacent to u' sends tau[root, side] to z, the other
common neighbour of u' and x, when z is big ("routed through the 6").
- Sender variables y[root, f_a, f_e]: f = the spoke on that side of the root is 6 and the vertex beyond it is big.
  Sender rows: for every non-R five word and every bigness of the vertices beyond its {6, big} spokes:
  sum over big roots y[root, f] + sum over flagged sides tau[root, side] >= 1 - t.
- Receiver u: a link five at w_i uses y[root, f], with f read from w_{i+-1}, w_{i+-2} (z = w_{i+-2}). Inflow: each s_j = 5
  with {w_j, w_{j+1}} = {6, big b} receives tau[root of s_j at b, side 6]. s_j's three other letters are outside u's
  patch, so the row takes the completion with the largest current tau (one row per completion, generated lazily).
- Option tfull: option F, z read as its letter 5..9 (Y[r, z_a, z_e], T[r, z_a, z_e, side], T only for z >= 7; the
  inflow T is keyed by the receiver's own letter). Sender rows run over every z-letter assignment, with the coupling.
- Options as wlp3x, plus tmerge (flags merged: y[root, f] = y[root, 00]) and tzero (tau fixed at 0). With both, the
  model is wlp3x's exactly (validation 3).
- Spec: loop/opus/G_ruleT_lp/FINDINGS.md (branch claude/project-thread-7uelj0), option B (z read as small/big):
  Y[r, f_a, f_e], T[r, f_a, f_e, side]; sender rows coupled through each 6-spoke's wheel (non-R6 for some q);
  outflow flags resolved through sep3x's RES window; inflow by the conservative per-transition maximum (sound).
  The bound uses the max over flags on the 125-state DP (admissible); exact flag vars are charged at resolution.
- Binary bin/sep3xt (sep3xt.cpp). Output out/wlp3xt_<tag>.txt.
(wlp3x docstring follows)
Job 29 L2 (exploratory): wlp3 + oriented big-big transfer variables, exact row and column generation.

Rule class:
- wlp3's rooted-word rules y (a five sends y[root] to each big neighbour);
- plus x[tau] in [0, XCAP]: charge passed along a big-big edge u -> v of type
  tau = (letter of u, letter of v, the two sides of the edge, unordered).
  A side is (common neighbour c, the vertex at u with c, the vertex at v with c). Letters 7, 8, 9 (9 = >= 9) for u
  and v, 5..9 for the side vertices.
- tau is read from u's 2-ball and, identically, from v's (see sep3x.cpp), so every transfer is counted once
  outgoing and once incoming.

Rows:
- Senders: as wlp3.
- Receivers of exact degree d = 7..DMAXP: y-load + sum over big positions of (x[tau_in] - x[tau_out]) <= d - 6 + t.
  Separated exactly by bin/sep3x (branch and bound with an admissible transfer bound).
- Receivers of degree d > DMAXP (letter 9): y-load + (number of big link positions) * z9 <= d - 6 + t.
  Here z9 >= x[tau] for every tau with to-letter 9, and outflows are dropped (conservative). These rows are separated
  by a max-plus DP; the Karp letter-9 cycle-mean bound covers d > 30 with the same weights.
- Columns: a tau column enters when a separated row first shows it. Unseen columns have zero reduced cost, so at
  convergence the optimum is exact for the full LP over the current pattern set.

Usage: python3 wlp3x.py [notx] [xcap=3] [tag=NAME] [warm=ROWSFILE] pat=... cpat=... w7plus   (as wlp3)
Output: out/wlp3x_<tag>.txt"""
import sys, os, re, subprocess, collections, time, itertools
import numpy as np
import scipy.sparse as sps
from scipy.optimize import linprog
HERE = os.path.dirname(os.path.abspath(__file__))
ARGS0 = sys.argv[1:]
NOTX = 'notx' in ARGS0
XCAP = float(next((a[5:] for a in ARGS0 if a.startswith('xcap=')), '3'))
WARMF = next((a[5:] for a in ARGS0 if a.startswith('warm=')), None)
MANY = int(next((a[5:] for a in ARGS0 if a.startswith('many=')), '40'))
MAXIT = int(next((a[6:] for a in ARGS0 if a.startswith('maxit=')), '100000'))   # 0 = solve the warm rows once, no separation   # rows kept per degree per iteration
ARGS_W = [a for a in ARGS0 if a not in ('notx',) and not a.startswith(('xcap=', 'warm=', 'many=', 'maxit='))]
# Loader exclusions by name (Long Table, 17 Oct): defect-derived verdict files (out/def_*) and oracle stand-ins (hr1_or1)
EXCL = ('hr1_or1',) if os.environ.get('WLP3X_DEF') == '1' else ('out/def_', 'hr1_or1')   # def_ restored once second-engined (WLP3X_DEF=1)
DROPPED = [a for a in ARGS_W if a.startswith(('pat=', 'cpat=')) and any(e in a for e in EXCL)]
ARGS_W = [a for a in ARGS_W if a not in DROPPED]
print('loader excluded %d files by name: %s' % (len(DROPPED), ' '.join(a.split('=', 1)[1] for a in DROPPED)), flush=True)
src = open(os.path.join(HERE, 'wlp3.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(HERE, 'wlp3.py')), 1)
sys.argv = ['wlp3'] + ARGS_W
exec(src[:src.index('A_ub, b_ub = [], []')])
SEP.stdin.close(); SEP.wait()                                     # replace sep3 by sep3x (same static input SF)
TMERGE = 'tmerge' in ARGS0; TZERO = 'tzero' in ARGS0
TFULL = 'tfull' in ARGS0   # option F: z read as its letter 5..9 (G_ruleT_lp option F) instead of small/big
def FL(spoke):             # values of a side's z field: 0 = the spoke is not 6
    return ((5, 6, 7, 8, 9) if TFULL else (0, 1)) if spoke == 6 else (0,)
def BIG(z): return z >= 7 if TFULL else z == 1
def ZOF(spoke, beyond):    # the z field read from an arrangement: spoke letter and the letter beyond it
    return (beyond if TFULL else int(beyond >= 7)) if spoke == 6 else 0
# ---- Rule T variables ----
def rev5(r): return (r[0], r[4], r[3], r[2], r[1])
def canon_root(raw):
    raw = tuple(raw); rv = rev5(raw); return (raw, False) if raw <= rv else (rv, True)
def ykey(raw, fa, fe):
    r, flip = canon_root(raw)
    if flip: fa, fe = fe, fa
    if TMERGE: fa = fe = 0
    if r == rev5(r): fa, fe = min(fa, fe), max(fa, fe)
    return (r, fa, fe)
def tkey(raw, fa, fe, side):
    """T[root, f_a, f_e, side] (G_ruleT_lp option B: z read as small/big), up to the reflection, which swaps the
    flags and the side."""
    r, flip = canon_root(raw)
    if flip: fa, fe, side = fe, fa, ('e' if side == 'a' else 'a')
    if TMERGE: fa = fe = 0
    if r == rev5(r) and (fe, fa, 'e' if side == 'a' else 'a') < (fa, fe, side): fa, fe, side = fe, fa, ('e' if side == 'a' else 'a')
    return (r, fa, fe, side)
YT = sorted({ykey(r, fa, fe) for r in roots for fa in FL(r[1]) for fe in FL(r[4])})
YI = {k: i for i, k in enumerate(YT)}
TAUV = sorted({tkey(r, fa, fe, sd) for r in roots for fa in FL(r[1]) for fe in FL(r[4]) for sd in ('a', 'e')
               if BIG(fa if sd == 'a' else fe)})
TI = {k: i for i, k in enumerate(TAUV)}
print('rule T%s: %d flag-split Y vars (from %d roots), %d tau vars%s%s' % (' option F (z letters)' if TFULL else '', len(YT), len(roots), len(TAUV),
      ', flags merged' if TMERGE else '', ', tau fixed at 0' if TZERO else ''), flush=True)
# inflow completions (conservative per-transition version of G_ruleT_lp section 2(ii)): s_j = 5 between a 6 and a big
# b, rooted at b towards the 6: word (b, X1, X2, X3, 6), side e (the 6), f_e = 1 (z = the receiver, big); its other
# flag f_a is free when X1 = 6. The 6-wheel side condition on the 6's private is dropped (over-counts: sound).
INS = {}   # (b, receiver letter U) -> T vars the five s_j can send to the receiver
for b in (7, 8, 9):
    for U_ in (7, 8, 9):
        S_ = set()
        for X in itertools.product(L, repeat=3):
            if isR5([6, b, X[0], X[1], X[2]]): continue
            for fa in FL(X[0]):
                S_.add(TI[tkey((b, X[0], X[1], X[2], 6), fa, U_ if TFULL else 1, 'e')])
        INS[(b, U_)] = sorted(S_)
if os.environ.get('TCHECK') == '1':   # validation (2): z reads the same T from its side as the five sends
    recv = set(v for k in INS for v in INS[k]); sent = set(TI.values())
    print('TCHECK: T vars %d; receivable at z %d; sent but never receivable %d; receivable but not a T var %d' % (
        len(sent), len(recv), len(sent - recv), len(recv - sent)), flush=True)
# static T section for sep3xt: flag vars per (U, state, choice)
tl = ['TF' if TFULL else 'T']
for U in (7, 8, 9):
    for (wp, sp, wc) in states:
        for sc in L:
            for wn in L:
                if TFULL:   # 36 slots, index 6 c_a + c_e, code 0 = spoke not 6, 1..5 = z letter 5..9
                    fv = [-1] * 36
                    if wc == 5 and not isR5([U, wn, sc, sp, wp]):
                        for fa in FL(wn):
                            for fe in FL(wp):
                                fv[(fa - 4 if fa else 0) * 6 + (fe - 4 if fe else 0)] = YI[ykey((U, wn, sc, sp, wp), fa, fe)]
                else:
                    fv = [-1] * 4
                    if wc == 5 and not isR5([U, wn, sc, sp, wp]):
                        for q in range(4):
                            fa, fe = q >> 1, q & 1
                            if (fa and wn != 6) or (fe and wp != 6): continue
                            fv[q] = YI[ykey((U, wn, sc, sp, wp), fa, fe)]
                tl.append(' '.join(map(str, fv)))
_sf = open(SF).read().split('\n', 1); open(SF, 'w').write(str(len(YT)) + '\n' + _sf[1])   # NV = Y vars in T mode
open(SF, 'a').write('\n'.join(tl) + '\n')
SEPX = subprocess.Popen([os.path.join(HERE, 'bin', 'sep3xt'), SF], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
TAGX = TAG + ('_notx' if NOTX else '_x') + ('_TF' if TFULL else '_T')
NY = len(YT); NT = len(TAUV)
TV = np.zeros(NT)   # current tau values
def tin(U_=9):
    """per big letter b: (max tau over the inflow completions into a receiver of letter U_, its var or -1)."""
    out = {}
    for b in (7, 8, 9):
        best, bv = 0.0, -1
        for v in INS[(b, U_)]:
            if TV[v] > best + 1e-12: best, bv = TV[v], v
        out[b] = (best, bv)
    return out
T0 = time.time()

# ---- tau codes (must match sep3x.cpp) ----
def sidecode(c, a, b): return c * 25 + a * 5 + b
def taucode(f, t, s1, s2):
    lo, hi = min(s1, s2), max(s1, s2); return ((f * 3 + t) * 125 + lo) * 125 + hi
def taus(d, lk, sv):
    """list of (tau_in, tau_out) for the big link positions of arrangement (d, link, s) (strings of digits 5..9)."""
    w = [int(c) - 5 for c in lk]; s = [int(c) - 5 for c in sv]; ui = 0 if d == 7 else 1 if d == 8 else 2; res = []
    for j in range(d):
        if w[j] < 2: continue
        W_ = lambda k: w[k % d]; S_ = lambda k: s[k % d]; lj = w[j] - 2
        to = taucode(ui, lj, sidecode(W_(j - 1), W_(j - 2), S_(j - 1)), sidecode(W_(j + 1), W_(j + 2), S_(j)))
        ti = taucode(lj, ui, sidecode(W_(j - 1), S_(j - 1), W_(j - 2)), sidecode(W_(j + 1), S_(j), W_(j + 2)))
        res.append((ti, to))
    return res
def tau_to(code): return (code // 15625) % 3

# ---- LP storage: rows as dicts over columns 'y<i>', 'x<tau>', 'z9', 't' ----
XCOL = {}                     # tau -> column index (after the y block)
rows, rhs, rinfo = [], [], []
have = set()
def xcol(tau):
    if tau not in XCOL:
        XCOL[tau] = len(XCOL)
        if tau_to(tau) == 2:  # z9 >= x[tau]
            rows.append({('x', tau): 1.0, ('z9',): -1.0}); rhs.append(0.0); rinfo.append(('z9', tau))
    return XCOL[tau]
for w_ in senders:            # sender rows: -sum y[root, f] - sum tau - t <= -1, every bigness of the far vertices
    w_ = list(w_)
    E = [j for j in range(5) if max(w_[j], w_[(j + 1) % 5]) >= 7 and min(w_[j], w_[(j + 1) % 5]) == 6]
    for bits in itertools.product(((5, 6, 7, 8, 9) if TFULL else (0, 1)), repeat=len(E)):
        B = dict(zip(E, bits))
        # coupling (G_ruleT_lp section 1): around each 6-spoke k, the far vertices zL (edge k-1,k) and zR (edge k,k+1)
        # must admit a non-R 6-wheel (5, x[k+1], zR, q, zL, x[k-1]) with letters in their flag sets
        def zset(e):
            if e not in B: return L
            return (B[e],) if TFULL else ((7, 8, 9) if B[e] == 1 else (5, 6))
        if not all(any(not isR6([5, w_[(k + 1) % 5], zR, q, zL, w_[(k - 1) % 5]]) for zR in zset(k) for zL in zset((k - 1) % 5) for q in L)
                   for k in range(5) if w_[k] == 6): continue
        r = collections.defaultdict(float); r[('t',)] = -1.0
        for j in range(5):
            if w_[j] < 7: continue
            raw = tuple(w_[j:] + w_[:j])
            fa = (B[j] if TFULL else int(B[j] == 1)) if raw[1] == 6 else 0
            fe = (B[(j - 1) % 5] if TFULL else int(B[(j - 1) % 5] == 1)) if raw[4] == 6 else 0
            r[('y', YI[ykey(raw, fa, fe)])] -= 1.0
            if BIG(fa): r[('tau', TI[tkey(raw, fa, fe, 'a')])] -= 1.0
            if BIG(fe): r[('tau', TI[tkey(raw, fa, fe, 'e')])] -= 1.0
        rows.append(dict(r)); rhs.append(-1.0); rinfo.append(('sender', ''.join(map(str, w_)) + ('/' + ''.join(map(str, bits)) if E else '')))
print('sender rows: %d' % sum(1 for i_ in rinfo if i_[0] == 'sender'), flush=True)
def recv_row(d, lk, sv, TN):
    """receiver row of an exact-d arrangement (d <= DMAXP), inflow completions TN[b] = var or -1."""
    U = min(d, 9); w = [int(c) for c in lk]; s_ = [int(c) for c in sv]
    r = collections.defaultdict(float); r[('t',)] = -1.0
    for i in range(d):
        if w[i] == 5:
            fa = ZOF(w[(i + 1) % d], w[(i + 2) % d]); fe = ZOF(w[(i - 1) % d], w[(i - 2) % d])
            r[('y', YI[ykey((U, w[(i + 1) % d], s_[i], s_[(i - 1) % d], w[(i - 1) % d]), fa, fe)])] += 1.0
        a_, b_ = w[i], w[(i + 1) % d]
        if s_[i] == 5 and min(a_, b_) == 6 and max(a_, b_) >= 7 and TN[max(a_, b_)] >= 0: r[('tau', TN[max(a_, b_)])] += 1.0
    if not NOTX:
        for ti, to in taus(d, lk, sv):
            xcol(ti); xcol(to); r[('x', ti)] += 1.0; r[('x', to)] -= 1.0
    return {k: v for k, v in r.items() if v != 0.0}
def add_recv(d, lk, sv, kind='recv'):
    TN = {b: v for b, (_, v) in tin(min(d, 9)).items()}
    key = (d, lk, sv, TN[7], TN[8], TN[9])
    if key in have: return False
    have.add(key); rows.append(recv_row(d, lk, sv, TN)); rhs.append(d - 6.0); rinfo.append((kind, d, lk, sv)); return True

# ---- DP rows for d > DMAXP (letter 9): y + z9 per big position ----
BIGSTATE = np.array([1.0 if states[a][2] >= 7 else 0.0 for a in range(NS)])
def tri9w(yv):
    """letter-9 transitions with Rule T weights: max over the flags (conservative: the far letters are not in the
    state) plus the inflow constant. Returns (a, b, weight, terms)."""
    TN = tin(9); out = []
    for a, b, rr in TRI[9]:
        (wp, sp, wc), (_, sc, wn) = states[a], states[b]; val, terms = 0.0, []
        if wc == 5:
            best = None
            for fa in FL(wn):
                for fe in FL(wp):
                    v = YI[ykey((9, wn, sc, sp, wp), fa, fe)]
                    if best is None or yv[v] > yv[best]: best = v
            val += yv[best]; terms.append(('y', best))
        if sc == 5 and min(wc, wn) == 6 and max(wc, wn) >= 7 and TN[max(wc, wn)][1] >= 0:
            val += TN[max(wc, wn)][0]; terms.append(('tau', TN[max(wc, wn)][1]))
        out.append((a, b, val, tuple(terms)))
    return out
def dp9(d, yv, z9, thr, many=40):
    U = 9; M = np.full((NS, NS), -np.inf); RM = {}
    for a, b, wv, terms in tri9w(yv):
        val = wv + z9 * BIGSTATE[a]
        if val > M[a, b]: M[a, b] = val; RM[a, b] = terms
    P = [None, M]; back = [None, None]
    for k in range(2, d + 1):
        C = P[-1][:, :, None] + M[None, :, :]; back.append(C.argmax(axis=1)); P.append(C.max(axis=1))
    diag = np.diag(P[d]); out = []
    for a0 in np.argsort(-diag)[:many]:
        if diag[a0] <= thr: break
        a0 = int(a0); path = []; nbig = 0; b = a0; seq = []
        for k in range(d, 1, -1):
            c = back[k][a0, b]; path.append(RM[c, b]); seq.append(c); b = c
        path.append(RM[a0, b]); seq.append(a0)
        nbig = int(sum(BIGSTATE[q] for q in seq))
        out.append((float(diag[a0]), tuple(sorted(x for p in path for x in p)), nbig))
    return out
have9 = set()
def add_row9(d, path, nbig):
    key = (d, path, nbig)
    if key in have9: return False
    have9.add(key); r = collections.defaultdict(float); r[('t',)] = -1.0
    for p in path: r[p] += 1.0
    if nbig and not NOTX: r[('z9',)] += float(nbig)
    rows.append(dict(r)); rhs.append(d - 6.0); rinfo.append(('recv9', d, nbig, path)); return True

# ---- separation through sep3x ----
def sepx(d, yv, xv, thr, many):
    xs = [(tau, v) for tau, v in xv.items() if v > 1e-12]
    TN = tin(min(d, 9))
    SEPX.stdin.write('q %d %.12f %d %d\n%s\nX %d %s\nT %.12f %.12f %.12f %d %d %d\n' % (d, thr, many, OMAX, ' '.join('%.12f' % x for x in yv),
                     len(xs), ' '.join('%d %.12f' % kv for kv in xs), TN[7][0], TN[8][0], TN[9][0], TN[7][1], TN[8][1], TN[9][1]))
    SEPX.stdin.flush(); out = []
    while True:
        f = SEPX.stdout.readline().split()
        if not f: raise RuntimeError('sep3x died')
        if f[0] == 'END': return out
        out.append((float(f[1]), f[2], f[3]))

def solve():
    nx = len(XCOL); nc = NY + nx + NT + 2; IZ, IT = NY + nx + NT, NY + nx + NT + 1
    data, ri, ci = [], [], []
    for k, r in enumerate(rows):
        for key, v in r.items():
            c = key[1] if key[0] == 'y' else (NY + XCOL[key[1]] if key[0] == 'x' else (NY + nx + key[1] if key[0] == 'tau' else (IZ if key[0] == 'z9' else IT)))
            data.append(v); ri.append(k); ci.append(c)
    A = sps.csr_matrix((data, (ri, ci)), shape=(len(rows), nc))
    cvec = np.zeros(nc); cvec[IT] = 1.0
    bounds = [(0, 1)] * NY + [(0, XCAP if not NOTX else 0)] * nx + [(0, 0 if TZERO else 1)] * NT + [(0, XCAP if not NOTX else 0), (None, None)]
    res = linprog(cvec, A_ub=A, b_ub=np.array(rhs), bounds=bounds, method='highs')
    if res.status != 0: raise RuntimeError('LP status %s %s' % (res.status, res.message))
    yv = res.x[:NY]; xv = {tau: res.x[NY + i] for tau, i in XCOL.items()}; z9 = res.x[IZ]; t = res.x[IT]
    TV[:] = res.x[NY + nx:NY + nx + NT]
    return res, yv, xv, z9, t

def check(d, lk, sv):
    SEPX.stdin.write('c %d %s %s\n' % (d, lk, sv)); SEPX.stdin.flush(); return SEPX.stdout.readline().strip() == '1'
# warm start: receiver rows of an earlier run (lines '... receiver d=<d> link <lk> s <sv>')
if WARMF:
    nw = 0
    for line in open(WARMF):
        m = re.search(r'receiver d=(\d+) link (\d+) s (\d+)', line)
        if m and int(m.group(1)) <= DMAXP:
            d, lk, sv = int(m.group(1)), m.group(2), m.group(3)
            if check(d, lk, sv) and add_recv(d, lk, sv, 'warm'): nw += 1
    print('warm rows', nw, flush=True)
DS, DSF = list(range(7, 13)), list(range(7, 31))
it = 0
while True:
    res, yv, xv, z9, t = solve()
    if it >= MAXIT: break
    added = 0
    for dl in (DS, DSF):
        for d in dl:
            thr = d - 6 + t + 1e-7
            if d <= DMAXP:
                for wgt, lk, sv in sepx(d, yv, {} if NOTX else xv, thr, MANY): added += add_recv(d, lk, sv)
            else:
                for wgt, path, nbig in dp9(d, yv, 0.0 if NOTX else z9, thr, MANY): added += add_row9(d, path, nbig)
        if added: break
    print('iter %d t=%.6f rows %d xcols %d z9=%.4f added %d (%.0fs)' % (it, t, len(rows), len(XCOL), z9, added, time.time() - T0), flush=True)
    it += 1
    if it % 5 == 0:   # row dump for warm restarts
        open(os.path.join(HERE, 'out', 'wlp3xt_%s_rows.txt' % TAGX), 'w').write(''.join(
            '  receiver d=%d link %s s %s\n' % (i_[1], i_[2], i_[3]) for i_ in rinfo if i_[0] in ('recv', 'warm')))
    if not added: break
res, yv, xv, z9, t = solve()
duals = -res.ineqlin.marginals
if os.environ.get('TSELF') == '1':   # validation: sep3xt's reported weights equal the Python row values
    import random as _rnd; _rnd.seed(5)
    ysc = float(os.environ.get('TSELF_YSCALE', '1')); yv = np.array([_rnd.random() * ysc for _ in range(NY)]); TV[:] = [_rnd.random() * 0.5 for _ in range(NT)]
    worst = 0.0; nrow = 0; nin = 0
    for d in range(7, 11):
        TN = {b: v for b, (_, v) in tin(min(d, 9)).items()}
        for wgt, lk, sv in sepx(d, yv, {}, d - 6.0, 40):
            r_ = recv_row(d, lk, sv, TN)
            val = sum(c * (yv[k[1]] if k[0] == 'y' else TV[k[1]] if k[0] == 'tau' else 0.0) for k, c in r_.items() if k[0] in ('y', 'tau'))
            nin += any(k[0] == 'tau' for k in r_); worst = max(worst, abs(val - wgt)); nrow += 1
    print('TSELF: random y and T; %d separated rows (%d with inflow), max |sep weight - Python row value| = %.3g' % (nrow, nin, worst), flush=True)
    sys.exit(0)
out = ['# wlp3x %s: %s; t* = %.6f; %d rows, %d transfer columns, z9 = %.4f, xcap %.1f' % (
    ' '.join(ARGS0), 'TRANSFERS OFF' if NOTX else 'transfers on', t, len(rows), len(XCOL), z9, XCAP)]
out.append('dual certificate (rows with positive weight):')
for k, dv in enumerate(duals):
    if dv > 1e-9:
        inf = rinfo[k]
        if inf[0] in ('recv', 'warm'): out.append('  %.4f  receiver d=%d link %s s %s' % (dv, inf[1], inf[2], inf[3]))
        elif inf[0] == 'recv9': out.append('  %.4f  receiver9 d=%d nbig=%d terms %s' % (dv, inf[1], inf[2], inf[3]))
        elif inf[0] == 'sender': out.append('  %.4f  sender %s' % (dv, inf[1]))
        else: out.append('  %.4f  %s' % (dv, inf))
nzx = sorted(((v, tau) for tau, v in xv.items() if v > 1e-9), reverse=True)
out.append('nonzero transfers: %d (top 20 by value):' % len(nzx))
for v, tau in nzx[:20]:
    f, t_ = tau // 15625 // 3, (tau // 15625) % 3; lo, hi = (tau // 125) % 125, tau % 125
    dec = lambda c: '%d%d%d' % (c // 25 + 5, c // 5 % 5 + 5, c % 5 + 5)
    out.append('  x[%d->%d | %s,%s] = %.4f' % (f + 7, t_ + 7, dec(lo), dec(hi), v))
# per-d max load at the optimum
for d in range(7, 31):
    if d <= DMAXP:
        r_ = sepx(d, yv, {} if NOTX else xv, -1e9, 1); v = r_[0][0] if r_ else 0.0
    else:
        r_ = dp9(d, yv, 0.0 if NOTX else z9, -1e18, 1); v = r_[0][0] if r_ else 0.0
    out.append('d=%d: max receiver load %.6f vs d-6+t = %.6f' % (d, v, d - 6 + t))
# Karp letter-9 tail with z9 per big position
Mk = np.full((NS, NS), -np.inf)
for a, b, wv, _ in tri9w(yv):
    val = wv + (0.0 if NOTX else z9) * BIGSTATE[a]
    Mk[a, b] = max(Mk[a, b], val)
n_ = NS; Dk = np.full((n_ + 1, n_), -np.inf); Dk[0, :] = 0.0
for k in range(1, n_ + 1): Dk[k] = (Dk[k - 1][:, None] + Mk).max(axis=0)
with np.errstate(invalid='ignore'):
    q = np.where(np.isfinite(Dk[n_]), np.min(np.where(np.isfinite(Dk[:n_]), (Dk[n_] - Dk[:n_]) / (n_ - np.arange(n_))[:, None], np.inf), axis=0), -np.inf)
lam = q.max()
out.append('letter-9 max cycle mean (with z9) lambda = %.6f; d*lambda <= d-6+t for all d >= %s' % (
    lam, ('%.2f' % ((6 - t) / (1 - lam))) if lam < 1 else 'never'))
import json
nzt = sorted(((TV[i], k) for k, i in TI.items() if TV[i] > 1e-9), reverse=True)
out.append('nonzero T (rule T): %d (top 20): %s' % (len(nzt), '; '.join('%s|%d%d%s %.4f' % (''.join(map(str, k[0])), k[1], k[2], k[3], v) for v, k in nzt[:20])))
json.dump({'t': float(t), 'z9': float(z9), 'yT': {'%s|%d%d' % (''.join(map(str, k[0])), k[1], k[2]): float(yv[i]) for k, i in YI.items() if yv[i] > 1e-12},
           'tau': {'%s|%d%d%s' % (''.join(map(str, k[0])), k[1], k[2], k[3]): float(TV[i]) for k, i in TI.items() if TV[i] > 1e-12},
           'x': {str(tau): float(v) for tau, v in xv.items() if v > 1e-12}, 'args': ARGS0},
          open(os.path.join(HERE, 'out', 'wlp3xt_%s_sol.json' % TAGX), 'w'))
SEPX.stdin.close(); SEPX.wait()
open(os.path.join(HERE, 'out', 'wlp3xt_%s.txt' % TAGX), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out[:60]))
