#!/usr/bin/env python3
"""[UNTESTED] Path 3 builders: constructed plane triangulations for multi-class Kempe searches.

Written by hand on the MacBook on 6 Oct 2026 and NEVER RUN there (battery rule). Run it on the Studio.
Every instance is validated by `analyse()` below before anything is written; a failed check raises and the
instance is skipped with a message (nothing is "fixed" silently).

Families (see ../MathPath3Constructions.md for mechanisms and predictions):
  AK   akempic (3,6)-triangulations P(a,b,s): triangular-lattice torus C/2L' modulo z -> -z      [Mohar 1985]
  RAK  repair of AK: delete the four degree-3 vertices (min degree 5; frozen colouring survives)
  FL   Florek's two-pole belt G_n (edge list of belt-joined.md section 1)
  TU   two-pole tube: poles of degree n, L rings of n, antiprism bands (TU(n,2) = G_n)
  SL   slipped two-pole stack: ring sizes differ by one somewhere (a 5-7 dislocation, or a 5-6 one at ring 1)
  CF   cone + Florek cap: apex v of degree 5 with a flat cone of radius R, E rings, then a pole of degree 5R
  CC   double cone: two flat cones of radius R joined by one antiprism band (CC(1) = icosahedron)

Outputs per instance NAME in OUTDIR:
  NAME.edges   "n E" + edges          (kmap, kreach)
  NAME.tri     "n F" + oriented faces (Studio intel fast/kempe.cpp; all faces in one consistent orientation)
  NAME.json    metadata: degrees, orbits of degree-5 vertices, separating 3/4-cycles, diamond / 2.122 proxies,
               rotation system, plantri ascii (n <= 26 only), special colourings (AK, RAK)
  all.g        one "G n NAME nf faces..." line per instance (MathRadiusCensus/census.cpp input)

Usage (Studio):  python3 path3_build.py --out OUTDIR --preset core|heavy|ak|all
                 python3 path3_build.py --out OUTDIR --only TU --n 9 --L 4      (single instance)
"""
import argparse
import json
import math
import os
import sys
from collections import defaultdict


# ----------------------------------------------------------------------------------------------------------
# construction helper
class Tri:
    def __init__(self, family, params):
        self.family, self.params = family, dict(params)
        self.n, self.faces, self.label = 0, [], []
        self.colourings = {}      # name -> list of colours (special colourings, e.g. the AK frozen one)
        self.notes = []

    @property
    def name(self):
        return self.family + "_" + "_".join("%s%s" % (k, v) for k, v in self.params.items())

    def v(self, lab):
        self.label.append(lab)
        self.n += 1
        return self.n - 1

    def ring(self, m, tag):
        return [self.v("%s%d" % (tag, i)) for i in range(m)]

    def f(self, a, b, c):
        self.faces.append((a, b, c))

    def fan(self, p, R):
        for i in range(len(R)):
            self.f(p, R[i], R[(i + 1) % len(R)])

    def band(self, X, Y, shift=0):
        """Triangulated annulus between cycles X and Y (same rotational direction), |len X - len Y| <= 1.
        Equal lengths: antiprism, X_i ~ Y_i, Y_{i-1} (Florek's u_i ~ v_i, v_{i-1}).
        Lengths m, m+1: 'slip' band; the lower-ring vertex X_0 gets 3 neighbours in Y (Y_m, Y_0, Y_1) and
        Y_0 gets exactly 1 neighbour in X (X_0).  `shift` rotates the LARGER ring (for equal rings: Y), which moves
        the vertex with a single neighbour across the band.  Triangles are stored unoriented; analyse() orients."""
        if len(X) == len(Y) + 1:            # larger ring given first: swap roles, keep the shift on the larger ring
            return self.band(Y, X, shift)
        k = shift % len(Y)
        Y = Y[k:] + Y[:k]
        m = len(X)
        if len(Y) == m:
            for i in range(m):
                self.f(X[i], Y[i], X[(i + 1) % m])
                self.f(X[(i + 1) % m], Y[i], Y[(i + 1) % m])
        elif len(Y) == m + 1:
            for i in range(m):
                self.f(X[i], Y[i], Y[i + 1])
                self.f(X[i], Y[i + 1], X[(i + 1) % m])
            self.f(X[0], Y[m], Y[0])
        else:
            raise ValueError("band: ring sizes differ by more than one")


