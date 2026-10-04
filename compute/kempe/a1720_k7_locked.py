"""
a1720_k7_locked.py -- Agent 1720, group K7: KC5 on one published triangulation
claimed to make Kempe's 1879 method fail, other than Errera and Kittell.

The graph is the Fritsch graph. MathWorld states that it is a planar graph on
nine vertices that tangles the Kempe chains in Kempe's colouring algorithm
(https://mathworld.wolfram.com/FritschGraph.html) and cites the edge list at
House of Graphs, graph 1088 (https://houseofgraphs.org/graphs/1088). The
neighbour lists below are the adjacencyList field of
https://houseofgraphs.org/api/graphs/1088 (graphName "Fritsch Graph").

KC5 is analyse_vertex from a1720_k6_kc5.py. Those functions are imported,
not rewritten. The n<=11 census, the icosahedron, Errera, and Kittell are
not recomputed.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Set, Tuple

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parent))
from a1720_k6_kc5 import (  # noqa: E402
    ROOT,
    adjacency,
    analyse_vertex,
    degree5_vertices,
)

# Verbatim adjacencyList from House of Graphs API, graph 1088.
FRITSCH: Dict[int, List[int]] = {
    0: [3, 4, 5, 6],
    1: [3, 4, 7, 8],
    2: [5, 6, 7, 8],
    3: [0, 1, 4, 5, 7],
    4: [0, 1, 3, 6, 8],
    5: [0, 2, 3, 6, 7],
    6: [0, 2, 4, 5, 8],
    7: [1, 2, 3, 5, 8],
    8: [1, 2, 4, 6, 7],
}

HOG_URL = "https://houseofgraphs.org/graphs/1088"
HOG_API = "https://houseofgraphs.org/api/graphs/1088"
MATHWORLD_URL = "https://mathworld.wolfram.com/FritschGraph.html"
OUT = ROOT / "backgroundMaterial" / "agent1720" / "groups" / "K7_results.json"
CACHE = ROOT / "compute" / "data" / "triangulations_n4_11.json"


def graph_from_dict(adj_dict: Dict[int, List[int]]) -> nx.Graph:
    """Undirected simple graph on vertices 0..8 from a dict of neighbour lists."""
    g = nx.Graph()
    g.add_nodes_from(range(9))
    for u, nbrs in adj_dict.items():
        for w in nbrs:
            g.add_edge(u, w)
    return g


def face_walks(g: nx.Graph, emb: nx.PlanarEmbedding) -> List[List[int]]:
    """Each facial walk once, as the vertex cycle returned by traverse_face."""
    seen: Set[Tuple[int, int]] = set()
    faces: List[List[int]] = []
    for u in g.nodes:
        for v in emb.neighbors_cw_order(u):
            if (u, v) in seen:
                continue
            face = emb.traverse_face(u, v)
            cyc = face + [face[0]]
            for i in range(len(face)):
                seen.add((cyc[i], cyc[i + 1]))
            faces.append(face)
    return faces


def structural(g: nx.Graph) -> Dict:
    """Planarity, edge count, and the requirement that every face is a triangle."""
    one_way = [
        [u, w]
        for u, nbrs in FRITSCH.items()
        for w in nbrs
        if u not in FRITSCH[w]
    ]
    planar, emb = nx.check_planarity(g, counterexample=False)
    faces = face_walks(g, emb) if planar else []
    lengths = sorted(len(f) for f in faces)
    n, m = g.number_of_nodes(), g.number_of_edges()
    info = {
        "n": n,
        "m": m,
        "simple": g.number_of_edges() == sum(len(v) for v in FRITSCH.values()) // 2,
        "symmetric_listing": one_way == [],
        "connected": nx.is_connected(g),
        "planar": planar,
        "n_faces": len(faces),
        "face_lengths": lengths,
        "all_faces_triangles": lengths == [3] * len(faces) and len(faces) > 0,
        "euler_characteristic": (n - m + len(faces)) if planar else None,
        "m_equals_3n_minus_6": m == 3 * n - 6,
        "degrees": sorted(d for _, d in g.degree()),
        "degree5_vertices": [u for u in range(n) if g.degree(u) == 5],
    }
    info["ok"] = bool(
        info["n"] == 9
        and info["m"] == 21
        and info["simple"]
        and info["symmetric_listing"]
        and info["connected"]
        and info["planar"]
        and info["all_faces_triangles"]
        and info["euler_characteristic"] == 2
        and info["m_equals_3n_minus_6"]
    )
    return info


def cache_matches(g: nx.Graph) -> List[str]:
    """Indices T_9_i in the cached census isomorphic to g. Does not run KC5."""
    data = json.loads(CACHE.read_text())
    hits = []
    for i, edges in enumerate(data["graphs"]["9"]):
        h = nx.Graph()
        h.add_nodes_from(range(9))
        h.add_edges_from(edges)
        if nx.is_isomorphic(g, h):
            hits.append(f"T_9_{i}")
    return hits


def main() -> None:
    t0 = time.perf_counter()
    g = graph_from_dict(FRITSCH)
    info = structural(g)
    edges = sorted(tuple(sorted(e)) for e in g.edges())
    matches = cache_matches(g)
    out: Dict = {
        "name": "Fritsch",
        "source": {
            "house_of_graphs_id": 1088,
            "house_of_graphs_url": HOG_URL,
            "house_of_graphs_api": HOG_API,
            "canonical_form": "HEutZhj",
            "mathworld_url": MATHWORLD_URL,
            "mathworld_statement": (
                "The Fritsch graph is the planar graph on nine vertices that "
                "tangles the Kempe chains in Kempe's coloring algorithm and "
                "thus provides an example of how Kempe's 1879 proof fails. "
                "MathWorld calls the Fritsch graph and the Soifer graph the "
                "smallest such counterexamples, and cites House of Graphs 1088."
            ),
        },
        "structural": info,
        "cache_isomorphs_n9": matches,
        "edges": edges,
        "kc5": None,
    }
    print(json.dumps({**info, "cache_isomorphs_n9": matches}), flush=True)
    if not info["ok"]:
        out["status"] = "blocked"
        out["elapsed_seconds"] = round(time.perf_counter() - t0, 2)
        OUT.write_text(json.dumps(out, indent=1) + "\n")
        print("blocked; wrote", OUT, flush=True)
        sys.exit(1)

    adj = adjacency(9, edges)
    rows = []
    for v in degree5_vertices(adj):
        tv = time.perf_counter()
        row = analyse_vertex(adj, v)
        row["elapsed_seconds"] = round(time.perf_counter() - tv, 2)
        rows.append(row)
        print(
            "v", v,
            {k: row[k] for k in row if k != "bad_witnesses"},
            flush=True,
        )
    elapsed = round(time.perf_counter() - t0, 2)
    out["kc5"] = {
        "n_degree5_vertices": len(rows),
        "n_bad_classes": sum(r["n_bad_classes"] for r in rows),
        "max_kempe_distance_to_fix": max(
            (r["max_kempe_distance_to_fix"] for r in rows), default=0
        ),
        "n_classes": sum(r["n_classes"] for r in rows),
        "vertices": rows,
    }
    out["status"] = "computed"
    out["elapsed_seconds"] = elapsed
    OUT.write_text(json.dumps(out, indent=1) + "\n")
    print("wrote", OUT, "elapsed", elapsed, flush=True)


if __name__ == "__main__":
    main()
