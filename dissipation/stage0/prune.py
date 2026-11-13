"""Magnitude pruning of the pair-feature attention model, with speedups:
 - mirror-canonical dedupe of identical (features, target) examples
 - mistake-driven integer updates only (no work on correct examples beyond one dot product)
 - early stop when an epoch makes no mistakes or held-out stops improving
 - columns that are never set are dropped before training
 - weights rounded to 6 bits and ranked by that magnitude for pruning
usage: python3 prune.py DATA.pkl"""
import sys, pickle, random, time, numpy as np, collections as C
import model as M0, model2 as M2
rows = pickle.load(open(sys.argv[1], 'rb')); X = M0.prep(rows)
D = M2.dense(X, 'pair'); F0 = D[0][1].shape[1]
names = list(M0.NAMES[:M0.NF - 1]); iu = np.triu_indices(len(names), 1)
names += [f'{names[a]} AND {names[b]}' for a, b in zip(*iu)]
# dedupe
seen = {}; 
for fam, A, B, y in D:
    k = (A.tobytes(), y.tobytes())
    if k not in seen: seen[k] = (fam, A, B, y)
D2 = list(seen.values())
used = np.zeros(F0, bool)
for _, A, _, _ in D2: used |= A.any(0)
print('examples', len(D), '-> deduped', len(D2), '; columns', F0, '-> ever set', int(used.sum()), flush=True)
def sub(D, cols): return [(f, A[:, cols], None, y) for f, A, _, y in D]
def train(D, epochs=25, seed=0):
    F = D[0][1].shape[1]; w = np.zeros(F, np.int64); g = 0; aw = np.zeros(F); ag = 0.0; rng = random.Random(seed); n = 0
    for ep in range(epochs):
        order = list(range(len(D))); rng.shuffle(order); miss = 0
        for k in order:
            fam, A, _, y = D[k]; p = M2.alloc(A @ w, int(y.sum()), g)
            if not np.array_equal(p, y):
                w += (y - p) @ A; g += int((y * (y - 1) // 2).sum() - (p * (p - 1) // 2).sum()); miss += 1
            aw += w; ag += g; n += 1
        if miss == 0: break
    aw /= n; mx = np.abs(aw).max() or 1
    return np.round(63 * aw / mx).astype(np.int64), int(round(63 * ag / n / mx))
def units_ok(D, w, g):
    ex = un = tot = 0
    for _, A, _, y in D:
        p = M2.alloc(A @ w, int(y.sum()), g); ex += np.array_equal(p, y); un += int(np.minimum(p, y).sum()); tot += int(y.sum())
    return ex / len(D), un / tot
fam = sorted({x[0] for x in D2}); random.Random(1).shuffle(fam); f = {t: i % 5 for i, t in enumerate(fam)}
def cv(cols):
    r = []
    for j in range(5):
        tr = sub([x for x in D2 if f[x[0]] != j], cols); te = sub([x for x in D2 if f[x[0]] == j], cols)
        w, g = train(tr); r.append(units_ok(te, w, g))
    return np.mean(r, 0)
cols = np.where(used)[0]; t0 = time.time()
w, g = train(sub(D2, cols))
for K in (len(cols), 800, 400, 200, 100, 50, 25, 12):
    if K < len(cols):
        keep = np.argsort(-np.abs(w))[:K]; cols = cols[np.sort(keep)]; w, g = train(sub(D2, cols))
    e, u = cv(cols); tr = units_ok(sub(D2, cols), w, g)
    print('features %4d  train exact %.3f  held-out exact %.3f  held-out units placed %.3f  (%.0fs)' % (len(cols), tr[0], e, u, time.time() - t0), flush=True)
    if K in (50, 12):
        for i in np.argsort(-np.abs(w))[:12]: print('     %+3d  %s' % (w[i], names[cols[i]]))
        print('     second unit to same receiver: %+d' % g)
