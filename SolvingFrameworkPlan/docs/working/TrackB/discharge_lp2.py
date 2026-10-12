#!/usr/bin/env python3
"""[Track B] Most general ONE-STEP word-local discharging: a 5-vertex y sends to each neighbour u of degree >= 7 an amount
sigma[D; a, b, c, e] that depends on its whole capped word read starting at u: y's rotation is u, a, b, c, e
(a, e = the two common neighbours of y and u; b, c = y's two neighbours not adjacent to u). D = min(deg u, 8). Reflection
symmetric: sigma[D;a,b,c,e] = sigma[D;e,c,b,a].

Receiver at u of degree d, link z_1..z_d, outer apexes w_i (face z_i z_{i+1} w_i, w_i != u): the 5-neighbour z_i has
rotation u, z_{i+1}, w_i, w_{i-1}, z_{i-1}, so it sends sigma[D; z_{i+1}, w_i, w_{i-1}, z_{i-1}].
Conditions (over ALL degree sequences, a superset of the realisable ones):
  d = 7 : every cyclic sequence of 7 pairs (z_i, w_i) receives <= 1        (cutting planes; separation by max-plus DP)
  d >= 8: max cycle mean <= 1/4 in the state graph (z_{i-1},w_{i-1},z_i,w_i) -> (z_i,w_i,z_{i+1},w_{i+1}), certified by a
          potential phi (LP rows), so a degree-d vertex receives <= d/4 <= d-6.
Sender: word w sends s(w) = sum over its letters >= 7.  S = {w : s(w) < 1} is unavoidable (Euler: total charge 12 > 0).
Usage: python3 discharge_lp2.py [--frame-only]"""
import itertools, sys, json, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from words import canon, fmt

L = [5, 6, 7, 8]; frame_only = '--frame-only' in sys.argv
def key(D, a, b, c, e): return min((D, a, b, c, e), (D, e, c, b, a))
keys = sorted({key(D, *t) for D in (7, 8) for t in itertools.product(L, repeat=4)})
K = {k: i for i, k in enumerate(keys)}; nk = len(keys)
states = list(itertools.product(L, repeat=4)); SI = {s: i for i, s in enumerate(states)}; ns = len(states)
PH0 = nk
words = sorted({canon(list(w)) for w in itertools.product(L, repeat=5)})
def forbidden(w): return any((w[i - 1], w[i], w[(i + 1) % 5]) in ((5, 5, 5), (5, 6, 5)) for i in range(5))
WZ0 = nk + ns; WZ = {w: WZ0 + i for i, w in enumerate(words)}; NV = WZ0 + len(words)
def sender_keys(w):
    out = []
    for i in range(5):
        if w[i] >= 7: out.append(K[key(w[i], w[(i + 1) % 5], w[(i + 2) % 5], w[(i + 3) % 5], w[(i + 4) % 5])])
    return out
from scipy.sparse import lil_matrix
base_rows = []  # list of (dict, lo, hi)
# potential rows for D = 8: transition (z0,w0,z1,w1) -> (z1,w1,z2,w2), weight [z1==5] sigma[8; z2, w1, w0, z0]
for (z0, w0, z1, w1) in states:
    for z2 in L:
        for w2 in L:
            d = {PH0 + SI[(z0, w0, z1, w1)]: 1.0}
            j = PH0 + SI[(z1, w1, z2, w2)]; d[j] = d.get(j, 0) - 1.0
            if z1 == 5: kk = K[key(8, z2, w1, w0, z0)]; d[kk] = d.get(kk, 0) + 1.0
            base_rows.append((d, -np.inf, 0.25))
for w in words:
    d = {}
    for kk in sender_keys(w): d[kk] = d.get(kk, 0) + 1.0
    d[WZ[w]] = d.get(WZ[w], 0) + 1.0
    base_rows.append((d, 1.0, np.inf))
cuts = []
def seq_row(seq):  # seq: list of 7 (z,w) pairs, cyclic
    d = {}
    for i in range(7):
        z, w = seq[i]
        if z != 5: continue
        zp, wp = seq[i - 1]; zn, _ = seq[(i + 1) % 7]
        kk = K[key(7, zn, w, wp, zp)]; d[kk] = d.get(kk, 0) + 1.0
    return d
