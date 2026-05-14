"""
merge_analysis.py — Analyze (a,5)-Kempe chain merging when vertex v is re-added.

Key results (Agent 0051):
  - Degree 3: ZERO merges (provable — neighbourhood is a triangle)
  - Degree 4: ~17% merge rate
  - Degree 5: ~31% merge rate
  - BFS-optimal paths: ZERO merges (13876 (a,5)-swaps at n=8)
  - Critical pattern: BFS never swaps a chain adjacent to v when v has 2+ chain neighbours

Agent 0051 / Plan 2: Kempe Swap Game + Topological Non-Crossing
"""

from typing import Dict, List, Set, Tuple, Optional, FrozenSet
from collections import Counter
import networkx as nx

from kempe_ops import (
    Colouring, CanonicalColouring,
    get_kempe_chain, get_all_kempe_chains, kempe_swap,
    enumerate_colourings, num_colours,
    canonical_form, colouring_from_canonical,
)
from reduction_search import bfs_reduce_to_4, _identify_swap


def analyze_merge_conditions(G: nx.Graph, col: Colouring,
                             v: int) -> List[Dict]:
    """
    For a single colouring and vertex v (coloured 5), analyze merge conditions
    for each colour a in {1,2,3,4}.

    Returns a list of dicts, one per colour a, describing:
      - num_nbrs_in_ba5: how many neighbours of v are in B_{a,5}(G-v)
      - distinct_chains: how many distinct (a,5)-chains they belong to in G-v
      - would_merge: True if distinct_chains >= 2
    """
    assert col[v] == 5
    H = G.copy()
    H.remove_node(v)
    col_H = {u: col[u] for u in H.nodes()}
    results = []

    for a in range(1, 5):
        nbrs_in_ba5 = [u for u in G.neighbors(v)
                       if u in H.nodes() and col_H[u] in (a, 5)]
        chains = set()
        for u in nbrs_in_ba5:
            chains.add(get_kempe_chain(H, col_H, u, a, 5))

        results.append({
            'colour_a': a,
            'num_nbrs_in_ba5': len(nbrs_in_ba5),
            'distinct_chains': len(chains),
            'would_merge': len(chains) >= 2,
        })

    return results


def bulk_merge_analysis(G: nx.Graph) -> Dict:
    """
    Analyze merge conditions for ALL 5-colourings and ALL colour-5 vertices.

    Returns statistics grouped by vertex degree.
    """
    all_cols = enumerate_colourings(G, 5)
    five_cols = [c for c in all_cols if num_colours(c) == 5]

    by_degree: Dict[int, Dict] = {}

    for col in five_cols:
        for v in G.nodes():
            if col[v] != 5:
                continue
            deg = G.degree(v)
            if deg not in by_degree:
                by_degree[deg] = {'total': 0, 'merges': 0, 'chain_dist': Counter()}
            conditions = analyze_merge_conditions(G, col, v)
            for c in conditions:
                if c['num_nbrs_in_ba5'] == 0:
                    continue
                by_degree[deg]['total'] += 1
                by_degree[deg]['chain_dist'][c['distinct_chains']] += 1
                if c['would_merge']:
                    by_degree[deg]['merges'] += 1

    result = {}
    for deg in sorted(by_degree):
        d = by_degree[deg]
        result[deg] = {
            'total_cases': d['total'],
            'merges': d['merges'],
            'merge_rate': d['merges'] / max(1, d['total']),
            'chain_count_distribution': dict(sorted(d['chain_dist'].items())),
        }
    return result


