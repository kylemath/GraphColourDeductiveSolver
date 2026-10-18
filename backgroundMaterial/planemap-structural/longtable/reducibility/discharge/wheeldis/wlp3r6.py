"""Job 31 (exploratory): wlp3x.py (L2) + the 6-relay (out/job31/RUNLOG.md).
- y56[r]: a five sends to a 6-neighbour (r = the five's word rooted at the 6); y6b[q]: a six passes to a big neighbour
  (q = the six's wheel word rooted at the big).
- Senders: sum y (bigs) + sum y56 (sixes) >= 1 - t. Sixes: for every non-R6 link word, with the maximising s letters
  (max-plus DP over the cycle): sum y56 - sum y6b <= t. Bigs: L2 + the inflow from each link 6, y6b at its private's
  current maximum (one row per completion, lazily; bin/sep3r).
- Option rzero: y56 = y6b = 0 (validation: must reproduce wlp3x exactly). Output out/wlp3r6_<tag>.txt.
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
LPM = next((a[3:] for a in ARGS0 if a.startswith('lp=')), 'highs')   # lp=ds: HiGHS dual simplex (Job 31 restart, LT 22:13Z)
LPM = {'ds': 'highs-ds', 'ipm': 'highs-ipm'}.get(LPM, LPM)
MANY6 = int(next((a[6:] for a in ARGS0 if a.startswith('many6=')), '0'))   # six-row cap per iteration (0 = MANY)
DROPK = int(next((a[5:] for a in ARGS0 if a.startswith('drop=')), '0'))   # drop cut rows slack for >= DROPK consecutive solves (0 = keep all)
ARGS_W = [a for a in ARGS0 if a not in ('notx',) and not a.startswith(('xcap=', 'warm=', 'many=', 'maxit=', 'lp=', 'drop=', 'many6='))]
# Loader exclusions by name (Long Table, 17 Oct): defect-derived verdict files (out/def_*) and oracle stand-ins (hr1_or1)
EXCL = ('hr1_or1',) if os.environ.get('WLP3X_DEF') == '1' else ('out/def_', 'hr1_or1')   # def_ restored once second-engined (WLP3X_DEF=1)
DROPPED = [a for a in ARGS_W if a.startswith(('pat=', 'cpat=')) and any(e in a for e in EXCL)]
ARGS_W = [a for a in ARGS_W if a not in DROPPED]
print('loader excluded %d files by name: %s' % (len(DROPPED), ' '.join(a.split('=', 1)[1] for a in DROPPED)), flush=True)
src = open(os.path.join(HERE, 'wlp3.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(HERE, 'wlp3.py')), 1)
sys.argv = ['wlp3'] + ARGS_W
exec(src[:src.index('A_ub, b_ub = [], []')])
SEP.stdin.close(); SEP.wait()                                     # replace sep3 by sep3x (same static input SF)
RZERO = 'rzero' in ARGS0
# ---- 6-relay variables ----
R56 = sorted({root(list(w), j) for w in senders for j in range(5) if w[j] == 6})
I56 = {r: i for i, r in enumerate(R56)}
def canon6(w):
    w = tuple(w); return min(min(s_[k:] + s_[:k] for k in range(6)) for s_ in (w, w[::-1]))
W6 = sorted({canon6(w) for w in itertools.product(L, repeat=6) if not isR6(list(w))})
R6B = sorted({root(list(w), j) for w in W6 for j in range(6) if w[j] >= 7})
I6B = {q: i for i, q in enumerate(R6B)}
N56, N6B = len(R56), len(R6B)
print('6-relay: %d y56 vars, %d y6b vars, %d non-R6 link words%s' % (N56, N6B, len(W6), ', y56 = y6b = 0' if RZERO else ''), flush=True)
def cand6(U, wn, sc, sp, wp):
    """y6b vars a link 6 at w_i can pass to a big receiver of letter U: its wheel (U, wn, sc, p, sp, wp) over non-R6 p."""
    return [I6B[root([U, wn, sc, p, sp, wp], 0)] for p in L if not isR6([U, wn, sc, p, sp, wp])]
rl = ['R']
for U in (7, 8, 9):
    for (wp, sp, wc) in states:
        for sc in L:
            for wn in L:
                c_ = cand6(U, wn, sc, sp, wp) if wc == 6 else []
                rl.append(' '.join(map(str, (c_ + [-1] * 5)[:5])))
open(SF, 'a').write('\n'.join(rl) + '\n')
if os.environ.get('RCHECK') == '1':   # validation 2: every y6b a six sends is receivable at its big, and back
    recv = set()
    for U in (7, 8, 9):
        for (wp, sp, wc) in states:
            for sc in L:
                for wn in L:
                    if wc == 6: recv.update(cand6(U, wn, sc, sp, wp))
    sent = {I6B[root(list(Lw), j)] for Lw in W6 for j in range(6) if Lw[j] >= 7}
    # independent enumerator: raw 6-tuples rooted at a big, non-R6, canonical by brute force over reflections
    raw = set()
    for w in itertools.product(L, repeat=6):
        if w[0] >= 7 and not isR6(list(w)): raw.add(min(w, (w[0],) + tuple(reversed(w[1:]))))
    raw56 = set()
    for w in itertools.product(L, repeat=5):
        if w[0] == 6 and not isR5(list(w)) and max(w) >= 7: raw56.add(min(w, (w[0],) + tuple(reversed(w[1:]))))
    print('RCHECK: y6b %d (independent enumerator %d, equal %s); y56 %d (independent %d, equal %s); sent %d, receivable %d, sent-not-receivable %d, receivable-not-sent %d' % (
        N6B, len(raw), raw == set(R6B), N56, len(raw56), raw56 == set(R56), len(sent), len(recv), len(sent - recv), len(recv - sent)), flush=True)
SEPX = subprocess.Popen([os.path.join(HERE, 'bin', 'sep3r'), SF], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
TAGX = TAG + ('_notx' if NOTX else '_x') + '_R6'
V6B = np.zeros(N6B)   # current y6b values
V56 = np.zeros(N56)
def best6(U, wn, sc, sp, wp):
    """(value, var) of the current maximum over the private, same tie rule as sep3r (first strictly larger)."""
    best, bv = 0.0, -1
    for v in cand6(U, wn, sc, sp, wp):
        if V6B[v] > best + 1e-15: best, bv = V6B[v], v
    return best, bv
NY = len(roots)
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
for w_ in senders:            # sender rows: -sum y - t <= -1
    r = collections.defaultdict(float); r[('t',)] = -1.0
    for j in range(5):
        if w_[j] >= 7: r[('y', ix[root(list(w_), j)])] -= 1.0
        if w_[j] == 6: r[('y56', I56[root(list(w_), j)])] -= 1.0
    rows.append(dict(r)); rhs.append(-1.0); rinfo.append(('sender', ''.join(map(str, w_))))
def recv_row(d, lk, sv):
    """receiver row of an exact-d arrangement (d <= DMAXP)."""
    U = min(d, 9); w = [int(c) for c in lk]; s_ = [int(c) for c in sv]
    r = collections.defaultdict(float); r[('t',)] = -1.0
    for i in range(d):
        if w[i] == 5:
            rt = root([U, w[(i + 1) % d], s_[i], s_[(i - 1) % d], w[(i - 1) % d]], 0); r[('y', ix[rt])] += 1.0
    if not NOTX:
        for ti, to in taus(d, lk, sv):
            xcol(ti); xcol(to); r[('x', ti)] += 1.0; r[('x', to)] -= 1.0
    for i in range(d):   # six inflow at the current maximum over the private
        if w[i] == 6:
            bv = best6(U, w[(i + 1) % d], s_[i], s_[(i - 1) % d], w[(i - 1) % d])[1]
            if bv >= 0: r[('y6b', bv)] += 1.0
    return {k: v for k, v in r.items() if v != 0.0}
def add_recv(d, lk, sv, kind='recv'):
    rr = recv_row(d, lk, sv)
    key = (d, lk, sv, tuple(sorted(k for k in rr if k[0] == 'y6b')))
    if key in have: return False
    have.add(key); rows.append(rr); rhs.append(d - 6.0); rinfo.append((kind, d, lk, sv)); return True

# ---- DP rows for d > DMAXP (letter 9): y + z9 per big position ----
BIGSTATE = np.array([1.0 if states[a][2] >= 7 else 0.0 for a in range(NS)])
def dp9(d, yv, z9, thr, many=40):
    U = 9; M = np.full((NS, NS), -np.inf); RM = {}
    for a, b, rr in TRI[U]:
        (wp, sp, wc), (_, sc, wn) = states[a], states[b]
        terms = ((('y', ix[rr]),) if rr is not None else ())
        val = (yv[ix[rr]] if rr is not None else 0.0) + z9 * BIGSTATE[a]
        if wc == 6:
            bvl, bv = best6(9, wn, sc, sp, wp)
            if bv >= 0: val += bvl; terms = terms + (('y6b', bv),)
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
    SEPX.stdin.write('q %d %.12f %d %d\n%s\nX %d %s\nR %d %s\n' % (d, thr, many, OMAX, ' '.join('%.12f' % x for x in yv),
                     len(xs), ' '.join('%d %.12f' % kv for kv in xs), N6B, ' '.join('%.12f' % x for x in V6B)))
    SEPX.stdin.flush(); out = []
    while True:
        f = SEPX.stdout.readline().split()
        if not f: raise RuntimeError('sep3x died')
        if f[0] == 'END': return out
        out.append((float(f[1]), f[2], f[3]))

def six_sep(v56, t, many=200):
    """six rows violated at (v56, V6B, t): for each non-R6 link word, the s letters maximising sum y56 (max-plus over
    the 6-cycle), minus the link bigs' y6b; returns [(value, link, s)] above t."""
    out = []
    for Lw in W6:
        Ms = []
        for i in range(6):   # M_i[s_{i-1}][s_i]: the term of the link vertex at position i
            M = np.zeros((5, 5)); wn, wp = Lw[(i + 1) % 6], Lw[(i - 1) % 6]
            for a_, sp in enumerate(L):
                for b_, sc in enumerate(L):
                    if Lw[i] == 5:
                        w5 = [6, wn, sc, sp, wp]
                        M[a_, b_] = -np.inf if isR5(w5) else v56[I56[root(w5, 0)]]
                    elif Lw[i] == 6:
                        if all(isR6([6, wn, sc, p, sp, wp]) for p in L): M[a_, b_] = -np.inf
            Ms.append(M)
        P = Ms[0]
        for M in Ms[1:]: P = (P[:, :, None] + M[None, :, :]).max(axis=1)
        dg = np.diag(P); a0 = int(dg.argmax()); best = dg[a0]
        if not np.isfinite(best): continue
        outv = sum(V6B[I6B[root(list(Lw), j)]] for j in range(6) if Lw[j] >= 7)
        if best - outv <= t + 1e-7: continue
        # backtrack the s letters (s_5 = index a0 closes the cycle)
        s_ = [None] * 6; s_[5] = a0; cur = a0
        Pk = [Ms[0]]
        for M in Ms[1:]: Pk.append((Pk[-1][:, :, None] + M[None, :, :]).max(axis=1))
        for i in range(5, 0, -1):
            col = Pk[i - 1][a0, :] + Ms[i][:, cur]; prv = int(col.argmax()); s_[i - 1] = prv; cur = prv
        out.append((best - outv, Lw, tuple(L[k] for k in s_)))
    out.sort(key=lambda x: -x[0]); return out[:many]