def cone(T, R, tag="c"):
    """Flat 5-fold cone of radius R: apex (degree 5 once closed), rings 1..R of 5i vertices.
    Returns (apex, rings). Inside the cone: ring-R corners (positions s*R) have degree 3, sides degree 4."""
    apex = T.v(tag + "apex")
    rings = [[apex]]
    for i in range(1, R + 1):
        rings.append(T.ring(5 * i, "%sr%d_" % (tag, i)))
    for i in range(1, R + 1):
        lo, up = rings[i - 1], rings[i]
        for s in range(5):
            lower = [lo[(s * (i - 1) + j) % len(lo)] for j in range(i)]      # corner s .. corner s+1 of ring i-1
            upper = [up[(s * i + j) % len(up)] for j in range(i + 1)]       # corner s .. corner s+1 of ring i
            for j in range(i):
                T.f(lower[j], upper[j + 1], upper[j])
            for j in range(i - 1):
                T.f(lower[j], lower[j + 1], upper[j + 1])
    return apex, rings


# ----------------------------------------------------------------------------------------------------------
# families
def florek(n):
    """G_n exactly as belt-joined.md section 1: poles a, b; u_i ~ a, v_i ~ b, u_i u_{i+1}, v_i v_{i+1}, u_i v_i,
    u_i v_{i-1}. Degrees: belt 5, poles n. Florek (arXiv:2511.00485, abstract): at least floor(n/6) Kempe classes."""
    T = Tri("FL", {"n": n})
    a = T.v("a")
    u = T.ring(n, "u")
    vv = T.ring(n, "v")
    b = T.v("b")
    T.fan(a, u)
    T.band(u, vv)
    T.fan(b, vv)
    return T


def stack(sizes, shifts=None, family="SL", params=None):
    """Two-pole stack: pole a, rings of the given sizes (consecutive sizes differ by <= 1), pole b."""
    shifts = shifts or [0] * (len(sizes) - 1)
    if params is None:
        params = {"rings": "-".join(map(str, sizes))}
        if any(shifts):
            params["sh"] = "-".join(map(str, shifts))
    T = Tri(family, params)
    a = T.v("a")
    R = [T.ring(m, "r%d_" % (k + 1)) for k, m in enumerate(sizes)]
    b = T.v("b")
    T.fan(a, R[0])
    for k in range(len(sizes) - 1):
        T.band(R[k], R[k + 1], shifts[k])
    T.fan(b, R[-1])
    return T


def tube(n, L):
    return stack([n] * L, family="TU", params={"n": n, "L": L})


def cone_florek(R, E):
    """CF(R,E): flat cone of radius R around apex v, then E rings of 5R (antiprism), then a pole of degree 5R.
    Degrees: apex 5, cone corners 5, cone interior 6, inner rings 6, last ring 5, pole 5R."""
    T = Tri("CF", {"R": R, "E": E})
    apex, rings = cone(T, R)
    prev = rings[-1]
    for e in range(E):
        D = T.ring(5 * R, "d%d_" % (e + 1))
        T.band(prev, D)
        prev = D
    b = T.v("pole")
    T.fan(b, prev)
    T.notes.append("hole of interest: vertex 0 (cone apex), flat (all-degree-6) ball of radius %d around it" % (R - 1))
    return T


def double_cone(R, twist=0):
    """CC(R,twist): two flat cones of radius R glued by one antiprism band (any gluing of two discs is a sphere).
    Degrees: apices 5, corners 5 (3 + 2), others 6.  CC(1,0) is the icosahedron."""
    T = Tri("CC", {"R": R, "tw": twist})
    a1, r1 = cone(T, R, "p")
    a2, r2 = cone(T, R, "q")
    T.band(r1[-1], list(reversed(r2[-1])), twist)
    T.notes.append("holes of interest: apices %d, %d (flat ball of radius %d)" % (a1, a2, R - 1))
    return T


