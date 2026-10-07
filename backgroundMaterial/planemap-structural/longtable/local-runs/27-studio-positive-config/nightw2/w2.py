#!/usr/bin/env python3
"""w2.py (NightW2): co-occurrence of k<=2 exit failures on (5,5,5,5,6) Gamma-cycles, from jobm-gamma-sequences.jsonl.
Usage: python3 w2.py [DIR, default ../; ../jobr27/ for order 27]. Single core, < 1 s.
Labels at R3 states: 'L' lockless, 'X' fixed point of sigma (Lemma Fix: {A,B}-graph acyclic), other = single-lock exit."""
import json, sys
from collections import Counter
D = sys.argv[1] if len(sys.argv) > 1 else '../'
K1 = {1: 0, 2: 1, 4: 2, 8: 3, 16: 4}
cycles = []
for l in open(D + 'jobm-gamma-sequences.jsonl'):
    r = json.loads(l)
    if r['pattern'] != '5,5,5,5,6': continue
    for cyc in r['jobm']:
        s0 = next(i for i, x in enumerate(cyc) if x[0] == 3 and x[1] == 16)
        cyc = cyc[s0:] + cyc[:s0]
        cycles.append((r['run'], r['name'], r['hole'], [(t, K1[km], e) for t, km, e, f in cyc]))
def lab(x): return 'L' if x[2] == 'L' else ('X' if x[2] == 'X' else 'S')
pat = Counter(); pair = Counter(); nper = 0; allfail = []; cross = Counter(); single_ctx = Counter()
for run, name, hole, cyc in cycles:
    L = len(cyc); assert L % 10 == 0
    for b in range(0, L, 10):
        per = cyc[b:b + 10]; assert [(x[0], x[1]) for x in per[4:9:2]] == [(3, 2), (3, 1), (3, 0)]
        t = tuple(lab(per[i]) for i in (4, 6, 8)); pat[t] += 1; nper += 1
        if 'L' not in t: allfail.append((run, name, hole, b // 10, t))
        for (i, a), (j, c) in [((4, 'k2'), (6, 'k1')), ((6, 'k1'), (8, 'k0')), ((4, 'k2'), (8, 'k0'))]:
            if lab(per[i]) == 'X' and lab(per[j]) == 'X': pair[(a, c)] += 1
        for i in (4, 6, 8):
            if lab(per[i]) == 'S': single_ctx[t] += 1
        # across the period boundary: k0 of this period with k2 of the next period
        nx = cyc[(b + 10) % L: (b + 10) % L + 10]
        cross[(lab(per[8]), lab(nx[4]))] += 1
print('records (cycles):', len(cycles), ' periods:', nper)
print('(k2, k1, k0) label patterns per period (L lockless, X fixed point, S single-lock):')
for k, v in pat.most_common(): print('   ', v, ' '.join(k))
print('both fixed points in one period:', dict(pair), ' (k2,k0) pair count =', pair[('k2', 'k0')])
print('periods with no lockless k<=2 exit (W2 failures):', len(allfail), allfail)
print('patterns of periods containing a single-lock k<=2 exit:', dict(single_ctx))
print('(k0 of period, k2 of next period) label pairs:', dict(cross))
