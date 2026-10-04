"""W3: find_safe_nonoptimal_path on every stored colouring of T_9_35 at vertex 6.

Stops after 600 seconds and reports how many colourings finished.
Does not edit docs/navigator. Does not install packages.
"""

from __future__ import annotations

import json
import os
import signal
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "compute", "kempe"))

import counterexample_energy_targeted as cet  # noqa: E402
from kempe_ops import colouring_from_canonical, is_proper_colouring, num_colours  # noqa: E402
from reduction_search import _identify_swap, bfs_reduce_to_4  # noqa: E402
from triangulation_db import generate_triangulations  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
MERGE_PATH = os.path.join(
    ROOT,
    "backgroundMaterial/agent1545/coordinator/manager_M1/sub_S1/merge_tolerant_results.json",
)
DETAILS_PATH = os.path.join(
    ROOT,
    "backgroundMaterial/agent1520/coordinator/manager_M1/sub_S3/counterexample_details.json",
)
OUT_PATH = os.path.join(os.path.dirname(__file__), "w3_batch_results.json")

PUBLISHED = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 3, 6: 5, 7: 2, 8: 5}
LIMIT_S = 600.0
VERTEX = 6


class SearchTimeout(Exception):
    pass


def _on_alarm(signum, frame):
    raise SearchTimeout()


def _as_colouring(raw: dict) -> dict:
    return {int(k): int(v) for k, v in raw.items()}


def _key(col: dict) -> tuple:
    return tuple(col[i] for i in range(9))


def _fmt(col: dict) -> str:
    return ",".join(f"{i}:{col[i]}" for i in range(9))


def load_colourings() -> dict:
    with open(MERGE_PATH) as f:
        merge = json.load(f)
    with open(DETAILS_PATH) as f:
        details = json.load(f)

    exhaustive = []
    for entry in merge["exhaustive_details"]:
        if entry.get("graph") == "T_9_35" and entry.get("vertex") == VERTEX:
            exhaustive.append(_as_colouring(entry["colouring"]))

    ce = []
    for entry in merge["ce_details"]:
        if entry.get("graph") == "T_9_35" and entry.get("vertex") == VERTEX:
            ce.append(_as_colouring(entry["colouring"]))

    degree4 = []
    for entry in details:
        if entry.get("vertex") == VERTEX and entry.get("degree") == 4:
            degree4.append(_as_colouring(entry["colouring"]))

    ordered = []
    seen = set()
    sources = {"exhaustive_details": 0, "ce_details": 0, "counterexample_details_deg4": 0}
    added_from = []

    def add(col: dict, source: str) -> None:
        k = _key(col)
        if k in seen:
            return
        seen.add(k)
        ordered.append(col)
        sources[source] += 1
        added_from.append(source)

    for col in exhaustive:
        add(col, "exhaustive_details")
    for col in ce:
        add(col, "ce_details")
    for col in degree4:
        add(col, "counterexample_details_deg4")

    return {
        "n_exhaustive_entries": len(exhaustive),
        "n_ce_entries": len(ce),
        "n_degree4_entries": len(degree4),
        "n_unique": len(ordered),
        "first_seen_in": sources,
        "colourings": ordered,
        "added_from": added_from,
    }


def describe_steps(H, path) -> list:
    steps = []
    for i in range(len(path) - 1):
        cur = colouring_from_canonical(H, path[i])
        nxt = colouring_from_canonical(H, path[i + 1])
        a, b = _identify_swap(H, cur, nxt)
        swapped = sorted(u for u in H.nodes() if cur[u] != nxt[u])
        steps.append({"pair": [a, b], "vertices": swapped})
    return steps


