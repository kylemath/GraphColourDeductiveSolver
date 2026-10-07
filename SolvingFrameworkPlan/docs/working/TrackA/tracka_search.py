#!/usr/bin/env python3
"""Track A step 3 [exploratory]: adversarial edge-flip search INSIDE THE FRAME CLASS (Job AW / BQ machinery, adapted).

State: oriented face list of a triangulation on a fixed vertex set. Move: a random edge flip anywhere (no protected hole:
the objective is global), then up to 3 repair flips raising a degree-4 vertex (as jobaw.move). A move is accepted as a
candidate only if the result is in the frame class: triangulation, min degree 5, NoSep, no Occ of DiamondM/P, C2122M/P
(tracka_lib.quick_frame = the Lean Occ definition), plus max degree <= MAXD (engine practicality; not a frame condition).
Evaluator: bin/picyc --full at every degree-5 vertex (Kempe classes of T - v, class sizes and filled counts).
Objectives (minimised):
  R: (number of PureClean degree-5 vertices, max over degree-5 v of min class F/size)   hit = 0 PureClean vertices (R* fails)
  W: (min over degree-5 v of min class F/size,)                                          hit = 0 (some deg-5 vertex not PureClean)
Walk: try up to 400 moves for a frame-class candidate; accept if key <= current or with probability 0.15 (as Job AW).
usage: tracka_search.py SEEDS.json STEPS WALKS OUT.jsonl [objectives=R,W]   (Pool(4), run under nice -n 10)"""
import sys, os, json, random, itertools
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tracka_lib import rot_from_faces, faces_from_rot, quick_frame, G
from holes import picyc_holes, score
MAXD = 10

def flip(F, a, b):
    fa = [t for t in F if a in t and b in t]
    if len(fa) != 2: return None
    def third(t): return [x for x in t if x not in (a, b)][0]
    t1, t2 = fa; c, d = third(t1), third(t2)
    if any(c in t and d in t for t in F): return None   # c ~ d already: flip would create a multi-edge
    def has(t, u, v): i = t.index(u); return t[(i + 1) % 3] == v
    if not has(t1, a, b): t1, t2 = t2, t1; c, d = d, c
    return [t for t in F if t is not fa[0] and t is not fa[1]] + [(a, d, c), (b, c, d)]

def move(F, rng):
    es = sorted({(min(a, b), max(a, b)) for t in F for a, b in itertools.combinations(t, 2)})
    a, b = rng.choice(es); Gf = flip(F, a, b)
    for _ in range(4):
        if Gf is None: return None
        deg = {}
        for t in Gf:
            for x in t: deg[x] = deg.get(x, 0) + 1
        low = [v for v, d in deg.items() if d < 5]
        if not low:
            if max(deg.values()) > MAXD: return None
            rot = rot_from_faces(Gf); ok, g, why = quick_frame(rot)
            return (Gf, rot) if ok and g.is_triangulation() else None
        v = rng.choice(low); opp = [tuple(x for x in t if x != v) for t in Gf if v in t]
        rng.shuffle(opp); H = None
        for c, d in opp:
            H = flip(Gf, c, d)
            if H is not None: break
        Gf = H
    return None

def key(sc, obj):
    # M (added after the first census runs): npc = deg5 on every graph seen, so R's first component only counts degree-5
    # vertices; M = ([npc > 0], margin, worst) attacks the margin directly (hit = npc == 0, same as R).
    if obj == 'R': return (sc['npc'], round(sc['margin'], 9))
    if obj == 'M': return (int(sc['npc'] > 0), round(sc['margin'], 9), round(sc['worst'], 9))
    return (round(sc['worst'], 9),)

def walk(args):
    name, F0, obj, w, steps = args
    rng = random.Random(7919 * w + hash(obj) % 1000 + sum(map(ord, name)))
    F = [tuple(t) for t in F0]; rot = rot_from_faces(F)
    ok, g, why = quick_frame(rot)
    if not ok: return dict(seed=name, obj=obj, walk=w, error='seed not in frame class: ' + why)
    sc = score(picyc_holes(rot)); k = key(sc, obj)
    best, bestF, bestsc = k, F, sc; start = k; nev = 0; log = [(0, k)]; hits = []; trace = []
    for it in range(steps):
        cand = None
        for _ in range(400):
            m = move(F, rng)
            if m is None: continue
            H, hrot = m; nev += 1; s2 = score(picyc_holes(hrot)); cand = (H, s2); break
        if cand is None: break
        H, s2 = cand; k2 = key(s2, obj)
        if k2 <= k or rng.random() < 0.15: F, k, sc = H, k2, s2
        if k2 < best: best, bestF, bestsc = k2, H, s2; log.append((it, k2))
        if it % 25 == 0: trace.append((it, k))
        hit = (s2['npc'] == 0) if obj in ('R', 'M') else (s2['worst'] == 0)
        if hit and len(hits) < 5: hits.append(dict(it=it, score=k2, faces=[list(t) for t in H]))
    return dict(seed=name, n=len(rot), obj=obj, walk=w, steps=steps, evaluations=nev, start=start, best=best,
                best_deg5=bestsc['deg5'], best_worst=bestsc['worst'], best_margin=bestsc['margin'], best_npc=bestsc['npc'],
                best_faces=[list(t) for t in bestF], log=log, trace=trace, hits=hits)

if __name__ == '__main__':
    seeds = json.load(open(sys.argv[1])); steps = int(sys.argv[2]); walks = int(sys.argv[3]); out = sys.argv[4]
    objs = (sys.argv[5] if len(sys.argv) > 5 else 'R,W').split(',')
    jobs = [(s['name'], s['faces'], o, w, steps) for s in seeds for o in objs for w in range(walks)]
    with Pool(4) as P, open(out, 'w') as f:
        for r in P.imap_unordered(walk, jobs):
            f.write(json.dumps(r) + '\n'); f.flush()
            print(r['seed'], r['obj'], r['walk'], 'evals', r.get('evaluations'), 'start', r.get('start'), 'best', r.get('best'),
                  'hits', len(r.get('hits', [])), r.get('error', ''), flush=True)
