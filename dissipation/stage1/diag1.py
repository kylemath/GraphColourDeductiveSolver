import pickle, numpy as np, lp, net as NT, collections
B = pickle.load(open('cache_B.pkl', 'rb')); N = B['N']
s = lp.solve(B, np.zeros((N, 7)), np.zeros(N, bool), verbose=False)
d = s['res'].ineqlin.marginals
print('t', s['t'], 'nonzero duals', int((np.abs(d) > 1e-9).sum()))
Pf = np.concatenate([s['P'], [0]])
c1 = -60 + Pf[B['P7']].max(2).sum(1); live = ~B['excused']
f5 = 60 - Pf[B['P5']].sum(1); f6 = -Pf[B['O6']].sum(1) + Pf[B['I6']].max(2).sum(1)
print('5-rows at max:', [(B['W5'][i], round(f5[i], 2)) for i in np.argsort(-f5)[:6]])
print('6-rows at max:', [(B['W6'][i], round(f6[i], 2)) for i in np.argsort(-f6)[:6]])
o = np.argsort(-np.where(live, c1, -999))[:8]
print('7-rows at max:', [(B['R7'][i], round(c1[i], 2)) for i in o])
print('count of rows within 1e-6 of t:', int((np.where(live, c1, -999) > s['t'] - 1e-6).sum()), int((f5 > s['t'] - 1e-6).sum()), int((f6 > s['t'] - 1e-6).sum()))
