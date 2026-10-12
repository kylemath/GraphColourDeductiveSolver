#!/usr/bin/env python3
"""[Track B] Optimise a one-step discharging rule family and read off the unavoidable set it proves.

Charges: ch(v) = 6 - deg(v); total 12 on any spherical triangulation (Euler).
Rule family sigma: a degree-5 vertex v sends to each neighbour u with deg(u) >= 7 the amount sigma[p, D, q], where
D = min(deg u, 8) and p, q = min(deg, 8) of the two common neighbours of v and u (the two faces on vu); sigma symmetric in p,q.
These are exactly the two letters next to u in v's link word, so everything a 5-vertex sends is a function of its capped word.

Receiver conditions (sufficient for every vertex of degree >= 7 to end with charge <= 0):
  d = 7 : for every cyclic sequence z_1..z_7 in {5,6,7,8}: sum_{z_i = 5} sigma[z_{i-1},7,z_{i+1}] <= 1      (enumerated)
  d >= 8: maximum mean weight of a cycle in the order-2 de Bruijn graph on {5,6,7,8} with edge (a,b)->(b,c) of weight
          sigma[a,8,c] if b = 5 (else 0) is <= 1/4, certified by a potential phi:  w(a,b,c) <= 1/4 + phi(b,c) - phi(a,b).
          Then any degree-d link receives <= d/4 <= d - 6 for d >= 8.
Sender: a 5-vertex with capped word w sends s(w) = sum over letters >= 7 of sigma[left, letter, right].
Conclusion: every triangulation with min degree 5 has a 5-vertex with a word in S = {w : s(w) < 1}   (else total <= 0).
MILP: minimise |S| (binary z_w, s(w) >= 1 - z_w), over sigma >= 0.
The words containing 555 or 565 are listed separately: in the frame class they need an unclean-tip appearance
(a separating 4-cycle), so they can be dropped from S only with an F2-type argument.
Usage: python3 discharge_lp.py [--frame-only]  (frame-only: do not require 555/565 words to be discharged)"""
import itertools, sys, json
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from words import canon, fmt

CAP = 8; L = [5, 6, 7, 8]
frame_only = '--frame-only' in sys.argv
# sigma variables
keys = []
for D in (7, 8):
    for p in L:
        for q in L:
            if p <= q: keys.append((p, D, q))
K = {k: i for i, k in enumerate(keys)}
def sk(p, D, q): return K[(min(p, q), D, max(p, q))]
# phi variables (pairs)
pairs = [(a, b) for a in L for b in L]; PH = {pq: len(keys) + i for i, pq in enumerate(pairs)}
words = sorted({canon(list(w)) for w in itertools.product(L, repeat=5)})
def forbidden(w): return any((w[i - 1], w[i], w[(i + 1) % 5]) in ((5, 5, 5), (5, 6, 5)) for i in range(5))
W0 = len(keys) + len(pairs); WZ = {w: W0 + i for i, w in enumerate(words)}; NV = W0 + len(words)
rows, lo, hi = [], [], []
def row(coefs, l, h):
    r = np.zeros(NV)
    for i, c in coefs: r[i] += c
    rows.append(r); lo.append(l); hi.append(h)
# d = 7 receiver
seen = set()
for z in itertools.product(L, repeat=7):
    c = min(tuple(z[i:] + z[:i]) for i in range(7))
    if c in seen or 5 not in z: continue
    seen.add(c)
    co = [(sk(z[i - 1], 7, z[(i + 1) % 7]), 1.0) for i in range(7) if z[i] == 5]
    row(co, -np.inf, 1.0)
# d >= 8 potential
for a in L:
    for b in L:
        for c in L:
            co = [(PH[(a, b)], 1.0), (PH[(b, c)], -1.0)]
            if b == 5: co.append((sk(a, 8, c), 1.0))
            row(co, -np.inf, 0.25)
# sender
def sends(w, sig=None):
    co = []
    for i in range(5):
        if w[i] >= 7: co.append((sk(w[i - 1], w[i], w[(i + 1) % 5]), 1.0))
    if sig is None: return co
    return sum(sig[j] for j, _ in co)
for w in words:
    co = sends(w) + [(WZ[w], 1.0)]
    row(co, 1.0, np.inf)
cost = np.zeros(NV)
for w in words:
    cost[WZ[w]] = 0.0 if (frame_only and forbidden(w)) else 1.0
cost[:len(keys)] += 1e-4  # tie-break: small sigma
integ = np.zeros(NV); lb = np.zeros(NV); ub = np.full(NV, np.inf)
for i in range(len(keys), W0): lb[i] = -np.inf  # phi free
for w in words: integ[WZ[w]] = 1; ub[WZ[w]] = 1
res = milp(c=cost, constraints=LinearConstraint(np.array(rows), lo, hi), integrality=integ, bounds=Bounds(lb, ub),
           options={'time_limit': 600})
print('status', res.status, res.message)
x = res.x; sig = x[:len(keys)]
print('sigma (p,D,q): value')
for k in keys:
    if sig[K[k]] > 1e-7: print('  ', k, round(sig[K[k]], 6))
S = [w for w in words if sends(w, sig) < 1 - 1e-7]
Sa = [w for w in S if not forbidden(w)]; Sf = [w for w in S if forbidden(w)]
print('|S| allowed words (no 555/565):', len(Sa), ' plus 555/565 words:', len(Sf), ' (universe %d + %d)' % (
    sum(1 for w in words if not forbidden(w)), sum(1 for w in words if forbidden(w))))
print('S (allowed):', ' '.join(fmt(w, CAP) for w in Sa))
json.dump({'sigma': {str(k): float(sig[K[k]]) for k in keys}, 'phi': {str(p): float(x[PH[p]]) for p in pairs},
           'S_allowed': [fmt(w, CAP) for w in Sa], 'S_forbidden': [fmt(w, CAP) for w in Sf]},
          open('out/discharge-%s.json' % ('frameonly' if frame_only else 'all'), 'w'), indent=1)
