import pickle, numpy as np, lp, net as NT, sys
from scipy.optimize import linprog
B = pickle.load(open('cache_B.pkl', 'rb')); N = B['N']
U = B['is7'] / np.maximum(B['is7'].sum(1, keepdims=True), 1)
def solve_theta(th, shares, own):
    # fix theta via bounds by monkeypatching solve's bounds: emulate with a tiny wrapper
    import scipy.optimize as so
    orig = so.linprog
    def lp2(c, A_ub=None, b_ub=None, bounds=None, method=None):
        bounds = list(bounds); bounds[1] = (th, th); return orig(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method=method)
    lp.linprog = lp2
    try: return lp.solve(B, shares, own, verbose=False)
    finally: lp.linprog = orig
for th in [float(x) for x in sys.argv[1:]]:
    own = np.ones(N, bool)
    for it in range(6):
        s = solve_theta(th, U, own)
        Pf = np.concatenate([s['P'], [0]]); c1 = -60 + Pf[B['P7']].max(2).sum(1)
        new = c1 >= th - 1e-9
        if (new == own).all(): break
        own = new | (own & False)
    print('theta %6.1f: t = %.4f (%.5f t-units) after %d own-term iterations, surplus rows %d' % (th, s['t'], s['t'] / 60, it + 1, int((c1 > th + 1e-9).sum())), flush=True)
