#!/usr/bin/env python3
"""routeb/rsst_summary.py -- summarise rsst_run.py JSONL outputs per configuration."""
import sys, json, glob
from collections import defaultdict, Counter
rows = [json.loads(l) for f in sys.argv[1:] for l in open(f) if l.startswith('{')]
by = defaultdict(list)
for r in rows: by[r['idx']].append(r)
stat = Counter()
for i in sorted(by):
    rs = by[i]; red = [r['v'] for r in rs if r.get('reducible')]; cap = [r['v'] for r in rs if 'capped' in r or 'error' in r]
    kind = 'C' if rs[0]['contract'] else 'D'
    st = 'reducible-at-some-v' if red else ('capped' if cap else 'not-reducible-at-any-v')
    stat[(rs[0]['r'], kind, st)] += 1
    print(i, rs[0]['name'], 'ring', rs[0]['r'], kind, 'deg5', len(rs), 'reducible at', red, 'lost', [r.get('lost') for r in rs], 'capped/err', cap, 'max s', max(r['secs'] for r in rs))
print('\nrows', len(rows), 'configurations', len(by))
for k in sorted(stat): print(' ring %d %s %s: %d' % (k[0], k[1], k[2], stat[k]))
