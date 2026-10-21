# s52c CKEEP copy of wlp.py (coordinator 21 Oct 15:53Z, Opus reading): R5 / R6 = D wheels + kept C 6-wheels (+ the 555 rule).
"""Wheel-level discharging LP (exploratory).  See README.md section 0.
Letters 5,6,7,8,9 (9 = degree >= 9).  R5/R6 = reducible 5-/6-wheel words (Job 17 D, Lean-certified C; the six
565xxx 6-wheels excluded).  Variables y[r] for rooted words r = (u, a, b, c, e) (u >= 7 = the sender's letter, the
5's link read from u), up to the reflection (u,a,b,c,e) ~ (u,e,c,b,a).
  sender rows   : every non-R cyclic 5-word w with a big letter: sum over big positions y[root] >= 1 - t
  receiver rows : degree d (letter min(d,9)), arrangement (w_i, s_i)_{i<d}: sum over w_i = 5 of y[...] <= d - 6 + t
Receiver rows are generated lazily by a max-plus DP over states (w_{i-1}, s_{i-1}, w_i).
Usage: python3 wlp.py [extra-R-option ...]   options: noC (drop C wheels)"""
import sys, os, itertools, collections
import numpy as np
from scipy.optimize import linprog
HERE = os.path.dirname(os.path.abspath(__file__)); DIS = os.path.dirname(HERE)
OPT = set(sys.argv[1:])
L = (5, 6, 7, 8, 9)
def canon(w):
    w = tuple(w); return min(min(s[k:] + s[:k] for k in range(len(s))) for s in (w, w[::-1]))
R5, R6 = set(), set()
_CKEEPSET = {l.split()[0] for l in open(os.environ['CKEEP']) if l.strip() and not l.startswith('#')}   # s52c copy of wlp.py (CKEEP only)
UNCERT = {'565667', '565676', '565677', '565757', '565767', '565777'}
for line in open(os.path.join(DIS, 'studio17', 'wheels17_verdicts.txt')):
    if line.startswith('#'): continue
    f = line.split(); nm, v = f[0], f[2]
    fam, w = nm.split('_')
    if v == 'D' or (v == 'C' and w not in UNCERT and fam == 'c6' and nm in _CKEEPSET):   # s52c _ck copy: C wheels only if kept (c6)
        (R5 if fam == 'c5' else R6).add(tuple(map(int, w)))
if 'noC' in OPT: R5.discard((6, 6, 6, 6, 6))
R5 |= {canon(w) for w in OPT_EXTRA} if (OPT_EXTRA := [tuple(map(int, o[3:])) for o in OPT if o.startswith('R5=')]) else set()
FANS = []                             # D-reducible fans (fans.py, out/fans_dfast.out): F = any degree
if 'nofan' not in OPT:
    for line in open(os.path.join(HERE, 'out', 'fans_dfast.out')):
        if 'D=true' in line: FANS.append(tuple(0 if ch == 'F' else int(ch) for ch in line.split()[0][2:]))
def _match(w, pat):
    w = tuple(w)
    for s in (w, w[::-1]):
        for k in range(5):
            r = s[k:] + s[:k]
            if all(p == 0 or p == q for p, q in zip(pat, r)): return True
    return False
def isR5(w):
    return canon(w) in R5 or any(_match(w, p) for p in FANS)
def isR6(w):                          # census 6-wheels, or a 2.122 (6-centre, link 5,5,5 consecutive)
    w = tuple(w)
    return canon(w) in R6 or any(w[i] == w[(i + 1) % 6] == w[(i + 2) % 6] == 5 for i in range(6))
def root(w, j):                       # w cyclic, position j is the sender
    a = tuple(w[j:] + w[:j]); b = (a[0],) + tuple(reversed(a[1:])); return min(a, b)

# sender rows
W5 = sorted({canon(w) for w in itertools.product(L, repeat=5)})
senders = [w for w in W5 if not isR5(w) and max(w) >= 7]
roots = sorted({root(list(w), j) for w in senders for j in range(5) if w[j] >= 7})
ix = {r: i for i, r in enumerate(roots)}
nv = len(roots) + 1                   # last var = t

