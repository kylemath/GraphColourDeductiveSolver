"""
degree4_analysis.py — M1-S1: Characterize degree-4 link and merge-prone configurations.

Agent 1210, Manager M1, Sub-subagent S1: Link Structure Analyst

Enumerates ALL possible (a,5)-chain configurations at degree-4 vertices,
classifies merge-prone cases, and analyzes structural constraints from planarity.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from typing import Dict, List, Set, Tuple, FrozenSet
from collections import Counter, defaultdict
import networkx as nx

from kempe_ops import (
    Colouring, get_kempe_chain, get_all_kempe_chains,
    kempe_swap, enumerate_colourings, num_colours, canonical_form,
)
from triangulation_db import generate_triangulations
from merge_analysis import analyze_merge_conditions, bfs_path_merge_check


def classify_degree4_configurations(G: nx.Graph) -> Dict:
    """
    For all 5-colourings with a degree-4 vertex coloured 5,
    classify the colour pattern of the 4 neighbours and
    determine merge-prone configurations.
    """
    all_cols = enumerate_colourings(G, 5)
    five_cols = [c for c in all_cols if num_colours(c) == 5]

    pattern_stats = defaultdict(lambda: {
        'count': 0, 'merge_prone': 0, 'colours_a_with_merge': Counter()
    })

    for col in five_cols:
        for v in G.nodes():
            if col[v] != 5 or G.degree(v) != 4:
                continue

            nbrs = sorted(G.neighbors(v))
            nbr_colours = tuple(col[u] for u in nbrs)
            pattern = tuple(sorted(nbr_colours))

            pattern_stats[pattern]['count'] += 1

            conditions = analyze_merge_conditions(G, col, v)
            for cond in conditions:
                if cond['would_merge']:
                    pattern_stats[pattern]['merge_prone'] += 1
                    pattern_stats[pattern]['colours_a_with_merge'][cond['colour_a']] += 1

    return dict(pattern_stats)


def analyze_degree4_link_merge_geometry(G: nx.Graph) -> Dict:
    """
    For degree-4 vertices in merge-prone situations, analyze WHERE in
    the C4 link the different chains touch.

    In a C4 link (u1-u2-u3-u4-u1), the non-adjacent pairs are:
      (u1, u3) and (u2, u4)

    Only these pairs can be in different chains (adjacent pairs share
    an edge, so they must be in the same chain if both are in B_{a,5}).
    """
    all_cols = enumerate_colourings(G, 5)
    five_cols = [c for c in all_cols if num_colours(c) == 5]

    stats = {
        'total_degree4_v5': 0,
        'merge_prone_cases': 0,
        'opposite_pair_merges': 0,
        'adjacent_pair_merges': 0,
        'chain_size_distribution': Counter(),
        'merge_prone_chain_sizes': [],
    }

    emb_cache = {}

    for col in five_cols:
        for v in G.nodes():
            if col[v] != 5 or G.degree(v) != 4:
                continue

            stats['total_degree4_v5'] += 1

            H = G.copy()
            H.remove_node(v)
            col_H = {u: col[u] for u in H.nodes()}
            nbrs = list(G.neighbors(v))

            for a in range(1, 5):
                nbrs_in_ba5 = [u for u in nbrs if col_H.get(u, 0) in (a, 5)]
                if len(nbrs_in_ba5) < 2:
                    continue

                chains = {}
                for u in nbrs_in_ba5:
                    chains[u] = get_kempe_chain(H, col_H, u, a, 5)

                distinct_chains = set(chains.values())
                if len(distinct_chains) < 2:
                    continue

                stats['merge_prone_cases'] += 1

                for ch in distinct_chains:
                    stats['chain_size_distribution'][len(ch)] += 1
                    stats['merge_prone_chain_sizes'].append(len(ch))

                for i, u1 in enumerate(nbrs_in_ba5):
                    for u2 in nbrs_in_ba5[i+1:]:
                        if chains[u1] != chains[u2]:
                            if G.has_edge(u1, u2):
                                stats['adjacent_pair_merges'] += 1
                            else:
                                stats['opposite_pair_merges'] += 1

    return stats


def bfs_avoidance_degree4_detailed(max_n: int = 8) -> Dict:
    """
    Detailed BFS avoidance analysis focusing on degree-4 vertices only.
    """
    db = generate_triangulations(max_n)
    total_stats = {
        'total_a5_swaps': 0,
        'merge_prone_cases': 0,
        'bfs_avoided': 0,
        'bfs_used_merge_chain': 0,
        'by_n': {},
    }

    for n in range(4, max_n + 1):
        n_stats = {'a5_swaps': 0, 'merge_prone': 0, 'avoided': 0, 'used': 0}
        for T in db[n]:
            for v in sorted(T.nodes()):
                if T.degree(v) != 4:
                    continue
                result = bfs_path_merge_check(T, v)
                n_stats['a5_swaps'] += result['total_a5_swaps']
                n_stats['merge_prone'] += result['multi_chain_cases']
                n_stats['avoided'] += result['multi_chain_cases'] - result['multi_chain_swap_adjacent']
                n_stats['used'] += result['multi_chain_swap_adjacent']

        total_stats['total_a5_swaps'] += n_stats['a5_swaps']
        total_stats['merge_prone_cases'] += n_stats['merge_prone']
        total_stats['bfs_avoided'] += n_stats['avoided']
        total_stats['bfs_used_merge_chain'] += n_stats['used']
        total_stats['by_n'][n] = n_stats

    return total_stats


if __name__ == '__main__':
    print("=" * 70)
    print("M1-S1: Degree-4 Link Structure Analysis")
    print("=" * 70)

    print("\n--- Phase 1: Colour pattern classification (n=6,7) ---")
    db = generate_triangulations(7)
    for n in [6, 7]:
        for T in db[n]:
            name = T.graph.get('name', '?')
            patterns = classify_degree4_configurations(T)
            if patterns:
                print(f"\n{name} (n={n}):")
                for pat, info in sorted(patterns.items()):
                    if info['merge_prone'] > 0:
                        print(f"  Pattern {pat}: {info['count']} cases, "
                              f"{info['merge_prone']} merge-prone, "
                              f"colours: {dict(info['colours_a_with_merge'])}")

    print("\n--- Phase 2: Merge geometry at degree-4 (n=6,7,8) ---")
    db8 = generate_triangulations(8)
    for n in [6, 7, 8]:
        for T in db8[n]:
            name = T.graph.get('name', '?')
            geom = analyze_degree4_link_merge_geometry(T)
            if geom['merge_prone_cases'] > 0:
                print(f"\n{name} (n={n}):")
                print(f"  Degree-4 v5 cases: {geom['total_degree4_v5']}")
                print(f"  Merge-prone: {geom['merge_prone_cases']}")
                print(f"  Opposite pair (non-adj): {geom['opposite_pair_merges']}")
                print(f"  Adjacent pair: {geom['adjacent_pair_merges']}")
                print(f"  Chain sizes: {dict(geom['chain_size_distribution'])}")

    print("\n--- Phase 3: BFS avoidance at degree-4 only (n=4..8) ---")
    d4_stats = bfs_avoidance_degree4_detailed(8)
    print(f"\nOverall degree-4 BFS avoidance:")
    print(f"  Total (a,5)-swaps: {d4_stats['total_a5_swaps']}")
    print(f"  Merge-prone cases: {d4_stats['merge_prone_cases']}")
    print(f"  BFS avoided: {d4_stats['bfs_avoided']}")
    print(f"  BFS used merge chain: {d4_stats['bfs_used_merge_chain']}")
    for n, ns in sorted(d4_stats['by_n'].items()):
        if ns['merge_prone'] > 0:
            print(f"  n={n}: {ns['a5_swaps']} swaps, {ns['merge_prone']} merge-prone, "
                  f"{ns['avoided']} avoided, {ns['used']} used")

    print("\n" + "=" * 70)
    print("DONE: M1-S1 Analysis Complete")
    print("=" * 70)
