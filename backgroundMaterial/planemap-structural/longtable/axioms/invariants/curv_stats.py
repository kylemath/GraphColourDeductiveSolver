"""Aggregate curv_track output: identity, alpha invariance, role cycling, swap curvature parity, monotonicity."""
import sys, json
from collections import Counter
C = Counter(); dk = Counter(); dn = Counter(); mono = Counter(); seen = set(); kseq = []
for p in sys.argv[1:]:
    for l in open(p):
        d = json.loads(l); rows = d['rows']
        key = (d['name'], d['hole'], tuple(r['state'] for r in rows))
        if key in seen: continue
        seen.add(key); C['runs'] += 1
        a = [r['role'].index('a') for r in rows]
        C['alpha_fixed'] += len(set(a)) == 1
        ok3 = all(rows[t + 1]['role'][c] == {'m': 'A', 'A': 'B', 'B': 'm', 'a': 'a'}[rows[t]['role'][c]] for t in range(len(rows) - 1) for c in range(4))
        C['roles_cycle_mAB'] += ok3
        for r in rows:
            C['states'] += 1; C['identity'] += r['identity']; C['pi_mismatch'] += r.get('pi_mismatch', False)
            dk[r['dkappa_alpha']] += 1
        al = a[0]
        ka = [r['kappa'][al] for r in rows]; na = [r['n'][al] for r in rows]
        for x, y in zip(na, na[1:]): dn[y - x] += 1
        mono['incr' if all(y >= x for x, y in zip(ka, ka[1:])) else 'decr' if all(y <= x for x, y in zip(ka, ka[1:])) else 'no'] += 1
print(dict(C))
print('d kappa_alpha per pi step:', dict(sorted(dk.items())))
print('d n_alpha per pi step:', dict(sorted(dn.items())))
print('kappa_alpha monotone along run:', dict(mono))