def akempic(a, b, s):
    """AK(a,b,s): (3,6)-triangulation C/Lam modulo z -> -z, Lam = 2*<(a,0),(s,b)> inside the triangular lattice Z^2
    (neighbours +-(1,0), +-(0,1), +-(1,-1)).  Order 2ab+2, four degree-3 vertices (the 2-torsion points).
    RECONSTRUCTION [from memory: (3,6)-sphere triangulations are such quotients]; Florek (arXiv:2504.13316,
    read) describes them by index-vectors (K, M, S+) and |P| = 2KM+2.  The special colouring c0(x,y) =
    (x mod 2) + 2 (y mod 2) is well defined (Lam is inside 2Z^2, and -p = p mod 2) and nonsingular.
    The builder tests directly whether c0 is FROZEN (all six bichromatic subgraphs connected), which is the
    akempic property for this colouring; no index convention is needed for that test."""
    T = Tri("AK", {"a": a, "b": b, "s": s})
    A2, B2x, B2y = 2 * a, 2 * s, 2 * b

    def red(x, y):
        k = y // B2y
        x -= k * B2x
        y -= k * B2y
        return (x % A2, y)

    def key(x, y):
        return min(red(x, y), red(-x, -y))

    ids = {}
    for x in range(A2):
        for y in range(B2y):
            k = key(x, y)
            if k not in ids:
                ids[k] = T.v("p%d_%d" % k)
    faces = set()
    for x in range(A2):
        for y in range(B2y):
            up = (key(x, y), key(x + 1, y), key(x, y + 1))
            dn = (key(x + 1, y), key(x, y + 1), key(x + 1, y + 1))
            for t in (up, dn):
                fs = frozenset(ids[q] for q in t)
                if len(fs) != 3:
                    raise ValueError("AK(%d,%d,%d): degenerate face" % (a, b, s))
                faces.add(fs)
    if len(faces) != 4 * a * b:
        raise ValueError("AK(%d,%d,%d): %d faces, expected %d (non-simple quotient)" % (a, b, s, len(faces), 4 * a * b))
    T.faces = [tuple(sorted(f)) for f in faces]
    col = [0] * T.n
    for (x, y), i in ids.items():
        col[i] = (x % 2) + 2 * (y % 2)
    T.colourings["c0_nonsingular"] = col
    if b == 1:
        T.notes.append("Florek Thm 1.3 (read) in HIS convention: index-vector (1,n,s) akempic iff gcd(s,n)=gcd(s+1,n)=1;"
                       " here gcd(s,n)=%d, gcd(s+1,n)=%d; whether our s equals his S+ is NOT checked"
                       % (math.gcd(s, a), math.gcd(s + 1, a)))
    return T


def repair_delete_deg3(T0):
    """RAK: delete every degree-3 vertex x and make its link triangle a face.  [hand] If c0 is frozen on T0 then
    c0 restricted is frozen on the result: each bichromatic subgraph of a frozen colouring of a triangulation is
    a tree (edge count 3n-6 = sum over the six pairs of (n_i + n_j - 1)); x is a leaf in the three trees that
    contain it, and deleting leaves keeps trees connected.  Degrees: the 3 neighbours of x drop by one.
    Stronger [hand, MathPath3Constructions.md section 1.3]: deleting a degree-3 vertex is Kempe-neutral, i.e. the
    Kempe graphs of T0 and T0 - x are isomorphic, so kappa(RAK) = kappa(AK) >= 2 when AK is akempic."""
    adj = defaultdict(set)
    for f in T0.faces:
        for i in range(3):
            adj[f[i]].add(f[(i + 1) % 3])
            adj[f[i]].add(f[(i + 2) % 3])
    dead = [x for x in range(T0.n) if len(adj[x]) == 3]
    for x in dead:
        for y in adj[x]:
            if y in dead:
                raise ValueError("two degree-3 vertices adjacent")
    faces = [f for f in T0.faces if not (set(f) & set(dead))]
    for x in dead:
        faces.append(tuple(sorted(adj[x])))
    keep = [x for x in range(T0.n) if x not in dead]
    new = {x: i for i, x in enumerate(keep)}
    T = Tri("RAK", T0.params)
    for x in keep:
        T.v(T0.label[x])
    T.faces = [tuple(new[q] for q in f) for f in faces]
    for k, col in T0.colourings.items():
        T.colourings[k + "_restricted"] = [col[x] for x in keep]
    T.notes = list(T0.notes) + ["deleted degree-3 vertices (old labels) %s" % dead]
    return T