# receiver DP: state (wp, sp, wc) = (w_{i-1}, s_{i-1}, w_i); transition chooses s_i, w_{i+1}; weight from w_i.
states = list(itertools.product(L, L, L))
def trans(U):
    """list of (state, nextstate, rootvar or None) allowed for receiver letter U"""
    T = []
    for (wp, sp, wc) in states:
        for sc in L:
            for wn in L:
                r = None
                if wc == 5:
                    w = [U, wn, sc, sp, wp]
                    if isR5(w): continue
                    r = root(w, 0)
                elif wc == 6:
                    if all(isR6([U, wn, sc, p, sp, wp]) for p in L): continue
                T.append(((wp, sp, wc), (wc, sc, wn), r))
    return T
TR = {U: trans(U) for U in (7, 8, 9)}

SI = {s: i for i, s in enumerate(states)}; NS = len(states)
TRI = {U: [(SI[a], SI[b], r) for a, b, r in TR[U]] for U in TR}
def best_arrangement(d, yv, return_all=None, thr=0.0):
    """max over cyclic arrangements of length d of sum y (max-plus matrix powers); returns (value, list of roots)."""
    U = min(d, 9)
    M = np.full((NS, NS), -np.inf); RM = {}
    for a, b, r in TRI[U]:
        M[a, b] = yv[ix[r]] if r is not None else 0.0; RM[a, b] = r
    P = [None, M]; back = [None, None]
    for k in range(2, d + 1):
        C = P[-1][:, :, None] + M[None, :, :]          # a, c, b
        back.append(C.argmax(axis=1)); P.append(C.max(axis=1))
    diag = np.diag(P[d])
    if return_all is not None:
        res_ = []
        for a0 in np.argsort(-diag)[:return_all]:
            if diag[a0] <= thr: break
            res_.append((diag[a0], _bt(back, RM, d, int(a0))))
        return res_
    a0 = int(diag.argmax()); val = diag[a0]
    if val == -np.inf: return -1, ()
    return val, _bt(back, RM, d, a0)
def _bt(back, RM, d, a0):
    path = []; b = a0
    for k in range(d, 1, -1):
        c = back[k][a0, b]; path.append(RM[c, b]); b = c
    path.append(RM[a0, b])
    return tuple(sorted(r for r in path if r is not None))

# ---- option bigw: receivers of degree 7, 8 enumerated by their whole link word, minus D-reducible 7-/8-wheels
RBIG = set()
if 'bigw' in OPT:
    for fn in ('bigwheels_dfast.out', 'bigwheels1516_dfast.out'):
        p = os.path.join(HERE, 'out', fn)
        if os.path.exists(p):
            for line in open(p):
                if 'D=true' in line: RBIG.add(tuple(map(int, line.split()[0].split('_')[1])))
WORDS = {}
def _prep(d):
    U = d; seen = set(); words = []; IDX = []
    for w in itertools.product(L, repeat=d):
        k = canon(w)
        if k in seen: continue
        seen.add(k)
        if k in RBIG: continue
        A = np.full((d, 5, 5), -1, dtype=np.int64)       # -1 allowed weight 0, -2 forbidden, >=0 var
        ok = True
        for i in range(d):
            wp, wc, wn = k[(i - 1) % d], k[i], k[(i + 1) % d]
            for a, sp in enumerate(L):
                for b, sc in enumerate(L):
                    if wc == 5:
                        ww = [U, wn, sc, sp, wp]
                        A[i, a, b] = -2 if isR5(ww) else ix[root(ww, 0)]
                    elif wc == 6:
                        if all(isR6([U, wn, sc, p, sp, wp]) for p in L): A[i, a, b] = -2
            if (A[i] == -2).all(): ok = False; break
        if ok: words.append(k); IDX.append(A)
    WORDS[d] = (words, np.array(IDX))
    print('bigw: d=%d %d non-R link words (R%d wheels used: %d)' % (d, len(words), d, sum(1 for x in RBIG if len(x) == d)), flush=True)
if 'bigw' in OPT:
    for d in (7, 8): _prep(d)
