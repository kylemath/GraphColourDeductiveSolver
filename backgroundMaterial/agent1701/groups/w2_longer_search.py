"""W2: one call of find_safe_nonoptimal_path on the given colouring of T_9_35.

Stops after 600 seconds and reports the elapsed time. Does not edit docs/navigator.
"""

from __future__ import annotations

import os
import signal
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "compute", "kempe"))

import counterexample_energy_targeted as cet  # noqa: E402
from all_paths_analysis import classify_path_safety  # noqa: E402
from kempe_ops import (  # noqa: E402
    canonical_form,
    colouring_from_canonical,
    is_proper_colouring,
    num_colours,
)
from reduction_search import _identify_swap  # noqa: E402
from triangulation_db import generate_triangulations  # noqa: E402
from verify_counterexamples import is_step_unsafe  # noqa: E402

COLOURING = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 3, 6: 5, 7: 2, 8: 5}
OPT_DIST = 2
MAX_EXTRA = 3
LIMIT_S = 600

_expansions = {"n": 0}
_orig_neighbours = cet.all_kempe_neighbours


def _counted_neighbours(G, colouring, k):
    _expansions["n"] += 1
    n = _expansions["n"]
    if n % 2000 == 0:
        print(f"expansions={n}", flush=True)
    return _orig_neighbours(G, colouring, k)


cet.all_kempe_neighbours = _counted_neighbours


class SearchTimeout(Exception):
    pass


def _on_alarm(signum, frame):
    raise SearchTimeout()


def describe_path(T, H, v, col, path):
    cls = classify_path_safety(T, H, v, col, path)
    col_G = dict(col)
    steps = []
    for i in range(len(path) - 1):
        cur_H = colouring_from_canonical(H, path[i])
        nxt_H = colouring_from_canonical(H, path[i + 1])
        a, b = _identify_swap(H, cur_H, nxt_H)
        swapped = sorted(u for u in H.nodes() if cur_H[u] != nxt_H[u])
        unsafe = is_step_unsafe(T, H, v, col_G, cur_H, nxt_H)
        steps.append(
            {
                "step": i,
                "pair": (a, b),
                "vertices": swapped,
                "is_step_unsafe": unsafe,
                "classify_unsafe": cls["steps"][i]["is_unsafe"],
            }
        )
        if swapped and a is not None and b is not None:
            from kempe_ops import kempe_swap

            col_G = kempe_swap(col_G, frozenset(swapped), a, b)
    end = colouring_from_canonical(H, path[-1])
    return {
        "length": len(path) - 1,
        "num_colours_end": num_colours(end),
        "classify_path_is_safe": cls["path_is_safe"],
        "classify_num_unsafe": cls["num_unsafe_steps"],
        "steps": steps,
        "colourings": [list(canon) for canon in path],
    }


def main() -> None:
    t_gen = time.perf_counter()
    db = generate_triangulations(9)
    gen_s = time.perf_counter() - t_gen
    T = db[9][35]
    name = T.graph.get("name", "T_9_35")
    v = 6
    H = T.copy()
    H.remove_node(v)
    col = dict(COLOURING)
    col_H = {u: col[u] for u in H.nodes()}

    print(f"graph={name} index=35", flush=True)
    print(f"degree={T.degree(v)} neighbours={sorted(T.neighbors(v))}", flush=True)
    print(f"proper_G={is_proper_colouring(T, col)} colours_G={num_colours(col)}", flush=True)
    print(
        f"proper_H={is_proper_colouring(H, col_H)} colours_H={num_colours(col_H)}",
        flush=True,
    )
    print(f"start_canon={canonical_form(H, col_H)}", flush=True)
    print(f"generate_s={gen_s:.3f}", flush=True)
    print(f"opt_dist={OPT_DIST} max_extra={MAX_EXTRA} max_dist={OPT_DIST + MAX_EXTRA}", flush=True)

    signal.signal(signal.SIGALRM, _on_alarm)
    signal.alarm(LIMIT_S)
    t0 = time.perf_counter()
    try:
        path = cet.find_safe_nonoptimal_path(
            T, H, v, col, col_H, OPT_DIST, max_extra=MAX_EXTRA
        )
        signal.alarm(0)
        elapsed = time.perf_counter() - t0
        print(f"elapsed_s={elapsed:.3f}", flush=True)
        print(f"expansions={_expansions['n']}", flush=True)
        print(f"found={path is not None}", flush=True)
        if path is None:
            print(f"distance_bound={OPT_DIST + MAX_EXTRA}", flush=True)
            print("RESULT none", flush=True)
            return
        info = describe_path(T, H, v, col, path)
        print(f"length={info['length']}", flush=True)
        print(f"num_colours_end={info['num_colours_end']}", flush=True)
        print(f"classify_path_is_safe={info['classify_path_is_safe']}", flush=True)
        print(f"classify_num_unsafe={info['classify_num_unsafe']}", flush=True)
        for step in info["steps"]:
            print(
                f"step={step['step']} pair={step['pair']} vertices={step['vertices']} "
                f"is_step_unsafe={step['is_step_unsafe']} "
                f"classify_unsafe={step['classify_unsafe']}",
                flush=True,
            )
        print(f"colourings={info['colourings']}", flush=True)
        print("RESULT found", flush=True)
    except SearchTimeout:
        elapsed = time.perf_counter() - t0
        print(f"elapsed_s={elapsed:.3f}", flush=True)
        print(f"expansions={_expansions['n']}", flush=True)
        print("RESULT timeout", flush=True)


if __name__ == "__main__":
    main()
