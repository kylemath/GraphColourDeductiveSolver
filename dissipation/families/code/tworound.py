"""Is each part's outer (second-ring) condition set inside the 1-ball of ONE spoke?
If so the part reads only N[hub] u N[s]: the footprint of two nearest-neighbour steps.
usage: python3 tworound.py RULES"""
import sys, itertools, collections as C
sys.path.insert(0, 'code')
from parts import parse
from behav import null_parts
FULL = (5, 9)
def outer(p):
    h = p['hub']; hats = set(); fans = set()
    for j, s in enumerate(p['slots']):
        if (s[2], s[3]) != FULL: hats.add(j)
        if any(tuple(f) != FULL for f in s[4]): fans.add(j)
    return h, hats, fans
def cover(p):
    """min number of spokes whose 1-balls contain all conditioned outer vertices; and whether target alone does"""
    h, hats, fans = outer(p)
    if not hats and not fans: return 0, True
    def ok(S):
        return all(j in S for j in fans) and all(j in S or (j - 1) % h in S for j in hats)
    for k in range(1, h + 1):
        for S in itertools.combinations(range(h), k):
            if ok(set(S)): return k, (k == 1 and ok({2}))
def summary(P, name):
    for grp, sel in (('RSST', lambda p: p['pre'] == 'drule'), ('added', lambda p: p['pre'] != 'drule')):
        Q = [p for p in P if sel(p)]; c = C.Counter(); tgt = 0
        for p in Q:
            k, t = cover(p); c[k] += 1; tgt += bool(t and k == 1)
        n = len(Q)
        print(f'{name:8s} {grp:6s} n={n} spokes needed: ' + ' '.join(f'{k}:{c[k]}' for k in sorted(c)) +
              f' | <=1 spoke {100*(c[0]+c[1])/n:.0f}%  target alone (of 1-spoke) {tgt}  mean {sum(k*v for k,v in c.items())/n:.2f}')
sc, P = parse(sys.argv[1])
summary(P, 'real')
for seed in (1, 2, 3): summary(null_parts(P, seed), f'null{seed}')