def best_words(d, yv, many, thr):
    words, IDX = WORDS[d]
    yy = np.concatenate([yv, [0.0, -np.inf]])
    W = yy[np.where(IDX >= 0, IDX, np.where(IDX == -1, len(yv), len(yv) + 1))]   # N, d, 5, 5
    P = W[:, 0]
    for k in range(1, d): P = (P[:, :, :, None] + W[:, k][:, None, :, :]).max(axis=2)
    val = np.einsum('nii->ni', P).max(axis=1)
    out = []
    for n in np.argsort(-val)[:many]:
        if val[n] <= thr: break
        Wn = W[n]; best = (-np.inf, None)
        for a0 in range(5):                       # s_{d-1} = s_{-1} = a0
            V = Wn[0][a0].copy(); bk = []
            for i in range(1, d):
                C = V[:, None] + Wn[i]; bk.append(C.argmax(axis=0)); V = C.max(axis=0)
            if V[a0] > best[0]:
                s = [None] * d; s[d - 1] = a0
                for i in range(d - 1, 0, -1): s[i - 1] = int(bk[i - 1][s[i]])
                best = (V[a0], s)
        s = best[1]
        path = tuple(sorted(int(IDX[n][i, s[i - 1], s[i]]) for i in range(d) if IDX[n][i, s[i - 1], s[i]] >= 0))
        out.append((val[n], tuple(roots[j] for j in path)))
    return out

# ---- option capD=k: a D-vertex has at most k LONE-BIG senders (pairs.py configurations, all D-reducible)
CAP = {int(o[3]): int(o[5:]) for o in OPT if o.startswith('cap') and '=' in o}
LONEV = np.array([1 if max(r[1:]) <= 6 else 0 for r in roots] + [0, 0])
def best_words_cap(d, yv, many, thr):
    words, IDX = WORDS[d]; cap = CAP[d]; C1 = cap + 1; n5 = 5 * C1
    yy = np.concatenate([yv, [0.0, -np.inf]])
    J = np.where(IDX >= 0, IDX, np.where(IDX == -1, len(yv), len(yv) + 1))
    W = yy[J]; LM = LONEV[J]                               # N, d, 5, 5
    def ext(Wk, Lk):                                       # (B,5,5) -> (B, n5, n5): (s,c) -> (s',c+lone)
        B = Wk.shape[0]; E = np.full((B, n5, n5), -np.inf)
        for c in range(C1):
            for inc in (0, 1):
                c2 = c + inc
                if c2 > cap: continue
                blk = np.where(Lk == inc, Wk, -np.inf)
                E[:, c * 5:(c + 1) * 5, c2 * 5:(c2 + 1) * 5] = blk
        return E
    vals = np.full(len(words), -np.inf)
    for b0 in range(0, len(words), 1500):
        sl = slice(b0, b0 + 1500)
        P = ext(W[sl, 0], LM[sl, 0])
        for k in range(1, d): P = (P[:, :, :, None] + ext(W[sl, k], LM[sl, k])[:, None, :, :]).max(axis=2)
        # closed walks: start (s, 0) end (s, c) for any c
        best = np.full(P.shape[0], -np.inf)
        for c in range(C1):
            best = np.maximum(best, np.stack([P[:, s, c * 5 + s] for s in range(5)], 1).max(axis=1))
        vals[sl] = best
    out = []
    for n in np.argsort(-vals)[:many]:
        if vals[n] <= thr: break
        Ws = [ext(W[n:n + 1, k], LM[n:n + 1, k])[0] for k in range(d)]
        bb = (-np.inf, None)
        for a0 in range(5):
            V = Ws[0][a0].copy(); bk = []
            for i in range(1, d):
                Cm = V[:, None] + Ws[i]; bk.append(Cm.argmax(axis=0)); V = Cm.max(axis=0)
            for c in range(C1):
                e = c * 5 + a0
                if V[e] > bb[0]:
                    st = [None] * d; st[d - 1] = e
                    for i in range(d - 1, 0, -1): st[i - 1] = int(bk[i - 1][st[i]])
                    bb = (V[e], st)
        s = [x % 5 for x in bb[1]]
        path = tuple(sorted(int(IDX[n][i, s[i - 1], s[i]]) for i in range(d) if IDX[n][i, s[i - 1], s[i]] >= 0))
        out.append((vals[n], tuple(roots[j] for j in path)))
    return out

