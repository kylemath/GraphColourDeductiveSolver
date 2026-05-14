#!/usr/bin/env python3
"""
mtl_bfs_test.py — Independent BFS test of the Merge-Tolerant Lifting claim.

Written from scratch. Zero dependency on any agent code.

CLAIM (existential MTL):
  For a planar triangulation G with a degree-5 vertex v, and ANY
  proper 5-colouring of G-v, there exists a proper 4-colouring of
  G-v reachable via Kempe chain swaps such that v's neighbours use
  at most 3 of {1,2,3,4} — leaving a free colour to extend to v.

WHAT THIS SCRIPT DOES:
  1. Enumerate every proper 5-colouring of G-v  (brute force).
  2. Build the full Kempe reconfiguration graph  (explicit adjacency).
  3. For each colouring that uses colour 5, BFS to the nearest proper
     4-colouring (colours ⊆ {1,2,3,4}).
  4. At that endpoint, report which colours sit on v's neighbours.
  5. Also check the weaker existential version via connected components.

Two test graphs:
  A. Pentagonal bipyramid  (7 vertices).  Sanity check — always passes
     because vertex 6 is adjacent to all of v's neighbours, forcing
     the 5-cycle to use only 3 colours in any valid 4-colouring.
  B. 8-vertex triangulation (non-trivial).  Some 4-colourings DO put
     all 4 colours on v's neighbours.  The real test.
"""

from itertools import product
from collections import deque, Counter


def test_graph(name, vertices, edges, v_nbrs):
    """Run the full MTL BFS test on one graph G-v."""
    palette = (1, 2, 3, 4, 5)

    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)

    print(f"\n{'═' * 62}")
    print(f"  {name}")
    print(f"  G-v: {len(vertices)} vertices, {len(edges)} edges")
    print(f"  v's neighbours in G: {list(v_nbrs)}")
    for v in vertices:
        print(f"    {v}: adj={sorted(adj[v])}, deg={len(adj[v])}")
    print(f"{'═' * 62}")

    # ── 1. Enumerate proper 5-colourings ──────────────────────

    def is_proper(c):
        return all(c[a] != c[b] for a, b in edges)

    def key_of(c):
        return tuple(c[v] for v in vertices)

    colourings = []
    key_to_idx = {}
    for vals in product(palette, repeat=len(vertices)):
        c = dict(zip(vertices, vals))
        if is_proper(c):
            k = key_of(c)
            key_to_idx[k] = len(colourings)
            colourings.append(c)

    N = len(colourings)
    is_4 = [all(c[v] <= 4 for v in vertices) for c in colourings]
    four_set = frozenset(i for i, flag in enumerate(is_4) if flag)
    starts = [i for i in range(N) if not is_4[i]]

    good_4 = sum(
        1 for i in four_set
        if len({colourings[i][v] for v in v_nbrs}) < 4
    )

    print(f"\n  Proper 5-colourings of G-v:  {N}")
    print(f"  4-colourings (⊆ {{1..4}}):    {len(four_set)}")
    print(f"    with free colour for v:    {good_4}")
    print(f"    WITHOUT free colour for v: {len(four_set) - good_4}")
    print(f"  Colourings using colour 5:   {len(starts)}")

    # ── 2. Build Kempe reconfiguration graph ──────────────────

    def kempe_nbrs(idx):
        c = colourings[idx]
        nbrs = set()
        for a in palette:
            for b in palette:
                if b <= a:
                    continue
                ab_verts = [v for v in vertices if c[v] in (a, b)]
                visited = set()
                for seed in ab_verts:
                    if seed in visited:
                        continue
                    comp = set()
                    q = deque([seed])
                    while q:
                        x = q.popleft()
                        if x in comp:
                            continue
                        comp.add(x)
                        for y in adj[x]:
                            if y not in comp and c[y] in (a, b):
                                q.append(y)
                    visited |= comp
                    new_c = dict(c)
                    for x in comp:
                        new_c[x] = b if c[x] == a else a
                    assert is_proper(new_c), "BUG: Kempe swap broke colouring"
                    ni = key_to_idx[key_of(new_c)]
                    if ni != idx:
                        nbrs.add(ni)
        return nbrs

    print("\n  Building reconfiguration graph...", end=" ", flush=True)
    R = [kempe_nbrs(i) for i in range(N)]
    print(f"{N} nodes, {sum(len(r) for r in R) // 2} edges")

    # ── 3. BFS: nearest 4-colouring from each 5-colouring ────

    results = []
    for si in starts:
        parent = {si: -1}
        queue = deque([si])
        found = None
        while queue:
            cur = queue.popleft()
            if cur in four_set:
                found = cur
                break
            for nb in R[cur]:
                if nb not in parent:
                    parent[nb] = cur
                    queue.append(nb)

        if found is None:
            results.append((si, None, None, None))
            continue

        d, x = 0, found
        while x != si:
            d += 1
            x = parent[x]

        used = frozenset(colourings[found][v] for v in v_nbrs)
        free = frozenset({1, 2, 3, 4} - used)
        results.append((si, found, d, free))

    # ── 4. Report ─────────────────────────────────────────────

    pass_n = sum(1 for _, _, _, f in results if f)
    fail_n = sum(1 for _, _, _, f in results if f is not None and len(f) == 0)
    unreach = sum(1 for _, ep, _, _ in results if ep is None)

    print(f"\n  ┌─ BFS-nearest results ─────────────────────────┐")
    print(f"  │  ✓ Free colour at endpoint:  {pass_n:>6}           │")
    print(f"  │  ✗ No free colour:           {fail_n:>6}           │")
    print(f"  │  ✗ Unreachable:              {unreach:>6}           │")
    print(f"  └──────────────────────────────────────────────────┘")

    dists = Counter(d for _, _, d, _ in results if d is not None)
    print(f"\n  Kempe-swap distance to nearest 4-colouring:")
    for d in sorted(dists):
        print(f"    d={d}: {dists[d]}")

    def fmt(ci):
        return [colourings[ci][v] for v in vertices]

    def fmt_nbrs(ci):
        return [colourings[ci][v] for v in v_nbrs]

    print(f"\n  Sample passes (up to 5):")
    shown = 0
    for si, ei, d, free in results:
        if free and shown < 5:
            print(f"    start={fmt(si)}  end={fmt(ei)}  d={d}")
            print(f"      v-nbrs={fmt_nbrs(ei)}  free={sorted(free)}")
            shown += 1

    if fail_n > 0:
        print(f"\n  FAILURES (up to 10):")
        shown = 0
        for si, ei, d, free in results:
            if free is not None and len(free) == 0 and shown < 10:
                print(f"    start={fmt(si)}  end={fmt(ei)}  d={d}")
                print(f"      v-nbrs={fmt_nbrs(ei)}  ALL 4 COLOURS USED")
                shown += 1

    # ── 5. Connected-component check (existential claim) ─────

    comp_id = [-1] * N
    num_comp = 0
    for i in range(N):
        if comp_id[i] >= 0:
            continue
        queue = deque([i])
        comp_id[i] = num_comp
        while queue:
            x = queue.popleft()
            for nb in R[x]:
                if comp_id[nb] < 0:
                    comp_id[nb] = num_comp
                    queue.append(nb)
        num_comp += 1

    comp_has_good = [False] * num_comp
    for i in four_set:
        if len({colourings[i][v] for v in v_nbrs}) < 4:
            comp_has_good[comp_id[i]] = True

    exist_pass = sum(1 for si in starts if comp_has_good[comp_id[si]])
    exist_fail = len(starts) - exist_pass

    print(f"\n  Existential MTL (ANY reachable good 4-colouring):")
    print(f"    ✓ Pass: {exist_pass}   ✗ Fail: {exist_fail}")
    print(f"    Connected components in reconfiguration graph: {num_comp}")

    # ── Verdict ───────────────────────────────────────────────

    print(f"\n  {'─' * 52}")
    if fail_n == 0 and unreach == 0:
        print(f"  MTL (nearest):     PASSED")
    else:
        print(f"  MTL (nearest):     FAILED  "
              f"({fail_n + unreach}/{len(starts)})")
    if exist_fail == 0:
        print(f"  MTL (existential): PASSED")
    else:
        print(f"  MTL (existential): FAILED  "
              f"({exist_fail}/{len(starts)})")
    print(f"  {'─' * 52}")

    return pass_n, fail_n, unreach, exist_pass, exist_fail


