#!/usr/bin/env python3
"""Track A task 3: summarise posw/search.jsonl: per n best key over all walks, evaluations, hits; dump per-n best graphs
(posw/best-by-n.json) for the two-orientation re-scan."""
import json
from collections import defaultdict
R = [json.loads(l) for l in open('posw/search.jsonl')]
print('walks', len(R), 'evaluations', sum(r['evaluations'] for r in R), 'hits', sum(len(r['hits']) for r in R), 'final n', sorted(r['final_n'] for r in R))
B = {}; cnt = defaultdict(int)
for r in R:
    for n, b in r['best_by_n'].items():
        cnt[int(n)] += 1
        if int(n) not in B or b['key'] > B[int(n)]['key']: B[int(n)] = dict(b, seed=r['seed'])
for n in sorted(B):
    b = B[n]; print('n %d walks-visiting %d best key %s npos %d maxw %d seed %s' % (n, cnt[n], b['key'], b['info']['npos'], b['info']['maxw'], b['seed']))
# per-step evaluation counts by n from traces
json.dump([dict(name='posw-best-n%d' % n, faces=B[n]['faces']) for n in sorted(B)], open('posw/best-by-n.json', 'w'))
