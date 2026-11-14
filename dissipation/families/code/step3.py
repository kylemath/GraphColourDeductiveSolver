import json, sys, random, collections as C, statistics as st
sys.path.insert(0, 'code')
from canon import cfg_from_pool
from editgraph import build, components
d = json.load(open('data/pool_configs.json'))['configs']
R = [cfg_from_pool(c) for c in d[:633]]
L = C.defaultdict(set); D = C.defaultdict(C.Counter)
for line in open('data/stage1_ext_profile.jsonl'):
    r = json.loads(line)
    for k in r['kS']:
        L[k].add((r['d'], r['link'])); D[k][r['d']] += 1
res = build(R)
E = res['edges']
def jac(a, b):
    A, B = L[a], L[b]
    if not A or not B: return None
    return len(A & B) / len(A | B)
def dom(a): return D[a].most_common(1)[0][0] if D[a] else None
rng = random.Random(7)
idx = [i for i in range(633) if L[i]]
out = {}
def stats(pairs, label):
    js = [jac(a, b) for a, b in pairs]; js = [x for x in js if x is not None]
    sd = [dom(a) == dom(b) for a, b in pairs if dom(a) and dom(b)]
    out[label] = dict(pairs=len(js), mean_jac=round(st.mean(js), 4) if js else None,
                      frac_jac_pos=round(sum(1 for x in js if x > 0) / len(js), 3) if js else None,
                      frac_same_dom_degree=round(sum(sd) / len(sd), 3) if sd else None)
for t in ['deg1', 'degk', 'add1', 'mirror']:
    stats(sorted(E.get(t, ())), 'edge_' + t)
comp, sizes = components(633, [E['deg1'], E['degk']])
fam_pairs = [(a, b) for v in comp.values() if len(v) > 1 for i, a in enumerate(v) for b in v[i + 1:]]
stats(fam_pairs, 'same_degree_family')
shape_pairs = [(a, b) for v in res['by_shape'].values() for i, a in enumerate(v) for b in v[i + 1:]]
stats(shape_pairs, 'same_shape')
rp = [tuple(rng.sample(idx, 2)) for _ in range(20000)]
stats(rp, 'random_pairs')
bym = C.defaultdict(list)
for i in idx: bym[(R[i]['m'], d[i]['ring'])].append(i)
mp = []
for _ in range(20000):
    a = rng.choice(idx); g = bym[(R[a]['m'], d[a]['ring'])]
    if len(g) > 1:
        b = rng.choice(g)
        if b != a: mp.append((a, b))
stats(mp, 'random_pairs_same_m_ring')
# per-family coverage concentration for families of size >= 4
fams = []
for v in sorted(comp.values(), key=len, reverse=True):
    if len(v) < 4: break
    allL = C.Counter(); 
    for a in v: allL.update(L[a])
    dd = C.Counter(); 
    for a in v: dd.update(D[a])
    tot = sum(dd.values())
    names = [d[a]['name'] for a in v]
    fams.append(dict(size=len(v), m=sorted(C.Counter(R[a]['m'] for a in v).items()),
                     kinds=dict(C.Counter(d[a]['kind'] for a in v)),
                     hub_degree_share={k: round(x / tot, 3) for k, x in sorted(dd.items())} if tot else {},
                     n_link_types=len(allL), members_with_leaves=sum(1 for a in v if L[a]),
                     example=names[:6]))
out['families_ge4'] = fams
json.dump(out, open('res3.json', 'w'), indent=1)
for k, v in out.items():
    if k != 'families_ge4': print(k, v)
print(len(fams), 'families >= 4'); [print(f) for f in fams[:12]]
