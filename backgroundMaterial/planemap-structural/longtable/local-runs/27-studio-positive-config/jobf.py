#!/usr/bin/env python3
"""jobf.py LABEL=FILE ...: Job F, sigma-C at every hole: per pattern, holes, groups, failing groups, max group size (cycles),
fraction of DD-step endpoints whose sigma-image lies on another pi-cycle; first failing group with class/hole size."""
import sys, json
from collections import defaultdict, Counter
P = defaultdict(Counter); first = None; tot = Counter(); posh = Counter()
for a in sys.argv[1:]:
    lab, f = a.split('=')
    for l in open(f):
        r = json.loads(l)
        if r['kind'] != 'hole' or 'sigC' not in r: continue
        sc = r['sigC']; e = P[r['pattern']]
        e['holes'] += 1; e['groups'] += sc['ncomp']; e['fail'] += sc['fail']; e['failholes'] += sc['fail'] > 0
        e['maxg'] = max(e['maxg'], sc['max_ncycles']); e['cross'] += sc['cross_edges']; e['end'] += sc['endpoints']; e['pos'] += r['npos'] > 0
        tot['holes'] += 1; tot['groups'] += sc['ncomp']; tot['fail'] += sc['fail']; tot['pos'] += r['npos'] > 0; tot['posok'] += (r['npos'] > 0 and sc['fail'] == 0)
        if sc['fail'] and first is None: first = (lab, r['name'], r['hole'], r['pattern'], 'hole states', r['states'], 'npos', r['npos'], sc)
print('=== totals', dict(tot)); print('=== first failing group:', first)
print('%-12s %8s %10s %6s %6s %7s %10s %8s' % ('pattern', 'holes', 'groups', 'fail', 'posH', 'maxgrp', 'endpoints', 'cross%'))
for k, e in sorted(P.items(), key=lambda kv: -kv[1]['holes']):
    print('%-12s %8d %10d %6d %6d %7d %10d %8.1f' % (k, e['holes'], e['groups'], e['fail'], e['pos'], e['maxg'], e['end'], 100.0 * e['cross'] / max(1, e['end'])))
