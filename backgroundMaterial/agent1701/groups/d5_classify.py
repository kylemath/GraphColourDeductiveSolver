"""D5b: classify proper 5-colourings of generate_triangulations(9)[9][25]
with c(3)=5.

G is the triangulation the generator names T_9_25. Vertex 3 has degree 5.
The written colouring that already kills "every shortest path is safe" is
counted with the others. This script does not re-check that kill.

For each colouring, find_safe_bfs_path decides whether a K1-safe shortest
path exists. K1-safety is check_path_safety, which calls is_step_unsafe.
A colouring whose call returns reason "exhausted" has every shortest path
K1-unsafe. On that set only, find_safe_nonoptimal_path(..., max_extra=1)
looks for a K1-safe path of length opt_dist+1, accepted only when
check_path_safety also accepts it.

When a safe shortest path exists, an unsafe shortest path is recorded if
find_safe_bfs_path checked more than one path before returning (each earlier
path failed check_path_safety), or, when it returned on the first path, if a
later shortest path fails check_path_safety.

Stops at 600 seconds. Does not edit docs/navigator. Does not install packages.
"""

from __future__ import annotations

import json
import os
import sys
import time
from collections import Counter, deque
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "compute", "kempe"))

import counterexample_energy_targeted as cet  # noqa: E402
from kempe_ops import (  # noqa: E402
    CanonicalColouring,
    all_kempe_neighbours,
    canonical_form,
    colouring_from_canonical,
    enumerate_colourings,
    is_proper_colouring,
    num_colours,
)
from reduction_search import bfs_reduce_to_4  # noqa: E402
from triangulation_db import generate_triangulations  # noqa: E402
from verify_counterexamples import (  # noqa: E402
    check_path_safety,
    find_safe_bfs_path,
)

OUT_PATH = os.path.join(os.path.dirname(__file__), "d5_classify_results.json")

VERTEX = 3
LIMIT_S = 600.0
MAX_PATHS = 1000

# The colouring already written in D5_witness.md. Counted, not re-opened.
WRITTEN = {0: 1, 1: 2, 2: 3, 3: 5, 4: 4, 5: 5, 6: 4, 7: 2, 8: 5}


def _key(col: dict) -> tuple:
    return tuple(col[i] for i in range(9))


def _fmt(col: dict) -> str:
    return ",".join(f"{i}:{col[i]}" for i in range(9))


def dump(payload: dict) -> None:
    with open(OUT_PATH, "w") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")


def opt_dist_of(H, col) -> Optional[int]:
    col_H = {u: col[u] for u in H.nodes()}
    path = bfs_reduce_to_4(H, col_H, k=5)
    if path is None:
        return None
    return len(path) - 1


def longer_ok(G, H, col, opt_dist: int) -> dict:
    col_H = {u: col[u] for u in H.nodes()}
    t0 = time.perf_counter()
    found = cet.find_safe_nonoptimal_path(
        G, H, VERTEX, col, col_H, opt_dist, max_extra=1
    )
    elapsed = time.perf_counter() - t0
    if found is None:
        return {
            "search_seconds": elapsed,
            "returned": False,
            "length_is_opt_plus_1": False,
        }
    length = len(found) - 1
    is_safe = check_path_safety(G, H, VERTEX, col, found)
    end_colours = num_colours(colouring_from_canonical(H, found[-1]))
    return {
        "search_seconds": elapsed,
        "returned": True,
        "length": length,
        "is_step_safe": is_safe,
        "end_colours": end_colours,
        "length_is_opt_plus_1": length == opt_dist + 1 and end_colours <= 4 and is_safe,
    }


