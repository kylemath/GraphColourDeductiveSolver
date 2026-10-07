#!/usr/bin/env python3
"""jobi.py LABEL=FILE ...: Job I at (5,5,5,5,6) / (5,5,5,6,6) holes: per lockless sigma-exit (u, f) of the target excursion, min f, distinct targets,
lockless exits per Gamma-cycle versus L/10 and L/5; positive non-Gamma cycles; nonpositivity of every non-Gamma cycle."""
import sys, json, re
from collections import Counter, defaultdict
for a in sys.argv[1:]:
    lab, f = a.split('=')
    R = defaultdict(Counter); UF = defaultdict(Counter); ratio = defaultdict(Counter); posnon = []; holes = Counter(); maxw_nonG = Counter()
    for l in open(f):
        r = json.loads(l)
        if r['kind'] != 'hole': continue
        p = r['pattern']; holes[p] += 1
        # every cycle with w > 0 appears in jobg (gamma or not); non-Gamma positive cycles are exactly those with gamma false
        for g in r.get('jobg', []):
            kind = 'gamma' if g['gamma'] else 'nonGamma_pos'
            R[(p, kind)]['cycles'] += 1
            if not g['gamma']: posnon.append((r['name'], r['hole'], p, r['linkdeg'], 'L', g['L'], 'w', g['w'], 'a,b,d', g['a'], g['b'], g['d']))
            for k, v in g['exits'].items():
                if k.startswith('lockless_'):
                    m = re.search(r'_u(\d+)_f(\d+)', k); UF[(p, kind)][(int(m.group(1)), int(m.group(2)))] += v
            if g['gamma']:
                n10 = g['L'] // 10
                ratio[p]['a>=L/5' if g['a'] >= g['L'] // 5 else ('a>=L/10' if g['a'] >= n10 else 'a<L/10')] += 1
                ratio[p]['min_a_over_L10'] = min(ratio[p].get('min_a_over_L10', 999), g['a'] / n10 if n10 else 999) if False else 0
                R[(p, kind)]['a_list_' + str(g['a']) + '_L' + str(g['L'])] += 1
    print('=== %s holes %s' % (lab, dict(holes)))
    for k in sorted(R):
        fs = [ff for (u, ff) in UF[k]]
        print('  %s %s: cycles %d; lockless exits (u,f) %s; min f %s' % (k[0], k[1], R[k]['cycles'], sorted(UF[k].items()), min(fs) if fs else None))
        print('     lockless count per cycle (a, L):', sorted((x[7:], v) for x, v in R[k].items() if x.startswith('a_list_')))
    for p in ratio: print('  %s Gamma-cycles: %s' % (p, {k: v for k, v in ratio[p].items() if k != 'min_a_over_L10'}))
    print('  positive NON-Gamma cycles: %d; first: %s' % (len(posnon), posnon[:3]))
