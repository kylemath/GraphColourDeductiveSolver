"""Kill test for one route: plane triangulations and 3-vertex-colouring.

Statement. A simple maximal plane graph on n >= 3 vertices admits a proper
vertex colouring with three colours if and only if every vertex has even degree.

Kill witness. One cached triangulation T_n_i in which those two predicates
disagree.

The cache is compute/data/triangulations_n4_11.json. For each graph the script
1. checks the plantri edge count 3n-6,
2. reads a combinatorial embedding (networkx check_planarity),
3. tests even degrees,
4. decides 3-colourability by exact backtrack and, separately, by Glucose3,
5. if every degree is even, runs the face-sign construction and checks that
   the colouring it returns is proper.

Usage:
    /Users/fulkanjou/GraphColour/.venv/bin/python compute/discovery/a1720_s4b.py
"""

from __future__ import annotations

import json
import time
from collections import deque
from pathlib import Path

import networkx as nx
from pysat.solvers import Glucose3

ROOT = Path(__file__).resolve().parents[2]
TRI = ROOT / "compute" / "data" / "triangulations_n4_11.json"
OUT = ROOT / "backgroundMaterial" / "agent1720" / "groups" / "S4b_results.json"

PLANTRI = {
    "4": 1,
    "5": 1,
    "6": 2,
    "7": 5,
    "8": 14,
    "9": 50,
    "10": 233,
    "11": 1249,
}


def is_proper(n: int, adj: list[list[int]], color: list[int]) -> bool:
    if any(c not in (0, 1, 2) for c in color):
        return False
    for v in range(n):
        for u in adj[v]:
            if u > v and color[u] == color[v]:
                return False
    return True


def sat_three_colourable(n: int, edges: list[list[int]]) -> bool:
    """Independent decision: Glucose3 on the standard 3-colour clauses."""
    solver = Glucose3(use_timer=False)
    try:
        for v in range(n):
            solver.add_clause([3 * v + c + 1 for c in range(3)])
            for c1 in range(3):
                for c2 in range(c1 + 1, 3):
                    solver.add_clause([-(3 * v + c1 + 1), -(3 * v + c2 + 1)])
        for u, v in edges:
            for c in range(3):
                solver.add_clause([-(3 * u + c + 1), -(3 * v + c + 1)])
        return bool(solver.solve())
    finally:
        solver.delete()


def three_colouring(n: int, adj: list[list[int]]) -> list[int] | None:
    """Exact search. Returns a proper colouring with colours {0,1,2}, or None."""
    color = [-1] * n
    degree = [len(adj[v]) for v in range(n)]

    def bt(placed: int) -> bool:
        if placed == n:
            return True
        best_v = -1
        best_used = 0
        best_key: tuple[int, int, int] | None = None
        for v in range(n):
            if color[v] >= 0:
                continue
            used = 0
            sat = 0
            for u in adj[v]:
                cu = color[u]
                if cu >= 0 and (used & (1 << cu)) == 0:
                    used |= 1 << cu
                    sat += 1
            if used == 7:
                return False
            key = (-sat, -degree[v], v)
            if best_key is None or key < best_key:
                best_key = key
                best_v = v
                best_used = used
        for c in range(3):
            if best_used & (1 << c):
                continue
            color[best_v] = c
            if bt(placed + 1):
                return True
            color[best_v] = -1
        return False

    if bt(0):
        return color
    return None


def combinatorial_faces(n: int, edges: list[list[int]]) -> list[list[int]]:
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    graph.add_edges_from((u, v) for u, v in edges)
    planar, embedding = nx.check_planarity(graph)
    if not planar:
        raise RuntimeError("cached triangulation was reported non-planar")
    seen: set[tuple[int, int]] = set()
    faces: list[list[int]] = []
    for u, v in graph.edges():
        for a, b in ((u, v), (v, u)):
            if (a, b) in seen:
                continue
            face = list(embedding.traverse_face(a, b))
            for i in range(len(face)):
                seen.add((face[i], face[(i + 1) % len(face)]))
            faces.append(face)
    return faces


