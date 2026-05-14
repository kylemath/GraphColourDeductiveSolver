"""
n9_merge_investigation.py — Investigate the 539 BFS merges found at n=9.

Agent 1419, Manager M1 — CRITICAL INVESTIGATION

For each case where the first BFS path uses an unsafe swap at n=9,
check: does there exist an ALTERNATIVE BFS-optimal path that is safe?

This determines whether the existential conjecture holds at n=9.
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(__file__))

from typing import Dict, List, Set, Tuple, Optional, FrozenSet
from collections import Counter, deque
import networkx as nx

from kempe_ops import (
    Colouring, CanonicalColouring,
    get_kempe_chain, get_all_kempe_chains, kempe_swap,
    enumerate_colourings, num_colours,
    canonical_form, colouring_from_canonical, all_kempe_neighbours,
)
from triangulation_db import generate_triangulations
from reduction_search import bfs_reduce_to_4, _identify_swap
from merge_analysis import bfs_path_merge_check
from all_paths_analysis import bfs_all_optimal_paths, classify_path_safety


def investigate_n9_merges() -> Dict:
    """
    For each (graph, v) pair at n=9 where bfs_path_merge_check finds merges,
    enumerate ALL optimal paths and check if any are safe.
    """
    db = generate_triangulations(9)
    triangulations = db[9]

    results = {
        'problematic_graphs': [],
        'total_merge_cases_checked': 0,
        'has_safe_alternative': 0,
        'no_safe_alternative': 0,
        'counterexamples': [],
    }

    for idx, T in enumerate(triangulations):
        name = T.graph.get('name', f'T_9_{idx}')

        for v in sorted(T.nodes()):
            deg = T.degree(v)
            if deg > 5:
                continue

            result = bfs_path_merge_check(T, v)
            if result['merges'] == 0:
                continue

            print(f"\nInvestigating {name}, v={v} (deg={deg}): "
                  f"{result['merges']} merges in first BFS path")

            H = T.copy()
            H.remove_node(v)

            all_cols = enumerate_colourings(T, 5)
            v5_cols = [c for c in all_cols if c[v] == 5 and num_colours(c) == 5]

            graph_has_counterexample = False

            for col in v5_cols:
                col_H = {u: col[u] for u in H.nodes()}

                is_merge_prone = False
                for a_colour in range(1, 5):
                    nbrs_in = [u for u in T.neighbors(v)
                               if u in H.nodes() and col_H[u] in (a_colour, 5)]
                    if len(nbrs_in) < 2:
                        continue
                    chain_set = set()
                    for u in nbrs_in:
                        chain_set.add(get_kempe_chain(H, col_H, u, a_colour, 5))
                    if len(chain_set) >= 2:
                        is_merge_prone = True
                        break

                if not is_merge_prone:
                    continue

                first_path = bfs_reduce_to_4(H, col_H, k=5)
                if first_path is None or len(first_path) <= 1:
                    continue

                first_class = classify_path_safety(T, H, v, col, first_path)
                if first_class['path_is_safe']:
                    continue

                results['total_merge_cases_checked'] += 1

                opt_dist, all_opt_paths = bfs_all_optimal_paths(H, col_H, k=5)
                if not all_opt_paths:
                    continue

                safe_count = 0
                for p in all_opt_paths:
                    c = classify_path_safety(T, H, v, col, p)
                    if c['path_is_safe']:
                        safe_count += 1

                if safe_count > 0:
                    results['has_safe_alternative'] += 1
                else:
                    results['no_safe_alternative'] += 1
                    graph_has_counterexample = True
                    ce = {
                        'graph': name,
                        'vertex': v,
                        'degree': deg,
                        'colouring': canonical_form(T, col),
                        'opt_dist': opt_dist,
                        'total_paths': len(all_opt_paths),
                        'safe_paths': 0,
                    }
                    results['counterexamples'].append(ce)
                    print(f"  *** NO SAFE PATH: {name} v={v}, "
                          f"{len(all_opt_paths)} paths, all unsafe")

            if graph_has_counterexample:
                results['problematic_graphs'].append(name)

        if (idx + 1) % 10 == 0:
            print(f"\n  Progress: [{idx+1}/50], "
                  f"checked={results['total_merge_cases_checked']}, "
                  f"safe_alt={results['has_safe_alternative']}, "
                  f"no_safe={results['no_safe_alternative']}")

    return results


if __name__ == '__main__':
    print("=" * 70)
    print("N=9 MERGE INVESTIGATION — Existential Conjecture Test")
    print("Agent 1419, Manager M1 — CRITICAL")
    print("=" * 70)

    t0 = time.time()
    results = investigate_n9_merges()
    elapsed = time.time() - t0

    print("\n" + "=" * 70)
    print(f"INVESTIGATION RESULTS (completed in {elapsed:.1f}s)")
    print("=" * 70)
    print(f"Cases where first BFS path was unsafe: {results['total_merge_cases_checked']}")
    print(f"Has safe alternative path: {results['has_safe_alternative']}")
    print(f"NO safe alternative (TRUE counterexample): {results['no_safe_alternative']}")

    if results['no_safe_alternative'] > 0:
        print(f"\n*** HARD KILL: {results['no_safe_alternative']} TRUE COUNTEREXAMPLES ***")
        print("The existential BFS Avoidance conjecture FAILS at n=9.")
        for ce in results['counterexamples'][:10]:
            print(f"  {ce['graph']}: v={ce['vertex']} (deg={ce['degree']}), "
                  f"dist={ce['opt_dist']}, {ce['total_paths']} paths all unsafe")
    else:
        print("\n*** EXISTENTIAL CONJECTURE HOLDS AT n=9 ***")
        print("Every merge-prone case has at least one safe optimal path.")
    print("=" * 70)
