"""D-reducibility for a free completion whose ring has size at most 6.

The test is the one in Robertson, Sanders, Seymour, and Thomas, *The
Four-Colour Theorem*, J. Combin. Theory Ser. B 70 (1997), section 3.
It is not the ring-Kempe search in ``reducibility_checker.py``.

A near-triangulation S (the free completion) has ring vertices
``0 .. ring_size-1`` in cyclic order and the given interior vertices.
Edge-colours are ``{-1, 0, 1}``. A tri-colouring is an assignment of
those colours to the edges such that every finite triangular face
receives all three; equivalently, the edge-colours are the nonzero
differences of a proper vertex 4-colouring, with vertex colours the
Klein group ``Z2 x Z2``.

Let C* be every map from the ring edges to ``{-1, 0, 1}``. Let C be
the set of restrictions to the ring of tri-colourings of S. Let C' be
the maximal consistent subset of C* \\ C, in the sense of RSST
(signed non-crossing matchings). S is D-reducible when C' is empty.
"""

from __future__ import annotations

import json
import time
from collections import defaultdict
from itertools import product
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Sequence, Set, Tuple

Edge = Tuple[int, int]
Tri = Tuple[int, int, int]
Colouring = Tuple[int, ...]

THETA: Tuple[int, ...] = (-1, 0, 1)
# Nonzero elements of Z2 x Z2, written as integers 1, 2, 3 = 01, 10, 11,
# sent bijectively to the RSST edge-colours.
XOR_TO_EDGE = {1: -1, 2: 0, 3: 1}

ROOT = Path(__file__).resolve().parents[2]
OUT_PATH = ROOT / "backgroundMaterial" / "agent1720" / "groups" / "S3_results.json"


def _norm(u: int, v: int) -> Edge:
    return (u, v) if u < v else (v, u)


def ring_cycle_edges(ring_size: int) -> List[Edge]:
    return [_norm(i, (i + 1) % ring_size) for i in range(ring_size)]


def degrees(vertices: Iterable[int], edges: Sequence[Edge]) -> Dict[int, int]:
    deg: Dict[int, int] = {v: 0 for v in vertices}
    for u, v in edges:
        deg[u] = deg.get(u, 0) + 1
        deg[v] = deg.get(v, 0) + 1
    return deg


def incidence_is_disk(
    ring_size: int, edges: Sequence[Edge], triangles: Sequence[Tri]
) -> bool:
    """Cycle edge in one triangle, every other edge in two, dual connected."""
    edge_set = {_norm(u, v) for u, v in edges}
    cycle = set(ring_cycle_edges(ring_size))
    count: Dict[Edge, int] = defaultdict(int)
    for a, b, c in triangles:
        for e in (_norm(a, b), _norm(b, c), _norm(c, a)):
            if e not in edge_set:
                return False
            count[e] += 1
    if set(count) != edge_set:
        return False
    for edge, used in count.items():
        if used != (1 if edge in cycle else 2):
            return False
    buckets: Dict[Edge, List[int]] = defaultdict(list)
    for i, (a, b, c) in enumerate(triangles):
        for e in (_norm(a, b), _norm(b, c), _norm(c, a)):
            buckets[e].append(i)
    seen = {0}
    stack = [0]
    while stack:
        i = stack.pop()
        a, b, c = triangles[i]
        for e in (_norm(a, b), _norm(b, c), _norm(c, a)):
            for j in buckets[e]:
                if j not in seen:
                    seen.add(j)
                    stack.append(j)
    return len(seen) == len(triangles)


def birkhoff_diamond() -> Tuple[int, List[int], List[Edge], List[Tri]]:
    """Chordless disk triangulation: ring 6, four interior vertices of degree 5.

    Cap lengths around the ring are (2, 1, 2, 1). Vertex 6 caps edges 0-1 and
    1-2; 7 caps 2-3; 8 caps 3-4 and 4-5; 9 caps 5-0. The fifth interior edge
    joins the two cap-1 vertices.
    """
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
    """One interior vertex joined to every vertex of the ring."""
    hub = ring_size
    edges = ring_cycle_edges(ring_size) + [(hub, i) for i in range(ring_size)]
    return ring_size, [hub], edges


