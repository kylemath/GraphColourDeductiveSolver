"""
safe_path_search.py — Agent 1545-M2-S1: Non-Optimal Safe Path Verification.

For each merge-prone (G, v, colouring) case: find the shortest reconfiguration
path to a 4-colouring that avoids ALL merge-prone swaps incident to v.

A swap is "safe" if either:
  (a) It's a {1,2,3,4}-swap (no colour 5 involved), or
  (b) It's an (a,5)-swap where v's neighbors don't have ≥2 distinct (a,5)-chains
      in G-v (not merge-prone for this pair), or
  (c) It's an (a,5)-swap where the swapped chain isn't incident to any of v's
      neighbors with colour a or 5 (so no merge through v is possible).

Key outputs:
  - For the 48 true counterexamples (all BFS-optimal paths unsafe): d_safe, detour cost
  - For the 330 mixed cases: verify d_safe = d_opt
  - For all 163,584 merge-prone cases: verify safe path existence
"""

import sys
import os
import time
import json
from typing import Dict, List, Set, Tuple, Optional, FrozenSet
from collections import Counter, defaultdict, deque
import networkx as nx

sys.path.insert(0, os.path.dirname(__file__))

from kempe_ops import (
    Colouring, CanonicalColouring,
    get_kempe_chain, get_all_kempe_chains, kempe_swap,
    enumerate_colourings, num_colours,
    canonical_form, colouring_from_canonical, all_kempe_neighbours,
)
from triangulation_db import generate_triangulations
from reduction_search import bfs_reduce_to_4, _identify_swap


def safe_kempe_neighbours(
    G: nx.Graph, H: nx.Graph, v: int,
    col_H: Colouring, k: int = 5
) -> List[CanonicalColouring]:
    """
    Return all distinct colourings reachable from col_H by a single SAFE
    Kempe swap in R(G-v, k).

    Precomputes merge-prone status for each (a,5) colour pair once, then
    filters out chains whose swap would merge through v.
    """
    seen: Set[CanonicalColouring] = set()
    results: List[CanonicalColouring] = []

    merge_cache: Dict[int, Tuple[bool, Set[FrozenSet[int]]]] = {}
    for the_a in range(1, 5):
        v_nbrs = [u for u in G.neighbors(v)
                  if u in H.nodes() and col_H.get(u, 0) in (the_a, 5)]
        if len(v_nbrs) < 2:
            merge_cache[the_a] = (False, set())
            continue
        chains = set()
        for u in v_nbrs:
            chains.add(get_kempe_chain(H, col_H, u, the_a, 5))
        merge_cache[the_a] = (len(chains) >= 2, chains)

    for a in range(1, k + 1):
        for b in range(a + 1, k + 1):
            if 5 not in (a, b):
                for chain in get_all_kempe_chains(H, col_H, a, b):
                    new_col = kempe_swap(col_H, chain, a, b)
                    canon = canonical_form(H, new_col)
                    if canon not in seen:
                        seen.add(canon)
                        results.append(canon)
            else:
                the_a = a if a != 5 else b
                is_mp, nbr_chains = merge_cache[the_a]

                for chain in get_all_kempe_chains(H, col_H, a, b):
                    if is_mp and chain in nbr_chains:
                        continue
                    new_col = kempe_swap(col_H, chain, a, b)
                    canon = canonical_form(H, new_col)
                    if canon not in seen:
                        seen.add(canon)
                        results.append(canon)

    return results


def safe_bfs_to_4(
    G: nx.Graph, H: nx.Graph, v: int,
    col_H: Colouring, k: int = 5,
    max_nodes: int = 500_000
) -> Tuple[Optional[int], int]:
    """
    BFS from start colouring to any 4-colouring using only safe swaps.

    Returns (d_safe, nodes_explored) where d_safe is the shortest safe path
    length, or None if no safe path exists within max_nodes BFS frontier.
    """
    start_c = canonical_form(H, col_H)
    if num_colours(col_H) <= 4:
        return (0, 1)

    visited: Set[CanonicalColouring] = {start_c}
    dist: Dict[CanonicalColouring, int] = {start_c: 0}
    queue: deque = deque([start_c])

    while queue:
        if len(visited) > max_nodes:
            return (None, len(visited))

        current = queue.popleft()
        d = dist[current]

        current_col = colouring_from_canonical(H, current)
        for nbr in safe_kempe_neighbours(G, H, v, current_col, k):
            if nbr in visited:
                continue
            visited.add(nbr)
            dist[nbr] = d + 1

            nbr_col = colouring_from_canonical(H, nbr)
            if num_colours(nbr_col) <= 4:
                return (d + 1, len(visited))
            queue.append(nbr)

    return (None, len(visited))


