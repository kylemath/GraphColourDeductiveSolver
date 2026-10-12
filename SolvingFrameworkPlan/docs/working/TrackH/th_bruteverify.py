#!/usr/bin/env python3
"""Track H: brute-force check of a counterexample, with ABSOLUTE colourings (no renaming quotient, no shared code).
Finds every proper 4-colouring of G - h by backtracking, takes the Kempe class (BFS over all component swaps) of a
colouring whose link is (a, m, a, A, B), and reports: class size (absolute), #filled (link with <= 3 colours),
and for every unfilled class state: Lock1, Lock2, inA, inB, D1, D2, and P1-P3 parities (odd-G-degree counts).
usage: th_bruteverify.py FILE NAME HOLE"""
import sys
from collections import deque
p = None
for l in open(sys.argv[1]):
    q = l.split()
    if q and q[0] == sys.argv[2]: p = q
rot = [list(map(int, r.split(','))) for r in p[2].split(';')]; h = int(sys.argv[3]); n = len(rot)
X = rot[h]; V = [v for v in range(n) if v != h]; adj = {v: [w for w in rot[v] if w != h] for v in V}
assert all(v in rot[w] for v in range(n) for w in rot[v]), 'asymmetric'
assert all(X[(t + 1) % 5] in rot[X[t]] for t in range(5)) and all(X[(t + 2) % 5] not in rot[X[t]] for t in range(5)), 'link not an induced 5-cycle'
order = sorted(V, key=lambda v: -len(adj[v])); cols = []
c = {}
def rec(i):
    if i == len(order): cols.append(tuple(c[v] for v in V)); return
    v = order[i]; forb = {c[w] for w in adj[v] if w in c}
    for a in range(4):
        if a not in forb: c[v] = a; rec(i + 1); del c[v]
sys.setrecursionlimit(10000); rec(0)
pos = {v: i for i, v in enumerate(V)}
def comp(col, s, pair):
    seen = {s}; st = [s]
    while st:
        u = st.pop()
        for w in adj[u]:
            if w not in seen and col[pos[w]] in pair: seen.add(w); st.append(w)
    return seen
def link(col): return [col[pos[x]] for x in X]
start = next(s for s in cols if len(set(link(s))) == 4)
seen = {start}; dq = deque([start])
while dq:
    s = dq.popleft()
    for a in range(4):
        for b in range(a + 1, 4):
            left = {v for v in V if s[pos[v]] in (a, b)}
            while left:
                v0 = next(iter(left)); K = comp(s, v0, (a, b)); left -= K
                t = list(s)
                for v in K: t[pos[v]] = b if s[pos[v]] == a else a
                t = tuple(t)
                if t not in seen: seen.add(t); dq.append(t)
odd = {v for v in V if len(rot[v]) % 2}
F = 0; bad = {'D1': 0, 'D2': 0, 'P1': 0, 'P2': 0, 'P3': 0, 'notDL': 0}
for s in seen:
    lk = link(s)
    if len(set(lk)) <= 3: F += 1; continue
    j = next(t for t in range(5) if lk[t] == lk[(t + 2) % 5]); x = [X[(j + k) % 5] for k in range(5)]
    al, mu, A, B = lk[j], lk[(j + 1) % 5], lk[(j + 3) % 5], lk[(j + 4) % 5]
    L1 = x[3] in comp(s, x[1], (mu, A)); L2 = x[4] in comp(s, x[1], (mu, B))
    KA = comp(s, x[2], (al, A)); KB = comp(s, x[2], (al, B)); KM = comp(s, x[2], (al, mu))
    inA, inB = x[0] in KA, x[0] in KB
    bad['notDL'] += not (L1 and L2); bad['D1'] += L1 != (not inB); bad['D2'] += L2 != (not inA)
    bad['P1'] += (len(KA & odd) % 2 == 1) != (not inA); bad['P2'] += (len(KB & odd) % 2 == 1) != (not inB); bad['P3'] += len(KM & odd) % 2 != 1
print(f'n={n} colourings(absolute)={len(cols)} class(absolute)={len(seen)} = {len(seen) / 24:g} x 24  filled={F}  failures={bad}')
