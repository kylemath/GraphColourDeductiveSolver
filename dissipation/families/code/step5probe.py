import json, sys, collections as C
sys.path.insert(0, 'code')
from canon import cfg_from_pool, shape_codes
from editgraph import build, components
d = json.load(open('data/pool_configs.json'))['configs'][:633]
R = [cfg_from_pool(c) for c in d]
res = build(R); E = res['edges']
def xedges(c):
    if c['kind'] != 'C': return None
    out = set()
    for e in c['X'].strip(',').split(','):
        a, b = e.split('-')
        if a[0] != 'I' or b[0] != 'I': return None
        out.add(frozenset((int(a[1:]), int(b[1:]))))
    return out
orders = [shape_codes(r['irot'])[1] for r in R]
def aligned(i, o):
    X = xedges(d[i]); pos = {v: k for k, v in enumerate(o)}
    return frozenset(frozenset(pos[v] for v in e) for e in X)
kinds = C.Counter(); sameX = C.Counter()
for t in ('deg1', 'degk'):
    for i, j in E[t]:
        kinds[tuple(sorted((d[i]['kind'], d[j]['kind'])))] += 1
        if d[i]['kind'] == 'C' == d[j]['kind'] and xedges(d[i]) is not None and xedges(d[j]) is not None:
            Xj = aligned(j, orders[j][0])
            sameX['same X' if any(aligned(i, o) == Xj for o in orders[i]) else 'different X'] += 1
print('degree-edit pairs by reducibility kind', dict(kinds))
print('C-C degree-edit pairs: contraction set', dict(sameX))
comp, sizes = components(633, [E['deg1'], E['degk']])
fam = []
for v in sorted(comp.values(), key=len, reverse=True)[:10]:
    Xs = set()
    o0 = None
    for i in v:
        if xedges(d[i]) is None: continue
        Xs.add(min(tuple(sorted(tuple(sorted(e)) for e in aligned(i, o))) for o in orders[i]))
    fam.append((len(v), dict(C.Counter(d[i]['kind'] for i in v)), 'distinct aligned X among I-I C members:', len(Xs)))
for f in fam: print(f)
json.dump(dict(kinds={'-'.join(k): x for k, x in kinds.items()}, sameX=dict(sameX), top10=fam), open('res5probe.json', 'w'), indent=1)
