# driver: per-cell z part of given receiver rows (s61 engine, planted sol); argv: engine_dir sol vfile pcheck-args...
import sys, json
eng, sol, vf = sys.argv[1:4]
sys.argv = [eng + '/pcheck.py', 'none'] + sys.argv[4:]
g = {'__file__': eng + '/pcheck.py', '__name__': 'drv'}
exec(open(eng + '/pcheck.py').read(), g)
S = json.load(open(sol)); g['ZV'].update({tuple(k): v for k, v in S['z']})
for ln in open(vf).read().split('\n')[:5]:
    if not ln: continue
    d, load, ex, lk, sv = ln.split(); d = int(d)
    w = [int(c) for c in lk]; s = [int(c) for c in sv]
    out = []
    for cl, tau in g['fy2_cells'](d, w, s):
        cf = g['recv_coef_R2'](d, lk, sv, True, tau)
        out.append('%s: z-part %.3f' % (cl, sum(v * g['ZV'].get(k[1], 0.0) for k, v in cf.items() if k[0] == 'z')))
    print(lk, sv, 'excess %s' % ex, ' | '.join(out))
