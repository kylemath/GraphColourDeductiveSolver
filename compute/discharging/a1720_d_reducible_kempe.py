"""D-reducibility by the RSST ring-colour closure.

A free completion is D-reducible when the maximal consistent set of bad
ring edge-colourings is empty. Colours lie in ``{-1,0,1}``. A signed
non-crossing matching is the Kempe interchange on the ring: for a colour
``θ``, the edges not coloured ``θ`` are paired, and every ring colouring
that fits the same signed matching is kept or lost together. This is the
test in Robertson, Sanders, Seymour, and Thomas, J. Combin. Theory Ser. B
70 (1997), §3. It is not the extension count in ``a1720_d_reducibility.py``,
which uses no Kempe interchange.
"""

from __future__ import annotations

import json
import time
from collections import defaultdict, deque
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

COLOURS: Tuple[int, ...] = (-1, 0, 1)
# Nonzero elements of Z_2 x Z_2, written 1=(1,0), 2=(0,1), 3=(1,1).
XOR_TO_EDGE: Dict[int, int] = {1: -1, 2: 1, 3: 0}
Edge = Tuple[int, int]
Tri = Tuple[int, int, int]
RingColouring = Tuple[int, ...]
SignedPair = Tuple[int, int, int]

ROOT = Path(__file__).resolve().parents[2]
OUT_PATH = ROOT / "backgroundMaterial" / "agent1720" / "groups" / "S3b_results.json"


def _norm(u: int, v: int) -> Edge:
    return (u, v) if u < v else (v, u)


def ring_cycle_edges(ring_size: int) -> List[Edge]:
    return [_norm(i, (i + 1) % ring_size) for i in range(ring_size)]


def chromatic_cycle_count(n: int, k: int = 4) -> int:
    """Proper k-colourings of C_n on a fixed set of k colours."""
    return (k - 1) ** n + (-1) ** n * (k - 1)


def catalan(m: int) -> int:
    """The m-th Catalan number, counting non-crossing matchings of 2m points."""
    if m < 0:
        raise ValueError(m)
    value = 1
    for i in range(m):
        value = value * (2 * m - i) // (i + 1)
    return value // (m + 1)


@lru_cache(maxsize=None)
def noncrossing_matchings(positions: Tuple[int, ...]) -> Tuple[Tuple[Edge, ...], ...]:
    """Non-crossing perfect matchings of points in cyclic order.

    The number on ``2m`` consecutive points is the Catalan number ``C_m``.
    """
    if not positions:
        return ((),)
    if len(positions) % 2:
        return ()
    first = positions[0]
    found: List[Tuple[Edge, ...]] = []
    for j in range(1, len(positions), 2):
        partner = positions[j]
        pair = (first, partner) if first < partner else (partner, first)
        inside = noncrossing_matchings(positions[1:j])
        outside = noncrossing_matchings(positions[j + 1 :])
        for left in inside:
            for right in outside:
                found.append((pair,) + left + right)
    return tuple(found)


def companions(ring_size: int, theta: int, pairs: Sequence[SignedPair]) -> List[RingColouring]:
    """Every ring colouring that ``θ``-fits this signed matching."""
    others = [colour for colour in COLOURS if colour != theta]
    choices: List[Tuple[Tuple[int, int], ...]] = []
    for _i, _j, sign in pairs:
        if sign == 1:
            choices.append(((others[0], others[0]), (others[1], others[1])))
        elif sign == -1:
            choices.append(((others[0], others[1]), (others[1], others[0])))
        else:
            raise ValueError(f"sign {sign}")
    colourings: List[RingColouring] = []
    for choice in product(*choices) if choices else ((),):
        colouring = [theta] * ring_size
        for (i, j, _sign), (left, right) in zip(pairs, choice):
            colouring[i] = left
            colouring[j] = right
        colourings.append(tuple(colouring))
    return colourings


def has_witness(colouring: RingColouring, theta: int, live: set[RingColouring]) -> bool:
    """True when some signed matching ``θ``-fits ``colouring`` and stays inside ``live``."""
    support = tuple(i for i, colour in enumerate(colouring) if colour != theta)
    for matching in noncrossing_matchings(support):
        pairs = tuple(
            (i, j, 1 if colouring[i] == colouring[j] else -1) for i, j in matching
        )
        if all(other in live for other in companions(len(colouring), theta, pairs)):
            return True
    return False


