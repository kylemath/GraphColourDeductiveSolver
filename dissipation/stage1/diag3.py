import pickle, numpy as np, lp, collections
B = pickle.load(open('cache_B.pkl', 'rb')); N = B['N']
B2 = dict(B); B2['excused'] = B['excused'] | B['has7']
s = lp.solve(B2, np.zeros((N, 7)), np.zeros(N, bool), verbose=False)
print('5-rows + 6-rows + the %d live 7-rows with no 7 neighbour: t = %.6f = %s' % (int((~B2['excused']).sum()), s['t'], __import__('fractions').Fraction(s['t']).limit_denominator(1000)))
d = s['res'].ineqlin.marginals; print('binding constraints (dual != 0):', int((np.abs(d) > 1e-9).sum()))
Pf = np.concatenate([s['P'], [0]]); c1 = -60 + Pf[B['P7']].max(2).sum(1)
live = ~B2['excused']
for i in np.flatnonzero(live & (c1 > s['t'] - 1e-6))[:12]: print('  7-row', B['R7'][i], 'c1 %.3f' % c1[i])
f5 = 60 - Pf[B['P5']].sum(1); f6 = -Pf[B['O6']].sum(1) + Pf[B['I6']].max(2).sum(1)
print('  binding 5-links', [B['W5'][i] for i in np.flatnonzero(f5 > s['t'] - 1e-6)])
print('  binding 6-links', [B['W6'][i] for i in np.flatnonzero(f6 > s['t'] - 1e-6)])
