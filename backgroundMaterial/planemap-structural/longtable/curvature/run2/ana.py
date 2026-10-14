"""Regressions of hole difficulty on the radial curvature profile (orders 28-33). Usage: ana.py DATADIR > ana-out.txt
Design A: pooled, controls = hole link word (fixed effect) + n7 (#vertices of degree >= 7 in the graph).
Design B: within-graph, controls = graph fixed effect + word fixed effect (n7 and every graph-level total absorbed).
SEs are cluster-robust by graph (holes of one graph are not independent). Effects: per +1 unit of C(2) and per SD."""
import sys, numpy as np, json
D = sys.argv[1]
def load(o):
    f = np.load('%s/f%d.npz' % (D, o)); v = {k: f[k] for k in f.files}
    C = np.cumsum(v['K'].astype(float), axis=1); v['C'] = C
    v['C1'], v['C2'], v['C3'] = C[:, 1], C[:, 2], C[:, 3]
    v['P12'] = (v['P'][:, 1] + v['P'][:, 2]).astype(float); v['P2'] = v['P'][:, 2].astype(float); v['M2'] = v['M'][:, 2].astype(float)
    v['S3'] = v['S'][:, 3].astype(float); v['ecc'] = v['ecc'].astype(float)
    v['R4'] = (v['R'] >= 4).astype(float); v['R3'] = (v['R'] >= 3).astype(float)
    v['tight'] = (np.abs(v['mf'] - 0.25) < 1e-6).astype(float); v['dlc'] = (v['ndlc'] > 0).astype(float)
    v['Rf'] = v['R'].astype(float); v['NRf'] = v['NR'].astype(float); v['mff'] = v['mf'].astype(float)
    return v
def demean(X, groups, it=30):
    X = X.astype(float).copy()
    for _ in range(it if len(groups) > 1 else 1):
        for g in groups:
            cnt = np.bincount(g); 
            for j in range(X.shape[1]):
                X[:, j] -= (np.bincount(g, X[:, j]) / np.maximum(cnt, 1))[g]
    return X
def ols(y, X, cl):
    """OLS on already-residualised data, cluster-robust covariance."""
    XtX = X.T @ X; b = np.linalg.solve(XtX, X.T @ y); e = y - X @ b
    s = np.zeros((cl.max() + 1, X.shape[1]))
    for j in range(X.shape[1]): s[:, j] = np.bincount(cl, X[:, j] * e, minlength=cl.max() + 1)
    iv = np.linalg.inv(XtX); V = iv @ (s.T @ s) @ iv
    return b, np.sqrt(np.diag(V))
def fit(v, yname, xnames, design, mask=None):
    m = np.isfinite(v[yname]) if mask is None else mask & np.isfinite(v[yname])
    y = v[yname][m]; X = np.column_stack([v[x][m] for x in xnames]); cl = v['gid'][m]
    if design == 'A':
        X = np.column_stack([X, v['n7'][m].astype(float)])
        Z = demean(np.column_stack([y, X]), [v['word'][m]])
    else:
        Z = demean(np.column_stack([y, X]), [v['word'][m], cl])
    yt, Xt = Z[:, 0], Z[:, 1:]
    b, se = ols(yt, Xt, cl)
    # partial correlation of y with first predictor (others + FE partialled)
    if Xt.shape[1] > 1:
        o = Xt[:, 1:]; xr = Xt[:, 0] - o @ np.linalg.lstsq(o, Xt[:, 0], rcond=None)[0]; yr = yt - o @ np.linalg.lstsq(o, yt, rcond=None)[0]
    else: xr, yr = Xt[:, 0], yt
    pr = np.corrcoef(xr, yr)[0, 1]; sc = xr.std() / yr.std()
    return dict(n=int(m.sum()), b=b[:len(xnames)], se=se[:len(xnames)], pr=pr, prci=((b[0] - 1.96 * se[0]) * sc, (b[0] + 1.96 * se[0]) * sc),
                sdx=v[xnames[0]][m].std(), sdxw=xr.std(), ymean=y.mean())
def logit(v, yname, xname, nctl=150000, seed=1):
    """case-control logistic regression: all cases + random controls; word dummies (words with >= 5 cases), n7.
    Slopes (log odds ratios) are consistent under case-control sampling; intercept is not reported."""
    y = v[yname]; rng = np.random.default_rng(seed)
    wc = np.bincount(v['word'], y.astype(int)); okw = np.where(wc >= 5)[0]
    inw = np.isin(v['word'], okw)
    cases = np.where((y == 1) & inw)[0]; ctl = np.where((y == 0) & inw)[0]
    ctl = rng.choice(ctl, min(nctl, len(ctl)), replace=False); idx = np.concatenate([cases, ctl])
    W = (v['word'][idx][:, None] == okw[None, :]).astype(float)
    X = np.column_stack([v[xname][idx], v['n7'][idx], W]); yy = y[idx]; cl = v['gid'][idx]
    b = np.zeros(X.shape[1])
    for _ in range(40):
        p = 1 / (1 + np.exp(-X @ b)); w = p * (1 - p)
        H = X.T @ (X * w[:, None]) + 1e-8 * np.eye(X.shape[1]); g = X.T @ (yy - p)
        st = np.linalg.solve(H, g); b += st
        if np.abs(st).max() < 1e-9: break
    p = 1 / (1 + np.exp(-X @ b)); iv = np.linalg.inv(X.T @ (X * (p * (1 - p))[:, None]))
    s = np.zeros((cl.max() + 1, X.shape[1]))
    for j in range(X.shape[1]): s[:, j] = np.bincount(cl, X[:, j] * (yy - p), minlength=cl.max() + 1)
    V = iv @ (s.T @ s) @ iv; se = np.sqrt(V[0, 0])
    return dict(cases=len(cases), ctl=len(ctl), words=len(okw), lor=b[0], se=se, OR=np.exp(b[0]), ci=(np.exp(b[0] - 1.96 * se), np.exp(b[0] + 1.96 * se)),
                sdx=v[xname].std())
