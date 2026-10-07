#!/usr/bin/env python3
"""Track A phase 2 seeds [exploratory]: frame-class graphs of orders beyond the census (n = 29..36), grown from marginal census
graphs. Grow move = insert a vertex into a random face, then degree-repair flips (tracka_search.move logic) and up to 30
random frame-preserving flips for mixing; every intermediate graph kept is in the frame class (quick_frame + is_triangulation).
usage: grow_seeds.py OUT.json TARGET_N SEEDNAMES...   (single process)"""
import sys, json, random, itertools
from tracka_lib import rot_from_faces, faces_from_rot, quick_frame, parse_line
from tracka_search import flip, move
def grow(F, rng):
    n = 1 + max(x for t in F for x in t); a, b, c = rng.choice(F)
    H = [t for t in F if t != (a, b, c)] + [(a, b, n), (b, c, n), (c, a, n)]
    for _ in range(3):
        deg = {}
        for t in H:
            for x in t: deg[x] = deg.get(x, 0) + 1
        low = [v for v, d in deg.items() if d < 5]
        if not low: break
        v = low[0]; opp = [tuple(x for x in t if x != v) for t in H if v in t]; rng.shuffle(opp); H2 = None
        for c1, d1 in opp:
            H2 = flip(H, c1, d1)
            if H2 is not None: break
        if H2 is None: return None
        H = H2
    return H
def frame(H):
    rot = rot_from_faces(H); ok, g, _ = quick_frame(rot); return ok and g.is_triangulation() and max(g.deg) <= 10
if __name__ == '__main__':
    out, N = sys.argv[1], int(sys.argv[2]); lines = {}
    for fn in ('out/frame-12-24.txt', 'out/frame-25-26.txt', 'out/frame-27.txt', 'out/frame28-cfree-list.txt'):
        for l in open(fn): lines[l.split()[0]] = l
    res = []
    for si, name in enumerate(sys.argv[3:]):
        for rep in range(2):
            rng = random.Random(100 * si + rep); F = [tuple(t) for t in faces_from_rot(parse_line(lines[name])[1])]; tries = 0
            while 1 + max(x for t in F for x in t) < N and tries < 300:
                tries += 1; H = None
                for _ in range(200):
                    H = grow(F, rng)
                    if H is not None and frame(H): break
                    H = None
                if H is None:   # mix and retry
                    m = move(F, rng)
                    if m: F = m[0]
                    continue
                F = H
                for _ in range(30):
                    m = move(F, rng)
                    if m: F = m[0]
            n = 1 + max(x for t in F for x in t)
            if n == N and frame(F): res.append(dict(name='%s-grow%d-r%d' % (name, N, rep), faces=[list(t) for t in faces_from_rot(rot_from_faces(F))]))
            print(name, rep, 'reached', n, flush=True)
    json.dump(res, open(out, 'w'))
