# usage: python3 run_harden.py soft.pkl OUT_TAG
import pickle, sys, time, json, numpy as np, harden as H, net as NT
B = pickle.load(open('cache_B.pkl', 'rb')); N = B['N']; T0 = time.time()
def log(*a): print(*a, '[%.0fs]' % (time.time() - T0), flush=True)
soft = pickle.load(open(sys.argv[1], 'rb')); tag = sys.argv[2]
Praw, th_soft, W, tau = soft[1]
log('soft: max %.4f theta %.2f' % (soft[0], th_soft))
thetas = sorted({float(round(th_soft + d)) for d in (-6, -3, 0, 3, 6)} | {0.0})
best = None
for bits in (2, 3, 4):
    Wq = H.quantise(W, bits)
    for m in (0, 1, 2) if bits < 4 else (0, 2, 4):
        t, th, s = H.best_lp(B, H.hard_shares(B, Wq, m), thetas)
        log('bits %d margin %d: LP t = %.4f at theta %.0f, nonzero weights %d' % (bits, m, t, th, int((Wq != 0).sum())))
        if best is None or t < best[0]: best = (t, bits, m, Wq.copy(), th, s)
t, bits, m, Wq, th, s = best
# prune by rounded magnitude: zero the smallest weights in blocks while the LP value does not rise
order = np.argsort(np.abs(Wq), kind='stable'); nz = [i for i in order if Wq[i] != 0]
blk = max(1, len(nz) // 16)
for a in range(0, len(nz), blk):
    W2 = Wq.copy(); W2[nz[a:a + blk]] = 0
    t2, th2, s2 = H.best_lp(B, H.hard_shares(B, W2, m), [th])
    if t2 <= t + 1e-9: Wq, t, s = W2, t2, s2
log('pruned: nonzero weights %d, LP t = %.4f' % (int((Wq != 0).sum()), t))
# snap P to multiples of 3, theta integer, polish on the exact evaluator
P = (3 * np.round(s['P'] / 3)).astype(np.int64); thi = int(round(th))
mx, E = H.exact_max(B, P, thi, Wq, m); log('snapped: exact max %d/%d = %.4f' % (mx, NT.SCALE, mx / NT.SCALE))
P, thi, cur = H.polish_P(B, P, thi, Wq, m, log=log)
pickle.dump(dict(P=P, theta=thi, W=Wq, margin=m, bits=bits, lp_t=t), open('hard_%s.pkl' % tag, 'wb'))
log('DONE exact max %d/%d = %.4f charge units' % (cur[0], NT.SCALE, cur[0] / NT.SCALE))
