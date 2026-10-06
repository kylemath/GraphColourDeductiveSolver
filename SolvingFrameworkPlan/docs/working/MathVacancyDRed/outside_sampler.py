"""Empirical joint-realisability of the three Tait matchings (M_1, M_2, M_3) of a ring colouring.

[computed, exploratory] Math worker, 2026-10-06.  Lower-bound tool only: it records the
triples REALISED by explicitly generated triangulated outer discs O with boundary ring
0..m-1 (random walk of stackings, unstackings and interior flips from the wheel), over all
proper 4-colourings of O.  A triple seen here is certainly realisable; a triple not seen
may still be realisable by a larger outside.
"""
import random, sys, time
from collections import defaultdict
import vdred


def disc_wheel(m):
    w = m
    return [frozenset((i, (i + 1) % m, w)) for i in range(m)]


def adj_of(faces):
    adj = defaultdict(set)
    for f in faces:
        for a in f:
            adj[a] |= f - {a}
    return adj


def random_disc(m, nint, rng, steps=60):
    faces = disc_wheel(m)
    nxt = m + 1
    ring_edges = {frozenset((i, (i + 1) % m)) for i in range(m)}
    for _ in range(steps):
        adj = adj_of(faces)
        interior = [x for x in adj if x >= m]
        op = rng.random()
        if op < 0.25 and len(interior) < nint:
            f = rng.choice(faces)
            a, b, c = tuple(f)
            faces.remove(f)
            faces += [frozenset((a, b, nxt)), frozenset((b, c, nxt)), frozenset((a, c, nxt))]
            nxt += 1
        elif op < 0.35 and len(interior) > 1:
            d3 = [x for x in interior if len(adj[x]) == 3]
            if d3:
                x = rng.choice(d3)
                nb = adj[x]
                faces = [f for f in faces if x not in f] + [frozenset(nb)]
        else:
            f = rng.choice(faces)
            a, b = rng.sample(sorted(f), 2)
            e = frozenset((a, b))
            if e in ring_edges:
                continue
            g = [h for h in faces if e <= h and h != f]
            if len(g) != 1:
                continue
            g = g[0]
            c = next(iter(f - e)); d = next(iter(g - e))
            if d in adj[c]:
                continue
            # keep interior vertices of degree >= 3 and ring vertices of degree >= 2
            if (a >= m and len(adj[a]) <= 3) or (b >= m and len(adj[b]) <= 3):
                continue
            if (a < m and len(adj[a]) <= 2) or (b < m and len(adj[b]) <= 2):
                continue
            faces.remove(f); faces.remove(g)
            faces += [frozenset((a, c, d)), frozenset((b, c, d))]
    return faces


def colourings(faces):
    adj = adj_of(faces)
    order = sorted(adj)
    idx = {x: i for i, x in enumerate(order)}
    nbr = [[idx[y] for y in adj[x]] for x in order]
    n = len(order)
    c = [-1] * n
    out = []
    def rec(i, mx):
        if i == n:
            out.append(tuple(c)); return
        used = {c[j] for j in nbr[i] if c[j] >= 0}
        for col in range(min(mx + 2, 4)):
            if col not in used:
                c[i] = col; rec(i + 1, max(mx, col))
        c[i] = -1
    rec(0, -1)
    return order, idx, out


def matchings_of(faces, m, col):
    """col: dict vertex -> colour.  Returns (kappa, (M1, M2, M3)) in raw colours, M_th as
    partner tuple over positions of vdred-style transitional list."""
    efaces = defaultdict(list)
    for f in faces:
        for a in f:
            for b in f:
                if a < b:
                    efaces[(a, b)].append(f)
    res = []
    for th in (1, 2, 3):
        H = lambda x: col[x] in (0, th)
        T = [i for i in range(m) if H(i) != H((i + 1) % m)]
        pos = {i: k for k, i in enumerate(T)}
        M = [None] * len(T)
        for i in T:
            if M[pos[i]] is not None:
                continue
            e = tuple(sorted((i, (i + 1) % m)))
            f = efaces[e][0]
            while True:
                tr = [tuple(sorted(p)) for p in ((a, b) for a in f for b in f if a < b)
                      if H(p[0]) != H(p[1])]
                assert len(tr) == 2
                e2 = tr[0] if tr[1] == e else tr[1]
                fs = [g for g in efaces[e2] if g != f]
                if not fs:   # ring edge
                    j = e2[0] if (e2[0] + 1) % m == e2[1] else e2[1]
                    break
                e, f = e2, fs[0]
            M[pos[i]] = pos[j]; M[pos[j]] = pos[i]
        res.append(tuple(M))
    return res


def record(faces, m, store):
    order, idx, cols = colourings(faces)
    for c in cols:
        col = {x: c[idx[x]] for x in order}
        kap = tuple(col[i] for i in range(m))
        Ms = matchings_of(faces, m, col)
        cc, sig = vdred.canon(kap)
        trip = [None, None, None]
        for th in (1, 2, 3):
            trip[vdred.map_split(th, sig) - 1] = Ms[th - 1]
        store[cc].add(tuple(trip))


def full_count(kap):
    m = len(kap)
    tot = 1
    for th in (1, 2, 3):
        h = [(x == 0 or x == th) for x in kap]
        t = sum(h[i] != h[(i + 1) % m] for i in range(m))
        tot *= len(vdred.nc_matchings(t))
    return tot


def ring_colourings(m):
    out = set()
    def rec(seq, mx):
        if len(seq) == m:
            if seq[-1] != seq[0]:
                out.add(tuple(seq))
            return
        for col in range(min(mx + 2, 4)):
            if col != seq[-1]:
                rec(seq + [col], max(mx, col))
    rec([0], 0)
    return sorted(out)


if __name__ == '__main__':
    m = int(sys.argv[1]); nint = int(sys.argv[2]); ndisc = int(sys.argv[3])
    rng = random.Random(1000 * m + nint)
    store = defaultdict(set)
    t0 = time.process_time()
    for k in range(ndisc):
        faces = random_disc(m, rng.randint(1, nint), rng)
        record(faces, m, store)
    kaps = ring_colourings(m)
    seen = sum(len(store[k]) for k in kaps)
    full = sum(full_count(k) for k in kaps)
    # pair projections
    pfull = pseen = 0
    for k in kaps:
        h = []
        for th in (1, 2, 3):
            hh = [(x == 0 or x == th) for x in k]
            h.append(len(vdred.nc_matchings(sum(hh[i] != hh[(i + 1) % m] for i in range(m)))))
        for a, b in ((0, 1), (0, 2), (1, 2)):
            pfull += h[a] * h[b]
            pseen += len({(t[a], t[b]) for t in store[k]})
    print(f"m={m} nint<={nint} discs={ndisc}: ring colourings {len(kaps)}, triples seen {seen}/{full}, "
          f"pairs seen {pseen}/{pfull}, cpu {time.process_time()-t0:.1f}s", flush=True)
    for k in kaps:
        if len(store[k]) < full_count(k):
            print('  ', k, len(store[k]), '/', full_count(k))