have6 = set()
def add_six(Lw, sv):
    key = (Lw, sv)
    if key in have6: return False
    have6.add(key); r = collections.defaultdict(float); r[('t',)] = -1.0
    for i in range(6):
        if Lw[i] == 5: r[('y56', I56[root([6, Lw[(i + 1) % 6], sv[i], sv[(i - 1) % 6], Lw[(i - 1) % 6]], 0)])] += 1.0
        elif Lw[i] >= 7: r[('y6b', I6B[root(list(Lw), i)])] -= 1.0
    rows.append(dict(r)); rhs.append(0.0); rinfo.append(('six', ''.join(map(str, Lw)), ''.join(map(str, sv)))); return True

def solve():
    nx = len(XCOL); B56 = NY + nx; B6B = B56 + N56; nc = B6B + N6B + 2; IZ, IT = nc - 2, nc - 1
    data, ri, ci = [], [], []
    for k, r in enumerate(rows):
        for key, v in r.items():
            c = key[1] if key[0] == 'y' else (NY + XCOL[key[1]] if key[0] == 'x' else (B56 + key[1] if key[0] == 'y56' else
                (B6B + key[1] if key[0] == 'y6b' else (IZ if key[0] == 'z9' else IT))))
            data.append(v); ri.append(k); ci.append(c)
    A = sps.csr_matrix((data, (ri, ci)), shape=(len(rows), nc))
    cvec = np.zeros(nc); cvec[IT] = 1.0
    bounds = [(0, 1)] * NY + [(0, XCAP if not NOTX else 0)] * nx + [(0, 0 if RZERO else 1)] * (N56 + N6B) + [(0, XCAP if not NOTX else 0), (None, None)]
    res = linprog(cvec, A_ub=A, b_ub=np.array(rhs), bounds=bounds, method=LPM)
    if res.status != 0: raise RuntimeError('LP status %s %s' % (res.status, res.message))
    yv = res.x[:NY]; xv = {tau: res.x[NY + i] for tau, i in XCOL.items()}; z9 = res.x[IZ]; t = res.x[IT]
    global V56; V56 = res.x[B56:B56 + N56]; V6B[:] = res.x[B6B:B6B + N6B]
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
            continue
        m = re.search(r'six link (\d+) s (\d+)', line)
        if m: nw += add_six(tuple(int(c) for c in m.group(1)), tuple(int(c) for c in m.group(2))); continue
        m = re.search(r'recv9 d=(\d+) nbig=(\d+) path (.*)$', line)
        if m: import ast as _ast; nw += add_row9(int(m.group(1)), _ast.literal_eval(m.group(3)), int(m.group(2)))
    print('warm rows', nw, flush=True)
