"""
a1720_k6_kittell.py -- Agent 1720, group K6b: KC5 on the Kittell triangulation.

The adjacency is copied from SageMath's graphs.KittellGraph() in
src/sage/graphs/generators/smallgraphs.py (branch develop, function
KittellGraph). That file's doctest states order 23 and size 63. MathWorld
describes the Kittell graph as a planar graph on 23 nodes and 63 edges
(https://mathworld.wolfram.com/KittellGraph.html).

The list in a1720_k6_named.py is not used. This script does not write
K6_named.json or K6_cache_n4_11.json.

KC5 is the implementation in a1720_k6_kc5.py (analyse_vertex, adjacency,
degree5_vertices). Those functions are imported, not rewritten.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Set, Tuple

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parent))
from a1720_k6_kc5 import ROOT, adjacency, analyse_vertex, degree5_vertices  # noqa: E402

# Verbatim dict_of_lists from SageMath KittellGraph (develop smallgraphs.py).
KITTELL: Dict[int, List[int]] = {
    0: [1, 2, 4, 5, 6, 7],
    1: [0, 2, 7, 10, 11, 13],
    2: [0, 1, 11, 4, 14],
    3: [16, 12, 4, 5, 14],
    4: [0, 2, 3, 5, 14],
    5: [0, 16, 3, 4, 6],
    6: [0, 5, 7, 15, 16, 17, 18],
    7: [0, 1, 6, 8, 13, 18],
    8: [9, 18, 19, 13, 7],
    9: [8, 10, 19, 20, 13],
    10: [1, 9, 11, 13, 20, 21],
    11: [1, 2, 10, 12, 14, 15, 21],
    12: [11, 16, 3, 14, 15],
    13: [8, 1, 10, 9, 7],
    14: [11, 12, 2, 3, 4],
    15: [6, 11, 12, 16, 17, 21, 22],
    16: [3, 12, 5, 6, 15],
    17: [18, 19, 22, 6, 15],
    18: [8, 17, 19, 6, 7],
    19: [8, 9, 17, 18, 20, 22],
    20: [9, 10, 19, 21, 22],
    21: [10, 11, 20, 22, 15],
    22: [17, 19, 20, 21, 15],
}

SAGE_URL = (
    "https://github.com/sagemath/sage/blob/develop/src/sage/graphs/"
    "generators/smallgraphs.py"
)
MATHWORLD_URL = "https://mathworld.wolfram.com/KittellGraph.html"
OUT = ROOT / "backgroundMaterial" / "agent1720" / "groups" / "K6_kittell.json"


def graph_from_dict(adj_dict: Dict[int, List[int]]) -> nx.Graph:
    """Undirected simple graph on vertices 0..22 from a dict of neighbour lists."""
    g = nx.Graph()
    g.add_nodes_from(range(23))
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
        for u, nbrs in KITTELL.items()
        for w in nbrs
        if u not in KITTELL[w]
    ]
    planar, emb = nx.check_planarity(g, counterexample=False)
    faces = face_walks(g, emb) if planar else []
    lengths = sorted(len(f) for f in faces)
    n, m = g.number_of_nodes(), g.number_of_edges()
    info = {
        "n": n,
        "m": m,
        "simple": g.number_of_edges() == sum(len(v) for v in KITTELL.values()) // 2,
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
        info["n"] == 23
        and info["m"] == 63
        and info["simple"]
        and info["symmetric_listing"]
        and info["connected"]
        and info["planar"]
        and info["all_faces_triangles"]
        and info["euler_characteristic"] == 2
        and info["m_equals_3n_minus_6"]
    )
    return info


def main() -> None:
    t0 = time.perf_counter()
    g = graph_from_dict(KITTELL)
    info = structural(g)
    edges = sorted(tuple(sorted(e)) for e in g.edges())
    out: Dict = {
        "name": "Kittell",
        "source": {
            "sage_function": "graphs.KittellGraph",
            "sage_file": "src/sage/graphs/generators/smallgraphs.py",
            "sage_url": SAGE_URL,
            "sage_doctest_order_size": [23, 63],
            "mathworld_url": MATHWORLD_URL,
            "mathworld_statement": (
                "The Kittell graph is a planar graph on 23 nodes and 63 edges "
                "that tangles the Kempe chains in Kempe's coloring algorithm."
            ),
        },
        "structural": info,
        "edges": edges,
        "kc5": None,
    }
    print(json.dumps(info), flush=True)
    if not info["ok"]:
        out["status"] = "blocked"
        out["elapsed_seconds"] = round(time.perf_counter() - t0, 2)
        OUT.write_text(json.dumps(out, indent=1) + "\n")
        print("blocked; wrote", OUT, flush=True)
        sys.exit(1)

    adj = adjacency(23, edges)
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
        "max_kempe_distance_to_fix": max(r["max_kempe_distance_to_fix"] for r in rows),
        "n_classes": sum(r["n_classes"] for r in rows),
        "vertices": rows,
    }
    out["status"] = "computed"
    out["elapsed_seconds"] = elapsed
    OUT.write_text(json.dumps(out, indent=1) + "\n")
    print("wrote", OUT, "elapsed", elapsed, flush=True)


if __name__ == "__main__":
    main()
