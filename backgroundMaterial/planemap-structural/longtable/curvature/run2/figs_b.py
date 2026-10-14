"""Figure (b): game maps coloured by curvature with distance shells; hard vs easy holes on the same map.
Usage: figs_b.py game-out.jsonl"""
import sys, json
from draw import *
G = [json.loads(l) for l in open(sys.argv[1])]
def pick(m, which):
    H = [g for g in G if g['map'] == m]
    if which == 'designated': return next(g for g in H if g['designated'])
    key = lambda g: (g['maxdF'], g['maxrun'], g['meandF'])
    return min(H, key=key) if which == 'easy' else max(H, key=key)
panels = [('r178', 'designated', 'r178 (order 34), record hole: HARD'), ('r178', 'easy', 'r178, easiest degree-5 hole: EASY'),
          ('r210', 'designated', 'r210 (order 34), deepest hole: HARD'), ('r210', 'easy', 'r210, easiest degree-5 hole: EASY'),
          ('six', 'designated', 'six (order 28): flat 66666 hole'), ('c30', 'designated', 'c30 (C30 dual): 55555 hole, curvature all around')]
fig, axs = plt.subplots(2, 3, figsize=(16, 13))
for ax, (m, w, t) in zip(axs.flat, panels):
    g = pick(m, w)
    S3 = None
    draw_map(ax, m, g['hole'], None)
    ax.set_title('%s\nhole %d, word %s | C(1)=%+d  C(2)=%+d  C(3)=%+d\nworst start: %d swaps to fill | longest locked (DL) run %s | all-DL cycles %d' % (
        t, g['hole'], g['word'], g['C'][1], g['C'][2], g['C'][3], g['maxdF'], ('endless' if g['maxrun'] >= 999 else g['maxrun']), g['cyc']), fontsize=9, loc='left')
legend(fig, y=0.005)
fig.suptitle('Where is the curvature relative to the hole?  Red = pentagon regions (+1), blue = 7+ neighbours (-1, -2, ...).\n'
             'Thick lines = distance shells around the hole. C(r) = net curvature within r steps (whole map = +12).', fontsize=12)
fig.tight_layout(rect=(0, 0.04, 1, 0.95), h_pad=3); fig.savefig('../figs/b_maps_curvature.png', dpi=130); fig.savefig('../figs/b_maps_curvature.svg')
print('ok')
