import pickle, time, numpy as np, rows as RW, net2 as N2
t = time.time(); D = RW.load(); R6 = N2.rows6(D['W6'])
B = N2.build(D['R7'], R6, D['W5']); B['meta'] = dict(pkl_md5=D['pkl_md5'])
pickle.dump(B, open('cache_B2.pkl', 'wb'))
A7, A6 = B['A7'], B['A6']
print('built %.1fs: 7-rows %d (excused %d), 6-rows %d (excused %d), 5-rows %d' % (time.time() - t, A7['n'], A7['excused'].sum(), A6['n'], A6['excused'].sum(), len(D['W5'])))
print('views R2 %d, R3 %d; sender entries R2 %d, R3 %d; contexts R2 %d, R3 %d; features %d; push params %d' % (B['nV2'], B['nV3'], len(A7['src']), len(A6['src']), len(B['F2']), len(B['F3']), B['F2'].shape[1], N2.NPAR))
t = time.time(); E = N2.exact(B, np.zeros(N2.NPAR, int), 0, 0, np.zeros(B['F2'].shape[1], int), 0, np.zeros(B['F3'].shape[1], int), 0); print('exact eval %.0f ms' % ((time.time() - t) * 1000))
