"""Lower bound on t* that no receiver-centred configuration of ring <= RMAX can remove (README §6, exploratory).
Input: HARD arrangements written by gen.py (receiver d, link word, s word), i.e. arrangements every sender set of which
(|S| >= 2, ring <= RMAX, pairs2.py type: u + S + links, B free) has been tested by dfast and found not D.  The LP is the
sender rows of wlp.py plus only these receiver rows, so its optimum t_hard is a lower bound for wlp2.py with every D
configuration of that type and ring <= RMAX forbidden (dfast-only verdicts; see README §6).
Option nopendC: drop HARD rows containing a not-D overload at a 7 whose C verdict is pending (Studio Job 27), i.e.
the bound if every pending C verdict comes back C.
Usage: python3 hardlp.py OUT.txt HARDFILE [HARDFILE ...] [nopendC]"""
import sys, os, re
import numpy as np
from scipy.optimize import linprog
HERE = os.path.dirname(os.path.abspath(__file__))
ARGS = sys.argv[1:]
src = open(os.path.join(HERE, 'wlp.py')).read().replace('__file__', repr(os.path.join(HERE, 'wlp.py')))
sys.argv = ['wlp']; exec(src[:src.index('# receiver DP')])
NOC = 'nopendC' in ARGS; ARGS = [a for a in ARGS if a != 'nopendC']
OUTF, FILES = ARGS[0], ARGS[1:]
rows = {}
for fn in FILES:
    for line in open(fn):
        m = re.search(r'HARD d=(\d+) link (\d+) s (\d+)', line)
        if not m: continue
        if NOC and not re.search(r'pendC=0\)', line): continue      # drop rows a pending C verdict (Job 27) could remove
        d, lk, sv = int(m.group(1)), m.group(2), m.group(3); U = min(d, 9)
        w = [int(c) for c in lk]; s = [int(c) for c in sv]; path = []
        for i in range(d):
            if w[i] == 5:
                ww = [U, w[(i + 1) % d], s[i], s[(i - 1) % d], w[(i - 1) % d]]
                assert not isR5(ww), (lk, sv, i)
                path.append(root(ww, 0))
            elif w[i] == 6:
                assert not all(isR6([U, w[(i + 1) % d], s[i], p, s[(i - 1) % d], w[(i - 1) % d]]) for p in L)
        rows.setdefault((d, tuple(sorted(path))), (lk, sv))
A_ub, b_ub = [], []
for w in senders:
    row = np.zeros(nv); row[-1] = -1
    for j in range(5):
        if w[j] >= 7: row[ix[root(list(w), j)]] -= 1
    A_ub.append(row); b_ub.append(-1)
keys = list(rows)
for d, path in keys:
    row = np.zeros(nv); row[-1] = -1
    for r in path: row[ix[r]] += 1
    A_ub.append(row); b_ub.append(d - 6)
res = linprog(np.eye(nv)[-1], A_ub=np.array(A_ub), b_ub=np.array(b_ub),
              bounds=[(0, 1)] * (nv - 1) + [(None, None)], method='highs')
duals = -res.ineqlin.marginals; ns = len(senders)
out = ['# hardlp %s%s: %d HARD receiver rows; t_hard = %.6f' % (' '.join(FILES), ' nopendC' if NOC else '', len(keys), res.fun),
       'dual certificate:']
for i, dv in enumerate(duals):
    if dv > 1e-9:
        if i < ns: out.append('  %.4f  sender %s' % (dv, ''.join(map(str, senders[i]))))
        else:
            d, path = keys[i - ns]; lk, sv = rows[(d, path)]
            out.append('  %.4f  receiver d=%d link %s s %s: %s' % (dv, d, lk, sv, ' '.join('%d|%s' % (r[0], ''.join(map(str, r[1:]))) for r in path)))
open(OUTF, 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
