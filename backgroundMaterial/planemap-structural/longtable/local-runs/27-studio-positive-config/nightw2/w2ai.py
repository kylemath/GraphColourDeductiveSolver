#!/usr/bin/env python3
"""w2ai.py (NightW2 §9): W2**(a),(b) from Job AI's explicit {A,B}-cycle bases (jobuv/jobai.json), (5,5,5,5,6), 552 periods.
Ring names renormalised so p = x2 (y = w1, z = w2), matching NightW2 §1. Position-5 cycles are {2,3}-cycles, position-7 cycles {3,4}-cycles (§1 colours).
Note: jobai.json stores only |K| per step, not K's vertices, so |C5 & K4| and 'C8 created by K7 \\ K4' cannot be read here. Single core, < 1 s."""
import json, re
from collections import Counter
d = json.load(open('../jobuv/jobai.json'))
def norm(names):
    xs = [int(n[1]) for n in names if n[0] == 'x']
    return names
c = Counter(); n = 0
def rs(cyc, sh):
    out = []
    for nm in cyc['ring']:
        if nm == 'm': out.append('m'); continue
        out.append('%s%d' % (nm[0], (int(nm[1]) - sh) % 5))
    return tuple(sorted(out))
for r in d:
    for per in r['periods']:
        n += 1
        # find p's index: at pos 4 (R3k2) p = x_q; infer shift from any cycle? use 'p' flag not enough -> use ring P path: pos-4 2-ball path y w0 w4 x4 x3 z (q=2)
        # shift s such that ring names map with q -> 2: recover q from jobai via the fixed local path is not stored; use a cycle containing both y and z flags
        P4, P5, P6, P7, P8 = (per[str(k)] for k in range(4, 9))
        F4 = P4['rank'] == 0; F8 = P8['rank'] == 0
        if F4:
            c[('F4: rank C5 >= 1', P5['rank'] >= 1)] += 1
            for cy in P5['cycles']:
                c[('F4: C5 through p/y/z/m', cy['p'], cy['y'], cy['z'], cy['m'])] += 1
                c[('F4: C5 len', cy['len'])] += 1
            if P6['rank'] == 0:
                for cy in P8['cycles']:
                    c[('F4 kill case: C8 through p/y/z/m', cy['p'], cy['y'], cy['z'], cy['m'])] += 1
                    s5 = set(v for q in P5['cycles'] for v in q['verts'])
                    c[('F4 kill case: |C8 & (union of C5)|', len(set(cy['verts']) & s5))] += 1
        if F8:
            c[('F8: rank C7 >= 1', P7['rank'] >= 1)] += 1
            for cy in P7['cycles']: c[('F8: C7 through p/y/z/m', cy['p'], cy['y'], cy['z'], cy['m'])] += 1
        # W2': any cycle at 4/6/8 through y or z, broken down
        yz = tuple(any(cy['y'] or cy['z'] for cy in per[str(k)]['cycles']) for k in (4, 6, 8))
        c[('W2prime (pos4, pos6, pos8 has y/z-cycle)', yz)] += 1
        c[('pos4 y/z-cycle or pos8 y/z-cycle', yz[0] or yz[2])] += 1
print('periods', n)
for k, v in sorted(c.items(), key=str): print(v, k)
