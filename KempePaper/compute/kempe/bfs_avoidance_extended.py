"""
bfs_avoidance_extended.py — M1-S1: Extended BFS avoidance tests at n=9,10.

Agent 1419, Manager M1, Sub-subagent S1

Runs bfs_path_merge_check() for ALL degree-≤5 vertices across all
triangulations at n=9 (50 graphs) and n=10 (233 graphs).
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(__file__))

from typing import Dict, List
from collections import Counter
import networkx as nx

from kempe_ops import enumerate_colourings, num_colours
from triangulation_db import generate_triangulations
from merge_analysis import bfs_path_merge_check


def extended_bfs_avoidance(target_n: int) -> Dict:
    """
    Run bfs_path_merge_check on all degree-≤5 vertices for all
    triangulations at vertex count target_n.
    """
    db = generate_triangulations(target_n)
    triangulations = db[target_n]

    total_stats = {
        'n': target_n,
        'num_graphs': len(triangulations),
        'total_a5_swaps': 0,
        'total_merges': 0,
        'total_multi_chain_cases': 0,
        'total_multi_chain_swap_adjacent': 0,
        'total_colourings_tested': 0,
        'by_degree': {4: {'a5_swaps': 0, 'multi_chain': 0, 'swap_adj': 0},
                      5: {'a5_swaps': 0, 'multi_chain': 0, 'swap_adj': 0}},
        'per_graph': [],
    }

    for idx, T in enumerate(triangulations):
        name = T.graph.get('name', f'T_{target_n}_{idx}')
        graph_stats = {
            'name': name,
            'a5_swaps': 0,
            'merges': 0,
            'multi_chain': 0,
            'swap_adj': 0,
            'vertices_tested': 0,
            'colourings_tested': 0,
        }

        for v in sorted(T.nodes()):
            deg = T.degree(v)
            if deg > 5:
                continue

            result = bfs_path_merge_check(T, v)
            graph_stats['vertices_tested'] += 1
            graph_stats['colourings_tested'] += result['total_colourings']
            graph_stats['a5_swaps'] += result['total_a5_swaps']
            graph_stats['merges'] += result['merges']
            graph_stats['multi_chain'] += result['multi_chain_cases']
            graph_stats['swap_adj'] += result['multi_chain_swap_adjacent']

            total_stats['total_a5_swaps'] += result['total_a5_swaps']
            total_stats['total_merges'] += result['merges']
            total_stats['total_multi_chain_cases'] += result['multi_chain_cases']
            total_stats['total_multi_chain_swap_adjacent'] += result['multi_chain_swap_adjacent']
            total_stats['total_colourings_tested'] += result['total_colourings']

            if deg in (4, 5):
                total_stats['by_degree'][deg]['a5_swaps'] += result['total_a5_swaps']
                total_stats['by_degree'][deg]['multi_chain'] += result['multi_chain_cases']
                total_stats['by_degree'][deg]['swap_adj'] += result['multi_chain_swap_adjacent']

        total_stats['per_graph'].append(graph_stats)

        if (idx + 1) % 10 == 0 or idx == 0:
            print(f"  [{idx+1}/{len(triangulations)}] {name}: "
                  f"{graph_stats['a5_swaps']} (a,5)-swaps, "
                  f"{graph_stats['multi_chain']} merge-prone, "
                  f"{graph_stats['swap_adj']} BFS-used-unsafe")

    return total_stats


def extended_all_paths_at_n9() -> Dict:
    """
    Run the all-paths analysis at n=9 to check whether the existential
    pattern (from n=8) continues.
    """
    from all_paths_analysis import all_paths_merge_analysis
    return all_paths_merge_analysis(max_n=9)


if __name__ == '__main__':
    print("=" * 70)
    print("M1-S1: Extended BFS Avoidance Tests")
    print("Agent 1419, Manager M1, Sub-subagent S1")
    print("=" * 70)

    print("\n--- Phase 1: n=9 (50 triangulations) ---")
    t0 = time.time()
    stats_9 = extended_bfs_avoidance(9)
    t9 = time.time() - t0

    print(f"\nn=9 RESULTS (completed in {t9:.1f}s):")
    print(f"  Graphs: {stats_9['num_graphs']}")
    print(f"  Total (a,5)-swaps: {stats_9['total_a5_swaps']}")
    print(f"  Total merges: {stats_9['total_merges']}")
    print(f"  Merge-prone cases: {stats_9['total_multi_chain_cases']}")
    print(f"  BFS used unsafe: {stats_9['total_multi_chain_swap_adjacent']}")
    print(f"  Colourings tested: {stats_9['total_colourings_tested']}")
    for deg in [4, 5]:
        d = stats_9['by_degree'][deg]
        rate = d['multi_chain'] / max(1, d['a5_swaps']) * 100
        print(f"  Degree {deg}: {d['a5_swaps']} (a,5)-swaps, "
              f"{d['multi_chain']} merge-prone ({rate:.1f}%), "
              f"{d['swap_adj']} BFS-used")

    if stats_9['total_merges'] > 0:
        print("\n*** COUNTEREXAMPLE FOUND AT n=9 ***")
    else:
        print("\n  BFS avoidance HOLDS at n=9 (0 merges)")

    print("\n" + "=" * 70)
    print("DONE: M1-S1 Extended Analysis")
    print("=" * 70)
