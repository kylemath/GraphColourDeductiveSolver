"""Rule H ("lone five unloads to a big hat over a 66 spoke pair"), restricted LP (exploratory, E_rule_change).
Rule H: a degree-5 v with exactly one big neighbour (lone five) and two consecutive degree-6 spokes x, y whose hat z
(common neighbour of x, y other than v) has degree >= 7 sends h[w, k] to z (distance 2; physically through x and y).
The lone five's direct payment to its big neighbour becomes y[w, F], F = set of its 66 spoke pairs with a big hat.
Sender rows:   non-lone words as wlp.py;  lone word w, each F:  y[w,F] + sum_{k in F} h[w,k] >= 1 - t.
Receiver rows: an arrangement (d, link, s) of wlp3 plus the privates p_j of its link 6s (non-R 6-wheels) and the outer
hats q (free).  Load = sum over link 5s of y[...] (lone ones with their F read from p's/q) + sum over ring-2 fives s_j
with w_j = w_j+1 = 6 that are lone (word (6,6,p_j+1,q,p_j)) of h[...]; max over p's and q's (constraint generation).
Row source: out/job28/tight_13.txt (the rows tight at t* = 7/27) + rows from a pattern-free DP, each checked against
the j28_13 pattern registry with sep3 'c' (10 d=10-only pattern files of that registry are absent here; d<=9 unaffected).
RESTRICTED LP: its t is a LOWER bound for rule class base+H.  Usage: python3 hatlp.py [noh] [dp=ITERS]"""
import sys, os, itertools, re, subprocess, time
import numpy as np
from scipy.optimize import linprog
ME = os.path.dirname(os.path.abspath(__file__))
WD = os.path.abspath(os.path.join(ME, '..', '..', '..'))
ARGS = sys.argv[1:]
NOH = 'noh' in ARGS
DPIT = int(next((a[3:] for a in ARGS if a.startswith('dp=')), '0'))
src = open(os.path.join(WD, 'wlp.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(WD, 'wlp.py')))
sys.argv = ['wlp']; exec(src[:src.index('# ---- option bigw')])
# ---------------- sep3 for the pattern check only
pargs = open(os.path.join(WD, 'out', 'job28', 'j28_13.args')).read().split()
pargs = [a for a in pargs if not a.startswith(('pat=', 'cpat=')) or os.path.exists(os.path.join(WD, a.split('=', 1)[1].replace(':all', '')))]
w3 = open(os.path.join(WD, 'wlp3.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(WD, 'wlp3.py')), 1)
w3 = w3.replace("os.path.join(HERE, 'bin')", repr(os.path.join(ME, 'bin'))).replace("os.path.join(HERE, 'bin', ", "os.path.join(%r, " % os.path.join(ME, 'bin'))
sys.argv = ['wlp3', 'tag=hat'] + pargs
exec(w3[:w3.index('A_ub, b_ub = [], []')])
def check(d, lk, sv):
    SEP.stdin.write('c %d %s %s\n' % (d, lk, sv)); SEP.stdin.flush(); return SEP.stdout.readline().strip() == '1'
# ---------------- variables
BIG = (7, 8, 9)
def isbig(x): return x >= 7
def orient(x, j, rev):
    n = 5; return [x[(j + (-k if rev else k)) % n] for k in range(n)], ([(j + (-k if rev else k)) % n for k in range(n)])
def pairs66(o):  # o = (B,a,b,c,e): pair k = (o[k+1], o[k+2])
    return [k for k in range(3) if o[k + 1] == 6 and o[k + 2] == 6]
def lone(x): return sum(1 for v in x if v >= 7) == 1
def key_y(x, j, Fpos):
    """x cyclic 5-list, j = big root index, Fpos = set of cyclic position pairs {(m, m+1)} (as frozensets) flagged"""
    best = None
    for rev in (False, True):
        o, idx = orient(x, j, rev)
        F = tuple(sorted(k for k in range(3) if frozenset((idx[k + 1], idx[k + 2])) in Fpos))
        c = (tuple(o), F)
        best = c if best is None or c < best else best
    return best
def key_h(x, j, pr):
    best = None
    for rev in (False, True):
        o, idx = orient(x, j, rev)
        k = next(k for k in range(3) if frozenset((idx[k + 1], idx[k + 2])) == pr)
        c = (tuple(o), k); best = c if best is None or c < best else best
    return best
VAR = {}
def var(k):
    if k not in VAR: VAR[k] = len(VAR)
    return VAR[k]
var('t')
A_ub, b_ub, RINFO = [], [], []
for w in senders:
    x = list(w); bigs = [j for j in range(5) if x[j] >= 7]
    if lone(x) and not NOH:
        j = bigs[0]; o, idx = orient(x, j, False); P = pairs66(o)
        Ppos = [frozenset((idx[k + 1], idx[k + 2])) for k in P]
        for m in range(len(Ppos) + 1):
            for Fs in itertools.combinations(Ppos, m):
                row = {var('t'): -1.0}
                ky = ('y',) + key_y(x, j, set(Fs)); row[var(ky)] = row.get(var(ky), 0) - 1
                for pr in Fs:
                    kh = ('h',) + key_h(x, j, pr); row[var(kh)] = row.get(var(kh), 0) - 1
                A_ub.append(row); b_ub.append(-1.0); RINFO.append(('sender', ''.join(map(str, w)), len(Fs)))
    else:
        row = {var('t'): -1.0}
        for j in bigs:
            ky = ('y',) + key_y(x, j, set()); row[var(ky)] = row.get(var(ky), 0) - 1
        A_ub.append(row); b_ub.append(-1.0); RINFO.append(('sender', ''.join(map(str, w)), 0))
NSEND = len(A_ub)
# ---------------- receiver row evaluation
def p_opts(U, w, s, j, d):
    return [p for p in L if not isR6([U, w[(j + 1) % d], s[j], p, s[(j - 1) % d], w[(j - 1) % d]])]
def terms(d, w, s, P):
    """list of alternatives per independent unit: returns list of lists of {var: coef} dicts (max taken per unit)"""
    U = min(d, 9); units = []
    for i in range(d):
        if w[i] == 5:
            x = [U, w[(i + 1) % d], s[i], s[(i - 1) % d], w[(i - 1) % d]]
            if NOH or not lone(x): units.append([{('y',) + key_y(x, 0, set()): 1}]); continue
            o = x  # orientation already (B,a,b,c,e) with positions 0..4
            fixed = set(); alt = []
            if x[1] == 6 and x[2] == 6 and isbig(P[(i + 1) % d]): fixed.add(frozenset((1, 2)))
            if x[3] == 6 and x[4] == 6 and isbig(P[(i - 1) % d]): fixed.add(frozenset((3, 4)))
            opts = [fixed] + ([fixed | {frozenset((2, 3))}] if (x[2] == 6 and x[3] == 6) else [])
            units.append([{('y',) + key_y(x, 0, F): 1} for F in opts])
    if not NOH:
        for j in range(d):
            if w[j] == 6 and w[(j + 1) % d] == 6 and s[j] == 5:
                alts = []
                for q in L:
                    x = [6, 6, P[(j + 1) % d], q, P[j]]
                    if not lone(x) or isR5(x): continue
                    jb = next(k for k in range(5) if x[k] >= 7)
                    alts.append({('h',) + key_h(x, jb, frozenset((0, 1))): 1})
                if alts: units.append(alts + [{}])
    return units
def row_max(d, lk, sv, val):
    w = [int(c) for c in lk]; s = [int(c) for c in sv]; U = min(d, 9)
    six = [j for j in range(d) if w[j] == 6]
    opts = [p_opts(U, w, s, j, d) for j in six]
    if any(not o for o in opts): return None
    best = None
    for combo in itertools.product(*opts):
        P = [0] * d
        for j, p in zip(six, combo): P[j] = p
        tot = {}; v = 0.0
        for alts in terms(d, w, s, P):
            sc = [sum(val.get(k, 0.0) * c for k, c in a.items()) for a in alts]
            m = int(np.argmax(sc)); v += sc[m]
            for k, c in alts[m].items(): tot[k] = tot.get(k, 0) + c
        if best is None or v > best[0]: best = (v, tot, combo)
    return best

# ---------------- pattern-free DP over (w, p, s) arrangements (heuristic separation; candidates checked with sep3 'c')
WP = [(w_, 0) for w_ in (5, 7, 8, 9)] + [(6, p) for p in L]
DST = [(a, b, c) for a in WP for b in L for c in WP]          # (w_{i-1},p_{i-1}), s_{i-1}, (w_i,p_i)
DSI = {x: i for i, x in enumerate(DST)}
def unit_val(alts, val): return max(sum(val.get(k, 0.0) * c for k, c in a.items()) for a in alts)
_TCACHE = {}
def dp_struct(U):
    if U in _TCACHE: return _TCACHE[U]
    T = []
    for (A, sp, C) in DST:
        (wp, pp), (wc, pc) = A, C
        for sc in L:
            for Bn in WP:
                wn, pn = Bn; units = []
                if wc == 6 and isR6([U, wn, sc, pc, sp, wp]): continue
                if wc == 5:
                    x = [U, wn, sc, sp, wp]
                    if isR5(x): continue
                    if NOH or not lone(x): units.append([('y',) + key_y(x, 0, set())])
                    else:
                        fixed = set()
                        if x[1] == 6 and x[2] == 6 and pn >= 7: fixed.add(frozenset((1, 2)))
                        if x[3] == 6 and x[4] == 6 and pp >= 7: fixed.add(frozenset((3, 4)))
                        opts = [fixed] + ([fixed | {frozenset((2, 3))}] if (x[2] == 6 and x[3] == 6) else [])
                        units.append([('y',) + key_y(x, 0, F) for F in opts])
                if not NOH and wc == 6 and wn == 6 and sc == 5:
                    al = []
                    for q in L:
                        x = [6, 6, pn, q, pc]
                        if not lone(x) or isR5(x): continue
                        jb = next(k for k in range(5) if x[k] >= 7)
                        al.append(('h',) + key_h(x, jb, frozenset((0, 1))))
                    if al: units.append(al + [None])
                T.append((DSI[(A, sp, C)], DSI[(C, sc, Bn)], units))
    _TCACHE[U] = T; return T
def dp_matrix(d, val):
    n = len(DST); M = np.full((n, n), -np.inf)
    for a, b, units in dp_struct(min(d, 9)):
        v = sum(max((val.get(k, 0.0) if k is not None else 0.0) for k in u) for u in units)
        if v > M[a, b]: M[a, b] = v
    return M
def dp_cands(d, val, thr):
    M = dp_matrix(d, val); n = M.shape[0]; out = set()
    for a0 in range(n):
        v = np.full(n, -np.inf); v[a0] = 0.0; back = []
        for step in range(d):
            cand = v[:, None] + M; arg = cand.argmax(axis=0); v = cand[arg, np.arange(n)]; back.append(arg)
        if v[a0] <= thr: continue
        seq = [a0]; cur = a0
        for step in range(d - 1, -1, -1): cur = back[step][cur]; seq.append(cur)
        seq = seq[::-1][:d]          # states at steps 0..d-1
        lk = ''.join(str(DST[x][2][0]) for x in seq); sv = ''.join(str(DST[DSI_next][1]) for DSI_next in seq[1:] + seq[:1])
        out.add((lk, sv))
    return out
ROWS = []
for line in open(os.path.join(WD, 'out', 'job28', 'tight_13.txt')):
    m = re.search(r'receiver d=(\d+) link (\d+) s (\d+)', line)
    if m: ROWS.append((int(m.group(1)), m.group(2), m.group(3)))
HAVE = set(); RSET = set(ROWS)
def solve():
    nv = len(VAR); A = np.zeros((len(A_ub), nv))
    for r, row in enumerate(A_ub):
        for k, c in row.items(): A[r, k] += c
    bounds = [(None, None) if k == 'tdummy' else (0, 1) for k in range(nv)]; bounds[var('t')] = (None, None)
    c = np.zeros(nv); c[var('t')] = 1
    res = linprog(c, A_ub=A, b_ub=np.array(b_ub), bounds=bounds, method='highs')
    inv = {i: k for k, i in VAR.items()}
    return res, {inv[i]: res.x[i] for i in range(nv)}
def add_row(d, lk, sv, tot, combo):
    keyr = (d, lk, sv, tuple(sorted(tot.items())))
    if keyr in HAVE: return False
    HAVE.add(keyr); row = {var('t'): -1.0}
    for k, cf in tot.items(): row[var(k)] = row.get(var(k), 0) + cf
    A_ub.append(row); b_ub.append(d - 6.0); RINFO.append(('recv', d, lk, sv, combo)); return True
val = {}
t0 = time.time()
for it in range(60):
    added = 0; tt = val.get('t', -1.0)
    for d, lk, sv in ROWS:
        b = row_max(d, lk, sv, val)
        if b is None: continue
        if b[0] > d - 6 + tt + 1e-7 or it == 0:
            added += add_row(d, lk, sv, b[1], b[2])
    if DPIT and it >= 1 and it <= DPIT:
        for d in (7, 8, 9):
            c = dp_cands(d, val, d - 6 + tt + 1e-7); nn = 0
            for lk, sv in sorted(c):
                if (d, lk, sv) in RSET or not check(d, lk, sv): continue
                RSET.add((d, lk, sv)); ROWS.append((d, lk, sv)); nn += 1
                b = row_max(d, lk, sv, val)
                if b is not None: added += add_row(d, lk, sv, b[1], b[2])
            print('  dp d=%d: %d cycles above thr, %d new allowed rows' % (d, len(c), nn), flush=True)
    res, val = solve()
    print('iter %d t=%.6f rows %d added %d vars %d (%.0fs)' % (it, val['t'], len(A_ub), added, len(VAR), time.time() - t0), flush=True)
    if not added: break
OUT = [ln for ln in []]
duals = -res.ineqlin.marginals
print('RESULT t* (restricted, lower bound) = %.6f  %s' % (val['t'], 'noh' if NOH else 'rule H'))
for i, dv in enumerate(duals):
    if dv > 1e-9: print('  dual %.4f %s' % (dv, RINFO[i]))
for k, v in sorted(val.items(), key=lambda kv: -kv[1]):
    if k != 't' and k[0] == 'h' and v > 1e-9: print('  h', k, '%.4f' % v)
import json
json.dump({'t': val['t'], 'vars': {repr(k): v for k, v in val.items() if v > 1e-12}, 'rows': ROWS},
          open(os.path.join(ME, 'hatlp_%s.json' % ('noh' if NOH else 'h')), 'w'))
SEP.stdin.close()
