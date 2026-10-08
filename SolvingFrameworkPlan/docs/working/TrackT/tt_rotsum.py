#!/usr/bin/env python3
"""summarise tt_rot.py output"""
import json, sys, collections
agg = collections.defaultdict(lambda: collections.Counter()); ex = {}
for l in open(sys.argv[1]):
    try: d = json.loads(l)
    except Exception: continue
    key = 'mirror' if tuple(d['order']) == (0, 4, 3, 2, 1) else 'planar' if d['planar'] else 'nonplanar'
    a = agg[key]; a['holes'] += 1; a['steps'] += d['steps']; a['viol'] += d['viol']; a['closed'] += d['nclosed']
    a['rrun_max'] = max(a['rrun_max'], d['rrun']); a['nrcm_max'] = max(a['nrcm_max'], d['nrcm'])
    for w in d['closed']:
        L = len(w); law = all((int(w[i]) - int(w[(i + 1) % L])) % 2 == 1 for i in range(L))
        a['closed_law'] += law; a['closed_with1'] += '1' in w
        if law: ex.setdefault(key, []).append((d['g'], d['h'], d['order'], w))
    if d['rrun'] >= 8: ex.setdefault(key + '_rrun', []).append((d['g'], d['h'], d['order'], d['rrun']))
for k, v in agg.items(): print(k, dict(v))
for k, v in ex.items(): print(k, v[:6])
