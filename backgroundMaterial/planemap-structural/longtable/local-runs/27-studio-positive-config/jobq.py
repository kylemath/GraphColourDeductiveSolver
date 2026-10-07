#!/usr/bin/env python3
"""jobq.py: Job Q from jobq-steps.jsonl ((5,5,5,5,6) Gamma-cycles). Row: [pos, type, kmask, sigma fixed point, sigma lockless, |K step|, |K & K_sigma(x)|,
|K & K_sigma(pi x)|, |K_sigma(x)|, |other {alpha,mu} vertices|, K meets them]. Periods start at R3k4."""
import json
from collections import Counter
K1 = {1: 0, 2: 1, 4: 2, 8: 3, 16: 4}
fixpat = Counter(); llpat = Counter(); flips = Counter(); nfix = Counter(); r3fix = Counter()
for l in open('jobq-steps.jsonl'):
    r = json.loads(l)
    for cyc in r['jobq']:
        s0 = next(i for i, x in enumerate(cyc) if x[1] == 3 and x[2] == 16); cyc = cyc[s0:] + cyc[:s0]; L = len(cyc)
        for b in range(0, L, 10):
            per = cyc[b:b + 10]; fixpat[''.join(str(x[3]) for x in per)] += 1; llpat[''.join(str(x[4]) for x in per)] += 1
            for i, x in enumerate(per):
                if x[1] == 3: r3fix[(K1[x[2]], 'fixed' if x[3] else ('lockless' if x[4] else 'other'))] += 1
        for i in range(L):
            a, b2 = cyc[i], cyc[(i + 1) % L]
            if a[3] != b2[3]:   # the step a -> pi a flips "sigma would be a fixed point"
                flips[('step %d' % (i % 10), 'to fixed' if b2[3] else 'to non-fixed', 'K meets K_sigma(x)' if a[6] else 'K misses K_sigma(x)', 'K meets K_sigma(pi x)' if a[7] else 'K misses K_sigma(pi x)', 'K meets other {a,mu}' if a[10] else 'K misses other {a,mu}')] += 1
print('periods: %d' % sum(fixpat.values()))
print('R3 visits by k and exit (fixed point / lockless / other):', sorted(r3fix.items()))
print('per-period "sigma fixed point" pattern (positions R3k4 R1k1 R3k3 R1k0 R3k2 R1k4 R3k1 R1k3 R3k0 R1k2):'); [print('   ', v, k) for k, v in fixpat.most_common()]
print('per-period "sigma lockless" pattern:'); [print('   ', v, k) for k, v in llpat.most_common(12)]
print('steps that flip the fixed-point predicate (step i = state i -> state i+1 of the period):'); [print('   ', v, k) for k, v in sorted(flips.items())]
