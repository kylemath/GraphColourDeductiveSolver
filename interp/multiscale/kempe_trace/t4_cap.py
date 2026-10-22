# Valour's claim: a run cap (max bicoloured run <= 3 on the seam row) does not bound trace complexity.
# For each L: random level seam rows with maxrun<=3 (and, for comparison, uncapped level rows), random proper
# annulus of depth D below (SAT, random assumptions); record blocks / cyclic nesting depth / max span of the 6 traces.
import json, sys, random, time, statistics as st
sys.path.insert(0, '/mnt/project-files/multiscale/kempe_trace'); sys.path.insert(0, '/mnt/project-files/multiscale/opus_attack/bandfill')
from kt import *; from t2_tubes import random_level_row, sat_colour
from tube import band_graph, maxrun
D = int(sys.argv[2]) if len(sys.argv) > 2 else 8; N = int(sys.argv[1]) if len(sys.argv) > 1 else 60
rng = random.Random(5); out = []
for L in range(8, 31, 2):
    n, e, t = band_graph(L, D+1); adj = [set() for _ in range(n)]
    for u, v in e: adj[u].add(v); adj[v].add(u)
    bd = [D*L + i for i in range(L)]; S = set(range(n))
    for cap in (3, None):
        rows = []; dep = []; spans = []; blocks = []; sing = []; tries = 0
        while len(rows) < N and tries < 50*N:
            tries += 1; r = random_level_row(L, rng)
            if cap and maxrun(r) > cap: continue
            col = sat_colour(adj, S, {bd[i]: r[i] for i in range(L)}, rng, nrand=10)
            if col is None: continue
            sm = summary(traces(adj, S, col, bd), L)
            rows.append(r); dep.append(sm['depth']); spans.append(sm['maxspan']); blocks.append(sm['nblocks']); sing.append(sm['nsingle'])
            assert sm['noncrossing']
        rec = dict(L=L, cap=cap, D=D, n=len(rows), depth_max=max(dep), depth_mean=round(st.mean(dep), 2), span_max=max(spans), span_mean=round(st.mean(spans), 2),
                   blocks_mean=round(st.mean(blocks), 2), blocks_min=min(blocks), single_mean=round(st.mean(sing), 2))
        print(rec, flush=True); out.append(rec)
        json.dump(out, open('t4_cap.json', 'w'), indent=1)
