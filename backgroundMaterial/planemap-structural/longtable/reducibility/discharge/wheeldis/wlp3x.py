"""Job 29 L2 (exploratory): wlp3 + oriented big-big transfer variables, exact row and column generation.

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
import sys, os, re, subprocess, collections, time
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
SEPX = subprocess.Popen([os.path.join(HERE, 'bin', 'sep3x' + ('f' if os.environ.get('WLP_SEPF') == '1' else '')), SF], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
TAGX = TAG + ('_notx' if NOTX else '_x')
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
    return {k: v for k, v in r.items() if v != 0.0}
def add_recv(d, lk, sv, kind='recv'):
    key = (d, lk, sv)
    if key in have: return False
    have.add(key); rows.append(recv_row(d, lk, sv)); rhs.append(d - 6.0); rinfo.append((kind, d, lk, sv)); return True

# ---- DP rows for d > DMAXP (letter 9): y + z9 per big position ----
BIGSTATE = np.array([1.0 if states[a][2] >= 7 else 0.0 for a in range(NS)])
def dp9(d, yv, z9, thr, many=40):
    U = 9; M = np.full((NS, NS), -np.inf); RM = {}
    for a, b, rr in TRI[U]:
        val = (yv[ix[rr]] if rr is not None else 0.0) + z9 * BIGSTATE[a]
        if val > M[a, b]: M[a, b] = val; RM[a, b] = rr
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
        out.append((float(diag[a0]), tuple(sorted(p for p in path if p is not None)), nbig))
    return out
have9 = set()
def add_row9(d, path, nbig):
    key = (d, path, nbig)
    if key in have9: return False
    have9.add(key); r = collections.defaultdict(float); r[('t',)] = -1.0
    for p in path: r[('y', ix[p])] += 1.0
    if nbig and not NOTX: r[('z9',)] += float(nbig)
    rows.append(dict(r)); rhs.append(d - 6.0); rinfo.append(('recv9', d, nbig, path)); return True

# ---- separation through sep3x ----
def sepx(d, yv, xv, thr, many):
    xs = [(tau, v) for tau, v in xv.items() if v > 1e-12]
    SEPX.stdin.write('q %d %.12f %d %d\n%s\nX %d %s\n' % (d, thr, many, OMAX, ' '.join('%.12f' % x for x in yv),
                     len(xs), ' '.join('%d %.12f' % kv for kv in xs)))
    SEPX.stdin.flush(); out = []
    while True:
        f = SEPX.stdout.readline().split()
        if not f: raise RuntimeError('sep3x died')
        if f[0] == 'END': return out
        out.append((float(f[1]), f[2], f[3]))

def solve():
    nx = len(XCOL); nc = NY + nx + 2; IZ, IT = NY + nx, NY + nx + 1
    data, ri, ci = [], [], []
    for k, r in enumerate(rows):
        for key, v in r.items():
            c = key[1] if key[0] == 'y' else (NY + XCOL[key[1]] if key[0] == 'x' else (IZ if key[0] == 'z9' else IT))
            data.append(v); ri.append(k); ci.append(c)
    A = sps.csr_matrix((data, (ri, ci)), shape=(len(rows), nc))
    cvec = np.zeros(nc); cvec[IT] = 1.0
    bounds = [(0, 1)] * NY + [(0, XCAP if not NOTX else 0)] * nx + [(0, XCAP if not NOTX else 0), (None, None)]
    res = linprog(cvec, A_ub=A, b_ub=np.array(rhs), bounds=bounds, method='highs')
    if res.status != 0: raise RuntimeError('LP status %s %s' % (res.status, res.message))
    yv = res.x[:NY]; xv = {tau: res.x[NY + i] for tau, i in XCOL.items()}; z9 = res.x[IZ]; t = res.x[IT]
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
        open(os.path.join(HERE, 'out', 'wlp3x_%s_rows.txt' % TAGX), 'w').write(''.join(
            '  receiver d=%d link %s s %s\n' % (i_[1], i_[2], i_[3]) for i_ in rinfo if i_[0] in ('recv', 'warm')))
    if not added: break
res, yv, xv, z9, t = solve()
duals = -res.ineqlin.marginals
out = ['# wlp3x %s: %s; t* = %.6f; %d rows, %d transfer columns, z9 = %.4f, xcap %.1f' % (
    ' '.join(ARGS0), 'TRANSFERS OFF' if NOTX else 'transfers on', t, len(rows), len(XCOL), z9, XCAP)]
out.append('dual certificate (rows with positive weight):')
for k, dv in enumerate(duals):
    if dv > 1e-9:
        inf = rinfo[k]
        if inf[0] in ('recv', 'warm'): out.append('  %.4f  receiver d=%d link %s s %s' % (dv, inf[1], inf[2], inf[3]))
        elif inf[0] == 'recv9': out.append('  %.4f  receiver9 d=%d nbig=%d roots %s' % (dv, inf[1], inf[2], ' '.join('%d|%s' % (r_[0], ''.join(map(str, r_[1:]))) for r_ in inf[3])))
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
for a, b, rr in TRI[9]:
    val = (yv[ix[rr]] if rr is not None else 0.0) + (0.0 if NOTX else z9) * BIGSTATE[a]
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
           'x': {str(tau): float(v) for tau, v in xv.items() if v > 1e-12}, 'args': ARGS0},
          open(os.path.join(HERE, 'out', 'wlp3x_%s_sol.json' % TAGX), 'w'))
SEPX.stdin.close(); SEPX.wait()
open(os.path.join(HERE, 'out', 'wlp3x_%s.txt' % TAGX), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out[:60]))
