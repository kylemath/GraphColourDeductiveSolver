#!/usr/bin/env python3
"""jobt.py: Job T from jobm-gamma-sequences.jsonl (orders 25-26) and jobr27/jobm-gamma-sequences.jsonl (order 27). Periods = blocks of 10 from R3@k=4 (well-formed
blocks only: one R3 at each k). Outcome tuple over k = 4,3,2,1,0: L<f> lockless, X fixed point, D other DL, 1 Lock1-only, 2 Lock2-only. Block debt 10."""
import json
from collections import Counter, defaultdict
K1 = {1: 0, 2: 1, 4: 2, 8: 3, 16: 4}; K2 = {3: 0, 6: 1, 12: 2, 24: 3, 17: 4}
res = defaultdict(lambda: {'tuples': defaultdict(list), 'pairmin': None, 'win': {1: None, 2: None, 3: None}, 'iii': Counter(), 'cycles': 0, 'skipped': 0, 'cyc_ok': Counter()})
for fn, order in (('jobm-gamma-sequences.jsonl', '25-26'), ('jobr27/jobm-gamma-sequences.jsonl', '27')):
    for l in open(fn):
        r = json.loads(l); KM = K1 if r['pattern'] == '5,5,5,5,6' else K2; o = res[(r['pattern'], order)]
        for seq in r['jobm']:
            try: s0 = next(i for i, x in enumerate(seq) if x[0] == 3 and KM.get(x[1]) == 4)
            except StopIteration: o['skipped'] += 1; continue
            seq = seq[s0:] + seq[:s0]; blocks = []
            ok = True
            for b in range(0, len(seq), 10):
                r3 = {KM.get(x[1], -1): x for x in seq[b:b + 10] if x[0] == 3}
                if sorted(r3) != [0, 1, 2, 3, 4] or any(x[0] == 2 for x in seq[b:b + 10]): ok = False; break
                tup = tuple(('L%d' % r3[k][3]) if r3[k][2] == 'L' else r3[k][2] for k in (4, 3, 2, 1, 0))
                cr = sum(3 * r3[k][3] - 1 for k in r3 if r3[k][2] == 'L'); blocks.append((tup, cr))
            if not ok: o['skipped'] += 1; continue
            o['cycles'] += 1; n = len(blocks); tag = (r['run'], r['name'], r['hole'], len(seq))
            for t, c in blocks: o['tuples'][t].append(c)
            for w in (1, 2, 3):
                if w > n: continue
                m = min(sum(blocks[(i + t) % n][1] for t in range(w)) for i in range(n))
                if o['win'][w] is None or m / (10 * w) < o['win'][w][0]: o['win'][w] = (round(m / (10 * w), 3), m, tag)
                o['cyc_ok'][(w, m >= 10 * w)] += 1
            if n >= 2:
                pm = min(blocks[i][1] + blocks[(i + 1) % n][1] for i in range(n))
                if o['pairmin'] is None or pm < o['pairmin'][0]: o['pairmin'] = (pm, tag)
            for i in range(n):   # (iii) k=4 failure in period i => all k<=2 visits of periods i, i+1 lockless with f >= 2 ?
                if blocks[i][0][0][0] != 'L':
                    ks = [blocks[i][0][j] for j in (2, 3, 4)] + [blocks[(i + 1) % n][0][j] for j in (2, 3, 4)]
                    o['iii'][all(x[0] == 'L' and int(x[1:]) >= 2 for x in ks)] += 1
for (pat, order), o in sorted(res.items()):
    print('== %s order %s: cycles %d (skipped, not R1/R3-periodic: %d)' % (pat, order, o['cycles'], o['skipped']))
    print('  (i) period credit by outcome tuple (k=4,3,2,1,0) [count, min, max]:')
    for t, cs in sorted(o['tuples'].items(), key=lambda kv: min(kv[1])): print('     %-36s %4d %3d %3d' % (' '.join(t), len(cs), min(cs), max(cs)))
    print('  (ii) min credit of two adjacent periods: %s (>= 20 ?)' % (o['pairmin'],))
    print('  (iii) k=4 failure in period i => all k<=2 visits of periods i, i+1 lockless with f >= 2: %s' % dict(o['iii']))
    print('  (iv) min window credit / 10w:', {w: o['win'][w] for w in (1, 2, 3)}, '; cycles with window min >= 10w:', dict(o['cyc_ok']))
