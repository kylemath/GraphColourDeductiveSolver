# Adversarial complement to t4_cap: for a fixed (capped / uncapped) level seam word, can SOME proper interior (annulus of
# depth D, all rows free) realise nesting depth 3 for pair (0,1) [blocks (i1,i6) > (i2,i5) > (i3,i4)]?  Then depth 2.
import json, sys, random, time, itertools
sys.path.insert(0, '/mnt/project-files/multiscale/kempe_trace'); sys.path.insert(0, '/mnt/project-files/multiscale/opus_attack/bandfill')
from kt import *; from collar import Collar; from t2_tubes import random_level_row
from tube import band_graph, maxrun
D = 8; NW = int(sys.argv[1]) if len(sys.argv) > 1 else 12; rng = random.Random(21); out = []
def feasible(adj, S, col, bd, L, blocks):
    P = {p: [] for p in PAIRS}; P[(0, 1)] = blocks
    C = Collar(adj, S, col, bd, D+1); C.target_exact(P, D=L+D); r = C.solve()
    if r is None: return False
    tr = traces(adj, S, r, bd)[(0, 1)]
    comp = {i: b for b in tr for i in b}
    assert all(comp[b[0]] == comp[b[1]] for b in blocks) and len({comp[b[0]] for b in blocks}) == len(blocks)
    return True
for L in range(10, 19, 2):
    n, e, t = band_graph(L, D+1); adj = [set() for _ in range(n)]
    for u, v in e: adj[u].add(v); adj[v].add(u)
    bd = [D*L + i for i in range(L)]; S = set(range(n))
    for cap in (3, None):
        res = []; t0 = time.time()
        words = []
        while len(words) < NW:
            r = random_level_row(L, rng)
            if cap and maxrun(r) > cap: continue
            if not cap and maxrun(r) <= 3: continue      # uncapped sample = words that violate the cap
            words.append(r)
        for r in words:
            col = {bd[i]: r[i] for i in range(L)}
            # dummy full colouring for Collar (only boundary + fixed matter; all interior free): give interior colour 0
            colf = {v: 0 for v in S}; colf.update(col)
            pos = [i for i in range(L) if r[i] in (0, 1)]
            best = 1
            for kk, size in ((3, 6), (2, 4)):
                ok = False
                for sub in list(itertools.combinations(pos, size))[:40]:
                    blocks = [(sub[j], sub[size-1-j]) for j in range(size//2)]
                    if feasible(adj, S, colf, bd, L, blocks): ok = True; break
                if ok: best = kk; break
            res.append(best)
        rec = dict(L=L, cap=cap, D=D, nwords=NW, depth3=res.count(3), depth2=res.count(2), depth1=res.count(1), sec=round(time.time()-t0))
        print(rec, flush=True); out.append(rec); json.dump(out, open('t4_adv.json', 'w'), indent=1)
