"""Collect near-rigid 1212 windows (length >= MINL) with planar quantities from sphere holes:
TrackS notable6 list (R-run >= 6 holes) and the Census33/34 maxima graphs (all degree-5 holes)."""
import sys, json, os, time
from pf_lib import Sphere, nr_windows, state_info
import tt_lib
W = '/Users/fulkanjou/GraphColour/SolvingFrameworkPlan/docs/working/'
MINL = int(sys.argv[1]) if len(sys.argv) > 1 else 5
specs = []
for l in open(W + 'TrackS/out/notable6.txt'):
    p = l.split()
    specs.append((W + p[0] if not p[0].startswith('/') else p[0], [s for s in p[1:]]))
for f in ('Census33/out/maxima_graphs.txt', 'Census34/out/maxima_graphs.txt'):
    G = tt_lib.load_graphs(W + f)
    specs.append((W + f, [f'{nm}:{h}' for nm, rot in G.items() for h in range(len(rot)) if len(rot[h]) == 5]))
seen = set()
for path, sl in specs:
    path2 = path if os.path.exists(path) else W + '../../../' + path.split('working/')[-1]
    if not os.path.exists(path2):
        alt = '/Users/fulkanjou/GraphColour/SolvingFrameworkPlan/docs/working/' + path.split('working/')[-1]
        path2 = alt
    names = {s.rsplit(':', 1)[0] for s in sl}
    try:
        G = tt_lib.load_graphs(path2, names)
    except FileNotFoundError:
        print('# missing', path, file=sys.stderr); continue
    for s in sl:
        nm, h = s.rsplit(':', 1); h = int(h)
        if nm not in G or (nm, h) in seen: continue
        seen.add((nm, h))
        sp = Sphere(G[nm], h)
        for w in nr_windows(sp):
            if len(w) < MINL: continue
            rows = [state_info(sp, P, M) for (P, M) in w]
            print(json.dumps(dict(g=nm, h=h, n=sp.g.n, L=len(w), word=''.join(str(r['kH']) for r in rows), states=rows)), flush=True)
