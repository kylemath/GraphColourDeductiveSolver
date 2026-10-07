#!/usr/bin/env python3
"""jobg.py LABEL=FILE ...: Job G summary. kmask bit i = x_{j+i} has degree >= 6 (k = 3 <-> kmask 8, k = 4 <-> kmask 16; kmask 0 = (5,5,5,5,5))."""
import sys, json, re
from collections import Counter, defaultdict
for a in sys.argv[1:]:
    lab, f = a.split('='); T = Counter(); S2 = Counter(); S4 = Counter(); S5 = Counter(); Gfail = []; slack = []; per_pat = Counter(); exits = Counter()
    for l in open(f):
        r = json.loads(l)
        if r['kind'] != 'hole' or 'jobg' not in r: continue
        T['gamma_holes'] += 1; T['shared_targets'] += r['jobg_shared_targets']; T['holes_with_shared'] += r['jobg_shared_targets'] > 0
        for g in r['jobg']:
            T['gamma'] += 1; per_pat[r['pattern']] += 1; T['s1_checked'] += g['s1_checked']; T['s1_bad'] += g['s1_bad']
            T['a'] += g['a']; T['b'] += g['b']; T['d'] += g['d']
            slack.append((g['G_credit'] - g['L'], r['name'], r['hole'], r['pattern'], g['L'], g['a'], g['b'], g['d']))
            if not g['G_ok']: Gfail.append((r['name'], r['hole'], r['pattern'], 'L', g['L'], 'credit', g['G_credit'], 'a,b,d', g['a'], g['b'], g['d'], g['exits']))
            for k, v in g['exits'].items():
                exits[k.split('_')[0]] += v
                if k.startswith('DL_'): S2[re.sub(r'_same\d', '', k)] += v
                if k.startswith('onelock_'): S4[re.sub(r'_wT-?\d+', '', k)] += v
                if k.startswith('lockless_') and r['pattern'] == '5,5,5,5,5': S5[re.search(r'_f(\d+)', k).group(1)] += v
    print('=== %s: Gamma-cycles %d at %d holes, by pattern %s' % (lab, T['gamma'], T['gamma_holes'], dict(per_pat)))
    print('  exits a (lockless) %d, b (single-lock) %d, d (DL) %d' % (T['a'], T['b'], T['d']))
    print('  S1 k=3/k=4 criteria checked at %d R3 states, violations %d' % (T['s1_checked'], T['s1_bad']))
    print('  S2 DL exits (kmask, fixed point?, image type):', dict(S2))
    print('  S3 Conjecture G: failures %d of %d; min slack %s; shared target cycles between Gamma-cycles: %d (at %d holes)' % (len(Gfail), T['gamma'], sorted(slack)[:3], T['shared_targets'], T['holes_with_shared']))
    for x in Gfail[:3]: print('    G FAIL', x)
    print('  S4 single-lock exits (kmask, locks, u, f):', sorted(S4.items()))
    print('  S5 (5,5,5,5,5) lockless-exit f histogram:', dict(S5))