# ----------------------------------------------------------------------------------------------------------
# validation and invariants
def analyse(T):
    n, F = T.n, T.faces
    if any(len(set(f)) != 3 for f in F):
        raise ValueError("face with repeated vertex")
    if len({frozenset(f) for f in F}) != len(F):
        raise ValueError("repeated face")
    ef = defaultdict(list)
    for i, f in enumerate(F):
        for k in range(3):
            ef[frozenset((f[k], f[(k + 1) % 3]))].append(i)
    if any(len(l) != 2 for l in ef.values()):
        raise ValueError("an edge is not in exactly two faces")
    E = len(ef)
    if n - E + len(F) != 2 or E != 3 * n - 6:
        raise ValueError("not a sphere triangulation: n=%d E=%d F=%d" % (n, E, len(F)))
    # consistent orientation (BFS over faces)
    orient = {0: tuple(F[0])}
    todo = [0]
    while todo:
        i = todo.pop()
        f = orient[i]
        for k in range(3):
            x, y = f[k], f[(k + 1) % 3]
            for j in ef[frozenset((x, y))]:
                if j == i:
                    continue
                g = F[j]
                z = [q for q in g if q != x and q != y][0]
                want = (y, x, z)                       # neighbour must traverse the shared edge as y -> x
                if j in orient:
                    o = orient[j]
                    if (y, x) not in {(o[t], o[(t + 1) % 3]) for t in range(3)}:
                        raise ValueError("non-orientable / inconsistent")
                else:
                    orient[j] = want
                    todo.append(j)
    if len(orient) != len(F):
        raise ValueError("face graph disconnected")
    OF = [orient[i] for i in range(len(F))]
    # rotation system (one fixed rotational sense) and manifold check
    nxt = defaultdict(dict)
    for (a, b, c) in OF:
        nxt[a][b] = c
        nxt[b][c] = a
        nxt[c][a] = b
    rot = []
    for x in range(n):
        start = next(iter(nxt[x]))
        r = [start]
        while True:
            y = nxt[x][r[-1]]
            if y == start:
                break
            r.append(y)
            if len(r) > n:
                raise ValueError("bad rotation")
        if len(r) != len(nxt[x]):
            raise ValueError("vertex %d: link is not a single cycle" % x)
        rot.append(r)
    deg = [len(r) for r in rot]
    adj = [set(r) for r in rot]
    facesets = {frozenset(f) for f in F}
    sep3 = []
    for a in range(n):
        for b in adj[a]:
            if b <= a:
                continue
            for c in adj[a] & adj[b]:
                if c > b and frozenset((a, b, c)) not in facesets:
                    sep3.append((a, b, c))
    sep4 = 0                                         # chordless 4-cycles = separating 4-cycles in a triangulation
    for x in range(n):
        for z in range(x + 1, n):
            if z in adj[x]:
                continue
            C = sorted(adj[x] & adj[z])
            for i in range(len(C)):
                for j in range(i + 1, len(C)):
                    if C[j] not in adj[C[i]]:
                        sep4 += 1
    sep4 //= 2                                       # each 4-cycle x-y-z-w is found from {x,z} and from {y,w}
    diamond = []
    for e, (i, j) in ef.items():
        a, b = tuple(e)
        c = [q for q in F[i] if q not in e][0]
        d = [q for q in F[j] if q not in e][0]
        if deg[a] == deg[b] == deg[c] == deg[d] == 5:
            diamond.append(sorted((a, b, c, d)))
    p2122 = [x for x in range(n) if deg[x] == 5 and any(
        deg[rot[x][k]] == 5 and deg[rot[x][(k + 1) % 5]] == 6 and deg[rot[x][(k + 2) % 5]] == 5 for k in range(5))]
    orbits = vertex_orbits(rot)
    naut = orbits.pop("_naut")
    d5 = [x for x in range(n) if deg[x] == 5]
    reps = sorted({min(o) for o in orbits.values() if deg[min(o)] == 5})
    info = {
        "name": T.name, "family": T.family, "params": T.params, "n": n, "E": E, "F": len(F),
        "degree_histogram": {str(d): deg.count(d) for d in sorted(set(deg))},
        "min_degree": min(deg), "n_deg5": len(d5),
        "separating_triangles": len(sep3), "separating_4cycles": sep4,
        "four_connected": len(sep3) == 0,
        "diamond_proxy": len(diamond) > 0, "diamond_examples": diamond[:3],
        "c2122_proxy_holes": p2122,
        "n_automorphisms": naut,
        "deg5_orbit_reps": [{"v": r, "orbit_size": len(orbits[r]),
                             "link_degrees": [deg[y] for y in rot[r]]} for r in reps],
        "labels": T.label, "notes": T.notes,
        "rotation": rot, "faces_oriented": OF,
        "core_class_candidate": min(deg) >= 5 and len(sep3) == 0,
    }
    if n <= 26:  # plantri -a style (letters); the rotation sense is ours, plantri's is clockwise (mirror if needed)
        info["plantri_ascii"] = "%d " % n + ",".join("".join(chr(97 + y) for y in r) for r in rot)
    for k, col in T.colourings.items():
        info.setdefault("special_colourings", {})[k] = {"colouring": col, **colouring_report(col, adj, deg)}
    return info


