#!/usr/bin/env python3
"""Task 1 full check (3F-U = -5 sum w on EVERY class, orders 12-19) and Task 4 torus sanity."""
import sys, re, ast
from collections import Counter
sys.path.insert(0, '../common')
from kempe_py import Space, gentri_rotation, adj_from_rot
from escape import pi_of, GENTRI
tot = Counter()
for n in (12, 14, 16, 17, 18, 19):
    for gi, line in enumerate([l for l in open(GENTRI % n) if l.startswith('G')], 1):
        rot = gentri_rotation(line); adj = adj_from_rot(rot)
        for h in range(len(rot)):
            if len(rot[h]) != 5: continue
            try: sp = Space(adj, h, link=rot[h])
            except AssertionError: continue
            sp.build_graph(); cl, nc = sp.classes()
            S = len(sp.states); pi = [pi_of(sp, k) for k in range(S)]
            assert sorted(p[0] for p in pi) == list(range(S))
            for p in range(S): assert cl[pi[p][0]] == cl[p]
            lam = Counter(); U = Counter(); F = Counter()
            for k in range(S):
                lam[cl[k]] += pi[k][1]; (F if sp.filled(k) else U)[cl[k]] += 1
            for c in range(nc):
                assert 3 * F[c] - U[c] == -lam[c] and lam[c] % 5 == 0, (n, gi, h, c)
                tot[n] += 1
print('3F-U=-sum lambda, lambda sum = 0 mod 5: OK on all classes, per order:', dict(tot))
# torus
txt = open('../18-torus-floor/aggregate-output.txt').read()
faces = ast.literal_eval(re.search(r'faces = (\[\[.*\]\])', txt).group(1))
v = 11; link = [6, 15, 12, 8, 7]
adj = {}
for f in faces:
    for a in f:
        for b in f:
            if a != b: adj.setdefault(a, set()).add(b)
sp = Space(adj, v, link=link); sp.build_graph(); cl, nc = sp.classes()
lm = 0
for i in sp.linki: lm |= 1 << i
print('torus n=16 T-v: states', len(sp.states), 'classes', nc)
for c in range(nc):
    mem = [k for k in range(len(sp.states)) if cl[k] == c]
    nontriv = lp = 0
    for k in mem:
        for t, p, q, K in sp.moves(k):
            if t != k: nontriv += 1
            if t != k and not K & lm: lp += 1
    print(' class', c, 'size', len(mem), 'filled', sum(sp.filled(k) for k in mem), 'non-renaming swaps', nontriv, 'link-preserving non-renaming swaps', lp)
