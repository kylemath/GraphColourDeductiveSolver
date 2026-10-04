"""Finite check of Hajós's conjecture at k=5.

A counterexample is a simple graph with chromatic number at least 5 and no
subdivision of K5. The check covers the NetworkX graph atlas (all graphs on
at most 7 vertices) and every cached triangulation T_n_i for n=4..11.

The same pass records minimum degrees. Euler's formula gives
sum_v (6-deg v)=12 for a maximal planar graph, so a triangulation on
n<=11 vertices has a vertex of degree at most 4. The icosahedron is the
standard degree-5 obstruction to deleting such a vertex forever.
"""

from __future__ import annotations

import json
import time
from itertools import combinations
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "compute" / "data" / "triangulations_n4_11.json"
OUT = ROOT / "backgroundMaterial" / "agent1720" / "groups" / "S4_results.json"
PLANTRI = {4: 1, 5: 1, 6: 2, 7: 5, 8: 14, 9: 50, 10: 233, 11: 1249}


def _popcount(x: int) -> int:
    return bin(x).count("1")


def _bit_adj(n: int, edges: list[tuple[int, int]]) -> list[int]:
    adj = [0] * n
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    return adj


def colourable(n: int, adj: list[int], k: int) -> bool:
    """Exact backtrack. Vertices are ordered by nonincreasing degree."""
    order = sorted(range(n), key=lambda i: -_popcount(adj[i]))
    pos = [0] * n
    for i, v in enumerate(order):
        pos[v] = i
    radj = [0] * n
    for v in range(n):
        m = adj[v]
        while m:
            bit = m & -m
            u = bit.bit_length() - 1
            radj[pos[v]] |= 1 << pos[u]
            m ^= bit
    colour = [-1] * n

    def bt(i: int) -> bool:
        if i == n:
            return True
        used = 0
        m = radj[i]
        while m:
            bit = m & -m
            u = bit.bit_length() - 1
            c = colour[u]
            if c >= 0:
                used |= 1 << c
            m ^= bit
        for c in range(k):
            if used & (1 << c):
                continue
            colour[i] = c
            if bt(i + 1):
                return True
        colour[i] = -1
        return False

    return bt(0)


def _internal_paths(
    adj: list[int], start: int, goal: int, free: int
) -> list[int]:
    """Internal-vertex bitmasks of simple start-goal paths through `free`."""
    found: list[int] = []

    def dfs(u: int, visited: int) -> None:
        m = adj[u]
        while m:
            bit = m & -m
            w = bit.bit_length() - 1
            m ^= bit
            if w == goal:
                if visited:
                    found.append(visited)
                continue
            if free & (1 << w) and not visited & (1 << w):
                dfs(w, visited | (1 << w))

    dfs(start, 0)
    return found


def has_k5_subdivision(n: int, adj: list[int]) -> bool:
    """True iff the graph contains a subdivision of K5.

    Branch vertices have degree at least 4. Each missing branch edge consumes
    at least one private internal vertex.
    """
    if n < 5:
        return False
    candidates = [v for v in range(n) if _popcount(adj[v]) >= 4]
    if len(candidates) < 5:
        return False
    for branch in combinations(candidates, 5):
        bmask = 0
        for v in branch:
            bmask |= 1 << v
        missing = [
            (a, b)
            for a, b in combinations(branch, 2)
            if not adj[a] & (1 << b)
        ]
        internal_mask = ((1 << n) - 1) ^ bmask
        if not missing:
            return True
        if len(missing) > _popcount(internal_mask):
            continue

        def route(i: int, free: int) -> bool:
            if i == len(missing):
                return True
            a, b = missing[i]
            for used in _internal_paths(adj, a, b, free):
                if route(i + 1, free ^ used):
                    return True
            return False

        if route(0, internal_mask):
            return True
    return False


def graph_bits(G: nx.Graph) -> tuple[int, list[int]]:
    relabel = {v: i for i, v in enumerate(G.nodes())}
    n = len(relabel)
    edges = [(relabel[u], relabel[v]) for u, v in G.edges()]
    return n, _bit_adj(n, edges)


def _self_test() -> None:
    k5 = nx.complete_graph(5)
    n, adj = graph_bits(k5)
    assert has_k5_subdivision(n, adj)
    assert not colourable(n, adj, 4)
    assert colourable(n, adj, 5)

    sub = nx.complete_graph(5)
    sub.add_edge(0, 5)
    sub.remove_edge(0, 1)
    sub.add_edge(5, 1)
    n, adj = graph_bits(sub)
    assert has_k5_subdivision(n, adj)

    k4 = nx.complete_graph(4)
    n, adj = graph_bits(k4)
    assert not has_k5_subdivision(n, adj)
    assert colourable(n, adj, 4)
    assert not colourable(n, adj, 3)

    petersen = nx.petersen_graph()
    n, adj = graph_bits(petersen)
    assert not has_k5_subdivision(n, adj)
    assert colourable(n, adj, 4)


