#!/usr/bin/env python3
"""w2rank.py (NightW2): global {A,B} cycle ranks (Job AG, jobuv/jobag.json) at the k<=2 R3 states of each period, (5,5,5,5,6) only.
Period positions 4, 6, 8 = R3k2, R3k1, R3k0 (period starts at R3k4). Single core, < 1 s."""
import json
from collections import Counter
d = json.load(open('../jobuv/jobag.json'))
tri = Counter(); s48 = Counter(); n = 0; ex = Counter(); cross = Counter()
for r in d:
    if r['deg'] != 6: continue
    rows = r['rows']; L = len(rows)
    s0 = next(i for i, x in enumerate(rows) if x and x['k'] == 4); rows = rows[s0:] + rows[:s0]
    for b in range(0, L, 10):
        per = rows[b:b + 10]; ks = [per[i]['k'] for i in (4, 6, 8)]; assert ks == [2, 1, 0], ks
        t = tuple(per[i]['r_all'] for i in (4, 6, 8)); tri[t] += 1; n += 1
        s48[(min(t[0], 3), min(t[2], 3))] += 1
        ex[tuple(per[i]['ex'][0] for i in (4, 6, 8))] += 1
        nx = rows[(b + 10) % L:(b + 10) % L + 10]; cross[(min(per[8]['r_all'], 3), min(nx[4]['r_all'], 3))] += 1
print('deg-6 periods:', n)
print('(rank k2, rank k1, rank k0) histogram:'); [print('   ', v, k) for k, v in sorted(tri.items())]
print('(rank k2, rank k0) capped at 3:', sorted(s48.items()))
print('min rank k2 + rank k0:', min(a + c for a, b, c in tri), ' min of sum of three:', min(sum(t) for t in tri))
print('(k0 rank, next-period k2 rank) capped at 3:', sorted(cross.items()))
print('exit kinds (k2,k1,k0):', dict(ex))
