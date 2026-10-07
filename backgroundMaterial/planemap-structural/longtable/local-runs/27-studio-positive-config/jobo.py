#!/usr/bin/env python3
"""jobo.py: Job O from jobo-steps.jsonl. Rows (pi order): [pos, type, kmask, pairmask, compmask, |comp|, yz_before, yz_after, |K(y)|, |K(z)|];
bits of pairmask/compmask: 1 = p, 2 = m, 4 = y, 8 = z. Each cycle is rotated to start at R3@k=4 (kmask 16) and cut into periods of 10 steps."""
import json
from collections import Counter
nb = Counter(); persist = 0; persist_cont = 0; pairs_k4 = 0; patterns = Counter(); comppat = Counter(); events = []; per_step_break = Counter(); per_step_restore = Counter()
NAME = {1: 'p', 2: 'm', 4: 'y', 8: 'z'}
def names(mask): return ''.join(NAME[b] for b in (1, 2, 4, 8) if mask & b) or '-'
for l in open('jobo-steps.jsonl'):
    r = json.loads(l)
    for cyc in r['jobo']['cycles']:
        s0 = next(i for i, x in enumerate(cyc) if x[1] == 3 and x[2] == 16); cyc = cyc[s0:] + cyc[:s0]; L = len(cyc)
        for b in range(0, L, 10):
            per = cyc[b:b + 10]; nb[sum(1 for x in per if not x[7])] += 1
            patterns[tuple(names(x[3]) for x in per)] += 1; comppat[tuple(names(x[4]) for x in per)] += 1
        k4 = [i for i in range(0, L, 10)]
        for a, i in enumerate(k4):
            i2 = k4[(a + 1) % len(k4)]; pairs_k4 += 1
            if not cyc[i][6] and not cyc[i2][6]:
                persist += 1
                if all(not cyc[(i + t) % L][6] for t in range(10)): persist_cont += 1
            if not cyc[i][6]:   # failing k=4 visit: last break before, first restore after (step indices relative to the period start = this visit)
                br = next(t for t in range(1, L + 1) if cyc[(i - t) % L][6] and not cyc[(i - t) % L][7]); rs = next(t for t in range(0, L) if cyc[(i + t) % L][7])
                per_step_break[10 - br] += 1; per_step_restore[rs] += 1
                events.append((r['run'], r['name'], r['hole'], 'broken at step', -br, '(rel. to the k=4 visit; pair', names(cyc[(i - br) % L][3]), 'comp', names(cyc[(i - br) % L][4]), 'size', cyc[(i - br) % L][5], ')',
                               'restored at step', rs, '(pair', names(cyc[(i + rs) % L][3]), 'comp', names(cyc[(i + rs) % L][4]), 'size', cyc[(i + rs) % L][5], ')', 'y~z off for', br + rs, 'steps'))
print('(i) periods by number of steps (of 10) after which y and z are NOT joined:', sorted(nb.items()))
print('(ii) consecutive k=4 visit pairs: %d; both failing: %d; failing throughout the period between: %d' % (pairs_k4, persist, persist_cont))
print('(iii) swap-pair pattern over the 10 steps (which of p,m,y,z carry a colour of the swapped pair), counts:')
for k, v in patterns.most_common(): print('    ', v, k)
print('     swapped-component contents pattern (which of p,m,y,z lie in the swapped component), most common:')
for k, v in comppat.most_common(8): print('    ', v, k)
print('failing k=4 visits: break / restore events (steps relative to the visit):')
for e in events: print('  ', e)
print('break step (position in the preceding period, 0..9):', dict(per_step_break), '; restore step after the visit:', dict(per_step_restore))
