#!/usr/bin/env python3
"""[exploratory] NightBudget pass-2 summary of nightbudget2-records.jsonl ((5,5,5,5,6) holes)."""
import json, os
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
c = Counter(); D = Counter(); mins = {}
for l in open(os.path.join(HERE, 'nightbudget2-records.jsonl')):
    r = json.loads(l); src = 'census' if r['src'] == 'census' else 'other'
    for gk in ('sigma', 'union'):
        for g in r['groups'][gk]:
            c[(gk, src, 'groups with DD')] += 1
            c[(gk, src, "B'_c fails")] += g['slack_c'] < 0
            mins[(gk, src)] = min(mins.get((gk, src), 10 ** 9), g['slack_c'])
            if g['Rm']:
                c[(gk, src, 'R- nonempty')] += 1
                for V in ('V1', 'V2', 'V3'): c[(gk, src, V + ' payer flow ok')] += g.get(V, False)
    for k, v in r['det'].items(): D[(src, k)] += v
for k, v in sorted(c.items()): print(k, v)
print("min B'_c slack", mins)
print('failing literal-R images: (src, (k, kind, full R3 ring?, filled run before / u / f))')
for k, v in sorted(D.items()): print('  %6d %s' % (v, k))
