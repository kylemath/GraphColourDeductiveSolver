"""[exploratory] NightPotential: per Gamma-cycle (gamma54.json) the number of forest pair-graphs (rank 0, over all six pairs and all states)
versus fixed-point visits (R3 k<=2 with rank_AB = 0), step-8 breaks and Rtot; per-position forest profile."""
import json
from collections import Counter, defaultdict
G = json.load(open('gamma54.json')); T = Counter(); rows = []; prof = defaultdict(Counter)
for x in G:
    R = x['rows']; n = len(R)
    forests = sum(sum(1 for v in r['rkabs'] if v == 0) for r in R)
    fx = sum(1 for i, r in enumerate(R) if i % 10 in (4, 6, 8) and r['AB'] == 0)
    brk = sum(1 for i in range(n) if i % 10 == 8 and R[i]['J'] and not R[(i + 1) % n]['J'])
    rt = sum(r['Rtot'] for r in R)
    rows.append((forests, fx, brk, rt))
    for i, r in enumerate(R):
        for nm in ('AB', 'muA', 'muB', 'alMu', 'alA', 'alB'): prof[nm][i % 10] += (r[nm] == 0)
print('per cycle (forest pair-graphs summed over states, fixed visits, breaks, sum Rtot):')
for t in sorted(Counter(rows).items()): print('  ', t)
print('forest count by role pair and position 0..9 (out of 108 periods):')
for nm in prof: print('  %-5s' % nm, [prof[nm][p] for p in range(10)])
import itertools
xs = [r[0] for r in rows]; ys = [r[1] for r in rows]
print('forests - 6*fixed visits distribution:', Counter(a - 6 * b for a, b, _, _ in rows))
print('sumRtot + forests:', Counter(r[3] + r[0] for r in rows))