def check_atlas() -> dict:
    graphs = list(nx.graph_atlas_g())
    not4 = 0
    not4_with_tk5 = 0
    not4_by_order: dict[int, int] = {}
    counterexamples: list[dict] = []
    by_order = {i: 0 for i in range(8)}
    for G in graphs:
        n, adj = graph_bits(G)
        by_order[n] = by_order.get(n, 0) + 1
        if colourable(n, adj, 4):
            continue
        not4 += 1
        not4_by_order[n] = not4_by_order.get(n, 0) + 1
        tk5 = has_k5_subdivision(n, adj)
        if tk5:
            not4_with_tk5 += 1
        else:
            counterexamples.append(
                {"n": n, "edges": G.number_of_edges(), "tk5": False}
            )
    return {
        "graphs": len(graphs),
        "by_order": {str(k): v for k, v in sorted(by_order.items())},
        "not_4_colourable": not4,
        "not_4_colourable_by_order": {str(k): v for k, v in sorted(not4_by_order.items())},
        "not_4_colourable_with_K5_subdivision": not4_with_tk5,
        "counterexamples": counterexamples,
    }


def check_triangulations() -> dict:
    data = json.loads(CACHE.read_text())
    graphs = data["graphs"]
    counts: dict[str, int] = {}
    min_degree: dict[str, dict[str, int]] = {}
    nonplanar: list[str] = []
    not4: list[str] = []
    tk5_hits: list[str] = []
    planar_but_tk5: list[str] = []
    for n_str, edge_lists in graphs.items():
        n = int(n_str)
        counts[n_str] = len(edge_lists)
        hist = {"3": 0, "4": 0, "ge5": 0}
        for i, edges in enumerate(edge_lists):
            name = f"T_{n}_{i}"
            adj_nx = [[] for _ in range(n)]
            for u, v in edges:
                adj_nx[u].append(v)
                adj_nx[v].append(u)
            degrees = [len(nei) for nei in adj_nx]
            dmin = min(degrees)
            if dmin <= 3:
                hist["3"] += 1
            elif dmin == 4:
                hist["4"] += 1
            else:
                hist["ge5"] += 1
            adj = _bit_adj(n, [tuple(e) for e in edges])
            G = nx.Graph()
            G.add_nodes_from(range(n))
            G.add_edges_from(edges)
            planar, _ = nx.check_planarity(G)
            if not planar:
                nonplanar.append(name)
            tk5 = has_k5_subdivision(n, adj)
            if tk5:
                tk5_hits.append(name)
            if planar and tk5:
                planar_but_tk5.append(name)
            if not colourable(n, adj, 4):
                not4.append(name)
        min_degree[n_str] = hist
    return {
        "counts": counts,
        "plantri_expected": {str(k): v for k, v in PLANTRI.items()},
        "counts_match_plantri": counts == {str(k): v for k, v in PLANTRI.items()},
        "min_degree_histogram": min_degree,
        "nonplanar": nonplanar,
        "K5_subdivision": tk5_hits,
        "planar_and_K5_subdivision": planar_but_tk5,
        "not_4_colourable": not4,
    }


def check_icosahedron() -> dict:
    G = nx.icosahedral_graph()
    n, adj = graph_bits(G)
    degrees = [d for _, d in G.degree()]
    planar, _ = nx.check_planarity(G)
    return {
        "n": n,
        "edges": G.number_of_edges(),
        "min_degree": min(degrees),
        "max_degree": max(degrees),
        "planar": planar,
        "maximal_planar_edge_count": G.number_of_edges() == 3 * n - 6,
        "K5_subdivision": has_k5_subdivision(n, adj),
        "four_colourable": colourable(n, adj, 4),
    }


def main() -> None:
    _self_test()
    start = time.perf_counter()
    atlas = check_atlas()
    triangulations = check_triangulations()
    icosahedron = check_icosahedron()
    elapsed = time.perf_counter() - start
    out = {
        "elapsed_seconds": elapsed,
        "atlas_n_le_7": atlas,
        "triangulations_n4_11": triangulations,
        "icosahedron": icosahedron,
    }
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(f"elapsed_seconds {elapsed:.3f}")
    print(f"atlas graphs {atlas['graphs']} not4 {atlas['not_4_colourable']} counterexamples {len(atlas['counterexamples'])}")
    print(f"triangulation counts match {triangulations['counts_match_plantri']}")
    print(f"nonplanar {len(triangulations['nonplanar'])} tk5 {len(triangulations['K5_subdivision'])} not4 {len(triangulations['not_4_colourable'])}")
    print(f"min_degree {triangulations['min_degree_histogram']}")
    print(f"icosahedron {icosahedron}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
