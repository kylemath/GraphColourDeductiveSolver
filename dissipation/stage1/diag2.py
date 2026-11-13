import pickle, numpy as np, lp, net as NT
B = pickle.load(open('cache_B.pkl', 'rb')); N = B['N']
# (a) 5/6 rows only: excuse every 7-row
B2 = dict(B); B2['excused'] = np.ones(N, bool)
s = lp.solve(B2, np.zeros((N, 7)), np.zeros(N, bool), verbose=False); print('5- and 6-rows alone: t = %.4f' % s['t'])
# (b) forward but M forced to its value -- how much of t comes from incoming forwards? uniform shares, own=theta for c1>=theta
U = B['is7'] / np.maximum(B['is7'].sum(1, keepdims=True), 1)
s = lp.solve(B, U, np.ones(N, bool), verbose=False)
Pf = np.concatenate([s['P'], [0]]); c1 = -60 + Pf[B['P7']].max(2).sum(1)
own = c1 >= s['theta']; s = lp.solve(B, U, own, verbose=False)
Pf = np.concatenate([s['P'], [0]]); c1 = -60 + Pf[B['P7']].max(2).sum(1)
f5 = 60 - Pf[B['P5']].sum(1); f6 = -Pf[B['O6']].sum(1) + Pf[B['I6']].max(2).sum(1)
M = s['M']; inc = np.where(B['is7'], M[np.where(B['is7'], B['vX'], 0)], 0).sum(1)
fin = np.where(B['has7'], np.minimum(c1, s['theta']), c1) + inc
live = ~B['excused']; t = s['t']
print('uniform: t %.4f theta %.4f; binding 7-rows %d, 5-rows %d, 6-rows %d' % (t, s['theta'], int((live & (fin > t - 1e-6)).sum()), int((f5 > t - 1e-6).sum()), int((f6 > t - 1e-6).sum())))
print('M stats: max %.2f, mean %.2f, nonzero %d / %d' % (M.max(), M.mean(), int((M > 1e-9).sum()), len(M)))
o = np.argsort(-np.where(live, fin, -999))[:5]
for i in o: print('  ', B['R7'][i], 'c1 %.2f inc %.2f fin %.2f' % (c1[i], inc[i], fin[i]))
print('surplus rows (c1 > theta):', int((c1 > s['theta'] + 1e-9).sum()), ' max c1 %.2f' % c1.max())
