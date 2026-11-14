"""Idea F: edge transfer laws for the TOTAL expected net charge into a receiver (all 604 parts summed).
 L0  potential/degree law: net(d, w) = sum_i a(d, w_i), a antisymmetric  (10 parameters)
 L1  diamond law: net = sum_i g(d, w_i, {w_{i-1}, w_{i+1}}), g antisymmetric in (d, w_i)  (150 parameters)
 L1u same without antisymmetry (375 parameters)
R^2 is orbit-weighted over all receiver classes; also split by template."""
import numpy as np, itertools, collections as C
from common import *
P = load(); pre = np.array([p['pre'][:2] for p in P])
A = np.load('../real58.npz'); B = np.load('../real911.npz')
rows = []; Y = {t: [] for t in ('all', 'dr', 'SP', 'ST')}; wt = []
for z, ds in ((A, (5, 6, 7, 8)), (B, (9, 10, 11))):
    for d in ds:
        M = z[f'M{d}'].astype(float); O = z[f'O{d}'].astype(float)
        for w, o in zip(z[f'W{d}'], O): rows.append((d, tuple(int(x) for x in w))); wt.append(o / O.sum())
        Y['all'].append(M.sum(1))
        for t in ('dr', 'SP', 'ST'): Y[t].append(M[:, pre == t].sum(1))
Y = {k: np.concatenate(v) for k, v in Y.items()}; wt = np.array(wt)
e = {k: float((wt * v * v).sum()) for k, v in Y.items()}
print('weighted energy of summed behaviour by template:', {k: f'{v:.4g}' for k, v in e.items()})
pairs = [(a, b) for a in range(5, 10) for b in range(a, 10)]
def feats(kind):
    idx = {}; X = np.zeros((len(rows), 400), np.float32)
    def col(k):
        if k not in idx: idx[k] = len(idx)
        return idx[k]
    for r, (d, w) in enumerate(rows):
        dd = min(d, 9); n = len(w)
        for i in range(n):
            x = w[i]; ctx = tuple(sorted((w[i - 1], w[(i + 1) % n])))
            if kind == 'L0':
                if x != dd: X[r, col((min(dd, x), max(dd, x)))] += 1 if dd < x else -1
            elif kind == 'L1':
                if x != dd: X[r, col((min(dd, x), max(dd, x), ctx))] += 1 if dd < x else -1
            else: X[r, col((dd, x, ctx))] += 1
    return X[:, :len(idx)], idx
for kind in ('L0', 'L1', 'L1u'):
    X, idx = feats(kind); sw = np.sqrt(wt)[:, None]
    out = {}
    for t in ('all', 'dr', 'SP', 'ST'):
        y = Y[t]; b, *_ = np.linalg.lstsq(X * sw, y * sw[:, 0], rcond=None)
        res = y - X @ b; out[t] = 1 - (wt * res * res).sum() / (wt * y * y).sum()
        if t == 'all':
            D = np.array([r[0] for r in rows]); per = {d: round(float(1 - (wt[D == d] * res[D == d] ** 2).sum() / (wt[D == d] * y[D == d] ** 2).sum()), 3) for d in range(5, 12)}
            if kind == 'L0': print('  L0 coefficients a(lo,hi) = charge from lo-degree to hi-degree vertex per edge:', {k: round(float(b[v]), 2) for k, v in idx.items()})
    print(kind, 'params', X.shape[1], 'R2 (uncentred):', {k: round(float(v), 4) for k, v in out.items()}, ' by receiver degree (all):', per)
