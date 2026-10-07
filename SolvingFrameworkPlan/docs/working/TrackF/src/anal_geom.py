#!/usr/bin/env python3
"""Track F: hole geometry vs DL-run length (multi-hole view).
For each hole: pentagon distance profile (number of other degree-5 vertices at dual distance 2, 3, 4, ...).
Reports mean / max of per-hole maxrun by n2 = #pentagons at distance 2 and by the full profile (d2,d3);
per graph: does the hole with the most near pentagons have the shortest runs?  And the DL-state pocket statistics
(np2 = pentagons in the Lock2 pocket, with mean length of the run containing the state).
usage: anal_geom.py GRAPHS.txt HOLES.jsonl..."""
import sys, json, collections
G = {}
for l in open(sys.argv[1]):
    p = l.split(); name, n = p[0], int(p[1]); rot = [list(map(int, r.split(','))) for r in p[2].split(';')]; G[name] = rot
def prof(rot, h):
    dist = {h: 0}; q = [h]
    for u in q:
        for w in rot[u]:
            if w not in dist: dist[w] = dist[u] + 1; q.append(w)
    c = collections.Counter(dist[v] for v in range(len(rot)) if v != h and len(rot[v]) == 5)
    return tuple(c.get(d, 0) for d in range(2, 9))
recs = [json.loads(l) for f in sys.argv[2:] for l in open(f)]
recs = [d for d in recs if d.get('kind') == 'hole' and d['graph'] in G]
for d in recs: d['prof'] = prof(G[d['graph']], d['hole'])
by = collections.defaultdict(list)
for d in recs: by[d['prof'][0]].append(d['maxrun'])
print('n2 = #other pentagons at dual distance 2 (the w-positions):  holes, mean maxrun, max maxrun')
for k in sorted(by): v = by[k]; print(f'  n2={k}: {len(v):6d} holes  mean {sum(v)/len(v):.2f}  max {max(v)}')
by = collections.defaultdict(list)
for d in recs: by[(d['prof'][0], d['prof'][1])].append(d['maxrun'])
print('(n2, n3):  holes, mean maxrun, max maxrun')
for k in sorted(by): v = by[k]; print(f'  {k}: {len(v):6d}  mean {sum(v)/len(v):.2f}  max {max(v)}')
# per order: correlation of maxrun with n2 restricted to largest order
import statistics
for n in sorted({d['n'] for d in recs}):
    R = [d for d in recs if d['n'] == n]
    if len(R) < 30: continue
    x = [d['prof'][0] + 0.5 * d['prof'][1] for d in R]; y = [d['maxrun'] for d in R]
    import numpy as np
    try: r = float(np.corrcoef(x, y)[0, 1])
    except Exception: r = float('nan')
    print(f'order {n} (C{2*n-4}): holes {len(R)}  corr(maxrun, n2 + n3/2) = {r:.3f}')
# Lock2 pocket pentagon count vs mean length of the containing run (all DL states)
agg = collections.defaultdict(lambda: [0, 0.0]); agg1 = collections.Counter()
for d in recs:
    for k, (c, m) in d['np2'].items(): agg[int(k)][0] += c; agg[int(k)][1] += c * m
    for k, c in d['np1'].items(): agg1[int(k)] += c
print('np2 (pentagons in the Lock2 pocket) over all DL states: count, mean length of the containing maximal run')
for k in sorted(agg): c, s = agg[k]; print(f'  np2={k}: {c:12d}  mean run {s/c:.3f}')
print('np1 (pentagons in the Lock1 inner pocket):', dict(sorted(agg1.items())))