DS, DSF = list(range(7, 13)), list(range(7, 31))
AGE = []                                # consecutive solves with positive slack, per row (cut rows only)
CUT = ('recv', 'warm', 'six', 'recv9')
def unkey(k):
    inf = rinfo[k]
    if inf[0] in ('recv', 'warm'): have.discard((inf[1], inf[2], inf[3], tuple(sorted(q for q in rows[k] if q[0] == 'y6b'))))
    elif inf[0] == 'six': have6.discard((tuple(int(c) for c in inf[1]), tuple(int(c) for c in inf[2])))
    elif inf[0] == 'recv9': have9.discard((inf[1], inf[3], inf[2]))
def dump_all():
    L_ = []
    for k, inf in enumerate(rinfo):
        a_ = AGE[k] if k < len(AGE) else 0
        if inf[0] in ('recv', 'warm'): L_.append('  receiver d=%d link %s s %s age %d\n' % (inf[1], inf[2], inf[3], a_))
        elif inf[0] == 'six': L_.append('  six link %s s %s age %d\n' % (inf[1], inf[2], a_))
        elif inf[0] == 'recv9': L_.append('  recv9 d=%d nbig=%d path %r\n' % (inf[1], inf[2], inf[3]))
    open(os.path.join(HERE, 'out', 'wlp3r6_%s_rows_all.txt' % TAGX), 'w').write(''.join(L_))
