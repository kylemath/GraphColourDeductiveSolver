import pickle, numpy as np, time, sys, lp, train as TR
B = pickle.load(open('cache_B.pkl', 'rb')); N = B['N']
s0 = lp.solve(B, np.zeros((N, 7)), np.zeros(N, bool), verbose=False)
seed = int(sys.argv[1]); steps = int(sys.argv[2]); l1 = float(sys.argv[3])
t = time.time(); best = TR.train(B, s0['P'], s0['t'], steps=steps, dev='cpu', seed=seed, l1=l1)
print('seed %d l1 %g: %d steps in %.0fs, best soft max %.4f' % (seed, l1, steps, time.time() - t, best[0]), flush=True)
pickle.dump(best, open('soft_s%d_%d.pkl' % (seed, steps), 'wb'))
