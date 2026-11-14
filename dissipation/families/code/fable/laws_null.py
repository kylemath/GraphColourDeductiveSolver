"""Same laws as laws.py on d=5..8 only, real vs slot-scrambled null rule sets (null58_*.npz made with behav.py --null)."""
import numpy as np, sys
def run(fn):
    A = np.load(fn); rows = []; y = []; wt = []
    for d in (5, 6, 7, 8):
        M = A[f'M{d}'].astype(float); O = A[f'O{d}'].astype(float)
        for w, o in zip(A[f'W{d}'], O): rows.append((d, tuple(int(x) for x in w))); wt.append(o / O.sum())
        y.append(M.sum(1))
    y = np.concatenate(y); wt = np.array(wt); out = {}
    for kind in ('L0', 'L1', 'L1u'):
        idx = {}; X = np.zeros((len(rows), 400), np.float32)
        for r, (d, w) in enumerate(rows):
            n = len(w)
            for i in range(n):
                x = w[i]; ctx = tuple(sorted((w[i - 1], w[(i + 1) % n])))
                if kind == 'L1u': k, s = (d, x, ctx), 1
                elif x == d: continue
                else: k, s = ((min(d, x), max(d, x)) + ((ctx,) if kind == 'L1' else ())), (1 if d < x else -1)
                X[r, idx.setdefault(k, len(idx))] += s
        X = X[:, :len(idx)]; sw = np.sqrt(wt)
        b, *_ = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None); res = y - X @ b
        out[kind] = (X.shape[1], round(float(1 - (wt * res ** 2).sum() / (wt * y ** 2).sum()), 4))
    return out
for fn in sys.argv[1:]: print(fn, run(fn))
