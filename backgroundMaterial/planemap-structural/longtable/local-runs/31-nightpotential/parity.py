"""[exploratory] NightPotential: is (#Kempe components over the six pairs) mod 2 a function of the link colouring alone?  gentri order 16-18, all colourings."""
import sys, os, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../30-nighta34'))
from eng import H as EH, graphs, holes6
from openruns import ncomp, PAIRS
from collections import Counter, defaultdict
T = Counter(); bad = 0
for n in (17, 18, 19):
    for gi, rot in graphs(n):
        for h in holes6(rot):
            pass
            Hh = EH(rot, h); seen = defaultdict(set)
            for c in Hh.sp.states:
                lc = tuple(c[x] for x in Hh.X); mp = {}; key = tuple(mp.setdefault(t, len(mp)) for t in lc)
                N = sum(ncomp(Hh, c, a, b) for a, b in PAIRS)
                # arcs-joined count for each pair
                seen[key].add(N % 2); T[(key, N % 2)] += 1
            bad += sum(1 for k, v in seen.items() if len(v) > 1)
            T['holes'] += 1
            if T['holes'] > 60: break
        if T['holes'] > 60: break
print('link patterns with both parities:', bad)
for k in sorted((k for k in T if k != 'holes'), key=str): print(k, T[k])
