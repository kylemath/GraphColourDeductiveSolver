"""WP14 probe: hard states and target distance on LARGER minimum-degree-five triangulations.

Not an exhaustive check.  Graphs: the pentakis dodecahedron (n=32), the frequency-2 geodesic
icosahedron (n=42), and random minimum-degree-five triangulations obtained from them by random
degree-preserving-safe edge flips (min degree >= 5, simple).  Colourings of T - r are SAMPLED by
random Kempe walks (so only the Kempe classes visited are seen).  For every sampled hard state
(no target within two swaps; by Lemma 1 = locked with every single-swap successor locked) the exact
target distance is computed by bounded BFS up to depth CAP.

Usage: python3 probe_large.py [seed] [graphs] [walk_steps]
Orders 19-20 of the Plantri corpus are NOT used (holdout).
"""
import json
import random
import sys
import time

from wp14_common import HERE, LT, lock, ncol  # noqa: F401
sys.path.insert(0, str(LT))
from mass_core import validate_triangulation  # noqa: E402

CAP = 6


# ------------------------------------------------------------------ graphs
def faces_of(rot):
    seen, out = set(), []
    for u, ns in enumerate(rot):
        for k, v in enumerate(ns):
            w = ns[(k + 1) % len(ns)]
            f = frozenset((u, v, w))
            if f not in seen:
                seen.add(f)
                out.append((u, v, w))
    return out


def from_faces(n, faces):
    """Rotation system from an oriented face list (each face (a,b,c) counter-clockwise)."""
    nxt = [dict() for _ in range(n)]
    for a, b, c in faces:
        for x, y, z in ((a, b, c), (b, c, a), (c, a, b)):
            nxt[x][y] = z  # around x: after y comes z
    rot = []
    for x in range(n):
        start = next(iter(nxt[x]))
        cyc, y = [start], nxt[x][start]
        while y != start:
            cyc.append(y)
            y = nxt[x][y]
        assert len(cyc) == len(nxt[x])
        rot.append(cyc)
    return rot


def icosahedron_faces():
    import math
    phi = (1 + 5 ** 0.5) / 2
    P = [(-1, phi, 0), (1, phi, 0), (-1, -phi, 0), (1, -phi, 0), (0, -1, phi), (0, 1, phi),
         (0, -1, -phi), (0, 1, -phi), (phi, 0, -1), (phi, 0, 1), (-phi, 0, -1), (-phi, 0, 1)]
    F = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6),
         (7, 1, 8), (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9), (4, 9, 5), (2, 4, 11), (6, 2, 10),
         (8, 6, 7), (9, 8, 1)]
    return P, F


def geodesic2():
    P, F = icosahedron_faces()
    mid, n = {}, 12

    def m(a, b):
        nonlocal n
        k = frozenset((a, b))
        if k not in mid:
            mid[k] = n
            n += 1
        return mid[k]
    out = []
    for a, b, c in F:
        ab, bc, ca = m(a, b), m(b, c), m(c, a)
        out += [(a, ab, ca), (ab, b, bc), (ca, bc, c), (ab, bc, ca)]
    return from_faces(n, out)


def pentakis():
    # kis of the dodecahedron = dual-of-icosahedron faces get centre vertices; build as
    # icosahedron's dual: vertices = 12 ico vertices (face centres, degree 5) + 20 ico faces (degree 6)
    P, F = icosahedron_faces()
    out = []
    # around each icosahedron vertex v, its 5 faces in cyclic order; triangulate: v + consecutive face pair
    # plus faces f, g sharing an ico edge (a,b): triangles (a, f, g)?  Simpler: pentakis = ico vertices U face
    # vertices, edges v-f (v in f) and f-g (f,g adjacent faces).  Faces: (v, f, g) for f,g adjacent faces at v.
    rot_ico = from_faces(12, F)
    fid = {frozenset(f): 12 + k for k, f in enumerate(F)}
    for v in range(12):
        ns = rot_ico[v]
        for k in range(5):
            a, b, c = ns[k], ns[(k + 1) % 5], ns[(k + 2) % 5]
            f1 = fid[frozenset((v, a, b))]
            f2 = fid[frozenset((v, b, c))]
            out.append((v, f1, f2))
    return from_faces(32, out)


def flip_random(rot, rng, tries=1):
    n = len(rot)
    done = 0
    for _ in range(tries * 20):
        u = rng.randrange(n)
        k = rng.randrange(len(rot[u]))
        v = rot[u][k]
        a = rot[u][(k + 1) % len(rot[u])]
        b = rot[u][(k - 1) % len(rot[u])]
        if len(rot[u]) <= 5 or len(rot[v]) <= 5 or b in rot[a] or a == b:
            continue
        # rot[a]: insert b between u and v ; rot[b]: insert a between v and u
        ra = rot[a]
        iu, iv = ra.index(u), ra.index(v)
        if (iu + 1) % len(ra) == iv:
            ra.insert(iv, b)
        else:
            ra.insert(iu, b)
        rb = rot[b]
        iu, iv = rb.index(u), rb.index(v)
        if (iu + 1) % len(rb) == iv:
            rb.insert(iv, a)
        else:
            rb.insert(iu, a)
        rot[u].remove(v)
        rot[v].remove(u)
        done += 1
        if done >= tries:
            break
    validate_triangulation(rot)
    return rot


