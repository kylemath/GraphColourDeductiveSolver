"""
pattern_analysis.py — M3-S2: Pattern Analyst — Statistical analysis of BFS avoidance.

Agent 1210, Manager M3, Sub-subagent S2

Deep analysis of BFS avoidance data: path length distributions,
merge-prone case frequencies, structural predictors, chain sizes.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from typing import Dict, List, Tuple
from collections import Counter, defaultdict
import networkx as nx

from kempe_ops import (
    Colouring, get_kempe_chain, enumerate_colourings, num_colours,
    canonical_form, colouring_from_canonical,
)
from triangulation_db import generate_triangulations
from reduction_search import bfs_reduce_to_4, bulk_distance_to_4col, _identify_swap
from merge_analysis import analyze_merge_conditions, bfs_path_merge_check


def path_length_distribution(max_n: int = 10) -> Dict:
    """Distribution of BFS path lengths by n and vertex degree."""
    db = generate_triangulations(max_n)
    results = {}

    for n in range(4, max_n + 1):
        dist_hist = Counter()
        by_degree = defaultdict(Counter)

        for T in db[n]:
            result = bulk_distance_to_4col(T, k=5)
            for d, count in result['distance_histogram'].items():
                if d > 0:
                    dist_hist[d] += count

        results[n] = {
            'histogram': dict(sorted(dist_hist.items())),
            'total': sum(dist_hist.values()),
            'mean': (sum(d * c for d, c in dist_hist.items()) /
                     max(1, sum(dist_hist.values()))),
        }
        print(f"n={n}: {dict(sorted(dist_hist.items()))}")

    return results


def merge_prone_frequency(max_n: int = 9) -> Dict:
    """How many merge-prone cases per triangulation and per vertex?"""
    db = generate_triangulations(max_n)
    results = {}

    for n in range(6, max_n + 1):
        graph_stats = []
        for T in db[n]:
            total_mp = 0
            for v in T.nodes():
                if T.degree(v) > 5:
                    continue
                result = bfs_path_merge_check(T, v)
                total_mp += result['multi_chain_cases']
            graph_stats.append({
                'name': T.graph.get('name', '?'),
                'merge_prone': total_mp,
                'min_degree': min(T.degree(v) for v in T.nodes()),
                'num_deg4': sum(1 for v in T.nodes() if T.degree(v) == 4),
                'num_deg5': sum(1 for v in T.nodes() if T.degree(v) == 5),
            })

        results[n] = graph_stats
        total = sum(g['merge_prone'] for g in graph_stats)
        avg = total / max(1, len(graph_stats))
        print(f"n={n}: {len(graph_stats)} graphs, total merge-prone={total}, avg={avg:.1f}")

    return results


def structural_predictors(max_n: int = 9) -> Dict:
    """Which structural properties predict merge rate?"""
    db = generate_triangulations(max_n)
    results = []

    for n in range(6, max_n + 1):
        for T in db[n]:
            from merge_analysis import bulk_merge_analysis
            merge_stats = bulk_merge_analysis(T)

            total_merges = sum(v.get('merges', 0) for v in merge_stats.values())
            total_cases = sum(v.get('total_cases', 0) for v in merge_stats.values())
            merge_rate = total_merges / max(1, total_cases)

            degs = sorted(T.degree(v) for v in T.nodes())
            min_deg = min(degs)
            max_deg = max(degs)
            avg_deg = sum(degs) / len(degs)

            results.append({
                'name': T.graph.get('name', '?'),
                'n': n,
                'min_degree': min_deg,
                'max_degree': max_deg,
                'avg_degree': avg_deg,
                'merge_rate': merge_rate,
                'total_merges': total_merges,
                'total_cases': total_cases,
            })

    return results


def distance_bound_trend(max_n: int = 10) -> Dict:
    """Track how max distance evolves with n. Does n-4 get tighter or looser?"""
    db = generate_triangulations(max_n)
    results = {}

    for n in range(4, max_n + 1):
        max_d = 0
        for T in db[n]:
            result = bulk_distance_to_4col(T, k=5)
            max_d = max(max_d, result['max_distance'])
        bound = n - 4
        gap = bound - max_d
        results[n] = {
            'max_distance': max_d,
            'bound': bound,
            'gap': gap,
            'tight': gap == 0,
        }
        print(f"n={n}: max_dist={max_d}, bound={bound}, gap={gap}, tight={'Yes' if gap == 0 else 'No'}")

    return results


if __name__ == '__main__':
    print("=" * 70)
    print("M3-S2: Pattern Analysis")
    print("=" * 70)

    print("\n--- Phase 1: Path length distribution ---")
    pld = path_length_distribution(9)

    print("\n--- Phase 2: Merge-prone frequency ---")
    mpf = merge_prone_frequency(8)

    print("\n--- Phase 3: Structural predictors ---")
    sp = structural_predictors(8)
    print("\nTop merge rate graphs:")
    for r in sorted(sp, key=lambda x: -x['merge_rate'])[:10]:
        print(f"  {r['name']}: merge_rate={r['merge_rate']:.3f}, "
              f"min_deg={r['min_degree']}, max_deg={r['max_degree']}")

    print("\n--- Phase 4: Distance bound trend ---")
    dbt = distance_bound_trend(10)

    print("\n" + "=" * 70)
    print("DONE: M3-S2 Pattern Analysis Complete")
    print("=" * 70)
