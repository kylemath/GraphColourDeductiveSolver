#!/usr/bin/env python3
"""Track A task 3 [exploratory]: flip + grow search in the FRAME CLASS maximising positive pi-winding.
Moves: with prob PGROW (if n < NMAX) insert a vertex in a random face + degree repair (grow_seeds.grow), always accepted
(drift in n); otherwise a frame-preserving flip (tracka_search.move), hill-climb accepted if key >= current or with prob 0.15.
Every graph visited passes quick_frame + is_triangulation (Lean-faithful Occ filter), max degree <= 10.
Evaluator: picyc --full, plantri orientation (best graphs re-checked in both orientations by posw_scan.py).
Key (maximised): ([max class sum w > 0], total positive weight sum_{w>0} w over all holes, -min slack -sum w / N over classes with N > 8).
Hit: a class with sum w > 0 (quarter floor fails).  Walks are wall-clock capped.
usage: posw_search.py SEEDS.json OUT.jsonl WALL_SECONDS NMAX"""
import sys, os, json, random, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tracka_lib import rot_from_faces, quick_frame
from tracka_search import move
from grow_seeds import grow, frame
from posw_scan import picyc_raw, hole_summary
PGROW = 0.12
def evaluate(F):
    hs = [hole_summary(r) for r in picyc_raw(rot_from_faces(F))]
    # third component uses classes with N > 8 only: the w = 0 block classes (N = 4, 8; slack 0) would make it flat (task 2)
    big = [-c[2] / c[0] for h in hs for c in h['cls'] if c[0] > 8]
    # first component = [some class has sum w > 0] rather than max class sum w: the raw max is pinned at 0 by the w = 0 block
    # classes and otherwise rewards splitting off tiny classes; positive mass and normalised slack carry the gradient.
    key = (int(max(h['max_cls_sumw'] for h in hs) > 0), sum(h['posw'] for h in hs), -round(min(big), 9) if big else 0)
    return key, dict(npos=sum(h['npos'] for h in hs), maxw=max(h['maxw'] for h in hs),
                     poslinks=[h['linkdeg'] for h in hs if h['npos']])
def walk(a):
    name, F0, w, wall, nmax = a; rng = random.Random(1009 * w + sum(map(ord, name))); t0 = time.time()
    F = [tuple(t) for t in F0]; k, info = evaluate(F); n = 1 + max(x for t in F for x in t)
    best = {}; nev = 1; hits = []; trace = []
    def note(n, k, info, F):
        if n not in best or k > best[n]['key']: best[n] = dict(key=k, info=info, faces=[list(t) for t in F])
    note(n, k, info, F)
    it = 0
    while time.time() - t0 < wall:
        it += 1
        if n < nmax and rng.random() < PGROW:
            H = None
            for _ in range(200):
                H = grow(F, rng)
                if H is not None and frame(H): break
                H = None
            if H is None: continue
            k2, i2 = evaluate(H); nev += 1; F, k, info, n = H, k2, i2, n + 1
        else:
            m = None
            for _ in range(400):
                m = move(F, rng)
                if m is not None: break
            if m is None: continue
            H = m[0]; k2, i2 = evaluate(H); nev += 1
            if k2 >= k or rng.random() < 0.15: F, k, info = H, k2, i2
        note(n, k2, i2, H)
        if k2[0] > 0 and len(hits) < 5: hits.append(dict(it=it, n=n, key=k2, faces=[list(t) for t in H]))
        if it % 10 == 0: trace.append((it, n, k, round(time.time() - t0)))
    return dict(seed=name, walk=w, evaluations=nev, iters=it, final_n=n, best_by_n={str(a): b for a, b in sorted(best.items())}, hits=hits, trace=trace)
if __name__ == '__main__':
    seeds = json.load(open(sys.argv[1])); out = sys.argv[2]; wall = float(sys.argv[3]); nmax = int(sys.argv[4])
    jobs = [(s['name'], s['faces'], i, wall, nmax) for i, s in enumerate(seeds)]
    with Pool(int(os.environ.get("POSW_POOL", "4"))) as P, open(out, "w") as f:
        for r in P.imap_unordered(walk, jobs):
            f.write(json.dumps(r) + '\n'); f.flush()
            print(r['seed'], 'evals', r['evaluations'], 'final n', r['final_n'], 'hits', len(r['hits']),
                  {n: b['key'] for n, b in r['best_by_n'].items()}, flush=True)
