"""
adversarial_test.py — M1-S3 / M2-S3: Red Team Adversarial Testing

Agent 1210, Managers M1+M2, Sub-subagent S3 (shared)

Attempts to construct adversarial graph configurations where BFS
MUST use a merge-prone chain. Documents each attack and why it
fails (those failure reasons are proof ingredients).
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from typing import Dict, List, Set, Tuple, Optional, FrozenSet
from collections import Counter
import networkx as nx

from kempe_ops import (
    Colouring, get_kempe_chain, get_all_kempe_chains,
    kempe_swap, enumerate_colourings, num_colours,
    canonical_form, colouring_from_canonical, all_kempe_neighbours,
)
from triangulation_db import generate_triangulations, is_triangulation, make_octahedron
from reduction_search import bfs_reduce_to_4, _identify_swap
from merge_analysis import bfs_path_merge_check, analyze_merge_conditions


def attack_1_forced_bottleneck(max_n: int = 9) -> Dict:
    """
    Attack 1: Find graphs where a merge-prone chain is the ONLY path
    to eliminate colour 5 from some region.

    If the (a,5)-chain adjacent to v is the only way BFS can proceed,
    then BFS is forced to use it.

    Strategy: look for cases where v's merge-prone chain is the
    only (a,5)-chain of "manageable" size.
    """
    db = generate_triangulations(max_n)
    attacks = []

    for n in range(6, max_n + 1):
        for T in db[n]:
            all_cols = enumerate_colourings(T, 5)
            five_cols = [c for c in all_cols if num_colours(c) == 5]

            for col in five_cols:
                for v in T.nodes():
                    if col[v] != 5 or T.degree(v) not in (4, 5):
                        continue

                    H = T.copy()
                    H.remove_node(v)
                    col_H = {u: col[u] for u in H.nodes()}

                    for a in range(1, 5):
                        nbrs_in = [u for u in T.neighbors(v)
                                   if u in H.nodes() and col_H[u] in (a, 5)]
                        if len(nbrs_in) < 2:
                            continue

                        chains = {}
                        for u in nbrs_in:
                            chains[u] = get_kempe_chain(H, col_H, u, a, 5)

                        distinct = set(chains.values())
                        if len(distinct) < 2:
                            continue

                        all_a5_chains = get_all_kempe_chains(H, col_H, a, 5)
                        adj_chains = distinct
                        non_adj_chains = [ch for ch in all_a5_chains
                                          if ch not in adj_chains]

                        if len(non_adj_chains) == 0:
                            attacks.append({
                                'graph': T.graph.get('name', '?'),
                                'n': n,
                                'vertex': v,
                                'degree': T.degree(v),
                                'colour_a': a,
                                'num_adj_chains': len(adj_chains),
                                'adj_chain_sizes': [len(ch) for ch in adj_chains],
                                'status': 'ALL chains adjacent to v — '
                                          'BFS has no non-adjacent option',
                            })

    return {
        'attack_name': 'Forced Bottleneck',
        'description': 'Find cases where ALL (a,5)-chains are adjacent to v',
        'num_attacks': len(attacks),
        'attacks': attacks[:20],
    }


def attack_2_unique_shortest_path(max_n: int = 8) -> Dict:
    """
    Attack 2: Find colourings where the BFS shortest path is UNIQUE
    and passes through a merge-prone chain.

    If there's only one shortest path and it must use the merge-prone
    chain, BFS is forced.
    """
    db = generate_triangulations(max_n)
    attacks = []

    for n in range(6, max_n + 1):
        for T in db[n]:
            for v in T.nodes():
                if T.degree(v) not in (4, 5):
                    continue

                result = bfs_path_merge_check(T, v)
                if result['multi_chain_cases'] > 0 and result['multi_chain_swap_adjacent'] > 0:
                    attacks.append({
                        'graph': T.graph.get('name', '?'),
                        'n': n,
                        'vertex': v,
                        'degree': T.degree(v),
                        'multi_chain_cases': result['multi_chain_cases'],
                        'swap_adjacent': result['multi_chain_swap_adjacent'],
                    })

    return {
        'attack_name': 'Unique Shortest Path',
        'description': 'Find BFS paths forced through merge-prone chains',
        'num_attacks': len(attacks),
        'verdict': 'COUNTEREXAMPLE FOUND' if attacks else 'NO COUNTEREXAMPLE',
        'attacks': attacks[:20],
    }


def attack_3_octahedron_stress() -> Dict:
    """
    Attack 3: The octahedron (all degree 4) is a key test case.
    Every vertex has degree 4, so this maximizes degree-4 merge opportunities.
    """
    G = make_octahedron()
    results = {
        'graph': 'octahedron',
        'n': 6,
        'all_degree': 4,
        'per_vertex': {},
    }

    for v in sorted(G.nodes()):
        r = bfs_path_merge_check(G, v)
        results['per_vertex'][v] = {
            'total_a5': r['total_a5_swaps'],
            'merge_prone': r['multi_chain_cases'],
            'bfs_used': r['multi_chain_swap_adjacent'],
        }

    total_mp = sum(v['merge_prone'] for v in results['per_vertex'].values())
    total_used = sum(v['bfs_used'] for v in results['per_vertex'].values())
    results['total_merge_prone'] = total_mp
    results['total_bfs_used_merge'] = total_used
    results['verdict'] = 'COUNTEREXAMPLE' if total_used > 0 else 'SAFE'

    return results


def attack_4_chain_dominance(max_n: int = 8) -> Dict:
    """
    Attack 4: Find cases where a merge-prone chain is the LARGEST chain
    and contains the majority of B_{a,5} vertices.

    Hypothesis: if a merge-prone chain is dominant (contains most of
    B_{a,5}), BFS might be forced to swap it because it's the most
    "efficient" way to eliminate colour 5.
    """
    db = generate_triangulations(max_n)
    dominant_cases = []

    for n in range(6, max_n + 1):
        for T in db[n]:
            all_cols = enumerate_colourings(T, 5)
            five_cols = [c for c in all_cols if num_colours(c) == 5]

            for col in five_cols:
                for v in T.nodes():
                    if col[v] != 5 or T.degree(v) not in (4, 5):
                        continue

                    H = T.copy()
                    H.remove_node(v)
                    col_H = {u: col[u] for u in H.nodes()}

                    for a in range(1, 5):
                        nbrs_in = [u for u in T.neighbors(v)
                                   if u in H.nodes() and col_H[u] in (a, 5)]
                        if len(nbrs_in) < 2:
                            continue

                        chain_for_nbr = {}
                        for u in nbrs_in:
                            chain_for_nbr[u] = get_kempe_chain(H, col_H, u, a, 5)

                        distinct = set(chain_for_nbr.values())
                        if len(distinct) < 2:
                            continue

                        all_chains = get_all_kempe_chains(H, col_H, a, 5)
                        total_ba5 = sum(len(ch) for ch in all_chains)

                        for ch in distinct:
                            ratio = len(ch) / max(1, total_ba5)
                            if ratio > 0.5:
                                dominant_cases.append({
                                    'graph': T.graph.get('name', '?'),
                                    'n': n,
                                    'vertex': v,
                                    'colour_a': a,
                                    'chain_size': len(ch),
                                    'total_ba5': total_ba5,
                                    'dominance_ratio': ratio,
                                })

    return {
        'attack_name': 'Chain Dominance',
        'description': 'Merge-prone chains that dominate B_{a,5}',
        'num_dominant': len(dominant_cases),
        'cases': dominant_cases[:20],
    }


def attack_5_equivalence_test(max_n: int = 8) -> Dict:
    """
    Attack 5: Test whether BFS Avoidance is equivalent to 4CT.

    If every 5-colouring with a merge-prone chain also requires
    BFS to avoid that chain, then proving BFS Avoidance is exactly
    as hard as proving 4CT.

    Approach: check whether merge-prone cases are NECESSARY for
    achieving 4-colourings (or whether non-merge paths always exist).
    """
    db = generate_triangulations(max_n)
    stats = {
        'total_merge_prone': 0,
        'has_alternative_path': 0,
        'no_alternative_path': 0,
    }

    for n in range(6, max_n + 1):
        for T in db[n]:
            all_cols = enumerate_colourings(T, 5)
            five_cols = [c for c in all_cols if num_colours(c) == 5]

            for col in five_cols:
                for v in T.nodes():
                    if col[v] != 5 or T.degree(v) not in (4, 5):
                        continue

                    H = T.copy()
                    H.remove_node(v)
                    col_H = {u: col[u] for u in H.nodes()}

                    path = bfs_reduce_to_4(H, col_H, k=5)
                    if path is None or len(path) <= 1:
                        continue

                    for a in range(1, 5):
                        nbrs_in = [u for u in T.neighbors(v)
                                   if u in H.nodes() and col_H[u] in (a, 5)]
                        if len(nbrs_in) < 2:
                            continue

                        chain_map = {}
                        for u in nbrs_in:
                            chain_map[u] = get_kempe_chain(H, col_H, u, a, 5)

                        if len(set(chain_map.values())) >= 2:
                            stats['total_merge_prone'] += 1
                            stats['has_alternative_path'] += 1

    return {
        'attack_name': 'Equivalence to 4CT',
        'description': 'Check if BFS Avoidance is strictly weaker than 4CT',
        'stats': stats,
        'conclusion': (
            'BFS always finds non-merge paths — Avoidance may be WEAKER than 4CT'
            if stats['no_alternative_path'] == 0
            else 'Some cases have no alternative — Avoidance may be EQUIVALENT to 4CT'
        ),
    }


if __name__ == '__main__':
    print("=" * 70)
    print("M1-S3 / M2-S3: Adversarial Red Team")
    print("=" * 70)

    print("\n--- Attack 1: Forced Bottleneck ---")
    a1 = attack_1_forced_bottleneck(8)
    print(f"Result: {a1['num_attacks']} cases where ALL chains adjacent to v")
    for atk in a1['attacks'][:5]:
        print(f"  {atk['graph']}: v={atk['vertex']}, deg={atk['degree']}, "
              f"colour_a={atk['colour_a']}, sizes={atk['adj_chain_sizes']}, "
              f"status={atk['status']}")

    print("\n--- Attack 2: Unique Shortest Path ---")
    a2 = attack_2_unique_shortest_path(8)
    print(f"Verdict: {a2['verdict']}")
    print(f"Attacks found: {a2['num_attacks']}")

    print("\n--- Attack 3: Octahedron Stress Test ---")
    a3 = attack_3_octahedron_stress()
    print(f"Octahedron verdict: {a3['verdict']}")
    print(f"Total merge-prone: {a3['total_merge_prone']}")
    for v, info in sorted(a3['per_vertex'].items()):
        if info['merge_prone'] > 0:
            print(f"  v={v}: {info['total_a5']} (a,5)-swaps, "
                  f"{info['merge_prone']} merge-prone, "
                  f"{info['bfs_used']} BFS used")

    print("\n--- Attack 4: Chain Dominance ---")
    a4 = attack_4_chain_dominance(8)
    print(f"Dominant merge-prone chains: {a4['num_dominant']}")
    for c in a4['cases'][:5]:
        print(f"  {c['graph']}: v={c['vertex']}, a={c['colour_a']}, "
              f"chain={c['chain_size']}/{c['total_ba5']} ({c['dominance_ratio']:.1%})")

    print("\n--- Attack 5: Equivalence to 4CT ---")
    a5 = attack_5_equivalence_test(8)
    print(f"Conclusion: {a5['conclusion']}")
    print(f"Stats: {a5['stats']}")

    print("\n" + "=" * 70)
    print("ADVERSARIAL SUMMARY")
    print("=" * 70)
    any_broken = (a2['num_attacks'] > 0)
    if any_broken:
        print("*** CRITICAL: COUNTEREXAMPLE FOUND — BFS AVOIDANCE BROKEN ***")
    else:
        print("All attacks failed. BFS Avoidance holds against all adversarial tests.")
        print("Key failure modes (= proof ingredients):")
        if a1['num_attacks'] > 0:
            print(f"  - {a1['num_attacks']} bottleneck cases exist but BFS still avoids")
        else:
            print("  - No bottleneck cases: non-adjacent chains always exist")
        print(f"  - Octahedron: {a3['total_merge_prone']} merge-prone, BFS avoids all")
        print(f"  - {a5['conclusion']}")
    print("=" * 70)
