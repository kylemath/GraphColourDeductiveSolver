"""Which state features predict 'the A5v 1212 run stops after this state'?  (INVARIANTS-1)
Usage: ml.py prefix.  Data: kind 'a5' runs (maximal); label 1 = last state of its run (end reason not None),
0 = state with a successor in the run.  Features: only those computable at state t (and t-1).
Single-feature threshold stumps (balanced accuracy) + numpy logistic regression (standardised)."""
import sys, json, gzip
import numpy as np
from collections import defaultdict, Counter

pref = sys.argv[1]
runs = defaultdict(list)
for l in gzip.open(pref + '_feat.jsonl.gz', 'rt'):
    r = json.loads(l)
    if r['kind'] == 'a5': runs[r['run']].append(r)
meta = {r['id']: r for r in json.load(gzip.open(pref + '_runs.json.gz', 'rt'))}
print('end reasons of maximal A5v runs:', Counter(meta[i]['end'] for i in runs).most_common())
print('start reasons:', Counter(meta[i]['start'] for i in runs).most_common())
print('end reason by run length:', sorted(Counter((len(s), meta[i]['end']) for i, s in runs.items()).items()))
F = ['nX', 'nY', 'xx', 'yy', 'xy', 'pX', 'vcross', 'xycross', 'f8planar', 'w', 'n', 'pXn', 'nXn', 'tpos']
X = []; y = []; grp = []
for i, s in runs.items():
    s.sort(key=lambda r: r['t'])
    for r in s:
        if r.get('w') is None: continue
        r['pXn'] = r['pX'] / max(1, r['nX'] - 1); r['nXn'] = r['nX'] / r['n']; r['tpos'] = r['t']
        X.append([float(r[f]) for f in F]); y.append(1 if r['t'] == len(s) - 1 else 0); grp.append(i)
X = np.array(X); y = np.array(y)
print('states', len(y), 'last', int(y.sum()))


def bal_acc(pred, y):
    tp = ((pred == 1) & (y == 1)).sum() / max(1, (y == 1).sum())
    tn = ((pred == 0) & (y == 0)).sum() / max(1, (y == 0).sum())
    return (tp + tn) / 2


res = []
for j, f in enumerate(F):
    best = (0.5, None, None)
    for th in np.unique(X[:, j]):
        for sgn in (1, -1):
            pred = (sgn * X[:, j] >= sgn * th).astype(int)
            b = bal_acc(pred, y)
            if b > best[0]: best = (b, th, sgn)
    res.append((best[0], f, best[1], best[2]))
print('single-feature stumps (balanced acc, feature, threshold, direction):')
for r in sorted(res, reverse=True): print('  %.3f %-9s th=%s dir=%s' % r)
# logistic regression (no tpos, to avoid the trivial length cue)
cols = [j for j, f in enumerate(F) if f not in ('tpos',)]
Z = X[:, cols]; mu = Z.mean(0); sd = Z.std(0) + 1e-9; Z = (Z - mu) / sd
Z = np.hstack([Z, np.ones((len(Z), 1))]); wv = np.zeros(Z.shape[1])
pw = (y == 0).sum() / max(1, (y == 1).sum()); sw = np.where(y == 1, pw, 1.0)
for it in range(3000):
    p = 1 / (1 + np.exp(-Z @ wv)); g = Z.T @ (sw * (p - y)) / len(y) + 1e-3 * wv
    wv -= 0.5 * g
p = 1 / (1 + np.exp(-Z @ wv))
print('logistic (class-weighted) balanced acc: %.3f' % bal_acc((p >= 0.5).astype(int), y))
for j, c in enumerate(cols): print('  coef %-9s %+.3f' % (F[c], wv[j]))