def vertex_orbits(rot):
    """Orbits of the automorphism group of the embedding (rotations and reflections) by BFS codes from darts."""
    n = len(rot)

    def code(u, w, mirror):
        lab = [-1] * n
        lab[u] = 0
        order = [u]
        parent = {u: w}
        out = []
        i = 0
        while i < len(order):
            x = order[i]
            i += 1
            r = rot[x][::-1] if mirror else rot[x]
            s = r.index(parent[x])
            for k in range(len(r)):
                y = r[(s + k) % len(r)]
                if lab[y] < 0:
                    lab[y] = len(order)
                    order.append(y)
                    parent[y] = x
                out.append(lab[y])
            out.append(-1)
        return tuple(out), order

    ref, o0 = code(0, rot[0][0], False)
    par = list(range(n))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    naut = 0
    for u in range(n):
        for w in rot[u]:
            for m in (False, True):
                c, o = code(u, w, m)
                if c == ref:
                    naut += 1
                    for k in range(n):
                        a, b = find(o0[k]), find(o[k])
                        if a != b:
                            par[a] = b
    orb = defaultdict(list)
    for x in range(n):
        orb[find(x)].append(x)
    res = {min(l): l for l in orb.values()}
    res["_naut"] = naut
    return res


def colouring_report(col, adj, deg):
    n = len(col)
    proper = all(col[x] != col[y] for x in range(n) for y in adj[x])
    conn = {}
    for i in range(4):
        for j in range(i + 1, 4):
            S = [x for x in range(n) if col[x] in (i, j)]
            if not S:
                conn["%d%d" % (i, j)] = 0
                continue
            seen = {S[0]}
            st = [S[0]]
            while st:
                x = st.pop()
                for y in adj[x]:
                    if col[y] in (i, j) and y not in seen:
                        seen.add(y)
                        st.append(y)
            comps, rest = 1, set(S) - seen
            while rest:                                # count components
                z = rest.pop()
                comps += 1
                st = [z]
                while st:
                    x = st.pop()
                    for y in adj[x]:
                        if col[y] in (i, j) and y in rest:
                            rest.discard(y)
                            st.append(y)
            conn["%d%d" % (i, j)] = comps
    odd = [sum(1 for x in range(n) if col[x] == i and deg[x] % 2) % 2 for i in range(4)]
    return {"proper": proper, "bichromatic_components": conn,
            "frozen": proper and all(v == 1 for v in conn.values()),
            "odd_vertex_parity_by_colour": odd}


# ----------------------------------------------------------------------------------------------------------
def write(T, out, allg):
    try:
        info = analyse(T)
    except ValueError as e:
        print("SKIP %s: %s" % (T.name, e), file=sys.stderr)
        return None
    name = T.name
    base = os.path.join(out, name)
    E = sorted({tuple(sorted((f[k], f[(k + 1) % 3]))) for f in T.faces for k in range(3)})
    with open(base + ".edges", "w") as fh:
        fh.write("%d %d\n" % (T.n, len(E)) + "".join("%d %d\n" % e for e in E))
    with open(base + ".tri", "w") as fh:
        fh.write("%d %d\n" % (T.n, len(info["faces_oriented"])) + "".join("%d %d %d\n" % tuple(f) for f in info["faces_oriented"]))
    with open(base + ".json", "w") as fh:
        json.dump(info, fh)
    allg.write("G %d %s %d %s\n" % (T.n, name, len(T.faces), " ".join("%d %d %d" % tuple(f) for f in info["faces_oriented"])))
    print(json.dumps({k: info[k] for k in ("name", "n", "min_degree", "n_deg5", "separating_triangles",
                                             "separating_4cycles", "diamond_proxy", "c2122_proxy_holes",
                                             "n_automorphisms")}
                     | {"orbit_reps": [r["v"] for r in info["deg5_orbit_reps"]],
                        "frozen": {k: v["frozen"] for k, v in info.get("special_colourings", {}).items()}}))
    return info


