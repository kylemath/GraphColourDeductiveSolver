"""Job 30 B: is a wlp3xt (Rule T) solution feasible for the full LP over a registry? (feascheck.py for Rule T)
- Exhaustive separation with bin/sep3xt (SEP_NODELIMIT=0) at d = 7..DMAXP, threshold d - 6 + t + EPS, with the
  solution's Y, T (inflow by the per-transition maximum, as in wlp3xt) and transfers x.
- d = DMAXP+1..30 by wlp3xt's letter-9 DP (max over flags plus inflow, and z9 per big position).
- Sender rows: every Rule T sender row of wlp3xt, evaluated directly.
Usage: python3 feascheckt.py SOLUTION.json [eps=1e-7] <wlp3xt args (registry, notx/tmerge/tzero as in the run)>
Prints violated rows and 'FEASIBLE' when there are none."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
SOLF = sys.argv[1]; SOL = json.load(open(SOLF))
EPS = float(next((a[4:] for a in sys.argv[2:] if a.startswith('eps=')), '1e-7'))
os.environ['SEP_NODELIMIT'] = '0'
src = open(os.path.join(HERE, 'wlp3xt.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(HERE, 'wlp3xt.py')), 1)
sys.argv = ['wlp3xt', 'tag=feast', 'maxit=0'] + [a for a in sys.argv[2:] if not a.startswith('eps=')]
exec(src[:src.index('def solve():')])
yv = np.zeros(NY)
for k, v in SOL['yT'].items():
    r, f = k.split('|'); yv[YI[(tuple(int(c) for c in r), int(f[0]), int(f[1]))]] = v
for k, v in SOL['tau'].items():
    r, f = k.split('|'); TV[TI[(tuple(int(c) for c in r), int(f[0]), int(f[1]), f[2])]] = v
xv = {int(k): v for k, v in SOL['x'].items()}; t = SOL['t']; z9 = SOL['z9']
print('solution t = %.9f, %d Y > 0, %d T > 0, %d x > 0, z9 = %.4f' % (t, int((yv > 0).sum()), int((TV > 0).sum()), len(xv), z9), flush=True)
bad = 0
val = lambda k: yv[k[1]] if k[0] == 'y' else TV[k[1]] if k[0] == 'tau' else xv.get(k[1], 0.0) if k[0] == 'x' else z9 if k[0] == 'z9' else t
for k_, r in enumerate(rows):   # sender rows (and z9 rows) as built by wlp3xt: sum <= rhs
    if rinfo[k_][0] in ('sender', 'z9') and sum(c * val(key) for key, c in r.items()) > rhs[k_] + EPS:
        bad += 1; print('VIOLATED', rinfo[k_])
for d in range(7, DMAXP + 1):
    out = sepx(d, yv, {} if NOTX else xv, d - 6 + t + EPS, 20)
    for o in out: print('VIOLATED d=%d load %.9f > %.9f link %s s %s' % (d, o[0], d - 6 + t, o[1], o[2]))
    bad += len(out); print('d=%d: %d violated' % (d, len(out)), flush=True)
for d in range(DMAXP + 1, 31):
    for wgt, path, nbig in dp9(d, yv, 0.0 if NOTX else z9, d - 6 + t + EPS, 5):
        bad += 1; print('VIOLATED d=%d DP load %.9f > %.9f' % (d, wgt, d - 6 + t))
SEPX.stdin.close(); SEPX.wait()
print('FEASIBLE' if bad == 0 else 'INFEASIBLE: %d violated rows' % bad)
