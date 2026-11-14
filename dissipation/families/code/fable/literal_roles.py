"""Idea E: what is each literal of an SP part for?
Flip one literal at a time (value outside its interval, rest of the ball inside the part) and ask:
 (a) does the hub's charge after RSST change (literal is needed to make the hub overcharged)?
 (b) does the literal sit on the target's own first ring (spokes 1,2,3, hats 2,3, fans of 2)?
Also: SP share of behaviour-matrix energy, and hub pictures after exact merges."""
import random, numpy as np, collections as C, pickle
from common import *
from ball import *
from ledger import picture
P = load(); R = Rules(P); rng = random.Random(2)
def charge(d, link, asg):
    W = Ball(d, link, asg); o = R.out(W); i = R.inn(W)
    return 60 * (6 - d) - sum(x.get('dr', 0) for x in o) + sum(x.get('dr', 0) for x in i)
def outside(iv):
    return [v for v in range(5, 10) if not (iv[0] <= v <= iv[1])]
tab = C.Counter(); perpart = []
for p in P:
    if p['pre'] != 'SP_': continue
    d = p['hub']; nrel = 0; nlit = 0
    lits = []
    for j, s in enumerate(p['slots']):
        if s[:2] != FULL: lits.append(('sp', j, None, s[:2]))
        if s[2:4] != FULL: lits.append(('hat', j, None, s[2:4]))
        for k, f in enumerate(s[4]):
            if f != FULL: lits.append(('fan', j, k, f))
    for kind, j, k, iv in lits:
        changed = False
        for rep in range(3):
            dd, link, asg = ball_from_part(p, 0, rng)
            c0 = charge(dd, link, asg)
            v = rng.choice(outside(iv)); link = list(link); asg = dict(asg)
            if kind == 'sp':
                link[j] = v
                for t in range(3): asg.pop(200 + 3 * j + t, None)
                for t in range(npriv(v)): asg[200 + 3 * j + t] = rng.randint(5, 9)
            elif kind == 'hat': asg[100 + (j - 1) % d] = v
            else: asg[200 + 3 * j + k] = v
            if charge(dd, tuple(link), asg) != c0: changed = True; break
        onT = (kind == 'sp' and j in (1, 2, 3)) or (kind == 'hat' and j in (2, 3)) or (kind == 'fan' and j == 2)
        tab[(kind, 'hub-charge' if changed else 'no charge effect', 'target ring' if onT else 'elsewhere')] += 1
        nlit += 1; nrel += changed or onT
    perpart.append((nlit, nrel))
tot = sum(tab.values())
for k, v in sorted(tab.items()): print(k, v, f'{v/tot:.3f}')
pp = np.array(perpart); print('literals per SP part mean', pp[:, 0].mean().round(2), ' explained (charge or target ring) mean', pp[:, 1].mean().round(2), ' share', (pp[:, 1].sum() / pp[:, 0].sum()).round(3))
# behaviour-matrix energy by template
A = np.load('../real58.npz'); B = np.load('../real911.npz')
pre = np.array([p['pre'][:2] for p in P]); e = C.Counter()
for z, ds in ((A, (5, 6, 7, 8)), (B, (9, 10, 11))):
    for d in ds:
        M = z[f'M{d}'].astype(float)
        for t in ('dr', 'SP', 'ST'): e[t] += (M[:, pre == t] ** 2).sum()
s = sum(e.values()); print('behaviour-matrix energy share by template:', {k: round(v / s, 5) for k, v in e.items()})
W = pickle.load(open('merged_real.pkl', 'rb'))
def unnorm(b): return dict(hub=b[0], slots=tuple((s[0][0], s[0][1], s[1][0], s[1][1], s[2]) for s in b[1]))
print('hub pictures after exact merges:', len({picture(unnorm(b)) for b in W}), 'from boxes', len(W))
