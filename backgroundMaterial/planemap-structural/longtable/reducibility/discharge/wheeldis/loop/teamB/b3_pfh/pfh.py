"""Team B round B3: the PFH rule family (own code; LOG.md round B3).  Charge 6 - deg.  LP variables:
  y[k]  a 5 -> adjacent big,  k = ('y', the 5's link rooted at the target)       (root letter 7..9)
  p[k]  a 5 -> adjacent 6,    k = ('p', the 5's link rooted at the 6)            (root letter 6)
  f[k]  a 6 -> adjacent big,  k = ('f', the 6's link rooted at the target)
  h[k]  a 7 -> adjacent big,  k = ('h', the 7's link rooted at the target)
Rooted links are tuples (target, n1, ..., n_{d-1}) read around the sender, canonical under reflection.
Rows: 5: out >= 1 - t;  6: in - out <= t;  big of degree d: in - out <= d - 6 + t (letter min(d, 9)).
Wheel-level R from wlp.py (R5 with fans, R6 exact, RBIG 7-/8-wheels).  Unchecked R conditions only make rows harder,
never easier, so every row generated is a valid constraint for the R used."""
import sys, os, itertools, time
import numpy as np
from scipy.optimize import linprog
HERE = os.path.dirname(os.path.abspath(__file__))
WD = os.path.abspath(os.path.join(HERE, '../../..'))
ARGS = sys.argv[1:]
src = open(os.path.join(WD, 'wlp.py')).read().replace('__file__', repr(os.path.join(WD, 'wlp.py')))
sys.argv = ['wlp']
exec(src[:src.index('# sender rows')])
HERE = os.path.join(WD, 'loop', 'teamB', 'b3_pfh')
sys.argv = [sys.argv[0]] + ARGS
L = (5, 6, 7, 8, 9)
RBIG = set()
for fn in ('bigwheels_dfast.out', 'bigwheels1516_dfast.out', 'bigwheels1516_dfast_partial.out'):
    pth = os.path.join(WD, 'out', fn)
    if os.path.exists(pth):
        for line in open(pth):
            if 'D=true' in line:
                RBIG.add(canon(tuple(map(int, line.split()[0].split('_')[1]))))
OPTS = {a.split('=')[0]: (a.split('=')[1] if '=' in a else True) for a in ARGS}
USE_P = 'noP' not in OPTS
USE_H = 'noH' not in OPTS
DEX = int(OPTS.get('dex', 15))
LIMIT = int(float(OPTS.get('limit', 2e7)))
MANY = int(OPTS.get('many', 60))
TFIX = float(OPTS['tfix']) if 'tfix' in OPTS else None   # feasibility mode at a fixed t (certificate if separation ends clean)
CENTER = float(OPTS['center']) if 'center' in OPTS else None   # phase-2 centring offset for the separation point
CAP = float(OPTS['cap']) if 'cap' in OPTS else None   # optional upper bound on every transfer (a rule-class restriction)


def isRbig(w):
    return canon(w) in RBIG


def rooted(word, j):
    """word cyclic around the sender, j = target position -> canonical rooted tuple."""
    a = tuple(word[j:] + word[:j])
    b = (a[0],) + tuple(reversed(a[1:]))
    return min(a, b)


VAR = {}
LASTARR = {}
VARL = []


def var(k):
    if k not in VAR:
        VAR[k] = len(VARL)
        VARL.append(k)
    return VAR[k]


def val(x, k):
    i = VAR.get(k)
    return x[i] if (i is not None and i < len(x)) else 0.0


# ---------------- sender rows (5s): exhaustive, fixed
S5 = []
for w in sorted({canon(w) for w in itertools.product(L, repeat=5)}):
    if isR5(w):
        continue
    terms = []
    for j in range(5):
        if w[j] >= 7:
            terms.append(var(('y', rooted(list(w), j))))
        elif w[j] == 6 and USE_P:
            terms.append(var(('p', rooted(list(w), j))))
    assert terms or True
    S5.append((w, terms))
assert all(t for _, t in S5), [w for w, t in S5 if not t][:5]


# ---------------- 6 rows: for each exact non-R 6-link v, max over the 6's second ring s (cyclic DP) of
#                  sum over fives of p - sum over bigs of f
V6 = []
for v in itertools.product(L, repeat=6):
    if canon(v) != v or isR6(v):
        continue
    V6.append(v)


