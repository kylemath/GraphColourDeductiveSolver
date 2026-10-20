# exec the s33z engine (pcheck.py minus its command dispatch) into the caller's globals: ENGARGS = list of pcheck args
import os
_E = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s33z/eng'
def engine(args, g):
    import sys
    sys.argv = [os.path.join(_E, 'pcheck.py'), 'none'] + args
    src = open(os.path.join(_E, 'pcheck.py')).read(); last = src.rstrip().rsplit('\n', 1)
    assert "cmd_rowR2" in last[1]
    g['__file__'] = os.path.join(_E, 'pcheck.py')
    exec(compile(last[0], os.path.join(_E, 'pcheck.py'), 'exec'), g)
