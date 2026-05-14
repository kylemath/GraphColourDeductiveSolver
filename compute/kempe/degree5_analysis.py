"""
degree5_analysis.py — M2-S1: Characterize degree-5 link and exploit non-interleaving.

Agent 1210, Manager M2, Sub-subagent S1: Non-Interleaving Exploiter

Enumerates ALL possible (a,5)-chain configurations at degree-5 vertices,
applies Theorem A (non-interleaving) constraints, and classifies merge-prone cases.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from typing import Dict, List, Set, Tuple, FrozenSet
from collections import Counter, defaultdict
import networkx as nx

from kempe_ops import (
    Colouring, get_kempe_chain, get_all_kempe_chains,
    kempe_swap, enumerate_colourings, num_colours,
)
from triangulation_db import generate_triangulations
from merge_analysis import analyze_merge_conditions, bfs_path_merge_check


def classify_degree5_configurations(G: nx.Graph) -> Dict:
    """
    For all 5-colourings with a degree-5 vertex coloured 5,
    classify the colour pattern of the 5 neighbours using the
    8-type Degree-5 Classification.
    """
    all_cols = enumerate_colourings(G, 5)
    five_cols = [c for c in all_cols if num_colours(c) == 5]

    type_stats = defaultdict(lambda: {
        'count': 0, 'merge_prone': 0, 'colours_with_merge': Counter()
    })

    for col in five_cols:
        for v in G.nodes():
            if col[v] != 5 or G.degree(v) != 5:
                continue

            nbrs = sorted(G.neighbors(v))
            nbr_colours = tuple(col[u] for u in nbrs)
            colour_multiset = tuple(sorted(nbr_colours))
            num_fives = sum(1 for c in nbr_colours if c == 5)
            num_distinct_14 = len(set(c for c in nbr_colours if c != 5))
            type_key = (num_fives, num_distinct_14, colour_multiset)

            type_stats[type_key]['count'] += 1

            conditions = analyze_merge_conditions(G, col, v)
            for cond in conditions:
                if cond['would_merge']:
                    type_stats[type_key]['merge_prone'] += 1
                    type_stats[type_key]['colours_with_merge'][cond['colour_a']] += 1

    return dict(type_stats)


def analyze_noninterleaving_at_degree5(G: nx.Graph) -> Dict:
    """
    For degree-5 vertices coloured 5, check non-interleaving constraints.

    In a C5 link (u1-u2-u3-u4-u5-u1), non-adjacent pairs are:
      u1-u3, u1-u4, u2-u4, u2-u5, u3-u5

    Theorem A says: for disjoint colour pairs {a,b} and {c,d}, the
    corresponding Kempe chains don't interleave in the cyclic order.

    We check: do merge-prone (a,5)-chains always involve non-adjacent
    pairs, and does non-interleaving constrain which configurations
    can actually occur?
    """
    all_cols = enumerate_colourings(G, 5)
    five_cols = [c for c in all_cols if num_colours(c) == 5]

    stats = {
        'total_degree5_v5': 0,
        'merge_prone_cases': 0,
        'non_adj_pairs_in_diff_chains': 0,
        'chain_gap_distribution': Counter(),
        'merge_prone_by_gap': Counter(),
    }

    for col in five_cols:
        for v in G.nodes():
            if col[v] != 5 or G.degree(v) != 5:
                continue

            stats['total_degree5_v5'] += 1

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

                distinct = set(chains.values())
                if len(distinct) < 2:
                    continue

                stats['merge_prone_cases'] += 1

                for i, u1 in enumerate(nbrs_in_ba5):
                    for u2 in nbrs_in_ba5[i+1:]:
                        if chains[u1] != chains[u2]:
                            stats['non_adj_pairs_in_diff_chains'] += 1
                            i1 = nbrs.index(u1)
                            i2 = nbrs.index(u2)
                            gap = min(abs(i1-i2), 5-abs(i1-i2))
                            stats['merge_prone_by_gap'][gap] += 1

    return stats


def bfs_avoidance_degree5_detailed(max_n: int = 8) -> Dict:
    """
    Detailed BFS avoidance analysis focusing on degree-5 vertices only.
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
                if T.degree(v) != 5:
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


