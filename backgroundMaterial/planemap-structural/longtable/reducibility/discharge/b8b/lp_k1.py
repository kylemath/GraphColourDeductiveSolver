"""B8b (exploratory): the LP over the complete K <= 1 sender key list.
Variables: sigma[key] = amount a K = 1 sender with this key sends to its unique big vertex (the only legal target
of a rule of the 4/7 shape), plus t.  Sender rows: every non-R K = 1 key: 1 - sigma[key] <= t (ALL keys of the list,
not samples).  Receiver rows: (6 - d) + sum sigma over the lone-u senders around u, for
  (i) every explicit class graph in b8b/out/{patches,search7}.txt (actual keys), and
  (ii) the proved bound: at most d lone-u senders (README 8.2), which with any sigma <= 1 gives the worst row
       (6 - d) + d * max sigma; the LP optimum with (ii) is computed in closed form below.
Case (a): untested keys count as non-R.  Case (b): untested keys excluded (only tested-not-D keys are senders).
Minimise t; print t, sigma on the receivers' keys, and the dual weights (certificate)."""
import sys, os, collections
import numpy as np
from scipy.optimize import linprog
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import ball, patch

keys = {}
for line in open(os.path.join(HERE, 'out', 'k1keys.tsv')):
    f = line.rstrip('\n').split('\t')
    if f[2] == '1': keys[f[0]] = (f[5], int(f[4]), f[3])
recv = []
for fn in ('patches.txt', 'search7.txt'):
    p = os.path.join(HERE, 'out', fn)
    if not os.path.exists(p): continue
    for line in open(p):
        name, rot = ball.parse_line(line)
        S = patch.senders(rot, 0)
        recv.append((name, len(rot[0]), collections.Counter(s['key'] for s in S if s['lone'])))

for case, ok in (('a', ('U', 'notD')), ('b', ('notD',))):
    send = sorted(k for k, v in keys.items() if v[0] in ok)
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
    print('case (%s): sender rows %d (all non-R K=1 keys), explicit receiver rows %d, t = %.6f' % (
        case, len(send), len(A) - len(send), res.x[-1]))
    for i in np.argsort(-y)[:6]:
        if y[i] > 1e-9: print('   dual %.4f  %s' % (y[i], names[i]))
print('closed form with the proved bound (<= d lone-u senders, sigma uniform):')
print('   receiver d with k senders: t >= (k - (d - 6)) / (k + 1);  d = 8, k = 8 (hemi8, notD): t = 2/3;'
      '  d = 7, k <= 7: t <= 3/4;  d >= 9, k <= d: t <= 6/(d+1) <= 0.6')
