#!/usr/bin/env python3
"""Track A task 3: per-n table for posw search files (search.jsonl, search2.jsonl).
Per n: walks visiting, recorded states (trace every 10 iterations + per-n best), walks with a w > 0 cycle at n,
max positive weight (sum over holes of w over w > 0 cycles), max w of one cycle, min slack over classes with N > 8 among recorded states
(slack = -sum w / N; the key ranks positive mass first, so this is the min over recorded states, not over all evaluations).
usage: posw_report.py SEARCH.jsonl..."""
import sys, json
from collections import defaultdict
R = [json.loads(l) for fn in sys.argv[1:] for l in open(fn)]
print('walks', len(R), 'evaluations', sum(r['evaluations'] for r in R), 'hits', sum(len(r['hits']) for r in R))
vis = defaultdict(set); posw = defaultdict(int); maxw = defaultdict(int); npos = defaultdict(int); wpos = defaultdict(set); sl = defaultdict(lambda: 9.0); rec = defaultdict(int)
for i, r in enumerate(R):
    for n, b in r['best_by_n'].items():
        n = int(n); k = b['key']; vis[n].add(i); rec[n] += 1
        posw[n] = max(posw[n], k[1]); maxw[n] = max(maxw[n], b['info']['maxw']); npos[n] = max(npos[n], b['info']['npos'])
        if k[1] > 0: wpos[n].add(i)
        sl[n] = min(sl[n], -k[2])
    for it, n, k, t in r['trace']:
        rec[n] += 1; sl[n] = min(sl[n], -k[2])
        if k[1] > 0: wpos[n].add(i); posw[n] = max(posw[n], k[1])
print('n | walks | recorded | walks w>0 | max posw | max npos | max w | min slack (N>8)')
for n in sorted(vis):
    print('%d | %d | %d | %d | %d | %d | %d | %.4f' % (n, len(vis[n]), rec[n], len(wpos[n]), posw[n], npos[n], maxw[n], sl[n]))
