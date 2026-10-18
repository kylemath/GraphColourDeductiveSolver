"""Can w2's link five e (w2 = 7, s1 = 6, f = 5, frame letters w1 = 6, s2 = 7, u = 7) be a LONE five with NO 6-relay
route (rule S: a 6-neighbour y of e with a big neighbour outside N[e])?  Enumerates e's 2-ball letters
(x2, x3 in {5,6}; p1, q, r, r', x4, x3-private in 5..9) with every 5-/6-wheel inside the 2-ball non-R (isR5/isR6),
w1's 6-wheel (u, w2, s1, p1, s0 = 6, w0 = 5) non-R.  usage: python3 eroute.py"""
import itertools
from defs import isR5, isR6
L = (5, 6, 7, 8, 9); big = lambda d: d >= 7
lone_noroute = []; lone_route = 0
for x2, x3 in itertools.product((5, 6), repeat=2):
    if isR5((7, 6, x2, x3, 5)): continue                       # e: w2, s1, x2, x3, f
    n2 = 1 if x2 == 6 else 0; n3 = 1 if x3 == 6 else 0          # privates of x2, x3
    for p1, q, r, x4 in itertools.product(L, repeat=4):
        if isR6((7, 7, 6, p1, 6, 5)): continue                  # w1
        if isR6((6, 7, 5, x2, q, p1)): continue                 # s1: w1, w2, e, x2, q, p1
        if isR5((5, x3, x4, 7, 7)): continue                    # f: e, x3, x4, s2, w2
        for pr2 in itertools.product(L, repeat=n2):
            w = (5, x3, r) + pr2 + (q, 6)                       # x2: e, x3, r, [r'], q, s1
            if (isR5 if x2 == 5 else isR6)(w): continue
            for pr3 in itertools.product(L, repeat=n3):
                w3 = (5, 5, x4) + pr3 + (r, x2)                 # x3: e, f, x4, [priv], r, x2
                if (isR5 if x3 == 5 else isR6)(w3): continue
                outs = [p1, q]                                   # s1's neighbours outside N[e] (w1 = 6)
                if x2 == 6: outs += [r, q] + list(pr2)
                if x3 == 6: outs += [r, x4] + list(pr3)
                if any(big(o) for o in outs): lone_route += 1
                else: lone_noroute.append(dict(x2=x2, x3=x3, p1=p1, q=q, r=r, x4=x4, pr2=pr2, pr3=pr3))
print('lone e with a rule-S route:', lone_route, '  lone e with NO route:', len(lone_noroute))
for z in lone_noroute[:20]: print('  ', z)
