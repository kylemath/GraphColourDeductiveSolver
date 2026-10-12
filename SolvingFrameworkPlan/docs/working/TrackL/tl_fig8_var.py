#!/usr/bin/env python3
"""Track L [data]: which hypotheses the sigma-type lemma needs, in the F12 figure-eight model (tl_fig8.py).
At DL states with k(H) = 2: side of C' tallied against (k(F13), k(H^Xt), k(H^Yt)).  usage: tl_fig8_var.py NMAX"""
import sys
from collections import Counter
from tl_fig8 import instances, analyse
for n in range(1, int(sys.argv[1]) + 1, 2):
    st = Counter()
    for p in range(0, n // 2 + 1):
        m = n - 2 * p
        if m < 1 or m % 2 == 0: continue
        for E, (pp, mm, side) in instances(p, m):
            r = analyse(E, pp, mm, side)
            if r is None or r['kH'] != 2: continue
            st[(r['k13'], r['kHX'], r['kHY'], r['side'])] += 1
    print('n', n, '(k13,kHX,kHY,side):', dict(sorted(st.items(), key=str)), flush=True)
