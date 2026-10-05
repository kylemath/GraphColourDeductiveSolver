"""beyond-short-fill: constructed examples with ell = 3 and kappa = infinity (no Kempe-only
fill at the original hole).  Hand-built graphs only; no census.  Output:
beyond-short-fill-constructions.txt.

Every number printed is recomputed here from scratch with beyond_short_fill_core.
"""
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from beyond_short_fill_core import (adj_from_edges, all_distances, anatomy, canon,  # noqa: E402
                                    colourings_minus, fmt_move, is_proper, is_target,
                                    kempe_dist, kempe_moves, mixed_dist, replay)

PRISM = [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5), (0, 3), (1, 4), (2, 5)]
NAMES7 = ["a0", "a1", "a2", "b0", "b1", "b2", "h"]


def euler_check(adj, rot):
    """rot[v] = cyclic order of neighbours; returns V - E + F (2 iff the rotation system
    is a plane embedding of a connected graph)."""
    n = len(adj)
    assert all(sorted(rot[v]) == sorted(adj[v]) for v in range(n))
    darts = {(x, y) for x in range(n) for y in adj[x]}
    seen = set()
    F = 0
    for d in darts:
        if d in seen:
            continue
        F += 1
        x, y = d
        while (x, y) not in seen:
            seen.add((x, y))
            r = rot[y]
            z = r[(r.index(x) - 1) % len(r)]   # next dart of the face
            x, y = y, z
    E = len(darts) // 2
    return n - E + F


def kempe_class(adj, k, h, s):
    cls = {canon(s)}
    st = [canon(s)]
    while st:
        x = st.pop()
        for _, nc in kempe_moves(adj, k, h, x):
            y = canon(nc)
            if y not in cls:
                cls.add(y)
                st.append(y)
    return cls


def report_example(name, n, edges, k, h, s, names=None, rot=None, full=True):
    adj = adj_from_edges(n, edges)
    nm = names or [str(i) for i in range(n)]
    print(f"\n=== {name}: n = {n}, |E| = {len(edges)}, k = {k}, hole {nm[h]}, "
          f"deg(hole) = {len(adj[h])}")
    if rot is not None:
        print(f"  plane rotation system given; V - E + F = {euler_check(adj, rot)} (2 = planar)")
    assert is_proper(adj, s)
    print("  start s:", {nm[v]: s[v] for v in range(n) if v != h})
    print("  link colours of hole:", [s[w] for w in adj[h]], " target?", is_target(adj, k, h, s))
    cls = kempe_class(adj, k, h, s)
    print(f"  Kempe class of s in G - hole: {len(cls)} state(s) up to renaming; "
          f"targets in class: {sum(is_target(adj, k, h, c) for c in cls)}")
    frozen = all(canon(nc) == canon(s) for _, nc in kempe_moves(adj, k, h, s))
    print("  s Kempe-frozen (every swap is a global renaming):", frozen)
    kap, _, csz = kempe_dist(adj, k, h, s)
    ell, path = mixed_dist(adj, k, h, s)
    print(f"  kappa = {'nofill' if kap is None else kap} (Kempe class exhausted, {csz} states); "
          f"ell = {ell}")
    print("  shortest mixed path (canonical-label moves):", [fmt_move(m) for m in path])
    for txt, hh, c in replay(adj, k, h, s, path):
        print(f"    {txt:40s} hole {nm[hh]}: link colours {[c[w] for w in adj[hh]]}")
    an = anatomy(adj, k, h, canon(s), {(hh, cc): d for (hh, cc), d in
                                        _ell_map_from(adj, k, h, s).items()})
    print(f"  anatomy: {len(an)} (slide, K1, K2) decompositions with ell(t) = 2")
    for r in an:
        r2 = dict(r)
        r2["u"] = nm[r["u"]]
        for key in ("K1", "rho_nbrs_u", "rho_nbrs_u_in_K1", "rho_nbrs_u_in_Ht", "K1_meets_Nh",
                    "common_rho_nbr_hu"):
            if key in r2:
                r2[key] = [nm[x] for x in r2[key]]
        print("    ", r2)
    if full:
        t0 = time.time()
        st, ellm, kapm = all_distances(adj, k, [h])
        J = Counter((ellm.get((h, c)), kapm[h].get(c)) for c in st[h])
        print("  joint (ell, kappa) over ALL colourings of G - hole (None = unreachable / nofill):",
              sorted(J.items(), key=str), f"[{time.time() - t0:.1f}s]")
    return adj


def _ell_map_from(adj, k, h, s, cap=3):
    """Exact mixed distances (<= cap) for every state within distance cap of s, enough for
    anatomy(): we BFS out from s and evaluate ell of each neighbour by capped BFS."""
    from collections import deque
    from beyond_short_fill_core import slide_moves
    memo = {}

    def ell_of(hh, cc):
        key = (hh, cc)
        if key not in memo:
            d, _ = mixed_dist(adj, k, hh, cc, cap=cap)
            memo[key] = d
        return memo[key]
    s = canon(s)
    out = {(h, s): ell_of(h, s)}
    for mv, u, t in slide_moves(adj, h, s):
        out[(u, canon(t))] = ell_of(u, canon(t))
    return {key: v for key, v in out.items() if v is not None}


