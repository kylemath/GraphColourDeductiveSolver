"""Identify generate_triangulations(9)[35] and compare it to the first
degree-4, vertex-6 record in counterexample_details.json.

Does not enumerate colourings.
"""

from __future__ import annotations

import json
import os
import sys
import time
from typing import Iterable, List, Sequence, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "compute", "kempe"))

from triangulation_db import generate_triangulations  # noqa: E402

Edge = Tuple[int, int]

JSON_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "agent1520",
    "coordinator",
    "manager_M1",
    "sub_S3",
    "counterexample_details.json",
)


def sorted_edges(pairs: Iterable[Sequence[int]]) -> List[Edge]:
    return sorted((min(int(u), int(v)), max(int(u), int(v))) for u, v in pairs)


def main() -> None:
    t0 = time.time()
    db = generate_triangulations(9)
    elapsed = time.time() - t0
    graphs = db[9]
    print(f"n9_count={len(graphs)} elapsed_s={elapsed:.1f}")
    if len(graphs) <= 35:
        raise SystemExit(f"index 35 missing; only {len(graphs)} graphs")

    T = graphs[35]
    name = T.graph.get("name")
    edges = sorted_edges(T.edges())
    deg6 = int(T.degree(6))
    nbrs = sorted(int(u) for u in T.neighbors(6))

    print(f"name={name!r}")
    print(f"edge_count={len(edges)}")
    print(f"degree_vertex_6={deg6}")
    print(f"neighbours_vertex_6={nbrs}")
    print("edges=")
    for e in edges:
        print(f"  {e[0]} {e[1]}")

    with open(JSON_PATH) as f:
        records = json.load(f)

    match_idx = None
    record = None
    for i, obj in enumerate(records):
        if obj.get("vertex") == 6 and obj.get("degree") == 4:
            match_idx = i
            record = obj
            break
    if record is None:
        raise SystemExit("no JSON object with vertex 6 and degree 4")

    json_edges = sorted_edges(record["graph_edges"])
    json_nbrs = sorted(int(u) for u in record.get("neighbours", []))
    print(f"json_record_index={match_idx}")
    print(f"json_edge_count={len(json_edges)}")
    print(f"json_neighbours={json_nbrs}")

    only_gen = [e for e in edges if e not in json_edges]
    only_json = [e for e in json_edges if e not in edges]
    same = edges == json_edges
    print(f"edge_lists_equal={same}")
    print(f"only_in_index_35={only_gen}")
    print(f"only_in_json={only_json}")
    print(f"neighbours_equal={nbrs == json_nbrs}")


if __name__ == "__main__":
    main()
