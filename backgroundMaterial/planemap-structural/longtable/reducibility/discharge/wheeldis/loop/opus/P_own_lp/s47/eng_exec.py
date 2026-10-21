# exec the s47 engine (pcheck.py minus its command dispatch) into the caller's globals: ENGARGS = list of pcheck args
import os
_E = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eng')
def engine(args, g):
    import sys
    sys.argv = [os.path.join(_E, 'pcheck.py'), 'none'] + args
    src = open(os.path.join(_E, 'pcheck.py')).read(); last = src.rstrip().rsplit('\n', 1)
    assert "'rowR2': cmd_rowR2" in last[1]
    g['__file__'] = os.path.join(_E, 'pcheck.py')
    exec(compile(last[0], os.path.join(_E, 'pcheck.py'), 'exec'), g)
