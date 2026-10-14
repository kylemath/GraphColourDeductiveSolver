"""Analyse mech.py output. Usage: mech_ana.py MECH.jsonl FEATDIR > mech-out.txt"""
import sys, json, collections, numpy as np, warnings; warnings.filterwarnings('ignore')
src, D = sys.argv[1], sys.argv[2]
samp = {}
for l in open('mech-sample.txt'):
    g, h, R = l.split(); samp[(g, int(h))] = int(R)
f = np.load(D + '/f33.npz'); names = f['names']; C = np.cumsum(f['K'].astype(float), 1)
key = {(names[g], h): i for i, (g, h) in enumerate(zip(f['gid'], f['hole']))}
par = collections.Counter(); rows = []; holes = []
for l in open(src):
    r = json.loads(l); R = samp[(r['g'], r['h'])]; i = key[(r['g'], r['h'])]
    for a, b, c, d, v in r['par']: par[(a, b, c, d)] += v
    dl = r['dl']
    for x in dl: rows.append([R, C[i, 2]] + x[:5] + [z for K in x[5:] for z in K])
    if dl:
        A = np.array([[x[0], x[1], x[5][0], x[5][1], x[5][4], x[5][5], x[8][0], x[8][1], x[9][0], x[9][1]] for x in dl], float)
        holes.append([R, C[i, 1], C[i, 2], f['word'][i], r['maxdF'], A[:, 1].max(), A[:, 2].mean(), A[:, 3].mean(), (A[:, 5] >= 3).mean(), A[:, 4].mean(), (A[:, 3] == 1).mean(), r['nDL'] / r['S']])
    else:
        holes.append([R, C[i, 1], C[i, 2], f['word'][i], r['maxdF'], 0, np.nan, np.nan, np.nan, np.nan, np.nan, 0])
X = np.array(rows, float); Hh = np.array(holes, float)
# columns: 0 R, 1 C2, 2 dF, 3 fwd, 4 cont, 5 locks(pi), 6 N, then 6 per chain (size,Q,P,M,meand,nearpos) for KA(7..12) KB(13..18) Kmu(19..24) L1(25..30) L2(31..36)
cn = {'KA': 7, 'KB': 13, 'Kmu': 19, 'L1': 25, 'L2': 31}
print('holes analysed %d (stratified: all R>=4 + 400 each of R=0..3, shuffled; first-N subset if cut at 15 min); DL states %d' % (len(Hh), len(X)))
print('\n[data] lock-parity check over all unfilled states (engine lock flags L1,L2 vs parity of Q(K_{alpha,delta}(x2)), Q(K_{alpha,gamma}(x2))):')
for k, v in sorted(par.items()): print('   L1=%d L2=%d  Q(KA) odd=%d  Q(KB) odd=%d : %d states' % (k[0], k[1], k[2], k[3], v))
bad = sum(v for k, v in par.items() if not (k[1] == k[2] and k[0] == k[3])); print('   mismatches:', bad)
print('\n[data] charge Q = sum(6-deg) inside each chain, DL states:')
for nm, c in cn.items():
    q = X[:, c + 1]; print('   %-3s size mean %.1f | Q mean %.2f | Q odd %.4f | Q=1 %.3f | Q<0 %.3f | nearest +charge dist mean %.2f' % (nm, X[:, c].mean(), q.mean(), (q % 2 == 1).mean(), (q == 1).mean(), (q < 0).mean(), X[X[:, c + 5] >= 0, c + 5].mean()))
def tab(name, x, y, bins):
    print('   %s:' % name, ' '.join('[%s: n=%d %.3f]' % (b, ((x >= lo) & (x < hi)).sum(), y[(x >= lo) & (x < hi)].mean()) for b, lo, hi in bins if ((x >= lo) & (x < hi)).sum() > 50))
print('\n[data] does the pi-swap leave the state doubly locked (run continues)?  P(cont) =', '%.3f' % X[:, 4].mean())
sz = [('2-5', 2, 6), ('6-9', 6, 10), ('10-13', 10, 14), ('14+', 14, 99)]
tab('by size |KA|', X[:, 7], X[:, 4], sz)
qb = [('Q<0', -99, 0), ('Q=1', 1, 2), ('Q=3', 3, 4), ('Q=5', 5, 6), ('Q>=7', 7, 99)]
tab('by Q(KA)', X[:, 8], X[:, 4], qb)
for nm, lo, hi in sz:
    m = (X[:, 7] >= lo) & (X[:, 7] < hi); tab('   within |KA| %s, by Q(KA)' % nm, X[m, 8], X[m, 4], qb)
