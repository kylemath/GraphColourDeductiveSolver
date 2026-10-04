"""W5: classify proper 5-colourings of T_9_35 with c(6)=5 that lie outside S.

S is exhaustive_details in merge_tolerant_results.json with graph T_9_35
and vertex 6. One colouring from S is a sanity check only.

For each colouring outside S:
- one shortest path from bfs_reduce_to_4, marked unsafe when check_path_safety
  (is_step_unsafe) fails;
- a K1-safe path of length opt_dist+1 only among those, via
  find_safe_nonoptimal_path(..., max_extra=1), accepted only if
  check_path_safety also accepts it;
- every shortest path unsafe, via find_safe_bfs_path, only when a timed
  probe says the full check fits in the remaining part of a 600s cap.
  A safe bfs_reduce_to_4 path already witnesses that not every shortest
  path is unsafe, so find_safe_bfs_path is called only on the unsafe set.

Stops at 600 seconds. Writes partial counts for colourings that finished.
Does not edit docs/navigator. Does not install packages.
"""

from __future__ import annotations

import json
import os
import signal
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "compute", "kempe"))

import counterexample_energy_targeted as cet  # noqa: E402
from kempe_ops import (  # noqa: E402
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

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
MERGE_PATH = os.path.join(
    ROOT,
    "backgroundMaterial/agent1545/coordinator/manager_M1/sub_S1/merge_tolerant_results.json",
)
OUT_PATH = os.path.join(os.path.dirname(__file__), "w5_classify_results.json")

PUBLISHED = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 3, 6: 5, 7: 2, 8: 5}
VERTEX = 6
LIMIT_S = 600.0
PROBE_N = 20
PROBE_CALL_S = 3.0


class CallTimeout(Exception):
    pass


def _on_alarm(signum, frame):
    raise CallTimeout()


def _key(col: dict) -> tuple:
    return tuple(col[i] for i in range(9))


def _fmt(col: dict) -> str:
    return ",".join(f"{i}:{col[i]}" for i in range(9))


def _as_colouring(raw: dict) -> dict:
    return {int(k): int(v) for k, v in raw.items()}


def load_S() -> set:
    with open(MERGE_PATH) as f:
        merge = json.load(f)
    keys = set()
    for entry in merge["exhaustive_details"]:
        if entry.get("graph") == "T_9_35" and entry.get("vertex") == VERTEX:
            keys.add(_key(_as_colouring(entry["colouring"])))
    return keys


def one_path_record(G, H, col) -> dict:
    col_H = {u: col[u] for u in H.nodes()}
    t0 = time.perf_counter()
    bfs_path = bfs_reduce_to_4(H, col_H, k=5)
    bfs_s = time.perf_counter() - t0
    record = {
        "bfs_seconds": bfs_s,
        "colours_on_H": num_colours(col_H),
    }
    if bfs_path is None:
        record["status"] = "no_bfs_path"
        record["opt_dist"] = None
        record["one_shortest_unsafe"] = False
        return record
    opt_dist = len(bfs_path) - 1
    t1 = time.perf_counter()
    safe = check_path_safety(G, H, VERTEX, col, bfs_path)
    record["safety_seconds"] = time.perf_counter() - t1
    record["status"] = "path"
    record["opt_dist"] = opt_dist
    record["one_shortest_unsafe"] = not safe
    record["end_colours"] = num_colours(colouring_from_canonical(H, bfs_path[-1]))
    return record


def longer_record(G, H, col, opt_dist: int) -> dict:
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
            "length": None,
            "is_step_safe": None,
            "end_colours": None,
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


