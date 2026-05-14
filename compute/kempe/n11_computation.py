"""
n11_computation.py — M3-S1: Scale Engineer — Extend computation to n=11.

Agent 1210, Manager M3, Sub-subagent S1

Strategy:
1. Generate all 1,249 triangulations at n=11
2. Run bulk_distance_to_4col on each
3. Verify max distance ≤ n-4 = 7
4. Report timing and any failures
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(__file__))

from typing import Dict, List
import networkx as nx

from kempe_ops import enumerate_colourings, num_colours
from triangulation_db import generate_triangulations, is_triangulation
from reduction_search import bulk_distance_to_4col


def run_n11_verification() -> Dict:
    """Full n=11 verification: generate triangulations + distance bounds."""

    print("Phase 0: Generating triangulations up to n=11...")
    t0 = time.time()
    db = generate_triangulations(11)
    t_gen = time.time() - t0
    print(f"  Generation time: {t_gen:.1f}s")

    for n in range(4, 12):
        count = len(db[n])
        print(f"  n={n}: {count} triangulations")

    n11_count = len(db[11])
    print(f"\nExpected 1249 at n=11, got {n11_count}")
    assert n11_count == 1249, f"WRONG COUNT: expected 1249, got {n11_count}"

    for i, T in enumerate(db[11]):
        assert is_triangulation(T), f"T_{11}_{i} is not a valid triangulation!"

    print(f"\nPhase 1: Running distance verification on all {n11_count} n=11 triangulations...")
    print("(This may take 15-60 minutes)")

    results = {
        'n': 11,
        'num_triangulations': n11_count,
        'generation_time': t_gen,
        'max_distance_overall': 0,
        'all_reachable': True,
        'distance_histogram_across_graphs': {},
        'max_dist_per_graph': [],
        'failures': [],
        'timing_per_graph': [],
        'total_4col': 0,
        'total_5col': 0,
    }

    for i, T in enumerate(db[11]):
        name = T.graph.get('name', f'T_11_{i}')
        t_start = time.time()

        try:
            result = bulk_distance_to_4col(T, k=5)
            t_elapsed = time.time() - t_start

            d = result['max_distance']
            results['max_dist_per_graph'].append(d)
            results['max_distance_overall'] = max(results['max_distance_overall'], d)
            results['total_4col'] += result['num_4col']
            results['total_5col'] += result['num_5col']
            results['timing_per_graph'].append(t_elapsed)

            if not result['all_reachable']:
                results['all_reachable'] = False
                results['failures'].append({
                    'graph': name,
                    'unreachable': len(result['unreachable']),
                })
                print(f"  *** FAILURE: {name} has unreachable colourings! ***")

            if d > 7:
                results['failures'].append({
                    'graph': name,
                    'max_distance': d,
                    'exceeds_bound': True,
                })
                print(f"  *** FAILURE: {name} has max distance {d} > n-4=7! ***")

            if (i + 1) % 50 == 0 or i == 0:
                avg_t = sum(results['timing_per_graph']) / len(results['timing_per_graph'])
                remaining = (n11_count - i - 1) * avg_t
                print(f"  [{i+1}/{n11_count}] {name}: max_dist={d}, "
                      f"4col={result['num_4col']}, 5col={result['num_5col']}, "
                      f"time={t_elapsed:.1f}s, est_remaining={remaining:.0f}s")

        except Exception as e:
            t_elapsed = time.time() - t_start
            results['failures'].append({
                'graph': name,
                'error': str(e),
            })
            print(f"  *** ERROR on {name}: {e} (after {t_elapsed:.1f}s) ***")

    total_time = sum(results['timing_per_graph'])
    results['total_computation_time'] = total_time

    from collections import Counter
    results['distance_histogram_across_graphs'] = dict(
        Counter(results['max_dist_per_graph']))

    return results


if __name__ == '__main__':
    print("=" * 70)
    print("M3-S1: n=11 Computation")
    print("=" * 70)

    results = run_n11_verification()

    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print(f"Triangulations: {results['num_triangulations']}")
    print(f"Generation time: {results['generation_time']:.1f}s")
    print(f"Total computation time: {results['total_computation_time']:.1f}s")
    print(f"Max distance overall: {results['max_distance_overall']}")
    print(f"Bound n-4 = 7: {'HOLDS' if results['max_distance_overall'] <= 7 else 'VIOLATED'}")
    print(f"All reachable: {results['all_reachable']}")
    print(f"Total 4-colourings: {results['total_4col']}")
    print(f"Total 5-colourings: {results['total_5col']}")
    print(f"Distance histogram: {results['distance_histogram_across_graphs']}")
    print(f"Failures: {len(results['failures'])}")
    for f in results['failures']:
        print(f"  {f}")

    print("\n" + "=" * 70)
    if results['failures']:
        print("*** CRITICAL: FAILURES FOUND — POTENTIAL COUNTEREXAMPLES ***")
    else:
        print("ALL CLEAR: n=11 verification passed")
    print("=" * 70)
