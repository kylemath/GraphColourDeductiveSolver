#!/usr/bin/env python3
"""Track N [hand-checkable enumeration]: which pi-steps c -> pi(c) between DL states with N <= 9 are consistent with the
Euler-level data only, in ANY graph satisfying Lemma E's sphere constants at both states.
Unknowns per state (role order am, AB, aA, mB, aB, mA): component counts c_r >= link minimum (1,1,2,1,2,1) (Lemma J1),
cycle ranks b_r >= 0, chi_r = c_r - b_r.  Constraints:
  Lemma E: chi1+chi2 = 2, chi3+chi4 = 3, chi5+chi6 = 3 at both states;
  J2 (transport of P2 of c to P3 of pi c, as graphs): c'5 = c3, c'6 = c4, b'5 = b3, b'6 = b4;
  St (star identity, at colours mu and B): chi'2 + chi'3 = chi1 + chi6, chi'1 + chi'4 = chi2 + chi5;
  N = sum c <= 9 at both.  Prints every admissible (N, N') pair with an example."""
import itertools
BASE = (1, 1, 2, 1, 2, 1)
def states():
    for extra in [None] + list(range(6)):
        c = list(BASE)
        if extra is not None: c[extra] += 1
        for b in itertools.product(range(3), repeat=6):
            chi = [c[i] - b[i] for i in range(6)]
            if chi[0] + chi[1] == 2 and chi[2] + chi[3] == 3 and chi[4] + chi[5] == 3:
                yield tuple(c), b, tuple(chi)
S = list(states())
found = {}
for (c, b, a) in S:
    for (c2, b2, a2) in S:
        if c2[4] != c[2] or c2[5] != c[3] or b2[4] != b[2] or b2[5] != b[3]: continue
        if a2[1] + a2[2] != a[0] + a[5] or a2[0] + a2[3] != a[1] + a[4]: continue
        key = (sum(c), sum(c2)); found.setdefault(key, []).append((c, b, c2, b2))
for k in sorted(found): print('N -> N\' =', k, 'count', len(found[k]), 'e.g. c,b,c\',b\' =', found[k][0])
for k in [(8, 8), (9, 9)]:
    if k not in found: print(k, 'IMPOSSIBLE at Euler level')
