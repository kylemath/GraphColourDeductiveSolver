#!/usr/bin/env python3
"""[Track E] aggregate C0 outputs (out/c0_16.jsonl + out/c0_more.jsonl, deduplicated by graph only approximately: records are per (T, t0))."""
import json, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
R = []
for f in ('out/c0_16.jsonl', 'out/c0_more.jsonl'):
    p = os.path.join(HERE, f)
    if os.path.exists(p): R += [json.loads(l) for l in open(p)]
out = []
P = lambda *a: out.append(' '.join(str(x) for x in a))
P('(T, t0) records:', len(R), ' graphs (t0 = 0) by order:', sorted(Counter(r['n'] for r in R if r['t0'] == 0).items()))
for k in ['J_nonint', 'cycles_not_pm3', 'cyclicQ_cancel_fail', 'forest_s_multi_partner', 'group_fail']: P(k, sum(r[k] for r in R))
P('pairs total', sum(r['pairs'] for r in R), ' pairs with cyclic Q_s', sum(r['cyclicQ_pairs'] for r in R), ' tree terms', sum(r['tree_terms'] for r in R))
P('records with pairs = 0:', sum(r['pairs'] == 0 for r in R), ' of which with no separating triangle:', sum(r['pairs'] == 0 and r['sep_tri'] == 0 for r in R))
nz = [r for r in R if r['pairs'] > 0]
P('lower moments (j < c_min) all zero:', all(r['lower_moments_zero'] for r in R), '; moment j = c_min nonzero:', sum(r['leading_moment'] != [0, 0] for r in nz), '/', len(nz), '(random integer weights, not the spoke-circulation weights)')
P('c_min distribution', sorted(Counter(r['cmin'] for r in nz).items()))
open(os.path.join(HERE, 'out/c0-summary.txt'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