def chain_size_comparison(max_n: int = 8) -> Dict:
    """
    Compare chain sizes: are merge-prone chains systematically larger
    than the chains BFS actually selects?
    """
    db = generate_triangulations(max_n)
    merge_prone_sizes = []
    bfs_selected_sizes = []

    for n in range(6, max_n + 1):
        for T in db[n]:
            all_cols = enumerate_colourings(T, 5)
            five_cols = [c for c in all_cols if num_colours(c) == 5]

            for col in five_cols:
                for v in T.nodes():
                    if col[v] != 5 or T.degree(v) != 5:
                        continue

                    H = T.copy()
                    H.remove_node(v)
                    col_H = {u: col[u] for u in H.nodes()}

                    for a in range(1, 5):
                        nbrs_in = [u for u in T.neighbors(v)
                                   if u in H.nodes() and col_H[u] in (a, 5)]
                        if len(nbrs_in) < 2:
                            continue
                        chain_map = {}
                        for u in nbrs_in:
                            chain_map[u] = get_kempe_chain(H, col_H, u, a, 5)
                        distinct = set(chain_map.values())
                        if len(distinct) >= 2:
                            for ch in distinct:
                                merge_prone_sizes.append(len(ch))

    return {
        'merge_prone_chain_sizes': merge_prone_sizes,
        'mean_merge_prone': sum(merge_prone_sizes) / max(1, len(merge_prone_sizes)),
        'max_merge_prone': max(merge_prone_sizes) if merge_prone_sizes else 0,
        'min_merge_prone': min(merge_prone_sizes) if merge_prone_sizes else 0,
        'size_distribution': dict(Counter(merge_prone_sizes)),
    }


if __name__ == '__main__':
    print("=" * 70)
    print("M2-S1: Degree-5 Non-Interleaving + Merge Analysis")
    print("=" * 70)

    print("\n--- Phase 1: Configuration classification (n=6,7) ---")
    db = generate_triangulations(7)
    for n in [6, 7]:
        for T in db[n]:
            name = T.graph.get('name', '?')
            types = classify_degree5_configurations(T)
            merge_types = {k: v for k, v in types.items() if v['merge_prone'] > 0}
            if merge_types:
                print(f"\n{name} (n={n}) — merge-prone types:")
                for key, info in sorted(merge_types.items()):
                    num5, ndist14, pat = key
                    print(f"  #5s={num5}, #distinct_14={ndist14}, pattern={pat}: "
                          f"{info['count']} cases, {info['merge_prone']} merge-prone")

    print("\n--- Phase 2: Non-interleaving analysis (n=6,7,8) ---")
    db8 = generate_triangulations(8)
    for n in [6, 7, 8]:
        for T in db8[n]:
            name = T.graph.get('name', '?')
            ni = analyze_noninterleaving_at_degree5(T)
            if ni['merge_prone_cases'] > 0:
                print(f"\n{name} (n={n}):")
                print(f"  Degree-5 v5: {ni['total_degree5_v5']}")
                print(f"  Merge-prone: {ni['merge_prone_cases']}")
                print(f"  Non-adj pairs in diff chains: {ni['non_adj_pairs_in_diff_chains']}")
                print(f"  By cyclic gap: {dict(ni['merge_prone_by_gap'])}")

    print("\n--- Phase 3: BFS avoidance degree-5 only (n=4..8) ---")
    d5_stats = bfs_avoidance_degree5_detailed(8)
    print(f"\nOverall degree-5 BFS avoidance:")
    print(f"  Total (a,5)-swaps: {d5_stats['total_a5_swaps']}")
    print(f"  Merge-prone: {d5_stats['merge_prone_cases']}")
    print(f"  BFS avoided: {d5_stats['bfs_avoided']}")
    print(f"  BFS used merge chain: {d5_stats['bfs_used_merge_chain']}")
    for n, ns in sorted(d5_stats['by_n'].items()):
        if ns['merge_prone'] > 0:
            print(f"  n={n}: {ns['a5_swaps']} swaps, {ns['merge_prone']} merge-prone, "
                  f"{ns['avoided']} avoided, {ns['used']} used")

    print("\n--- Phase 4: Chain size comparison ---")
    sizes = chain_size_comparison(8)
    print(f"\nMerge-prone chain sizes at degree 5:")
    print(f"  Mean: {sizes['mean_merge_prone']:.2f}")
    print(f"  Min: {sizes['min_merge_prone']}, Max: {sizes['max_merge_prone']}")
    print(f"  Distribution: {sizes['size_distribution']}")

    print("\n" + "=" * 70)
    print("DONE: M2-S1 Analysis Complete")
    print("=" * 70)