def is_merge_prone(G: nx.Graph, H: nx.Graph, v: int, col_H: Colouring) -> bool:
    """Check if (G, v, col_H) has ≥2 distinct (a,5)-chains for some a."""
    for the_a in range(1, 5):
        v_nbrs = [u for u in G.neighbors(v)
                  if u in H.nodes() and col_H.get(u, 0) in (the_a, 5)]
        if len(v_nbrs) < 2:
            continue
        chains = set()
        for u in v_nbrs:
            chains.add(get_kempe_chain(H, col_H, u, the_a, 5))
        if len(chains) >= 2:
            return True
    return False


def check_path_safety(
    G: nx.Graph, H: nx.Graph, v: int, col: Colouring,
    path: List[CanonicalColouring]
) -> bool:
    """Check if a BFS path is entirely safe (no step causes a merge at v)."""
    col_G = dict(col)

    for i in range(len(path) - 1):
        cur_H = colouring_from_canonical(H, path[i])
        nxt_H = colouring_from_canonical(H, path[i + 1])

        a, b = _identify_swap(H, cur_H, nxt_H)
        if a is None:
            continue

        swapped_verts = frozenset(u for u in H.nodes() if cur_H[u] != nxt_H[u])

        if 5 in (a, b):
            the_a = a if a != 5 else b
            col_H_cur = {w: col_G[w] for w in H.nodes()}
            v_nbrs = [u for u in G.neighbors(v)
                      if u in H.nodes() and col_H_cur.get(u, 0) in (the_a, 5)]
            chains = set()
            for u in v_nbrs:
                chains.add(get_kempe_chain(H, col_H_cur, u, the_a, 5))

            if len(chains) >= 2 and swapped_verts:
                sv = next(iter(swapped_verts))
                if col_H_cur.get(sv, 0) in (the_a, 5):
                    swapped_chain = get_kempe_chain(H, col_H_cur, sv, the_a, 5)
                    if swapped_chain in chains:
                        return False

        if swapped_verts and a is not None:
            col_G = kempe_swap(col_G, swapped_verts, a, b)

    return True


