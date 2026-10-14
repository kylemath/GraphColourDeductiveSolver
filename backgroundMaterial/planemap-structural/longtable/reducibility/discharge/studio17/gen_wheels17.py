#!/usr/bin/env python3
"""Studio Job 17 (exploratory): wheel configurations for the C-reducibility census.
A c-wheel = centre of degree c (interior 0) + its c neighbours x_0..x_{c-1} (interior 1..c) with degrees word[i];
ring as in wheels.py: x_i sees s_{i-1}, (d_i - 5) private ring vertices, s_i; ring length = sum(word) - 4c.
Words up to rotation and reflection: c = 5 over {5,6,7,8}, c = 6 over {5,6,7}; ring <= 16.  Writes wheels17.txt."""
import itertools
def canon(w):
    c = []
    for s in (w, w[::-1]):
        for k in range(len(s)): c.append(tuple(s[k:] + s[:k]))
    return min(c)
def wheel(word):
    c = len(word); ring = []
    for i, d in enumerate(word):
        for p in range(d - 5): ring.append(('p', i, p))
        ring.append(('s', i))
    pos = {v: k for k, v in enumerate(ring)}; m = c + 1
    ra = [[] for _ in range(m)]; ia = [[] for _ in range(m)]
    for i, d in enumerate(word):
        a = 1 + i
        ra[a] = [pos[('s', (i - 1) % c)]] + [pos[('p', i, p)] for p in range(d - 5)] + [pos[('s', i)]]
        ia[a] = [0, 1 + (i + 1) % c, 1 + (i - 1) % c]
    ia[0] = list(range(1, c + 1))
    return len(ring), m, ra, ia
fmt = lambda L: ';'.join(','.join(map(str, x)) if x else '-' for x in L)
seen = set(); out = []
for c, alph in ((5, (5, 6, 7, 8)), (6, (5, 6, 7))):
    for w in itertools.product(alph, repeat=c):
        k = canon(list(w))
        if k in seen: continue
        seen.add(k)
        r, m, ra, ia = wheel(list(k))
        if r > 16: continue
        out.append((c, r, 'c%d_%s' % (c, ''.join(map(str, k))), m, ra, ia))
out.sort(key=lambda x: (x[1], x[2]))
with open('wheels17.txt', 'w') as f:
    for c, r, nm, m, ra, ia in out: f.write('%s %d %d %s %s\n' % (nm, r, m, fmt(ra), fmt(ia)))
import collections
print(len(out), collections.Counter((c, r) for c, r, *_ in out))