def six_row(v, x):
    """returns (value of best row at x, terms [(sign, key)])"""
    fk = [('f', rooted(list(v), j)) for j in range(6) if v[j] >= 7]
    base = -sum(val(x, k) for k in fk)
    # five at k: word (6, v[k+1], s_k, s_{k-1}, v[k-1]); s_k between v_k and v_{k+1}
    # DP over s_0..s_5 cyclic
    best = (-np.inf, None)
    for s0 in L:
        # dp over s_1..s_5, carrying s_{k-1}; weight of five k uses s_{k-1}, s_k
        dp = {s0: (0.0, [])}
        for k in range(1, 6):
            nd = {}
            for sp, (acc, path) in dp.items():
                for sc in L:
                    wt, tm = 0.0, None
                    if v[k] == 5:
                        ww = (6, v[(k + 1) % 6], sc, sp, v[k - 1])
                        if isR5(ww):
                            continue
                        tm = ('p', rooted(list(ww), 0))
                        wt = val(x, tm)
                    cand = (acc + wt, path + ([tm] if tm else []))
                    if sc not in nd or cand[0] > nd[sc][0]:
                        nd[sc] = cand
            dp = nd
        for s5, (acc, path) in dp.items():
            # five at 0 uses s_0 and s_5
            if v[0] == 5:
                ww = (6, v[1], s0, s5, v[5])
                if isR5(ww):
                    continue
                tm = ('p', rooted(list(ww), 0))
                tot = acc + val(x, tm)
                path = path + [tm]
            else:
                tot = acc
            if tot > best[0]:
                best = (tot, path)
    if best[1] is None:
        return -np.inf, None
    return best[0] + base, [(1, k) for k in best[1]] + [(-1, k) for k in fk]


# ---------------- big receivers.  Contribution of link vertex w_i to u given (w_{i-1}, s_{i-1}, w_i, s_i, w_{i+1}):
# candidates = list of keys (or None for "allowed, contributes 0"), maximised over privates.
def contrib_cands(U, wp, sp, wc, sc, wn):
    if wc == 5:
        ww = (U, wn, sc, sp, wp)
        return [] if isR5(ww) else [('y', rooted(list(ww), 0))]
    if wc == 6:
        out = []
        for p in L:
            ww = (U, wn, sc, p, sp, wp)
            if isR6(ww):
                continue
            out.append(('f', rooted(list(ww), 0)) if U >= 7 else None)
        return sorted(set(out), key=lambda k: (k is None, k))
    if wc == 7:
        out = []
        for pa, pb in itertools.product(L, L):
            ww = (U, wn, sc, pa, pb, sp, wp)
            if isRbig(ww):
                continue
            out.append(('h', rooted(list(ww), 0)) if USE_H else None)
        return sorted(set(out), key=lambda k: (k is None, k))
    return [None]


STATES = list(itertools.product(L, L, L))
SI = {s: i for i, s in enumerate(STATES)}
EDGES = {}


def edges(U):
    if U not in EDGES:
        E = []
        for (wp, sp, wc) in STATES:
            for sc in L:
                for wn in L:
                    c = contrib_cands(U, wp, sp, wc, sc, wn)
                    if not c:
                        continue
                    E.append((SI[(wp, sp, wc)], SI[(wc, sc, wn)], c))
        EDGES[U] = E
    return EDGES[U]


def edge_weights(U, x):
    W = np.full((125, 125), -np.inf)
    K = {}
    for a, b, c in edges(U):
        best, bk = -np.inf, None
        for k in c:
            vv = 0.0 if k is None else val(x, k)
            if vv > best:
                best, bk = vv, k
        if best > W[a, b]:
            W[a, b] = best
            K[(a, b)] = bk
    return W, K


def best_cycles(W, K, d, thr, cap=60):
    P = W.copy()
    back = [None, None]
    for _ in range(2, d + 1):
        C = P[:, :, None] + W[None, :, :]
        back.append(C.argmax(axis=1))
        P = C.max(axis=1)
    diag = np.diag(P)
    out = []
    for a0 in np.argsort(-diag)[:cap]:
        a0 = int(a0)
        if not diag[a0] > thr:
            break
        keys = []
        b = a0
        for k in range(d, 1, -1):
            c = back[k][a0, b]
            keys.append(K[(c, b)])
            b = c
        keys.append(K[(a0, b)])
        out.append((diag[a0], [k for k in keys if k is not None]))
    return out


