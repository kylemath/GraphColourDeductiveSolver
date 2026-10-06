"""Targeted witnesses for the ring colourings of the states lost under the 'full' adversary.

[computed, exploratory] Math worker, 2026-10-06.  For each canonical ring colouring kappa that
occurs in a lost state, sample random outer discs and enumerate only the colourings of the
disc that extend kappa; record the realised triples.  Then rerun vdred_joint with the
witnessed adversary (W = these witnesses).  W is a subset of the realisable triples, so a
non-reducible verdict here is a non-reducible verdict for the exact joint game.
"""
import random, sys, time
from collections import defaultdict
import graphs, vdred, vdred_joint, outside_sampler as osm


def extensions(faces, m, kap):
    adj = osm.adj_of(faces)
    inner = sorted(x for x in adj if x >= m)
    col = {i: kap[i] for i in range(m)}
    for i in range(m):
        for j in adj[i]:
            if j < m and kap[i] == kap[j]:
                return
    out = []
    def rec(k):
        if k == len(inner):
            out.append(dict(col)); return
        x = inner[k]
        used = {col[y] for y in adj[x] if y in col}
        for c in range(4):
            if c not in used:
                col[x] = c; rec(k + 1)
        col.pop(x, None)
    rec(0)
    for cl in out:
        yield cl


if __name__ == '__main__':
    ndisc = int(sys.argv[1]) if len(sys.argv) > 1 else 150
    F, v = graphs.pentakis(), 0
    cfg = graphs.ball_config(F, v, 2)
    m = len(cfg['ring'])
    t0 = time.process_time()
    full = vdred_joint.solve_joint(cfg, verbose=False)
    C = full['_C']
    lost = [c for c, x in full['_U'].items() if x >= vdred.INF]
    kaps = sorted({vdred.canon(tuple(c[i] for i in C.ring))[0] for c in lost})
    print(f"full adversary: {len(lost)} lost states, {len(kaps)} distinct ring colourings", flush=True)
    rng = random.Random(4242)
    W = defaultdict(set)
    for kap in kaps:
        for k in range(ndisc):
            faces = osm.random_disc(m, rng.randint(1, 12), rng, steps=200)
            for cl in extensions(faces, m, kap):
                Ms = osm.matchings_of(faces, m, cl)
                W[kap].add(tuple(Ms))   # kap is already canonical, so no relabelling
    tw = time.process_time() - t0
    tot = sum(osm.full_count(k) for k in kaps)
    print(f"targeted witnesses: {sum(len(W[k]) for k in kaps)} of {tot} possible triples on these "
          f"ring colourings ({ndisc} discs each), {tw:.1f}s", flush=True)
    r = vdred_joint.solve_joint(cfg, adversary='witnessed', allowed=W, verbose=True)
    print('  ', {k: x for k, x in r.items() if not k.startswith('_')}, flush=True)