def _adjacency(edges: Sequence[Edge]) -> Dict[int, List[int]]:
    adj: Dict[int, List[int]] = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def extendable_ring_edge_colourings(
    ring_size: int, interior: Sequence[int], edges: Sequence[Edge]
) -> Set[Colouring]:
    """Ring edge-colours induced by proper vertex 4-colourings of S.

    Vertex colours are ``0,1,2,3`` as elements of ``Z2 x Z2``. The colour of
    a ring edge is the image of the symmetric difference of its ends.
    """
    if ring_size > 6:
        raise ValueError(f"ring size {ring_size} exceeds 6")
    adj = _adjacency(edges)
    verts = list(range(ring_size)) + list(interior)
    found: Set[Colouring] = set()
    colour: Dict[int, int] = {}

    def search(index: int) -> None:
        if index == len(verts):
            found.add(tuple(
                XOR_TO_EDGE[colour[i] ^ colour[(i + 1) % ring_size]]
                for i in range(ring_size)
            ))
            return
        vertex = verts[index]
        used = {colour[u] for u in adj[vertex] if u in colour}
        for colour_id in range(4):
            if colour_id in used:
                continue
            colour[vertex] = colour_id
            search(index + 1)
            del colour[vertex]

    search(0)
    return found


def noncrossing_pairings(points: Sequence[int]) -> Iterator[List[Tuple[int, int]]]:
    """Non-crossing perfect matchings of points in cyclic order.

    The Catalan recurrence: the first point is joined to an odd-indexed
    partner, and the two intervening arcs are matched separately.
    """
    if not points:
        yield []
        return
    first = points[0]
    for j in range(1, len(points), 2):
        partner = points[j]
        left = points[1:j]
        right = points[j + 1:]
        for left_pairs in noncrossing_pairings(left):
            for right_pairs in noncrossing_pairings(right):
                yield [(first, partner)] + left_pairs + right_pairs


def _fitting_colourings(
    pairs: Sequence[Tuple[int, int]],
    lam: Colouring,
    theta: int,
    ring_size: int,
) -> Iterator[Colouring]:
    """Edge-colourings that theta-fit the signed matching read off ``lam``."""
    others = [c for c in THETA if c != theta]
    options: List[Tuple[int, int, Tuple[Tuple[int, int], Tuple[int, int]]]] = []
    for e, f in pairs:
        same = lam[e] == lam[f]
        if same:
            opts = ((others[0], others[0]), (others[1], others[1]))
        else:
            opts = ((others[0], others[1]), (others[1], others[0]))
        options.append((e, f, opts))

    def rec(index: int, current: List[int]) -> Iterator[Colouring]:
        if index == len(options):
            yield tuple(current)
            return
        e, f, opts = options[index]
        for ce, cf in opts:
            current[e] = ce
            current[f] = cf
            yield from rec(index + 1, current)

    base = [theta] * ring_size
    yield from rec(0, base)


def _some_matching_stays_inside(
    lam: Colouring, alive: Set[Colouring]
) -> bool:
    """Exists a non-crossing pairing whose whole theta-fit class lies in ``alive``."""
    ring_size = len(lam)
    for theta in THETA:
        support = [i for i in range(ring_size) if lam[i] != theta]
        if len(support) % 2 == 1:
            return False
        found = False
        for pairs in noncrossing_pairings(support):
            if all(col in alive for col in _fitting_colourings(pairs, lam, theta, ring_size)):
                found = True
                break
        if not found:
            return False
    return True


def maximal_consistent_subset(bad: Set[Colouring]) -> Set[Colouring]:
    """Maximal consistent subset of ``bad``, by deleting colourings that cannot belong to one."""
    alive = set(bad)
    changed = True
    while changed:
        changed = False
        doomed = [
            lam for lam in alive
            if not _some_matching_stays_inside(lam, alive)
        ]
        if doomed:
            changed = True
            for lam in doomed:
                alive.remove(lam)
    return alive


def direct_vertex_extensions(
    ring_size: int, interior: Sequence[int], edges: Sequence[Edge]
) -> Dict[str, int]:
    """Proper vertex 4-colourings of the ring, and how many extend to S.

    This is not D-reducibility. It is recorded so the two tests are not confused.
    """
    ring_edges = [e for e in edges if e[0] < ring_size and e[1] < ring_size]
    total = 0
    extend = 0
    for assign in product(range(4), repeat=ring_size):
        if any(assign[u] == assign[v] for u, v in ring_edges):
            continue
        total += 1
        colour = {i: assign[i] for i in range(ring_size)}
        if _interior_extends(edges, colour, interior):
            extend += 1
    return {
        "ring_vertex_colourings": total,
        "extend_directly": extend,
        "fail_directly": total - extend,
    }


def _interior_extends(
    edges: Sequence[Edge],
    ring_colouring: Dict[int, int],
    interior: Sequence[int],
) -> bool:
    adj = _adjacency(edges)
    colour = dict(ring_colouring)

    def search(index: int) -> bool:
        if index == len(interior):
            return True
        vertex = interior[index]
        used = {colour[u] for u in adj[vertex] if u in colour}
        for colour_id in range(4):
            if colour_id in used:
                continue
            colour[vertex] = colour_id
            if search(index + 1):
                return True
            del colour[vertex]
        return False

    return search(0)


