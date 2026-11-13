import sys, collections, random, time; sys.path.insert(0, '/tmp/swarm-W16/code')
import torus as TT, w16lib as W, explore as X, clusters as CL
from lp_patterns import lab_str
W.init()
def reasons(T):
    out = []
    for v in range(T.n):
        d = T.deg[v]
        if d < 5 or d > 9: out.append(('deg', d)); continue
        w0, s0, _, _ = TT.words(T, v)
        if min(w0) < 5 or min(s0) < 5: out.append(('deg4nb', d)); continue
        lab = W.vertex_row(T, v); st = W.row_status(lab)
        if st: out.append((st, lab_str(lab))); continue
        if d >= 7:
            w, s, r, ap = TT.words(T, v); pv = W.privates(T, v)
            if any(min(x) < 5 for x in pv if x): out.append(('deg4priv', d)); continue
            k = W.payee_kills(d, w, s, pv)
            if k: out.append(('kill' + ','.join(x[1] for x in k), lab_str(lab)))
    return out
# random flip clusters of k flips in the 6x6 lattice, tally reasons
random.seed(1); tally = collections.Counter(); best = []
for trial in range(400):
    T = TT.lattice_torus(6, 0, 6); touched = set()
    k = random.choice([3, 4, 5, 6])
    for _ in range(k):
        cand = CL.near_edges(T, touched, 1) if touched else [(0, 1)]
        u, v = random.choice(cand); a = T.opp.get((u, v)); b = T.opp.get((v, u))
        if a is not None and T.flip(u, v): touched |= {u, v, a, b}
    R = reasons(T)
    if any(r[0] in ('deg', 'deg4nb', 'deg4priv') for r in R): continue
    for r in R: tally[r[0]] += 1
    best.append((len(R), R))
best.sort(key=lambda x: x[0])
print('tally', tally.most_common())
for n, R in best[:8]: print(n, R)
