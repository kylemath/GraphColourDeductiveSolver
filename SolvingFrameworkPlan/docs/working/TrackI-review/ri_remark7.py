"""Track I review: data check of Remark 7 (no written proof in RigidIsolation.md).
Claim: a Kempe swap of a component containing no link vertex preserves N + L1 + L2 (mod 2).
usage: python3 ri_remark7.py SEED COUNT OUT.json   (random min-degree-5 spheres, n = 14..24, full enumeration)
"""
import sys, json, random
from collections import Counter
import ri_core as rc

seed, count, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
rng = random.Random(seed); st = Counter()
for gi in range(count):
    n = rng.randint(14, 24)
    s = rc.random_surface(rc.tetra(), n, rng, 200 * n, target_min5=True)
    if rc.min_degree(s) < 5:
        continue
    st['graphs'] += 1
    for h in [v for v in s.V if len(s.adj[v]) == 5][:3]:
        V, ix, nbr = rc.graph_minus(s, h)
        L = [ix[x] for x in s.link(h)]
        Lset = set(L)
        for col in rc.enumerate_colourings(nbr, limit=20000):
            a = rc.hole_state(nbr, col, L)
            if a is None:
                continue
            N0 = rc.N_total(nbr, col)
            done = set()
            for p, q in rc.PAIRS:
                for v in range(len(col)):
                    if col[v] not in (p, q) or (p, q, v) in done:
                        continue
                    K = rc.component(nbr, col, v, p, q)
                    for w in K:
                        done.add((p, q, w))
                    if K & Lset:
                        continue
                    c2 = list(col)
                    for w in K:
                        c2[w] = q if col[w] == p else p
                    b = rc.hole_state(nbr, c2, L)
                    N1 = rc.N_total(nbr, c2)
                    st['moves'] += 1
                    st['N_parity_change'] += (N1 - N0) % 2
                    st['remark7_FAIL'] += (N1 + b['L1'] + b['L2'] - N0 - a['L1'] - a['L2']) % 2
                    if a['DL'] and b['DL']:
                        st['DL->DL_moves'] += 1
                        st['DL->DL_N_parity_change'] += (N1 - N0) % 2
    json.dump(dict(st), open(out, 'w'), indent=1)
print(dict(st))
