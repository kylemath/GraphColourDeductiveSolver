"""WP13 generator core: rotation-system triangulations, local moves, validation, canonical form.

A triangulation is a list `rot` of neighbour lists (vertex v -> cyclic list of neighbours),
the same object returned by longtable/mass_core.parse_ascii.  Face convention (shared with
mass_core.validate_triangulation): the dart (a, b) is followed by (b, succ_b(a)), where
succ_b(a) is the entry after a in rot[b] (cyclically); every such orbit has length 3.

Moves (all preserve "simple spherical triangulation with minimum degree >= 5"):
  * flip(u, v):   replace edge uv by the opposite diagonal xy; allowed only when
                  deg u >= 6, deg v >= 6 and x, y non-adjacent.
  * split(v,i,k): vertex splitting (inverse edge contraction) of a vertex of degree d >= 6
                  along neighbours N[i], N[i+k] with 3 <= k <= d-3; adds one vertex.
Stdlib only.
"""
import random


def succ(rot, b, a):
    ns = rot[b]
    return ns[(ns.index(a) + 1) % len(ns)]


def pred(rot, b, a):
    ns = rot[b]
    return ns[(ns.index(a) - 1) % len(ns)]


# ---------------------------------------------------------------- validation

def check_triangulation(rot, min_degree=5):
    """Independent re-implementation of the corpus checks; raises AssertionError."""
    n = len(rot)
    assert n >= 4
    for v, ns in enumerate(rot):
        assert len(ns) >= min_degree, ("degree", v, len(ns))
        assert len(set(ns)) == len(ns), ("multi-edge", v)
        assert v not in ns, ("loop", v)
        for w in ns:
            assert 0 <= w < n and v in rot[w], ("asymmetric", v, w)
    e = sum(len(ns) for ns in rot) // 2
    assert e == 3 * n - 6, ("edges", e, n)
    seen, faces = set(), 0
    for v, ns in enumerate(rot):
        for w in ns:
            if (v, w) in seen:
                continue
            d, L = (v, w), 0
            while d not in seen:
                seen.add(d)
                L += 1
                a, b = d
                d = (b, succ(rot, b, a))
            assert d == (v, w) and L == 3, ("face", v, w, L)
            faces += 1
    assert n - e + faces == 2, ("euler", n, e, faces)
    # connectivity (Euler with all faces triangles already implies sphere if connected)
    stack, mark = [0], {0}
    while stack:
        x = stack.pop()
        for y in rot[x]:
            if y not in mark:
                mark.add(y)
                stack.append(y)
    assert len(mark) == n, "disconnected"
    return True


# ---------------------------------------------------------------- moves

def flip_ok(rot, u, v):
    if len(rot[u]) < 6 or len(rot[v]) < 6:
        return None
    x = succ(rot, v, u)  # face (u, v, x)
    y = succ(rot, u, v)  # face (v, u, y)
    if x == y or y in rot[x]:
        return None
    return x, y


def flip(rot, u, v, xy=None):
    """Flip edge uv in place; returns (x, y).  Caller must have checked flip_ok."""
    x, y = xy if xy else flip_ok(rot, u, v)
    rot[u].remove(v)
    rot[v].remove(u)
    # in rot[x], u follows v (face u,v,x: succ_x(v) = u); put y between them
    rx = rot[x]
    rx.insert(rx.index(v) + 1, y)
    ry = rot[y]
    ry.insert(ry.index(u) + 1, x)
    return x, y


def split(rot, v, i, k):
    """Split v (degree d >= 6) into v and new vertex w; v keeps N[i..i+k], w gets N[i+k..i+d]."""
    d = len(rot[v])
    assert d >= 6 and 3 <= k <= d - 3
    N = rot[v][i:] + rot[v][:i]
    w = len(rot)
    keep = N[: k + 1]
    give = N[k:] + [N[0]]
    rot[v] = keep + [w]
    rot.append(give + [v])
    for z in N[k + 1:]:
        rz = rot[z]
        rz[rz.index(v)] = w
    # N[k] and N[0] are adjacent to both v and w; insert w next to v on the side of w's region
    for z in (N[k], N[0]):
        rz = rot[z]
        p = rz.index(v)
        nxt = rz[(p + 1) % len(rz)]
        if nxt in give or nxt == w:
            rz.insert(p + 1, w)
        else:
            rz.insert(p, w)
    return w


