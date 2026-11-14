"""Null and recall checks for the overflow law.
null: real RSST+ST parts, SP parts slot-scrambled (behav.null_parts) -> share of SP balls with hub charge 6 / hub ending at 0.
recall: uniform random hub balls: how many are overcharged after RSST, and how many of those does an SP part touch."""
import random, numpy as np, collections as C, sys
from common import *
from ball import *
import behav
P = load()
def lawshare(Q, seed):
    R = Rules(Q); rng = random.Random(seed); cs = []; ends = []
    for p in Q:
        if p['pre'] != 'SP_': continue
        d, link, asg = ball_from_part(p, 0, rng)
        W = Ball(d, link, asg)
        o = R.out(W); i = R.inn(W)
        c = 60 * (6 - d) - sum(x.get('dr', 0) for x in o) + sum(x.get('dr', 0) for x in i)
        cs.append(c); ends.append(c - sum(x.get('SP', 0) for x in o))
    cs = np.array(cs); ends = np.array(ends)
    return dict(c_eq_6=float(np.mean(cs == 6)), c_pos=float(np.mean(cs > 0)), end_eq_0=float(np.mean(ends == 0)), median_c=float(np.median(cs)))
print('real', lawshare(P, 1))
for s in (1, 2, 3):
    N = behav.null_parts(P, s)
    Q = [q if p['pre'] == 'SP_' else p for p, q in zip(P, N)]
    print('null', s, lawshare(Q, 1))
R = Rules(P); rng = random.Random(5)
for d in (7, 8):
    cnt = C.Counter(); n = 12000
    for _ in range(n):
        dd, link, asg = random_ball(d, rng)
        W = Ball(dd, link, asg); o = R.out(W); i = R.inn(W)
        c = 60 * (6 - d) - sum(x.get('dr', 0) for x in o) + sum(x.get('dr', 0) for x in i)
        sp = sum(x.get('SP', 0) for x in o)
        cnt[('c>0', c > 0)] += 1
        if c > 0: cnt[('c', c)] += 1; cnt[('c>0 & SP', sp > 0)] += 1
        if sp > 0: cnt['SP fires'] += 1
    print('random hub', d, 'n', n, sorted(cnt.items(), key=str))
