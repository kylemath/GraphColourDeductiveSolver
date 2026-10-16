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
Class (b) on top: rules_b.py adds 7->7 transfers z on big-big edges that share a 5 (pool LP, small pools only): sender rows are added while violated.
Usage: python3 rules_c2.py OUT POOLFILE[:dmax] ... [mode=tie,free,nomir,noLL]"""
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

# views -> sparse coords; vars = (aid, j)
VAR = {}; VARL = []; COL = {}
def sp(V):
    return np.array([COL.setdefault(c, len(COL)) for c in V], dtype=np.int32), np.array(list(V.values()), dtype=np.int8)
index = collections.defaultdict(list); main = []
LOADED = set()
for aid, key in enumerate(ARR):
    d = key[0]; w, s = list(key[1:d + 1]), list(key[d + 1:]); U = min(d, 9)
    for j in range(d):
        if w[j] != 5: continue
        word = [U, w[(j + 1) % d], s[j], s[j - 1], w[j - 1]]
        if sum(1 for c in word if c >= 7) == 1: LOADED.add(aid)
        vid = len(VARL); VARL.append((aid, j, root(word, 0)))
        for ori in (1, -1):
            if ori == 1: ww, ss, jj = w, s, j
            else: ww = [w[(-k) % d] for k in range(d)]; ss = [s[(-k - 1) % d] for k in range(d)]; jj = (-j) % d
            for p in range(5):
                V, X = view(d, ww, ss, jj, p)
                if V is None: continue
                if p == 0:
                    if ori == 1: main.append((vid, sp(V), X))
                else: index[(p, tuple(X))].append((vid, sp(V)))
NC = len(COL)
def dense(spv):
    a = np.zeros(NC, dtype=np.int8); a[spv[0]] = spv[1]; return a
BUCK = {k: (np.array([v for v, _ in lst], dtype=np.int64), np.array([dense(x) for _, x in lst])) for k, lst in index.items()}
del index
def okmask(M, a):
    return ~(((M != 0) & (a != 0) & (M != a)).any(axis=1))
LOADV = np.array([VARL[v][0] in LOADED for v in range(len(VARL))])
MAIN = []   # (vid, [(ids, mats) per big partner position]) ; lone senders have []
nskip = 0
for vid, spv, X in main:
    a0 = dense(spv); P = [k for k in range(1, 5) if X[k] >= 7]; cands = []
    for k in P:
        b = BUCK.get((k, tuple(X)))
        if b is None: cands = None; break
        m = okmask(b[1], a0)
        if not m.any(): cands = None; break
        cands.append((b[0][m], b[1][m]))
    if cands is None: nskip += 1; continue
    MAIN.append((vid, cands))
del main
print('vars', len(VARL), 'coords', NC, 'main views with a closed situation', len(MAIN), 'without', nskip,
      'by #partners', collections.Counter(len(c) for _, c in MAIN), flush=True)


# ---- class (b): big-big edges.  For receiver A (aid) and big link neighbour at position a, the partner view is found
# in the frame of a 5 v adjacent to both (v = w_{a+1} -> b = x4 ; v = w_{a-1} -> b = x1).  Edge variable: unordered
# pair {(aid, a), (aid', a')} (a' = u's position in A'), antisymmetric.
import itertools as it
VIEW0 = {}
for vid, cands in MAIN: VIEW0[vid] = cands
VID = {(aid, j): v for v, (aid, j, _) in enumerate(VARL)}
def partner_pos(aid2, vid2, p):
    """u's position in A' (original indexing) for partner view vid2 at frame position p (u = x0)."""
    return None
# rebuild partner views with orientation info for the pool (small pools only)
PART = collections.defaultdict(list)   # (p, X) -> list of (aid', a', dense view)
for aid, key in enumerate(ARR):
    d = key[0]; w, s_ = list(key[1:d + 1]), list(key[d + 1:])
    for j in range(d):
        if w[j] != 5: continue
        for ori in (1, -1):
            if ori == 1: ww, ss, jj = w, s_, j
            else: ww = [w[(-k) % d] for k in range(d)]; ss = [s_[(-k - 1) % d] for k in range(d)]; jj = (-j) % d
            for p in (1, 4):
                V, X = view(d, ww, ss, jj, p)
                if V is None: continue
                upos = (jj - 1) % d if p == 1 else (jj + 1) % d          # u = x0 = x_{p+4} (p=1) or x_{p+1} (p=4)
                if ori == -1: upos = (-upos) % d
                PART[(p, tuple(X))].append((aid, upos, dense(sp(V))))
EDGE = {}; ROWS_B = []
nmiss = 0
for aid, key in enumerate(ARR):
    d = key[0]; w, s_ = list(key[1:d + 1]), list(key[d + 1:]); U = min(d, 9)
    nbrs = []
    for a in range(d):
        if w[a] < 7: continue
        opts = []
        for jv, p in (((a + 1) % d, 4), ((a - 1) % d, 1)):
            if w[jv] != 5: continue
            V, X = view(d, w, s_, jv, 0); a0 = dense(sp(V))
            for aid2, a2, M in PART.get((p, tuple(X)), []):
                if okmask(M[None, :], a0)[0]: opts.append((aid2, a2))
            break
        if not opts: nmiss += 1; continue
        nbrs.append((a, sorted(set(opts))))
    for combo in it.product(*[o for _, o in nbrs]):
        terms = []
        for (a, _), (aid2, a2) in zip(nbrs, combo):
            k1, k2 = (aid, a), (aid2, a2)
            if k1 == k2: continue                       # mirror edge: z = 0 by antisymmetry
            key_ = tuple(sorted((k1, k2))); sg = 1 if key_[0] == k1 else -1
            EDGE.setdefault(key_, len(EDGE)); terms.append((EDGE[key_], sg))
        ROWS_B.append((aid, terms))
print('class b: edges', len(EDGE), 'receiver rows', len(ROWS_B), 'big nbrs without a common-5 view', nmiss, flush=True)
SITS = set()
for vid, cands in MAIN:
    if not cands: SITS.add((vid,)); continue
    for combo in it.product(*[list(range(len(c[0]))) for c in cands]):
        ok = True
        for x, y_ in it.combinations(range(len(combo)), 2):
            if not okmask(cands[x][1][combo[x]][None, :], cands[y_][1][combo[y_]])[0]: ok = False; break
        if ok: SITS.add(tuple(sorted([vid] + [int(cands[i][0][combo[i]]) for i in range(len(combo))])))
for mode in ('tie', 'free'):
    rk = sorted({r for _, _, r in VARL}); rix = {r: i for i, r in enumerate(rk)}
    nyv = len(rk) if mode == 'tie' else len(VARL); ne = len(EDGE); nv = nyv + ne + 1
    colv = np.array([rix[VARL[v][2]] for v in range(len(VARL))]) if mode == 'tie' else np.arange(len(VARL))
    A_, b_ = [], []
    for sit in SITS:
        r = np.zeros(nv); r[-1] = -1
        for v in sit: r[colv[v]] -= 1
        A_.append(r); b_.append(-1)
    for aid, terms in ROWS_B:
        r = np.zeros(nv); r[-1] = -1
        for v, (a2, j, _) in enumerate(VARL):
            if a2 == aid: r[colv[v]] += 1
        for e, sg in terms: r[nyv + e] -= sg
        A_.append(r); b_.append(ARR[aid][0] - 6)
    res = linprog(np.eye(nv)[-1], A_ub=np.array(A_), b_ub=np.array(b_), bounds=[(0, 1)] * nyv + [(-1, 1)] * ne + [(None, None)], method='highs')
    msg = '## class (b) mode=%s: %d situations, %d receiver rows, %d edge vars; t_low = %.6f' % (mode, len(SITS), len(ROWS_B), ne, res.fun)
    print(msg, flush=True)
    open(OUTF, 'a').write(msg + '\n')
