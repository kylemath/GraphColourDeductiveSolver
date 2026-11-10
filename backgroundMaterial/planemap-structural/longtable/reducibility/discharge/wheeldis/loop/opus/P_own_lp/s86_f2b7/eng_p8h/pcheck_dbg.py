# s86 debug driver: pcheck.py with one extra exec'd file ($ROWDBG) after pinout.py (used to override f2b_selftest for row-by-row dumps)
import os
_P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pcheck.py'); _src = open(_P).read()
_a = "exec(open(os.path.join(HERE, 'pinout.py')).read())"
assert _a in _src
_src = _src.replace(_a, _a + "; exec(open(os.environ['ROWDBG']).read())", 1)
__file__ = _P
exec(compile(_src, _P, 'exec'))
