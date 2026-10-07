import json, glob
from collections import Counter
H = Counter(); Hn = {}; cls = []
for f in sorted(glob.glob('out-*.jsonl'), key=lambda f: int(f[4:-6])):
    n = int(f[4:-6]); hn = Counter()
    for l in open(f):
        r = json.loads(l)
        if r['kind'] == 'graph':
            for w, L, c in r['hist']: hn[(w, L)] += c
        else: cls.append(r)
    Hn[n] = hn; H.update(hn)
print('cycles (per hole-space) by order:', {n: sum(h.values()) for n, h in Hn.items()})
wh = Counter(); lh = Counter()
for (w, L), c in H.items(): wh[w] += c; lh[L] += c
print('winding histogram, all cycles orders 12-24:', sorted(wh.items()))
print('max winding', max(wh), 'min', min(wh))
print('positive winding histogram:', {w: c for w, c in sorted(wh.items()) if w > 0})
print('cycle length histogram (all):', sorted(lh.items()))
pl = Counter((w, L) for (w, L), c in H.items() for _ in range(c) if w > 0)
print('positive (w,L):', sorted(pl.items()))
print('length mod 10 of positive cycles:', Counter(L % 10 for (w, L) in pl.elements()))
print('length mod 5 of all cycles:', Counter({m: sum(c for L, c in lh.items() if L % 5 == m) for m in range(5)}))
print('all cycles (w,L) with w!=0 length mod 10:', Counter(L % 10 for (w, L), c in H.items() if w != 0 for _ in range(c)))
print()
print('classes (hole-spaces) with positive cycle by order:', Counter(r['n'] for r in cls))
print('npos distribution:', Counter(r['npos'] for r in cls))
print('positive cycles by order:', Counter(r['n'] for r in cls for c in r['cycles']))
print('positive windings:', Counter(c['w'] for r in cls for c in r['cycles']))
print('max w+', max(c['w'] for r in cls for c in r['cycles']))
print('L mod 10:', Counter(c['L'] % 10 for r in cls for c in r['cycles']))
print('(w,L):', sorted(Counter((c['w'], c['L']) for r in cls for c in r['cycles']).items()))
print('L/w ratio:', sorted(Counter(round(c['L'] / c['w'], 2) for r in cls for c in r['cycles']).items()))
print('has neighbour:', sum('minnb' in c for r in cls for c in r['cycles']), '/', sum(len(r['cycles']) for r in cls))
print('min neighbour winding < 0:', sum(c.get('minnb', 0) < 0 for r in cls for c in r['cycles']))
print('dominates |w-|>=w+:', Counter(c.get('dominates') for r in cls for c in r['cycles']))
nd = [(r['n'], r['gentri'], r['hole'], c['w'], c['minnb'], c['L']) for r in cls for c in r['cycles'] if c.get('dominates') is False]
print('non-dominating:', nd[:20])
print('(w+, minnb):', sorted(Counter((c['w'], c.get('minnb')) for r in cls for c in r['cycles']).items()))
print('minnb swap types (counted per positive cycle: set of types):')
t = Counter(); t1 = Counter()
for r in cls:
    for c in r['cycles']:
        s = frozenset(tuple(k) for k, v in c.get('minnb_swaps', []))
        t[tuple(sorted(s))] += 1
        for k in s: t1[k] += 1
for k, v in t1.most_common(): print('  any swap of type', k, ':', v)
print('  distinct type-sets:', len(t))
for k, v in t.most_common(8): print('  ', v, k)
ex = [c for r in cls for c in r['cycles']]
print('cycles with a DL-alphaAB-type swap to min nbr:', sum(any(k[0][:2] == ['DL', 'alphaAB'] for k in c.get('minnb_swaps', [])) for c in ex))
print('cycles whose min-nbr swaps ALL ring2:', sum(all(k[0][2] == 'ring2' for k in c.get('minnb_swaps', [])) for c in ex), ' ALL noring2:', sum(all(k[0][2] == 'noring2' for k in c.get('minnb_swaps', [])) for c in ex))
print('cycles with a negative neighbour (any):', sum(any(w < 0 for w, _ in c['nbw']) for c in ex))
print('classes: flow neighbour windings sample:')
for r in cls[-8:]: print(r['n'], r['gentri'], r['hole'], r['windings'], [(c['w'], c['L'], c['nbw']) for c in r['cycles']])
