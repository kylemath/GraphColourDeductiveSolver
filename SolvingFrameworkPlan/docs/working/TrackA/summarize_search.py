#!/usr/bin/env python3
"""Track A: summarise search jsonl files: per (seed, objective) start/best, global best per objective, evaluations, hits;
margin trend = best key reached per walk vs iteration (first/last log entry). Saves best graphs to out/best/."""
import json, sys, os
from collections import defaultdict
os.makedirs('out/best', exist_ok=True)
R = [json.loads(l) for fn in sys.argv[1:] for l in open(fn)]
ev = sum(r.get('evaluations', 0) or 0 for r in R); hits = sum(len(r.get('hits', [])) for r in R)
print('walks', len(R), 'evaluations', ev, 'hits', hits, 'errors', sum(1 for r in R if 'error' in r))
by = defaultdict(list)
for r in R:
    if 'error' in r: print('ERR', r['seed'], r['obj'], r['error']); continue
    by[(r['seed'], r['obj'])].append(r)
glob = {}
for (s, o), rs in sorted(by.items()):
    b = min(rs, key=lambda r: r['best'])
    print('%-45s %s n=%d start=%s best=%s (deg5 %d, margin %.4f, worst %.4f) evals=%d' % (s, o, b['n'], b['start'], b['best'], b['best_deg5'], b['best_margin'], b['best_worst'], sum(r['evaluations'] for r in rs)))
    if o not in glob or b['best'] < glob[o]['best']: glob[o] = b
for o, b in glob.items():
    print('GLOBAL BEST', o, b['seed'], 'walk', b['walk'], b['best'], 'deg5', b['best_deg5'], 'margin', b['best_margin'], 'worst', b['best_worst'])
    json.dump(dict(faces=b['best_faces'], seed=b['seed'], obj=o, best=b['best']), open('out/best/best-%s-%s.json' % (o, os.path.basename(sys.argv[1]).split('.')[0]), 'w'))
# overall min margin and min worst seen among bests (any objective)
allb = [r for rs in by.values() for r in rs]
print('min best_margin over all walks', min(r['best_margin'] for r in allb), '; min best_worst', min(r['best_worst'] for r in allb))
