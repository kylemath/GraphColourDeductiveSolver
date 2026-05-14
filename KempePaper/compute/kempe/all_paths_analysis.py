"""
all_paths_analysis.py — M1-S3: ALL BFS-optimal paths analysis (GATING ITEM).

Agent 1419, Manager M1, Sub-subagent S3

For each merge-prone case at n <= 8, enumerate ALL BFS-optimal paths
(not just the first). Classify: do ALL optimal paths avoid unsafe swaps,
or do SOME use them?

Also: for each merge-prone case, record which alternative swap BFS chose
and classify it (was it a {1,2,3,4}-swap? which pair? was it a safe (a,5)-swap?).
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from typing import Dict, List, Set, Tuple, Optional, FrozenSet
from collections import Counter, defaultdict, deque
import networkx as nx

from kempe_ops import (
    Colouring, CanonicalColouring,
    get_kempe_chain, get_all_kempe_chains, kempe_swap,
    enumerate_colourings, num_colours,
    canonical_form, colouring_from_canonical, all_kempe_neighbours,
)
from triangulation_db import generate_triangulations
from reduction_search import _identify_swap


def bfs_all_optimal_paths(G: nx.Graph, start: Colouring, k: int = 5
                          ) -> Tuple[int, List[List[CanonicalColouring]]]:
    """
    BFS from start to any 4-colouring in R(G,k).
    Returns (optimal_distance, list_of_all_optimal_paths).

    Enumerates ALL shortest paths, not just the first.
    """
    start_c = canonical_form(G, start)
    if num_colours(start) <= 4:
        return (0, [[start_c]])

    dist: Dict[CanonicalColouring, int] = {start_c: 0}
    parents: Dict[CanonicalColouring, List[CanonicalColouring]] = {start_c: []}
    queue: deque = deque([start_c])
    targets: List[CanonicalColouring] = []
    target_dist: Optional[int] = None

    while queue:
        current = queue.popleft()
        d = dist[current]

        if target_dist is not None and d > target_dist:
            break

        current_col = colouring_from_canonical(G, current)
        for nbr in all_kempe_neighbours(G, current_col, k):
            nd = d + 1

            if target_dist is not None and nd > target_dist:
                continue

            if nbr not in dist:
                dist[nbr] = nd
                parents[nbr] = [current]
                queue.append(nbr)

                nbr_col = colouring_from_canonical(G, nbr)
                if num_colours(nbr_col) <= 4:
                    if target_dist is None:
                        target_dist = nd
                    targets.append(nbr)

            elif dist[nbr] == nd:
                parents[nbr].append(current)

    if not targets:
        return (-1, [])

    all_paths: List[List[CanonicalColouring]] = []
    for t in targets:
        stack: List[Tuple[CanonicalColouring, List[CanonicalColouring]]] = [(t, [t])]
        while stack:
            node, path_so_far = stack.pop()
            if not parents[node]:
                all_paths.append(list(reversed(path_so_far)))
            else:
                for p in parents[node]:
                    stack.append((p, path_so_far + [p]))

    return (target_dist, all_paths)


def classify_path_safety(G: nx.Graph, H: nx.Graph, v: int, col: Colouring,
                         path: List[CanonicalColouring]
                         ) -> Dict:
    """
    Classify each step of a BFS-optimal path for safety.

    A step is 'unsafe' if it swaps an (a,5)-Kempe chain that is adjacent to v
    AND v has 2+ neighbours in distinct (a,5)-chains (merge-prone).

    Returns per-step classification and overall path safety verdict.
    """
    steps = []
    col_G = dict(col)
    has_unsafe = False

    for i in range(len(path) - 1):
        cur_H = colouring_from_canonical(H, path[i])
        nxt_H = colouring_from_canonical(H, path[i + 1])
        a, b = _identify_swap(H, cur_H, nxt_H)

        swapped_verts = frozenset(u for u in H.nodes() if cur_H[u] != nxt_H[u])

        step_info = {
            'step': i,
            'colour_pair': (a, b),
            'chain_size': len(swapped_verts),
            'is_14_swap': a is not None and b is not None and 5 not in (a, b),
            'is_a5_swap': a is not None and b is not None and 5 in (a, b),
            'chain_adjacent_to_v': False,
            'merge_prone_at_step': False,
            'is_unsafe': False,
        }

        if step_info['is_a5_swap']:
            the_a = a if a != 5 else b
            col_H_cur = {w: col_G[w] for w in H.nodes()}

            chain_adj = any(u in swapped_verts for u in G.neighbors(v))
            step_info['chain_adjacent_to_v'] = chain_adj

            v_nbrs = [u for u in G.neighbors(v)
                       if u in H.nodes() and col_H_cur.get(u, 0) in (the_a, 5)]
            chains_of_nbrs = set()
            for u in v_nbrs:
                chains_of_nbrs.add(get_kempe_chain(H, col_H_cur, u, the_a, 5))

            if len(chains_of_nbrs) >= 2:
                step_info['merge_prone_at_step'] = True
                swapped_chain = None
                if swapped_verts:
                    sv = next(iter(swapped_verts))
                    if col_H_cur.get(sv, 0) in (the_a, 5):
                        swapped_chain = get_kempe_chain(H, col_H_cur, sv, the_a, 5)

                if swapped_chain in chains_of_nbrs:
                    step_info['is_unsafe'] = True
                    has_unsafe = True

        if swapped_verts and a is not None and b is not None:
            col_G = kempe_swap(col_G, swapped_verts, a, b)

        steps.append(step_info)

    return {
        'steps': steps,
        'path_is_safe': not has_unsafe,
        'num_14_swaps': sum(1 for s in steps if s['is_14_swap']),
        'num_a5_swaps': sum(1 for s in steps if s['is_a5_swap']),
        'num_unsafe_steps': sum(1 for s in steps if s['is_unsafe']),
        'num_merge_prone_steps': sum(1 for s in steps if s['merge_prone_at_step']),
    }


def all_paths_merge_analysis(max_n: int = 8) -> Dict:
    """
    GATING ANALYSIS: For each merge-prone case at n <= max_n,
    enumerate ALL BFS-optimal paths and classify safety.

    Returns:
    - total_merge_prone_cases: how many (graph, v, colouring) tuples are merge-prone
    - all_paths_safe: cases where ALL optimal paths avoid unsafe swaps
    - some_paths_unsafe: cases where SOME optimal paths use unsafe swaps
    - all_paths_unsafe: cases where ALL optimal paths use unsafe swaps
    - alternative_swap_classification: what BFS uses instead of unsafe swaps
    """
    db = generate_triangulations(max_n)

    results = {
        'by_n': {},
        'total_merge_prone_colourings': 0,
        'all_paths_safe': 0,
        'some_safe_some_unsafe': 0,
        'all_paths_unsafe': 0,
        'alternative_swap_types': Counter(),
        'path_count_distribution': Counter(),
        'counterexamples': [],
    }

    for n in range(6, max_n + 1):
        n_stats = {
            'graphs': len(db[n]),
            'merge_prone_colourings': 0,
            'all_safe': 0,
            'mixed': 0,
            'all_unsafe': 0,
            'total_paths_enumerated': 0,
        }

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

                    opt_dist, all_opt_paths = bfs_all_optimal_paths(H, col_H, k=5)
                    if opt_dist <= 0 or not all_opt_paths:
                        continue

                    n_stats['merge_prone_colourings'] += 1
                    results['total_merge_prone_colourings'] += 1
                    n_stats['total_paths_enumerated'] += len(all_opt_paths)
                    results['path_count_distribution'][len(all_opt_paths)] += 1

                    safe_count = 0
                    unsafe_count = 0

                    for p in all_opt_paths:
                        classification = classify_path_safety(T, H, v, col, p)
                        if classification['path_is_safe']:
                            safe_count += 1
                            for s in classification['steps']:
                                if s['merge_prone_at_step'] and not s['is_unsafe']:
                                    if s['is_14_swap']:
                                        results['alternative_swap_types'][
                                            f"{{1,2,3,4}}-swap {s['colour_pair']}"] += 1
                                    elif s['is_a5_swap'] and not s['chain_adjacent_to_v']:
                                        results['alternative_swap_types'][
                                            'safe (a,5)-swap (not adjacent)'] += 1
                        else:
                            unsafe_count += 1

                    if unsafe_count == 0:
                        results['all_paths_safe'] += 1
                        n_stats['all_safe'] += 1
                    elif safe_count == 0:
                        results['all_paths_unsafe'] += 1
                        n_stats['all_unsafe'] += 1
                        results['counterexamples'].append({
                            'graph': T.graph.get('name', '?'),
                            'n': n,
                            'vertex': v,
                            'degree': T.degree(v),
                            'num_paths': len(all_opt_paths),
                            'opt_dist': opt_dist,
                        })
                    else:
                        results['some_safe_some_unsafe'] += 1
                        n_stats['mixed'] += 1

        results['by_n'][n] = n_stats
        print(f"n={n}: {n_stats['merge_prone_colourings']} merge-prone, "
              f"all_safe={n_stats['all_safe']}, mixed={n_stats['mixed']}, "
              f"all_unsafe={n_stats['all_unsafe']}, "
              f"paths_enumerated={n_stats['total_paths_enumerated']}")

    return results


if __name__ == '__main__':
    print("=" * 70)
    print("M1-S3: ALL-PATHS BFS Analysis (GATING ITEM)")
    print("Agent 1419, Manager M1, Sub-subagent S3")
    print("=" * 70)

    results = all_paths_merge_analysis(max_n=8)

    print("\n" + "=" * 70)
    print("GATING RESULTS")
    print("=" * 70)
    print(f"Total merge-prone colourings: {results['total_merge_prone_colourings']}")
    print(f"ALL paths safe: {results['all_paths_safe']}")
    print(f"Mixed (some safe, some unsafe): {results['some_safe_some_unsafe']}")
    print(f"ALL paths unsafe: {results['all_paths_unsafe']}")
    print(f"Path count distribution: {dict(results['path_count_distribution'])}")
    print(f"Alternative swap types: {dict(results['alternative_swap_types'])}")

    if results['all_paths_unsafe'] > 0:
        print("\n*** CRITICAL: ALL-PATHS-UNSAFE CASES FOUND ***")
        for ce in results['counterexamples']:
            print(f"  {ce}")
    elif results['some_safe_some_unsafe'] > 0:
        print("\n*** IMPORTANT: Some paths use unsafe swaps — "
              "conjecture should be EXISTENTIAL (there exists a safe path) ***")
    else:
        print("\n*** ALL optimal paths are safe in ALL merge-prone cases ***")
        print("*** Conjecture can remain UNIVERSAL (all paths avoid) ***")

    print("\nPer-n breakdown:")
    for n, ns in sorted(results['by_n'].items()):
        print(f"  n={n}: {ns}")

    print("=" * 70)