# ══════════════════════════════════════════════════════════════
# Graph A: Pentagonal bipyramid (7 vertices total, v = 0)
#
#   v = 0, degree 5, connected to {1,2,3,4,5}
#   Vertex 6 connected to all of {1,2,3,4,5}  (antipodal hub)
#   G-v = wheel W_5:  hub 6, rim 1-2-3-4-5-1
#
#   V=7  E=15  F=10  →  V-E+F = 2  ✓
#   Expected: trivially passes (vertex 6 forces ≤ 3 colours on rim)
# ══════════════════════════════════════════════════════════════

test_graph(
    "Graph A: Pentagonal bipyramid — sanity check",
    vertices=(1, 2, 3, 4, 5, 6),
    edges=(
        (1, 2), (2, 3), (3, 4), (4, 5), (5, 1),
        (6, 1), (6, 2), (6, 3), (6, 4), (6, 5),
    ),
    v_nbrs=(1, 2, 3, 4, 5),
)


# ══════════════════════════════════════════════════════════════
# Graph B: 8-vertex triangulation  (v = 0)
#
#   v = 0, degree 5, connected to {1,2,3,4,5}
#   Pentagon 1-2-3-4-5-1 with chord 1-3
#   Vertex 6 triangulates face 1-2-3  (edges 6-1, 6-2, 6-3)
#   Vertex 7 triangulates quad 1-3-4-5 (edges 7-1, 7-3, 7-4, 7-5)
#
#   V=8  E=18  F=12  →  V-E+F = 2  ✓
#   Some 4-colourings of G-v put all 4 colours on v's neighbours.
#   Example: 1→1, 2→2, 3→4, 4→1, 5→3, 6→3, 7→2 → nbrs={1,2,3,4}
# ══════════════════════════════════════════════════════════════

test_graph(
    "Graph B: 8-vertex triangulation — real test",
    vertices=(1, 2, 3, 4, 5, 6, 7),
    edges=(
        (1, 2), (2, 3), (3, 4), (4, 5), (5, 1),
        (1, 3),
        (6, 1), (6, 2), (6, 3),
        (7, 1), (7, 3), (7, 4), (7, 5),
    ),
    v_nbrs=(1, 2, 3, 4, 5),
)
