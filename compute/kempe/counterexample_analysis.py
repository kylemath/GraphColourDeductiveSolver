"""
counterexample_analysis.py — Deep analysis of n=9 BFS Avoidance counterexamples.

Agent 1419 — HARD KILL Investigation

Two graphs have true counterexamples: T_9_25 (v=3, deg 5) and T_9_35 (v=6, deg 4).
For each counterexample, investigate:
1. Graph structure (edges, degree sequence)
2. Whether LONGER (non-optimal) safe paths exist
3. Whether a different vertex removal avoids the problem
4. Whether the 4-colouring is still achievable via any path
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from typing import Dict, List, Set, Tuple
from collections import Counter
import networkx as nx

from kempe_ops import (
    Colouring, CanonicalColouring,
    get_kempe_chain, get_all_kempe_chains, kempe_swap,
    enumerate_colourings, num_colours,
    canonical_form, colouring_from_canonical, all_kempe_neighbours,
)
from triangulation_db import generate_triangulations
from reduction_search import bfs_reduce_to_4, _identify_swap, bulk_distance_to_4col
from merge_analysis import bfs_path_merge_check, analyze_merge_conditions


def dump_graph_structure(T: nx.Graph) -> Dict:
    """Full structural analysis of a graph."""
    name = T.graph.get('name', '?')
    degrees = sorted([T.degree(v) for v in T.nodes()])
    return {
        'name': name,
        'n': T.number_of_nodes(),
        'edges': T.number_of_edges(),
        'degree_sequence': degrees,
        'adjacency': {v: sorted(T.neighbors(v)) for v in sorted(T.nodes())},
        'min_degree': min(degrees),
        'max_degree': max(degrees),
    }


def check_longer_safe_paths(T: nx.Graph, v: int) -> Dict:
    """
    For counterexample cases, check whether ANY path (not just optimal)
    from the 5-colouring to a 4-colouring avoids unsafe swaps.
    
    Strategy: BFS in R(G-v, 5) but filter out unsafe swaps.
    If we can still reach a 4-colouring, the path exists (just longer).
    """
    from collections import deque

    H = T.copy()
    H.remove_node(v)

    all_cols = enumerate_colourings(T, 5)
    v5_cols = [c for c in all_cols if c[v] == 5 and num_colours(c) == 5]

    results = {
        'vertex': v,
        'degree': T.degree(v),
        'total_v5_colourings': len(v5_cols),
        'merge_prone_colourings': 0,
        'has_safe_optimal': 0,
        'has_safe_nonoptimal': 0,
        'no_safe_path_at_all': 0,
        'optimal_dist_when_safe_nonoptimal': [],
        'safe_path_dist_when_nonoptimal': [],
    }

    for col in v5_cols:
        col_H = {u: col[u] for u in H.nodes()}

        is_merge_prone = False
        merge_colours = []
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
                merge_colours.append(a_colour)

        if not is_merge_prone:
            continue

        results['merge_prone_colourings'] += 1

        opt_path = bfs_reduce_to_4(H, col_H, k=5)
        opt_dist = len(opt_path) - 1 if opt_path else -1

        from all_paths_analysis import bfs_all_optimal_paths, classify_path_safety
        _, all_opt = bfs_all_optimal_paths(H, col_H, k=5)
        has_safe_opt = False
        for p in all_opt:
            c = classify_path_safety(T, H, v, col, p)
            if c['path_is_safe']:
                has_safe_opt = True
                break

        if has_safe_opt:
            results['has_safe_optimal'] += 1
            continue

        start_c = canonical_form(H, col_H)
        visited = {start_c: 0}
        queue = deque([start_c])
        found_safe = False
        safe_dist = -1

        max_explore = 50000

        while queue and len(visited) < max_explore:
            current = queue.popleft()
            d = visited[current]
            current_col = colouring_from_canonical(H, current)

            for nbr in all_kempe_neighbours(H, current_col, 5):
                if nbr in visited:
                    continue

                nbr_col_H = colouring_from_canonical(H, nbr)

                a, b = _identify_swap(H, current_col, nbr_col_H)
                is_unsafe = False
                if a is not None and b is not None and 5 in (a, b):
                    the_a = a if a != 5 else b
                    swapped = frozenset(u for u in H.nodes()
                                       if current_col[u] != nbr_col_H[u])

                    v_nbrs = [u for u in T.neighbors(v)
                              if u in H.nodes() and current_col.get(u, 0) in (the_a, 5)]
                    chains_of_nbrs = set()
                    for u in v_nbrs:
                        chains_of_nbrs.add(get_kempe_chain(H, current_col, u, the_a, 5))

                    if len(chains_of_nbrs) >= 2:
                        sw_chain = None
                        if swapped:
                            sv = next(iter(swapped))
                            if current_col.get(sv, 0) in (the_a, 5):
                                sw_chain = get_kempe_chain(H, current_col, sv, the_a, 5)
                        if sw_chain in chains_of_nbrs:
                            is_unsafe = True

                if is_unsafe:
                    continue

                visited[nbr] = d + 1
                queue.append(nbr)

                if num_colours(nbr_col_H) <= 4:
                    found_safe = True
                    safe_dist = d + 1
                    break

            if found_safe:
                break

        if found_safe:
            results['has_safe_nonoptimal'] += 1
            results['optimal_dist_when_safe_nonoptimal'].append(opt_dist)
            results['safe_path_dist_when_nonoptimal'].append(safe_dist)
        else:
            results['no_safe_path_at_all'] += 1

    return results


def check_alternative_vertices(T: nx.Graph) -> Dict:
    """
    For the counterexample graph, check: is there a vertex v' whose removal
    avoids all merge problems? The proof only needs ONE working vertex removal.
    """
    results = {'graph': T.graph.get('name', '?'), 'per_vertex': {}}

    for v in sorted(T.nodes()):
        if T.degree(v) > 5:
            results['per_vertex'][v] = {'degree': T.degree(v), 'skip': True}
            continue

        r = bfs_path_merge_check(T, v)
        results['per_vertex'][v] = {
            'degree': T.degree(v),
            'skip': False,
            'merges': r['merges'],
            'multi_chain_cases': r['multi_chain_cases'],
            'swap_adjacent': r['multi_chain_swap_adjacent'],
            'total_a5_swaps': r['total_a5_swaps'],
        }

    return results


if __name__ == '__main__':
    print("=" * 70)
    print("COUNTEREXAMPLE DEEP ANALYSIS")
    print("Agent 1419 — HARD KILL Investigation")
    print("=" * 70)

    db = generate_triangulations(9)

    for graph_idx in [25, 35]:
        T = db[9][graph_idx]
        name = T.graph.get('name', f'T_9_{graph_idx}')
        print(f"\n{'='*70}")
        print(f"Graph: {name}")
        print(f"{'='*70}")

        struct = dump_graph_structure(T)
        print(f"Degree sequence: {struct['degree_sequence']}")
        print(f"Adjacency:")
        for v, nbrs in struct['adjacency'].items():
            print(f"  {v} (deg {T.degree(v)}): {nbrs}")

        print(f"\n--- Alternative vertex analysis ---")
        alt = check_alternative_vertices(T)
        for v, info in sorted(alt['per_vertex'].items()):
            if info.get('skip'):
                print(f"  v={v} (deg={info['degree']}): skipped (deg>5)")
            else:
                print(f"  v={v} (deg={info['degree']}): "
                      f"merges={info['merges']}, "
                      f"merge_prone={info['multi_chain_cases']}, "
                      f"swap_adj={info['swap_adjacent']}")

    target_pairs = [(25, 3), (35, 6)]

    for graph_idx, target_v in target_pairs:
        T = db[9][graph_idx]
        name = T.graph.get('name', f'T_9_{graph_idx}')
        print(f"\n{'='*70}")
        print(f"Longer-path analysis: {name}, v={target_v}")
        print(f"{'='*70}")

        longer = check_longer_safe_paths(T, target_v)
        print(f"Merge-prone colourings: {longer['merge_prone_colourings']}")
        print(f"Has safe optimal path: {longer['has_safe_optimal']}")
        print(f"Has safe non-optimal path: {longer['has_safe_nonoptimal']}")
        print(f"No safe path at all: {longer['no_safe_path_at_all']}")
        if longer['safe_path_dist_when_nonoptimal']:
            print(f"Optimal distances (when non-opt safe exists): "
                  f"{longer['optimal_dist_when_safe_nonoptimal']}")
            print(f"Safe path distances: {longer['safe_path_dist_when_nonoptimal']}")

    print("\n" + "=" * 70)
    print("DEEP ANALYSIS COMPLETE")
    print("=" * 70)
