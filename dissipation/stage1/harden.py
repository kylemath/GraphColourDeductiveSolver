# Harden: integer attention weights (few bits, ranked by magnitude), hard top-within-margin shares, exact LP for (P, theta)
# over a theta grid with own-term alternation, prune weights by rounded magnitude, then snap P to multiples of 3 and polish
# with integer coordinate moves on the EXACT evaluator.
import numpy as np, scipy.optimize as so, lp, net as NT, time

def hard_shares(B, Wint, margin):
    sc_ctx = B['F'].astype(np.int64) @ np.asarray(Wint, dtype=np.int64)
    sc = np.where(B['is7'], sc_ctx[np.where(B['is7'], B['cX'], 0)], np.iinfo(np.int64).min // 4)
    mx = sc.max(1, keepdims=True); inS = B['is7'] & (sc >= mx - margin)
    return inS / np.maximum(inS.sum(1, keepdims=True), 1)

def lp_fixed_theta(B, shares, th, own, **kw):
    orig = so.linprog
    def lp2(c, A_ub=None, b_ub=None, bounds=None, method=None):
        bounds = list(bounds); bounds[1] = (th, th); return orig(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method=method)
    lp.linprog = lp2
    try: return lp.solve(B, shares, own, verbose=False, **kw)
    finally: lp.linprog = orig

def best_lp(B, shares, thetas, iters=6):
    """min over theta in the grid of the LP value with own-term alternation. Returns (t, theta, sol)."""
    best = (1e9, None, None); N = B['N']
    for th in thetas:
        own = np.ones(N, bool); s = None
        for it in range(iters):
            s2 = lp_fixed_theta(B, shares, th, own)
            if s2 is None: break
            s = s2
            Pf = np.concatenate([s['P'], [0]]); c1 = -60 + Pf[B['P7']].max(2).sum(1)
            new = c1 >= th - 1e-9
            if (new == own).all(): break
            own = new
        if s is not None and s['t'] < best[0]: best = (s['t'], th, s)
    return best

def quantise(W, bits=3):
    """integer weights with |w| <= 2^bits - 1, keeping the ranking by magnitude."""
    W = np.asarray(W, dtype=np.float64); m = np.abs(W).max()
    if m == 0: return np.zeros(len(W), dtype=np.int64)
    return np.round(W / m * (2 ** bits - 1)).astype(np.int64)

def exact_max(B, P, theta, Wint, margin):
    E = NT.exact(B, P, theta, Wint, margin)
    live = ~B['excused']
    f = np.concatenate([E['f7'][live], E['f5'], E['f6']])
    return f.max(), E

def polish_P(B, P, theta, Wint, margin, step=3, rounds=4, log=print):
    """integer coordinate descent on P (multiples of 3) and theta on the exact evaluator: objective (max, #rows at max)."""
    live = ~B['excused']
    def obj(P, th):
        E = NT.exact(B, P, th, Wint, margin); f = np.concatenate([E['f7'][live], E['f5'], E['f6']]); m = f.max()
        return (int(m), int((f == m).sum()))
    cur = obj(P, theta); P = P.copy()
    for rd in range(rounds):
        improved = False
        for i in range(NT.NPAR):
            for d in (step, -step):
                if P[i] + d < 0: continue
                P[i] += d; o = obj(P, theta)
                if o < cur: cur = o; improved = True; break
                P[i] -= d
        for d in (1, -1, 3, -3):
            o = obj(P, theta + d)
            if o < cur: cur = o; theta += d; improved = True
        log('    polish round %d: exact max %d/%d = %.4f units, %d rows at max' % (rd, cur[0], NT.SCALE, cur[0] / NT.SCALE, cur[1]))
        if not improved: break
    return P, theta, cur
