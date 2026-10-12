#!/usr/bin/env python3
"""Track H: component-count vectors (am, AB, aA, mB, aB, mA) and cycle ranks over all unfilled states of a hole;
checks the Euler identity  c_k - beta_k = chi + [k != 1]  per partition (k=1: {am|AB}, 2: {aA|mB}, 3: {aB|mA}),
where chi = n - e + f of the closed triangulated surface (f = 2e/3), and counts 'rigid' states (vector (1,1,2,1,2,1)).
usage: th_rigid.py FILE NAME HOLE"""
import sys
from collections import Counter
from th_engine import read_graphs, Hole
g = read_graphs(sys.argv[1])[sys.argv[2]]; h = int(sys.argv[3]); H = Hole(g, h)
n = len(g); e = sum(len(a) for a in g) // 2; chi = n - e + (2 * e) // 3
vec = Counter(); euler_bad = 0; rigid = Counter()
for i in range(len(H.states)):
    col = H.col(i); lk = [col[x] for x in H.X]
    if len(set(lk)) <= 3: continue
    j = next(t for t in range(5) if lk[t] == lk[(t + 2) % 5]); al, mu, A, B = lk[j], lk[(j + 1) % 5], lk[(j + 3) % 5], lk[(j + 4) % 5]
    cs = []; bs = []
    for pr in [(al, mu), (A, B), (al, A), (mu, B), (al, B), (mu, A)]:
        left = {v for v in H.V if col[v] in pr}; k = 0; Vn = len(left)
        while left:
            s = next(iter(left)); left -= H.comp(col, s, pr); k += 1
        E = sum(1 for v in H.V for w in H.adj[v] if w > v and col[v] in pr and col[w] in pr)
        cs.append(k); bs.append(E - Vn + k)
    for kk, d in [(0, 0), (2, 1), (4, 1)]:
        euler_bad += (cs[kk] + cs[kk + 1]) - (bs[kk] + bs[kk + 1]) != chi + d
    vec[tuple(cs)] += 1
    if tuple(cs) == (1, 1, 2, 1, 2, 1): rigid[(bs[0], bs[1], bs[2], bs[3], bs[4], bs[5])] += 1
print(sys.argv[2], 'chi', chi, 'unfilled', sum(vec.values()), 'euler_bad', euler_bad, 'rigid', sum(rigid.values()), dict(rigid))
print('  most common vectors', vec.most_common(6))