def presets(which):
    L = []
    if which in ("core", "all"):
        L += [florek(n) for n in (5, 6, 7, 8, 9, 10, 11, 12)]                       # 12..26; n=5 icosahedron
        L += [tube(n, Lr) for n, Lr in ((6, 3), (6, 4), (6, 5), (7, 3), (8, 3), (8, 4), (9, 3), (9, 4), (12, 3))]
        L += [stack(s) for s in ([8, 9, 9], [9, 10, 10], [10, 11, 11], [11, 12, 12], [8, 8, 9, 9], [9, 9, 10, 10],
                                 [9, 10, 10, 9])]
        L += [stack([9, 10, 9, 9], [0, 5, 0])]      # two dislocations in adjacent bands (shift keeps degrees >= 5)
        L += [cone_florek(2, 1), cone_florek(2, 2), cone_florek(2, 3), cone_florek(3, 1)]
        L += [double_cone(1), double_cone(2, 0), double_cone(2, 1), double_cone(2, 2)]
    if which in ("ak", "core", "all"):
        top = 17 if which == "core" else 32        # |P| = 2nn+2 <= 64; RAK order 2nn-2
        for nn in range(1, top):
            for b in ((1,) if which == "core" else [d for d in range(1, nn + 1) if nn % d == 0]):
                a = nn // b
                for s in range(a):
                    try:
                        P = akempic(a, b, s)
                    except ValueError as e:
                        print("SKIP AK(%d,%d,%d): %s" % (a, b, s, e), file=sys.stderr)
                        continue
                    adj = defaultdict(set)
                    for f in P.faces:
                        for i in range(3):
                            adj[f[i]] |= {f[(i + 1) % 3], f[(i + 2) % 3]}
                    if not colouring_report(P.colourings["c0_nonsingular"], adj, [len(adj[x]) for x in range(P.n)])["frozen"]:
                        continue                   # keep only akempic (frozen c0) instances
                    L.append(P)
                    try:
                        L.append(repair_delete_deg3(P))
                    except ValueError as e:
                        print("SKIP RAK(%d,%d,%d): %s" % (a, b, s, e), file=sys.stderr)
    if which in ("heavy", "all"):
        L += [tube(9, 5), tube(12, 4), stack([9, 9, 10, 10, 10]), cone_florek(3, 2), double_cone(3, 0)]
    return L


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--preset", default="core", choices=["core", "heavy", "ak", "all"])
    ap.add_argument("--only", choices=["FL", "TU", "SL", "CF", "CC", "AK", "RAK"])
    ap.add_argument("--n", type=int)
    ap.add_argument("--L", type=int)
    ap.add_argument("--sizes", help="SL ring sizes, e.g. 9,10,10")
    ap.add_argument("--R", type=int)
    ap.add_argument("--E", type=int, default=1)
    ap.add_argument("--twist", type=int, default=0)
    ap.add_argument("--a", type=int)
    ap.add_argument("--b", type=int, default=1)
    ap.add_argument("--s", type=int)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    if a.only:
        T = {"FL": lambda: florek(a.n), "TU": lambda: tube(a.n, a.L),
             "SL": lambda: stack([int(x) for x in a.sizes.split(",")]),
             "CF": lambda: cone_florek(a.R, a.E), "CC": lambda: double_cone(a.R, a.twist),
             "AK": lambda: akempic(a.a, a.b, a.s),
             "RAK": lambda: repair_delete_deg3(akempic(a.a, a.b, a.s))}[a.only]()
        Ls = [T]
    else:
        Ls = presets(a.preset)
    with open(os.path.join(a.out, "all.g"), "a") as allg:
        for T in Ls:
            write(T, a.out, allg)


if __name__ == "__main__":
    main()
