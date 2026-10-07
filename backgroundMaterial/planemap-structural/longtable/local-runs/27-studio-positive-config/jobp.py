#!/usr/bin/env python3
"""jobp.py: Job P from jobp-steps.jsonl. Roles 0..4 = x_{j+i}, 5..9 = w_{j+i}, 10 = m (p's third outer neighbour; p = x_{j+k}).
P1: per k (0..4), the role edges whose bridge bit equals 'lockless' at every R3@k state (and those equal to 'not lockless'); credit at k <= 2 vs 7L/20.
P2: geometry of the step-8 (R3k0 -> R1k2) and step-0 (R3k4 -> R1k1) swaps in periods where y ~ z breaks / is restored."""
import json
from collections import defaultdict, Counter
RN = ['x0', 'x1', 'x2', 'x3', 'x4', 'w0', 'w1', 'w2', 'w3', 'w4', 'm']
K1 = {1: 0, 2: 1, 4: 2, 8: 3, 16: 4}
match = defaultdict(lambda: defaultdict(Counter)); nvis = Counter(); exits = Counter(); credit = []
P2 = []
for l in open('jobp-steps.jsonl'):
    r = json.loads(l)
    for cyc in r['jobp']['cycles']:
        s0 = next(i for i, x in enumerate(cyc) if x['type'] == 3 and x['kmask'] == 16); cyc = cyc[s0:] + cyc[:s0]; L = len(cyc)
        c012 = 0
        for x in cyc:
            if x['type'] != 3: continue
            k = K1[x['kmask']]; ll = x['exit'] == 'L'; nvis[k] += 1; exits[(k, x['exit'])] += 1
            for e, bit in x['edges'].items(): match[k][e][(bit == 1) == ll] += 1
            if k <= 2 and ll: c012 += 3 * x['f'] - 1
        credit.append((c012 / (7 * L / 20), c012, L, r['run'], r['name'], r['hole']))
        for b in range(0, L, 10):
            per = cyc[b:b + 10]; yz = [x['K'][2] for x in per]
            if 0 in yz:
                for st in (8, 0, 1, 3):
                    x = per[st]; nxt = per[(st + 1) % 10]['K'][2] if st < 9 else cyc[(b + 10) % L]['K'][2]
                    P2.append((r['run'], r['name'], r['hole'], 'period', b // 10, 'step', st, 'y~z before', x['K'][2], 'after', nxt, '|K|', x['K'][0], 'dist(K,v)', x['K'][1],
                               '|K & K_yz|', x['K'][3], 'K cuts y,z in K_yz', x['K'][4], 'K on shortest y-z path', x['K'][5], 'K separates y,z in T-K', x['K'][6]))
print('P1: R3 visits per k:', dict(nvis)); print('    exits per k:', sorted(exits.items()))
for k in range(5):
    exact = [RN[int(e.split('-')[0])] + RN[int(e.split('-')[1])] for e, c in match[k].items() if c[False] == 0 and c[True] == nvis[k]]
    anti = [RN[int(e.split('-')[0])] + RN[int(e.split('-')[1])] for e, c in match[k].items() if c[True] == 0 and c[False] == nvis[k]]
    best = sorted(((c[False], e) for e, c in match[k].items()))[:3]
    print('  k=%d: edges with bridge <=> lockless (0 exceptions): %s; bridge <=> NOT lockless: %s; best (exceptions, edge): %s'
          % (k, exact, anti, [(n, RN[int(e.split('-')[0])] + RN[int(e.split('-')[1])]) for n, e in best]))
credit.sort(); print('P1: k<=2 credit / (7L/20): min %.3f at %s; below 1 in %d of %d cycles' % (credit[0][0], credit[0][3:], sum(1 for c in credit if c[0] < 1), len(credit)))
print('P2 (failing periods; steps 8 = R3k0->R1k2 (p,y), 0 = R3k4->R1k1 (m,z), 1 = R1k1->R3k3 (m,y), 3 = R1k0->R3k2 (p,z)):')
for x in P2: print('  ', x)