def main():
    print("beyond-short-fill constructions: ell = 3, kappa = nofill")
    print("vertex names for the prism examples:", NAMES7, "(+ z1, z2 apices)")

    # ---- E1: planar prism example, k = 3
    E1 = PRISM + [(6, 0), (6, 1), (6, 3)]
    rot7 = _fix_rot(adj_from_edges(7, E1))   # a plane rotation system, found and checked
    s7 = (0, 1, 2, 2, 0, 1, None)
    report_example("E1 prism + degree-3 hole (planar, 3 colours)", 7, E1, 3, 6, s7, NAMES7,
                   rot7)

    # ---- E2: apex joins, k = 4, 5, 6
    for j in (1, 2, 3):
        n = 7 + j
        E = list(E1)
        for z in range(7, n):
            E += [(z, v) for v in range(z)]
        s = s7[:6] + (None,) + tuple(3 + i for i in range(j))
        report_example(f"E2.{j} E1 joined with K_{j} (k = {3 + j})", n, E, 3 + j, 6, s,
                       NAMES7 + [f"z{i + 1}" for i in range(j)], full=(j <= 2))

    # ---- E3: degree-5 hole, 4 colours: E2.1 plus edge h-b2
    E3 = E1 + [(7, v) for v in range(7)] + [(6, 5)]
    report_example("E3 E1 + apex z1 + edge h-b2 (k = 4, deg(hole) = 5)", 8, E3, 4, 6,
                   s7[:6] + (None, 3), NAMES7 + ["z1"])

    # ---- E4: planar ladders C3 x P_m with the same hole, k = 3 (per-start BFS only)
    for m in range(2, 7):
        n = 3 * m + 1
        E = []
        for L in range(m):
            a = 3 * L
            E += [(a, a + 1), (a + 1, a + 2), (a, a + 2)]
            if L:
                E += [(a - 3 + i, a + i) for i in range(3)]
        h = n - 1
        E += [(h, 0), (h, 1), (h, 3)]
        # layer 0 = (0,1,2), layer 1 = shift -1 = (2,0,1), later layers alternate shifts
        cols = [0, 1, 2, 2, 0, 1]
        for L in range(2, m):
            prev = cols[-3:]
            cols += [(c + (1 if L % 2 else -1)) % 3 for c in prev]
        s = tuple(cols[:3 * m]) + (None,)
        adj = adj_from_edges(n, E)
        assert is_proper(adj, s)
        kap, _, csz = kempe_dist(adj, 3, h, s)
        ell, path = mixed_dist(adj, 3, h, s)
        replay(adj, 3, h, s, path)
        print(f"\n=== E4 ladder C3 x P{m} + hole (planar, k = 3): n = {n}: kappa = "
              f"{'nofill' if kap is None else kap} (class {csz}), ell = {ell}, path "
              f"{[fmt_move(mv) for mv in path]}")

    # ---- negative checks on planar 4-colour constructions
    print("\n=== planar 4-colour attempts (icosahedron-based; negative)")
    E = []
    for i in range(5):
        E += [(0, 1 + i), (1 + i, 1 + (i + 1) % 5), (6 + i, 6 + (i + 1) % 5), (11, 6 + i),
              (1 + i, 6 + i), (1 + (i + 1) % 5, 6 + i)]
    ico = adj_from_edges(12, E)
    iso = ico + [[]]
    cols = colourings_minus(iso, 4, 12)
    sizes = []
    seen = set()
    for c in cols:
        if c not in seen:
            cl = kempe_class(iso, 4, 12, c)
            seen |= cl
            sizes.append(len(cl))
    print(f"  icosahedron: {len(cols)} 4-colourings up to renaming; Kempe class sizes {sizes}"
          " (every 4-colouring is Kempe-frozen)")

    def joint(name, n, EE, h):
        adj = adj_from_edges(n, EE)
        st, ellm, kapm = all_distances(adj, 4, [h])
        J = Counter((ellm.get((h, c)), kapm[h].get(c)) for c in st[h])
        print(f"  {name}: deg(hole) = {len(adj[h])}, joint (ell, kappa) = {sorted(J.items(), key=str)}")
    joint("icosahedron, hole = vertex 0", 12, E, 0)
    cn = sorted(set(ico[0]) & set(ico[1]))
    EA = [x for x in E if set(x) != {0, 1}] + [(12, 0), (12, 1)] + [(12, c) for c in cn]
    joint("icosahedron with edge 0-1 replaced by a degree-4 vertex", 13, EA, 12)
    pent = set(ico[0]) & set(ico[1]) | set(ico[1]) & set(ico[2]) | {0, 1, 2}
    EB = [x for x in E if set(x) not in ({0, 1}, {1, 2})] + [(12, p) for p in sorted(pent)]
    joint("icosahedron with face-edges 0-1, 1-2 removed, degree-5 vertex in the pentagon",
          13, EB, 12)


def _fix_rot(adj):
    """Find a plane rotation system for the 7-vertex example by brute force over neighbour
    cyclic orders (tiny), so the planarity certificate is computed, not asserted."""
    from itertools import permutations
    n = len(adj)
    opts = []
    for v in range(n):
        nb = adj[v]
        first, rest = nb[0], nb[1:]
        opts.append([[first] + list(p) for p in permutations(rest)])
    import itertools
    for choice in itertools.product(*opts):
        if euler_check(adj, list(choice)) == 2:
            return list(choice)
    raise AssertionError("not planar")


if __name__ == "__main__":
    main()
