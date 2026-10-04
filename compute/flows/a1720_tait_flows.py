"""Group D1 (Agent 1720): Tait colourings, nowhere-zero flows and P(T,4).

For every cached triangulation ``T`` (``compute/data/triangulations_n4_11.json``)
build the plane dual ``T*`` (cubic, ``2n-4`` vertices) and count, by four
independent methods,

(a) labelled 3-edge-colourings of ``T*`` (backtracking over edges),
(b) nowhere-zero ``Z2 x Z2``-flows of ``T*`` (pairs of elements of the ``Z2``
    cycle space whose supports cover ``E``),
(c) nowhere-zero ``Z4``-flows of ``T*`` for a fixed orientation (values on the
    cotree edges of a spanning tree are free; tree values are forced by
    Kirchhoff's law through the signed fundamental-cycle matrix), and again for
    a second, random orientation,
(d) ``P(T,4)`` by backtracking over proper vertex 4-colourings of ``T``,

and check ``(a) = (b) = (c) = P(T,4)/4``.  For ``n <= max_extra_n`` it also checks
``F(T*,k) = P(T,k)/k`` for ``k = 3, 5`` (Tutte duality at other ``k``).

Sanity graphs with known answers: ``K4`` (6 Tait colourings) and the Petersen
graph (0 Tait colourings, 0 nowhere-zero 4-flows, 240 nowhere-zero Z5-flows).

Usage::

    .venv/bin/python compute/flows/a1720_tait_flows.py [max_n] [max_extra_n]
"""

from __future__ import annotations

import itertools
import json
import random
import sys
import time
from pathlib import Path

import networkx as nx
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "compute" / "data" / "triangulations_n4_11.json"
OUT = ROOT / "backgroundMaterial" / "agent1720" / "groups" / "D1_results.json"

Edge = tuple[int, int]


# --------------------------------------------------------------------------
# Plane dual
# --------------------------------------------------------------------------

def plane_dual(T: nx.Graph) -> tuple[nx.MultiGraph, list[list[int]]]:
    """Return the plane dual of a connected plane graph and its face list.

    The embedding is the one returned by ``nx.check_planarity``; for a
    3-connected planar graph (every triangulation with ``n >= 4``) it is
    unique up to reflection (Whitney), so ``T*`` is well defined.
    Dual vertex ``i`` is face ``i``; dual edge ``e*`` joins the two faces on
    either side of the primal edge ``e`` and carries ``primal=e``.
    """
    ok, emb = nx.check_planarity(T)
    if not ok:
        raise ValueError("graph is not planar")
    face_of: dict[tuple[int, int], int] = {}
    faces: list[list[int]] = []
    for u, v in emb.edges():
        if (u, v) in face_of:
            continue
        marked: set[tuple[int, int]] = set()
        face = emb.traverse_face(u, v, mark_half_edges=marked)
        for he in marked:
            face_of[he] = len(faces)
        faces.append(face)
    D = nx.MultiGraph()
    D.add_nodes_from(range(len(faces)))
    for u, v in T.edges():
        D.add_edge(face_of[(u, v)], face_of[(v, u)], primal=(u, v))
    return D, faces


def simple_dual(T: nx.Graph) -> nx.Graph:
    """Plane dual of a triangulation as a simple graph (asserts it is simple and cubic)."""
    D, faces = plane_dual(T)
    n, m = T.number_of_nodes(), T.number_of_edges()
    assert len(faces) == 2 * n - 4 and all(len(f) == 3 for f in faces), "not a triangulation"
    assert n - m + len(faces) == 2, "Euler's formula fails"
    G = nx.Graph()
    G.add_nodes_from(D.nodes())
    for a, b in D.edges():
        assert a != b and not G.has_edge(a, b), "dual has a loop or parallel edge"
        G.add_edge(a, b)
    assert all(d == 3 for _, d in G.degree()), "dual is not cubic"
    return G


# --------------------------------------------------------------------------
# (a) Tait colourings by backtracking
# --------------------------------------------------------------------------

