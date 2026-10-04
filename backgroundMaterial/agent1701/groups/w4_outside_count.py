"""W4: count proper 5-colourings of T_9_35 with c(6)=5, and split them by S.

S is the set of colourings in exhaustive_details of merge_tolerant_results.json
with graph T_9_35 and vertex 6.

Does not path-search. Stops if enumerate_colourings exceeds 600 seconds.
Does not edit docs/navigator. Does not install packages.
"""

from __future__ import annotations

import json
import os
import signal
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "compute", "kempe"))

from kempe_ops import enumerate_colourings, is_proper_colouring  # noqa: E402
from triangulation_db import generate_triangulations  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
MERGE_PATH = os.path.join(
    ROOT,
    "backgroundMaterial/agent1545/coordinator/manager_M1/sub_S1/merge_tolerant_results.json",
)
VERTEX = 6
LIMIT_S = 600.0


class EnumTimeout(Exception):
    pass


def _on_alarm(signum, frame):
    raise EnumTimeout()


def _as_colouring(raw: dict) -> dict:
    return {int(k): int(v) for k, v in raw.items()}


def _key(col: dict) -> tuple:
    return tuple(col[i] for i in range(9))


def main() -> None:
    wall0 = time.perf_counter()

    t_json = time.perf_counter()
    with open(MERGE_PATH) as f:
        merge = json.load(f)
    json_s = time.perf_counter() - t_json

    stored = []
    for entry in merge["exhaustive_details"]:
        if entry.get("graph") == "T_9_35" and entry.get("vertex") == VERTEX:
            stored.append(_as_colouring(entry["colouring"]))
    stored_keys = [_key(c) for c in stored]
    S = set(stored_keys)

    t_gen = time.perf_counter()
    db = generate_triangulations(9)
    gen_s = time.perf_counter() - t_gen
    graphs = db[9]
    G = graphs[35]
    name = G.graph.get("name")

    signal.signal(signal.SIGALRM, _on_alarm)
    signal.setitimer(signal.ITIMER_REAL, LIMIT_S)
    t_enum = time.perf_counter()
    try:
        all_cols = enumerate_colourings(G, 5)
    except EnumTimeout:
        elapsed = time.perf_counter() - t_enum
        print("status=timeout")
        print(f"enum_elapsed_s={elapsed:.3f}")
        print(f"limit_s={LIMIT_S:.1f}")
        print("partial_count=unknown")
        print("note=enumerate_colourings has no progress counter; no partial list was returned")
        return
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0.0)
    enum_s = time.perf_counter() - t_enum

    fixed = [c for c in all_cols if c.get(VERTEX) == 5]
    fixed_keys = [_key(c) for c in fixed]
    fixed_set = set(fixed_keys)

    in_S = [k for k in fixed_keys if k in S]
    outside = [k for k in fixed_keys if k not in S]
    missing_from_enum = [k for k in S if k not in fixed_set]
    s_not_colour_5 = [k for k in stored_keys if k[VERTEX] != 5]

    proper_fixed = sum(1 for c in fixed if is_proper_colouring(G, c))
    proper_S = 0
    for c in stored:
        if is_proper_colouring(G, c):
            proper_S += 1

    wall = time.perf_counter() - wall0

    print(f"status=ok")
    print(f"graph_name={name!r}")
    print(f"n9_count={len(graphs)}")
    print(f"index=35")
    print(f"order={G.order()}")
    print(f"size={G.size()}")
    print(f"degree_vertex_6={G.degree(VERTEX)}")
    print(f"stored_entries={len(stored)}")
    print(f"stored_distinct={len(S)}")
    print(f"stored_with_c6_not_5={len(s_not_colour_5)}")
    print(f"stored_proper_on_G={proper_S}")
    print(f"all_proper_5_colourings={len(all_cols)}")
    print(f"with_c6_eq_5={len(fixed)}")
    print(f"with_c6_eq_5_distinct={len(fixed_set)}")
    print(f"with_c6_eq_5_proper={proper_fixed}")
    print(f"in_S={len(in_S)}")
    print(f"in_S_distinct={len(set(in_S))}")
    print(f"outside_S={len(outside)}")
    print(f"outside_S_distinct={len(set(outside))}")
    print(f"S_missing_from_enum={len(missing_from_enum)}")
    print(f"json_load_s={json_s:.3f}")
    print(f"generate_triangulations_s={gen_s:.3f}")
    print(f"enumerate_colourings_s={enum_s:.3f}")
    print(f"wall_s={wall:.3f}")
    print(f"outside_larger_than_30={len(set(outside)) > 30}")


if __name__ == "__main__":
    main()
