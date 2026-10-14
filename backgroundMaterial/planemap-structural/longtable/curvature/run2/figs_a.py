"""Figure (a): radial curvature profile vs difficulty, order 33 (+ consistency over orders 28-33). Usage: figs_a.py DATADIR"""
import sys, json, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, warnings
warnings.filterwarnings('ignore')
D = sys.argv[1]; OUT = '../figs/'
f = np.load(D + '/f33.npz'); K = f['K'].astype(float); C = np.cumsum(K, 1); R = f['R'].astype(float); word = f['word']; S = f['S'].astype(float)
plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False})
cols = {1: '#c0392b', 2: '#e67e22', 3: '#2c7fb8', 4: '#7f7f7f'}
fig, ax = plt.subplots(2, 2, figsize=(11, 8.2))
# panel 1: mean R vs C(r)
for r in (1, 2, 3, 4):
    x = C[:, r]; xs, ms, lo, hi = [], [], [], []
    for v in np.unique(x):
        m = x == v
        if m.sum() < 300: continue
        y = R[m]; se = y.std() / np.sqrt(m.sum()); xs.append(v); ms.append(y.mean()); lo.append(y.mean() - 1.96 * se); hi.append(y.mean() + 1.96 * se)
    ax[0, 0].plot(xs, ms, 'o-', color=cols[r], label='r = %d' % r); ax[0, 0].fill_between(xs, lo, hi, color=cols[r], alpha=.2)
ax[0, 0].set_xlabel('C(r) = total curvature within distance r of the hole\n(count of +1 for each degree-5, -1 per extra edge of degree 7+)')
ax[0, 0].set_ylabel('mean R (longest locked run at the hole)'); ax[0, 0].legend(title='radius r', frameon=False)
ax[0, 0].set_title('A. Raw: locked-run length vs curvature inside radius r', loc='left', fontsize=10)
ax[0, 0].text(0.02, 0.02, 'r=1 is just the hole\'s own neighbours;\nC(4)~12 = the whole sphere', transform=ax[0, 0].transAxes, fontsize=8, color='#555')
# panel 2: P(R>=4) vs C(2), raw and word-adjusted
x = C[:, 2]; y4 = (R >= 4).astype(float)
# word-adjusted: residual from word mean + overall mean
wm = np.bincount(word, y4) / np.bincount(word); adj = y4 - wm[word] + y4.mean()
wmR = np.bincount(word, R) / np.bincount(word); adjR = R - wmR[word] + R.mean()
xs = [v for v in np.unique(x) if (x == v).sum() >= 300]
for yy, lab, c, mk in [(y4, 'raw', '#999', 's'), (adj, 'adjusted for the hole\'s own neighbour word', '#e67e22', 'o')]:
    m_ = [yy[x == v].mean() * 1000 for v in xs]; se = [yy[x == v].std() / np.sqrt((x == v).sum()) * 1960 for v in xs]
    ax[0, 1].errorbar(xs, m_, yerr=se, fmt=mk + '-', color=c, label=lab, capsize=2)
ax[0, 1].set_xlabel('C(2) = curvature within distance 2 of the hole'); ax[0, 1].set_ylabel('holes with R >= 4, per 1000')
ax[0, 1].set_title('B. The rare long locks thin out as near curvature grows', loc='left', fontsize=10); ax[0, 1].legend(frameon=False, fontsize=8)
ax[0, 1].text(0.98, 0.95, 'logistic, word + #deg7+ controlled:\nodds ratio 0.80 per +1 of C(2)\n95% CI [0.74, 0.86]', transform=ax[0, 1].transAxes, ha='right', va='top', fontsize=8)
# panel 3: shell growth law
for r, c in [(1, cols[1]), (2, cols[2]), (3, cols[3])]:
    g = S[:, r + 1] - S[:, r]; t = 6 - C[:, r]
    m = f['ecc'] > r
    pairs, cnt = np.unique(np.column_stack([t[m], g[m]]), axis=0, return_counts=True)
    ax[1, 0].scatter(pairs[:, 0] + (r - 2) * 0.12, pairs[:, 1], s=6 + 60 * np.sqrt(cnt / cnt.max()), color=c, alpha=.7, label='r = %d' % r)
lim = [-10, 10]; ax[1, 0].plot(lim, lim, 'k--', lw=1, label='|S_{r+1}| - |S_r| = 6 - C(r)')
ax[1, 0].set_xlim(-6, 10); ax[1, 0].set_ylim(-14, 10)
ax[1, 0].set_xlabel('6 - C(r)'); ax[1, 0].set_ylabel('growth of the shells:  |S_{r+1}| - |S_r|')
ax[1, 0].set_title('C. Discrete Gauss-Bonnet: curvature slows shell growth', loc='left', fontsize=10); ax[1, 0].legend(frameon=False, fontsize=8)
ax[1, 0].text(0.02, 0.97, 'exact at r = 1, 2 (all 979,741 holes);\nat r = 3 the shells start to fold\n(sphere closing up) and fall below the line', transform=ax[1, 0].transAxes, va='top', fontsize=8)
# panel 4: consistency across orders
O = json.load(open('orders.json'))
for j, (key, lab, c) in enumerate([('Rf_A', 'R, pooled (word + #deg7+ controls)', '#2c7fb8'), ('Rf_B', 'R, within graph (graph + word fixed effects)', '#c0392b'), ('NRf_B', 'NR, within graph', '#7f7f7f')]):
    os_ = sorted(O, key=int); b = [O[o][key][0] for o in os_]; e = [1.96 * O[o][key][1] for o in os_]
    ax[1, 1].errorbar(np.array([int(o) for o in os_]) + (j - 1) * 0.12, b, yerr=e, fmt='o', color=c, capsize=2, label=lab)
ax[1, 1].axhline(0, color='k', lw=.8); ax[1, 1].set_xlabel('order (number of regions)'); ax[1, 1].set_ylabel('change in mean run length per +1 of C(2)')
ax[1, 1].set_title('D. Same sign at every order (effect is small)', loc='left', fontsize=10); ax[1, 1].legend(frameon=False, fontsize=8)
fig.suptitle('Curvature near the hole vs locked-run difficulty, frame census (order 33: 979,741 holes)', fontsize=12)
fig.tight_layout(); fig.savefig(OUT + 'a_radial_profile.png', dpi=150); fig.savefig(OUT + 'a_radial_profile.svg')
print('ok')
