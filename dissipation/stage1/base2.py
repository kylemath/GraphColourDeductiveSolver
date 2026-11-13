import pickle, numpy as np, lp2, net2 as N2, time, sys
B = pickle.load(open('cache_B2.pkl', 'rb')); A7, A6 = B['A7'], B['A6']
z7 = np.zeros((A7['n'], 7)); z6 = np.zeros((A6['n'], 6))
print('R1 only (hat-aware pushes):'); s = lp2.solve(B, z7, z6, np.zeros(A7['n'], bool), np.zeros(A6['n'], bool))
u2 = (A7['tgt2'] >= 0) / np.maximum((A7['tgt2'] >= 0).sum(1, keepdims=True), 1)
u3 = (A6['tgt3'] >= 0) / np.maximum((A6['tgt3'] >= 0).sum(1, keepdims=True), 1)
print('R1 + R2 uniform (no R3):'); s = lp2.solve(B, u2, z6, np.ones(A7['n'], bool), np.zeros(A6['n'], bool))
print('R1 + R2 + R3 uniform, thetas free:'); s = lp2.solve(B, u2, u3, np.ones(A7['n'], bool), np.ones(A6['n'], bool))
print('   th7 %.3f th6 %.3f' % (s['th7'], s['th6']))
