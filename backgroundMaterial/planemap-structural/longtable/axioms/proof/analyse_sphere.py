import json, sys
from collections import Counter
rows = [json.loads(l) for l in open(sys.argv[1])]
def ham(d): return [s for s in d['states'] if s['kH'] == 1]
dA = Counter(); dO = Counter(); a5 = Counter(); seqs = []
for d in rows:
    hs = ham(d)
    ar = [s['area_in'] for s in hs]
    for x, y in zip(ar, ar[1:]): dA[y - x] += 1
    O = [s['O_corner'] for s in d['states']]
    for x, y in zip(O, O[1:]): dO[y - x] += 1
    for s in d['states']: a5[s['a5v']] += 1
    if d['L'] >= 7: seqs.append((d['g'], d['h'], d['L'], d['word'], ar, O, [s['DX_corner'] for s in d['states']], [s['DY_corner'] for s in d['states']]))
print('windows', len(rows), 'A5v', dict(a5))
print('area_in change between consecutive Ham states', sorted(dA.items()))
print('|O| change per step', sorted(dO.items()))
for s in seqs: print(s)
