# exact evaluation of an LP solution with rational amounts: P, th7, th6 rounded to the nearest multiple of 1/U, evaluated exactly.
import pickle, sys, math, numpy as np, net3 as N2
from fractions import Fraction as Fr
B = pickle.load(open('cache_B3.pkl', 'rb')); R = pickle.load(open(sys.argv[1], 'rb')); s = R['sol']
for U in [int(x) for x in sys.argv[2:]]:
    P = np.maximum(np.round(s['P'] * U), 0).astype(np.int64); a = int(round(s['th7'] * U)); b = int(round(s['th6'] * U))
    E = N2.exact(B, P, a, b, R['W2'], R['m2'], R['W3'], R['m3'], U=U)
    m = N2.maxfinal(B, E)
    print('U=%d: exact max final %s = %.6f charge units (LP float %.6f); non-zero amounts %d' % (U, Fr(int(m), U * N2.SCALE), m / (U * N2.SCALE), s['t'], int((P > 0).sum())))
