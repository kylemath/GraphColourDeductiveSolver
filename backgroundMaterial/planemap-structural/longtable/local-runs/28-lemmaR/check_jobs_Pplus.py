#!/usr/bin/env python3
"""[exploratory] NightLemmaR: Lemma P+ on the Studio's Job S records (DD-endpoint form, orders 25-27).
Overflow of a target = max(rem, 0); capped deficit of a source Z = def(Z) + overflow of every target T in nbrN(Z) with rem(T) > 0
(conservative: the whole overflow is charged to every neighbouring source). P1+ = every capped deficit > 0 fits, by a greedy
largest-first single-target assignment, into the slack -min(rem, 0) of its nonpositive sigma-neighbours. Also the hole-level sum."""
import json, os
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '27-studio-positive-config', 'jobs-records.jsonl')
from collections import defaultdict
agg = defaultdict(lambda: [0, 0, 0, 0, []])
for l in open(fn):
    r = json.loads(l); J = r['jobs']; run = r['run']; T = {t[0]: t for t in J['targets']}
    ov = {i: max(t[6], 0) for i, t in T.items()}; slack = {i: -min(t[6], 0) for i, t in T.items()}
    a = agg[run]; a[0] += 1
    capdef = [(p['def'] + sum(ov.get(i, 0) for i in p['nbrN']), p) for p in J['pos']]
    if any(ov.values()): a[1] += 1
    ok = True
    for d, p in sorted(capdef, key=lambda x: -x[0]):
        if d <= 0: continue
        cand = [i for i in p['nbrN'] if i in slack and slack[i] >= d]
        if not cand: ok = False; break
        i = max(cand, key=lambda i: slack[i]); slack[i] -= d
    if not ok: a[2] += 1; a[4].append((r['name'], r['hole']))
    hole_sum = sum(p['def'] for p in J['pos']) + sum(max(t[6], 0) for t in J['targets']) + sum(min(t[6], 0) for t in J['targets'])
    if hole_sum > 0: a[3] += 1
for run, a in sorted(agg.items()):
    print('%s: holes %d, holes with an overflowing target %d, P1+ (greedy one-target, conservative) fails %d %s, hit-part sum > 0: %d' % (run, a[0], a[1], a[2], a[4][:3], a[3]))
