#!/usr/bin/env python3
"""Job BS summary from jobbs-flat.jsonl: per fullerene size, longest DL run along pi at the flat (6,6,6,6,6) holes, all-DL cycles, min F/N.
Run with --nocls, so jobbo.min_F_over_N is the 2.0 sentinel; studiointel flat_kclass found kappa = 1 at all 153 holes, so class F/N = F / states (reported here)."""
import json, os
from collections import defaultdict, Counter
HERE = os.path.dirname(os.path.abspath(__file__))
R = [json.loads(l) for l in open(os.path.join(HERE, 'jobbs-flat.jsonl'))]
by = defaultdict(list)
for r in R: by[r['n']].append(r)
print('rows (hole x orientation):', len(R), ' patterns:', dict(Counter(r['pattern'] for r in R)))
print('%4s %6s %6s %8s %8s %10s %10s %s' % ('n', 'C_N', 'rows', 'maxrun', 'allDL', 'min F/N', 'npos>0', 'run-length histogram (summed)'))
for n in sorted(by):
    rs = by[n]; h = Counter()
    for r in rs:
        for k, v in r['jobbo']['runlen'].items(): h[int(k)] += v
    print('%4d %6s %6d %8d %8d %10.4f %10d %s' % (n, 'C%d' % (2 * (n - 2)), len(rs), max(r['jobbo']['maxrun'] for r in rs), sum(len(r['jobbo']['all_DL_cycles']) for r in rs),
          min(r['F'] / r['states'] for r in rs), sum(r['npos'] > 0 for r in rs), dict(sorted(h.items()))))
m = max(R, key=lambda r: r['jobbo']['maxrun']); f = min(R, key=lambda r: r['F'] / r['states'])
print('HEADLINE: longest DL run', m['jobbo']['maxrun'], 'at', m['name'], 'hole', m['hole'], '| all-DL cycles at (6,6,6,6,6):', sum(len(r['jobbo']['all_DL_cycles']) for r in R),
      '| min F/N (= F/states, kappa = 1) %.4f' % (f['F'] / f['states']), 'at', f['name'], 'hole', f['hole'], '| sigC fails', sum(r['sigC']['fail'] for r in R), '| rows with a positive cycle', [(r['name'], r['hole'], r['npos'], r['maxw']) for r in R if r['npos'] > 0])
