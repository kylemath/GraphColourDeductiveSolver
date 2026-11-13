import sys, pickle, numpy as np
sys.argv = ['wide.py', 'all4.pkl']  # reuse feature code on one file for a quick test set
src = open('wide.py').read().split("def fit(")[0].replace("def is_test(r):\n    if r['src'] == 'random': return r['file'] == files[-1]", "def is_test(r):\n    if r['src'] == 'random': return True")
exec(src)
res = pickle.load(open('wide_model.pkl', 'rb'))
def pred(classes, W, X):
    out = np.empty(len(X), np.int64)
    for s in range(0, len(X), 4096): out[s:s + 4096] = classes[W[:, X[s:s + 4096]].sum(2).argmax(0)]
    return out
for k, name in enumerate(('RSST push', 'added push', 'tunnel')):
    cl, W = res[name]; mag = np.sort(np.abs(W).ravel())[::-1]
    for K in (None, 8000, 4000, 2000, 1000, 500, 200):
        Wk = W if K is None else np.where(np.abs(W) >= max(mag[K - 1], 1), W, 0)
        p = pred(cl, Wk, Xte); ok = p == Yte[:, k]; nz = Yte[:, k] != 0
        print('%-11s weights %6d  edge exact %.4f  non-zero edges %.3f' % (name, int((Wk != 0).sum()), ok.mean(), ok[nz].mean()), flush=True)