def bfs_path_merge_check(G: nx.Graph, v: int) -> Dict:
    """
    For each 5-colouring of G where c(v) = 5, find the BFS-optimal path
    in R(G-v, 5) and check whether any (a,5)-swap in that path would cause
    a merge when v is re-added.

    Returns detailed statistics including:
      - total_a5_swaps: number of (a,5)-swaps examined
      - merges: number that would merge (should be 0)
      - chain_adjacent_to_v: swaps where the chain touches v's neighbourhood
      - multi_chain_but_safe: cases where v has 2+ chain neighbours but swap avoids them
    """
    H = G.copy()
    H.remove_node(v)

    all_cols = enumerate_colourings(G, 5)
    v5_cols = [c for c in all_cols if c[v] == 5 and num_colours(c) == 5]

    stats = {
        'vertex': v,
        'degree': G.degree(v),
        'total_colourings': len(v5_cols),
        'total_a5_swaps': 0,
        'merges': 0,
        'chain_adjacent_to_v': 0,
        'chain_not_adjacent_to_v': 0,
        'multi_chain_cases': 0,
        'multi_chain_swap_adjacent': 0,
    }

    for col in v5_cols:
        col_H = {u: col[u] for u in H.nodes()}
        path_H = bfs_reduce_to_4(H, col_H, k=5)
        if path_H is None or len(path_H) <= 1:
            continue

        col_G = dict(col)

        for step_idx in range(len(path_H) - 1):
            cur_H = colouring_from_canonical(H, path_H[step_idx])
            nxt_H = colouring_from_canonical(H, path_H[step_idx + 1])
            a, b = _identify_swap(H, cur_H, nxt_H)
            if a is None:
                continue

            swapped_verts = frozenset(
                u for u in H.nodes() if cur_H[u] != nxt_H[u])

            if 5 not in (a, b):
                if swapped_verts:
                    col_G = kempe_swap(col_G, swapped_verts, a, b)
                continue

            stats['total_a5_swaps'] += 1
            the_a = a if a != 5 else b
            col_H_cur = {w: col_G[w] for w in H.nodes()}

            chain_adj = any(u in swapped_verts for u in G.neighbors(v))
            if chain_adj:
                stats['chain_adjacent_to_v'] += 1
            else:
                stats['chain_not_adjacent_to_v'] += 1

            v_nbrs = [u for u in G.neighbors(v)
                       if u in H.nodes() and col_H_cur.get(u, 0) in (the_a, 5)]
            chains_of_nbrs = set()
            for u in v_nbrs:
                chains_of_nbrs.add(
                    get_kempe_chain(H, col_H_cur, u, the_a, 5))

            if len(chains_of_nbrs) >= 2:
                stats['multi_chain_cases'] += 1

                swapped_chain = None
                if swapped_verts:
                    sv = next(iter(swapped_verts))
                    if col_H_cur.get(sv, 0) in (the_a, 5):
                        swapped_chain = get_kempe_chain(
                            H, col_H_cur, sv, the_a, 5)

                if swapped_chain in chains_of_nbrs:
                    stats['multi_chain_swap_adjacent'] += 1
                    stats['merges'] += 1

            if swapped_verts:
                col_G = kempe_swap(col_G, swapped_verts, a, b)

    return stats


def v5_descent_analysis(G: nx.Graph) -> Dict:
    """
    For each 5-colouring with |V_5| >= 1, check whether there exists a
    single Kempe swap (on any pair) that reduces |V_5| by exactly 1 without
    increasing it.

    Tests the |V_5| descent hypothesis: can we always greedily reduce |V_5|?
    """
    all_cols = enumerate_colourings(G, 5)
    five_cols = [c for c in all_cols if num_colours(c) == 5]

    stats = {
        'total_tested': 0,
        'descent_exists': 0,
        'no_descent': 0,
        'no_descent_details': [],
        'min_v5_delta_when_no_direct': [],
    }

    for col in five_cols:
        v5_before = sum(1 for c in col.values() if c == 5)
        stats['total_tested'] += 1

        found_descent = False
        best_delta = float('inf')

        for a in range(1, 6):
            for b in range(a + 1, 6):
                for chain in get_all_kempe_chains(G, col, a, b):
                    new_col = kempe_swap(col, chain, a, b)
                    v5_after = sum(1 for c in new_col.values() if c == 5)
                    delta = v5_after - v5_before
                    best_delta = min(best_delta, delta)
                    if delta == -1:
                        found_descent = True

        if found_descent:
            stats['descent_exists'] += 1
        else:
            stats['no_descent'] += 1
            stats['min_v5_delta_when_no_direct'].append(best_delta)
            if len(stats['no_descent_details']) < 5:
                stats['no_descent_details'].append({
                    'v5_count': v5_before,
                    'best_delta': best_delta,
                })

    return stats
