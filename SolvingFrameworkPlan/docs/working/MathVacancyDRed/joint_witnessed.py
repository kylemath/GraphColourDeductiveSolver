"""Run vdred_joint with the WITNESSED adversary (triples realised by explicit outsides).

[computed, exploratory] Math worker, 2026-10-06.  The witnessed set W is a subset of the truly
realisable triples, so the adversary here is weaker than in the exact joint game:
a NON-reducible verdict here implies non-reducible in the exact joint game.
Witness outsides: the configuration's own outside in its host triangulation, random
outside-flip completions of it (verify.outside_flips), and random discs (outside_sampler).
"""
import random, sys, time
from collections import defaultdict
import graphs, vdred, vdred_joint, outside_sampler as osm, verify


def own_outside(F, cfg):
    v, r = cfg['v'], cfg['r']
    adj = graphs.adjacency(F)
    dist = {v: 0}; fr = [v]
    while fr:
        nf = []
        for x in fr:
            for y in adj[x]:
                if y not in dist:
                    dist[y] = dist[x] + 1; nf.append(y)
        fr = nf
    inside = {frozenset(f) for f in F if all(dist[x] <= r for x in f) and min(dist[x] for x in f) < r}
    ring = cfg['ring']
    lab = {x: i for i, x in enumerate(ring)}
    nxt = len(ring)
    out = []
    for f in F:
        if frozenset(f) in inside:
            continue
        g = []
        for x in f:
            if x not in lab:
                lab[x] = nxt; nxt += 1
            g.append(lab[x])
        out.append(frozenset(g))
    return out


if __name__ == '__main__':
    name = sys.argv[1]; nrand = int(sys.argv[2]); nflip = int(sys.argv[3])
    F, v = {'T4': (graphs.T4(), 4), 'A3': (graphs.A(3), 0), 'pentakis': (graphs.pentakis(), 0)}[name]
    cfg = graphs.ball_config(F, v, 2)
    m = len(cfg['ring'])
    t0 = time.process_time()
    W = defaultdict(set)
    rng = random.Random(77)
    if nflip >= 0:   # own outside; costly for ring 10 (26-vertex disc): pass -1 to skip
        osm.record(own_outside(F, cfg), m, W)
    for k in range(nflip):
        F2 = verify.outside_flips(F, cfg, rng.randint(1, 10), rng)
        osm.record(own_outside(F2, cfg), m, W)
    for k in range(nrand):
        osm.record(osm.random_disc(m, rng.randint(1, 12), rng, steps=200), m, W)
    tw = time.process_time() - t0
    print(f"{name}: witnessed triples {sum(len(s) for s in W.values())} over {len(W)} ring colourings "
          f"(own outside + {nflip} flips + {nrand} random discs), {tw:.1f}s", flush=True)
    r = vdred_joint.solve_joint(cfg, adversary='witnessed', allowed=W)
    print('  ', {k: x for k, x in r.items() if not k.startswith('_')}, flush=True)
