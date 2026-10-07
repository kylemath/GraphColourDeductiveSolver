#!/usr/bin/env python3
"""[exploratory] Torus quarter-floor scan. For each generated torus triangulation and each degree-5 vertex v:
all 4-colourings of T-v up to renaming, Kempe classes, filled count (link of v uses <=3 colours)."""
import sys, json, random, time
sys.path.insert(0, '../common'); sys.path.insert(0, '.')
from torus import *
from kempe_py import Space
from fractions import Fraction

MAXSTATES = 400000
def analyse(n, F, v):
    adj = adjacency(F, n); link = link_cycle(F, v); assert len(link) == 5
    t = time.time()
    sp = Space(adj, v, link)
    if len(sp.states) > MAXSTATES: return {'v': v, 'skipped': len(sp.states)}
    sp.build_graph(); cl, ncl = sp.classes()
    size = [0] * ncl; fil = [0] * ncl
    for k in range(len(sp.states)):
        size[cl[k]] += 1; fil[cl[k]] += sp.filled(k)
    return {'v': v, 'states': len(sp.states), 'classes': [[size[c], fil[c]] for c in range(ncl)],
            'secs': round(time.time() - t, 2)}

def main(out, budget, seed, sizes, reps):
    rng = random.Random(seed); t0 = time.time(); seen = set(); fam = []
    plan = []
    for (r, s) in sizes:
        plan.append((r, s, 0, 0.0)); plan.append((r, s, 1, 0.0))        # 0 flips (6-regular, no deg-5), single flip
        for steps, bias in [(3,0.0),(10,0.0),(30,0.0),(30,0.7),(80,0.9),(150,0.9)]:
            for rep in range(reps): plan.append((r, s, steps, bias))
    with open(out, 'w') as fo:
        for (r, s, steps, bias) in plan:
            if time.time() - t0 > budget: break
            n, F = lattice(r, s)
            F = random_walk(n, F, steps, rng, bias) if steps else F
            assert validate(n, F) is None
            inv = (n, invariant(n, F))
            if inv in seen: continue
            seen.add(inv)
            adj = adjacency(F, n); d5 = [v for v in range(n) if len(adj[v]) == 5]
            res = [analyse(n, F, v) for v in d5]
            rec = {'family': f'T({r},{s})', 'steps': steps, 'bias': bias, 'n': n,
                   'degseq': sorted(len(a) for a in adj.values()), 'faces': sorted(sorted(f) for f in F), 'holes': res}
            fo.write(json.dumps(rec) + '\n'); fo.flush()
            print(rec['family'], steps, bias, 'deg5:', len(d5), 'states:', [x.get('states', x.get('skipped')) for x in res][:8], round(time.time() - t0), flush=True)

if __name__ == '__main__':
    sizes = [tuple(map(int, x.split('x'))) for x in sys.argv[5].split(',')]
    main(sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), sizes, int(sys.argv[4]))
