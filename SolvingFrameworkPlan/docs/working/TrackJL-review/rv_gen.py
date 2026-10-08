#!/usr/bin/env python3
"""TrackJL-review: fresh random triangulations of S^2 / RP^2 by vertex insertion + random
edge flips (written from scratch).  Output lines: 'name n adj0;adj1;...' with every
adjacency list in cyclic link order.  Every output surface is validated: simple graph,
every edge in exactly two faces, every vertex link a single cycle, V - E + F = chi.

usage: rv_gen.py surface(sphere|rp2|torus) count nmin nmax mindeg seed
"""
import random, sys
from collections import defaultdict


def edges_of(faces):
    ef = defaultdict(list)
    for f in faces:
        a, b, c = f
        for e in ((a, b), (b, c), (a, c)):
            ef[frozenset(e)].append(f)
    return ef


def degrees(faces, n):
    d = [0] * n
    for e in edges_of(faces):
        for v in e:
            d[v] += 1
    return d


def link_cycle(v, faces_v):
    # faces_v: list of triangles containing v; returns cyclic order of link vertices
    nb = defaultdict(list)
    for f in faces_v:
        a, b = [x for x in f if x != v]
        nb[a].append(b); nb[b].append(a)
    if any(len(l) != 2 for l in nb.values()):
        return None
    start = next(iter(nb)); cyc = [start]; prev = None; cur = start
    while True:
        nxt = nb[cur][0] if nb[cur][0] != prev else nb[cur][1]
        if nxt == start:
            break
        cyc.append(nxt); prev, cur = cur, nxt
        if len(cyc) > len(nb):
            return None
    return cyc if len(cyc) == len(nb) else None


def validate(faces, n, chi):
    ef = edges_of(faces)
    if any(len(fs) != 2 for fs in ef.values()):
        return None
    if len(set(frozenset(f) for f in faces)) != len(faces):
        return None
    if n - len(ef) + len(faces) != chi:
        return None
    byv = defaultdict(list)
    for f in faces:
        for v in f:
            byv[v].append(f)
    adj = []
    for v in range(n):
        cyc = link_cycle(v, byv[v])
        if cyc is None or len(cyc) < 3:
            return None
        adj.append(cyc)
    return adj


def flip(faces_set, ef, e, mindeg, deg):
    a, b = tuple(e)
    f1, f2 = ef[e]
    c = [x for x in f1 if x not in e][0]
    d = [x for x in f2 if x not in e][0]
    if c == d or frozenset((c, d)) in ef:
        return False
    if deg[a] - 1 < mindeg or deg[b] - 1 < mindeg:
        return False
    return (a, b, c, d, f1, f2)


def apply_flip(faces, ef, deg, data):
    a, b, c, d, f1, f2 = data
    faces.discard(f1); faces.discard(f2)
    g1 = tuple(sorted((a, c, d))); g2 = tuple(sorted((b, c, d)))
    faces.add(g1); faces.add(g2)
    for f in (f1, f2):
        x, y, z = f
        for ee in ((x, y), (y, z), (x, z)):
            fe = frozenset(ee)
            if fe in ef:
                ef[fe] = [g for g in ef[fe] if g != f]
    del ef[frozenset((a, b))]
    for g in (g1, g2):
        x, y, z = g
        for ee in ((x, y), (y, z), (x, z)):
            ef.setdefault(frozenset(ee), []).append(g)
    deg[a] -= 1; deg[b] -= 1; deg[c] += 1; deg[d] += 1


def make(surface, n, mindeg, rng):
    if surface == 'sphere':
        faces = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]; k = 4; chi = 2
    elif surface == 'torus':
        faces = [((i) % 7, (i + 1) % 7, (i + 3) % 7) for i in range(7)] + [((i) % 7, (i + 2) % 7, (i + 3) % 7) for i in range(7)]
        k = 7; chi = 0
    else:
        F = [(1, 2, 3), (1, 3, 4), (1, 4, 5), (1, 5, 6), (1, 6, 2), (2, 3, 5), (3, 4, 6), (4, 5, 2), (5, 6, 3), (6, 2, 4)]
        faces = [tuple(sorted(x - 1 for x in f)) for f in F]; k = 6; chi = 1
    faces = set(tuple(sorted(f)) for f in faces)
    while k < n:
        f = rng.choice(sorted(faces)); faces.discard(f)
        a, b, c = f
        for g in ((a, b, k), (b, c, k), (a, c, k)):
            faces.add(tuple(sorted(g)))
        k += 1
    ef = edges_of(faces); ef = {e: list(v) for e, v in ef.items()}
    deg = degrees(faces, n)
    # mixing with min degree 3
    for _ in range(30 * n):
        e = rng.choice(list(ef.keys()))
        dta = flip(faces, ef, e, 3, deg)
        if dta:
            apply_flip(faces, ef, deg, dta)
    if mindeg > 3:
        # repair: reduce deficit
        for it in range(400 * n):
            defi = sum(max(0, mindeg - x) for x in deg)
            if defi == 0:
                break
            e = rng.choice(list(ef.keys()))
            dta = flip(faces, ef, e, 3, deg)
            if not dta:
                continue
            a, b, c, d, _, _ = dta
            nd = list(deg); nd[a] -= 1; nd[b] -= 1; nd[c] += 1; nd[d] += 1
            if sum(max(0, mindeg - x) for x in nd) <= defi:
                apply_flip(faces, ef, deg, dta)
        if any(x < mindeg for x in deg):
            return None
        for _ in range(30 * n):
            e = rng.choice(list(ef.keys()))
            dta = flip(faces, ef, e, mindeg, deg)
            if dta:
                apply_flip(faces, ef, deg, dta)
    adj = validate(list(faces), n, chi)
    return adj


def main():
    surface, count, nmin, nmax, mindeg, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
    rng = random.Random(seed)
    made = 0; tries = 0
    while made < count and tries < 20 * count:
        tries += 1
        n = rng.randint(nmin, nmax)
        adj = make(surface, n, mindeg, rng)
        if adj is None:
            continue
        if not any(len(a) == 5 for a in adj):
            continue
        name = f"{surface}{mindeg}_s{seed}_{made}"
        print(name, n, ";".join(",".join(map(str, a)) for a in adj))
        made += 1


if __name__ == '__main__':
    main()