def count_tait(G: nx.Graph) -> int:
    """Number of proper 3-edge-colourings of a cubic graph, colours labelled.

    Edges are processed in BFS order; the three edges at the root are fixed
    to colours 0,1,2 and the result multiplied by ``3! = 6`` (colour symmetry).
    """
    root = min(G.nodes())
    order: list[Edge] = []
    seen: set[frozenset[int]] = set()
    for u in [root] + [v for _, v in nx.bfs_edges(G, root)]:
        for w in sorted(G[u]):
            key = frozenset((u, w))
            if key not in seen:
                seen.add(key)
                order.append((u, w))
    used: dict[int, int] = {v: 0 for v in G.nodes()}  # bitmask of colours at v
    for c, (u, w) in enumerate(order[:3]):
        assert u == root
        used[u] |= 1 << c
        used[w] |= 1 << c
    rest = order[3:]

    def rec(i: int) -> int:
        if i == len(rest):
            return 1
        u, w = rest[i]
        free = 7 & ~(used[u] | used[w])
        total = 0
        for c in range(3):
            b = 1 << c
            if free & b:
                used[u] |= b
                used[w] |= b
                total += rec(i + 1)
                used[u] &= ~b
                used[w] &= ~b
        return total

    return 6 * rec(0)


# --------------------------------------------------------------------------
# Spanning tree / fundamental cycles
# --------------------------------------------------------------------------

def fundamental_cycles(G: nx.Graph, orient: dict[frozenset[int], Edge]) -> tuple[list[Edge], np.ndarray]:
    """Signed fundamental-cycle matrix of a connected graph.

    Returns ``(edges, C)`` where ``edges`` lists the oriented edges (tree edges
    first, then cotree edges) and row ``j`` of ``C`` is the integer flow that
    sends one unit around the fundamental cycle of the ``j``-th cotree edge in
    its own direction.  Every row satisfies ``B @ row = 0`` over the integers,
    where ``B`` is the signed incidence matrix (asserted).
    """
    root = min(G.nodes())
    parent: dict[int, int | None] = {root: None}
    for a, b in nx.bfs_edges(G, root):
        parent[b] = a
    tree = {frozenset((v, p)) for v, p in parent.items() if p is not None}
    tree_edges = [orient[k] for k in sorted(tree, key=sorted)]
    cotree_edges = [orient[k] for k in sorted(set(orient) - tree, key=sorted)]
    edges = tree_edges + cotree_edges
    idx = {frozenset(e): i for i, e in enumerate(edges)}
    depth = {root: 0}
    for v in nx.bfs_tree(G, root):
        if parent[v] is not None:
            depth[v] = depth[parent[v]] + 1

    def path_to_root(v: int) -> list[int]:
        p = [v]
        while parent[p[-1]] is not None:
            p.append(parent[p[-1]])
        return p

    C = np.zeros((len(cotree_edges), len(edges)), dtype=np.int64)
    for j, (a, b) in enumerate(cotree_edges):
        row = C[j]
        row[idx[frozenset((a, b))]] = 1
        # walk from b back to a through the tree: b -> lca -> a
        pb, pa = path_to_root(b), path_to_root(a)
        sa = set(pa)
        lca = next(x for x in pb if x in sa)
        walk = pb[: pb.index(lca) + 1] + list(reversed(pa[: pa.index(lca)]))
        for x, y in zip(walk, walk[1:]):
            e = orient[frozenset((x, y))]
            row[idx[frozenset((x, y))]] += 1 if e == (x, y) else -1
    B = np.zeros((G.number_of_nodes(), len(edges)), dtype=np.int64)
    nodes = {v: i for i, v in enumerate(G.nodes())}
    for i, (x, y) in enumerate(edges):
        B[nodes[x], i] += 1  # outflow
        B[nodes[y], i] -= 1
    assert not (B @ C.T).any(), "fundamental cycle violates Kirchhoff"
    assert len(tree_edges) == G.number_of_nodes() - 1
    return edges, C


