"""Wheel-level discharging LP with receiver-centred forbidden patterns (README §6, exploratory).
Sender rows and rooted-word variables as wlp.py (wheel R + certified C wheels + D fans), plus the D 7-/8-wheels (bigw).
Receiver rows for exact d = 7..DMAXP come from bin/sep (sep.cpp): the heaviest arrangements (w_i, s_i) that contain
no forbidden pattern.  A pattern = a receiver of exact degree d + a sender set S with abstract rooted words over
{5, 6, B} (B = degree >= 7, a free ring vertex); it is read from a dfast output line's name (p<d>_... from pairs.py,
e<d>_... from pairs2.py).  Rows for d = DMAXP+1..30 use the plain DP of wlp.py; the Karp letter-9 bound covers the rest.
Usage: python3 wlp2.py [tag=NAME] [pat=FILE[:all]] ...   (':all' = every line of FILE is forbidden, not only D=true)
       [dmaxp=15] [oracle=R: forbid every arrangement with a sender set S, |S| >= 2, whose configuration has ring <= R,
       whatever its verdict -- an optimistic bound on what ring <= R receiver-centred configurations can do]"""
import sys, os, subprocess, itertools, collections
import numpy as np
from scipy.optimize import linprog
HERE = os.path.dirname(os.path.abspath(__file__))
ARGS = sys.argv[1:]
src = open(os.path.join(HERE, 'wlp.py')).read().replace('__file__', repr(os.path.join(HERE, 'wlp.py')))
sys.argv = ['wlp']; exec(src[:src.index('# ---- option bigw')]); sys.argv = [sys.argv[0]] + ARGS
TAG = next((a[4:] for a in ARGS if a.startswith('tag=')), 'run')
DMAXP = int(next((a[6:] for a in ARGS if a.startswith('dmaxp=')), '15'))
OMAX = int(next((a[7:] for a in ARGS if a.startswith('oracle=')), '0'))   # forbid every sender set with ring <= OMAX
RBIG = set()
for line in open(os.path.join(HERE, 'out', 'bigwheels_dfast.out')):
    if 'D=true' in line: RBIG.add(line.split()[0].split('_')[1])
AB = {5: 0, 6: 1, 7: 2, 8: 2, 9: 2}
def code(a, b, c, e): return AB[a] * 27 + AB[b] * 9 + AB[c] * 3 + AB[e]

def parse(name):
    """pattern name -> (d, [(pos, code)]) or None.  Unspecified: '.', '9' in a p-link, '0' in a p-s word."""
    f = name.split('_'); d = int(f[0][1:]); lk, sv = f[1], f[2]
    def L(ch, kind):
        if ch == '.' or (f[0][0] == 'p' and ((kind == 'w' and ch == '9') or (kind == 's' and ch == '0'))): return None
        return 'B' if ch == 'B' else int(ch)
    w = [L(ch, 'w') for ch in lk]; s = [L(ch, 's') for ch in sv]
    A = {5: 0, 6: 1, 'B': 2}; P = []
    for i in range(d):
        if w[i] != 5: continue
        r = (w[(i + 1) % d], s[i], s[(i - 1) % d], w[(i - 1) % d])
        if None in r: continue
        P.append((i, A[r[0]] * 27 + A[r[1]] * 9 + A[r[2]] * 3 + A[r[3]]))
    return d, P
PATS = []; PSRC = collections.Counter()
for a in ARGS:
    if not a.startswith('pat='): continue
    fn = a[4:]; allf = fn.endswith(':all'); fn = fn[:-4] if allf else fn
    for line in open(fn if os.path.isabs(fn) else os.path.join(HERE, fn)):
        if not line.strip(): continue
        if allf or 'D=true' in line:
            d, P = parse(line.split()[0])
            assert len(P) >= 1, line
            PATS.append((d, P)); PSRC[(os.path.basename(fn), d)] += 1
print('patterns:', dict(PSRC), flush=True)

