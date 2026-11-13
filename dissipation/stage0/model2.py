"""Diagnostic: same task with dense integer matrices; optional pair features (degree 2) and left/right features.
usage: python3 model2.py DATA.pkl MODE   MODE in lin | pair | lr | lrpair"""
import sys, pickle, random, collections as C, numpy as np
import model as M0
from behav import npriv
VAL = [5, 6, 7, 8, 9]
def lr_feats(r):
    """unsymmetrised: one-hot of degrees at fixed relative positions; returns two versions (as is, mirrored)."""
    d, link, asg = r['d'], r['link'], r['asg']; outs = []
    for sgn in (1, -1):
        rowsf = []
        for i in range(d):
            v = []
            def oh(x): return [int(x == t) for t in VAL]
            for o in (0, 1, -1, 2, -2, 3, -3): v += oh(link[(i + sgn * o) % d])
            hl, hr = asg[100 + (i - 1) % d], asg[100 + i]
            if sgn < 0: hl, hr = hr, hl
            v += oh(hl) + oh(hr)
            # hats one further out
            h2l, h2r = asg[100 + (i - 2) % d], asg[100 + (i + 1) % d]
            if sgn < 0: h2l, h2r = h2r, h2l
            v += oh(h2l) + oh(h2r)
            fans = [asg[200 + 3 * i + j] for j in range(npriv(link[i]))]
            if sgn < 0: fans = fans[::-1]
            for j in range(3): v += oh(fans[j]) if j < len(fans) else [0] * 5
            e = r['et'][i]
            v += [int(e is None)] + [int(e is not None and e < t) for t in (0, -12, -24, -36, -48, -60)]
            v += [int(d == 8)]
            rowsf.append(v)
        outs.append(np.array(rowsf, np.int32))
    return outs
def dense(X, mode):
    out = []
    for fam, fs, y, r in X:
        if mode.startswith('lr'):
            A, B = lr_feats(r)
        else:
            A = np.array([[(m >> k) & 1 for k in range(M0.NF - 1)] for m in fs], np.int32); B = None
        def exp(A):
            if not mode.endswith('pair'): return A
            n = A.shape[1]; iu = np.triu_indices(n, 1)
            return np.concatenate([A, A[:, iu[0]] * A[:, iu[1]]], 1)
        out.append((fam, exp(A), None if B is None else exp(B), np.array(y)))
    return out
def alloc(base, units, g):
    got = np.zeros(len(base), np.int64)
    for u in range(units):
        got[int(np.argmax(base + g * got))] += 1
    return got
def train(D, epochs=25, seed=0):
    F = D[0][1].shape[1]; w = np.zeros(F, np.int64); g = 0; aw = np.zeros(F, np.float64); ag = 0.0; rng = random.Random(seed); n = 0
    for ep in range(epochs):
        order = list(range(len(D))); rng.shuffle(order)
        for k in order:
            fam, A, B, y = D[k]
            for (Af, yf) in ((A, y),) + (((B, y),) if B is not None else ()):
                p = alloc(Af @ w, int(y.sum()), g)
                if not np.array_equal(p, yf):
                    w += (yf - p) @ Af
                    g += int((yf * (yf - 1) // 2).sum() - (p * (p - 1) // 2).sum())
            aw += w; ag += g; n += 1
    return aw / n, ag / n
def ev(D, w, g):
    return float(np.mean([np.array_equal(alloc(A @ w, int(y.sum()), g), y) for _, A, B, y in D]))
if __name__ == '__main__':
    rows = pickle.load(open(sys.argv[1], 'rb')); X = M0.prep(rows); mode = sys.argv[2]
    D = dense(X, mode)
    fam = sorted({x[0] for x in D}); random.Random(1).shuffle(fam); f = {t: i % 5 for i, t in enumerate(fam)}
    te_acc = []; tr_acc = []
    for j in range(5):
        tr = [x for x in D if f[x[0]] != j]; te = [x for x in D if f[x[0]] == j]
        w, g = train(tr); te_acc.append(ev(te, w, g)); tr_acc.append(ev(tr, w, g))
    print(sys.argv[1], mode, 'features', D[0][1].shape[1], 'train %.3f  held-out %.3f' % (np.mean(tr_acc), np.mean(te_acc)), flush=True)