def first_unsafe_after_safe_start(
    G, H, col, max_paths: int = MAX_PATHS
) -> dict:
    """Shortest-path walk using check_path_safety.

    Called only when find_safe_bfs_path already returned a safe path on its
    first checked path. Stops at the first K1-unsafe shortest path.
    """
    col_H = {u: col[u] for u in H.nodes()}
    start_c = canonical_form(H, col_H)
    if num_colours(col_H) <= 4:
        return {"status": "already_4", "paths_checked": 0, "opt_dist": 0}

    dist: Dict[CanonicalColouring, int] = {start_c: 0}
    parents: Dict[CanonicalColouring, List[CanonicalColouring]] = {start_c: []}
    queue: deque = deque([start_c])
    target_dist: Optional[int] = None
    targets: List[CanonicalColouring] = []

    while queue:
        current = queue.popleft()
        d = dist[current]
        if target_dist is not None and d > target_dist:
            break
        current_col = colouring_from_canonical(H, current)
        for nbr in all_kempe_neighbours(H, current_col, 5):
            nd = d + 1
            if target_dist is not None and nd > target_dist:
                continue
            if nbr not in dist:
                dist[nbr] = nd
                parents[nbr] = [current]
                queue.append(nbr)
                nbr_col = colouring_from_canonical(H, nbr)
                if num_colours(nbr_col) <= 4:
                    if target_dist is None:
                        target_dist = nd
                    targets.append(nbr)
            elif dist[nbr] == nd:
                parents[nbr].append(current)

    if not targets:
        return {"status": "no_target", "paths_checked": 0, "opt_dist": None}

    paths_checked = 0
    for t in targets:
        stack: List[Tuple[CanonicalColouring, List[CanonicalColouring]]] = [(t, [t])]
        while stack:
            if paths_checked >= max_paths:
                return {
                    "status": "max_paths",
                    "paths_checked": paths_checked,
                    "opt_dist": target_dist,
                }
            node, path_so_far = stack.pop()
            if not parents[node]:
                full_path = list(reversed(path_so_far))
                paths_checked += 1
                if not check_path_safety(G, H, VERTEX, col, full_path):
                    return {
                        "status": "unsafe_found",
                        "paths_checked": paths_checked,
                        "opt_dist": target_dist,
                    }
            else:
                for p in parents[node]:
                    stack.append((p, path_so_far + [p]))

    return {
        "status": "all_safe",
        "paths_checked": paths_checked,
        "opt_dist": target_dist,
    }


