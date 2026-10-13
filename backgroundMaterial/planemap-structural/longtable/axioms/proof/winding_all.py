"""|winding| of every cubic vertex's matched edge along closed orbits (sign needs a rotation system;
|rho| does not).  rho(w) = (#forward - #backward steps)/3 w.r.t. any cyclic order of w's edges."""
import sys
from collections import Counter
sys.path.insert(0, '..')
from ax_lib import G5, parse_line
for path in sys.argv[1:]:
    for l in open(path):
        l = l.strip()
        if l.startswith('SOL'): l = l.split(' ', 1)[1].split('{')[0]
        if not l or not l[0].isdigit(): continue
        g = G5(*parse_line(l)); P, good, cyc = g.orbits()
        for c in cyc:
            if len(c) < 10: continue
            L = len(c); hist = Counter(); nbr = {g.other(e, g.v) for e in g.fv}; dist = Counter()
            for w in range(g.n):
                if w == g.v: continue
                inc = g.inc[w]; idx = {x: i for i, x in enumerate(inc)}
                word = [next(x for x in inc if x in c[t]) for t in range(L)]
                st = sum(1 if (idx[word[(t + 1) % L]] - idx[word[t]]) % 3 == 1 else -1 for t in range(L))
                hist[abs(st) // 3] += 1
                if w in nbr: dist['nbr', abs(st) // 3] += 1
            print(path.split('/')[-1], 'L', L, 'word', ''.join(map(str, g.word(c))), '|rho| hist', dict(hist), dict(dist))
