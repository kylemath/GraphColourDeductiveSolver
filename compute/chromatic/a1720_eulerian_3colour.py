"""Exact 3-colouring check for Eulerian plane triangulations (Agent 1720, A3).

Statement under test: a simple plane triangulation is 3-vertex-colourable if and
only if every vertex degree is even.

For every graph ``graphs[str(n)][i]`` in ``compute/data/triangulations_n4_11.json``
the script

* computes the degree sequence;
* searches for a proper vertex colouring with colours ``{0,1,2}`` by exhaustive
  backtracking (the first vertex in the search order is fixed at colour 0, which
  is legitimate because the colours may be permuted);
* does not treat degree parity as a reason to skip the search;
* on each all-even graph, also builds the colouring from the proof: 2-colour the
  faces of a planar embedding, orient each edge with the black face on the left,
  and propagate colour by ``+1`` in ``Z/3Z`` along oriented edges.

Stored values ``P3`` in ``compute/data/chromatic_polys_n4_11.json`` are read as an
independent check. That file is not written.

Usage::

    /Users/fulkanjou/GraphColour/.venv/bin/python compute/chromatic/a1720_eulerian_3colour.py

Output: ``backgroundMaterial/agent1720/groups/A3_results.json``.
"""

from __future__ import annotations

import json
import time
from collections import defaultdict, deque
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import networkx as nx

ROOT = Path(__file__).resolve().parents[2]
TRI_PATH = ROOT / "compute" / "data" / "triangulations_n4_11.json"
POLY_PATH = ROOT / "compute" / "data" / "chromatic_polys_n4_11.json"
OUT_PATH = (
    ROOT / "backgroundMaterial" / "agent1720" / "groups" / "A3_results.json"
)

Edge = Sequence[int]


def degrees(n: int, edges: Sequence[Edge]) -> List[int]:
    """Return the degree of each vertex ``0 .. n-1``."""
    deg = [0] * n
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1
    return deg


def adjacency(n: int, edges: Sequence[Edge]) -> List[int]:
    """Return ``adj[v]`` as a bitmask of the neighbours of ``v``."""
    adj = [0] * n
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    return adj


def three_colour(
    n: int, adj: Sequence[int]
) -> Tuple[Optional[List[int]], int]:
    """Exact search for a proper colouring with colours ``0, 1, 2``.

    Returns ``(colouring or None, number of search nodes)``. The vertex of
    largest degree is coloured ``0`` and never recoloured.
    """
    order = sorted(range(n), key=lambda v: -bin(adj[v]).count("1"))
    col = [-1] * n
    nodes = 0

    def rec(i: int) -> bool:
        nonlocal nodes
        nodes += 1
        if i == n:
            return True
        v = order[i]
        used = 0
        mask = adj[v]
        while mask:
            bit = mask & -mask
            u = bit.bit_length() - 1
            c = col[u]
            if c != -1:
                used |= 1 << c
            mask ^= bit
        for c in (0, 1, 2):
            if (used >> c) & 1:
                continue
            col[v] = c
            if rec(i + 1):
                return True
        col[v] = -1
        return False

    col[order[0]] = 0
    if rec(1):
        return col, nodes
    return None, nodes


def colouring_is_proper(n: int, edges: Sequence[Edge], col: Sequence[int]) -> bool:
    """True when ``col`` uses ``{0,1,2}`` on every vertex and differs on every edge."""
    if len(col) != n or any(c not in (0, 1, 2) for c in col):
        return False
    return all(col[u] != col[v] for u, v in edges)


