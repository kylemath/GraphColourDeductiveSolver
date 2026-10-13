import sys
from collections import Counter
from win_lib import load
for path in sys.argv[1:]:
    ws = load(path); c = Counter()
    for w in ws:
        for t in range(1, w.W, 2):
            seq, pos, p = w.ham_positions(t)
            c['e0e1_uncrossed' if p[1] < p[0] else 'e0e1_crossed'] += 1
    print(path, len(ws), dict(c))