def safe_path_analysis(target_n: int, verbose: bool = True) -> Dict:
    """
    Run safe path analysis on all triangulations at n = target_n.

    For every merge-prone case, finds d_opt (standard BFS) and d_safe
    (shortest path using only safe swaps), computing the detour cost.
    """
    if verbose:
        print(f"\n{'='*70}")
        print(f"Agent 1545-M2-S1: Safe Path Analysis at n = {target_n}")
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
        'safe_bfs_nodes_explored': [],
    }

    for idx, T in enumerate(triangulations):
        name = T.graph.get('name', f'T_{target_n}_{idx}')

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

                path_opt = bfs_reduce_to_4(H, col_H, k=5)
                if path_opt is None or len(path_opt) <= 1:
                    results['safe_at_optimal'] += 1
                    results['detour_cost_histogram'][0] += 1
                    continue

                d_opt = len(path_opt) - 1

                if check_path_safety(T, H, v, col, path_opt):
                    results['safe_at_optimal'] += 1
                    results['detour_cost_histogram'][0] += 1
                    continue

                d_safe, nodes_explored = safe_bfs_to_4(T, H, v, col_H, k=5)
                results['safe_bfs_nodes_explored'].append(nodes_explored)

                if d_safe is None:
                    results['no_safe_path'] += 1
                    results['no_safe_path_cases'].append({
                        'graph': name, 'vertex': v, 'degree': deg,
                        'd_opt': d_opt, 'nodes_explored': nodes_explored,
                    })
                    if verbose:
                        print(f"\n*** KILL CRITERION: NO SAFE PATH at {name}, "
                              f"v={v}, d_opt={d_opt} ***")
                elif d_safe == d_opt:
                    results['safe_alt_at_optimal'] += 1
                    results['detour_cost_histogram'][0] += 1
                else:
                    detour = d_safe - d_opt
                    results['safe_nonoptimal'] += 1
                    results['detour_cost_histogram'][detour] += 1
                    results['max_detour_cost'] = max(
                        results['max_detour_cost'], detour)
                    results['true_counterexamples'].append({
                        'graph': name, 'vertex': v, 'degree': deg,
                        'd_opt': d_opt, 'd_safe': d_safe,
                        'detour_cost': detour,
                    })

        if verbose and ((idx + 1) % max(1, len(triangulations) // 20) == 0
                        or idx == 0):
            elapsed = time.time() - t_start
            rate = (idx + 1) / elapsed if elapsed > 0 else 0
            remaining = (len(triangulations) - idx - 1) / rate if rate > 0 else 0
            print(f"  [{idx+1}/{len(triangulations)}] {name}: "
                  f"mp={results['total_merge_prone']}, "
                  f"safe_opt={results['safe_at_optimal']}, "
                  f"mixed={results['safe_alt_at_optimal']}, "
                  f"detour={results['safe_nonoptimal']}, "
                  f"no_safe={results['no_safe_path']} "
                  f"({elapsed:.0f}s, ~{remaining:.0f}s remaining)")

    results['total_time_s'] = round(time.time() - t_start, 1)
    results['detour_cost_histogram'] = dict(results['detour_cost_histogram'])

    avg_explored = 0
    if results['safe_bfs_nodes_explored']:
        avg_explored = sum(results['safe_bfs_nodes_explored']) / len(
            results['safe_bfs_nodes_explored'])
    results['avg_safe_bfs_nodes'] = round(avg_explored, 1)
    results['max_safe_bfs_nodes'] = (
        max(results['safe_bfs_nodes_explored'])
        if results['safe_bfs_nodes_explored'] else 0)
    del results['safe_bfs_nodes_explored']

    if verbose:
        _print_results(results)

    return results


def _print_results(results: Dict) -> None:
    """Print formatted results summary."""
    n = results['n']
    print(f"\n{'='*70}")
    print(f"SAFE PATH ANALYSIS RESULTS: n = {n}")
    print(f"{'='*70}")
    print(f"  Graphs tested: {results['num_graphs']}")
    print(f"  Colourings tested: {results['total_colourings_tested']}")
    print(f"  Merge-prone cases: {results['total_merge_prone']}")
    print(f"  Safe at optimal (first path): {results['safe_at_optimal']}")
    print(f"  Safe at optimal (alternative): {results['safe_alt_at_optimal']}")
    print(f"  Safe but non-optimal (detour): {results['safe_nonoptimal']}")
    print(f"  NO safe path (KILL): {results['no_safe_path']}")
    print(f"  Max detour cost: {results['max_detour_cost']}")
    print(f"  Detour cost histogram: {results['detour_cost_histogram']}")
    print(f"  Avg safe-BFS nodes explored: {results['avg_safe_bfs_nodes']}")
    print(f"  Max safe-BFS nodes explored: {results['max_safe_bfs_nodes']}")
    print(f"  Computation time: {results['total_time_s']}s")

    if results['no_safe_path_cases']:
        print(f"\n*** KILL CRITERION: {len(results['no_safe_path_cases'])} cases "
              f"with NO safe path ***")
        for case in results['no_safe_path_cases']:
            print(f"  {case}")

    if results['true_counterexamples']:
        print(f"\n  True CEs (safe path non-optimal): "
              f"{len(results['true_counterexamples'])}")
        for ce in results['true_counterexamples'][:20]:
            print(f"    {ce}")
        if len(results['true_counterexamples']) > 20:
            print(f"    ... and {len(results['true_counterexamples']) - 20} more")

    total_safe = (results['safe_at_optimal'] + results['safe_alt_at_optimal']
                  + results['safe_nonoptimal'])
    if results['total_merge_prone'] > 0:
        rate = total_safe / results['total_merge_prone'] * 100
        print(f"\n  Safe path existence rate: {total_safe}/{results['total_merge_prone']} "
              f"({rate:.4f}%)")

    if results['no_safe_path'] == 0:
        print(f"\n  *** Conjecture 5.5' HOLDS at n={n} ***")
    else:
        print(f"\n  *** Conjecture 5.5' FAILS at n={n} ***")


if __name__ == '__main__':
    print("=" * 70)
    print("Agent 1545-M2-S1: Non-Optimal Safe Path Verification")
    print("=" * 70)

    print("\n--- Phase 1: n=8 validation (expect all safe at optimal) ---")
    r8 = safe_path_analysis(8)

    print("\n--- Phase 2: n=9 full analysis ---")
    r9 = safe_path_analysis(9)

    results_path = os.path.join(
        os.path.dirname(__file__), '..', '..', 'backgroundMaterial',
        'agent1545', 'coordinator', 'manager_M2', 'sub_S1',
        'safe_path_results.json')
    os.makedirs(os.path.dirname(results_path), exist_ok=True)

    serializable = {'n8': dict(r8), 'n9': dict(r9)}
    with open(results_path, 'w') as f:
        json.dump(serializable, f, indent=2, default=str)
    print(f"\nResults saved to {results_path}")

    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    for n, r in [(8, r8), (9, r9)]:
        total_safe = (r['safe_at_optimal'] + r['safe_alt_at_optimal']
                      + r['safe_nonoptimal'])
        print(f"  n={n}: {r['total_merge_prone']} merge-prone, "
              f"safe={total_safe}, no_safe={r['no_safe_path']}, "
              f"max_detour={r['max_detour_cost']}, time={r['total_time_s']}s")

    if r9['no_safe_path'] > 0:
        print("\n*** KILL CRITERION TRIGGERED ***")
    else:
        print(f"\n*** Conjecture 5.5' HOLDS through n=9 ***")
        print(f"*** Max detour cost at n=9: {r9['max_detour_cost']} ***")
