"""At every Hamiltonian state of the given windows: bits (b_{t-1}, b_t) and the order type of the far ends
p1, p3, p0 of e1, e3, e0 along H_t (positions from the e2-neighbour)."""
import sys
from collections import Counter, defaultdict
from win_lib import load
tab = defaultdict(Counter)
for path in sys.argv[1:]:
    for w in load(path):
        for t in range(1, w.W, 2):
            seq, pos, p = w.ham_positions(t)
            b = (int(w.state(t - 1)['a5v']), int(w.state(t)['a5v']))
            order = ''.join(sorted('013', key=lambda c: p[int(c)]))
            tab[b][order] += 1
for b in sorted(tab): print(b, dict(sorted(tab[b].items())))
