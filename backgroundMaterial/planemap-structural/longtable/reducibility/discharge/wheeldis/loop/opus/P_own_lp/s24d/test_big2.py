# consistency: the D part of the window table summed over a row's positions = sum of recv_coef_R2 D coefficients x DV
import random
rng = random.Random(7); OUTL = open('test_big2.log', 'w')
y0 = np.zeros(len(ROOTS)); MV0 = lambda sg: None
keys = set()
for d in range(7, 12):
    for _ in range(300):
        w = [rng.choice(LET) for _ in range(d)]; s = [rng.choice(LET) for _ in range(d)]
        for k in recv_coef_R2(d, ''.join(map(str, w)), ''.join(map(str, s)), True):
            if k[0] == 'D': keys.add(k[1])
DV.clear(); W0 = {U: window_table_R2(U, y0, {}, MV0) for U in (7, 8, 9)}
DV.update({k: rng.random() for k in keys}); W1 = {U: window_table_R2(U, y0, {}, MV0) for U in (7, 8, 9)}
bad = 0; n = 0; rng = random.Random(7)
for d in range(7, 12):
    for _ in range(300):
        w = [rng.choice(LET) for _ in range(d)]; s = [rng.choice(LET) for _ in range(d)]; U = min(d, 9)
        cf = recv_coef_R2(d, ''.join(map(str, w)), ''.join(map(str, s)), True)
        a = sum(v * DV.get(k[1], 0.0) for k, v in cf.items() if k[0] == 'D')
        I = lambda j: LET.index(w[j % d]); J = lambda j: LET.index(s[j % d])
        b_ = 0.0
        for i in range(d):
            ix = (I(i - 2), I(i - 1), I(i), I(i + 1), I(i + 2), J(i - 2), J(i - 1), J(i), J(i + 1))
            v1, v0 = W1[U][ix], W0[U][ix]
            if np.isfinite(v0): b_ += v1 - v0
        n += 1
        if abs(a - b_) > 1e-9 and all(np.isfinite(W0[U][(I(i - 2), I(i - 1), I(i), I(i + 1), I(i + 2), J(i - 2), J(i - 1), J(i), J(i + 1))]) for i in range(d)): bad += 1
OUTL.write('big2 row/window consistency: %d random rows d=7..11, %d D keys, %d mismatches\n' % (n, len(keys), bad)); print(open('test_big2.log').read() if False else 'n=%d keys=%d bad=%d' % (n, len(keys), bad))
C = class_table_R2(True); OUTL.write('class table (big2) max %d\n' % int(C.max())); print('class max', int(C.max()))
OUTL.close()
