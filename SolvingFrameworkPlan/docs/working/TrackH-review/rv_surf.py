"""Fresh random simplicial triangulations of closed surfaces (sphere, torus, RP^2, Klein bottle),
grown by stellar face subdivisions and random edge flips.  Written for this review only."""
import random
from collections import defaultdict


def base(surface):
    if surface == 'sphere':  # octahedron
        F = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (5, 2, 1), (5, 3, 2), (5, 4, 3), (5, 1, 4)]
        return F, 2
    if surface == 'torus':  # 7-vertex Moebius torus
        F = []
        for i in range(7):
            F.append((i, (i + 1) % 7, (i + 3) % 7))
            F.append((i, (i + 2) % 7, (i + 3) % 7))
        return F, 0
    if surface == 'rp2':  # 6-vertex RP^2 (hemi-icosahedron)
        F = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 5), (0, 5, 1),
             (1, 2, 4), (2, 3, 5), (3, 4, 1), (4, 5, 2), (5, 1, 3)]
        return F, 1
    if surface == 'klein':  # 3x3 grid with a flipped identification (9 vertices): build as 4x3 to be simplicial
        # vertices (i,j), i in Z_4 rows, j in Z_3 cols?  Use 3x4 grid: Klein needs care; use torus-like
        # grid of size a x b with twisted gluing in one direction.
        a, b = 4, 4
        def v(i, j):
            # i mod a; crossing i boundary flips j
            q, i2 = divmod(i, a)
            j2 = j % b
            if q % 2:
                j2 = (-j) % b
            return i2 * b + j2
        F = []
        for i in range(a):
            for j in range(b):
                p, q_, r, s = v(i, j), v(i, j + 1), v(i + 1, j), v(i + 1, j + 1)
                F.append((p, q_, s))
                F.append((p, s, r))
        return F, 0
    raise ValueError(surface)


def check_complex(F):
    """Simplicial closed surface: distinct vertices per face, distinct faces, every edge in exactly
    2 faces, every vertex link a single cycle."""
    ef = defaultdict(int)
    if len({frozenset(f) for f in F}) != len(F):
        return False
    for f in F:
        if len(set(f)) != 3:
            return False
        a, b, c = f
        for e in ((a, b), (b, c), (a, c)):
            ef[frozenset(e)] += 1
    if any(k != 2 for k in ef.values()):
        return False
    # vertex links connected
    vf = defaultdict(list)
    for f in F:
        for u in f:
            vf[u].append(f)
    for u, fs in vf.items():
        ladj = defaultdict(list)
        for f in fs:
            o = [w for w in f if w != u]
            ladj[o[0]].append(o[1])
            ladj[o[1]].append(o[0])
        start = next(iter(ladj))
        seen = {start}
        st = [start]
        while st:
            y = st.pop()
            for z in ladj[y]:
                if z not in seen:
                    seen.add(z)
                    st.append(z)
        if len(seen) != len(ladj):
            return False
    return True


def adjacency(F):
    adj = defaultdict(set)
    for a, b, c in F:
        adj[a] |= {b, c}
        adj[b] |= {a, c}
        adj[c] |= {a, b}
    n = max(adj) + 1
    return [sorted(adj[v]) for v in range(n)]


def link_cycle(F, h):
    """Cyclic order of the link of h from the faces containing h."""
    ladj = defaultdict(list)
    for f in F:
        if h in f:
            o = [w for w in f if w != h]
            ladj[o[0]].append(o[1])
            ladj[o[1]].append(o[0])
    start = min(ladj)
    cyc = [start]
    prev = None
    cur = start
    while True:
        nxt = [z for z in ladj[cur] if z != prev]
        nxt = nxt[0] if prev is not None else ladj[cur][0]
        if nxt == start:
            break
        cyc.append(nxt)
        prev, cur = cur, nxt
    return cyc


def random_surface(surface, nverts, rng, flips_per_vertex=6, mindeg=3):
    F, chi = base(surface)
    F = [tuple(f) for f in F]
    n = max(max(f) for f in F) + 1
    while n < nverts:
        f = F.pop(rng.randrange(len(F)))
        a, b, c = f
        F += [(a, b, n), (b, c, n), (a, c, n)]
        n += 1
        for _ in range(flips_per_vertex):
            flip(F, rng, mindeg)
    for _ in range(flips_per_vertex * n):
        flip(F, rng, mindeg)
    assert check_complex(F), surface
    return F, chi


def flip(F, rng, mindeg):
    i = rng.randrange(len(F))
    f = F[i]
    a, b = rng.sample(f, 2)
    c = [w for w in f if w not in (a, b)][0]
    js = [k for k, g in enumerate(F) if k != i and a in g and b in g]
    if len(js) != 1:
        return False
    k = js[0]
    d = [w for w in F[k] if w not in (a, b)][0]
    if c == d:
        return False
    # new edge c-d must not exist
    for g in F:
        if c in g and d in g:
            return False
    deg = defaultdict(int)
    for g in F:
        for u in g:
            deg[u] += 1
    if deg[a] - 1 < mindeg or deg[b] - 1 < mindeg:
        return False
    newF = [g for kk, g in enumerate(F) if kk not in (i, k)] + [(a, c, d), (b, c, d)]
    F[:] = newF
    return True