def constructive_colouring(
    n: int, edges: Sequence[Edge]
) -> Tuple[str, Optional[List[int]]]:
    """Build the ``Z/3Z`` colouring from a 2-face-colouring, or return an error tag.

    Faces are traced so that the face lies on the right of the directed walk
    (NetworkX ``PlanarEmbedding.traverse_face``). Black is colour ``0``. Each
    edge is oriented with the black face on the left, and the head is one more
    than the tail in ``Z/3Z``.
    """
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    graph.add_edges_from((int(u), int(v)) for u, v in edges)
    planar, emb = nx.check_planarity(graph)
    if not planar:
        return "not planar", None

    marked: set = set()
    faces: List[List[int]] = []
    for v in emb.nodes:
        for w in emb.neighbors_cw_order(v):
            if (v, w) in marked:
                continue
            faces.append(list(emb.traverse_face(v, w, marked)))
    if any(len(face) != 3 for face in faces):
        return "non-triangular face", None

    edge_faces: Dict[Tuple[int, int], List[Tuple[int, int, int]]] = defaultdict(list)
    for fi, face in enumerate(faces):
        for i in range(3):
            a = face[i]
            b = face[(i + 1) % 3]
            key = (a, b) if a < b else (b, a)
            edge_faces[key].append((fi, a, b))
    if any(len(lst) != 2 for lst in edge_faces.values()):
        return "edge not on two faces", None

    dual: Dict[int, set] = defaultdict(set)
    for lst in edge_faces.values():
        f0, f1 = lst[0][0], lst[1][0]
        dual[f0].add(f1)
        dual[f1].add(f0)
    face_colour = [-1] * len(faces)
    face_colour[0] = 0
    queue: deque = deque([0])
    while queue:
        f = queue.popleft()
        for g in dual[f]:
            if face_colour[g] == -1:
                face_colour[g] = 1 - face_colour[f]
                queue.append(g)
            elif face_colour[g] == face_colour[f]:
                return "dual not bipartite", None
    if any(c < 0 for c in face_colour):
        return "face uncoloured", None

    oriented: Dict[Tuple[int, int], Tuple[int, int]] = {}
    for key, lst in edge_faces.items():
        directions = []
        for fi, a, b in lst:
            if face_colour[fi] == 0:
                directions.append((b, a))
            else:
                directions.append((a, b))
        if directions[0] != directions[1]:
            return "orientation conflict", None
        oriented[key] = directions[0]

    delta: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
    for tail, head in oriented.values():
        delta[tail].append((head, 1))
        delta[head].append((tail, -1))

    colour: List[Optional[int]] = [None] * n
    colour[0] = 0
    queue = deque([0])
    while queue:
        u = queue.popleft()
        for v, step in delta[u]:
            want = (colour[u] + step) % 3
            if colour[v] is None:
                colour[v] = want
                queue.append(v)
            elif colour[v] != want:
                return "colour conflict", None
    if any(c is None for c in colour):
        return "not all vertices coloured", None
    out = [int(c) for c in colour]
    if not colouring_is_proper(n, edges, out):
        return "not proper", out
    return "ok", out


def is_simple(n: int, edges: Sequence[Edge]) -> bool:
    """No loops and no repeated undirected edges; endpoints lie in ``0 .. n-1``."""
    seen = set()
    for u, v in edges:
        if u == v or not (0 <= u < n and 0 <= v < n):
            return False
        key = (u, v) if u < v else (v, u)
        if key in seen:
            return False
        seen.add(key)
    return True


