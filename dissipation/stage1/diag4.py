import pickle, numpy as np, lp, harden as H, collections, net as NT
B = pickle.load(open('cache_B.pkl', 'rb')); N = B['N']
U = B['is7'] / np.maximum(B['is7'].sum(1, keepdims=True), 1)
t, th, s = H.best_lp(B, U, [10.0])
Pf = np.concatenate([s['P'], [0]]); c1 = -60 + Pf[B['P7']].max(2).sum(1)
M = s['M']; inc = np.where(B['is7'], M[np.where(B['is7'], B['vX'], 0)], 0).sum(1)
own = np.where(B['has7'], np.minimum(c1, th), c1); fin = own + inc; live = ~B['excused']
b7 = np.flatnonzero(live & (fin > t - 1e-6))
print('t %.4f theta %.1f; binding 7-rows %d' % (t, th, len(b7)))
print('binding 7-rows by (c1 > theta, incoming > 0):', collections.Counter((bool(c1[i] > th + 1e-9), bool(inc[i] > 1e-9)) for i in b7))
print('distinct link words among binding 7-rows:', collections.Counter(B['R7'][i][0] for i in b7).most_common(10))
print('max c1 over live 7-rows %.3f; rows with c1 > theta: %d' % (c1[live].max(), int((live & (c1 > th + 1e-9)).sum())))
print('push table (nonzero, rounded):')
names = {}
for du in (5, 6):
    for dv in (6, 7):
        for (x, y), p in sorted(NT.PAIR.items()):
            if x > y: continue
            for n5 in range(7):
                v = s['P'][NT.pidx(du, dv, x, y, n5)]
                if v > 1e-6: print('   %d->%d common {%d,%d} n5=%d : %.3f' % (du, dv, x, y, n5, v))