# static tables for sep: per U, state a = (wp, sp, wc) -> choice (sc, wn)
lines = [str(len(roots))]
for U in (7, 8, 9):
    for (wp, sp, wc) in states:
        for sc in L:
            for wn in L:
                al, v, cd = 1, -1, -1
                if wc == 5:
                    w = [U, wn, sc, sp, wp]
                    if isR5(w): al = 0
                    else: v = ix[root(w, 0)]; cd = code(wn, sc, sp, wp)
                elif wc == 6:
                    if all(isR6([U, wn, sc, p, sp, wp]) for p in L): al = 0
                lines.append('%d %d %d' % (al, v, cd))
lines.append(str(len(RBIG))); lines += sorted(RBIG)
lines.append(str(len(PATS)))
for d, P in PATS: lines.append('%d %d %s' % (d, len(P), ' '.join('%d %d' % pc for pc in P)))
os.makedirs(os.path.join(HERE, 'bin'), exist_ok=True)
SF = os.path.join(HERE, 'bin', 'sep_%s.in' % TAG); open(SF, 'w').write('\n'.join(lines) + '\n')
SEP = subprocess.Popen([os.path.join(HERE, 'bin', 'sep'), SF], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
def sep(d, yv, thr, many):
    SEP.stdin.write('q %d %.12f %d %d\n%s\n' % (d, thr, many, OMAX, ' '.join('%.12f' % x for x in yv))); SEP.stdin.flush()
    out = []
    while True:
        f = SEP.stdout.readline().split()
        if f[0] == 'END': return out, int(f[2])
        out.append((float(f[1]), f[2], f[3], tuple(roots[int(x)] for x in f[4:])))

A_ub, b_ub = [], []
for w in senders:
    row = np.zeros(nv); row[-1] = -1
    for j in range(5):
        if w[j] >= 7: row[ix[root(list(w), j)]] -= 1
    A_ub.append(row); b_ub.append(-1)
rec_rows = []; have = set(); info = {}
def add_rows(dlist, many):
    added = 0
    for d in dlist:
        thr = d - 6 + t + 1e-7
        if d <= DMAXP:
            res_, nodes = sep(d, yv, thr, many); gen = [(v, p) for v, lk, sv, p in res_]
            for v, lk, sv, p in res_: info.setdefault((d, tuple(sorted(p))), (lk, sv))
        else:
            gen = best_arrangement(d, yv, return_all=many, thr=thr)
        for val, path in gen:
            path = tuple(sorted(path))
            if (d, path) in have: continue
            have.add((d, path)); row = np.zeros(nv); row[-1] = -1
            for r in path: row[ix[r]] += 1
            A_ub.append(row); b_ub.append(d - 6); rec_rows.append((d, path)); added += 1
    return added
DS = list(range(7, 13)); DSF = list(range(7, 31))
WARM = next((a[5:] for a in ARGS if a.startswith('warm=')), None)   # earlier tight/row file: reuse rows still allowed
def check(d, lk, sv):
    SEP.stdin.write('c %d %s %s\n' % (d, lk, sv)); SEP.stdin.flush(); return SEP.stdout.readline().strip() == '1'
nwarm = 0
if WARM:
    import re as _re
    for line in open(WARM):
        m = _re.search(r'receiver d=(\d+) link (\d+) s (\d+)', line)
        if not m: continue
        d, lk, sv = int(m.group(1)), m.group(2), m.group(3)
        if d > DMAXP or not check(d, lk, sv): continue
        U = min(d, 9); w = [int(c) for c in lk]; s_ = [int(c) for c in sv]
        path = tuple(sorted(root([U, w[(i + 1) % d], s_[i], s_[(i - 1) % d], w[(i - 1) % d]], 0) for i in range(d) if w[i] == 5))
        if (d, path) in have: continue
        have.add((d, path)); info[(d, path)] = (lk, sv); row = np.zeros(nv); row[-1] = -1
        for r in path: row[ix[r]] += 1
        A_ub.append(row); b_ub.append(d - 6); rec_rows.append((d, path)); nwarm += 1
    print('warm rows', nwarm, flush=True)
ALLF = next((a[8:] for a in ARGS if a.startswith('allrows=')), None)   # write every receiver row's arrangement
yv = np.ones(nv - 1); t = 0.0
for it in range(5000):
    res = linprog(np.eye(nv)[-1], A_ub=np.array(A_ub), b_ub=np.array(b_ub),
                  bounds=[(0, 1)] * (nv - 1) + [(None, None)], method='highs')
    yv, t = res.x[:-1], res.x[-1]
    added = add_rows(DS, 40)
    if not added: added = add_rows(DSF, 40)
    print('iter', it, 't=%.6f' % t, 'rows', len(rec_rows), 'added', added, flush=True)
    if not added: break
res = linprog(np.eye(nv)[-1], A_ub=np.array(A_ub), b_ub=np.array(b_ub),
              bounds=[(0, 1)] * (nv - 1) + [(None, None)], method='highs')
duals = -res.ineqlin.marginals; yv = res.x[:-1]; t = res.x[-1]
out = ['# wlp2 %s: patterns %s; %d non-R sender words, %d rooted vars, %d receiver rows; t* = %.6f' % (
    ' '.join(ARGS), dict(PSRC), len(senders), len(roots), len(rec_rows), res.fun)]
out.append('dual certificate (rows with positive weight; receiver rows: link word w_0.., s word s_i between w_i,w_i+1):')
ns = len(senders)
for i, dv in enumerate(duals):
    if dv > 1e-9:
        if i < ns: out.append('  %.4f  sender %s' % (dv, ''.join(map(str, senders[i]))))
        else:
            d, path = rec_rows[i - ns]; lk, sv = info.get((d, path), ('?', '?'))
            out.append('  %.4f  receiver d=%d link %s s %s, %d 5-nbrs: %s' % (dv, d, lk, sv, len(path), ' '.join('%d|%s' % (r[0], ''.join(map(str, r[1:]))) for r in path)))
out.append('nonzero rule weights y[rooted word u|a b c e]:')
for r in roots:
    if res.x[ix[r]] > 1e-9: out.append('  %s|%s  %.4f' % (r[0], ''.join(map(str, r[1:])), res.x[ix[r]]))
# per-d slack at the optimum
for d in range(7, 31):
    if d <= DMAXP: v = sep(d, yv, -1.0, 1)[0]; v = v[0][0] if v else 0.0
    else: v = best_arrangement(d, yv)[0]
    out.append('d=%d: max receiver load %.6f vs d-6+t = %.6f' % (d, v, d - 6 + t))
def karp(M):
    n = M.shape[0]; D = np.full((n + 1, n), -np.inf); D[0, :] = 0.0
    for k in range(1, n + 1): D[k] = (D[k - 1][:, None] + M).max(axis=0)
    with np.errstate(invalid='ignore'):
        q = np.where(np.isfinite(D[n]), np.min(np.where(np.isfinite(D[:n]), (D[n] - D[:n]) / (n - np.arange(n))[:, None], np.inf), axis=0), -np.inf)
    return q.max()
M = np.full((NS, NS), -np.inf)
for a, b, r in TRI[9]: M[a, b] = max(M[a, b], yv[ix[r]] if r is not None else 0.0)
lam = karp(M)
out.append('letter-9 max cycle mean lambda = %.6f; d*lambda <= d-6+t for all d >= %s' % (
    lam, ('%.2f' % ((6 - t) / (1 - lam))) if lam < 1 else 'never'))
SEP.stdin.close(); SEP.wait()
slack = np.array(b_ub) - np.array(A_ub) @ res.x
tight = ['  receiver d=%d link %s s %s' % ((d,) + info.get((d, path), ('?', '?'))) for k, (d, path) in enumerate(rec_rows)
         if slack[ns + k] < 1e-7]
TF = next((a[6:] for a in ARGS if a.startswith('tight=')), None)
if TF: open(TF, 'w').write('\n'.join(tight) + '\n')
if ALLF: open(ALLF, 'w').write('\n'.join('  receiver d=%d link %s s %s' % ((d,) + info[(d, path)]) for d, path in rec_rows if (d, path) in info) + '\n')
out.append('tight receiver rows at the optimum: %d' % len(tight))
open(os.path.join(HERE, 'out', 'wlp2_%s.txt' % TAG), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out[:80]))