def main() -> None:
    t0 = time.perf_counter()
    graphs = json.loads(TRI_PATH.read_text())["graphs"]
    stored = json.loads(POLY_PATH.read_text())["graphs"]

    # Known anchors: K4 is the unique triangulation on 4 vertices and is not
    # 3-colourable; the octahedral graph is the unique all-degree-4 graph on
    # 6 vertices in this cache.
    k4 = graphs["4"][0]
    k4_col, _ = three_colour(4, adjacency(4, k4))
    if k4_col is not None:
        raise SystemExit("K4 was 3-coloured")
    oct_edges = graphs["6"][1]
    oct_deg = degrees(6, oct_edges)
    if oct_deg != [4, 4, 4, 4, 4, 4]:
        raise SystemExit(f"expected the octahedron at T_6_1, degrees {oct_deg}")

    eulerian: List[dict] = []
    odd_but_coloured: List[dict] = []
    even_but_uncoloured: List[dict] = []
    p3_disagreement: List[dict] = []
    data_faults: List[str] = []
    by_n: Dict[str, dict] = {}
    total_nodes = 0
    total_graphs = 0

    for n_key in sorted(graphs, key=int):
        n = int(n_key)
        records = graphs[n_key]
        even_count = 0
        even_coloured = 0
        odd_coloured = 0
        for i, edges in enumerate(records):
            total_graphs += 1
            name = f"T_{n}_{i}"
            if len(edges) != 3 * n - 6 or not is_simple(n, edges):
                data_faults.append(name)
            deg = degrees(n, edges)
            all_even = all(d % 2 == 0 for d in deg)
            col, nodes = three_colour(n, adjacency(n, edges))
            total_nodes += nodes
            if col is not None and not colouring_is_proper(n, edges, col):
                raise SystemExit(f"improper colouring returned for {name}")
            p3 = int(stored[n_key][i]["P3"])
            coloured = col is not None
            if coloured != (p3 > 0):
                p3_disagreement.append(
                    {"name": name, "backtracker": coloured, "P3": p3}
                )
            if all_even:
                even_count += 1
                status, built = constructive_colouring(n, edges)
                proper_built = built is not None and colouring_is_proper(n, edges, built)
                entry = {
                    "name": name,
                    "n": n,
                    "index": i,
                    "degrees": deg,
                    "backtracker_colouring": col,
                    "constructive_status": status,
                    "constructive_colouring": built,
                    "constructive_proper": proper_built,
                    "P3": p3,
                }
                eulerian.append(entry)
                if coloured and proper_built:
                    even_coloured += 1
                else:
                    even_but_uncoloured.append(entry)
            elif coloured:
                odd_coloured += 1
                odd_but_coloured.append(
                    {
                        "name": name,
                        "n": n,
                        "index": i,
                        "degrees": deg,
                        "backtracker_colouring": col,
                        "P3": p3,
                    }
                )
        by_n[n_key] = {
            "graphs": len(records),
            "all_degrees_even": even_count,
            "even_and_3colourable": even_coloured,
            "odd_degree_and_3colourable": odd_coloured,
        }

    elapsed = time.perf_counter() - t0
    if data_faults or p3_disagreement or odd_but_coloured or even_but_uncoloured:
        verdict = "disagreement"
    else:
        verdict = "agree"

    payload = {
        "group": "A3",
        "statement": (
            "A simple plane triangulation is 3-vertex-colourable if and only if "
            "every vertex degree is even."
        ),
        "checker": (
            "Exhaustive backtracking in three_colour; colours {0,1,2}; "
            "first search vertex fixed at 0. Degree parity is not a prune. "
            "constructive_colouring implements the Z/3Z orientation on all-even graphs."
        ),
        "graphs_checked": total_graphs,
        "backtrack_nodes": total_nodes,
        "elapsed_seconds": round(elapsed, 6),
        "verdict": verdict,
        "by_n": by_n,
        "eulerian": eulerian,
        "odd_degree_but_3colourable": odd_but_coloured,
        "even_degree_but_not_3colourable": even_but_uncoloured,
        "disagreement_with_stored_P3": p3_disagreement,
        "data_faults": data_faults,
        "anchors": {"K4_not_3colourable": True, "T_6_1_all_degrees_4": True},
    }
    OUT_PATH.write_text(json.dumps(payload, indent=2) + "\n")
    print(
        f"graphs {total_graphs} eulerian {len(eulerian)} "
        f"odd_but_coloured {len(odd_but_coloured)} "
        f"even_uncoloured {len(even_but_uncoloured)} "
        f"p3_disagree {len(p3_disagreement)} "
        f"nodes {total_nodes} seconds {elapsed:.4f} verdict {verdict}"
    )


if __name__ == "__main__":
    main()
