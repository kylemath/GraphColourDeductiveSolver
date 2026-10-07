#!/usr/bin/env python3
"""xcheck.py DIR: align jobq-steps (sigma fixed-point flag) with jobm-gamma-sequences (exit labels) cycle by cycle (exact type/k sequence,
any rotation) and count R3 states where 'X' (jobm) and 'fixed' (jobq) disagree, by jobm label."""
import json, sys
from collections import Counter
D = sys.argv[1] if len(sys.argv) > 1 else '../'
m = {}
for l in open(D + 'jobm-gamma-sequences.jsonl'):
    r = json.loads(l)
    if r['pattern'] == '5,5,5,5,6': m.setdefault((r['name'], r['hole'], r['run'][1:]), []).extend(r['jobm'])
c = Counter(); ncyc = 0
for l in open(D + 'jobq-steps.jsonl'):
    r = json.loads(l)
    if r.get('pattern') != '5,5,5,5,6': continue
    for q in r['jobq']:
        best = None
        for mc in m.get((r['name'], r['hole'], r['run'][1:]), []):
            if len(mc) != len(q): continue
            for s in range(len(q)):
                if all(mc[(i + s) % len(q)][0] == x[1] and mc[(i + s) % len(q)][1] == x[2] for i, x in enumerate(q)):
                    mis = [(mc[(i + s) % len(q)][2], x[3]) for i, x in enumerate(q) if x[1] == 3 and (mc[(i + s) % len(q)][2] == 'X') != bool(x[3])]
                    if best is None or len(mis) < len(best): best = mis
        ncyc += 1
        if best is None: c['nomatch'] += 1
        else:
            for t in best: c[t] += 1
print(D, 'cycles', ncyc, 'disagreements (jobm label, jobq fixed flag):', dict(c))