def maximal_consistent_subset(bad: Iterable[RingColouring]) -> List[RingColouring]:
    """Unique maximal consistent subset. Deleting a colouring cannot revive one."""
    live = set(bad)
    while True:
        kept = {
            colouring
            for colouring in live
            if all(has_witness(colouring, theta, live) for theta in COLOURS)
        }
        if kept == live:
            return sorted(live)
        live = kept


def adjacency(vertex_count: int, edges: Sequence[Edge]) -> List[List[int]]:
    adj: List[List[int]] = [[] for _ in range(vertex_count)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def survey_colourings(
    ring_size: int, interior: Sequence[int], edges: Sequence[Edge]
) -> Dict[str, object]:
    """Vertex-extension counts and the set of extendable ring edge-colourings.

    Vertex colours are ``Z_2 x Z_2``. The colour of a ring edge is the nonzero
    sum of its ends, renamed by ``XOR_TO_EDGE``.
    """
    vertices = ring_size + len(interior)
    adj = adjacency(vertices, edges)
    colour = [-1] * vertices
    extendable_edges: set[RingColouring] = set()
    ring_seen: set[RingColouring] = set()
    ring_extend: set[RingColouring] = set()
    full_colourings = 0

    def edge_key() -> RingColouring:
        return tuple(
            XOR_TO_EDGE[colour[i] ^ colour[(i + 1) % ring_size]]
            for i in range(ring_size)
        )

    def walk(index: int) -> None:
        nonlocal full_colourings
        if index == vertices:
            full_colourings += 1
            extendable_edges.add(edge_key())
            ring_extend.add(tuple(colour[:ring_size]))
            return
        if index == ring_size:
            ring_seen.add(tuple(colour[:ring_size]))
        for bit in range(4):
            if any(colour[nbr] == bit for nbr in adj[index] if nbr < index):
                continue
            colour[index] = bit
            walk(index + 1)
            colour[index] = -1

    walk(0)
    return {
        "vertex_ring_colourings": len(ring_seen),
        "vertex_direct_extensions": len(ring_extend),
        "full_vertex_colourings": full_colourings,
        "extendable_edge_colourings": extendable_edges,
    }


def analyse(
    ring_size: int, interior: Sequence[int], edges: Sequence[Edge]
) -> Dict[str, object]:
    """Consistent-set D-reducibility for one free completion."""
    if ring_size > 6:
        raise ValueError(f"ring size {ring_size} exceeds 6")
    surveyed = survey_colourings(ring_size, interior, edges)
    extendable: set[RingColouring] = surveyed["extendable_edge_colourings"]  # type: ignore[assignment]
    universe = list(product(COLOURS, repeat=ring_size))
    if len(universe) != 3 ** ring_size:
        raise RuntimeError("edge-colouring universe")
    bad = [colouring for colouring in universe if colouring not in extendable]
    consistent = maximal_consistent_subset(bad)
    return {
        "ring_size": ring_size,
        "interior": list(interior),
        "edge_colourings": len(universe),
        "extendable_edge_colourings": len(extendable),
        "bad_edge_colourings": len(bad),
        "maximal_consistent_bad": len(consistent),
        "bad_examples": [list(colouring) for colouring in consistent[:5]],
        "consistent_bad_colourings": [list(colouring) for colouring in consistent],
        "d_reducible": len(consistent) == 0,
        "vertex_ring_colourings": surveyed["vertex_ring_colourings"],
        "vertex_direct_extensions": surveyed["vertex_direct_extensions"],
        "vertex_direct_failures": (
            surveyed["vertex_ring_colourings"] - surveyed["vertex_direct_extensions"]
        ),
        "full_vertex_colourings": surveyed["full_vertex_colourings"],
    }


def degrees(vertices: Iterable[int], edges: Sequence[Edge]) -> Dict[int, int]:
    deg: Dict[int, int] = {v: 0 for v in vertices}
    for u, v in edges:
        deg[u] = deg.get(u, 0) + 1
        deg[v] = deg.get(v, 0) + 1
    return deg


def incidence_is_disk(
    ring_size: int, edges: Sequence[Edge], triangles: Sequence[Tri]
) -> bool:
    """Each cycle edge lies in one triangle, every other edge in two, dual connected."""
    edge_set = {_norm(u, v) for u, v in edges}
    cycle = set(ring_cycle_edges(ring_size))
    count: Dict[Edge, int] = defaultdict(int)
    for a, b, c in triangles:
        for edge in (_norm(a, b), _norm(b, c), _norm(c, a)):
            if edge not in edge_set:
                return False
            count[edge] += 1
    if set(count) != edge_set:
        return False
    for edge, used in count.items():
        if used != (1 if edge in cycle else 2):
            return False
    buckets: Dict[Edge, List[int]] = defaultdict(list)
    for i, (a, b, c) in enumerate(triangles):
        for edge in (_norm(a, b), _norm(b, c), _norm(c, a)):
            buckets[edge].append(i)
    seen = {0}
    stack = [0]
    while stack:
        i = stack.pop()
        a, b, c = triangles[i]
        for edge in (_norm(a, b), _norm(b, c), _norm(c, a)):
            for j in buckets[edge]:
                if j not in seen:
                    seen.add(j)
                    stack.append(j)
    return len(seen) == len(triangles)


def birkhoff_diamond() -> Tuple[int, List[int], List[Edge], List[Tri]]:
    """Chordless disk: ring 6, four interior vertices of degree 5, caps (2,1,2,1)."""
    ring = 6
    interior = [6, 7, 8, 9]
    edges = ring_cycle_edges(ring) + [
        (0, 6), (1, 6), (2, 6),
        (2, 7), (3, 7),
        (3, 8), (4, 8), (5, 8),
        (5, 9), (0, 9),
        (6, 7), (7, 8), (8, 9), (9, 6), (7, 9),
    ]
    triangles: List[Tri] = [
        (0, 1, 6), (1, 2, 6), (2, 6, 7), (2, 3, 7),
        (3, 7, 8), (3, 4, 8), (4, 5, 8), (5, 8, 9),
        (5, 0, 9), (0, 9, 6), (6, 7, 9), (7, 8, 9),
    ]
    return ring, interior, edges, triangles


def wheel(ring_size: int) -> Tuple[int, List[int], List[Edge]]:
    """One interior hub joined to every vertex of the ring."""
    interior = [ring_size]
    edges = ring_cycle_edges(ring_size) + [(ring_size, i) for i in range(ring_size)]
    return ring_size, interior, edges


def component_swap_closure_failures(
    ring_size: int, interior: Sequence[int], edges: Sequence[Edge]
) -> int:
    """Failures of the free bichromatic-component graph on the ring.

    That graph is not the RSST consistent-set test. Isolated vertices are
    components, so the closure can accept a configuration the signed-matching
    test rejects.
    """
    ring_adj: List[List[int]] = [[] for _ in range(ring_size)]
    for u, v in edges:
        if u < ring_size and v < ring_size:
            ring_adj[u].append(v)
            ring_adj[v].append(u)
    colourings = [
        assign
        for assign in product(range(4), repeat=ring_size)
        if all(assign[i] != assign[(i + 1) % ring_size] for i in range(ring_size))
        and all(
            assign[u] != assign[v]
            for u, v in edges
            if u < ring_size and v < ring_size
        )
    ]
    adj_lists, interior_edges = _component_extension_index(ring_size, interior, edges)
    extendable = [
        _extends_vertex(assign, adj_lists, interior_edges) for assign in colourings
    ]
    index = {colouring: i for i, colouring in enumerate(colourings)}
    reachable = list(extendable)
    queue: deque[int] = deque(i for i, ok in enumerate(extendable) if ok)

    def neighbours(colouring: RingColouring) -> List[RingColouring]:
        found: List[RingColouring] = []
        seen: set[RingColouring] = set()
        for a, b in combinations(range(4), 2):
            visited: set[int] = set()
            for start in range(ring_size):
                if start in visited or colouring[start] not in (a, b):
                    continue
                stack = [start]
                visited.add(start)
                component: List[int] = []
                while stack:
                    vertex = stack.pop()
                    component.append(vertex)
                    for nbr in ring_adj[vertex]:
                        if nbr not in visited and colouring[nbr] in (a, b):
                            visited.add(nbr)
                            stack.append(nbr)
                swapped = list(colouring)
                for vertex in component:
                    swapped[vertex] = b if colouring[vertex] == a else a
                key = tuple(swapped)
                if key != colouring and key not in seen:
                    seen.add(key)
                    found.append(key)
        return found

    while queue:
        current = queue.popleft()
        for nbr in neighbours(colourings[current]):
            j = index[nbr]
            if not reachable[j]:
                reachable[j] = True
                queue.append(j)
    return sum(1 for ok in reachable if not ok)


def _component_extension_index(
    ring_size: int, interior: Sequence[int], edges: Sequence[Edge]
) -> Tuple[List[List[int]], List[Edge]]:
    rank = {vertex: i for i, vertex in enumerate(interior)}
    adj: List[List[int]] = [[] for _ in interior]
    interior_edges: List[Edge] = []
    interior_set = set(interior)
    for u, v in edges:
        if u in interior_set and v in interior_set:
            interior_edges.append((rank[u], rank[v]))
            adj[rank[u]].append(v)
            adj[rank[v]].append(u)
        elif u in interior_set and v < ring_size:
            adj[rank[u]].append(v)
        elif v in interior_set and u < ring_size:
            adj[rank[v]].append(u)
    return adj, interior_edges


def _extends_vertex(
    colouring: RingColouring,
    adj_interior: Sequence[Sequence[int]],
    interior_edges: Sequence[Edge],
) -> bool:
    assignment = [-1] * len(adj_interior)

    def place(i: int) -> bool:
        if i == len(adj_interior):
            return all(assignment[u] != assignment[v] for u, v in interior_edges)
        used = {colouring[n] for n in adj_interior[i] if n < len(colouring)}
        used.update(
            assignment[n - len(colouring)]
            for n in adj_interior[i]
            if n >= len(colouring) and assignment[n - len(colouring)] >= 0
        )
        for colour in range(4):
            if colour in used:
                continue
            assignment[i] = colour
            if place(i + 1):
                return True
            assignment[i] = -1
        return False

    return place(0)


def canonical_vertex_orbits(ring_size: int) -> int:
    """Proper vertex 4-colourings of C_n, up to permuting the four colours."""
    orbits = set()
    for assign in product(range(4), repeat=ring_size):
        if any(assign[i] == assign[(i + 1) % ring_size] for i in range(ring_size)):
            continue
        rename: Dict[int, int] = {}
        orbits.add(tuple(rename.setdefault(colour, len(rename)) for colour in assign))
    return len(orbits)


def check_catalan() -> None:
    expected = (1, 1, 2, 5, 14)
    for m, count in enumerate(expected):
        positions = tuple(range(2 * m))
        got = len(noncrossing_matchings(positions))
        if got != count or got != catalan(m):
            raise SystemExit(f"Catalan C_{m}: generator {got}, formula {catalan(m)}")


def main() -> None:
    started = time.perf_counter()
    check_catalan()
    for n, expect in ((4, 84), (5, 240), (6, 732)):
        if chromatic_cycle_count(n) != expect:
            raise SystemExit(f"C{n} chromatic count")

    ring, interior, edges, triangles = birkhoff_diamond()
    deg = degrees(list(range(10)), edges)
    if not incidence_is_disk(ring, edges, triangles):
        raise SystemExit("Birkhoff diamond is not a triangulated disk")
    if any(deg[v] != 5 for v in interior) or len(edges) != 21 or len(triangles) != 12:
        raise SystemExit("Birkhoff diamond failed the degree certificate")

    diamond = analyse(ring, interior, edges)
    diamond["interior_degrees"] = {str(v): deg[v] for v in interior}
    diamond["edge_count"] = len(edges)
    diamond["internal_triangles"] = len(triangles)
    diamond["disk_triangulation"] = True
    diamond["vertex_ring_colourings_up_to_colour_permutation"] = canonical_vertex_orbits(6)

    r5, int5, e5 = wheel(5)
    degree5 = analyse(r5, int5, e5)
    degree5["interior_degrees"] = {"5": 5}
    degree5["vertex_ring_colourings_up_to_colour_permutation"] = canonical_vertex_orbits(5)
    witness = (-1, -1, 0, -1, 1)
    degree5["named_witness_in_consistent_bad_set"] = list(witness) in degree5[
        "consistent_bad_colourings"
    ]

    # Degree-4 wheel: same test, used only as a checksum against the known empty bad set.
    r4, int4, e4 = wheel(4)
    degree4 = analyse(r4, int4, e4)
    naive = {
        "birkhoff_diamond_failures": component_swap_closure_failures(ring, interior, edges),
        "degree5_failures": component_swap_closure_failures(r5, int5, e5),
        "note": (
            "Free swaps of every bichromatic ring component, including isolated "
            "vertices. Not the D-reducibility test."
        ),
    }

    elapsed = time.perf_counter() - started
    payload = {
        "definition": (
            "D-reducible means the maximal consistent set of bad ring "
            "edge-colourings in {-1,0,1} is empty. A signed non-crossing "
            "matching is a Kempe interchange on the ring: for each colour "
            "theta, every proper 4-colouring of the ring, up to translation "
            "in the Klein group, is kept with the colourings that fit the "
            "same matching. This is the RSST ring-colour closure."
        ),
        "literature": (
            "Robertson, Sanders, Seymour, Thomas, The Four-Colour Theorem, "
            "J. Combin. Theory Ser. B 70 (1997), 2-44, section 3."
        ),
        "ring_size_bound": 6,
        "elapsed_seconds": round(elapsed, 4),
        "cycle_colouring_counts": {
            "C4_vertex": chromatic_cycle_count(4),
            "C5_vertex": chromatic_cycle_count(5),
            "C6_vertex": chromatic_cycle_count(6),
            "C5_vertex_up_to_colour_permutation": canonical_vertex_orbits(5),
            "C6_vertex_up_to_colour_permutation": canonical_vertex_orbits(6),
            "C5_edge": 3 ** 5,
            "C6_edge": 3 ** 6,
        },
        "birkhoff_diamond": diamond,
        "degree5_vertex": degree5,
        "naive_component_swap_not_the_test": naive,
        "degree4_checksum": {
            "edge_colourings": degree4["edge_colourings"],
            "extendable_edge_colourings": degree4["extendable_edge_colourings"],
            "maximal_consistent_bad": degree4["maximal_consistent_bad"],
            "d_reducible": degree4["d_reducible"],
            "vertex_ring_colourings": degree4["vertex_ring_colourings"],
            "vertex_direct_failures": degree4["vertex_direct_failures"],
        },
        "claims": {
            "birkhoff_diamond_d_reducible": diamond["d_reducible"],
            "degree5_vertex_d_reducible": degree5["d_reducible"],
            "degree5_consistent_bad": degree5["maximal_consistent_bad"],
            "diamond_extendable_edge_colourings": diamond["extendable_edge_colourings"],
        },
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "elapsed_seconds": payload["elapsed_seconds"],
        "diamond": {
            "edge_colourings": diamond["edge_colourings"],
            "extendable": diamond["extendable_edge_colourings"],
            "consistent_bad": diamond["maximal_consistent_bad"],
            "vertex_ring": diamond["vertex_ring_colourings"],
            "vertex_fail": diamond["vertex_direct_failures"],
            "d_reducible": diamond["d_reducible"],
        },
        "degree5": {
            "edge_colourings": degree5["edge_colourings"],
            "extendable": degree5["extendable_edge_colourings"],
            "consistent_bad": degree5["maximal_consistent_bad"],
            "vertex_ring": degree5["vertex_ring_colourings"],
            "vertex_fail": degree5["vertex_direct_failures"],
            "witness": degree5["named_witness_in_consistent_bad_set"],
            "examples": degree5["bad_examples"][:3],
            "d_reducible": degree5["d_reducible"],
        },
        "degree4": payload["degree4_checksum"],
        "out": str(OUT_PATH),
    }, indent=2))

    if diamond["extendable_edge_colourings"] != 96 or diamond["d_reducible"] is not True:
        raise SystemExit("Birkhoff diamond failed the RSST count")
    if diamond["vertex_direct_failures"] != 348 or diamond["vertex_ring_colourings"] != 732:
        raise SystemExit("diamond vertex counts")
    if (
        degree5["extendable_edge_colourings"] != 30
        or degree5["maximal_consistent_bad"] != 30
        or degree5["d_reducible"] is not False
    ):
        raise SystemExit("degree-5 vertex failed the RSST count")
    if degree5["vertex_ring_colourings"] != 240 or degree5["vertex_direct_failures"] != 120:
        raise SystemExit("degree-5 vertex counts")
    if degree4["d_reducible"] is not True or degree4["extendable_edge_colourings"] != 15:
        raise SystemExit("degree-4 checksum failed")
    if degree4["vertex_direct_failures"] != 24:
        raise SystemExit("degree-4 vertex failure count")
    if naive["birkhoff_diamond_failures"] != 0 or naive["degree5_failures"] != 0:
        raise SystemExit(f"naive component-swap counts changed: {naive}")


if __name__ == "__main__":
    main()
