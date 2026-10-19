# usage: twin2.py CERT FORBIDFILE [engine flags]: for each receiver binder of CERT, the nearest forbidden row (fewest differing coefficients)
import sys, os, json
cert, forb = sys.argv[1], sys.argv[2]
sys.argv = ['pcheck.py', 'none'] + sys.argv[3:]
__file__ = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s27o/pcheck.py'
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()): exec(open(__file__).read())
F = []
for line in open(forb):
    f = line.split('#')[0].split()
    if f: F.append((int(f[0]), f[1], f[2]))
FC = [(x, recv_coef_R2(*x, True)) for x in F]
for c in sorted(json.load(open(cert)), key=lambda c: c['w']):
    r = c['row']
    if r[0] != 'receiverR2': continue
    a = (int(r[1]), r[2], r[3]); ca = recv_coef_R2(*a, True); best = None
    for x, cx in FC:
        if x[0] != a[0]: continue
        nd = sum(1 for k in set(ca) | set(cx) if ca.get(k, 0) != cx.get(k, 0))
        if best is None or nd < best[0]: best = (nd, x)
    print('%.6f %d %s/%s  nearest forbidden: %s' % (-c['w'], *a, 'none at this d' if best is None else '%s/%s (%d coeffs differ%s)' % (best[1][1], best[1][2], best[0], ', IDENTICAL ROW' if best[0] == 0 else '')))
