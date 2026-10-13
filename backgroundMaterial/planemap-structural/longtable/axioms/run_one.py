import sys, json, time
from ax_lib import *
src = sys.argv[1]
for li, line in enumerate(open(src)):
    if not line.strip(): continue
    g = G5(*parse_line(line))
    t0=time.time(); P, good, cyc = g.orbits()
    print(f"graph {li}: n={g.n} pm={len(P)} dl={len(good)} cycles={len(cyc)} planar={planar(g)} planar_rot={planar_rot(g)} ballr={ball_planar_radius(g)} t={time.time()-t0:.1f}s")
    for c in cyc:
        r = orbit_axioms(g, c)
        print(json.dumps(r))
