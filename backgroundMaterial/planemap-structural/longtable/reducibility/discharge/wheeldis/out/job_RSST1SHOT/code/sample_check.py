#!/usr/bin/env python3
"""Independent spot-check of the fullworld DFS claim at d = 5, 6: random fully fixed 2-balls (row-level window,
apexes fixed, every private drawn), ledger + direct containment, no DFS, no pruning.  Every filling with hi > 0
must contain a configuration (K633); count those that contain only 'none' ones (K582 gap).
usage: sample_check.py D N seed"""
import sys, os, random, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rcore as R
d, N, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rnd = random.Random(seed); st = collections.Counter(); bad = []
P = [5, 5, 5, 6, 6, 7, 8, 9]
for t in range(N):
    link = [rnd.choice(P) for _ in range(d)]; apex = [rnd.choice(P) for _ in range(d)]
    W = R.Window(d, link, apex); insts = R.instances(W)
    f = {}
    for i in range(d):
        for j in range(1, R.npriv(link[i]) + 1):
            f['p%d.%d' % (i, j)] = 9 if (link[i] >= 9 and j == 2) else rnd.choice(P)
    lo, hi, _ = R.ledger(d, insts, f)
    st['samples'] += 1
    if hi <= 0: continue
    st['hi_pos'] += 1
    c = R.contained(R.requirements(W), f)
    if not c: st['UNCONTAINED'] += 1; bad.append((link, apex, f, hi))
    elif not any(R.CONFIGS[i]['proved'] for i in c): st['only_none'] += 1
print(json.dumps({'d': d, 'N': N, 'seed': seed, 'stats': dict(st), 'uncontained_examples': bad[:5]}))