def _sign(triple: list[int]) -> int:
    """+1 if colours are a cyclic shift of (0,1,2), -1 if a cyclic shift of (0,2,1)."""
    i = triple.index(0)
    cyc = (triple[i], triple[(i + 1) % 3], triple[(i + 2) % 3])
    if cyc == (0, 1, 2):
        return 1
    if cyc == (0, 2, 1):
        return -1
    return 0


def face_sign_colouring(
    n: int, faces: list[list[int]]
) -> list[int] | None:
    """Textbook labelling: opposite cyclic orders on the two colour classes of faces.

    Returns a vertex colouring when the dual is bipartite and the labels close,
    and None when the dual is not bipartite.
    """
    if any(len(face) != 3 for face in faces):
        raise RuntimeError("a face is not a triangle")
    edge_faces: dict[tuple[int, int], list[int]] = {}
    for i, face in enumerate(faces):
        for k in range(3):
            a, b = face[k], face[(k + 1) % 3]
            key = (a, b) if a < b else (b, a)
            edge_faces.setdefault(key, []).append(i)
    dual: list[list[int]] = [[] for _ in faces]
    for incident in edge_faces.values():
        if len(incident) != 2:
            raise RuntimeError(f"edge lies on {len(incident)} faces")
        i, j = incident
        dual[i].append(j)
        dual[j].append(i)

    side = [-1] * len(faces)
    side[0] = 0
    stack = [0]
    while stack:
        f = stack.pop()
        for g in dual[f]:
            if side[g] < 0:
                side[g] = 1 - side[f]
                stack.append(g)
            elif side[g] == side[f]:
                return None

    color = [-1] * n
    seed = faces[0]
    # side 0 follows the stored boundary; side 1 uses the opposite cycle.
    order = seed if side[0] == 0 else [seed[0], seed[2], seed[1]]
    for vertex, col in zip(order, (0, 1, 2)):
        color[vertex] = col

    seen = {0}
    queue: deque[int] = deque([0])
    while queue:
        f = queue.popleft()
        for g in dual[f]:
            face = faces[g]
            unknown = [v for v in face if color[v] < 0]
            known = [v for v in face if color[v] >= 0]
            if len(unknown) == 1 and len(known) == 2:
                used = {color[v] for v in known}
                if len(used) != 2:
                    raise RuntimeError("face-sign conflict on a shared edge")
                color[unknown[0]] = ({0, 1, 2} - used).pop()
            if all(color[v] >= 0 for v in face):
                cols = [color[v] for v in face]
                if len(set(cols)) != 3:
                    raise RuntimeError("face-sign repeated a colour")
                want = 1 if side[g] == 0 else -1
                # Stored boundary orientation is fixed. side 0 must match face 0's
                # sign; side 1 must be the opposite sign.
                if _sign(cols) != want * _sign([color[v] for v in faces[0]]):
                    raise RuntimeError("face-sign orientation disagreed")
            if g not in seen and all(color[v] >= 0 for v in face):
                seen.add(g)
                queue.append(g)
    if any(c < 0 for c in color):
        raise RuntimeError("face-sign left a vertex uncoloured")
    if len(seen) != len(faces):
        raise RuntimeError("face-sign did not reach every face")
    return color