res = {}
v = load(33)
print('ORDER 33: %d holes, %d graphs, %d words' % (len(v['R']), v['gid'].max() + 1, v['word'].max() + 1))
print('C(1) range %d..%d, C(2) %d..%d (mean %.2f sd %.2f), C(3) %d..%d; ecc distribution %s' % (v['C1'].min(), v['C1'].max(), v['C2'].min(), v['C2'].max(), v['C2'].mean(), v['C2'].std(), v['C3'].min(), v['C3'].max(), dict(zip(*np.unique(v['ecc'], return_counts=True)))))
# identity at r=2 (clean shells): |S_3| = 17 - C(1) - C(2)
print('shell identity |S_3| = 17 - C(1) - C(2): holds at %d / %d holes' % ((v['S3'] == 17 - v['C1'] - v['C2']).sum(), len(v['S3'])))
print('corr(C2, within-word) with ecc: %.3f' % np.corrcoef(demean(np.column_stack([v['C2'], v['ecc']]), [v['word']]).T)[0, 1])
print('\n== linear effects of near curvature C(2) (per +1 unit of C(2); per-SD = x sd(C2 within word)) ==')
print('outcome | design | n | mean y | beta per unit [95% CI] | beta per within-word SD | partial r [95% CI]')
for y in ['Rf', 'NRf', 'R3', 'R4', 'mff', 'tight', 'dlc']:
    for des in 'AB':
        r = fit(v, y, ['C2'], des); res[(33, y, des)] = r
        print('%-5s | %s | %d | %.4f | %+.5f [%+.5f, %+.5f] | %+.5f | %+.4f [%+.4f, %+.4f]' % (y, des, r['n'], r['ymean'], r['b'][0], r['b'][0] - 1.96 * r['se'][0], r['b'][0] + 1.96 * r['se'][0], r['b'][0] * r['sdxw'], r['pr'], *r['prci']))
print('\n== separating positive (deg-5, P2) and negative (deg>=7 excess, M2) charge at distance 2; also C(3) beyond C(2) ==')
for y in ['Rf', 'NRf', 'R4', 'mff']:
    for des in 'AB':
        r = fit(v, y, ['P2', 'M2'], des); r2 = fit(v, y, ['C2', 'C3'], des); r3 = fit(v, y, ['C2', 'ecc'], des)
        print('%-4s %s | P2 %+.5f±%.5f  M2 %+.5f±%.5f | C2 %+.5f±%.5f  C3 %+.5f±%.5f | C2 %+.5f±%.5f ecc %+.5f±%.5f' % (y, des, r['b'][0], 1.96 * r['se'][0], r['b'][1], 1.96 * r['se'][1], r2['b'][0], 1.96 * r2['se'][0], r2['b'][1], 1.96 * r2['se'][1], r3['b'][0], 1.96 * r3['se'][0], r3['b'][1], 1.96 * r3['se'][1]))
print('\n== first-pass variable P12 = #deg-5 within distance 2 (for comparison) ==')
for y in ['Rf', 'R4']:
    for des in 'AB':
        r = fit(v, y, ['P12'], des); print('%-4s %s | P12 %+.5f [%+.5f, %+.5f]  partial r %+.4f' % (y, des, r['b'][0], r['b'][0] - 1.96 * r['se'][0], r['b'][0] + 1.96 * r['se'][0], r['pr']))
print('\n== logistic (case-control, word dummies + n7, cluster-robust): odds ratio per +1 C(2) ==')
for y in ['R4', 'R3', 'tight']:
    L = logit(v, y, 'C2'); res[(33, y, 'logit')] = L
    print('%-5s cases %d controls %d words %d | OR per unit %.3f [%.3f, %.3f] | OR per SD(C2)=%.2f: %.3f' % (y, L['cases'], L['ctl'], L['words'], L['OR'], *L['ci'], L['sdx'], np.exp(L['lor'] * L['sdx'])))
print('\n== all-DL pi-cycles (25 holes): C(2) distribution vs all holes ==')
m = v['ndlc'] > 0
print('C2 at all-DL holes:', sorted(v['C2'][m].astype(int).tolist()), ' mean %.2f vs census mean %.2f; words: %s' % (v['C2'][m].mean(), v['C2'].mean(), sorted(set(v['wordlist'][v['word'][m]].tolist()))))
# word-matched comparison
ex = [v['C2'][(v['word'] == w)].mean() for w in v['word'][m]]
print('word-matched expected mean C2 %.2f (observed %.2f)' % (np.mean(ex), v['C2'][m].mean()))
print('\n== orders 28-33: design A and B slope of R, NR, mf on C(2) ==')
orders = {}
for o in [28, 29, 30, 31, 32, 33]:
    w = v if o == 33 else load(o)
    row = {}
    for y in ['Rf', 'NRf', 'mff', 'R3']:
        for des in 'AB':
            r = fit(w, y, ['C2'], des); row[(y, des)] = (r['b'][0], r['se'][0], r['pr'], r['n'])
    orders[o] = row
    print('%d n=%6d | ' % (o, row[('Rf', 'A')][3]) + ' | '.join('%s%s %+.4f±%.4f (pr %+.3f)' % (y, d, *[row[(y, d)][0], 1.96 * row[(y, d)][1], row[(y, d)][2]]) for y in ['Rf', 'NRf', 'mff', 'R3'] for d in 'AB'))
json.dump({str(o): {'%s_%s' % k: val for k, val in row.items()} for o, row in orders.items()}, open('orders.json', 'w'))