# ------------------------------------------------------------------ colourings and Kempe moves
def colour(adj, verts, rng):
    order = sorted(verts, key=lambda v: -len(adj[v]))
    col = {}

    def go(k):
        if k == len(order):
            return True
        v = order[k]
        cs = [0, 1, 2, 3]
        rng.shuffle(cs)
        used = {col[w] for w in adj[v] if w in col}
        for c in cs:
            if c not in used:
                col[v] = c
                if go(k + 1):
                    return True
                del col[v]
        return False
    assert go(0)
    return col


def comp(adj, col, v, a, b):
    seen, st = {v}, [v]
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen and col[y] in (a, b):
                seen.add(y)
                st.append(y)
    return seen


def components(adj, col):
    out = []
    for a, b in ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)):
        pend = {v for v in col if col[v] in (a, b)}
        while pend:
            s = pend.pop()
            K = comp(adj, col, s, a, b)
            pend -= K
            out.append(((a, b), K))
    return out


def swap(col, pr, K):
    a, b = pr
    c = dict(col)
    for v in K:
        c[v] = b if col[v] == a else a
    return c


def p_of(col, B):
    return 1 if ncol(col, B) == 4 else 0


def nonhard(adj, col, B):
    """True iff a target is reachable within two swaps (Lemma 1 + Theorem 2)."""
    if p_of(col, B) == 0 or not lock(adj, col, B):
        return True
    for pr, K in components(adj, col):
        c1 = swap(col, pr, K)
        if p_of(c1, B) == 0 or not lock(adj, c1, B):
            return True
    return False


def key(col, V):
    seen = {}
    return tuple(seen.setdefault(col[v], len(seen)) for v in V)


def distance(adj, col, B, V, cap=CAP):
    """Exact target distance up to cap (None if > cap).  d<=2 iff nonhard."""
    if nonhard(adj, col, B):
        return None  # not asked
    frontier = {key(col, V): col}
    seen = set(frontier)
    for depth in range(1, cap - 1):
        nxt = {}
        for c in frontier.values():
            for pr, K in components(adj, c):
                c1 = swap(c, pr, K)
                k1 = key(c1, V)
                if k1 in seen:
                    continue
                seen.add(k1)
                if nonhard(adj, c1, B):
                    return depth + 2
                nxt[k1] = c1
        frontier = nxt
        if not frontier:
            return float("inf")
    return None


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    ngraphs = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    steps = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
    rng = random.Random(seed)
    bases = [("pentakis32", pentakis()), ("geodesic42", geodesic2())]
    results = []
    t0 = time.time()
    for gi in range(ngraphs):
        bname, base = bases[gi % 2]
        rot = [list(x) for x in base]
        nflips = 0 if gi < 2 else rng.randrange(5, 200)
        if nflips:
            rot = flip_random(rot, rng, nflips)
        validate_triangulation(rot)
        n = len(rot)
        d5 = [v for v in range(n) if len(rot[v]) == 5]
        for r in rng.sample(d5, min(3, len(d5))):
            B = list(rot[r])
            V = [v for v in range(n) if v != r]
            adj = {v: [w for w in rot[v] if w != r] for v in V}
            col = colour(adj, V, rng)
            seen, hardk = set(), {}
            locked = p1 = 0
            for _ in range(steps):
                v = rng.choice(V)
                b = rng.choice([x for x in range(4) if x != col[v]])
                col = swap(col, (col[v], b), comp(adj, col, v, col[v], b))
                k = key(col, V)
                if k in seen:
                    continue
                seen.add(k)
                if p_of(col, B) != 1:
                    continue
                p1 += 1
                if not lock(adj, col, B):
                    continue
                locked += 1
                if not nonhard(adj, col, B):
                    hardk[k] = dict(col)
            dists = {}
            for k, c in list(hardk.items())[:40]:
                dd = distance(adj, c, B, V)
                dists[str(dd)] = dists.get(str(dd), 0) + 1
            rec = {"graph": f"{bname}+{nflips}flips", "n": n, "root": r,
                   "root_nbr_degrees": [len(rot[v]) for v in B], "sampled_states": len(seen), "p1": p1,
                   "locked": locked, "hard": len(hardk), "hard_distance_hist(first40)": dists}
            results.append(rec)
            print(json.dumps(rec), f"{time.time() - t0:.0f}s", flush=True)
    out = HERE / f"probe_large_seed{seed}.json"
    out.write_text(json.dumps({"seed": seed, "cap": CAP, "results": results}, indent=1) + "\n")


if __name__ == "__main__":
    main()
