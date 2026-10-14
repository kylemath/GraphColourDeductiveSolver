"""Figure (e): mechanism test plots from mech_ana.py output arrays. Usage: figs_e.py DATADIR"""
import sys, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, warnings; warnings.filterwarnings('ignore')
D = sys.argv[1]; X = np.load(D + '/mechX.npy'); H = np.load(D + '/mechH.npy')
plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False})
fig, ax = plt.subplots(1, 3, figsize=(16, 5))
# A: Q distribution in DL states for KA and KB (all odd)
for nm, c, col in [('K_A (pi chain)', 7, '#d35400'), ('K_B', 13, '#6c3483')]:
    q = X[:, c + 1].astype(int); v, n = np.unique(q, return_counts=True)
    ax[0].bar(v + (0.2 if c == 13 else -0.2), n / n.sum(), width=0.4, color=col, label=nm)
ax[0].set_xticks(range(-5, 18, 2)); ax[0].set_xlabel('curvature Q = sum(6 - degree) inside the chain'); ax[0].set_ylabel('share of doubly locked states')
ax[0].set_title('A. In every doubly locked state both chains enclose\nODD curvature (1.71M states, 0 exceptions): a parity law', loc='left', fontsize=10); ax[0].legend(frameon=False)
# B: continuation vs size, by Q
qb = [('Q = 1', 1, 2, '#fdae6b'), ('Q = 3', 3, 4, '#e6550d'), ('Q = 5', 5, 6, '#a63603'), ('Q >= 7', 7, 99, '#7f2704'), ('Q < 0', -99, 0, '#3182bd')]
for lab, lo, hi, col in qb:
    m = (X[:, 8] >= lo) & (X[:, 8] < hi); xs, ys = [], []
    for s in range(2, 19):
        mm = m & (X[:, 7] == s)
        if mm.sum() > 300: xs.append(s); ys.append(X[mm, 4].mean())
    ax[1].plot(xs, ys, 'o-', color=col, label=lab, ms=4)
ax[1].set_xlabel('size of the pi-swap chain K_A (regions)'); ax[1].set_ylabel('P(still doubly locked after the swap)')
ax[1].set_title('B. Whether a lock run continues depends mainly on chain SIZE;\nat fixed size, extra curvature matters much less', loc='left', fontsize=10); ax[1].legend(frameon=False, title='curvature in K_A', fontsize=8)
# C: hole level
C2 = H[:, 2]; fr = H[:, 8]; ok = np.isfinite(fr)
xs = np.unique(C2[ok]); m_ = [fr[ok & (C2 == v)].mean() for v in xs]; n_ = [(ok & (C2 == v)).sum() for v in xs]
xs2 = [x for x, k in zip(xs, n_) if k >= 20]; m2 = [y for y, k in zip(m_, n_) if k >= 20]
ax[2].plot(xs2, m2, 'o-', color='#2c7fb8')
ax[2].set_xlabel('C(2) at the hole'); ax[2].set_ylabel('share of DL states whose pi-chain must reach\n3+ steps from the hole for its nearest pentagon')
ax[2].set_title('C. Near curvature lets lock chains close on nearby\npentagons (r = -0.46); but this does not explain R', loc='left', fontsize=10)
ax[2].text(0.02, 0.03, 'within-word regression of R on C(2): -0.106 [-0.173, -0.047]\nadding this "reach" variable: -0.099 [-0.165, -0.039]\n(2,391 sampled holes, enriched for R >= 4)', transform=ax[2].transAxes, fontsize=8)
fig.suptitle('Mechanism test at 2,391 order-33 holes (1.71M doubly locked states): curvature inside the lock chains', fontsize=12)
fig.tight_layout(); fig.savefig('../figs/e_mechanism.png', dpi=140); fig.savefig('../figs/e_mechanism.svg'); print('ok')