def default_orientation(G: nx.Graph) -> dict[frozenset[int], Edge]:
    """Orient each edge from the smaller to the larger label."""
    return {frozenset((u, v)): (min(u, v), max(u, v)) for u, v in G.edges()}


def random_orientation(G: nx.Graph, rng: random.Random) -> dict[frozenset[int], Edge]:
    """Orient each edge uniformly at random."""
    out = {}
    for u, v in G.edges():
        out[frozenset((u, v))] = (u, v) if rng.random() < 0.5 else (v, u)
    return out


# --------------------------------------------------------------------------
# (b) nowhere-zero Z2 x Z2 flows via the Z2 cycle space
# --------------------------------------------------------------------------

def count_z2z2_flows(G: nx.Graph) -> int:
    """Nowhere-zero ``Z2 x Z2``-flows = ordered pairs ``(c1, c2)`` of even subgraphs
    (elements of the ``Z2`` cycle space) with ``c1 | c2 = E``.
    """
    _, C = fundamental_cycles(G, default_orientation(G))
    m = C.shape[1]
    basis = [int(sum(1 << i for i in range(m) if C[j, i] % 2)) for j in range(C.shape[0])]
    space = [0]
    for b in basis:
        space += [s ^ b for s in space]
    arr = np.array(space, dtype=np.int64)
    full = (1 << m) - 1
    total = 0
    chunk = 256
    for s in range(0, len(arr), chunk):
        total += int(np.count_nonzero((arr[s:s + chunk, None] | arr[None, :]) == full))
    return total


# --------------------------------------------------------------------------
# (c) nowhere-zero Z_k flows via free cotree values
# --------------------------------------------------------------------------

def count_zk_flows(G: nx.Graph, k: int, orient: dict[frozenset[int], Edge]) -> int:
    """Nowhere-zero ``Z_k``-flows for the given orientation.

    A ``Z_k``-flow of a connected graph is determined by its (arbitrary) values
    on the cotree edges: ``phi = sum_j x_j C_j (mod k)``.  Enumerate all
    ``x in {1..k-1}^{cotree}`` and keep those whose forced tree values are nonzero.
    """
    edges, C = fundamental_cycles(G, orient)
    t = G.number_of_nodes() - 1
    M = C[:, :t] % k  # contribution of each cotree edge to each tree edge
    r = C.shape[0]
    total = 0
    vals = np.array(list(itertools.product(range(1, k), repeat=min(r, 8))), dtype=np.int64)
    if r <= 8:
        tv = (vals @ M) % k
        return int(np.count_nonzero((tv != 0).all(axis=1)))
    head = r - 8
    for prefix in itertools.product(range(1, k), repeat=head):
        base = (np.array(prefix, dtype=np.int64) @ M[:head]) % k
        tv = (base + vals @ M[head:]) % k
        total += int(np.count_nonzero((tv != 0).all(axis=1)))
    return total


# --------------------------------------------------------------------------
# (d) chromatic polynomial values by backtracking
# --------------------------------------------------------------------------

def count_colourings(T: nx.Graph, k: int) -> int:
    """Number of proper vertex ``k``-colourings (``P(T,k)``) by backtracking.

    Vertices are taken in BFS order; the first edge is fixed to colours
    ``(0,1)`` and the result multiplied by ``k(k-1)``.
    """
    root = min(T.nodes())
    order = [root] + [v for _, v in nx.bfs_edges(T, root)]
    pos = {v: i for i, v in enumerate(order)}
    back = [[pos[w] for w in T[v] if pos[w] < i] for i, v in enumerate(order)]
    col = [-1] * len(order)
    col[0], col[1] = 0, 1
    assert pos[order[1]] in [pos[w] for w in T[root]]

    def rec(i: int) -> int:
        if i == len(order):
            return 1
        forbidden = {col[j] for j in back[i]}
        total = 0
        for c in range(k):
            if c not in forbidden:
                col[i] = c
                total += rec(i + 1)
        col[i] = -1
        return total

    return k * (k - 1) * rec(2)


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

