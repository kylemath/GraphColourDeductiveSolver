import pickle, numpy as np, torch, time, sys, lp, train as TR
B = pickle.load(open('cache_B.pkl', 'rb')); N = B['N']
s0 = lp.solve(B, np.zeros((N, 7)), np.zeros(N, bool), verbose=False)
dev = sys.argv[1] if len(sys.argv) > 1 else 'cpu'; steps = int(sys.argv[2]) if len(sys.argv) > 2 else 300
t = time.time()
best = TR.train(B, s0['P'], s0['t'], steps=steps, dev=dev)
print('device %s, %d steps in %.0fs, best soft max %.4f' % (dev, steps, time.time() - t, best[0]))
pickle.dump(best, open('soft_%s_%d.pkl' % (dev, steps), 'wb'))
