import sys, os
sys.argv = ['pcheck.py', 'none'] + sys.argv[1:]
HERE0 = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s27o'
__file__ = os.path.join(HERE0, 'pcheck.py')
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(__file__).read())
pairs = [((7, '7665566', '6675676'), (7, '7765566', '6575676')), ((10, '6565665656', '6555555565'), (10, '6565665656', '6555565555')), ((10, '6565555665', '6665956566'), (10, '6565656565', '6556666666'))]
for a, b in pairs:
    ca = recv_coef_R2(*a, True); cb = recv_coef_R2(*b, True)
    diff = {k: (ca.get(k, 0), cb.get(k, 0)) for k in set(ca) | set(cb) if ca.get(k, 0) != cb.get(k, 0)}
    print(a, b, 'identical row' if not diff else 'differs in %d coefficients' % len(diff))
    for k, v in sorted(diff.items(), key=str): print('    ', k, v)
