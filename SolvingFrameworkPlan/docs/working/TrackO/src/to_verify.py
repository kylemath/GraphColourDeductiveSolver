#!/usr/bin/env python3
"""TrackO: second, independent computation of R with TrackM's tm_lib.py (Track A's kempe_py engine; read-only import).
usage: to_verify.py GRAPHS.txt name:hole [name:hole ...]
Interior = DL with dNDL >= 2 (no filled / non-DL state within one Kempe swap), exactly as TrackM's tm_run.py;
R = longest run of consecutive interior states along H.pi (-1 if an interior pi-cycle exists); also along H.pinv.
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '../../TrackM')))
from tm_lib import Hole  # noqa: E402


def maxrun(inter, f):
    best = 0
    for x in inter:
        k = 0; y = x; seen = set()
        while y is not None and y in inter:
            if y in seen: return -1
            seen.add(y); k += 1; y = f[y]
        best = max(best, k)
    return best


graphs = {}
for l in open(sys.argv[1]):
    p = l.split()
    if len(p) >= 3: graphs[p[0]] = [list(map(int, r.split(','))) for r in p[2].split(';')]
for spec in sys.argv[2:]:
    g, h = spec.rsplit(':', 1); h = int(h)
    H = Hole(graphs[g], h); H.classes_and_dist()
    inter = {x for x in range(H.S) if H.dNDL[x] >= 2}
    nDL = sum(1 for x in range(H.S) if not H.filled[x] and H.phi[x] == 2)
    print(f"{g} h={h} S={H.S} DL={nDL} interior={len(inter)} R(pi)={maxrun(inter, H.pi)} R(pinv)={maxrun(inter, H.pinv)}", flush=True)