def sanity() -> dict:
    """Known values on K4 and the Petersen graph."""
    K4 = nx.complete_graph(4)
    P = nx.petersen_graph()
    o = default_orientation(P)
    res = {
        "K4_tait": count_tait(K4),
        "K4_z2z2": count_z2z2_flows(K4),
        "K4_z4": count_zk_flows(K4, 4, default_orientation(K4)),
        "K4_P4_over_4": count_colourings(K4, 4) // 4,
        "K4_dual_is_K4": nx.is_isomorphic(simple_dual(K4), K4),
        "Petersen_tait": count_tait(P),
        "Petersen_z2z2": count_z2z2_flows(P),
        "Petersen_z4": count_zk_flows(P, 4, o),
        "Petersen_z5": count_zk_flows(P, 5, o),
    }
    assert res["K4_tait"] == res["K4_z2z2"] == res["K4_z4"] == res["K4_P4_over_4"] == 6
    assert res["Petersen_tait"] == res["Petersen_z2z2"] == res["Petersen_z4"] == 0
    assert res["Petersen_z5"] == 240, res["Petersen_z5"]
    return res


def main(max_n: int = 11, max_extra_n: int = 10) -> None:
    """Run all checks up to ``max_n`` and write ``D1_results.json``."""
    t0 = time.time()
    data = json.loads(DATA.read_text())
    rng = random.Random(1720)
    out: dict = {"sanity": sanity(), "per_n": {}, "mismatches": [], "graphs": {}}
    for n in range(4, max_n + 1):
        tn = time.time()
        rows = []
        for i, el in enumerate(data["graphs"][str(n)]):
            T = nx.Graph([tuple(e) for e in el])
            D = simple_dual(T)
            a = count_tait(D)
            b = count_z2z2_flows(D)
            c = count_zk_flows(D, 4, default_orientation(D))
            c2 = count_zk_flows(D, 4, random_orientation(D, rng))
            p4 = count_colourings(T, 4)
            row = {
                "name": f"T_{n}_{i}", "dual_vertices": D.number_of_nodes(),
                "dual_edges": D.number_of_edges(),
                "dual_vertex_connectivity": nx.node_connectivity(D),
                "dual_edge_connectivity": nx.edge_connectivity(D),
                "tait": a, "z2z2": b, "z4": c, "z4_random_orientation": c2, "P4": p4,
            }
            ok = a == b == c == c2 and 4 * a == p4 and a > 0
            if n <= max_extra_n:
                for k in (3, 5):
                    fk = count_zk_flows(D, k, default_orientation(D))
                    pk = count_colourings(T, k)
                    row[f"z{k}"], row[f"P{k}"] = fk, pk
                    ok = ok and k * fk == pk
            row["ok"] = ok
            if not ok:
                out["mismatches"].append(row)
            rows.append(row)
        el_n = time.time() - tn
        out["graphs"][str(n)] = rows
        out["per_n"][str(n)] = {
            "count": len(rows),
            "all_identities_hold": all(r["ok"] for r in rows),
            "extra_k3_k5_checked": n <= max_extra_n,
            "tait_min": min(r["tait"] for r in rows),
            "tait_max": max(r["tait"] for r in rows),
            "dual_vertex_connectivity_values": sorted({r["dual_vertex_connectivity"] for r in rows}),
            "dual_edge_connectivity_values": sorted({r["dual_edge_connectivity"] for r in rows}),
            "elapsed_seconds": round(el_n, 2),
        }
        print(f"n={n}: {len(rows)} graphs, ok={out['per_n'][str(n)]['all_identities_hold']}, "
              f"tait in [{out['per_n'][str(n)]['tait_min']},{out['per_n'][str(n)]['tait_max']}], "
              f"{el_n:.1f}s", flush=True)
    out["elapsed_seconds"] = round(time.time() - t0, 2)
    out["command"] = f".venv/bin/python compute/flows/a1720_tait_flows.py {max_n} {max_extra_n}"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"mismatches: {len(out['mismatches'])}; total {out['elapsed_seconds']}s; wrote {OUT}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 11,
         int(sys.argv[2]) if len(sys.argv) > 2 else 10)
