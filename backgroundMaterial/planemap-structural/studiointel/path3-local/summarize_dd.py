#!/usr/bin/env python3
"""path3-local/summarize_dd.py -- aggregate kc_dd_search logs: per run the seed stats, the maxima of excess_j, DL chain length, DD_j, sum_j DD_j,
the lowest filled fraction among classes with chain >= 2, where they occur, and the check totals. Usage: summarize_dd.py RUNDIR"""
import sys, os, json, glob, gzip
from collections import Counter
for p in sorted(glob.glob(os.path.join(sys.argv[1], 'log-*.jsonl*'))):
    seed = None; mx = {}; n = 0; bad = 0; stop = None; exc_hist = Counter()
    for L in (gzip.open(p, 'rt') if p.endswith('.gz') else open(p)):
        r = json.loads(L)
        if 'STOP' in r: stop = r; continue
        if 'stats' not in r: continue
        n += 1; s = r['stats']; bad += r['checks_bad']; exc_hist[s['max_excess']] += 1
        if seed is None: seed = s
        for k, better in (('max_excess', max), ('max_chain', max), ('max_DD', max), ('max_DDsum', max), ('min_frac_chain2', min), ('min_frac', min)):
            if k not in mx or better(s[k], mx[k][0]) != mx[k][0]: mx[k] = (s[k], r['sha'], r['step'], s.get('excess_class') if k == 'max_excess' else None)
    print(json.dumps({'run': os.path.basename(p)[4:].split('.jsonl')[0], 'evals': n, 'checks_bad': bad, 'stopped_below_quarter': stop is not None,
                      'seed': {k: seed[k] for k in ('max_excess', 'max_chain', 'max_DD', 'max_DDsum', 'min_frac', 'min_frac_chain2')} if seed else None,
                      'max': {k: list(v) for k, v in mx.items()}, 'excess_hist': sorted(exc_hist.items())}))
