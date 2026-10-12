#!/usr/bin/env python3
"""Track L [data]: switchable territories.  Circle with points 0..2r-1, B_odd = {(0,1),(2,3),..}, B_even = {(1,2),..,(2r-1,0)};
every point has a transverse: inside chord (non-crossing perfect matching of the inside points), outside chord or open end
(outside chords non-crossing and enclosing no open end).  tau_odd / tau_even = pairing of the open ends via B ∪ chords;
closed = internal closed curves.  Tests relations between tau_odd and tau_even.
usage: tl_territory.py RMAX"""
import sys
from collections import Counter
from tl_line import ncm


def outside_structs(pts):
    """non-crossing partial matchings of pts (cyclic order, as a list) whose unmatched points are not enclosed: yields
    (pairs, open)"""
    if not pts:
        yield [], []; return
    a = pts[0]
    # a open: then rest must have no chord enclosing... a open, and chords among rest must not enclose a -> in linear order
    # pts[1:], chords enclosing nothing open: treat recursively with a top-level sequence
    for pr, op in top(pts[1:]):
        yield pr, [a] + op
    for k in range(1, len(pts), 2):
        for m1 in ncm(pts[1:k]):
            for pr, op in top(pts[k + 1:]):
                yield [(a, pts[k])] + m1 + pr, op


def top(pts):
    """linear sequence: each point is open or starts a chord whose interior is a full non-crossing matching"""
    if not pts:
        yield [], []; return
    a = pts[0]
    for pr, op in top(pts[1:]):
        yield pr, [a] + op
    for k in range(1, len(pts), 2):
        for m1 in ncm(pts[1:k]):
            for pr, op in top(pts[k + 1:]):
                yield [(a, pts[k])] + m1 + pr, op


def pairing(n, B, chords, opens):
    mB = {}; mC = {}
    for x, y in B: mB[x] = y; mB[y] = x
    for x, y in chords: mC[x] = y; mC[y] = x
    res = {}; seen = set()
    for o in opens:
        if o in seen: continue
        x = o; seen.add(x)
        while True:
            y = mB[x]; seen.add(y)
            if y in mC: x = mC[y]; seen.add(x)
            else: break
        res[o] = y; res[y] = o
    closed = 0
    for s in range(n):
        if s in seen: continue
        closed += 1; x = s
        while True:
            seen.add(x); y = mB[x]; seen.add(y); x = mC[y]
            if x == s: break
    return res, closed


def meander_count(order, m1, m2):
    seen = set(); c = 0
    for s in order:
        if s in seen: continue
        c += 1; x = s
        while True:
            seen.add(x); y = m1[x]; seen.add(y); x = m2[y]
            if x == s: break
    return c


def main():
    for r in range(1, int(sys.argv[1]) + 1):
        n = 2 * r; st = Counter()
        Bo = [(2 * i, 2 * i + 1) for i in range(r)]; Be = [(2 * i + 1, (2 * i + 2) % n) for i in range(r)]
        for mask in range(1 << n):
            I = [x for x in range(n) if mask >> x & 1]; O = [x for x in range(n) if not mask >> x & 1]
            if len(I) % 2: continue
            for mi in ncm(I):
                for pr, op in outside_structs(O):
                    if not op or 0 not in op: continue   # reference open end at point 0
                    if len(op) % 2: continue
                    to, co = pairing(n, Bo, mi + pr, op); te, ce = pairing(n, Be, mi + pr, op)
                    if co or ce: st['closed'] += 1; continue
                    lam = meander_count(op, to, te)
                    st[('nopen', len(op), 'lam(to,te)', lam)] += 1
        print('r', r, dict(sorted(st.items(), key=str)), flush=True)


if __name__ == '__main__':
    main()
