"""Regenerate generate_triangulations(9)[25] and replay the first
vertex-3, degree-5 colouring in counterexample_details.json.

Does not enumerate other colourings. Does not edit the navigator.
"""

from __future__ import annotations

import json
import os
import sys
import time
from typing import Dict, Iterable, List, Sequence, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "compute", "kempe"))

from kempe_ops import (  # noqa: E402
    colouring_from_canonical,
    colours_used,
    get_kempe_chain,
    is_proper_colouring,
    kempe_swap,
    num_colours,
)
from reduction_search import _identify_swap, bfs_reduce_to_4  # noqa: E402
from triangulation_db import generate_triangulations, is_triangulation  # noqa: E402

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


def int_colouring(raw: Dict) -> Dict[int, int]:
    return {int(k): int(v) for k, v in raw.items()}


def main() -> None:
    t0 = time.time()
    db = generate_triangulations(9)
    gen_elapsed = time.time() - t0
    graphs = db[9]
    print(f"n9_count={len(graphs)} gen_elapsed_s={gen_elapsed:.1f}")
    if len(graphs) <= 25:
        raise SystemExit(f"index 25 missing; only {len(graphs)} graphs")

    T = graphs[25]
    name = T.graph.get("name")
    edges = sorted_edges(T.edges())
    print(f"name={name!r}")
    print(f"is_triangulation={is_triangulation(T)}")
    print(f"edge_count={len(edges)}")
    print(f"degree_vertex_3={int(T.degree(3))}")
    print(f"neighbours_vertex_3={sorted(int(u) for u in T.neighbors(3))}")
    print("edges=")
    for e in edges:
        print(f"  {e[0]} {e[1]}")

    with open(JSON_PATH) as f:
        records = json.load(f)

    match_idx = None
    record = None
    for i, obj in enumerate(records):
        if obj.get("vertex") == 3 and obj.get("degree") == 5:
            match_idx = i
            record = obj
            break
    if record is None:
        raise SystemExit("no JSON object with vertex 3 and degree 5")

    json_edges = sorted_edges(record["graph_edges"])
    only_gen = [e for e in edges if e not in json_edges]
    only_json = [e for e in json_edges if e not in edges]
    print(f"json_record_index={match_idx}")
    print(f"json_edge_count={len(json_edges)}")
    print(f"edge_lists_equal={edges == json_edges}")
    print(f"only_in_index_25={only_gen}")
    print(f"only_in_json={only_json}")

    col = int_colouring(record["colouring"])
    v = 3
    print(f"c_v={col[v]}")
    print(f"json_degree={record['degree']}")
    print(f"json_neighbours={record['neighbours']}")
    print(f"proper_on_G={is_proper_colouring(T, col)}")
    print(f"colours_on_G={sorted(colours_used(col))}")
    print(f"num_colours_on_G={num_colours(col)}")

    H = T.copy()
    H.remove_node(v)
    col_H = {u: col[u] for u in H.nodes()}
    print(f"proper_on_H={is_proper_colouring(H, col_H)}")
    print(f"colours_on_H={sorted(colours_used(col_H))}")
    print(f"num_colours_on_H={num_colours(col_H)}")

    t1 = time.time()
    path = bfs_reduce_to_4(H, col_H, k=5)
    bfs_elapsed = time.time() - t1
    print(f"bfs_elapsed_s={bfs_elapsed:.3f}")
    print(f"bfs_list_length={None if path is None else len(path)}")
    print(f"json_bfs_path_length={record['bfs_path_length']}")
    print(f"json_step_count={len(record['path_details'])}")

    if path is None:
        raise SystemExit("bfs_reduce_to_4 returned None")

    recorded = record["path_details"]
    if len(path) - 1 != len(recorded):
        print("STEP_COUNT_MISMATCH")

    cur_col_G = dict(col)
    for i in range(len(path) - 1):
        cur_H = colouring_from_canonical(H, path[i])
        nxt_H = colouring_from_canonical(H, path[i + 1])
        a, b = _identify_swap(H, cur_H, nxt_H)
        swapped = sorted(u for u in H.nodes() if cur_H[u] != nxt_H[u])
        step = recorded[i] if i < len(recorded) else {}
        print(f"--- step {i} ---")
        print(f"replay_swap_pair={[a, b]}")
        print(f"json_swap_pair={step.get('swap_pair')}")
        print(f"replay_swapped={swapped}")
        print(f"json_swapped={step.get('swapped_vertices')}")
        print(f"json_is_a5={step.get('is_a5')}")
        print(f"json_is_unsafe={step.get('is_unsafe')}")
        print(f"json_merge_prone={step.get('merge_prone')}")
        print(f"json_num_chains_at_v={step.get('num_chains_at_v')}")
        print(f"json_v_nbrs_in_ba5={step.get('v_nbrs_in_ba5')}")
        print(f"json_chain_size={step.get('chain_size')}")
        print(f"colouring_before={ {u: cur_H[u] for u in sorted(H.nodes())} }")

        if a is not None and 5 in (a, b):
            the_a = a if a != 5 else b
            nbrs = sorted(
                u for u in T.neighbors(v)
                if u in H.nodes() and cur_H[u] in (the_a, 5)
            )
            chains = {}
            for u in nbrs:
                chains[u] = sorted(get_kempe_chain(H, cur_H, u, the_a, 5))
            distinct = []
            for ch in chains.values():
                if ch not in distinct:
                    distinct.append(ch)
            print(f"replay_a={the_a}")
            print(f"replay_v_nbrs_in_ba5={nbrs}")
            print(f"replay_chains_by_nbr={chains}")
            print(f"replay_distinct_chains={distinct}")
            print(f"replay_num_chains={len(distinct)}")
            if swapped:
                sv = swapped[0]
                if cur_H[sv] in (the_a, 5):
                    sch = sorted(get_kempe_chain(H, cur_H, sv, the_a, 5))
                    print(f"replay_swapped_chain={sch}")
                    print(f"swapped_equals_a_nbr_chain={sch in distinct}")
                    print(f"swapped_meets_N_v={any(u in T.neighbors(v) for u in swapped)}")

        if swapped and a is not None:
            cur_col_G = kempe_swap(cur_col_G, frozenset(swapped), a, b)

    end_H = colouring_from_canonical(H, path[-1])
    print(f"end_H={ {u: end_H[u] for u in sorted(H.nodes())} }")
    print(f"end_proper={is_proper_colouring(H, end_H)}")
    print(f"end_colours={sorted(colours_used(end_H))}")
    print(f"end_num_colours={num_colours(end_H)}")
    print(f"path_edge_length={len(path) - 1}")
    print(f"total_elapsed_s={time.time() - t0:.1f}")
    print("json_merge_info=" + json.dumps(record["merge_info"]))
    print("json_verification=" + json.dumps(record["verification"]))


if __name__ == "__main__":
    main()
