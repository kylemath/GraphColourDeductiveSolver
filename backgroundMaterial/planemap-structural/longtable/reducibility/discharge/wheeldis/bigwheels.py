"""Receiver wheels (exploratory): c-wheels for c = 7, 8 (centre degree c, link word over {5,6,7,8}), up to rotation and
reflection, ring = sum(word) - 4c <= RMAX.  Same builder as studio17/gen_wheels17.py.  Writes bigwheels.txt.
Usage: python3 bigwheels.py [RMAX=14]"""
import sys, itertools, os
HERE = os.path.dirname(os.path.abspath(__file__))
RMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 14
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
for c in (7, 8):
    for w in itertools.product((5, 6, 7, 8), repeat=c):
        if sum(w) - 4 * c > RMAX: continue
        k = canon(list(w))
        if k in seen: continue
        seen.add(k); r, m, ra, ia = wheel(list(k))
        out.append((r, 'c%d_%s' % (c, ''.join(map(str, k))), m, ra, ia))
out.sort()
with open(os.path.join(HERE, 'bigwheels.txt'), 'w') as f:
    for r, nm, m, ra, ia in out: f.write('%s %d %d %s %s\n' % (nm, r, m, fmt(ra), fmt(ia)))
import collections
print(len(out), sorted(collections.Counter((nm[:2], r) for r, nm, *_ in out).items()))
