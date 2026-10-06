#!/usr/bin/env python3
"""studiointel search4.py -- [exploratory] (explore mode, 15:05). search3.py (fast engine, child CPU counted) with the score aimed at radius 6:
(#holes rho>=6, #rho>=5, #rho>=4, #rho>=3, mean DL fraction). Certificates as before (any hole rho>=5 or targetless)."""
import sys, os
sys.argv[0] = 'search3.py'
import search3, search2
def score(ev):
    rs = [(10 ** 9 if r is None else r) for r in ev['rho'].values()]
    return (sum(r >= 6 for r in rs), sum(r >= 5 for r in rs), sum(r >= 4 for r in rs), sum(r >= 3 for r in rs), ev['mean_DL_frac'])
search2.score = score
if __name__ == '__main__':
    src = open(search2.__file__).read()
    main = src[src.index("if __name__ == '__main__':"):].replace("if __name__ == '__main__':", "if True:", 1)
    g = dict(vars(search2)); g['__name__'] = 'search4_main'; exec(compile(main, search2.__file__ + ':main', 'exec'), g)