it = 0; ndrop = 0
while True:
    res, yv, xv, z9, t = solve()
    if DROPK:
        sl = np.asarray(res.ineqlin.residual); AGE += [0] * (len(rows) - len(AGE))
        for k in range(len(rows)): AGE[k] = AGE[k] + 1 if (sl[k] > 1e-9 and rinfo[k][0] in CUT) else 0
    n0 = len(rows)                      # rows present at this solve (separation may also append z9 rows via xcol)
    if it >= MAXIT: break
    added = 0
    for v_, Lw, sv in six_sep(V56, t, MANY6 or MANY): added += add_six(Lw, sv)
    for dl in (DS, DSF):
        for d in dl:
            thr = d - 6 + t + 1e-7
            if d <= DMAXP:
                for wgt, lk, sv in sepx(d, yv, {} if NOTX else xv, thr, MANY): added += add_recv(d, lk, sv)
            else:
                for wgt, path, nbig in dp9(d, yv, 0.0 if NOTX else z9, thr, MANY): added += add_row9(d, path, nbig)
        if added: break
    nd = 0
    if DROPK and added:   # drop only when new rows came in, so the final solve is over a row set the iterate satisfies
        keep = [k for k in range(len(rows)) if k >= n0 or AGE[k] < DROPK]
        for k in range(n0):
            if AGE[k] >= DROPK: unkey(k)
        nd = len(rows) - len(keep); ndrop += nd
        rows[:] = [rows[k] for k in keep]; rhs[:] = [rhs[k] for k in keep]; rinfo[:] = [rinfo[k] for k in keep]
        AGE[:] = [AGE[k] if k < n0 else 0 for k in keep]
    print('iter %d t=%.6f rows %d xcols %d z9=%.4f added %d%s (%.0fs)' % (it, t, len(rows), len(XCOL), z9, added,
          (' dropped %d' % nd) if DROPK else '', time.time() - T0), flush=True)
    if DROPK: dump_all()
    it += 1
    if it % 5 == 0:   # row dump for warm restarts
        open(os.path.join(HERE, 'out', 'wlp3r6_%s_rows.txt' % TAGX), 'w').write(''.join(
            '  receiver d=%d link %s s %s\n' % (i_[1], i_[2], i_[3]) for i_ in rinfo if i_[0] in ('recv', 'warm')))
    if not added: break
