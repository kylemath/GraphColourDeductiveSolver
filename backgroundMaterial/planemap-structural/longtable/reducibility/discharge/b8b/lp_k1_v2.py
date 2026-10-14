"""Job 18 (Studio, exploratory): lp_k1.py with the updated R.  Status per K = 1 key (b8b/out/k1keys.tsv):
  R if old R, or centre word 66666 (w66666 C-reducible, Job 16), or D-reducible in Job 14 / Job 13;
  notD if tested not D (and not 66666-centred); U if still untested (the 47 deferred ring 17-19 keys).
Case (a'): U counts as non-R.  Case (b'): U excluded.  Same receiver rows as lp_k1.py (explicit class graphs) plus the
proved bound (<= d lone-u senders)."""
import sys, os, collections
import numpy as np
from scipy.optimize import linprog
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import ball, patch
c66 = lambda k: all(b.split(':')[0] == '6' for b in k.split('|'))
dres = {}
for fn in ('out/dres-K1-studio.txt', 'studio13/dres-r15-16-studio.txt'):
    for line in open(os.path.join(os.path.dirname(HERE), fn)):
        if line.startswith('#'): continue
        f = line.split(); dres[f[0]] = f[2]
keys = {}; tally = collections.Counter()
for line in open(os.path.join(HERE, 'out', 'k1keys.tsv')):
    f = line.rstrip('\n').split('\t')
    if f[2] != '1': continue
    k, st = f[0], f[5]
    if st == 'R' or c66(k): new = 'R'
    elif dres.get(k) == 'D': new = 'R'
    elif dres.get(k) == 'notD': new = 'notD'
    elif st == 'notD': new = 'notD'
    else: new = 'U'
    keys[k] = (new, int(f[4]), f[3]); tally[(st, new)] += 1
print('status changes (old -> new):', dict(tally))
recv = []
for fn in ('patches.txt', 'search7.txt'):
    p = os.path.join(HERE, 'out', fn)
    if not os.path.exists(p): continue
    for line in open(p):
        name, rot = ball.parse_line(line)
        S = patch.senders(rot, 0)
        recv.append((name, len(rot[0]), collections.Counter(s['key'] for s in S if s['lone'])))
for case, ok in (("a'", ('U', 'notD')), ("b'", ('notD',))):
    send = sorted(k for k, v in keys.items() if v[0] in ok)
    print("case (%s): non-R K=1 senders %d %s" % (case, len(send), dict(collections.Counter((keys[k][2], keys[k][1]) for k in send))))
    if not send:
        print('   no senders: every K=1 2-ball is in R, t* <= 0 trivially (every 5 with K <= 1 is reducible)'); continue
    idx = {k: i for i, k in enumerate(send)}; nv = len(send) + 1
    A = []; b = []; names = []
    for k in send:
        a = np.zeros(nv); a[idx[k]] = -1; a[-1] = -1; A.append(a); b.append(-1); names.append('S ' + k)
    for name, d, C in recv:
        a = np.zeros(nv); a[-1] = -1; m = 0
        for k, c in C.items():
            if k in idx: a[idx[k]] += c; m += c
        if m == 0: continue
        A.append(a); b.append(d - 6); names.append('R %s (deg %d, %d senders)' % (name, d, m))
    c = np.zeros(nv); c[-1] = 1
    res = linprog(c, A_ub=np.array(A), b_ub=np.array(b), bounds=[(0, 1)] * len(send) + [(None, None)], method='highs')
    y = -res.ineqlin.marginals
    print('   explicit receiver rows %d, t* = %.6f (explicit rows only)' % (len(A) - len(send), res.x[-1]))
    for i in np.argsort(-y)[:6]:
        if y[i] > 1e-9: print('   dual %.4f  %s' % (y[i], names[i]))
    # closed form with the proved bound: a receiver of degree d holds at most d lone senders, but only of the
    # non-R types; give the per-degree worst case k_d = min(d, #positions those keys can occupy)
    byd = collections.Counter(keys[k][1] for k in send)
    print('   senders by big-vertex degree:', dict(byd))
