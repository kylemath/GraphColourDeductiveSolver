"""
a1720_k6_named.py -- K6: KC5 on named triangulations (Errera, Kittell,
icosahedron) and a cross-check of the S_4-quotient against kempe_ops.py.

The Errera and Kittell edge lists are reconstructed from the adjacency data of
SageMath's graphs.ErreraGraph() / graphs.KittellGraph(); they are accepted only
after the structural checks in `check_named` (vertex/edge count, planarity,
triangulation = 3n-6 edges, degree sequence).
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parent))
from a1720_k6_kc5 import (ROOT, adjacency, analyse_vertex, delete_vertex,  # noqa: E402
                          ncols_on, run_named)
import kempe_ops  # noqa: E402

ERRERA = {0: [1, 7, 14, 15, 16], 1: [2, 9, 14, 15], 2: [3, 8, 9, 10, 14],
          3: [4, 9, 10, 11], 4: [5, 10, 11, 12], 5: [6, 11, 12, 13],
          6: [7, 8, 12, 13, 16], 7: [13, 15, 16], 8: [10, 12, 14, 16],
          9: [11, 13, 15], 10: [12], 11: [13], 13: [15], 14: [16]}

KITTELL = {0: [1, 2, 4, 5, 6, 7], 1: [0, 2, 7, 10, 11, 13], 2: [0, 1, 11, 4, 14],
           3: [16, 12, 4, 5, 14, 15], 4: [0, 2, 3, 5, 14], 5: [0, 16, 3, 4, 6],
           6: [0, 5, 7, 16, 17], 7: [0, 1, 6, 8, 9, 10, 17],
           8: [7, 9, 10, 17, 18, 21], 9: [7, 8, 10, 11, 12, 13, 18, 19, 20],
           10: [1, 7, 8, 9, 13], 11: [1, 2, 12, 13, 14],
           12: [3, 9, 11, 14, 15, 19, 20], 13: [1, 9, 10, 11],
           14: [2, 3, 4, 11, 12], 15: [3, 12, 16, 20, 22],
           16: [3, 5, 6, 15, 17, 22], 17: [6, 7, 8, 16, 21, 22],
           18: [8, 9, 19, 20, 21, 22], 19: [9, 12, 18, 20],
           20: [9, 12, 15, 18, 19, 22], 21: [8, 17, 18, 22],
           22: [15, 16, 17, 18, 20, 21]}


def to_graph(d: Dict[int, List[int]]) -> nx.Graph:
    return nx.Graph([(a, b) for a in d for b in d[a]])


def check_named(name: str, G: nx.Graph, n: int, m: int) -> Dict:
    """Structural checks; a named graph is used only if all pass."""
    info = {"name": name, "n": G.number_of_nodes(), "m": G.number_of_edges(),
            "planar": nx.check_planarity(G)[0],
            "is_triangulation": G.number_of_edges() == 3 * G.number_of_nodes() - 6
            and nx.check_planarity(G)[0],
            "degrees": sorted(d for _, d in G.degree()),
            "expected_n_m": [n, m]}
    info["ok"] = info["n"] == n and info["m"] == m and info["is_triangulation"]
    return info


def brute_force_check(edges, n: int, v: int) -> Tuple[int, int]:
    """
    Recompute (number of classes, number of bad classes) at (G, v) using the
    unquotiented kempe_ops routines, as an independent check.
    """
    G = nx.Graph(edges)
    H = G.copy()
    nbrs = list(G.neighbors(v))
    H.remove_node(v)
    cols = kempe_ops.enumerate_colourings(H, 4)
    canon = [kempe_ops.canonical_form(H, c) for c in cols]
    idx = {c: i for i, c in enumerate(canon)}
    comp = [-1] * len(cols)
    ncls = nbad = 0
    for s in range(len(cols)):
        if comp[s] >= 0:
            continue
        comp[s] = ncls
        stack, good = [s], False
        while stack:
            x = stack.pop()
            col = kempe_ops.colouring_from_canonical(H, canon[x])
            if len({col[u] for u in nbrs}) <= 3:
                good = True
            for d in kempe_ops.all_kempe_neighbours(H, col, 4):
                y = idx[d]
                if comp[y] < 0:
                    comp[y] = ncls
                    stack.append(y)
        ncls += 1
        nbad += not good
    return ncls, nbad


def main() -> None:
    out: Dict = {"structural_checks": [], "named_results": [], "brute_force_crosscheck": []}
    ico = nx.icosahedral_graph()
    for name, G, n, m in [("icosahedron", ico, 12, 30),
                          ("Errera", to_graph(ERRERA), 17, 45),
                          ("Kittell", to_graph(KITTELL), 23, 63)]:
        info = check_named(name, G, n, m)
        out["structural_checks"].append(info)
        print(info, flush=True)
        if not info["ok"]:
            continue
        G = nx.convert_node_labels_to_integers(G, ordering="sorted")
        out["named_results"].append(run_named(name, n, list(G.edges())))

    # independent cross-check: quotient code vs raw kempe_ops on small cases
    data = json.loads((ROOT / "compute" / "data" / "triangulations_n4_11.json").read_text())
    t0 = time.time()
    for n in (7, 8, 9):
        for gi, E in enumerate(data["graphs"][str(n)]):
            adj = adjacency(n, E)
            for v in [u for u in range(n) if len(adj[u]) == 5]:
                r = analyse_vertex(adj, v)
                bf = brute_force_check(E, n, v)
                assert (r["n_classes"], r["n_bad_classes"]) == bf, (n, gi, v, r, bf)
                out["brute_force_crosscheck"].append([f"T_{n}_{gi}", v, *bf])
    print("crosscheck ok", len(out["brute_force_crosscheck"]), "pairs", time.time() - t0)
    p = ROOT / "backgroundMaterial" / "agent1720" / "groups" / "K6_named.json"
    p.write_text(json.dumps(out, indent=1))
    print("wrote", p)


if __name__ == "__main__":
    main()
