"""Figure (d): a deep locked run at r178 (hole 10, the order-34 R = NR = 8 record). Three consecutive doubly locked
states along pi; the two Kempe chains of x2 whose curvature parity decides the locks (TrackF Lemma LP) are overlaid:
K_A = {alpha,gamma}-chain of x2 (the pi-swap chain; Q odd <=> lock 2 shut), K_B = {alpha,delta}-chain of x2 (Q odd <=> lock 1 shut)."""
import sys, os, numpy as np
from draw import *
sys.path.insert(0, os.path.expanduser('~/4square')); from kempe_engine import HoleGame
KEY = 'r178'; rot, L = load(KEY); n = len(rot); deg = [len(r) for r in rot]; hole = json.load(open(G4 + 'maps/r178.json'))['hole']
H = HoleGame(n, rot, hole, rot[hole])
run = {}
def F(k):
    path = []; kk = k
    while H.dl[kk] and kk not in run and kk not in path: path.append(kk); kk = H.pi[kk]
    b = run.get(kk, 0) if H.dl[kk] and kk in run else (999 if kk in path else 0)
    for x in reversed(path): b = b + 1 if b < 999 else b; run[x] = b
    return run[k]
dl = [k for k in range(H.S) if H.dl[k]]
k0 = max(dl, key=lambda k: (F(k), H.dF[k]))
print('start state', k0, 'DL run', F(k0), 'dF', H.dF[k0])
PAL = ['#f6d55c', '#7fc8a9', '#f4a6a6', '#a7c7e7']  # game-like pastel elements
seq = [k0]
for _ in range(3): seq.append(H.pi[seq[-1]])
fig, axs = plt.subplots(1, 4, figsize=(22, 7.4))
for step, (ax, k) in enumerate(zip(axs, seq)):
    c = H.states[k]
    if not H.filled[k]:
        x, al, be, ga, de = H.frame(c); mp = {al: 0, be: 1, ga: 2, de: 3}
    else: mp = {i: i for i in range(4)}
    fill = [PAL[mp[c[v]]] if v != hole else '#222' for v in range(n)]
    draw_map(ax, KEY, hole, None, fill=fill, labels=None, shells=False)
    info = ''
    if not H.filled[k]:
        x, al, be, ga, de = H.frame(c)
        KA = H.chain_at(c, x[2], ga); KB = H.chain_at(c, x[2], de)
        for v in range(n):
            if v == hole: continue
            k_ = 6 - deg[v]; px, py = label_point(L, v)
            if k_: ax.text(px, py, '%+d' % k_, ha='center', va='center', fontsize=9, fontweight='bold', color='#b2182b' if k_ > 0 else '#2166ac', zorder=8)
        for K, col, off in [(KA, '#d35400', 0.012), (KB, '#6c3483', -0.012)]:
            for u in K:
                for w in rot[u]:
                    if w in K and u < w:
                        p, q = label_point(L, u), label_point(L, w)
                        ax.plot([p[0] + off, q[0] + off], [p[1] + off, q[1] + off], color=col, lw=3.2, alpha=.85, zorder=6, solid_capstyle='round')
            for u in K:
                p = label_point(L, u); ax.scatter(p[0] + off, p[1] + off, s=28, color=col, zorder=7)
        for i, xv in enumerate(x):
            p = label_point(L, xv); ax.text(p[0] - 0.07, p[1] + 0.07, 'x%d' % i, fontsize=9, fontweight='bold', color='k', zorder=9,
                                            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=.8))
        qa = sum(6 - deg[v] for v in KA); qb = sum(6 - deg[v] for v in KB)
        info = ('orange K_A (the chain pi swaps): %d regions,\n   curvature inside Q = %+d (%s -> lock 2 %s)\n'
                'purple K_B: %d regions, Q = %+d (%s -> lock 1 %s)\nswaps still needed to fill: %d' % (
                    len(KA), qa, 'odd' if qa % 2 else 'even', 'SHUT' if qa % 2 else 'open', len(KB), qb, 'odd' if qb % 2 else 'even', 'SHUT' if qb % 2 else 'open', H.dF[k]))
    ax.set_title(('start (doubly locked)' if step == 0 else 'after %d pi-swap%s' % (step, 's' if step > 1 else '')) + '\n' + info, fontsize=8.5, loc='left')
fig.suptitle('r178, hole 10 (order 34 record): a long locked run. Lock parity (TrackF Lemma LP): a lock is shut exactly when its chain encloses an ODD amount of curvature.\n'
             'Numbers = curvature of a region (+1 pentagon, -1 heptagon, ...); colours: yellow = alpha, green = beta, pink = gamma, blue = delta (rim reads alpha beta alpha gamma delta from x0); ', fontsize=11)
fig.tight_layout(rect=(0, 0, 1, 0.9)); fig.savefig('../figs/d_lock_chains_r178.png', dpi=130); fig.savefig('../figs/d_lock_chains_r178.svg')
print('ok')
