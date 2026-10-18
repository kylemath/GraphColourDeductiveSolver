"""Job 29: is a given solution (y, x, t) feasible for the LP over a given pattern registry?
- Exhaustive separation with bin/sep3x_new (SEP_NODELIMIT=0) at d = 7..DMAXP, threshold d - 6 + t + EPS.
- The max-plus DP at d = DMAXP+1..30 (z9 from the solution).
- The Karp letter-9 tail.
Usage: python3 feascheck.py SOLUTION.json [eps=1e-7] <pattern args as for wlp3x>   (WLP3X_DEF=1 keeps out/def_*)
Prints the violated rows (at most 20 per degree) and 'FEASIBLE' when there are none."""
import sys, os, json, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SOLF = sys.argv[1]; SOL = json.load(open(SOLF))
EPS = float(next((a[4:] for a in sys.argv[2:] if a.startswith('eps=')), '1e-7'))
PARGS = [a for a in sys.argv[2:] if not a.startswith('eps=')]
EXCL = ('hr1_or1',) if os.environ.get('WLP3X_DEF') == '1' else ('out/def_', 'hr1_or1')
PARGS = [a for a in PARGS if not (a.startswith(('pat=', 'cpat=')) and any(e in a for e in EXCL))]
src = open(os.path.join(HERE, 'wlp3.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(HERE, 'wlp3.py')), 1)
sys.argv = ['wlp3', 'tag=feas'] + PARGS
exec(src[:src.index('A_ub, b_ub = [], []')])
SEP.stdin.close(); SEP.wait()
SX = subprocess.Popen([os.path.join(HERE, 'bin', 'sep3x_new'), SF], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
                      env=dict(os.environ, SEP_NODELIMIT='0'))
yv = [0.0] * len(roots)
for k, v in SOL['y'].items():
    u, rest = k.split('|'); yv[ix[(int(u),) + tuple(int(c) for c in rest)]] = v
xs = [(int(k), v) for k, v in SOL['x'].items()]; t = SOL['t']; z9 = SOL['z9']
print('solution t = %.9f, %d nonzero y, %d nonzero x, z9 = %.4f; patterns loaded %d' % (t, sum(1 for v in yv if v > 0), len(xs), z9, len(PATS)), flush=True)
bad = 0
for d in range(7, DMAXP + 1):
    SX.stdin.write('q %d %.12f %d %d\n%s\nX %d %s\n' % (d, d - 6 + t + EPS, 20, 0, ' '.join('%.12f' % x for x in yv),
                   len(xs), ' '.join('%d %.12f' % kv for kv in xs))); SX.stdin.flush(); out = []
    while True:
        f = SX.stdout.readline().split()
        if f[0] == 'END': break
        out.append(f[1:4])
    for o in out: print('VIOLATED d=%d load %s > %.9f link %s s %s' % (d, o[0], d - 6 + t, o[1], o[2]))
    bad += len(out); print('d=%d: %d violated' % (d, len(out)), flush=True)
BIG = np.array([1.0 if states[a][2] >= 7 else 0.0 for a in range(NS)])
for d in range(DMAXP + 1, 31):
    M = np.full((NS, NS), -np.inf)
    for a, b, rr in TRI[9]: M[a, b] = max(M[a, b], (yv[ix[rr]] if rr is not None else 0.0) + z9 * BIG[a])
    P = M.copy()
    for k in range(2, d + 1): P = (P[:, :, None] + M[None, :, :]).max(axis=1)
    v = np.diag(P).max()
    if v > d - 6 + t + EPS: bad += 1; print('VIOLATED d=%d DP load %.9f > %.9f' % (d, v, d - 6 + t))
SX.stdin.close(); SX.wait()
print('FEASIBLE' if bad == 0 else 'INFEASIBLE: %d violated rows' % bad)
