#!/usr/bin/env python3
"""Track L [data]: the ladder picture in the F12 figure-eight model (tl_fig8.py).
Rungs = colour-3 chords in Ot joining Xt to Yt, ordered inner (near the x3 corner) -> outer (near x1).
Rung word: for each rung, 'h' if on H0, 'c' if on C'.  Tallied against the side of C' and the hypotheses.
usage: tl_ladder.py NMAX"""
import sys
from collections import Counter
from tl_fig8 import instances, analyse
for n in range(1, int(sys.argv[1]) + 1, 2):
    st = Counter(); ex = {}
    for p in range(0, n // 2 + 1):
        m = n - 2 * p
        if m < 1 or m % 2 == 0: continue
        for E, (pp, mm, side) in instances(p, m):
            r = analyse(E, pp, mm, side)
            if r is None or r['kH'] != 2 or r['k13'] != 1: continue
            rungs = []
            for k, (a, b, c, l) in enumerate(E):
                if c != 3 or l: continue
                w, y = (a, b) if a <= 2 * pp else (b, a)
                if 1 <= w <= 2 * pp and y > 2 * pp: rungs.append((w, y, k))
            rungs.sort(reverse=True)
            ys = [y for w, y, k in rungs]
            assert ys == sorted(ys, reverse=True)
            word = ''.join('h' if k in r['H0'] else 'c' for w, y, k in rungs)
            hyp = 'RIGIDu' if (r['kHX'] == 1 and r['kHY'] == 1) else 'kHX%d,kHY%d' % (r['kHX'], r['kHY'])
            key = (hyp, r['side'], word)
            st[key] += 1
    for k in sorted(st, key=str):
        if k[0] == 'RIGIDu' or st[k] >= 1 and len(k[2]) <= 5:
            pass
    print('n', n)
    for k in sorted(st, key=str):
        if k[0] == 'RIGIDu' or k[0] in ('kHX1,kHY2', 'kHX2,kHY1'):
            print('  ', k, st[k])