if not DROPK: res, yv, xv, z9, t = solve()   # with drop=, the last solve is already over the final rows
duals = -res.ineqlin.marginals
if os.environ.get('RSELF') == '1':   # validation 3: separator weights = Python rows; six DP = brute force
    import random as _r; _r.seed(4); sc_ = float(os.environ.get('RSELF_YSCALE', '1'))
    yv = np.array([_r.random() * sc_ for _ in range(NY)]); V6B[:] = [_r.random() for _ in range(N6B)]
    V56 = np.array([_r.random() for _ in range(N56)]); worst = 0.0; nrow = nin = 0
    for d in range(7, 11):
        for wgt, lk, sv in sepx(d, yv, {}, d - 6.0, 40):
            r_ = recv_row(d, lk, sv)
            val = sum(c * (yv[k[1]] if k[0] == 'y' else V6B[k[1]] if k[0] == 'y6b' else 0.0) for k, c in r_.items() if k[0] in ('y', 'y6b'))
            nin += any(k[0] == 'y6b' for k in r_); worst = max(worst, abs(val - wgt)); nrow += 1
    bad6 = 0; n6 = 0
    for Lw in W6[:200]:
        best = -np.inf
        for sv in itertools.product(L, repeat=6):
            v_ = 0.0; ok = True
            for i in range(6):
                wn, wp, sc, sp = Lw[(i + 1) % 6], Lw[(i - 1) % 6], sv[i], sv[(i - 1) % 6]
                if Lw[i] == 5:
                    if isR5([6, wn, sc, sp, wp]): ok = False; break
                    v_ += V56[I56[root([6, wn, sc, sp, wp], 0)]]
                elif Lw[i] == 6 and all(isR6([6, wn, sc, p, sp, wp]) for p in L): ok = False; break
            if ok: best = max(best, v_)
        outv = sum(V6B[I6B[root(list(Lw), j)]] for j in range(6) if Lw[j] >= 7)
        got = [x for x in six_sep(V56, -1e9, 10**6) if x[1] == Lw]
        dp = got[0][0] if got else -np.inf
        n6 += 1; bad6 += not ((not np.isfinite(best) and not got) or abs((best - outv) - dp) < 1e-9)
    print('RSELF: %d separated big rows (%d with six inflow), max |sep weight - Python row| = %.3g; six DP vs brute force: %d link words, %d mismatches' % (nrow, nin, worst, n6, bad6), flush=True)
    sys.exit(0)
