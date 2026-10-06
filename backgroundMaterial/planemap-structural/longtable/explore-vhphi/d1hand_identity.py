"""EXPLORATORY (D1-Hand). Numerical sanity check of two hand identities, for EVERY proper 4-colouring of T-x
(all colourings up to renaming, 17:0 and 17:1, a few degree-5 vertices x), no lock needed:
  (I1) sum over the 6 colour pairs of (components - cyclomatic number) of the pair subgraph of T-x equals 8;
  (I2) for each colour class i:  sum_{v in V_i}(deg_T v - 5) = (n-1) + r_i - 3 n_i - kappa_i,
       kappa_i = sum_{j != i}(comps_ij - cyc_ij), r_i = number of ring vertices of x in class i.
Usage: python3 d1hand_identity.py PLANTRI"""
import sys, itertools, subprocess
import tilley_apex as TA
from d1hand_lib import pair_stats

plantri = sys.argv[1]
bad1 = bad2 = tot = 0
for gi in (0, 1):
    line = subprocess.run([plantri, "-m5", "17", "-a"], capture_output=True, text=True).stdout.splitlines()[gi]
    rot = TA.parse(line); N = len(rot); adj = [set(r) for r in rot]
    for x in [v for v in range(N) if len(rot[v]) == 5][:3]:
        Gx = [set(a) - {x} for a in adj]; Gx[x] = set()
        verts = [v for v in range(N) if v != x]
        # colourings of T-x: colour with vertex x isolated -> canon over all N entries; x gets colour 0 (ignored)
        import random
        allc = TA.colourings(Gx, N)
        random.seed(1); random.shuffle(allc)
        for c in allc[:4000]:
            c = list(c); tot += 1
            ps = pair_stats(adj, c, x, N)
            if sum(v[0] - v[1] for v in ps.values()) != 8: bad1 += 1
            for i in range(4):
                Vi = [w for w in verts if c[w] == i]
                if not Vi: continue
                lhs = sum(len(adj[w]) - 5 for w in Vi)
                ri = sum(1 for w in rot[x] if c[w] == i)
                kap = sum(ps[tuple(sorted((i, j)))][0] - ps[tuple(sorted((i, j)))][1] for j in range(4) if j != i)
                if lhs != (N - 1) + ri - 3 * len(Vi) - kap: bad2 += 1
print("colourings tested", tot, "I1 failures", bad1, "I2 failures", bad2)