def best_cycle(W, K, d):
    P = W.copy()
    back = [None, None]
    for _ in range(2, d + 1):
        C = P[:, :, None] + W[None, :, :]
        back.append(C.argmax(axis=1))
        P = C.max(axis=1)
    diag = np.diag(P)
    a0 = int(diag.argmax())
    if diag[a0] == -np.inf:
        return -np.inf, []
    keys = []
    b = a0
    for k in range(d, 1, -1):
        c = back[k][a0, b]
        keys.append(K[(c, b)])
        b = c
    keys.append(K[(a0, b)])
    return diag[a0], [k for k in keys if k is not None]


# d = 7 receivers with hand-off out: enumerate u's link words explicitly
W7 = None


def prep7():
    global W7
    W7 = [w for w in sorted({canon(w) for w in itertools.product(L, repeat=7)}) if not isRbig(w)]


def best7(x, thr=None, cap=300):
    """max over non-R 7-link words and s, privates of in - out at a 7; with thr, also every word's best row above
    thr (capped, heaviest first) in .many"""
    best = (-np.inf, None)
    many = []
    for w in W7:
        out = [('h', rooted(list(w), j)) for j in range(7) if w[j] >= 7] if USE_H else []
        base = -sum(val(x, k) for k in out)
        # per position weight table over (s_{i-1}, s_i)
        tabs = []
        dead = False
        for i in range(7):
            T = np.full((5, 5), -np.inf)
            KK = {}
            for a, sp in enumerate(L):
                for b, sc in enumerate(L):
                    c = contrib_cands(7, w[i - 1], sp, w[i], sc, w[(i + 1) % 7])
                    for k in c:
                        vv = 0.0 if k is None else val(x, k)
                        if vv > T[a, b]:
                            T[a, b] = vv
                            KK[(a, b)] = k
            if np.all(T == -np.inf):
                dead = True
                break
            tabs.append((T, KK))
        if dead:
            continue
        # cyclic over s_0..s_6: position i uses (s_{i-1}, s_i)
        wbest = (-np.inf, None)
        for s6 in range(5):
            dp = tabs[0][0][s6, :].copy()
            bk = [None]
            for i in range(1, 7):
                C = dp[:, None] + tabs[i][0]
                bk.append(C.argmax(axis=0))
                dp = C.max(axis=0)
            tot = dp[s6] + base
            if tot > wbest[0]:
                ss = [None] * 7
                ss[6] = s6
                for i in range(6, 0, -1):
                    ss[i - 1] = int(bk[i][ss[i]])
                keys = [tabs[0][1][(s6, ss[0])]] + [tabs[i][1][(ss[i - 1], ss[i])] for i in range(1, 7)]
                wbest = (tot, [(1, k) for k in keys if k is not None] + [(-1, k) for k in out], w)
        if wbest[0] > best[0]:
            best = wbest
        if thr is not None and wbest[0] > thr:
            many.append(wbest)
    many.sort(key=lambda r: -r[0])
    best7.many = many[:cap]
    return best


