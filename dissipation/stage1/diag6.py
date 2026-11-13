import pickle, numpy as np, lp2, net2 as N2, collections
B = pickle.load(open('cache_B2.pkl', 'rb')); A7, A6 = B['A7'], B['A6']
s = lp2.solve(B, np.zeros((A7['n'], 7)), np.zeros((A6['n'], 6)), np.zeros(A7['n'], bool), np.zeros(A6['n'], bool), verbose=False)
Pf = np.concatenate([s['P'], [0]]); t = s['t']
c7 = -60 + Pf[A7['IN']].max(2).sum(1); c6 = Pf[A6['IN']].max(2).sum(1) - Pf[A6['OUT']].sum(1); f5 = 60 - Pf[B['P5']].sum(1)
b7 = np.flatnonzero(~A7['excused'] & (c7 > t - 1e-6)); b6 = np.flatnonzero(~A6['excused'] & (c6 > t - 1e-6)); b5 = np.flatnonzero(f5 > t - 1e-6)
print('t %.4f; binding 7-rows %d, 6-rows %d, 5-rows %d' % (t, len(b7), len(b6), len(b5)))
print(' 7 links:', collections.Counter(B['R7'][i][0] for i in b7).most_common(8))
print(' 7-rows with a 6/7 target among binding:', int(((A7['tgt2'][b7] >= 0).any(1)).sum()))
print(' 6 links:', collections.Counter(B['R6'][i][0] for i in b6).most_common(8))
print(' 6-rows with a 7 neighbour among binding:', int(((A6['tgt3'][b6] >= 0).any(1)).sum()))
print(' 5 links:', [B['W5'][i] for i in b5])
# lower bound check: 5- and 6-rows alone, and 7-rows alone
for name, ex7, ex6 in (('5+6 rows only', True, False), ('5+7 rows only', False, True)):
    B2 = dict(B); B2['A7'] = dict(A7); B2['A6'] = dict(A6)
    if ex7: B2['A7']['excused'] = np.ones(A7['n'], bool)
    if ex6: B2['A6']['excused'] = np.ones(A6['n'], bool)
    s2 = lp2.solve(B2, np.zeros((A7['n'], 7)), np.zeros((A6['n'], 6)), np.zeros(A7['n'], bool), np.zeros(A6['n'], bool), verbose=False)
    print('%s: t = %.4f' % (name, s2['t']))