# logistic: cont ~ size + Q (+ meand) -- standardized
def lg(y, Z):
    Z = np.column_stack([np.ones(len(y)), (Z - Z.mean(0)) / Z.std(0)]); b = np.zeros(Z.shape[1])
    for _ in range(30):
        p = 1 / (1 + np.exp(-Z @ b)); Hm = Z.T @ (Z * (p * (1 - p))[:, None]); b += np.linalg.solve(Hm, Z.T @ (y - p))
    se = np.sqrt(np.diag(np.linalg.inv(Hm))); return b[1:], se[1:]
b, se = lg(X[:, 4], X[:, [7, 8, 11]])
print('   logistic cont ~ z(|KA|) + z(Q(KA)) + z(mean dist of KA from hole): log-OR per SD %s (naive SE %s; states within a hole are not independent)' % (np.round(b, 3), np.round(se, 3)))
print('\n[data] distance to fill dF at DL states:  mean %.2f' % X[:, 2].mean())
tab('by Q(KA)', X[:, 8], X[:, 2], qb)
tab('by Q(L1 lock chain)', X[:, 26], X[:, 2], qb)
tab('by |KA|', X[:, 7], X[:, 2], sz)
for nm, c in cn.items():
    print('   corr(dF, Q(%s)) %+.3f  corr(dF, |%s|) %+.3f  corr(fwd run, Q(%s)) %+.3f' % (nm, np.corrcoef(X[:, 2], X[:, c + 1])[0, 1], nm, np.corrcoef(X[:, 2], X[:, c])[0, 1], nm, np.corrcoef(X[:, 3], X[:, c + 1])[0, 1]))
print('\n[data] hole level (n=%d): does near curvature act through the lock chains?' % len(Hh))
cols = ['R', 'C1', 'C2', 'word', 'maxdF', 'maxDLrun', 'mean|KA|', 'meanQ(KA)', 'frac KA nearest+charge>=3', 'mean dist KA', 'frac Q(KA)=1', 'DL share']
ok = np.isfinite(Hh[:, 6])
for j in [5, 6, 7, 8, 9, 10, 11, 4]:
    print('   corr(C2, %-26s) %+.3f   corr(R, it) %+.3f' % (cols[j], np.corrcoef(Hh[ok, 2], Hh[ok, j])[0, 1], np.corrcoef(Hh[ok, 0], Hh[ok, j])[0, 1]))
# mediation: R ~ C2 + word FE, then + mediators
def wdemean(Z, w):
    Z = Z.copy()
    for j in range(Z.shape[1]): Z[:, j] -= (np.bincount(w, Z[:, j]) / np.bincount(w))[w]
    return Z
w = np.unique(Hh[ok, 3].astype(int), return_inverse=True)[1]
Z = wdemean(Hh[ok][:, [0, 2, 6, 7, 9]], w)
for lab, cs in [('R ~ C2', [1]), ('R ~ C2 + mean|KA| + meanQ(KA) + mean dist KA', [1, 2, 3, 4])]:
    b = np.linalg.lstsq(Z[:, cs], Z[:, 0], rcond=None)[0]; e = Z[:, 0] - Z[:, cs] @ b
    r2 = 1 - e.var() / Z[:, 0].var(); print('   within-word OLS %-45s coef %s  R2 %.3f' % (lab, np.round(b, 4), r2))
np.save(D + '/mechX.npy', X); np.save(D + '/mechH.npy', Hh)
# mediation through "how far the pi-chain must reach for its odd charge"
okm = ok & np.isfinite(Hh[:, 8]); w2 = np.unique(Hh[okm, 3].astype(int), return_inverse=True)[1]
Z = wdemean(Hh[okm][:, [0, 2, 8, 11]], w2)
for lab, cs in [('R ~ C2', [1]), ('R ~ C2 + frac KA nearest+charge>=3', [1, 2]), ('R ~ C2 + frac>=3 + DL share', [1, 2, 3])]:
    b = np.linalg.lstsq(Z[:, cs], Z[:, 0], rcond=None)[0]; e = Z[:, 0] - Z[:, cs] @ b
    # bootstrap CI for the C2 coefficient
    rng = np.random.default_rng(0); bs = []
    for _ in range(500):
        ii = rng.integers(0, len(Z), len(Z)); bs.append(np.linalg.lstsq(Z[ii][:, cs], Z[ii, 0], rcond=None)[0])
    bs = np.array(bs); lo, hi = np.percentile(bs, [2.5, 97.5], axis=0)
    print('   mediation %-40s coefs %s  95%% CI lo %s hi %s  R2 %.3f' % (lab, np.round(b, 3), np.round(lo, 3), np.round(hi, 3), 1 - e.var() / Z[:, 0].var()))
