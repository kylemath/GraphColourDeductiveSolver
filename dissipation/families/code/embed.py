import sys, random, json, collections as C, numpy as np
sys.path.insert(0, 'code')
from parts import parse
from mir import mirror
sc, P = parse('data/synth_rules_588.txt'); T = 2
def canon(p):
    s = p['slots']; return min(s, mirror(p, T, 1, 'with_spoke'))
cls = {}
for p in P: cls.setdefault((p['pre'], p['hub'], p['w'], canon(p)), p)
Q = [dict(pre=k[0], hub=k[1], w=k[2], slots=k[3]) for k in cls]
OFF = range(-3, 4)  # slot offsets from target that exist for hubs 5..8 (wrap)
def feat(p):
    h = p['hub']; f = []
    f += [h == x for x in (5, 6, 7, 8)]; f += [p['w'] / 6]
    for o in OFF:
        if abs(o) > h // 2 or (o == h // 2 and h % 2 == 0 and o < 0):
            f += [0] * 17; continue
        s = p['slots'][(T + o) % h]
        f += [s[0] <= d <= s[1] for d in (5, 6, 7, 8, 9)]           # spoke allowed degrees
        f += [s[2] <= d <= s[3] for d in (5, 6, 7, 8, 9)]           # hat allowed degrees
        fans = s[4]; f += [len(fans) / 3]
        f += [sum(lo <= d <= hi for lo, hi in fans) / 3 for d in (5, 6, 7, 8, 9)]
        f += [(s[1] - s[0]) == 4]
    return np.array(f, float)
def null(rng):
    pos = C.defaultdict(list)
    for p in Q:
        for r, s in enumerate(p['slots']): pos[(p['pre'], p['hub'], r)].append(s)
    return [dict(p, slots=tuple(p['slots'][r] if r == T else rng.choice(pos[(p['pre'], p['hub'], r)]) for r in range(p['hub']))) for p in Q]
def kmeans(X, k, rng, it=60):
    best = None
    for rep in range(4):
        c = X[rng.sample(range(len(X)), k)]
        for _ in range(it):
            d = ((X[:, None] - c[None]) ** 2).sum(-1); a = d.argmin(1)
            c = np.array([X[a == j].mean(0) if (a == j).any() else c[j] for j in range(k)])
        sse = d.min(1).sum()
        if best is None or sse < best[0]: best = (sse, a)
    return best[1]
def silhouette(X, a):
    D = np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1)); s = []
    for i in range(len(X)):
        same = a == a[i]; same[i] = False
        if not same.any(): s.append(0); continue
        A = D[i, same].mean(); B = min(D[i, a == j].mean() for j in set(a) if j != a[i])
        s.append((B - A) / max(A, B))
    return float(np.mean(s))
def analyse(parts, rng):
    X = np.array([feat(p) for p in parts]); X = X - X.mean(0)
    sv = np.linalg.svd(X, compute_uv=False); v = sv ** 2 / (sv ** 2).sum(); cv = np.cumsum(v)
    D = np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1)); np.fill_diagonal(D, np.inf)
    out = dict(n=len(parts), dim=X.shape[1], pc1=round(v[0], 3), pc1_3=round(cv[2], 3), k90=int((cv < .9).sum() + 1),
               nn_dist_median=round(float(np.median(D.min(1))), 3), exact_dupes=int((D.min(1) == 0).sum()))
    for k in (5, 10, 20, 40):
        out[f'sil_k{k}'] = round(silhouette(X, kmeans(X, k, rng)), 3)
    return out, X
rng = random.Random(1)
real, X = analyse(Q, rng)
nulls = [analyse(null(random.Random(100 + i)), rng)[0] for i in range(10)]
print('real', real)
for key in real:
    v = [n[key] for n in nulls]; print(f'  {key}: real {real[key]}  null {np.mean(v):.3f} ± {np.std(v):.3f}')
# interpret top PCs
U, S, Vt = np.linalg.svd(X, full_matrices=False)
names = ['hub5', 'hub6', 'hub7', 'hub8', 'w']
for o in OFF:
    names += [f's{o:+d}_sp{d}' for d in range(5, 10)] + [f's{o:+d}_hat{d}' for d in range(5, 10)] + [f's{o:+d}_nfan'] + [f's{o:+d}_fan{d}' for d in range(5, 10)] + [f's{o:+d}_free']
for i in range(4):
    idx = np.argsort(-np.abs(Vt[i]))[:6]
    print(f'PC{i+1}', [(names[j], round(Vt[i, j], 2)) for j in idx])
a = kmeans(X, 10, rng)
for j in range(10):
    m = [Q[i] for i in range(len(Q)) if a[i] == j]
    print('cluster', j, len(m), dict(C.Counter((p['pre'], p['hub'], p['w']) for p in m).most_common(3)))
json.dump(dict(real=real, nulls=nulls), open('res_embed.json', 'w'), indent=1)
