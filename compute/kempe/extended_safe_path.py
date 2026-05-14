"""
extended_safe_path.py — Agent 1545-M2-S2: Extension to n=10, 11, 12.

Extends safe path analysis to larger triangulations.

Key questions:
  1. Does the counterexample rate (0.03% at n=9) grow or shrink with n?
  2. Does the maximum detour cost grow with n? If bounded, the proof works.
  3. Are there cases where NO safe path exists? (Kills the approach entirely)

Known triangulation counts (OEIS A000109):
  n=10: 233, n=11: 1,249, n=12: 7,595
"""

import sys
import os
import time
import json
from typing import Dict, List, Optional
from collections import Counter
import networkx as nx

sys.path.insert(0, os.path.dirname(__file__))

from kempe_ops import (
    Colouring, CanonicalColouring,
    get_kempe_chain, get_all_kempe_chains, kempe_swap,
    enumerate_colourings, num_colours,
    canonical_form, colouring_from_canonical,
)
from triangulation_db import generate_triangulations
from reduction_search import bfs_reduce_to_4, _identify_swap
from safe_path_search import (
    safe_bfs_to_4, is_merge_prone, check_path_safety, safe_kempe_neighbours,
)


def extended_safe_path_analysis(
    target_n: int,
    time_limit_s: float = 7200,
    verbose: bool = True
) -> Dict:
    """
    Run safe path analysis at n = target_n with per-graph timing and checkpointing.

    Processes each triangulation individually so progress is visible.
    Aborts cleanly if time_limit_s is exceeded.
    """
    if verbose:
        print(f"\n{'='*70}")
        print(f"Agent 1545-M2-S2: Extended Safe Path Analysis at n = {target_n}")
        print(f"{'='*70}")

    t_start = time.time()
    db = generate_triangulations(target_n)
    triangulations = db[target_n]
    t_gen = time.time() - t_start

    if verbose:
        print(f"Generated {len(triangulations)} triangulations in {t_gen:.1f}s")

    results = {
        'n': target_n,
        'num_graphs': len(triangulations),
        'graphs_completed': 0,
        'generation_time_s': round(t_gen, 1),
        'total_colourings_tested': 0,
        'total_merge_prone': 0,
        'safe_at_optimal': 0,
        'safe_alt_at_optimal': 0,
        'safe_nonoptimal': 0,
        'no_safe_path': 0,
        'max_detour_cost': 0,
        'detour_cost_histogram': Counter(),
        'true_counterexamples': [],
        'no_safe_path_cases': [],
        'per_graph_timing': [],
        'aborted': False,
    }

    for idx, T in enumerate(triangulations):
        if time.time() - t_start > time_limit_s:
            results['aborted'] = True
            if verbose:
                print(f"\n*** TIME LIMIT ({time_limit_s}s) REACHED at graph {idx}/{len(triangulations)} ***")
            break

        name = T.graph.get('name', f'T_{target_n}_{idx}')
        t_graph = time.time()
        graph_mp = 0
        graph_safe_opt = 0
        graph_mixed = 0
        graph_detour = 0
        graph_nosafe = 0

        for v in sorted(T.nodes()):
            deg = T.degree(v)
            if deg > 5:
                continue

            H = T.copy()
            H.remove_node(v)

            all_cols = enumerate_colourings(T, 5)
            v5_cols = [c for c in all_cols if c[v] == 5 and num_colours(c) == 5]
            results['total_colourings_tested'] += len(v5_cols)

            for col in v5_cols:
                col_H = {u: col[u] for u in H.nodes()}

                if not is_merge_prone(T, H, v, col_H):
                    continue

                results['total_merge_prone'] += 1
                graph_mp += 1

                path_opt = bfs_reduce_to_4(H, col_H, k=5)
                if path_opt is None or len(path_opt) <= 1:
                    results['safe_at_optimal'] += 1
                    graph_safe_opt += 1
                    results['detour_cost_histogram'][0] += 1
                    continue

                d_opt = len(path_opt) - 1

                if check_path_safety(T, H, v, col, path_opt):
                    results['safe_at_optimal'] += 1
                    graph_safe_opt += 1
                    results['detour_cost_histogram'][0] += 1
                    continue

                d_safe, nodes_explored = safe_bfs_to_4(T, H, v, col_H, k=5)

                if d_safe is None:
                    results['no_safe_path'] += 1
                    graph_nosafe += 1
                    results['no_safe_path_cases'].append({
                        'graph': name, 'vertex': v, 'degree': deg,
                        'd_opt': d_opt, 'nodes_explored': nodes_explored,
                    })
                    if verbose:
                        print(f"\n*** KILL CRITERION: NO SAFE PATH at {name}, "
                              f"v={v}, d_opt={d_opt}, explored={nodes_explored} ***")
                elif d_safe == d_opt:
                    results['safe_alt_at_optimal'] += 1
                    graph_mixed += 1
                    results['detour_cost_histogram'][0] += 1
                else:
                    detour = d_safe - d_opt
                    results['safe_nonoptimal'] += 1
                    graph_detour += 1
                    results['detour_cost_histogram'][detour] += 1
                    results['max_detour_cost'] = max(
                        results['max_detour_cost'], detour)
                    results['true_counterexamples'].append({
                        'graph': name, 'vertex': v, 'degree': deg,
                        'd_opt': d_opt, 'd_safe': d_safe,
                        'detour_cost': detour,
                    })

        t_graph_elapsed = time.time() - t_graph
        results['per_graph_timing'].append(t_graph_elapsed)
        results['graphs_completed'] = idx + 1

        if verbose and ((idx + 1) % max(1, len(triangulations) // 30) == 0
                        or idx == 0 or graph_nosafe > 0 or graph_detour > 0):
            elapsed = time.time() - t_start
            avg_t = sum(results['per_graph_timing']) / len(results['per_graph_timing'])
            remaining = (len(triangulations) - idx - 1) * avg_t
            print(f"  [{idx+1}/{len(triangulations)}] {name}: "
                  f"mp={graph_mp}, safe={graph_safe_opt}, mixed={graph_mixed}, "
                  f"detour={graph_detour}, nosafe={graph_nosafe} "
                  f"({t_graph_elapsed:.1f}s this graph, "
                  f"{elapsed:.0f}s total, ~{remaining:.0f}s remaining)")

    results['total_time_s'] = round(time.time() - t_start, 1)
    results['detour_cost_histogram'] = dict(results['detour_cost_histogram'])
    del results['per_graph_timing']

    if verbose:
        _print_extended_results(results)

    return results


def _print_extended_results(results: Dict) -> None:
    n = results['n']
    print(f"\n{'='*70}")
    print(f"EXTENDED SAFE PATH RESULTS: n = {n}")
    print(f"{'='*70}")
    print(f"  Graphs completed: {results['graphs_completed']}/{results['num_graphs']}")
    if results['aborted']:
        print(f"  *** COMPUTATION ABORTED (time limit) ***")
    print(f"  Colourings tested: {results['total_colourings_tested']}")
    print(f"  Merge-prone cases: {results['total_merge_prone']}")
    print(f"  Safe at optimal: {results['safe_at_optimal']}")
    print(f"  Safe alt at optimal (mixed): {results['safe_alt_at_optimal']}")
    print(f"  Safe non-optimal (detour): {results['safe_nonoptimal']}")
    print(f"  NO safe path (KILL): {results['no_safe_path']}")
    print(f"  Max detour cost: {results['max_detour_cost']}")
    print(f"  Detour cost histogram: {results['detour_cost_histogram']}")
    print(f"  Computation time: {results['total_time_s']}s")

    if results['total_merge_prone'] > 0:
        ce_rate = results['safe_nonoptimal'] / results['total_merge_prone'] * 100
        print(f"  CE rate (need detour): {ce_rate:.4f}%")

    total_safe = (results['safe_at_optimal'] + results['safe_alt_at_optimal']
                  + results['safe_nonoptimal'])
    if results['total_merge_prone'] > 0:
        safe_rate = total_safe / results['total_merge_prone'] * 100
        print(f"  Safe path existence rate: {total_safe}/{results['total_merge_prone']} "
              f"({safe_rate:.4f}%)")

    if results['no_safe_path'] > 0:
        print(f"\n*** KILL CRITERION: {len(results['no_safe_path_cases'])} cases ***")
        for case in results['no_safe_path_cases'][:5]:
            print(f"  {case}")
    elif results['aborted']:
        print(f"\n  Conjecture 5.5' holds for tested graphs (computation incomplete)")
    else:
        print(f"\n  *** Conjecture 5.5' HOLDS at n={n} ***")


if __name__ == '__main__':
    print("=" * 70)
    print("Agent 1545-M2-S2: Extended Safe Path Analysis (n=10, 11, 12)")
    print("=" * 70)

    all_results = {}

    for n in [10, 11, 12]:
        print(f"\n{'#'*70}")
        print(f"# Starting n={n}")
        print(f"{'#'*70}")

        time_limits = {10: 3600, 11: 7200, 12: 14400}
        try:
            r = extended_safe_path_analysis(n, time_limit_s=time_limits.get(n, 7200))
            all_results[n] = r
        except Exception as e:
            print(f"\n*** ERROR at n={n}: {e} ***")
            import traceback
            traceback.print_exc()
            all_results[n] = {'error': str(e)}
            break

        if r.get('no_safe_path', 0) > 0:
            print(f"\n*** KILL CRITERION AT n={n} — STOPPING ***")
            break

        if r.get('total_time_s', 0) > 3600:
            print(f"\nn={n} took {r['total_time_s']:.0f}s (>1h). Skipping larger n.")
            break

    results_path = os.path.join(
        os.path.dirname(__file__), '..', '..', 'backgroundMaterial',
        'agent1545', 'coordinator', 'manager_M2', 'sub_S2',
        'extended_results.json')
    os.makedirs(os.path.dirname(results_path), exist_ok=True)
    with open(results_path, 'w') as f:
        json.dump({str(n): r for n, r in all_results.items()}, f, indent=2, default=str)
    print(f"\nResults saved to {results_path}")

    print("\n" + "=" * 70)
    print("TREND ANALYSIS")
    print("=" * 70)
    print(f"{'n':>4} {'graphs':>7} {'merge_prone':>12} {'detour_CEs':>10} "
          f"{'max_detour':>10} {'no_safe':>8} {'CE_rate':>10} {'time':>8}")
    print("-" * 75)
    for n, r in sorted(all_results.items()):
        if 'error' in r:
            print(f"  n={n}: ERROR — {r['error']}")
            continue
        ce_rate = (r['safe_nonoptimal'] / max(1, r['total_merge_prone']) * 100
                   if r['total_merge_prone'] > 0 else 0)
        print(f"{n:>4} {r['num_graphs']:>7} {r['total_merge_prone']:>12} "
              f"{r['safe_nonoptimal']:>10} {r['max_detour_cost']:>10} "
              f"{r['no_safe_path']:>8} {ce_rate:>9.4f}% {r['total_time_s']:>7.0f}s")