def orient_fix(rot):
    """Reverse all rotations if the face convention fails (used after geometric builds)."""
    try:
        check_triangulation(rot)
        return rot
    except AssertionError:
        r2 = [list(reversed(ns)) for ns in rot]
        check_triangulation(r2)
        return r2


# ---------------------------------------------------------------- invariants

def degree_five(rot):
    return [v for v, ns in enumerate(rot) if len(ns) == 5]


def root_type(rot, r):
    """(number of degree-5, degree-6, degree>=7 neighbours) of r."""
    a = b = c = 0
    for w in rot[r]:
        d = len(rot[w])
        if d == 5:
            a += 1
        elif d == 6:
            b += 1
        else:
            c += 1
    return (a, b, c)


# ---------------------------------------------------------------- canonical form

def _code_from(rot, v0, w0, mirror):
    n = len(rot)
    num = [-1] * n
    num[v0] = 0
    first = [None] * n
    first[v0] = w0
    order = [v0]
    code = []
    head = 0
    cnt = 1
    while head < len(order):
        v = order[head]
        head += 1
        ns = rot[v]
        d = len(ns)
        s = ns.index(first[v])
        for t in range(d):
            w = ns[(s - t) % d] if mirror else ns[(s + t) % d]
            if num[w] < 0:
                num[w] = cnt
                cnt += 1
                first[w] = v
                order.append(w)
            code.append(num[w])
        code.append(-1)
    return tuple(code)


def _canonical(rot):
    inv = [(len(ns), tuple(sorted(len(rot[w]) for w in ns))) for ns in rot]
    cnt = {}
    for x in inv:
        cnt[x] = cnt.get(x, 0) + 1
    best_cls = min(cnt, key=lambda c: (cnt[c], c))
    best, start = None, None
    for v in range(len(rot)):
        if inv[v] != best_cls:
            continue
        for w in rot[v]:
            for m in (False, True):
                c = _code_from(rot, v, w, m)
                if best is None or c < best:
                    best, start = c, (v, w, m)
    return (best_cls, best), start


def canonical_code(rot):
    """Min over darts and both orientations of a BFS code: an isomorphism invariant (reflections
    identified) that is complete for connected plane maps.  Starting darts are restricted to
    vertices of the rarest iso-invariant class (degree, sorted neighbour degrees) for speed."""
    return _canonical(rot)[0]


def relabel_canonical(rot):
    """Isomorphic copy relabelled by BFS order from the canonical start (deterministic output)."""
    _, (v, w, m) = _canonical(rot)
    return _relabel_from(rot, v, w, m)


def _relabel_from(rot, v0, w0, mirror):
    n = len(rot)
    num = [-1] * n
    num[v0] = 0
    first = [None] * n
    first[v0] = w0
    order = [v0]
    head, cnt = 0, 1
    while head < len(order):
        v = order[head]
        head += 1
        ns = rot[v]
        for w in ns:
            if num[w] < 0:
                num[w] = cnt
                cnt += 1
                order.append(w)
    out = [None] * n
    for v in range(n):
        ns = [num[w] for w in rot[v]]
        out[num[v]] = list(reversed(ns)) if mirror else ns
    # rotate each list to start at its smallest label (cosmetic)
    out = [ns[ns.index(min(ns)):] + ns[: ns.index(min(ns))] for ns in out]
    return out


def to_ascii(rot):
    """plantri-style ASCII line; only defined for n <= 26."""
    if len(rot) > 26:
        return None
    return f"{len(rot)} " + ",".join("".join(chr(97 + w) for w in ns) for ns in rot)


def parse_ascii(line):
    n, code = line.strip().split(" ", 1)
    rot = [[ord(ch) - 97 for ch in row] for row in code.split(",")]
    assert len(rot) == int(n)
    return rot
