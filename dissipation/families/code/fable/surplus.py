"""Idea C: is an SP push explained by 'hub has slack, target is overcharged' (or the reverse)?
For concrete hub balls drawn inside each SP part: hub charge after RSST rules (bounds from the open
third ring), and the target's expected RSST charge from its (fully visible) first ring."""
import random, numpy as np, collections as C, sys
from common import *
from ball import *
P = load(); R = Rules(P)
A = np.load('../real58.npz'); 
pre = np.array([p['pre'] for p in P]); dr = pre == 'drule'
E0 = {}
for d in (5, 6, 7, 8):
    M = A[f'M{d}'].astype(float); e = 60 * (6 - d) + M[:, dr].sum(1)
    for w, x in zip(A[f'W{d}'], e): E0[tuple(int(v) for v in w)] = x
rng = random.Random(7)
def stats(d, link, asg):
    Wu = Ball(d, link, asg); Wl = Ball(d, link, asg, True)
    o = R.out(Wu); iu = R.inn(Wu); il = R.inn(Wl)
    base = 60 * (6 - d) - sum(x.get('dr', 0) for x in o)
    hi = base + sum(x.get('dr', 0) for x in iu); lo = base + sum(x.get('dr', 0) for x in il)
    return Wu, o, lo, hi
rows = []
SPs = [p for p in P if p['pre'] == 'SP_']
for p in SPs:
    for rep in range(2):
        d, link, asg = ball_from_part(p, 0, rng)
        W, o, lo, hi = stats(d, link, asg)
        assert o[2].get('SP', 0) >= p['w'], (p['tag'], o)
        tw = target_word(W, 2)
        et = E0[canon(tw)] if tw else None
        spout = sum(x.get('SP', 0) for x in o)
        rows.append((d, link[2], p['w'], lo, hi, et, spout, o[2].get('SP', 0)))
rows = np.array([[np.nan if v is None else v for v in r] for r in rows], float)
for d in (7, 8):
    m = rows[:, 0] == d
    print(f'hub {d}: n={m.sum()}  hub RSST charge lower {np.percentile(rows[m,3],[0,10,50,90,100])}  upper {np.percentile(rows[m,4],[0,10,50,90,100])}')
    print('   share hub upper bound <= -w (hub has slack for the push even in worst case):', np.mean(rows[m, 4] + rows[m, 6] <= 0).round(3),
          ' share lower bound + all SP out <= 0:', np.mean(rows[m, 3] + rows[m, 6] <= 0).round(3))
    print('   hub upper + total SP out: percentiles', np.percentile(rows[m, 4] + rows[m, 6], [0, 10, 50, 90, 100]))
    for td in (7, 8):
        mm = m & (rows[:, 1] == td)
        if mm.sum(): print(f'   target deg {td}: n={mm.sum()} target expected RSST charge percentiles', np.percentile(rows[mm, 5], [0, 10, 50, 90, 100]).round(1))
# background: random balls with hub 7 / 8
for d in (7, 8):
    bl = []
    for _ in range(3000):
        dd, link, asg = random_ball(d, rng)
        W, o, lo, hi = stats(dd, link, asg); bl.append((lo, hi, sum(x.get('SP', 0) for x in o)))
    bl = np.array(bl)
    print(f'random hub {d}: RSST charge lower pct {np.percentile(bl[:,0],[0,10,50,90,100])} upper {np.percentile(bl[:,1],[0,10,50,90,100])} share SP fires {np.mean(bl[:,2]>0):.4f}')
np.save('surplus_rows.npy', rows)