def universal_call(G, H, col) -> dict:
    t0 = time.perf_counter()
    signal.setitimer(signal.ITIMER_REAL, PROBE_CALL_S)
    try:
        result = find_safe_bfs_path(G, H, VERTEX, col)
        signal.setitimer(signal.ITIMER_REAL, 0.0)
    except CallTimeout:
        signal.setitimer(signal.ITIMER_REAL, 0.0)
        return {
            "seconds": time.perf_counter() - t0,
            "status": "timeout",
            "safe_path_exists": None,
            "reason": "timeout",
            "paths_checked": None,
        }
    elapsed = time.perf_counter() - t0
    reason = result.get("reason")
    safe_exists = bool(result.get("safe_path_exists"))
    if safe_exists:
        status = "has_safe_shortest"
    elif reason == "exhausted":
        status = "every_shortest_unsafe"
    elif reason == "max_paths_reached":
        status = "inconclusive_max_paths"
    else:
        status = "other"
    return {
        "seconds": elapsed,
        "status": status,
        "safe_path_exists": safe_exists,
        "reason": reason,
        "paths_checked": result.get("paths_checked"),
        "path_length_nodes": result.get("path_length"),
    }


def dump(payload: dict) -> None:
    with open(OUT_PATH, "w") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")


def main() -> None:
    signal.signal(signal.SIGALRM, _on_alarm)
    wall0 = time.perf_counter()
    deadline = wall0 + LIMIT_S

    S = load_S()
    t_gen = time.perf_counter()
    db = generate_triangulations(9)
    gen_s = time.perf_counter() - t_gen
    G = db[9][35]
    name = G.graph.get("name")
    H = G.copy()
    H.remove_node(VERTEX)

    t_enum = time.perf_counter()
    all_cols = enumerate_colourings(G, 5)
    enum_s = time.perf_counter() - t_enum
    fixed = [c for c in all_cols if c.get(VERTEX) == 5]
    outside = [c for c in fixed if _key(c) not in S]
    in_S = [c for c in fixed if _key(c) in S]

    published_in_S = _key(PUBLISHED) in S
    sanity_col = dict(PUBLISHED)
    sanity = {
        "colouring": _fmt(sanity_col),
        "in_S": published_in_S,
        "proper_on_G": is_proper_colouring(G, sanity_col),
        "c_vertex": sanity_col[VERTEX],
    }
    sanity.update(one_path_record(G, H, sanity_col))
    if sanity.get("one_shortest_unsafe") and sanity.get("opt_dist") is not None:
        sanity["longer"] = longer_record(G, H, sanity_col, sanity["opt_dist"])
    t_univ = time.perf_counter()
    sanity["universal"] = universal_call(G, H, sanity_col)
    sanity["universal_seconds"] = time.perf_counter() - t_univ
    print(
        f"SANITY opt_dist={sanity.get('opt_dist')} "
        f"one_unsafe={sanity.get('one_shortest_unsafe')} "
        f"longer={sanity.get('longer')} universal={sanity.get('universal')}",
        flush=True,
    )

    payload = {
        "graph_name": name,
        "vertex": VERTEX,
        "degree": G.degree(VERTEX),
        "n_nodes": G.order(),
        "n_edges": G.size(),
        "limit_s": LIMIT_S,
        "generate_seconds": gen_s,
        "enumerate_seconds": enum_s,
        "n_all_proper_5": len(all_cols),
        "n_c_vertex_5": len(fixed),
        "n_S_loaded": len(S),
        "n_in_S": len(in_S),
        "n_outside": len(outside),
        "sanity": sanity,
        "n_finished_one_path": 0,
        "stopped_reason": None,
    }
    print(
        f"SETUP name={name} outside={len(outside)} in_S={len(in_S)} "
        f"gen_s={gen_s:.3f} enum_s={enum_s:.3f}",
        flush=True,
    )

    finished = 0
    n_one_unsafe = 0
    n_one_safe = 0
    n_no_bfs = 0
    n_longer_safe = 0
    n_longer_returned_unsafe = 0
    n_longer_none = 0
    n_longer_wrong_length = 0
    opt_dist_hist: Counter = Counter()
    unsafe_indices = []
    one_path_seconds = 0.0
    longer_seconds = 0.0

    for index, col in enumerate(outside):
        if time.perf_counter() >= deadline:
            payload["stopped_reason"] = "deadline_before_one_path"
            break
        rec = one_path_record(G, H, col)
        one_path_seconds += rec["bfs_seconds"] + rec.get("safety_seconds", 0.0)
        if rec["status"] == "no_bfs_path":
            n_no_bfs += 1
        elif rec["one_shortest_unsafe"]:
            if time.perf_counter() >= deadline:
                payload["stopped_reason"] = "deadline_before_longer"
                break
            longer = longer_record(G, H, col, rec["opt_dist"])
            longer_seconds += longer["search_seconds"]
            n_one_unsafe += 1
            unsafe_indices.append(index)
            opt_dist_hist[rec["opt_dist"]] += 1
            if longer["length_is_opt_plus_1"]:
                n_longer_safe += 1
            elif longer["returned"] and longer["is_step_safe"] is False:
                n_longer_returned_unsafe += 1
            elif longer["returned"]:
                n_longer_wrong_length += 1
            else:
                n_longer_none += 1
        else:
            n_one_safe += 1
            opt_dist_hist[rec["opt_dist"]] += 1
        finished += 1
        if finished % 100 == 0:
            elapsed = time.perf_counter() - wall0
            print(
                f"PROGRESS one_path={finished}/{len(outside)} "
                f"unsafe={n_one_unsafe} longer_safe={n_longer_safe} "
                f"elapsed={elapsed:.1f}",
                flush=True,
            )

    one_path_done = finished == len(outside) and payload["stopped_reason"] is None
    payload.update(
        {
            "n_finished_one_path": finished,
            "one_path_complete": one_path_done,
            "n_one_shortest_path_unsafe": n_one_unsafe,
            "n_one_shortest_path_safe": n_one_safe,
            "n_no_bfs_path": n_no_bfs,
            "n_opt_plus_1_safe": n_longer_safe,
            "n_longer_returned_but_is_step_unsafe": n_longer_returned_unsafe,
            "n_longer_returned_wrong_shape": n_longer_wrong_length,
            "n_longer_none": n_longer_none,
            "n_unsafe_seen": len(unsafe_indices),
            "opt_dist_hist": {str(k): opt_dist_hist[k] for k in sorted(opt_dist_hist)},
            "one_path_cpu_seconds": one_path_seconds,
            "longer_cpu_seconds": longer_seconds,
        }
    )
    dump(payload)
    print(
        f"ONE_PATH complete={one_path_done} finished={finished} "
        f"unsafe={n_one_unsafe} safe={n_one_safe} no_bfs={n_no_bfs} "
        f"opt_plus_1={n_longer_safe} none={n_longer_none} "
        f"elapsed={time.perf_counter() - wall0:.3f}",
        flush=True,
    )

    universal = {
        "attempted": False,
        "status": "not_run",
    }
    remaining = deadline - time.perf_counter()
    if not one_path_done:
        universal = {
            "attempted": False,
            "status": "skipped",
            "reason": "one_path pass did not finish before the cap",
        }
    elif n_one_unsafe == 0 and n_no_bfs == 0:
        universal = {
            "attempted": False,
            "status": "complete_by_safe_witness",
            "reason": (
                "every outside colouring has a safe bfs_reduce_to_4 path, "
                "so none has every shortest path unsafe"
            ),
            "n_every_shortest_path_unsafe": 0,
            "n_has_safe_shortest": n_one_safe,
        }
    elif n_one_unsafe == 0 and n_no_bfs > 0:
        universal = {
            "attempted": False,
            "status": "skipped",
            "reason": (
                "no sampled shortest path was unsafe, but some colourings "
                "had no bfs_reduce_to_4 path; the universal count is not "
                "reported for that remainder"
            ),
            "n_no_bfs_path": n_no_bfs,
            "n_has_safe_shortest": n_one_safe,
        }
    else:
        probe_n = min(PROBE_N, n_one_unsafe)
        probe = []
        probe_timeout = False
        print(
            f"PROBE universal n={probe_n} of unsafe={n_one_unsafe} remaining_s={remaining:.1f}",
            flush=True,
        )
        for j in range(probe_n):
            if time.perf_counter() >= deadline:
                universal = {
                    "attempted": True,
                    "status": "skipped",
                    "reason": "deadline reached before the universal probe finished",
                    "probe_finished": j,
                }
                probe_timeout = True
                break
            rec = universal_call(G, H, outside[unsafe_indices[j]])
            probe.append(rec)
            print(
                f"PROBE j={j} status={rec['status']} paths={rec['paths_checked']} "
                f"s={rec['seconds']:.3f}",
                flush=True,
            )
            if rec["status"] == "timeout":
                probe_timeout = True
                break
        probe_elapsed = sum(p["seconds"] for p in probe)
        mean = probe_elapsed / len(probe) if probe else None
        rest_n = n_one_unsafe - len(probe)
        projected_rest = (mean * rest_n) if mean is not None else None
        projected_all = (mean * n_one_unsafe) if mean is not None else None
        remaining = deadline - time.perf_counter()
        universal = {
            "attempted": True,
            "probe_n": len(probe),
            "probe_seconds": probe_elapsed,
            "probe_mean_seconds": mean,
            "probe_max_seconds": max((p["seconds"] for p in probe), default=None),
            "projected_seconds_on_unsafe_set": projected_all,
            "projected_seconds_remaining_calls": projected_rest,
            "remaining_seconds_at_decision": remaining,
            "probe_statuses": dict(Counter(p["status"] for p in probe)),
            "probe_paths_checked": [p["paths_checked"] for p in probe],
        }
        run_rest = (
            not probe_timeout
            and projected_rest is not None
            and projected_rest <= remaining
            and len(probe) == probe_n
        )
        if not run_rest:
            universal["status"] = "skipped"
            if probe_timeout:
                universal["reason"] = (
                    "a find_safe_bfs_path call hit the "
                    f"{PROBE_CALL_S:.0f}s per-call cap, or the probe itself "
                    "ran out of time; testing every shortest path on the "
                    "unsafe set was not completed"
                )
            else:
                universal["reason"] = (
                    "projected time for find_safe_bfs_path on every colouring "
                    "with an unsafe bfs_reduce_to_4 path exceeds the time "
                    "left inside the ten-minute cap"
                )
        else:
            counts = Counter(p["status"] for p in probe)
            univ_seconds = probe_elapsed
            for j in range(probe_n, n_one_unsafe):
                if time.perf_counter() >= deadline:
                    universal["status"] = "incomplete"
                    universal["reason"] = (
                        "rate during the full pass reached the cap; "
                        "the universal count is not reported"
                    )
                    universal["n_unsafe_finished"] = j
                    break
                rec = universal_call(G, H, outside[unsafe_indices[j]])
                univ_seconds += rec["seconds"]
                counts[rec["status"]] += 1
                if rec["status"] == "timeout":
                    universal["status"] = "incomplete"
                    universal["reason"] = (
                        "a find_safe_bfs_path call timed out during the full pass; "
                        "the universal count is not reported"
                    )
                    universal["n_unsafe_finished"] = j
                    break
            else:
                universal["status"] = "complete"
                universal["n_every_shortest_path_unsafe"] = counts["every_shortest_unsafe"]
                universal["n_has_safe_shortest_among_unsafe_sample"] = counts[
                    "has_safe_shortest"
                ]
                universal["n_inconclusive_max_paths"] = counts["inconclusive_max_paths"]
                universal["n_other"] = counts["other"]
                universal["n_unsafe_finished"] = n_one_unsafe
                # Colourings whose sampled shortest path is safe are witnesses
                # that not every shortest path is unsafe.
                universal["n_excluded_by_safe_bfs_path"] = n_one_safe
            universal["status_counts"] = dict(counts)
            universal["universal_seconds"] = univ_seconds

    payload["universal"] = universal
    payload["elapsed_seconds"] = time.perf_counter() - wall0
    payload["n_colourings_finished"] = payload["n_finished_one_path"]
    dump(payload)
    print(
        f"SUMMARY elapsed={payload['elapsed_seconds']:.3f} "
        f"one_path_finished={payload['n_finished_one_path']} "
        f"one_unsafe={payload['n_one_shortest_path_unsafe']} "
        f"opt_plus_1={payload['n_opt_plus_1_safe']} "
        f"universal_status={universal.get('status')}",
        flush=True,
    )


if __name__ == "__main__":
    main()
