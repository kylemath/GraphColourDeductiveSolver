"""Statistics of primal Kempe features over all sphere NR runs (primal_*.jsonl)."""
import sys, json
from collections import Counter
C = Counter(); spread = Counter(); kd = Counter(); ch = Counter(); d2 = Counter(); mono = Counter(); llen_m = Counter()
seen = set()
for p in sys.argv[1:]:
    for l in open(p):
        d = json.loads(l)
        key = (d['name'], d['hole'], tuple(r['state'] for r in d['rows']))
        if key in seen: continue
        seen.add(key)
        rows = d['rows']; C['runs'] += 1
        for r in rows:
            C['states'] += 1
            ns = sorted(r['n'].values()); spread[ns[-1] - ns[0]] += 1
            kd[r['K_A'] - r['K_a']] += 1
            ch[tuple(r['chains'][q] for q in ('am', 'aA', 'aB', 'mA', 'mB', 'AB'))] += 1
            C['L1L2'] += r['L1'] * r['L2']
            C['K0neK'] += 1 - r['K0_eq_K']
        ll = [r['llen'] for r in rows]
        llen_m['nonincr' if all(b <= a for a, b in zip(ll, ll[1:])) else 'nondecr' if all(b >= a for a, b in zip(ll, ll[1:])) else 'no'] += 1
        # sorted class-size vector over the run: does it ever change?
        mono[len(set(tuple(sorted(r['n'].values())) for r in rows))] += 1
print('runs', C['runs'], 'states', C['states'], 'double lock at all states', C['L1L2'], 'K != K0 (pi defined, = A5v)', C['K0neK'])
print('max-min colour class size:', dict(sorted(spread.items())))
print('|K cap A| - |K cap alpha| for the pi swap chain:', dict(sorted(kd.items())))
print('chain counts (am,aA,aB,mA,mB,AB):', ch.most_common(8))
print('lock length llen monotone along run:', dict(llen_m))
print('number of distinct sorted class-size vectors per run:', dict(sorted(mono.items())))
