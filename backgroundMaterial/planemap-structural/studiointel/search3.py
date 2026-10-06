#!/usr/bin/env python3
"""studiointel search3.py -- PRODUCER for Phase D (declared in messages/2026-10-06/..._studiointel_..._declaration-phase-D-fast-engine.md).
Identical to search2.py (tabu search in the core class; stage X exact analysis) except:
  (1) the radius engine is the C++ engine fast/kempe.cpp via fast/fast.py (reproduces radius.py exactly: fast/regress_fast.py);
  (2) CPU time = own + children (os.times), so the cap counts the C++ engine;
  (3) score = (#degree-5 holes with rho >= 5, #with rho >= 4, #with rho >= 3, mean DL fraction); rho None counts as infinite.
Certificates as in search2.py (any hole with rho >= 5 or None)."""
import sys, os, time
# CPU accounting must include the C++ child processes: replace time.process_time globally (search.py and search2.py call it at run time)
_own = time.process_time
def _cpu():
    t = os.times(); return _own() + t.children_user + t.children_system
time.process_time = _cpu
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fast'))
import radius, fast
radius.analyse = fast.analyse                       # search.evaluate calls radius.analyse(faces, h, cap)
import search2
def score(ev):
    rs = [(10 ** 9 if r is None else r) for r in ev['rho'].values()]
    return (sum(r >= 5 for r in rs), sum(r >= 4 for r in rs), sum(r >= 3 for r in rs), ev['mean_DL_frac'])
search2.score = score
if __name__ == '__main__':
    src = open(search2.__file__).read()
    main = src[src.index("if __name__ == '__main__':"):].replace("if __name__ == '__main__':", "if True:", 1)
    g = dict(vars(search2)); g['__name__'] = 'search3_main'; exec(compile(main, search2.__file__ + ':main', 'exec'), g)
