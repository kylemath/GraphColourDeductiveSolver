import sys, json, numpy as np, collections as C
sys.path.insert(0, 'code')
from parts import parse
from mir import mirror
sc, P = parse('data/synth_rules_588.txt')
key = lambda p: (p['pre'], p['hub'], p['w'], p['slots'])
def load(a, b):
    A, B = np.load(a), np.load(b)
    rows, Ms = [], []
    for z in (A, B):
        for d in (5, 6, 7, 8, 9, 10, 11):
            if f'M{d}' in z:
                Ms.append(z[f'M{d}']); rows += [(d, tuple(int(x) for x in w)) for w in z[f'W{d}']]
    return np.vstack(Ms).astype(np.float64), rows
def mirror_pairs(parts):
    idx = {}
    for k, p in enumerate(parts): idx.setdefault(key(p), []).append(k)
    used = set(); classes = []
    for k, p in enumerate(parts):
        if k in used: continue
        mk = [j for j in idx.get((p['pre'], p['hub'], p['w'], mirror(p, 2, 1, 'with_spoke')), []) if j not in used and j != k]
        grp = [k] + mk[:1]; used |= set(grp); classes.append(grp)
    return classes
def five_pattern(w):
    b = tuple(1 if x == 5 else 0 for x in w); d = len(b)
    return min(min(b[r:] + b[:r], tuple(reversed(b[r:] + b[:r]))) for r in range(d))
RES = {'link class (rotation+mirror)': lambda r: r,
       'where the 5s sit (5 vs not-5 pattern)': lambda r: (r[0], five_pattern(r[1])),
       'link degree multiset': lambda r: (r[0], tuple(sorted(r[1]))),
       'receiver degree only': lambda r: r[0]}
def group(M, rows, f):
    g = {}; 
    for i, r in enumerate(rows): g.setdefault(f(r), []).append(i)
    return np.vstack([M[ix].sum(0) for ix in g.values()]), len(g)
def metrics(X):
    n = X.shape[1]
    norms = np.linalg.norm(X, axis=0); live = norms > 1e-12
    Y = X[:, live] / norms[live]
    sv = np.linalg.svd(Y, compute_uv=False); e = np.cumsum(sv ** 2) / (sv ** 2).sum()
    G = Y.T @ Y
    # single-linkage clusters at cosine >= 0.99 and >= 0.9
    out = dict(classes=n, silent=int((~live).sum()), rank90=int((e < .9).sum() + 1), rank99=int((e < .99).sum() + 1))
    for th in (0.999, 0.99, 0.9):
        m = Y.shape[1]; par = list(range(m))
        def f(x):
            while par[x] != x: par[x] = par[par[x]]; x = par[x]
            return x
        ii, jj = np.where(np.triu(G, 1) >= th)
        for a, b in zip(ii, jj): par[f(a)] = f(b)
        out[f'groups_cos{th}'] = len({f(x) for x in range(m)})
    return out, Y
def run(real, nulls):
    res = {}
    for name, f in RES.items():
        rr = {}
        for lab, (a, b, parts) in [('real', real)] + [(f'null{i}', x) for i, x in enumerate(nulls)]:
            M, rows = load(a, b)
            cl = mirror_pairs(parts)
            Mc = np.stack([M[:, g].mean(1) for g in cl], 1)   # mirror symmetrised: one column per mirror class
            X, ng = group(Mc, rows, f)
            rr[lab], Y = metrics(X)
            rr[lab]['neighbourhood_groups'] = ng
            if lab == 'real': rr['_Y'] = (Y, cl)
        res[name] = rr
    return res
real = ('beh/real58.npz', 'beh/real911.npz', P)
import importlib; B = importlib.import_module('behav')
nulls = [(f'beh/null58_{s}.npz', f'beh/null911_{s}.npz', B.null_parts(P, s)) for s in (1, 2, 3)]
res = run(real, nulls)
out = {}
for name, rr in res.items():
    Y, cl = rr.pop('_Y')
    out[name] = rr
    print('==', name, 'groups:', rr['real']['neighbourhood_groups'])
    for k in rr['real']:
        nv = [rr[f'null{i}'][k] for i in range(3)]
        print(f'   {k:18s} real {rr["real"][k]:7}   null {np.mean(nv):8.1f} ({min(nv)}-{max(nv)})')
json.dump(out, open('res_behav.json', 'w'), indent=1)