out = ['# wlp3x %s: %s; t* = %.6f; %d rows, %d transfer columns, z9 = %.4f, xcap %.1f' % (
    ' '.join(ARGS0), 'TRANSFERS OFF' if NOTX else 'transfers on', t, len(rows), len(XCOL), z9, XCAP)]
out.append('dual certificate (rows with positive weight):')
for k, dv in enumerate(duals):
    if dv > 1e-9:
        inf = rinfo[k]
        if inf[0] in ('recv', 'warm'): out.append('  %.4f  receiver d=%d link %s s %s' % (dv, inf[1], inf[2], inf[3]))
        elif inf[0] == 'recv9': out.append('  %.4f  receiver9 d=%d nbig=%d roots %s' % (dv, inf[1], inf[2], ' '.join('%d|%s' % (r_[0], ''.join(map(str, r_[1:]))) for r_ in inf[3])))
        elif inf[0] == 'sender': out.append('  %.4f  sender %s' % (dv, inf[1]))
        elif inf[0] == 'six': out.append('  %.4f  six link %s s %s' % (dv, inf[1], inf[2]))
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
for a, b, rr in TRI[9]:
    (wp, sp, wc), (_, sc, wn) = states[a], states[b]
    val = (yv[ix[rr]] if rr is not None else 0.0) + (0.0 if NOTX else z9) * BIGSTATE[a]
    if wc == 6: val += best6(9, wn, sc, sp, wp)[0]
    Mk[a, b] = max(Mk[a, b], val)
n_ = NS; Dk = np.full((n_ + 1, n_), -np.inf); Dk[0, :] = 0.0
for k in range(1, n_ + 1): Dk[k] = (Dk[k - 1][:, None] + Mk).max(axis=0)
with np.errstate(invalid='ignore'):
    q = np.where(np.isfinite(Dk[n_]), np.min(np.where(np.isfinite(Dk[:n_]), (Dk[n_] - Dk[:n_]) / (n_ - np.arange(n_))[:, None], np.inf), axis=0), -np.inf)
lam = q.max()
out.append('letter-9 max cycle mean (with z9) lambda = %.6f; d*lambda <= d-6+t for all d >= %s' % (
    lam, ('%.2f' % ((6 - t) / (1 - lam))) if lam < 1 else 'never'))
import json
json.dump({'t': float(t), 'z9': float(z9), 'y': {'%d|%s' % (r_[0], ''.join(map(str, r_[1:]))): float(yv[ix[r_]]) for r_ in roots if yv[ix[r_]] > 1e-12},
           'x': {str(tau): float(v) for tau, v in xv.items() if v > 1e-12},
           'y56': {''.join(map(str, r_)): float(V56[i]) for r_, i in I56.items() if V56[i] > 1e-12},
           'y6b': {''.join(map(str, q_)): float(V6B[i]) for q_, i in I6B.items() if V6B[i] > 1e-12}, 'args': ARGS0},
          open(os.path.join(HERE, 'out', 'wlp3r6_%s_sol.json' % TAGX), 'w'))
SEPX.stdin.close(); SEPX.wait()
open(os.path.join(HERE, 'out', 'wlp3r6_%s.txt' % TAGX), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out[:60]))
