import json, sys, random, time, statistics as st
sys.path.insert(0, 'code')
from canon import cfg_from_pool
from editgraph import build, summary
from nullgen import n1, n2, Torus
d = json.load(open('data/pool_configs.json'))['configs']
R = [cfg_from_pool(c) for c in d[:633]]
reps = int(sys.argv[1]); which = sys.argv[2]
rng = random.Random(12345)
out = {'RSST_or': summary(build(R)), 'RSST_un': summary(build(R, True))}
# reference: other reducible configs in the pool, m-matched sample
from canon import full_code
others = []; seenfc = set(full_code(c) for c in R); seen2=set()
for c in d[633:]:
    x = cfg_from_pool(c); fc = full_code(x)
    if fc in seen2: continue
    seen2.add(fc); others.append(x)
bym = {}
for c in others: bym.setdefault(c['m'], []).append(c)
rows = {'N1': [], 'N2': [], 'POOL': []}
host = None
for r in range(reps):
    t = time.time()
    if 'N1' in which:
        X = n1(R, rng); rows['N1'].append((summary(build(X)), summary(build(X, True))))
    if 'POOL' in which:
        X = []; pools = {k: list(v) for k, v in bym.items()}
        for k in pools: rng.shuffle(pools[k])
        for c in R:
            lst = pools.get(c['m'])
            if lst: X.append(lst.pop())
        rows['POOL'].append((summary(build(X)), summary(build(X, True)), len(X)))
    if 'N2' in which:
        host = Torus(40, 40, rng, 40000)
        X, fail = n2(R, rng, host)
        s = summary(build(X)); s['fail'] = fail
        rows['N2'].append((s, summary(build(X, True))))
    print('rep', r, round(time.time() - t, 1), file=sys.stderr, flush=True)
out['rows'] = rows
json.dump(out, open(f'res12_{which}.json', 'w'))
