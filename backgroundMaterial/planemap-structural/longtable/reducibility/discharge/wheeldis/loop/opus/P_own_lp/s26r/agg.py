import json, sys, collections
R = [json.loads(l) for l in open(sys.argv[1])]
print('r2 lines', len(R), 'r2 with r3 survivors', sum(1 for r in R if r['surv']))
print('total r3 domain', sum(r['domain'] for r in R), 'total r3 survivors (strict)', sum(r['surv'] for r in R))
E = [r for r in R if r.get('surv_exact')]
print('exact (no >=9 in ball) survivors', sum(r['surv_exact'] for r in E))
mx = max(r['max_exact'] for r in E); print('max ball sum(6-d) over exact survivors', mx)
top = sorted(E, key=lambda r: -r['max_exact'])[:12]
for r in top: print('  ', r['max_exact'], 'r2', r['r2'], 'r3', r['wit_max'], 'base2', r['base2'])
print('hist of per-r2 max', sorted(collections.Counter(r['max_exact'] for r in E).items()))
S = [r for r in R if 'surv_small' in r]
print('all-small r2:', [(r['r2'], r['surv_small'], r.get('max_small'), r.get('wit_small')) for r in S])
print('excluded out=0 letters per frame', collections.Counter(r['excl'] for r in R))
