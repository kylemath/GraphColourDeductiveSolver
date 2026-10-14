#!/usr/bin/env python3
"""Summarise S2 logs: distinct cycle classes, min gap overall / by chi / sphere vs not, filled per cycle state, hits."""
import sys, json
from collections import defaultdict
for f in sys.argv[1:]:
    R = [json.loads(l) for l in open(f)]
    hits = [r for r in R if r['ev'] == 'HIT']
    by = defaultdict(lambda: [0, 10 ** 9, 10 ** 9.0])
    for r in R:
        key = ('sphere' if r['chi'] == 2 and not r['pinched'] else ('pinched' if r['pinched'] else 'manifold chi<2'))
        b = by[key]; b[0] += 1; b[1] = min(b[1], r['gap']); b[2] = min(b[2], r['cls']['filled'] / r['cls']['onCyc'])
    chis = sorted({r['chi'] for r in R})
    low = sorted(R, key=lambda r: r['gap'])[:5]
    print(f, 'cycle classes', len(R), 'HITS', len(hits))
    for k, b in sorted(by.items()):
        print(f'  {k}: classes {b[0]}, min gap {b[1]}, min filled/onCyc {b[2]:.3f}')
    print('  chi values', chis)
    nonsph = [r for r in R if r['chi'] < 2 or r['pinched']]
    print('  min gap by chi:', sorted({(r['chi'], min(x['gap'] for x in R if x['chi'] == r['chi'])) for r in R}))
    for r in low:
        print('  low:', r['gap'], 'chi', r['chi'], 'orient', r['orientable'], 'pinched', r['pinched'], 'n', r['n'], 'cls', [r['cls'][k] for k in ('size', 'filled', 'DL', 'onCyc')])
