# usage: python3 harden2.py runs2/X.pkl TAG : snap the LP solution of a run, polish on the exact integer evaluator, save.
import pickle, sys, time, json, numpy as np, net3 as N2
from fractions import Fraction as Fr
B = pickle.load(open('cache_B3.pkl', 'rb')); R = pickle.load(open(sys.argv[1], 'rb')); tag = sys.argv[2]; T0 = time.time()
W2, W3, m2, m3, s = R['W2'], R['W3'], R['m2'], R['m3'], R['sol']
def obj(P, a, b):
    E = N2.exact(B, P, a, b, W2, m2, W3, m3); f = np.concatenate([E['f7'][~B['A7']['excused']], E['f6'][~B['A6']['excused']], E['f5']])
    m = f.max(); return (int(m), int((f == m).sum()))
P = (3 * np.round(s['P'] / 3)).astype(np.int64); a, b = int(round(s['th7'])), int(round(s['th6']))
cur = obj(P, a, b); print('LP t %.4f; snapped exact max %s' % (s['t'], Fr(cur[0], N2.SCALE)), flush=True)
for rd in range(8):
    imp = False
    for i in np.random.default_rng(rd).permutation(N2.NPAR):
        for d in (3, -3):
            if P[i] + d < 0: continue
            P[i] += d; o = obj(P, a, b)
            if o < cur: cur = o; imp = True; break
            P[i] -= d
    for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1), (3, 0), (-3, 0), (0, 3), (0, -3)):
        o = obj(P, a + da, b + db)
        if o < cur: cur = o; a += da; b += db; imp = True
    print(' round %d: exact max %s = %.4f units (%d rows at max) [%.0fs]' % (rd, Fr(cur[0], N2.SCALE), cur[0] / N2.SCALE, cur[1], time.time() - T0), flush=True)
    if not imp: break
pickle.dump(dict(P=P, th7=a, th6=b, W2=W2, W3=W3, m2=m2, m3=m3, max=cur), open('runs3/hard_%s.pkl' % tag, 'wb'))