def main() -> None:
    t0 = time.perf_counter()
    data = json.loads(TRI.read_text())
    graphs = data["graphs"]
    by_n: dict[str, dict[str, int]] = {}
    disagreements: list[dict[str, object]] = []
    sat_disagreements: list[str] = []
    eulerian_names: list[str] = []
    construction_errors: list[dict[str, str]] = []
    first_eulerian: dict[str, object] | None = None
    odd_witness: dict[str, object] | None = None
    total = 0
    eulerian_total = 0

    for n_str in [str(n) for n in range(4, 12)]:
        rows = graphs[n_str]
        n = int(n_str)
        stats = {
            "count": len(rows),
            "plantri": PLANTRI[n_str],
            "eulerian": 0,
            "three_colourable": 0,
            "both": 0,
            "neither": 0,
            "construction_ok": 0,
        }
        if len(rows) != PLANTRI[n_str]:
            raise RuntimeError(f"count mismatch at n={n}")
        for i, edges in enumerate(rows):
            total += 1
            if len(edges) != 3 * n - 6:
                raise RuntimeError(f"T_{n}_{i} has {len(edges)} edges")
            adj: list[list[int]] = [[] for _ in range(n)]
            for u, v in edges:
                adj[u].append(v)
                adj[v].append(u)
            degrees = [len(adj[v]) for v in range(n)]
            eulerian = all(d % 2 == 0 for d in degrees)
            colouring = three_colouring(n, adj)
            colourable = colouring is not None
            sat_yes = sat_three_colourable(n, edges)
            if sat_yes != colourable:
                sat_disagreements.append(f"T_{n}_{i}")
            if colourable and not is_proper(n, adj, colouring):
                raise RuntimeError(f"backtrack returned a bad colouring on T_{n}_{i}")
            if eulerian:
                stats["eulerian"] += 1
                eulerian_total += 1
                eulerian_names.append(f"T_{n}_{i}")
            if colourable:
                stats["three_colourable"] += 1
            if eulerian and colourable:
                stats["both"] += 1
            if not eulerian and not colourable:
                stats["neither"] += 1
            if eulerian != colourable:
                disagreements.append(
                    {
                        "name": f"T_{n}_{i}",
                        "eulerian": eulerian,
                        "three_colourable": colourable,
                        "degrees": degrees,
                    }
                )
            if eulerian:
                faces = combinatorial_faces(n, edges)
                if len(faces) != 2 * n - 4:
                    raise RuntimeError(f"T_{n}_{i} has {len(faces)} faces")
                try:
                    built = face_sign_colouring(n, faces)
                except RuntimeError as exc:
                    construction_errors.append({"name": f"T_{n}_{i}", "error": str(exc)})
                    built = None
                if built is None or not is_proper(n, adj, built):
                    construction_errors.append(
                        {"name": f"T_{n}_{i}", "error": "construction missing or improper"}
                    )
                else:
                    stats["construction_ok"] += 1
                    if first_eulerian is None:
                        first_eulerian = {
                            "name": f"T_{n}_{i}",
                            "degrees": degrees,
                            "backtrack_colouring": colouring,
                            "face_sign_colouring": built,
                        }
            elif odd_witness is None:
                odd_witness = {
                    "name": f"T_{n}_{i}",
                    "degrees": degrees,
                    "three_colourable": colourable,
                }
        by_n[n_str] = stats

    elapsed = time.perf_counter() - t0
    payload = {
        "statement": (
            "A simple maximal plane graph on n>=3 vertices is 3-vertex-colourable "
            "if and only if every degree is even."
        ),
        "cache": "compute/data/triangulations_n4_11.json",
        "graphs": total,
        "eulerian": eulerian_total,
        "disagreements": disagreements,
        "sat_disagreements": sat_disagreements,
        "eulerian_names": eulerian_names,
        "construction_errors": construction_errors,
        "kill_met": bool(disagreements),
        "by_n": by_n,
        "first_eulerian": first_eulerian,
        "first_odd_degree": odd_witness,
        "elapsed_seconds": round(elapsed, 4),
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({k: payload[k] for k in (
        "graphs", "eulerian", "eulerian_names", "disagreements",
        "sat_disagreements", "construction_errors", "kill_met",
        "elapsed_seconds", "first_eulerian", "first_odd_degree",
    )}, indent=2))
    print("by_n", json.dumps(by_n))


if __name__ == "__main__":
    main()
