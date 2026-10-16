"""Class (c) pool LP (exploratory, loop/rules).  A rule y(A, j): the amount a 5 at slot j of receiver arrangement A
(u's link word + s word, letters 5..9) sends to u.  Sender rows are SITUATIONS: a 5 v plus one arrangement view per
big neighbour of v, pairwise consistent on the vertices both views see (canonical coordinates around v, below).
POOL = a finite set of receiver arrangements (files with 'd=.. link .. s ..' lines).  Only situations whose every big
neighbour has a view in the pool are rows, so the optimum is a LOWER bound on the class-(c) LP whose rows are
pool arrangements + pool-closed situations (sound as a lower bound only if those situations are realizable; the
consistency test is pairwise letter agreement, a necessary condition).  Modes:
  tie   : y(A, j) = y(root word)  (rooted-word rule on the same rows; isolates the effect of information)
  free  : y(A, j) free per slot (class (c))
  nomir : free, and drop situations in which two big neighbours carry the SAME (arrangement, slot) (mirror pairs)
  noLL  : free, and drop situations with >= 2 'loaded' big neighbours (arrangement has a lone sender: one big nbr)
Usage: python3 rules_c.py OUT POOLFILE[:dmax] ... [mode=tie,free,nomir,noLL]"""
import sys, os, re, itertools, collections
import numpy as np
from scipy.optimize import linprog
D = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
ARGS = sys.argv[1:]
src = open(D + '/wlp.py').read().replace('__file__', repr(D + '/wlp.py'))
sys.argv = ['wlp']; exec(src[:src.index('# receiver DP')])
MODES = next((a[5:] for a in ARGS if a.startswith('mode=')), 'tie,free,nomir,noLL').split(',')
OUTF = ARGS[0]; FILES = [a for a in ARGS[1:] if not a.startswith('mode=')]

def ok_arr(d, w, s):
    U = min(d, 9)
    for i in range(d):
        if w[i] == 5 and isR5([U, w[(i + 1) % d], s[i], s[i - 1], w[i - 1]]): return False
        if w[i] == 6 and all(isR6([U, w[(i + 1) % d], s[i], p, s[i - 1], w[i - 1]]) for p in L): return False
    return True
def images(d, w, s):
    for r in range(d):
        yield tuple(w[(k + r) % d] for k in range(d)), tuple(s[(k + r) % d] for k in range(d))
        yield tuple(w[(r - k) % d] for k in range(d)), tuple(s[(r - k - 1) % d] for k in range(d))
POOL = {}   # canonical (d, w, s) -> id
ARR = []
for a in FILES:
    fn, dmax = (a.split(':') + ['99'])[:2]; dmax = int(dmax)
    for line in open(fn):
        m = re.search(r'd=(\d+) link (\d+) s (\d+)', line)
        if not m: continue
        d = int(m.group(1))
        if d > dmax: continue
        w = [int(c) for c in m.group(2)]; s = [int(c) for c in m.group(3)]
        mi = min(images(d, w, s)); key = (d,) + mi[0] + mi[1]
        if key in POOL: continue
        assert ok_arr(d, w, s), line
        POOL[key] = len(ARR); ARR.append(key)
print('pool:', collections.Counter(k[0] for k in ARR), flush=True)

def red(o, deg):
    if deg > 8: return o
    o %= deg
    return o - deg if o > deg // 2 else o
def cN(k, o, X):
    k %= 5; o = red(o, X[k])
    if o == 0: return ('v',)
    if o == 1: return ('x', (k + 1) % 5)
    if o == -1: return ('x', (k - 1) % 5)
    if o == 2: return cN(k + 1, -2, X)
    return ('N', k, o)
