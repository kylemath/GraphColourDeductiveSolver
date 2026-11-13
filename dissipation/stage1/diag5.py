import pickle, numpy as np, lp, harden as H, collections, net as NT
B = pickle.load(open('cache_B.pkl', 'rb')); N = B['N']
U = B['is7'] / np.maximum(B['is7'].sum(1, keepdims=True), 1)
t, th, s = H.best_lp(B, U, [10.0])
Pf = np.concatenate([s['P'], [0]]); c1 = -60 + Pf[B['P7']].max(2).sum(1)
sur = np.maximum(c1 - th, 0) * B['has7']
d = s['res'].ineqlin.marginals
M = s['M']; inc = np.where(B['is7'], M[np.where(B['is7'], B['vX'], 0)], 0).sum(1)
own = np.where(B['has7'], np.minimum(c1, th), c1); fin = own + inc; live = ~B['excused']
b7 = np.flatnonzero(live & (fin > t - 1e-6))
used = sorted({int(v) for i in b7 for v in B['vX'][i][B['is7'][i]] if M[v] > 1e-9})
n7 = B['is7'].sum(1)
for v in used:
    e = np.flatnonzero(B['sview'] == v); r = B['srow'][e]; val = sur[r] * U[r, B['sslot'][e]]
    k = e[np.argmax(val)]; rr = B['srow'][k]
    print('view %d M=%.3f: arg-max neighbour row %s, its #7-neighbours %d, surplus %.3f; neighbour rows with share 1 that reach M: %d' % (v, M[v], B['R7'][rr], n7[rr], sur[rr], int(((n7[r] == 1) & (sur[r] >= M[v] - 1e-6)).sum())))
rng = np.random.default_rng(0); res = []
for k in range(20):
    W = rng.integers(-3, 4, B['F'].shape[1]); m = int(rng.integers(0, 4))
    tt, th2, _ = H.best_lp(B, H.hard_shares(B, W, m), [6.0, 10.0])
    res.append(tt)
print('20 random integer attentions: LP t min %.4f median %.4f' % (min(res), np.median(res)))