def solve():
    R = base_rows + [(c, -np.inf, 1.0) for c in cuts]
    A = lil_matrix((len(R), NV)); lo = []; hi = []
    for r, (d, l, h) in enumerate(R):
        for j, v in d.items(): A[r, j] = v
        lo.append(l); hi.append(h)
    cost = np.zeros(NV)
    for w in words: cost[WZ[w]] = 0.0 if (frame_only and forbidden(w)) else 1.0
    cost[:nk] += 1e-5
    integ = np.zeros(NV); lb = np.zeros(NV); ub = np.full(NV, np.inf)
    lb[PH0:PH0 + ns] = -np.inf; ub[:nk] = 1.0
    for w in words: integ[WZ[w]] = 1; ub[WZ[w]] = 1
    res = milp(c=cost, constraints=LinearConstraint(A.tocsr(), lo, hi), integrality=integ, bounds=Bounds(lb, ub),
               options={'time_limit': 900})
    return res
def separate(sig):
    """max over cyclic sequences of 7 pairs of the received amount; returns (value, seq)"""
    # transition weight matrix over states (z0,w0,z1,w1)->(z1,w1,z2,w2)
    W = np.full((ns, ns), -np.inf)
    for (z0, w0, z1, w1) in states:
        i = SI[(z0, w0, z1, w1)]
        for z2 in L:
            for w2 in L:
                W[i, SI[(z1, w1, z2, w2)]] = sig[K[key(7, z2, w1, w0, z0)]] if z1 == 5 else 0.0
    best = (-1, None); viol = []
    # closed walks of length 7: max-plus power with argmax tracking, per start state
    for s0 in range(ns):
        val = W[s0].copy(); back = [np.full(ns, s0)]
        for step in range(6):
            M = val[:, None] + W
            arg = M.argmax(0); val = M[arg, np.arange(ns)]; back.append(arg)
        if val[s0] > best[0] + 1e-12:
            # reconstruct
            path = [s0]; cur = s0
            for step in range(6, -1, -1):
                prev = back[step][cur] if step > 0 else s0
                path.append(prev); cur = prev
            path = path[::-1]  # states s0 .. s0 (8 entries)
            seq = [states[p][2:] for p in path[1:]]  # (z_i, w_i) for i = 1..7
            best = (val[s0], seq)
        if val[s0] > 1 + 1e-7 and len(viol) < 40:
            path = [s0]; cur = s0
            for step in range(6, -1, -1):
                prev = back[step][cur] if step > 0 else s0
                path.append(prev); cur = prev
            path = path[::-1]; viol.append([states[p][2:] for p in path[1:]])
    return best[0], best[1], viol
t0 = time.time()
for it in range(200):
    res = solve()
    sig = res.x[:nk]
    v, seq, viol = separate(sig)
    nS = sum(1 for w in words if res.x[WZ[w]] > 0.5 and not (frame_only and forbidden(w)))
    print('iter', it, 'status', res.status, '|S| objective', nS, 'max d=7 receipt', round(v, 4), 'cuts', len(cuts),
          '%.0fs' % (time.time() - t0), flush=True)
    if v <= 1 + 1e-7: break
    for sq in viol: cuts.append(seq_row(sq))
S = [w for w in words if sum(sig[k] for k in sender_keys(w)) < 1 - 1e-7]
Sa = [w for w in S if not forbidden(w)]; Sf = [w for w in S if forbidden(w)]
print('FINAL |S| allowed:', len(Sa), ' 555/565 words in S:', len(Sf))
print('S (allowed):', ' '.join(fmt(w, 8) for w in Sa))
json.dump({'sigma': {str(k): float(sig[K[k]]) for k in keys if sig[K[k]] > 1e-9},
           'phi': {str(s): float(res.x[PH0 + SI[s]]) for s in states},
           'S_allowed': [fmt(w, 8) for w in Sa], 'S_forbidden': [fmt(w, 8) for w in Sf]},
          open('out/discharge2-%s.json' % ('frameonly' if frame_only else 'all'), 'w'), indent=1)
