"""B8 (exploratory): number of 2-ball keys (second-ring degrees 5..8, no symmetry reduction, no pruning) per hole
word by ring size; ring = sum_private (d-4) + sum_shared (d-5).  Usage: enum_count.py WORD..."""
import sys, collections
for w in sys.argv[1:]:
    d = [int(c) for c in w]; P = sum(x - 5 for x in d)
    poly = collections.Counter({0: 1})
    for parts in [(1, 2, 3, 4)] * P + [(0, 1, 2, 3)] * 5:
        nxt = collections.Counter()
        for r, c in poly.items():
            for a in parts: nxt[r + a] += c
        poly = nxt
    cum = lambda R: sum(c for r, c in poly.items() if r <= R)
    print(w, 'second ring', P + 5, ' <=14: %d  =15: %d  =16: %d  =17: %d  all: %d' % (cum(14), poly[15], poly[16], poly[17], sum(poly.values())))
