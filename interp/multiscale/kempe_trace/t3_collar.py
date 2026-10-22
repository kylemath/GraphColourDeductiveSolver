import json, sys, time, random
sys.path.insert(0, '/mnt/project-files/multiscale/kempe_trace'); sys.path.insert(0, '/mnt/project-files/multiscale/opus_attack/bandfill')
from kt import *; from collar import *; from t2_tubes import sat_colour, annulus
import sphere as SP
d = json.load(open('/mnt/project-files/multiscale/opus_attack/bandfill/sphere_L18_w4.json'))
g = SP.G(); g.adj = [set(a) for a in d['adj']]; adj = g.adj
g.tris = [(u, v, w) for u in range(len(adj)) for v in adj[u] if v > u for w in adj[u] & adj[v] if w > v]
L = 18; n = len(adj); A = set(d['A']); B = set(range(n)) - A; m = d['seam_row_A']
colA = {int(k): v for k, v in d['colA'].items()}; colB = {int(k): v for k, v in d['colB'].items()}
bdA = [m*L + i for i in range(L)]; bdB = [(m+1)*L + i for i in range(L)]
out = {}
WS = [int(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 else [2, 3, 4, 5, 6]
print('== T1: min window width k reachable by recolouring the collar (rows depth 1..w-1), Opus sphere ==')
base = {nm: summary(traces(adj, S, c, bd), L)['maxspan'] + 1 for nm, S, c, bd in (('A', A, colA, bdA), ('B', B, colB, bdB))}
print('current k (maxspan+1):', base)
out['T1'] = {'current': base}
for nm, S, c, bd in (('A', A, colA, bdA), ('B', B, colB, bdB)):
    for w in WS:
        t0 = time.time(); k, r, sm = min_window(adj, S, c, bd, w)
        nfree = len(Collar(adj, S, c, bd, w).free)
        print(f'side {nm} w={w} free={nfree}  min k = {k}  blocks {sm["nblocks"] if sm else None} depth {sm["depth"] if sm else None}  ({time.time()-t0:.1f}s)', flush=True)
        out['T1'][f'{nm}_w{w}'] = dict(k=k, nfree=nfree, summary={kk: v for kk, v in sm.items() if kk != 'per_pair'} if sm else None)
# T2: easy sides with the SAME seam word.  Random re-extensions of A (seam row fixed) against the fixed Opus B.
print('== T2: random A\' with the same seam word vs Opus B: W_band; traces of A\'; collar-reproducibility ==')
rng = random.Random(11); out['T2'] = []
for trial in range(int(sys.argv[2]) if len(sys.argv) > 2 else 6):
    t0 = time.time()
    cA2 = sat_colour(adj, A, {v: colA[v] for v in bdA}, rng, nrand=12)
    res = SP.closing(g, A, B, cA2, colB, set(bdA) | set(bdB), Wmax=3)
    tr = traces(adj, A, cA2, bdA); sm = summary(tr, L)
    rec = dict(trial=trial, W_band=res['W_band'], R=res['R_conf'], summary={k: v for k, v in sm.items() if k != 'per_pair'}, traces={str(p): b for p, b in tr.items()}, exact_w={})
    print(f"A' trial {trial}: W_band={res['W_band']} R={res['R_conf']} blocks {sm['nblocks']} single {sm['nsingle']} depth {sm['depth']} maxspan {sm['maxspan']} ({time.time()-t0:.0f}s)", flush=True)
    if res['W_band'] is not None and res['W_band'] <= 2:
        for w in WS:
            t1 = time.time(); r = exact(adj, A, colA, bdA, w, tr)
            rec['exact_w'][w] = r is not None
            print(f"   collar w={w} on Opus A reproduces A' traces exactly: {r is not None} ({time.time()-t1:.1f}s)", flush=True)
            if r is not None:
                res2 = SP.closing(g, A, B, r, colB, set(bdA) | set(bdB), Wmax=3)
                rec['exact_w'][f'{w}_Wband_after'] = res2['W_band']; print(f"      closing of normalised A vs B: W_band={res2['W_band']} R={res2['R_conf']}", flush=True)
                break
    out['T2'].append(rec)
    json.dump(out, open('t3_sphere.json', 'w'), indent=1)
json.dump(out, open('t3_sphere.json', 'w'), indent=1)