REG = 'reg' in OPTS
SEPB = None
if REG:
    import subprocess
    RB7S = set()
    for line in open(os.path.join(HERE, 'rbig7.txt')):
        RB7S.add(canon(tuple(map(int, line.strip()))))
    RBIG |= RB7S          # w7plus 7-wheels also forbidden as link-vertex wheels
    SEPB = subprocess.Popen([os.path.join(HERE, OPTS.get('sepb', 'sepb')), os.path.join(HERE, OPTS.get('pats', 'reg_patterns.txt')),
                             os.path.join(HERE, 'rbig7.txt')], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
ORACLE = OPTS.get('oracle')     # B6: kill separated arrangements that contain a verified RSST configuration (file of patterns)
ORC = {}
if ORACLE:
    sys.path.insert(0, os.path.join(WD, 'loop', 'teamB', 'b6_rpat'))
    import rpat
    ORACLE = os.path.join(HERE, ORACLE)
    OPAT = []
    if os.path.exists(ORACLE):
        for line in open(ORACLE):
            f = line.split()
            if f and not line.startswith('#'):
                d0, n0 = int(f[0]), int(f[1])
                OPAT.append((d0, [(int(f[2 + 2 * k]), int(f[3 + 2 * k])) for k in range(n0)]))
                SEPB.stdin.write('P %s\n' % line.split('#')[0].strip())
        SEPB.stdin.flush()
    print('oracle patterns loaded', len(OPAT), flush=True)


def pat_hits(d, sm, ws, ss):
    """does pattern sm (slot masks, any dihedral image) match arrangement (ws, ss)?"""
    wv = [int(c) - 5 for c in ws]
    sv = [int(c) - 5 for c in ss]
    for refl in (0, 1):
        for r in range(d):
            ok = True
            for sl, m in sm:
                if sl < d:
                    j = ((-sl) % d if refl else sl)
                    let = wv[(j + r) % d]
                else:
                    i = sl - d
                    j = ((-i - 1) % d if refl else i)
                    let = sv[(j + r) % d]
                if not (m >> let) & 1:
                    ok = False
                    break
            if ok:
                return True
    return False


def oracle_kill(d, ws, ss):
    k = (d, ws, ss)
    if k not in ORC:
        ORC[k] = rpat.kill(d, [int(c) for c in ws], [int(c) for c in ss])
    return ORC[k]
WCAND = {}


def wcands(U):
    if U not in WCAND:
        T = {}
        for wp, sp, wc, sc, wn in itertools.product(L, repeat=5):
            T[(wp, sp, wc, sc, wn)] = contrib_cands(U, wp, sp, wc, sc, wn)
        WCAND[U] = T
    return WCAND[U]


def wbest(c, x):
    best, bk = -np.inf, None
    for k in c:
        vv = 0.0 if k is None else val(x, k)
        if vv > best:
            best, bk = vv, k
    return best, bk


def sepb_query(d, x, thr, many, limit=0):
    U = min(d, 9)
    T = wcands(U)
    vals = []
    for key in itertools.product(L, repeat=5):
        b, _ = wbest(T[key], x)
        vals.append('-1e300' if b == -np.inf else '%.12f' % b)
    SEPB.stdin.write('T %d\n%s\n' % (U, ' '.join(vals)))
    if d == 7:
        hv = []
        for wd in itertools.product(L, repeat=7):
            hv.append('%.12f' % (sum(val(x, ('h', rooted(list(wd), j))) for j in range(7) if wd[j] >= 7) if USE_H else 0.0))
        SEPB.stdin.write('H\n%s\n' % ' '.join(hv))
    SEPB.stdin.write('Q %d %.12f %d %d\n' % (d, thr, many, limit))
    SEPB.stdin.flush()
    out = []
    while True:
        f = SEPB.stdout.readline().split()
        if f[0] == 'END':
            sepb_query.trunc = (f[2] == 'TRUNC')
            return out
        v, ws, ss = float(f[1]), f[2], f[3]
        wv = [int(c) for c in ws]; sv = [int(c) for c in ss]
        terms = []
        for i in range(d):
            _, k = wbest(T[(wv[i - 1], sv[i - 1], wv[i], sv[i], wv[(i + 1) % d])], x)
            if k is not None:
                terms.append((1, k))
        if d == 7 and USE_H:
            terms += [(-1, ('h', rooted(wv, j))) for j in range(7) if wv[j] >= 7]
        out.append((v, terms, ws, ss))


HW = {'h': None, 'rows': [], 'ncol': 0}


def solve_warm(rows):
    """persistent HiGHS model: new rows and columns are added and the previous basis is reused (dual simplex warm
    start). Column 0 is t, column i + 1 is VARL[i]. Rebuilt from scratch if earlier rows were removed."""
    import highspy
    inf = highspy.kHighsInf
    n = len(VARL)
    loaded = HW['rows']
    off = 2 if TFIX is not None else 1      # tfix: column 0 = t fixed at TFIX, column 1 = common margin m (maximised)
    if HW['h'] is None or len(rows) < len(loaded) or any(a is not b for a, b in zip(rows, loaded)):
        h = highspy.Highs()
        h.setOptionValue('output_flag', False)
        if TFIX is None:
            h.addCol(1.0, -5.0, inf, 0, np.array([], dtype=np.int32), np.array([], dtype=np.float64))
        else:
            h.addCol(0.0, TFIX, TFIX, 0, np.array([], dtype=np.int32), np.array([], dtype=np.float64))
            h.addCol(-1.0, -1.0, 1.0, 0, np.array([], dtype=np.int32), np.array([], dtype=np.float64))
        HW.update(h=h, rows=[], ncol=0)
    h = HW['h']
    if HW['ncol'] < n:
        k = n - HW['ncol']
        ub = CAP if CAP is not None else inf
        cost = np.full(k, 1e-7) if TFIX is not None else np.zeros(k)   # tfix: tiny cost keeps unconstrained transfers at 0
        h.addCols(k, cost, np.zeros(k), np.full(k, ub), 0, np.zeros(k, dtype=np.int32),
                  np.array([], dtype=np.int32), np.array([], dtype=np.float64))
        HW['ncol'] = n
    new = rows[len(HW['rows']):]
    if new:
        starts, idx, vals, lo, up = [], [], [], [], []
        for terms, tc, rhs in new:
            starts.append(len(idx))
            acc = {}
            for c, i in terms:
                acc[i + off] = acc.get(i + off, 0) + c
            if tc:
                acc[0] = acc.get(0, 0) + tc
                if off == 2:
                    acc[1] = 1.0
            for j, v in acc.items():
                if v:
                    idx.append(j)
                    vals.append(v)
            lo.append(-inf)
            up.append(rhs)
        h.addRows(len(new), np.array(lo), np.array(up), len(idx), np.array(starts, dtype=np.int32),
                  np.array(idx, dtype=np.int32), np.array(vals, dtype=np.float64))
        HW['rows'] = list(rows)
    h.run()
    st = h.getModelStatus()
    assert st == highspy.HighsModelStatus.kOptimal, h.modelStatusToString(st)
    col = np.array(h.getSolution().col_value)
    if off == 2:
        print('  margin %.6f' % col[1], flush=True)
        if col[1] < -1e-9:
            print('INFEASIBLE at t = %.6f : t* > %.6f (generated rows only, so a valid lower bound)' % (TFIX, TFIX), flush=True)
            sys.exit(0)
    return col[off:], col[0], None


def solve(rows):
    if 'warm' in OPTS and CENTER is None:
        return solve_warm(rows)
    """rows: list of (terms[(coef, varindex)], tcoef, rhs) meaning sum coef*x + tcoef*t <= rhs."""
    n = len(VARL) + 1
    from scipy.sparse import csr_matrix
    ri, ci, vv = [], [], []
    b = np.zeros(len(rows))
    for r, (terms, tc, rhs) in enumerate(rows):
        for c, i in terms:
            ri.append(r); ci.append(i); vv.append(c)
        ri.append(r); ci.append(n - 1); vv.append(tc)
        b[r] = rhs
    A = csr_matrix((vv, (ri, ci)), shape=(len(rows), n))
    cobj = np.zeros(n)
    cobj[-1] = 1
    bounds = [(0, CAP)] * (n - 1) + [(-5, None)]
    if TFIX is not None:
        # fixed-t mode: is there x with t = TFIX? maximise a common margin m on every row carrying t (feasible iff m >= 0)
        from scipy.sparse import hstack
        tc = np.array([1.0 if r[1] != 0 else 0.0 for r in rows])
        A2 = hstack([A, csr_matrix(tc.reshape(-1, 1))]).tocsr()
        c2 = np.zeros(n + 1)
        c2[-1] = -1
        b2 = [(0, CAP)] * (n - 1) + [(TFIX, TFIX), (-1, 1)]
        r2 = linprog(c2, A_ub=A2, b_ub=b, bounds=b2, method='highs')
        assert r2.status == 0, r2.message
        print('  margin %.6f' % r2.x[-1], flush=True)
        if r2.x[-1] < -1e-9:
            print('INFEASIBLE at t = %.6f : t* > %.6f (generated rows only, so a valid lower bound)' % (TFIX, TFIX), flush=True)
            sys.exit(0)
        return r2.x[:n - 1], TFIX, r2
    res = linprog(cobj, A_ub=A, b_ub=b, bounds=bounds, method='highs')
    assert res.status == 0, res.message
    if CENTER is None:
        return res.x[:-1], res.x[-1], res
    # phase 2 (separation point only): t fixed a little above the optimum, maximise a common margin m on every row
    # that carries t, so the next separation sees a centred x instead of an extreme vertex. The reported t is phase 1's.
    from scipy.sparse import hstack
    tc = np.array([1.0 if r[1] != 0 else 0.0 for r in rows])
    A2 = hstack([A, csr_matrix(tc.reshape(-1, 1))]).tocsr()
    c2 = np.zeros(n + 1)
    c2[-1] = -1
    b2 = [(0, CAP)] * (n - 1) + [(res.x[-1] + CENTER, res.x[-1] + CENTER), (0, 1)]
    r2 = linprog(c2, A_ub=A2, b_ub=b, bounds=b2, method='highs')
    if r2.status != 0:
        return res.x[:-1], res.x[-1], res
    return r2.x[:n - 1], res.x[-1], res


def main():
    t0 = time.time()
    rows = []
    for w, terms in S5:          # -(sum) - t <= -1
        rows.append(([(-1, i) for i in terms], -1, -1))
    if USE_P:
        valid = {}
        for a in L:
            for b in L:
                ks = set()
                for x5 in L:
                    for y5 in L:
                        ww = (6, a, x5, y5, b)
                        if not isR5(ww):
                            ks.add(('p', rooted(list(ww), 0)))
                valid[(a, b)] = ks
                for k in ks:          # p[k] - M[a,b] <= 0
                    rows.append(([(1, var(k)), (-1, var(('M', a, b)))], 0, 0))
        n6 = 0
        for v in V6:
            terms = []
            ok = True
            for k in range(6):
                if v[k] == 5:
                    if not valid[(v[(k + 1) % 6], v[k - 1])]:
                        ok = False
                        break
                    terms.append((1, var(('M', v[(k + 1) % 6], v[k - 1]))))
                elif v[k] >= 7:
                    terms.append((-1, var(('f', rooted(list(v), k)))))
            if ok and any(c > 0 for c, _ in terms):
                rows.append((terms, -1, 0))
                n6 += 1
        print('static 6-rows', n6, flush=True)
    if not REG:
        prep7()
    seen = set()
    it = 0
    full = False      # REG: node-limited separation until a pass finds nothing, then one exhaustive pass
    ck = os.path.join(HERE, 'ckpt_%s.pkl' % OPTS.get('tag', 'run'))
    if 'resume' in OPTS and os.path.exists(ck):
        import pickle
        with open(ck, 'rb') as fi:
            C = pickle.load(fi)
        assert C['VARL'][:len(VARL)] == VARL, 'checkpoint from a different model'
        VARL[:] = C['VARL']
        VAR.clear()
        VAR.update({k: i for i, k in enumerate(VARL)})
        rows[:] = C['rows']
        seen |= C['seen']
        LASTARR.update(C['LASTARR'])
        it = C['it']
        print('resumed from %s at it %d (%d rows)' % (ck, it, len(rows)), flush=True)
        if 'killed' in OPTS:      # B6: drop rows of arrangements the oracle killed (harvest.py)
            KA = set()
            for line in open(os.path.join(HERE, OPTS['killed'])):
                f = line.split()
                KA.add((int(f[0]), f[1], f[2]))
            keep = []
            for row in rows:
                terms, tc, rhs = row
                if tc == -1 and rhs >= 1:
                    rk = (rhs + 6, tuple(sorted((c, VARL[i]) for c, i in terms)))
                    arr = LASTARR.get(rk)
                    if arr and (rk[0], arr[0], arr[1]) in KA:
                        seen.discard(rk)
                        continue
                keep.append(row)
            print('dropped %d rows of oracle-killed arrangements' % (len(rows) - len(keep)), flush=True)
            rows[:] = keep
    while True:
        if it and it % 20 == 0:
            import pickle
            with open(ck + '.tmp', 'wb') as fo:
                pickle.dump({'VARL': VARL, 'rows': rows, 'seen': seen, 'LASTARR': LASTARR, 'it': it}, fo)
            os.replace(ck + '.tmp', ck)
        trunc = []
        kills = 0
        x, t, res = solve(rows)
        new = 0
        worst = {}
        # 6 rows
        for v in ([] if USE_P else V6):
            vv, tm = six_row(v, x)
            if tm is not None and vv > t + 1e-9:
                key = ('6', tuple(sorted(tm)))
                if key not in seen:
                    seen.add(key)
                    rows.append(([(sg, var(k)) for sg, k in tm], -1, 0))
                    new += 1
                worst['6'] = max(worst.get('6', -9), vv - t)
        if REG:
            for d in range(7, DEX + 1):
                tq = time.time()
                res_ = sepb_query(d, x, d - 6 + t + 1e-9, MANY, 0 if full else LIMIT)
                if sepb_query.trunc:
                    trunc.append(d)
                if time.time() - tq > 20:
                    print('  slow query d=%d %.0fs' % (d, time.time() - tq), flush=True)
                worst[d] = (res_[0][0] - (d - 6) - t) if res_ else 0
                for v_, tm, ws, ss in res_:
                    key = (d, tuple(sorted(tm)))
                    if ORACLE:
                        kk = oracle_kill(d, ws, ss)
                        if kk:
                            name, pt = kk
                            line = rpat.fmt(d, pt)
                            if (d, pt) not in OPAT:
                                OPAT.append((d, pt))
                                with open(ORACLE, 'a') as fo:
                                    fo.write('%s # %s %s/%s\n' % (line, name, ws, ss))
                                SEPB.stdin.write('P %s\n' % line)
                                SEPB.stdin.flush()
                                # drop rows of arrangements this pattern kills (they would over-constrain the LP)
                                keep = []
                                for row in rows:
                                    terms, tc, rhs = row
                                    if tc == -1 and rhs >= 1:
                                        rk = (rhs + 6, tuple(sorted((c, VARL[i]) for c, i in terms)))
                                        arr = LASTARR.get(rk)
                                        if arr and rk[0] == d and pat_hits(d, pt, arr[0], arr[1]):
                                            seen.discard(rk)
                                            continue
                                    keep.append(row)
                                kills += len(rows) - len(keep)
                                rows[:] = keep
                                new += 1
                            continue
                    if key not in seen:
                        seen.add(key)
                        rows.append(([(sg, var(k)) for sg, k in tm], -1, d - 6))
                        LASTARR[key] = (ws, ss)
                        new += 1
            it += 1
            print('it %d t=%.6f rows=%d vars=%d new=%d opat=%d rowsdropped=%d worst=%s trunc=%s full=%s (%.0fs)' % (
                it, t, len(rows), len(VARL), new, len(OPAT) if ORACLE else 0, kills, {k: round(v, 4) for k, v in worst.items()}, trunc, full, time.time() - t0), flush=True)
            if new == 0:
                if full or not trunc:
                    break
                full = True
            else:
                full = False
            continue
        # d = 7 (explicit, with hand-off out)
        v7, tm7, w7 = best7(x, thr=1 + t + 1e-9)
        for _v, tm, _w in best7.many:
            key = ('7', tuple(sorted(tm)))
            if key not in seen:
                seen.add(key)
                rows.append(([(sg, var(k)) for sg, k in tm], -1, 1))
                new += 1
        worst[7] = v7 - 1 - t
        # d = 8..DEX by the transfer DP
        for d in range(8, DEX + 1):
            U = min(d, 9)
            W, K = edge_weights(U, x)
            cyc = best_cycles(W, K, d, d - 6 + t + 1e-9)
            vd = best_cycle(W, K, d)[0]
            worst[d] = vd - (d - 6) - t
            for _vd, keys in cyc:
                key = (d, tuple(sorted(keys)))
                if key not in seen:
                    seen.add(key)
                    rows.append(([(1, var(k)) for k in keys], -1, d - 6))
                    new += 1
        it += 1
        print('it %d t=%.6f rows=%d vars=%d new=%d worst=%s (%.0fs)' % (
            it, t, len(rows), len(VARL), new, {k: round(v, 4) for k, v in worst.items()}, time.time() - t0), flush=True)
        if new == 0:
            break
    # tail: max mean of the letter-9 transfer graph
    W, K = edge_weights(9, x)
    lam = karp(W)
    print('converged t* = %.9f ; letter-9 max cycle mean = %.6f ; d >= %.1f covered by the mean bound' % (
        t, lam, (6 - t) / (1 - lam) if lam < 1 else float('inf')))
    return x, t, rows


def karp(W):
    n = W.shape[0]
    D = np.full((n + 1, n), -np.inf)
    D[0, :] = 0.0
    for k in range(1, n + 1):
        D[k] = (D[k - 1][:, None] + W).max(axis=0)
    best = -np.inf
    for v in range(n):
        if D[n, v] == -np.inf:
            continue
        m = min((D[n, v] - D[k, v]) / (n - k) for k in range(n) if D[k, v] > -np.inf)
        best = max(best, m)
    return best


if __name__ == '__main__':
    x, t, rows = main()
    import json
    tag = OPTS.get('tag', 'v0')
    with open(os.path.join(HERE, 'sol_%s.json' % tag), 'w') as fo:
        json.dump({'t': t, 'x': {repr(k): x[i] for i, k in enumerate(VARL) if x[i] > 1e-12}}, fo, indent=0)
