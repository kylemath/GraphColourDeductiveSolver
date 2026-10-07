#!/usr/bin/env python3
"""jobm.py: Job M from jobm-gamma-sequences.jsonl. Each Gamma-cycle is rotated to start at an R3 state with k = 4 and cut into blocks of 10 states
(5 R3 states, k = 4, 3, 2, 1, 0). (5,5,5,5,6): k = position of the degree-6 vertex relative to the repeat j; (5,5,5,6,6): k = position of the first of the
two adjacent degree-6 vertices (kmask 3, 6, 12, 24, 17 -> k 0..4). Success string: bit order k = 0..4, '1' = lockless exit. Block credit = sum (3f - 1)."""
import json
from collections import Counter, defaultdict
K1 = {1: 0, 2: 1, 4: 2, 8: 3, 16: 4}; K2 = {3: 0, 6: 1, 12: 2, 24: 3, 17: 4}
out = defaultdict(lambda: {'pat': Counter(), 'blocks': 0, 'dead': 0, 'minblock': None, 'mincycavg': None, 'k3givenk4': Counter(), 'longestdead': 0, 'exits': Counter(), 'cycles': 0, 'bad': 0})
for l in open('jobm-gamma-sequences.jsonl'):
    r = json.loads(l); P = r['pattern']; KM = K1 if P == '5,5,5,5,6' else K2; o = out[P]
    for seq in r['jobm']:
        o['cycles'] += 1; L = len(seq)
        s0 = next(i for i, x in enumerate(seq) if x[0] == 3 and KM.get(x[1]) == 4); seq = seq[s0:] + seq[:s0]
        blocks = [seq[i:i + 10] for i in range(0, L, 10)]; credits = []; deadflags = []
        for b in blocks:
            r3 = [(KM[x[1]], x[2], x[3]) for x in b if x[0] == 3]
            if sorted(k for k, _, _ in r3) != [0, 1, 2, 3, 4]: o['bad'] += 1; continue
            bits = {k: e for k, e, _ in r3}; o['pat'][''.join('1' if bits[k] == 'L' else '0' for k in range(5))] += 1
            for k, e, f in r3: o['exits'][(k, e, f)] += 1
            c = sum(3 * f - 1 for k, e, f in r3 if e == 'L'); credits.append(c); o['blocks'] += 1
            dead = all(e != 'L' for _, e, _ in r3); deadflags.append(dead); o['dead'] += dead
            o['k3givenk4'][('k4 ' + ('ok' if bits[4] == 'L' else 'fail'), 'k3 ' + ('ok' if bits[3] == 'L' else 'fail'))] += 1
            if o['minblock'] is None or c < o['minblock'][0]: o['minblock'] = (c, r['run'], r['name'], r['hole'], L, ''.join('1' if bits[k] == 'L' else '0' for k in range(5)))
        if not credits: o['nonperiodic'] = o.get('nonperiodic', 0) + 1; continue
        avg = sum(credits) / len(credits)
        if o['mincycavg'] is None or avg < o['mincycavg'][0]: o['mincycavg'] = (round(avg, 2), r['run'], r['name'], r['hole'], L)
        run = best = 0
        for d in deadflags + deadflags:
            run = run + 1 if d else 0; best = max(best, min(run, len(deadflags)))
        o['longestdead'] = max(o['longestdead'], best)
for P, o in out.items():
    c = o['k3givenk4']; a = c[('k4 ok', 'k3 ok')]; b = c[('k4 ok', 'k3 fail')]; cc = c[('k4 fail', 'k3 ok')]; d = c[('k4 fail', 'k3 fail')]
    print('== %s: Gamma-cycles %d (both orientations), blocks %d, malformed blocks %d, cycles with no well-formed block %d' % (P, o['cycles'], o['blocks'], o['bad'], o.get('nonperiodic', 0)))
    print('  success patterns (bits k = 0..4, 1 = lockless):', sorted(o['pat'].items(), key=lambda kv: -kv[1]))
    print('  P(k3 lockless | k4 lockless) = %d/%d; P(k3 lockless | k4 fails) = %d/%d' % (a, a + b, cc, cc + d))
    print('  min block credit:', o['minblock'], '; min per-cycle average block credit:', o['mincycavg'])
    print('  dead blocks:', o['dead'], '; longest run of consecutive dead blocks:', o['longestdead'])
    print('  exit kinds per k (k, kind, f):', sorted(o['exits'].items()))
