# one worker: python3 grid2.py MODE ARG ; MODE theta: ARG = "th7,th6" uniform shares; MODE rand: ARG = seed (random integer attention)
import pickle, sys, json, numpy as np, lp3 as lp2, net3 as N2, time
B = pickle.load(open('cache_B3.pkl', 'rb')); A7, A6 = B['A7'], B['A6']
mode, arg = sys.argv[1], sys.argv[2]
def hard(tgt, F, W, m):
    inS, k = N2.shares_int(tgt, F, W, m); return inS / k[:, None]
if mode == 'theta':
    th7, th6 = [float(x) for x in arg.split(',')]; fix = dict(th7=th7, th6=th6)
    W2 = np.zeros(B['F2'].shape[1], int); W3 = np.zeros(B['F3'].shape[1], int); m2 = m3 = 0
elif mode == 'mut':
    f, sd, rate = arg.split(':'); Pa = pickle.load(open(f, 'rb')); rng = np.random.default_rng(int(sd))
    def mut(W):
        W = W.copy(); k = rng.random(len(W)) < float(rate); W[k] = rng.integers(-3, 4, int(k.sum())); return W
    W2, W3 = mut(Pa['W2']), mut(Pa['W3']); m2, m3 = Pa['m2'], Pa['m3']
    if rng.random() < 0.25: m2 = int(rng.integers(0, 4))
    if rng.random() < 0.25: m3 = int(rng.integers(0, 4))
    fix = None
elif mode == 'soft':
    f, m = arg.split(':'); S = pickle.load(open(f, 'rb'))[1]
    q = lambda W: np.round(W / max(np.abs(W).max(), 1e-12) * 7).astype(int)
    W2, W3 = q(S['W2']), q(S['W3']); m2 = m3 = int(m); fix = None
else:
    rng = np.random.default_rng(int(arg)); W2 = rng.integers(-3, 4, B['F2'].shape[1]); W3 = rng.integers(-3, 4, B['F3'].shape[1])
    m2, m3 = int(rng.integers(0, 4)), int(rng.integers(0, 4)); fix = None
sh2 = hard(A7['tgt2'], B['F2'], W2, m2); sh3 = hard(A6['tgt3'], B['F3'], W3, m3)
own7 = np.ones(A7['n'], bool); own6 = np.ones(A6['n'], bool); hist = []
for it in range(5):
    s = lp2.solve(B, sh2, sh3, own7, own6, fix=fix, verbose=False)
    if s is None: hist.append(None); break
    hist.append(s['t'])
    Pf = np.concatenate([s['P'], [0]]); c7 = -60 + Pf[A7['IN']].max(2).sum(1)
    c6 = Pf[A6['IN']].max(2).sum(1) - Pf[A6['OUT']].sum(1) + np.where(A6['r2v'] >= 0, s['M2'][np.maximum(A6['r2v'], 0)], 0).sum(1)
    n7, n6 = c7 >= s['th7'] - 1e-9, c6 >= s['th6'] - 1e-9
    if (n7 == own7).all() and (n6 == own6).all(): break
    own7, own6 = n7, n6
best = min(h for h in hist if h is not None) if any(h is not None for h in hist) else None
print(json.dumps(dict(mode=mode, arg=arg, t=best, hist=hist, th7=s['th7'] if s else None, th6=s['th6'] if s else None)), flush=True)
if mode == 'rand' or True: pickle.dump(dict(W2=W2, W3=W3, m2=m2, m3=m3, sol=s, own7=own7, own6=own6), open('runs3/%s_%s.pkl' % (mode, arg.replace(',', '_').replace('/', '_').replace(':', '_')), 'wb'))