def main() -> None:
    signal.signal(signal.SIGALRM, _on_alarm)
    t0 = time.perf_counter()
    loaded = load_colourings()
    load_s = time.perf_counter() - t0

    t_gen = time.perf_counter()
    db = generate_triangulations(9)
    gen_s = time.perf_counter() - t_gen
    T = db[9][35]
    name = T.graph.get("name", "")
    H = T.copy()
    H.remove_node(VERTEX)

    deadline = t0 + LIMIT_S
    finished = []
    stopped_reason = None
    n_attempted_unfinished = 0

    print(
        f"unique={loaded['n_unique']} exhaustive_entries={loaded['n_exhaustive_entries']} "
        f"ce_entries={loaded['n_ce_entries']} degree4_entries={loaded['n_degree4_entries']} "
        f"graph_name={name} degree={T.degree(VERTEX)}",
        flush=True,
    )

    for index, col in enumerate(loaded["colourings"]):
        now = time.perf_counter()
        if now >= deadline:
            stopped_reason = "deadline_before_colouring"
            break
        remaining = deadline - now
        signal.setitimer(signal.ITIMER_REAL, remaining)
        col_H = {u: col[u] for u in H.nodes()}
        record = {
            "index": index,
            "colouring": _fmt(col),
            "source": loaded["added_from"][index],
            "is_published": col == PUBLISHED,
            "proper_on_T": is_proper_colouring(T, col),
            "proper_on_H": is_proper_colouring(H, col_H),
            "colours_on_H": num_colours(col_H),
        }
        t_item = time.perf_counter()
        try:
            bfs_path = bfs_reduce_to_4(H, col_H, k=5)
            record["bfs_seconds"] = time.perf_counter() - t_item
            if bfs_path is None:
                record["opt_dist"] = None
                record["status"] = "no_bfs_path"
                record["returned"] = None
            else:
                opt_dist = len(bfs_path) - 1
                record["opt_dist"] = opt_dist
                t_search = time.perf_counter()
                found = cet.find_safe_nonoptimal_path(
                    T, H, VERTEX, col, col_H, opt_dist, max_extra=3
                )
                record["search_seconds"] = time.perf_counter() - t_search
                if found is None:
                    record["status"] = "none"
                    record["returned"] = None
                    record["path_length"] = None
                else:
                    length = len(found) - 1
                    record["status"] = "path"
                    record["returned"] = "path"
                    record["path_length"] = length
                    record["longer_than_bfs"] = length > opt_dist
                    record["end_colours"] = num_colours(colouring_from_canonical(H, found[-1]))
                    record["steps"] = describe_steps(H, found)
            record["item_seconds"] = time.perf_counter() - t_item
            finished.append(record)
            print(
                f"done index={index} status={record['status']} "
                f"opt_dist={record.get('opt_dist')} length={record.get('path_length')} "
                f"item_s={record['item_seconds']:.3f} colouring={record['colouring']}",
                flush=True,
            )
        except SearchTimeout:
            signal.setitimer(signal.ITIMER_REAL, 0.0)
            n_attempted_unfinished = 1
            stopped_reason = "deadline_during_colouring"
            record["status"] = "unfinished"
            record["item_seconds"] = time.perf_counter() - t_item
            print(
                f"timeout during index={index} after {record['item_seconds']:.3f}s "
                f"colouring={record['colouring']}",
                flush=True,
            )
            break
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0.0)

    elapsed = time.perf_counter() - t0
    n_path = sum(1 for r in finished if r["status"] == "path")
    n_none = sum(1 for r in finished if r["status"] == "none")
    n_no_bfs = sum(1 for r in finished if r["status"] == "no_bfs_path")
    lengths = [r["path_length"] for r in finished if r["status"] == "path"]
    longer = [r["longer_than_bfs"] for r in finished if r["status"] == "path"]

    payload = {
        "graph_name": name,
        "vertex": VERTEX,
        "degree": T.degree(VERTEX),
        "max_extra": 3,
        "limit_s": LIMIT_S,
        "load_seconds": load_s,
        "generate_seconds": gen_s,
        "elapsed_seconds": elapsed,
        "n_exhaustive_entries": loaded["n_exhaustive_entries"],
        "n_ce_entries": loaded["n_ce_entries"],
        "n_degree4_entries": loaded["n_degree4_entries"],
        "n_unique": loaded["n_unique"],
        "first_seen_in": loaded["first_seen_in"],
        "n_ran": len(finished),
        "n_path": n_path,
        "n_none": n_none,
        "n_no_bfs_path": n_no_bfs,
        "n_unfinished_attempt": n_attempted_unfinished,
        "stopped_reason": stopped_reason,
        "lengths": lengths,
        "all_found_longer_than_bfs": all(longer) if longer else None,
        "results": finished,
    }
    with open(OUT_PATH, "w") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")
    print(
        f"SUMMARY ran={len(finished)} path={n_path} none={n_none} "
        f"no_bfs={n_no_bfs} unfinished_attempt={n_attempted_unfinished} "
        f"elapsed={elapsed:.3f} stopped={stopped_reason}",
        flush=True,
    )


if __name__ == "__main__":
    main()
