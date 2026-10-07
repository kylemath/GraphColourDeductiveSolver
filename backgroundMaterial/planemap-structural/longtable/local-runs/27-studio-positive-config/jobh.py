#!/usr/bin/env python3
"""jobh.py LABEL=FILE ...: Job H (sigma'-groups H1, and H2 = sigma' plus sigma at R3 endpoints) per pattern."""
import sys, json
from collections import defaultdict, Counter
for V in ['H1_sigmap', 'H2_sigmap_plus_sigmaR3']:
    P = defaultdict(Counter); first = None; tot = Counter()
    for a in sys.argv[1:]:
        lab, f = a.split('=')
        for l in open(f):
            r = json.loads(l)
            if r['kind'] != 'hole' or V not in r: continue
            h = r[V]; e = P[r['pattern']]
            e['holes'] += 1; e['groups'] += h['ncomp']; e['cycles'] += r['ncyc']; e['fail'] += h['fail']; e['maxg'] = max(e['maxg'], h['max_ncycles'])
            e['end'] += h['endpoints']; e['cross'] += h['endpoints_with_cross_sigmap']; e['pos'] += r['npos'] > 0; e['onegroup'] += h['ncomp'] == 1
            tot['holes'] += 1; tot['groups'] += h['ncomp']; tot['cycles'] += r['ncyc']; tot['fail'] += h['fail']; tot['pos'] += r['npos'] > 0; tot['onegroup'] += h['ncomp'] == 1
            if h['fail'] and first is None: first = (lab, r['name'], r['hole'], r['pattern'], 'states', r['states'], 'npos', r['npos'], h)
    print('=== %s totals %s; first failure: %s' % (V, dict(tot), first))
    print('%-12s %8s %10s %10s %6s %6s %7s %8s %9s' % ('pattern', 'holes', 'cycles', 'groups', 'fail', 'posH', 'maxgrp', 'cross%', '1-group%'))
    for k, e in sorted(P.items(), key=lambda kv: -kv[1]['holes']):
        print('%-12s %8d %10d %10d %6d %6d %7d %8.1f %9.1f' % (k, e['holes'], e['cycles'], e['groups'], e['fail'], e['pos'], e['maxg'], 100.0 * e['cross'] / max(1, e['end']), 100.0 * e['onegroup'] / e['holes']))