def d_reducibility(
    ring_size: int,
    interior: Sequence[int],
    edges: Sequence[Edge],
    witness_limit: int = 3,
) -> Dict[str, object]:
    """RSST D-reducibility. Refuses a ring larger than 6."""
    if ring_size > 6:
        raise ValueError(f"ring size {ring_size} exceeds 6")
    if any(v < ring_size for v in interior):
        raise ValueError("interior vertex ids must be >= ring_size")
    extendable = extendable_ring_edge_colourings(ring_size, interior, edges)
    universe = set(product(THETA, repeat=ring_size))
    bad = universe - extendable
    consistent = maximal_consistent_subset(bad)
    witnesses = [list(col) for col in sorted(consistent)[:witness_limit]]
    result: Dict[str, object] = {
        "ring_size": ring_size,
        "interior": list(interior),
        "edge_colourings": len(universe),
        "extend_to_tri_colouring": len(extendable),
        "bad": len(bad),
        "maximal_consistent_bad": len(consistent),
        "consistent_witnesses": witnesses,
        "d_reducible": len(consistent) == 0,
    }
    result.update(direct_vertex_extensions(ring_size, interior, edges))
    return result


def catalan_check() -> None:
    # Non-crossing perfect matchings of 2n points: the Catalan number C_n.
    expected = {0: 1, 2: 1, 4: 2, 6: 5, 8: 14}
    for n, count in expected.items():
        got = sum(1 for _ in noncrossing_pairings(list(range(n))))
        if got != count:
            raise SystemExit(f"non-crossing matchings of {n} points: {got} != {count}")


def main() -> None:
    started = time.perf_counter()
    catalan_check()

    ring, interior, edges, triangles = birkhoff_diamond()
    deg = degrees(list(range(ring)) + interior, edges)
    if not incidence_is_disk(ring, edges, triangles):
        raise SystemExit("Birkhoff diamond is not a triangulated disk")
    if any(deg[v] != 5 for v in interior) or len(edges) != 21:
        raise SystemExit("Birkhoff diamond degree or edge count is wrong")
    diamond = d_reducibility(ring, interior, edges)
    diamond["edges"] = [list(e) for e in edges]
    diamond["interior_degrees"] = {str(v): deg[v] for v in interior}
    diamond["edge_count"] = len(edges)
    diamond["internal_triangles"] = len(triangles)
    diamond["induced_ring"] = True

    wheel5 = d_reducibility(*wheel(5))
    wheel4 = d_reducibility(*wheel(4))

    elapsed = round(time.perf_counter() - started, 4)
    payload = {
        "definition": (
            "RSST 1997, section 3: the free completion is D-reducible when the "
            "maximal consistent subset of the ring edge-colourings that do not "
            "extend to a tri-colouring is empty. Edge-colours are {-1,0,1}."
        ),
        "ring_size_bound": 6,
        "elapsed_seconds": elapsed,
        "birkhoff_diamond": diamond,
        "degree5_vertex": wheel5,
        "degree4_vertex_sanity": wheel4,
        "claims": {
            "birkhoff_diamond_d_reducible": diamond["d_reducible"] is True,
            "degree5_vertex_not_d_reducible": wheel5["d_reducible"] is False,
            "degree4_vertex_d_reducible": wheel4["d_reducible"] is True,
        },
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    summary = {
        "elapsed_seconds": elapsed,
        "diamond": {
            "extend": diamond["extend_to_tri_colouring"],
            "bad": diamond["bad"],
            "consistent_bad": diamond["maximal_consistent_bad"],
            "d_reducible": diamond["d_reducible"],
        },
        "degree5": {
            "extend": wheel5["extend_to_tri_colouring"],
            "bad": wheel5["bad"],
            "consistent_bad": wheel5["maximal_consistent_bad"],
            "witness": wheel5["consistent_witnesses"][:1],
            "d_reducible": wheel5["d_reducible"],
        },
        "degree4": {
            "consistent_bad": wheel4["maximal_consistent_bad"],
            "d_reducible": wheel4["d_reducible"],
        },
    }
    print(json.dumps(summary, indent=2))
    if diamond["d_reducible"] is not True:
        raise SystemExit("Birkhoff diamond was not D-reducible")
    if wheel5["d_reducible"] is not False:
        raise SystemExit("degree-5 vertex was D-reducible")
    if wheel4["d_reducible"] is not True:
        raise SystemExit("degree-4 vertex was not D-reducible")


if __name__ == "__main__":
    main()
