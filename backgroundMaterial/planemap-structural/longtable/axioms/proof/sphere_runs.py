"""Near-rigid (1212) windows at census record holes, with planar quantities per state.
usage: sphere_runs.py GRAPHFILE name:hole ... > out.jsonl"""
import sys, json, time
from pf_lib import Sphere, nr_windows, state_info
import tt_lib

G = tt_lib.load_graphs(sys.argv[1], {s.rsplit(':', 1)[0] for s in sys.argv[2:]})
for spec in sys.argv[2:]:
    nm, h = spec.rsplit(':', 1); h = int(h)
    t0 = time.time()
    sp = Sphere(G[nm], h)
    W = nr_windows(sp)
    W.sort(key=len, reverse=True)
    for w in W[:6]:
        rows = [state_info(sp, P, M) for (P, M) in w]
        print(json.dumps(dict(g=nm, h=h, n=sp.g.n, L=len(w), word=''.join(str(r['kH']) for r in rows),
                              states=rows)), flush=True)
    print(f'# {spec} windows={len(W)} maxlen={len(W[0]) if W else 0} {time.time()-t0:.1f}s', file=sys.stderr, flush=True)