def view(d, w, s, j, p):
    """coords -> letter for the arrangement (w, s) centred at x_p with v = w_j"""
    U = min(d, 9); X = [0] * 5
    for t, val in enumerate((U, w[(j + 1) % d], s[j], s[(j - 1) % d], w[(j - 1) % d])): X[(p + t) % 5] = val
    V = {('x', k): X[k] for k in range(5)}
    lo = -((d - 1) // 2); hi = d // 2
    for o in range(lo, hi + 1):
        if o in (0, 1, -1): continue
        V[cN(p, o, X)] = w[(j + o) % d]
    for o in range(-(d // 2), d - d // 2):
        val = s[(j + o) % d]
        if o == 0: key = ('x', (p + 2) % 5)
        elif o == -1: key = ('x', (p + 3) % 5)
        elif o == 1: key = cN(p + 1, -3, X)
        elif o == -2: key = cN(p - 1, 3, X)
        elif o == 2: key = ('S', p % 5, 2)
        elif o == -3 and w[(j - 2) % d] == 5: key = ('S', (p - 1) % 5, 2)
        else: key = ('S', p % 5, o)
        if key in V and V[key] != val: return None, X      # self-inconsistent (tiny-degree wrap)
        V[key] = val
    return V, X
def consistent(A, B):
    if len(A) > len(B): A, B = B, A
    for k, v in A.items():
        b = B.get(k)
        if b is not None and b != v: return False
    return True

# views: index[(p, X)] -> list of (varid, view); vars = (aid, j)
VAR = {}; VARL = []
index = collections.defaultdict(list); main = []
LOADED = set()
for aid, (d, *ws) in enumerate(ARR):
    w, s = list(ws[:d]), list(ws[d:]); U = min(d, 9)
    for j in range(d):
        if w[j] != 5: continue
        word = [U, w[(j + 1) % d], s[j], s[j - 1], w[j - 1]]
        if sum(1 for c in word if c >= 7) == 1: LOADED.add(aid)
        vid = VAR.setdefault((aid, j), len(VARL))
        if vid == len(VARL): VARL.append((aid, j, root(word, 0)))
        for ori in (1, -1):
            if ori == 1: ww, ss, jj = w, s, j
            else: ww = [w[(-k) % d] for k in range(d)]; ss = [s[(-k - 1) % d] for k in range(d)]; jj = (-j) % d
            for p in range(5):
                V, X = view(d, ww, ss, jj, p)
                if V is None: continue
                if p == 0:
                    if ori == 1: main.append((vid, V, X))
                else: index[(p, tuple(X))].append((vid, V))
print('vars', len(VARL), 'main views', len(main), 'loaded arrangements', len(LOADED), flush=True)

COL = {}
def vec(V):
    for c in V: COL.setdefault(c, len(COL))
BUCK = {}
for key, lst in index.items():
    for _, V in lst: vec(V)
for _, V, _ in main: vec(V)
NC = len(COL)
def tov(V):
    a = np.zeros(NC, dtype=np.int8)
    for c, l in V.items(): a[COL[c]] = l
    return a
for key, lst in index.items():
    BUCK[key] = (np.array([v for v, _ in lst]), np.array([tov(V) for _, V in lst]))
def okmask(M, a):
    return ~(((M != 0) & (a != 0) & (M != a)).any(axis=1))
SIT = {}   # sorted vids -> 1
nsit_raw = 0; capped = 0
for vid, V0, X in main:
    P = [k for k in range(1, 5) if X[k] >= 7]
    a0 = tov(V0); cands = []
    for k in P:
        b = BUCK.get((k, tuple(X)))
        if b is None: cands = None; break
        m = okmask(b[1], a0); cands.append((b[0][m], b[1][m]))
        if not m.any(): cands = None; break
    if cands is None: continue
    tot = 1
    for c in cands: tot *= len(c[0])
    if tot > 200000: capped += 1; continue
    def rec(i, chosen, M):
        global nsit_raw
        if i == len(P):
            nsit_raw += 1; SIT.setdefault(tuple(sorted(chosen)), 1); return
        ids, MM = cands[i]
        ok = np.ones(len(ids), bool)
        for a in M: ok &= okmask(MM, a)
        for t in np.nonzero(ok)[0]: rec(i + 1, chosen + [int(ids[t])], M + [MM[t]])
    rec(0, [vid], [])
print('situations', len(SIT), 'raw', nsit_raw, 'main views skipped (>2e5 combos)', capped, 'coords', NC, flush=True)

def solve(mode):
    rk = sorted({r for _, _, r in VARL}); rix = {r: i for i, r in enumerate(rk)}
    nv = (len(rk) if mode == 'tie' else len(VARL)) + 1
    col = (lambda vid: rix[VARL[vid][2]]) if mode == 'tie' else (lambda vid: vid)
    rows, rhs, tags = [], [], []
    for sit in SIT:
        if mode == 'nomir' and len(set(sit)) < len(sit): continue
        if mode == 'noLL' and sum(1 for v in sit if VARL[v][0] in LOADED) >= 2: continue
        r = np.zeros(nv); r[-1] = -1
        for v in sit: r[col(v)] -= 1
        rows.append(r); rhs.append(-1); tags.append(('S', sit))
    byA = collections.defaultdict(list)
    for vid, (aid, j, _) in enumerate(VARL): byA[aid].append(vid)
    for aid, vids in byA.items():
        r = np.zeros(nv); r[-1] = -1
        for v in vids: r[col(v)] += 1
        rows.append(r); rhs.append(ARR[aid][0] - 6); tags.append(('R', aid))
    res = linprog(np.eye(nv)[-1], A_ub=np.array(rows), b_ub=np.array(rhs), bounds=[(0, 1)] * (nv - 1) + [(None, None)],
                  method='highs')
    du = -res.ineqlin.marginals
    out = ['## mode=%s: %d sender-situation rows, %d receiver rows, %d vars; t_low = %.6f' % (mode, sum(1 for t in tags if t[0] == 'S'), len(byA), nv - 1, res.fun)]
    for k in np.argsort(-du)[:40]:
        if du[k] < 1e-9: break
        tg = tags[k]
        if tg[0] == 'S':
            out.append('  %.4f sit  %s' % (du[k], ' + '.join('A%d.%d[%d|%s]%s' % (VARL[v][0], VARL[v][1], VARL[v][2][0], ''.join(map(str, VARL[v][2][1:])), '*' if VARL[v][0] in LOADED else '') for v in tg[1])))
        else:
            a = ARR[tg[1]]; d = a[0]
            out.append('  %.4f recv A%d d=%d link %s s %s' % (du[k], tg[1], d, ''.join(map(str, a[1:d + 1])), ''.join(map(str, a[d + 1:]))))
    return out
OUT = ['# rules_c %s' % ' '.join(ARGS), 'pool %s, vars %d, situations %d (skipped main views %d)' % (dict(collections.Counter(k[0] for k in ARR)), len(VARL), len(SIT), capped)]
for m in MODES:
    o = solve(m); OUT += o; print('\n'.join(o[:12]), flush=True)
open(OUTF, 'w').write('\n'.join(OUT) + '\n')
