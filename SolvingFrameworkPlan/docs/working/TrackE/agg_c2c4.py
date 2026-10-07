#!/usr/bin/env python3
"""[Track E] aggregate out/c2c4-*.jsonl -> out/c2c4-summary.txt (data)."""
import json, glob, os
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
recs = []
for f in sorted(glob.glob(os.path.join(HERE, 'out/c2c4-*.jsonl'))):
    recs += [json.loads(l) for l in open(f)]
out = []
P = lambda *a: out.append(' '.join(str(x) for x in a))
byn = Counter(r['n'] for r in recs); graphs = Counter((r['n'], r['g']) for r in recs)
P('records (graph, hole):', len(recs), 'by order:', dict(sorted(byn.items())), 'graphs:', len(graphs))
# C2 flip fractions
T = defaultdict(lambda: dict(swaps=0, flip=Counter(), nz5=0, hull0=0, hull0_noio=0, holes=0))
for r in recs:
    for t, A in r['types'].items():
        X = T[t]; X['swaps'] += A['swaps']; X['nz5'] += A['nz5']
        for k, v in A['flip'].items(): X['flip'][k] += v
        if A['swaps']:
            X['holes'] += 1; X['hull0'] += bool(A['hull0']); X['hull0_noio'] += bool(A['hull0_noio'])
P('\n== C2: single labelled chain swaps; flip[stat] = #swaps on which (-1)^stat changes sign ==')
groups = {'P (i^H)': ['P'], 'Pr (ring Heawood)': ['Pr'], 'n_a': ['n0', 'n1', 'n2', 'n3'], 'link counts': ['l0', 'l1', 'l2', 'l3'],
          'AT1 (12 orders)': None, 'KS Kasteleyn (12 orders)': None, 'io (cube coords)': None, 'kc (#components)': None,
          'W': ['W'], 'lam': ['lam'], 'L1': ['L1'], 'L2': ['L2'], 'hv (Heawood vertex sums)': None}
for t in ['nolink', 'link1', 'link2p', 'nl2', 'nl3', 'nl4', 'nl5', 'rename', 'lock', 'lock_nonrename', 'R1', 'all']:
    X = T[t]; s = X['swaps']
    if not s: P(t, 'no swaps'); continue
    P('\n[%s] swaps=%d  holes with such swaps=%d  hull0 (no F2-combination of all stats flips on every swap) in %d/%d holes; without io stats %d/%d; rep (zeta5) changes on %d'
      % (t, s, X['holes'], X['hull0'], X['holes'], X['hull0_noio'], X['holes'], X['nz5']))
    for gname, names in groups.items():
        if names is None:
            pre = gname.split()[0] + '_' if gname.split()[0] in ('AT1', 'KS', 'io', 'kc') else 'hv'
            names = [k for k in X['flip'] if k.startswith(pre)]
        vals = [X['flip'][k] for k in names]
        P('   %-26s flip fractions: %s' % (gname, ', '.join('%s=%d/%d' % (k, v, s) for k, v in zip(names, vals)) if len(names) <= 4
                                          else 'min %.4f max %.4f (100%% for %s; 0%% for %s)' % (min(vals) / s, max(vals) / s,
                                          [k for k, v in zip(names, vals) if v == s], [k for k, v in zip(names, vals) if v == 0])))
# bipartiteness
P('\n== C2/C3 general test: labelled Kempe classes in which the edge set E has an odd cycle (=> no function at all flips on every E-swap) ==')
B = Counter(); NC = 0; NCL = 0; anycube = Counter()
for r in recs:
    NC += len(r['classes'])
    for ci, c in enumerate(r['classes']):
        locked = c['locked'] > 0; NCL += locked
        okp = [E for E in r['bipcls'] if E.startswith('R1+') and ci not in r['bipcls'][E]]
        if locked:
            anycube['locked classes'] += 1
            anycube['some R1+ab (6 fixed pairs) bipartite'] += any(E.startswith('R1+ab') for E in okp)
            anycube['some R1+e0 (10 edge-cubes) bipartite'] += any(E.startswith('R1+e') for E in okp)
    for E, v in r['bip'].items(): B[E] += v
P('labelled classes:', NC, ' with locked states:', NCL)
for E in sorted(B): P('   %-24s odd-cycle classes: %d' % (E, B[E]))
P('per locked class:', dict(anycube))
# C4
C = Counter()
for r in recs: C.update(r['c4'])
P('\n== C4: canonical unfilled states and lock involutions (R1: lock1 first; R2: lock2 first) ==')
P(dict(sorted(C.items())))
open(os.path.join(HERE, 'out/c2c4-summary.txt'), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
