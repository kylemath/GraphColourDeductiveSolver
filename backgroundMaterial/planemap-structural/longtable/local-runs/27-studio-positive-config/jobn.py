#!/usr/bin/env python3
"""jobn.py: Job N summary from jobn-visits.jsonl. Row: [pos, k, lockless, yz_joined, pm_bridge, p, m, y, z, #m candidates, |K_{c(p),c(m)}(p)|, |K(y)|, |K(z)|, sigma fixed point]."""
import json
from collections import Counter
T = Counter(); fails = []; const_bad = []; changes = Counter()
for l in open('jobn-visits.jsonl'):
    r = json.loads(l)
    for ci, cyc in enumerate(r['jobn']):
        T['cycles'] += 1; ids = {k: set() for k in (3, 4)}; prev = {}
        for row in cyc:
            pos, k, ll, yz, br, p, m, y, z, nm, cp, cy, cz, fx = row
            T['visits_k%d' % k] += 1; T['a_eq_b'] += (yz == ll); T['bridge_eq_b'] += (br == ll); T['m_unique'] += (nm == 1)
            ids[k].add((p, m, y, z))
            if k in prev: changes[(k, 'compsize_changed' if prev[k] != cp else 'compsize_same')] += 1
            prev[k] = cp
            if not ll: fails.append((r['run'], r['name'], r['hole'], 'cycle', ci, 'pos', pos, 'k', k, 'yz', yz, 'bridge', br, '|K(p)|', cp, '|K(y)|', cy, '|K(z)|', cz))
        for k in (3, 4):
            if len(ids[k]) > 1: const_bad.append((r['run'], r['name'], r['hole'], ci, k, ids[k]))
        T['same_pmyz_k3_k4'] += len(ids[3] | ids[4]) == 1
nv = T['visits_k3'] + T['visits_k4']
print('Gamma-cycles at (5,5,5,5,6), orders 25-26, both orientations: %d; visits k=3: %d, k=4: %d' % (T['cycles'], T['visits_k3'], T['visits_k4']))
print('(a) y~z <=> lockless: %d/%d; pm bridge <=> lockless: %d/%d; m unique: %d/%d' % (T['a_eq_b'], nv, T['bridge_eq_b'], nv, T['m_unique'], nv))
print('(c) p, m, y, z constant along the cycle at each k: violations %d; same (p,m,y,z) at k=3 and k=4: %d/%d cycles' % (len(const_bad), T['same_pmyz_k3_k4'], T['cycles']))
print('(d) |K_{c(p),c(m)}(p)| vs the previous visit at the same k:', dict(changes))
print('failing visits (k, components):')
for f in fails: print('  ', f)
