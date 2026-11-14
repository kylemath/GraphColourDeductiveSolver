import json, sys, math, collections as C
sys.path.insert(0, 'code')
from canon import cfg_from_pool
from editgraph import build, components
d = json.load(open('data/pool_configs.json'))['configs'][:633]
act = set(int(x) for x in open('data/synth_active_588.txt').read().split())
R = [cfg_from_pool(c) for c in d]
res = build(R); E = res['edges']
comp, _ = components(633, [E['deg1'], E['degk']])
fam = {}
for k, v in enumerate(sorted(comp.values(), key=len, reverse=True)):
    for i in v: fam[i] = (k + 1, len(v))
nb = C.defaultdict(set)
for a, b in E['deg1'] | E['degk']: nb[a].add(b); nb[b].add(a)
out = []
for i, c in enumerate(d):
    m, r = c['m'], c['ring']
    ie = sorted({tuple(sorted((u, v))) for u in range(m) for v in c['int_adj'][u]})
    re_ = sorted({(u, t[1]) for u in range(m) for t in c['rot'][u] if t[0] == 'R'})
    # Tutte layout: ring on circle, interior by relaxation
    pos = {('R', k): (math.cos(2 * math.pi * k / r - math.pi / 2), math.sin(2 * math.pi * k / r - math.pi / 2)) for k in range(r)}
    for u in range(m): pos[('I', u)] = (0.0, 0.0)
    nbrs = {u: [('I', v) for v in c['int_adj'][u]] + [('R', t[1]) for t in c['rot'][u] if t[0] == 'R'] for u in range(m)}
    for _ in range(400):
        for u in range(m):
            xs = [pos[w] for w in nbrs[u]]
            pos[('I', u)] = (sum(x for x, _ in xs) / len(xs), sum(y for _, y in xs) / len(xs))
    X = c['X'] if c['X'] != '-' else ''
    out.append(dict(id=i, n=c['name'], k=c['kind'], X=X, r=r, m=m, deg=c['deg'], a=int(i in act),
                    ev=c.get('evidence', ''), fam=fam[i][0], fs=fam[i][1], nb=sorted(nb[i]),
                    ie=ie, re=re_, pi=[[round(pos[('I', u)][0], 4), round(pos[('I', u)][1], 4)] for u in range(m)]))
json.dump(out, open('db/configs.json', 'w'), separators=(',', ':'))
print(len(out), sum(o['a'] for o in out), C.Counter(o['k'] for o in out))
