import pickle, time, numpy as np, rows as RW, net as NT, os
t = time.time(); D = RW.load(); B = NT.build(D['R7'], D['W5'], D['W6'])
B['excused'] = NT.excused_rows(B); B['meta'] = dict(pkl_md5=D['pkl_md5'], n7=len(D['R7']), n5=len(D['W5']), n6=len(D['W6']))
B['W5'] = D['W5']; B['W6'] = D['W6']; B['R7'] = D['R7']
pickle.dump(B, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache_B.pkl'), 'wb'))
print('built in %.1fs' % (time.time() - t))
print('views', B['nview'], 'src entries', len(B['srow']), 'contexts', len(B['ctxs']), 'features', B['F'].shape[1])
print('7-slots', int(B['is7'].sum()), 'rows with no 7 nbr', int((~B['has7']).sum()), 'excused (no admissible neighbour row fits a view)', int(B['excused'].sum()))
t = time.time()
for _ in range(10): E = NT.exact(B, np.zeros(NT.NPAR, int), 0, np.zeros(B['F'].shape[1], int), 0)
print('exact eval %.1f ms' % ((time.time() - t) * 100))
