"""[exploratory] NightPotential: parity of dN (N = # Kempe components over six pairs) under an arbitrary Kempe swap, vs how the swapped component meets the link."""
import sys, os, itertools, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../30-nighta34'))
from eng import H as EH, graphs, holes6
from openruns import ncomp, PAIRS
from collections import Counter
random.seed(1); T = Counter(); nh = 0
for n in (18, 19):
    for gi, rot in graphs(n):
        for h in holes6(rot):
            Hh = EH(rot, h); nh += 1
            for c in random.sample(Hh.sp.states, min(40, len(Hh.sp.states))):
                N0 = sum(ncomp(Hh, c, a, b) for a, b in PAIRS)
                for a, b in PAIRS:
                    seen = set()
                    for v in range(Hh.N):
                        if c[v] in (a, b) and v not in seen:
                            K = Hh.comp(c, v, a, b); seen |= K
                            d = Hh.swap(c, K, a, b); N1 = sum(ncomp(Hh, d, x, y) for x, y in PAIRS)
                            inl = [x in K for x in Hh.X]
                            arcs = sum(1 for q in range(5) if inl[q] and not inl[q-1]) if not all(inl) else 9
                            # link colour change count
                            T[('|K∩link|', sum(inl), 'dN mod 2', (N1 - N0) % 2)] += 1
                            lc0 = len(set(c[x] for x in Hh.X)); lc1 = len(set(d[x] for x in Hh.X))
                            T[('link #colours', lc0, '->', lc1, 'dN mod 2', (N1 - N0) % 2)] += 1
            if nh >= 40: break
        if nh >= 40: break
    if nh >= 40: break
for k in sorted(T, key=str): print(k, T[k])
