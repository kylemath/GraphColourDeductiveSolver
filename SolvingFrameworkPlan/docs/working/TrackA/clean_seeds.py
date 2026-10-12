#!/usr/bin/env python3
"""Track A: turn non-frame constructed graphs (Job AS/AW/BV/BQ, n = 37) into frame-class seeds by flips (with degree repair)
that keep min degree 5 + NoSep + max degree <= 10 and do not increase the total Occ count (4 Lean configurations);
strict decreases preferred, sideways moves allowed. Writes out/seeds-constructed.json [{name, faces, from}]."""
import json, random, sys, itertools
from multiprocessing import Pool
from tracka_lib import rot_from_faces, G
from tracka_search import flip
P = '/Users/kylemathewson/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/local-runs/27-studio-positive-config/'
def tot(F):
    g = G(rot_from_faces(F))
    if min(g.deg) < 5 or max(g.deg) > 10 or not g.nosep(): return None
    return sum(g.occ_counts().values())
def mv(F, rng):
    es = sorted({(min(a, b), max(a, b)) for t in F for a, b in itertools.combinations(t, 2)})
    a, b = rng.choice(es); H = flip(F, a, b)
    for _ in range(4):
        if H is None: return None
        deg = {}
        for t in H:
            for x in t: deg[x] = deg.get(x, 0) + 1
        low = [v for v, d in deg.items() if d < 5]
        if not low: return H
        v = rng.choice(low); opp = [tuple(x for x in t if x != v) for t in H if v in t]; rng.shuffle(opp); H2 = None
        for c, d in opp:
            H2 = flip(H, c, d)
            if H2 is not None: break
        H = H2
    return None
def run(a):
    name, F, seed = a; rng = random.Random(seed); F = [tuple(t) for t in F]; c = tot(F)
    for it in range(3000):
        if c == 0: return dict(name='%s-clean%d' % (name, seed), faces=[list(t) for t in F], **{'from': name, 'iters': it})
        H = mv(F, rng)
        if H is None: continue
        c2 = tot(H)
        if c2 is not None and (c2 < c or (c2 == c and rng.random() < 0.3)): F, c = H, c2
    return dict(name=name, fail=c)
if __name__ == '__main__':
    src = ['jobas/best-A7f1.json', 'jobas/best-A7f2.json', 'jobas/best-A7f3.json', 'jobas/best-A7f4.json', 'jobas/best-walk-best-A7f1-1.json', 'jobas/best-walk-best-A7f1-3.json',
           'jobbq/best/' , 'jobbv/graphs/']
    import glob, os
    files = []
    for s in src: files += sorted(glob.glob(P + s + '*.json')) if s.endswith('/') else [P + s]
    jobs = [(os.path.basename(f)[:-5], json.load(open(f))['faces'], sd) for f in files for sd in (1, 2)]
    out = []
    with Pool(4) as Pp:
        for r in Pp.imap_unordered(run, jobs):
            print(r['name'], 'ok' if 'faces' in r else 'fail %s' % r['fail'], r.get('iters'), flush=True)
            if 'faces' in r: out.append(r)
    json.dump(out, open('out/seeds-constructed.json', 'w'))
