"""Which elementary swaps recur between near rule shapes? usage: python3 ops.py"""
import collections as C, json, re
src = open('code/build_atlas.py').read().split('# ---- configs')[0]
exec(src)
ids = lambda f: [r['id'] for r in rules if f(r)]
rsst_r = ids(lambda r: r['src'] == 'rsst'); all588 = ids(lambda r: r['src'] in ('rsst', 'ext588')); nl = ids(lambda r: r['src'] == 'nl26')
def canon(s):
    role, ch = s.split(': '); a, b = ch.split(' to ')
    kind = role.split()[0]
    if a > b: a, b = b, a           # undirected
    return kind, a, b
def gen(s):
    k, a, b = canon(s)
    if 'absent' in (a, b): return f'{k}: add or drop'
    def box(x):
        if x == '*' or x == 'any': return (5, 9)
        if x == '9+': return (9, 9)
        m = re.match(r'>=(\d)', x)
        if m: return (int(m[1]), 9)
        m = re.match(r'<=(\d)', x)
        if m: return (5, int(m[1]))
        m = re.match(r'in(\d)..(\d)', x)
        if m: return (int(m[1]), int(m[2]))
        return (int(x), int(x))
    A, B = box(a), box(b)
    if A[0] <= B[0] and A[1] >= B[1] or B[0] <= A[0] and B[1] >= A[1]: return f'{k}: widen or narrow'
    if abs(A[0] - B[0]) <= 1 and abs(A[1] - B[1]) <= 1: return f'{k}: shift degree by one'
    return f'{k}: other change'
out = {}
for name, ids in (('rsst', rsst_r), ('ext588', all588), ('nl26', nl)):
    pr = pairs_of(ids); n = len(pr)
    fine = C.Counter(); coarse = C.Counter(); npairs = C.Counter()
    for a in range(n):
        for b in range(a + 1, n):
            if rules[pr[a][0]]['lang'] != rules[pr[b][0]]['lang']: continue
            d = dist(RO[pr[a][0]], RO[pr[b][0]])
            if d == 0 or d > 2: continue
            npairs[d] += 1
            for s in diff(RO[pr[a][0]], RO[pr[b][0]]):
                fine[canon(s)] += 1; coarse[gen(s)] += 1
    tot = sum(fine.values())
    print('\n==', name, 'pairs at 1,2:', dict(npairs), 'changes', tot, 'distinct fine ops', len(fine))
    cum = 0
    for i, (k, v) in enumerate(fine.most_common(12)):
        cum += v; print(f'  {k} {v}  cum {cum/tot:.2f}')
    print('  coarse:', coarse.most_common())
    out[name] = dict(pairs=dict(npairs), fine=[[list(k), v] for k, v in fine.most_common()], coarse=coarse.most_common())
json.dump(out, open('results/ops.json', 'w'), indent=1)
