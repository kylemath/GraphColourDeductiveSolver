import pickle, sys, numpy as np, net2 as N2, collections
B = pickle.load(open('cache_B2.pkl', 'rb')); R = pickle.load(open(sys.argv[1], 'rb')); s = R['sol']; U = 1100
A7, A6 = B['A7'], B['A6']
P = np.maximum(np.round(s['P'] * U), 0).astype(np.int64); a = int(round(s['th7'] * U)); b = int(round(s['th6'] * U))
E = N2.exact(B, P, a, b, R['W2'], R['m2'], R['W3'], R['m3'], U=U); sc = U * N2.SCALE
mx = N2.maxfinal(B, E); tol = sc // 100
b7 = np.flatnonzero(~A7['excused'] & (E['f7'] >= mx - tol)); b6 = np.flatnonzero(~A6['excused'] & (E['f6'] >= mx - tol)); b5 = np.flatnonzero(E['f5'] >= mx - tol)
print('max %.4f; near-binding 7-rows %d, 6-rows %d, 5-rows %d' % (mx / sc, len(b7), len(b6), len(b5)))
for i in b7[:10]:
    in2 = np.where(A7['r2v'][i] >= 0, E['M2'][np.maximum(A7['r2v'][i], 0)], 0); in3 = np.where(A7['r3v'][i] >= 0, E['M3'][np.maximum(A7['r3v'][i], 0)], 0)
    print('  7', B['R7'][i], 'c1 %.2f in2 %.2f in3 %.2f' % (E['c1_7'][i] / U, in2.sum() / sc, in3.sum() / sc))
for i in b6[:6]: print('  6', B['R6'][i], 'c1 %.2f c2 %.2f' % (E['c1_6'][i] / U, E['c2_6'][i] / sc))
print('  5', [B['W5'][i] for i in b5])
# which senders realise the binding incoming terms, and how many targets they have
ntg = (A7['tgt2'] >= 0).sum(1); cnt = collections.Counter()
for i in b7:
    for v in A7['r2v'][i][A7['r2v'][i] >= 0]:
        if E['M2'][v] <= 0: continue
        e = A7['src'][A7['src'][:, 2] == v]; inS, k = N2.shares_int(A7['tgt2'], B['F2'], R['W2'], R['m2'])
        val = E['sur2'][e[:, 0]] * (N2.SCALE // k[e[:, 0]]) * inS[e[:, 0], e[:, 1]]
        j = e[np.argmax(val)]; cnt[(ntg[j[0]], int(k[j[0]]))] += 1
print('arg-max R2 senders on binding 7-rows, (#targets, #shared): count', dict(cnt))
