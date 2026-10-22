# Collar normalisation on the tube counterexample halves: min window width k reachable vs collar width w, per L.
import json, sys, time
sys.path.insert(0, '/mnt/project-files/multiscale/kempe_trace'); sys.path.insert(0, '/mnt/project-files/multiscale/opus_attack/bandfill')
from kt import *; from collar import *; from t2_tubes import annulus
from tube import band_graph
from csp import solve
EXT = 2
def extend_below(a, extra):
    L = len(a); n, e, t = band_graph(L, extra+1)
    dom = [set(range(4)) for _ in range(n)]
    for i in range(L): dom[extra*L+i] = {int(a[i])}
    sol = solve(n, e, t, dom); assert sol is not None
    return [''.join(map(str, sol[k*L:(k+1)*L])) for k in range(extra)]
ce = json.load(open('/mnt/project-files/multiscale/opus_attack/bandfill/counterexamples.json'))
out = []
for c in sorted(ce, key=lambda c: c['L']):
    L, w0 = c['L'], c['w']
    for side in 'AB':
        rows = c['A_rows_depth_w_to_seam'] if side == 'A' else [r[::-1] for r in reversed(c['B_rows_seam_to_depth_w'])]
        # side B rows are seam->depth; (k,i)->(-k,-i) is a tube automorphism, so reverse the row order and each row
        rows = extend_below(rows[0], EXT) + rows
        adj, col = annulus(rows); n = len(col); assert all(col[u] != col[v] for u in range(n) for v in adj[u]); seam = len(rows)-1; bd = [seam*L + i for i in range(L)]; S = set(range(n))
        base = summary(traces(adj, S, col, bd), L)
        rec = dict(L=L, wstar=w0, side=side, depth_rows=len(rows)-1, k_current=base['maxspan']+1, blocks=base['nblocks'], k_by_w={})
        line = f"L={L} w*={w0} {side}: current k={base['maxspan']+1} blocks={base['nblocks']} depth={base['depth']};"
        for w in range(2, len(rows)+1):
            t0 = time.time(); k, r, sm = min_window(adj, S, col, bd, w)
            rec['k_by_w'][w] = k; line += f" w{w}:k={k}"
        print(line, flush=True); out.append(rec)
        json.dump(out, open('t3_tubes.json', 'w'), indent=1)
