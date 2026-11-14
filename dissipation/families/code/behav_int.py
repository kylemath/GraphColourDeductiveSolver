import sys, numpy as np, collections as C
sys.path.insert(0, 'code')
exec(open('code/behav_an.py').read().split('def run(')[0])
M, rows = load('beh/real58.npz', 'beh/real911.npz')
cl = mirror_pairs(P)
Mc = np.stack([M[:, g].mean(1) for g in cl], 1)
tags = [P[g[0]]['tag'] for g in cl]
# duplicate groups on exact link classes
norms = np.linalg.norm(Mc, axis=0); Y = Mc / norms
G = Y.T @ Y
par = list(range(len(cl)))
def f(x):
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
for a, b in zip(*np.where(np.triu(G, 1) >= 0.999)): par[f(a)] = f(b)
grp = C.defaultdict(list)
for i in range(len(cl)): grp[f(i)].append(i)
big = sorted(grp.values(), key=len, reverse=True)
print('largest behaviour-duplicate groups (cos>=0.999):')
for g in big[:8]:
    print(len(g), [tags[i] for i in g][:8], 'weights', sorted({P[cl[i][0]]['w'] for i in g}), 'hubs', sorted({P[cl[i][0]]['hub'] for i in g}))
kinds = C.Counter()
for g in big:
    if len(g) > 1: kinds[tuple(sorted({P[cl[i][0]]['pre'] for i in g}))] += len(g) - 1
print('redundant members by template mix', dict(kinds))
# exact-equal vectors?
ex = C.Counter(tuple(np.round(Mc[:, i], 6)) for i in range(len(cl)))
print('exactly identical behaviour vectors: classes', len(cl), 'distinct', len(ex))
# factors at the 5-pattern resolution
X, ng = group(Mc, rows, lambda r: (r[0], five_pattern(r[1])))
keys = list({(r[0], five_pattern(r[1])): 0 for r in rows})
U, S, Vt = np.linalg.svd(X / np.linalg.norm(X, axis=0), full_matrices=False)
e = S ** 2 / (S ** 2).sum()
for k in range(4):
    top = np.argsort(-np.abs(U[:, k]))[:5]
    def show(t):
        d, b = keys[t]; return f"d{d}:" + ''.join('5' if x else '+' for x in b)
    tp = np.argsort(-np.abs(Vt[k]))[:5]
    print(f'factor {k+1} ({e[k]:.2f})', [(show(t), round(U[t, k], 2)) for t in top], '| parts', [tags[i] for i in tp])
