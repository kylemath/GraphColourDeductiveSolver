#!/usr/bin/env python3
"""studiointel replay_best.py -- deterministic replay of a finished Phase B run (search.py stage B, same seed, start, caps) to recover the
face list of its best graph. Verifies the replayed graph's sha256 equals the one in the original log. Writes seeds/<tag>.json."""
import sys, json, random, time, os
import graphs, radius, search
from builders import build
seed, start, want = int(sys.argv[1]), sys.argv[2], sys.argv[3]
rng = random.Random(seed); cur = build(start); deadline = time.process_time() + 1800
ev = search.evaluate(cur, 400000, deadline); key = lambda e: (e['F'], e['mean_DL_frac'])
best = (key(ev), cur)
while True:
    moved = False
    for nf in search.neighbours_flip(cur, rng):
        e2 = search.evaluate(nf, 400000, deadline)
        if e2 is None: sys.exit('capped')
        if 'inconclusive' in e2: continue
        if key(e2) > key(ev): cur, ev, moved = nf, e2, True; break
    if not moved: break
h = radius.graph_hash(cur); assert h.startswith(want), (h, want)
os.makedirs('seeds', exist_ok=True)
json.dump({'faces': cur, 'source': 'replay of search.py B --seed %d --start %s' % (seed, start), 'graph_sha256': h}, open('seeds/B%d-best.json' % seed, 'w'))
print('ok', h, len(graphs.degrees(cur)))
