#!/usr/bin/env python3
"""Track L [data]: line model with two outer matchings (Sigma_O from H, Sigma'_O from H^Yt), arbitrary pairs.
Table needed at in-shape c: lam(B2,S)=2, lam(B1,S)=1, lam(B2,S')=1, lam(B1,S')=2.  Is the side of C' forced?
usage: tl_line2.py PMAX"""
import sys
from collections import Counter
from tl_line import ncm, curves
for p in range(0, int(sys.argv[1]) + 1):
    n = 2 * p + 2; a, b = 0, n - 1
    B1 = [(2 * i, 2 * i + 1) for i in range(p + 1)]
    B2 = [(2 * i - 1, 2 * i) for i in range(1, p + 1)] + [(b, a)]
    st = Counter()
    for mask in range(1 << (2 * p)):
        I = [0] + [k for k in range(1, n - 1) if mask >> (k - 1) & 1]
        O = [k for k in range(1, n - 1) if not mask >> (k - 1) & 1] + [b]
        if len(I) % 2 or len(O) % 2: continue
        Os = list(ncm(O))
        for sI in ncm(I):
            for sO in Os:
                c2 = curves(n, B2, sI + sO)
                if len(c2) != 2 or len(curves(n, B1, sI + sO)) != 1: continue
                H0 = [c for c in c2 if a in c][0]; Cp = [c for c in c2 if a not in c][0]
                seg = next(i for i in range(1, p + 1) if (2 * i - 1) in Cp)
                cross = sum(1 for w in range(1, 2 * seg) if w in I and w in H0)
                side = 'AB' if cross % 2 == 0 else 'sigma'
                ok = 0
                for sO2 in Os:
                    if len(curves(n, B2, sI + sO2)) == 1 and len(curves(n, B1, sI + sO2)) == 2: ok += 1
                st[(side, 'has_partner' if ok else 'no_partner')] += 1
    print('p', p, dict(sorted(st.items())), flush=True)