def main() -> None:
    wall0 = time.perf_counter()
    deadline = wall0 + LIMIT_S

    t_gen = time.perf_counter()
    db = generate_triangulations(9)
    gen_s = time.perf_counter() - t_gen
    G = db[9][25]
    name = G.graph.get("name")
    H = G.copy()
    H.remove_node(VERTEX)

    t_enum = time.perf_counter()
    all_cols = enumerate_colourings(G, 5)
    enum_s = time.perf_counter() - t_enum
    fixed = [c for c in all_cols if c.get(VERTEX) == 5]
    n_exact_5 = sum(1 for c in fixed if num_colours(c) == 5)
    written_present = any(_key(c) == _key(WRITTEN) for c in fixed)
    written_proper = is_proper_colouring(G, WRITTEN)

    payload = {
        "graph_name": name,
        "graph_index": 25,
        "vertex": VERTEX,
        "degree": int(G.degree(VERTEX)),
        "n_nodes": G.order(),
        "n_edges": G.size(),
        "limit_s": LIMIT_S,
        "generate_seconds": gen_s,
        "enumerate_seconds": enum_s,
        "n_all_proper_5": len(all_cols),
        "n_c_vertex_5": len(fixed),
        "n_c_vertex_5_using_exactly_5_colours": n_exact_5,
        "written_colouring": _fmt(WRITTEN),
        "written_present": written_present,
        "written_proper": written_proper,
        "stopped_reason": None,
    }
    print(
        f"SETUP name={name} degree={G.degree(VERTEX)} "
        f"c5={len(fixed)} exact5={n_exact_5} "
        f"gen_s={gen_s:.3f} enum_s={enum_s:.3f} "
        f"written_present={written_present}",
        flush=True,
    )

    n_every = 0
    n_opt_plus_1 = 0
    n_longer_none = 0
    n_longer_rejected = 0
    n_some = 0
    n_all_safe = 0
    n_no_target = 0
    n_inconclusive = 0
    n_already_4 = 0
    n_finished = 0
    n_residual = 0
    n_some_by_early_unsafe = 0
    opt_hist: Counter = Counter()
    disagree_every_but_no_opt = 0
    written_bucket = None
    bfs_seconds = 0.0
    longer_seconds = 0.0
    residual_seconds = 0.0

    for col in fixed:
        if time.perf_counter() >= deadline:
            payload["stopped_reason"] = "deadline_before_colouring"
            break

        t_bfs = time.perf_counter()
        univ = find_safe_bfs_path(G, H, VERTEX, col, max_paths=MAX_PATHS)
        bfs_seconds += time.perf_counter() - t_bfs

        reason = univ.get("reason")
        safe_exists = bool(univ.get("safe_path_exists"))
        paths_checked = univ.get("paths_checked")
        bucket = None

        if safe_exists and reason == "already 4-colourable":
            n_all_safe += 1
            n_already_4 += 1
            bucket = "all_shortest_safe"
        elif (not safe_exists) and reason == "exhausted":
            if time.perf_counter() >= deadline:
                payload["stopped_reason"] = "deadline_before_longer"
                break
            dist = opt_dist_of(H, col)
            if dist is None:
                disagree_every_but_no_opt += 1
                n_inconclusive += 1
                bucket = "inconclusive"
            else:
                longer = longer_ok(G, H, col, dist)
                longer_seconds += longer["search_seconds"]
                n_every += 1
                opt_hist[dist] += 1
                if longer["length_is_opt_plus_1"]:
                    n_opt_plus_1 += 1
                elif longer["returned"] and longer.get("is_step_safe") is False:
                    n_longer_rejected += 1
                elif longer["returned"]:
                    n_longer_rejected += 1
                else:
                    n_longer_none += 1
                bucket = "every_shortest_unsafe"
        elif safe_exists:
            witnessed_unsafe = (
                isinstance(paths_checked, int) and paths_checked > 1
            )
            if witnessed_unsafe:
                n_some += 1
                n_some_by_early_unsafe += 1
                bucket = "some_shortest_unsafe"
            else:
                if time.perf_counter() >= deadline:
                    payload["stopped_reason"] = "deadline_before_residual"
                    break
                t_res = time.perf_counter()
                residual = first_unsafe_after_safe_start(G, H, col)
                residual_seconds += time.perf_counter() - t_res
                n_residual += 1
                status = residual["status"]
                if status == "unsafe_found":
                    n_some += 1
                    bucket = "some_shortest_unsafe"
                elif status in ("all_safe", "already_4"):
                    n_all_safe += 1
                    bucket = "all_shortest_safe"
                elif status == "no_target":
                    n_no_target += 1
                    bucket = "no_target"
                else:
                    n_inconclusive += 1
                    bucket = "inconclusive"
        elif reason == "max_paths_reached":
            n_inconclusive += 1
            bucket = "inconclusive"
        elif reason == "no 4-colouring reachable":
            n_no_target += 1
            bucket = "no_target"
        else:
            n_inconclusive += 1
            bucket = "inconclusive"

        n_finished += 1
        if _key(col) == _key(WRITTEN):
            written_bucket = bucket

        if n_finished % 100 == 0:
            elapsed = time.perf_counter() - wall0
            print(
                f"PROGRESS {n_finished}/{len(fixed)} "
                f"every={n_every} opt1={n_opt_plus_1} some={n_some} "
                f"all_safe={n_all_safe} elapsed={elapsed:.1f}",
                flush=True,
            )

    complete = n_finished == len(fixed) and payload["stopped_reason"] is None
    payload.update(
        {
            "n_finished": n_finished,
            "complete": complete,
            "n_every_shortest_path_unsafe": n_every,
            "n_of_those_opt_plus_1_safe": n_opt_plus_1,
            "n_longer_none": n_longer_none,
            "n_longer_returned_rejected_by_is_step": n_longer_rejected,
            "n_some_shortest_unsafe_safe_shortest_exists": n_some,
            "n_some_witnessed_by_find_safe_bfs_path_paths_checked": n_some_by_early_unsafe,
            "n_all_shortest_safe": n_all_safe,
            "n_already_4_colourable_on_H": n_already_4,
            "n_no_4_colouring_reachable": n_no_target,
            "n_inconclusive": n_inconclusive,
            "n_residual_searches": n_residual,
            "n_every_unsafe_but_bfs_reduce_returned_none": disagree_every_but_no_opt,
            "opt_dist_hist_every_unsafe": {
                str(k): opt_hist[k] for k in sorted(opt_hist)
            },
            "written_bucket": written_bucket,
            "find_safe_bfs_seconds": bfs_seconds,
            "longer_seconds": longer_seconds,
            "residual_seconds": residual_seconds,
            "elapsed_seconds": time.perf_counter() - wall0,
        }
    )
    dump(payload)
    print(
        f"SUMMARY complete={complete} finished={n_finished}/{len(fixed)} "
        f"every={n_every} opt_plus_1={n_opt_plus_1} some={n_some} "
        f"all_safe={n_all_safe} inconclusive={n_inconclusive} "
        f"no_target={n_no_target} written={written_bucket} "
        f"elapsed={payload['elapsed_seconds']:.3f}",
        flush=True,
    )


if __name__ == "__main__":
    main()
