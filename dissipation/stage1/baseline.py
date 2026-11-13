import pickle, numpy as np, lp, net as NT
B = pickle.load(open('cache_B.pkl', 'rb')); N = B['N']
z = np.zeros((N, 7))
print('round 1 only (no forward):'); s0 = lp.solve(B, z, np.zeros(N, bool)); print('   max final %.4f charge units = %.6f t-units' % (s0['t'], s0['t'] / 60))
U = B['is7'] / np.maximum(B['is7'].sum(1, keepdims=True), 1)
own = np.ones(N, bool)
for it in range(4):
    s = lp.solve(B, U, own); print('uniform forward, iter %d: t = %.4f (%.6f t-units), theta = %.3f' % (it, s['t'], s['t'] / 60, s['theta']))
    Pf = np.concatenate([s['P'], [0]]); c1 = -60 + Pf[B['P7']].max(2).sum(1)
    new = c1 >= s['theta']
    print('   rows choosing theta: %d -> %d' % (own.sum(), new.sum()))
    if (new == own).all(): break
    own = new