A_ub, b_ub = [], []
for w in senders:                      # -sum y - t <= -1
    row = np.zeros(nv); row[-1] = -1
    for j in range(5):
        if w[j] >= 7: row[ix[root(list(w), j)]] -= 1
    A_ub.append(row); b_ub.append(-1)
rec_rows = []; have = set()
DS = list(range(7, 13)); DSF = list(range(7, 31))
def add_rows(dlist, many):
    added = 0
    for d in dlist:
        gen = best_words_cap(d, yv, many, d - 6 + t + 1e-7) if d in CAP else best_words(d, yv, many, d - 6 + t + 1e-7) if ('bigw' in OPT and d in (7, 8)) else best_arrangement(d, yv, return_all=many, thr=d - 6 + t + 1e-7)
        for val, path in gen:
            if (d, path) in have: continue
            have.add((d, path)); row = np.zeros(nv); row[-1] = -1
            for r in path: row[ix[r]] += 1
            A_ub.append(row); b_ub.append(d - 6); rec_rows.append((d, path)); added += 1
    return added
for it in range(3000):
    res = linprog(np.eye(nv)[-1], A_ub=np.array(A_ub), b_ub=np.array(b_ub),
                  bounds=[(0, 1)] * (nv - 1) + [(None, None)], method='highs')
    yv, t = res.x[:-1], res.x[-1]
    added = add_rows(DS, 60)
    if not added: added = add_rows(DSF, 60)
    print('iter', it, 't=%.6f' % t, 'rows', len(rec_rows), 'added', added, flush=True)
    if not added: break
# dual certificate
res = linprog(np.eye(nv)[-1], A_ub=np.array(A_ub), b_ub=np.array(b_ub),
              bounds=[(0, 1)] * (nv - 1) + [(None, None)], method='highs')
duals = -res.ineqlin.marginals
out = ['# wheel-level LP %s: %d non-R sender words, %d rooted vars, %d receiver rows; t* = %.6f' % (
    ' '.join(sorted(OPT)), len(senders), len(roots), len(rec_rows), res.fun)]
out.append('dual certificate (rows with positive weight):')
ns = len(senders)
for i, dv in enumerate(duals):
    if dv > 1e-9:
        if i < ns: out.append('  %.4f  sender %s' % (dv, ''.join(map(str, senders[i]))))
        else:
            d, path = rec_rows[i - ns]
            out.append('  %.4f  receiver d=%d with %d 5-nbrs: %s' % (dv, d, len(path), ' '.join(''.join(map(str, r)) for r in path)))
out.append('nonzero rule weights y[rooted word u|a b c e]:')
for r in roots:
    if res.x[ix[r]] > 1e-9: out.append('  %s|%s  %.4f' % (r[0], ''.join(map(str, r[1:])), res.x[ix[r]]))
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
tag = '_'.join(sorted(OPT)) or 'base'
open(os.path.join(HERE, 'out', 'wlp_%s.txt' % tag), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out[:60]))

# uniform bound for all d >= 9: max cycle mean (Karp) of the letter-9 transfer matrix at the optimum
def karp(M):
    n = M.shape[0]; D = np.full((n + 1, n), -np.inf); D[0, :] = 0.0
    for k in range(1, n + 1): D[k] = (D[k - 1][:, None] + M).max(axis=0)
    with np.errstate(invalid='ignore'):
        q = np.where(np.isfinite(D[n]), np.min(np.where(np.isfinite(D[:n]), (D[n] - D[:n]) / (n - np.arange(n))[:, None], np.inf), axis=0), -np.inf)
    return q.max()
yv = res.x[:-1]; t = res.x[-1]
M = np.full((NS, NS), -np.inf)
for a, b, r in TRI[9]: M[a, b] = yv[ix[r]] if r is not None else 0.0
lam = karp(M)
msg = 'letter-9 max cycle mean lambda = %.6f per link position; d*lambda <= d-6+t for all d >= %s' % (
    lam, ('%.2f' % ((6 - t) / (1 - lam))) if lam < 1 else 'never')
print(msg); open(os.path.join(HERE, 'out', 'wlp_%s.txt' % tag), 'a').write(msg + '\n')
