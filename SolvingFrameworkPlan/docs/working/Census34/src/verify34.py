#!/usr/bin/env python3
"""Census34: second-engine check of R, NR and all-DL pi-cycles with TrackM's tm_lib.Hole (Track A kempe_py; read-only import).
usage: verify34.py GRAPHS.txt name:hole [...]
R  = longest run of interior states (DL, dNDL >= 2) along pi (and pinv); -1 if cyclic.
NR = longest run of DL states with Nch <= 9 along pi (and pinv); -1 if cyclic (NRC violation).
all-DL pi-cycles: lengths, and size / #filled of their Kempe class."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '../../TrackM')))
from tm_lib import Hole  # noqa: E402

def maxrun(S, f):
    best = 0
    for x in S:
        k = 0; y = x; seen = set()
        while y is not None and y in S:
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
    dl = {x for x in range(H.S) if not H.filled[x] and H.phi[x] == 2}
    inter = {x for x in dl if H.dNDL[x] >= 2}
    nr = {x for x in dl if H.Nch[x] <= 9}
    on = H.allDL_cycle_states(); cyc = []; done = set()
    for x in sorted(on):
        if x in done: continue
        L = 0; y = x
        while y not in done: done.add(y); L += 1; y = H.pi[y]
        c = H.cl[x]; cyc.append((L, sum(1 for s in range(H.S) if H.cl[s] == c), sum(1 for s in range(H.S) if H.cl[s] == c and H.filled[s])))
    print(f"{g} h={h} S={H.S} DL={len(dl)} interior={len(inter)} R(pi)={maxrun(inter, H.pi)} R(pinv)={maxrun(inter, H.pinv)} "
          f"NR(pi)={maxrun(nr, H.pi)} NR(pinv)={maxrun(nr, H.pinv)} allDLcycles={cyc}", flush=True)
