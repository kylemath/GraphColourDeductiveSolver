#!/usr/bin/env python3
"""Track L [data]: the abstract line model of the sigma-type lemma.

Points a = 0, w1..w_{2p}, b = 2p+1 on a line (the circle Xt cut at v, between b and a).  Upper half plane = inside Xt,
lower = outside.  B1 = {(0,1),(2,3),...,(2p,2p+1)}, B2 = {(1,2),(3,4),...,(2p-1,2p)} + the arc (b,a) through infinity.
Labels: a is I (its end e4 goes inside Xt), b is O (its end e2 goes outside).  Sigma_I, Sigma_O = non-crossing perfect
matchings of the I-points (upper) and O-points (lower).
H = B2 u Sigma (H0 = the curve through infinity), lam1 = #curves of B1 u Sigma.
Side of a free curve C' of H relative to H0: e0-side contains the open segment (a, w1); e3-side contains (w_2p, b).
Test: (lam2 = 2, lam1 = 1) => C' on the e3 side?   Also tabulates all (lam2, lam1, side).
usage: tl_line.py PMAX"""
import sys
from collections import Counter


def ncm(points):
    if not points:
        yield []; return
    a = points[0]
    for k in range(1, len(points), 2):
        for m1 in ncm(points[1:k]):
            for m2 in ncm(points[k + 1:]):
                yield [(a, points[k])] + m1 + m2


def curves(n, pairsA, pairsB):
    """curves of the union of two perfect matchings on n points: list of point sets"""
    mA = {}; mB = {}
    for x, y in pairsA: mA[x] = y; mA[y] = x
    for x, y in pairsB: mB[x] = y; mB[y] = x
    seen = set(); out = []
    for s in range(n):
        if s in seen: continue
        cur = set(); x = s
        while True:
            cur.add(x); y = mA[x]; cur.add(y); x = mB[y]
            if x == s: break
        seen |= cur; out.append(cur)
    return out


def main():
    PMAX = int(sys.argv[1])
    for p in range(0, PMAX + 1):
        n = 2 * p + 2; a, b = 0, n - 1
        B1 = [(2 * i, 2 * i + 1) for i in range(p + 1)]
        B2 = [(2 * i - 1, 2 * i) for i in range(1, p + 1)] + [(b, a)]
        st = Counter()
        for mask in range(1 << (2 * p)):
            I = [0] + [k for k in range(1, n - 1) if mask >> (k - 1) & 1]
            O = [k for k in range(1, n - 1) if not mask >> (k - 1) & 1] + [b]
            if len(I) % 2 or len(O) % 2: continue
            for sI in ncm(I):
                for sO in ncm(O):
                    S = sI + sO
                    c2 = curves(n, B2, S); c1 = curves(n, B1, S)
                    lam2, lam1 = len(c2), len(c1)
                    if lam2 != 2:
                        st[('lam2', lam2, 'lam1', lam1)] += 1; continue
                    H0 = [c for c in c2 if a in c][0]; Cp = [c for c in c2 if a not in c][0]
                    # a point of C' on a B2 segment (2i-1, 2i), both in C'
                    seg = next(i for i in range(1, p + 1) if (2 * i - 1) in Cp)
                    q = 2 * i - 1 if False else 2 * seg - 1
                    # walk at height +eps from just right of q-... we start above the open segment (2seg-1, 2seg), go left to (a, w1)
                    Iset = set(I)
                    cross = sum(1 for w in range(1, 2 * seg) if w in Iset and w in H0)
                    side = 'e0side(AB)' if cross % 2 == 0 else 'e3side(sigma)'
                    st[('lam2', 2, 'lam1', lam1, side)] += 1
        print('p', p, 'points', n, dict(sorted(st.items(), key=str)), flush=True)


if __name__ == '__main__':
    main()
