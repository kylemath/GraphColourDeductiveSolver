"""
merge_tolerant_check.py — Agent 1545-M1-S1: Post-Merge Colourability Check.

For each of the 48 counterexamples to {1,2,3,4}-Swap Sufficiency:
  1. Follow the BFS-optimal path in R(G-v, 5) to a 4-colouring of G-v
  2. At each step, track colours on v's neighbours
  3. After the FULL path: check if v has a free colour in {1,2,3,4}
  4. After each INTERMEDIATE step: check free colours for v

The merge-tolerant lifting thesis: even if the BFS path uses merge-prone
swaps, the FINAL 4-colouring of G-v may still leave a free colour for v.

For deg(v) ≤ 4: pigeonhole guarantees a free colour IF fewer than 4 distinct
colours appear on v's neighbours. But 4 neighbours CAN use all 4 colours.

For deg(v) = 5: at most 4 colours from {1,2,3,4} on 5 neighbours. A free
colour exists iff fewer than 4 distinct colours appear.
"""

import sys
import os
import json
import time
from typing import Dict, List, Set, Tuple, Optional, FrozenSet
from collections import defaultdict
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
from verify_counterexamples import (
    is_step_unsafe, check_path_safety, find_safe_bfs_path,
)


def find_all_bfs_paths_to_4col(
    H: nx.Graph, col_H: Colouring, k: int = 5, max_paths: int = 10000
) -> List[List[CanonicalColouring]]:
    """Enumerate ALL BFS-optimal paths from col_H to a 4-colouring in R(H, k)."""
    start_c = canonical_form(H, col_H)
    if num_colours(col_H) <= 4:
        return [[start_c]]

    dist: Dict[CanonicalColouring, int] = {start_c: 0}
    parents: Dict[CanonicalColouring, List[CanonicalColouring]] = {start_c: []}
    queue = [start_c]
    target_dist: Optional[int] = None
    targets: List[CanonicalColouring] = []

    while queue:
        next_queue = []
        for current in queue:
            d = dist[current]
            if target_dist is not None and d >= target_dist:
                continue
            current_col = colouring_from_canonical(H, current)
            for nbr in all_kempe_neighbours(H, current_col, k):
                nd = d + 1
                if target_dist is not None and nd > target_dist:
                    continue
                if nbr not in dist:
                    dist[nbr] = nd
                    parents[nbr] = [current]
                    next_queue.append(nbr)
                    nbr_col = colouring_from_canonical(H, nbr)
                    if num_colours(nbr_col) <= 4:
                        if target_dist is None:
                            target_dist = nd
                        targets.append(nbr)
                elif dist[nbr] == nd:
                    parents[nbr].append(current)
        queue = next_queue

    if not targets:
        return []

    all_paths: List[List[CanonicalColouring]] = []
    for t in targets:
        stack: List[Tuple[CanonicalColouring, List[CanonicalColouring]]] = [(t, [t])]
        while stack and len(all_paths) < max_paths:
            node, path_so_far = stack.pop()
            if not parents[node]:
                all_paths.append(list(reversed(path_so_far)))
            else:
                for p in parents[node]:
                    stack.append((p, path_so_far + [p]))
    return all_paths


def check_merge_tolerant_lifting(
    T: nx.Graph, v: int, col: Colouring, verbose: bool = False
) -> Dict:
    """
    For a single (graph, vertex, colouring) case:
    Follow every BFS-optimal path in R(G-v, 5) to a 4-colouring.
    After each path completes, check if v has a free colour in {1,2,3,4}.

    Returns detailed info about harmlessness of each path.
    """
    H = T.copy()
    H.remove_node(v)
    col_H = {u: col[u] for u in H.nodes()}
    nbrs = sorted(T.neighbors(v))

    all_paths = find_all_bfs_paths_to_4col(H, col_H, k=5, max_paths=100)

    if not all_paths:
        return {
            'status': 'NO_PATH',
            'num_paths': 0,
            'all_harmless': False,
            'any_harmless': False,
        }

    path_results = []
    any_harmless = False
    all_harmless = True

    for path_idx, path in enumerate(all_paths):
        final_col = colouring_from_canonical(H, path[-1])
        nbr_colours_final = {u: final_col[u] for u in nbrs}
        distinct_final = set(nbr_colours_final.values())
        free_colours_final = {1, 2, 3, 4} - distinct_final
        harmless = len(free_colours_final) > 0

        step_details = []
        for step_idx in range(len(path) - 1):
            cur_col = colouring_from_canonical(H, path[step_idx])
            nxt_col = colouring_from_canonical(H, path[step_idx + 1])
            a, b = _identify_swap(H, cur_col, nxt_col)
            swapped = frozenset(u for u in H.nodes() if cur_col[u] != nxt_col[u])

            nbr_colours_after = {u: nxt_col[u] for u in nbrs}
            distinct_after = set(nbr_colours_after.values())
            free_after = {1, 2, 3, 4} - distinct_after

            is_a5 = a is not None and 5 in (a, b)
            is_unsafe = False
            if is_a5:
                the_a = a if a != 5 else b
                v_nbrs_in_ba5 = [u for u in nbrs
                                 if u in H.nodes() and cur_col.get(u) in (the_a, 5)]
                chains = set()
                for u in v_nbrs_in_ba5:
                    chains.add(get_kempe_chain(H, cur_col, u, the_a, 5))
                merge_prone = len(chains) >= 2
                if merge_prone and swapped:
                    sv = next(iter(swapped))
                    if cur_col.get(sv) in (the_a, 5):
                        sc = get_kempe_chain(H, cur_col, sv, the_a, 5)
                        if sc in chains:
                            is_unsafe = True

            step_details.append({
                'step': step_idx,
                'swap_pair': (a, b),
                'chain_size': len(swapped),
                'is_a5': is_a5,
                'is_unsafe': is_unsafe,
                'nbr_colours_after': nbr_colours_after,
                'distinct_colours': len(distinct_after),
                'free_colours': sorted(free_after),
            })

        if harmless:
            any_harmless = True
        else:
            all_harmless = False

        pr = {
            'path_idx': path_idx,
            'path_length': len(path),
            'nbr_colours_final': nbr_colours_final,
            'distinct_colours_final': len(distinct_final),
            'free_colours_final': sorted(free_colours_final),
            'harmless': harmless,
            'step_details': step_details,
        }
        path_results.append(pr)

        if verbose and path_idx < 3:
            tag = "HARMLESS" if harmless else "HARMFUL"
            print(f"    Path {path_idx}: {tag}, "
                  f"free={sorted(free_colours_final)}, "
                  f"nbr_cols={nbr_colours_final}")
            for sd in step_details:
                u_tag = " UNSAFE" if sd['is_unsafe'] else ""
                print(f"      Step {sd['step']}: {sd['swap_pair']}{u_tag}, "
                      f"free_after={sd['free_colours']}")

    return {
        'status': 'CHECKED',
        'num_paths': len(all_paths),
        'all_harmless': all_harmless,
        'any_harmless': any_harmless,
        'num_harmless': sum(1 for p in path_results if p['harmless']),
        'num_harmful': sum(1 for p in path_results if not p['harmless']),
        'path_results': path_results,
    }


def run_full_check(verbose: bool = True) -> Dict:
    """
    Run post-merge colourability check on all 48 counterexamples.
    """
    print("=" * 70)
    print("Agent 1545-M1-S1: Post-Merge Colourability Check")
    print("=" * 70)

    t_start = time.time()
    db = generate_triangulations(9)
    t_gen = time.time() - t_start
    print(f"Generated triangulations in {t_gen:.1f}s")

    counterexample_specs = {
        25: [3],  # T_9_25, vertex 3, deg 5
        35: [6],  # T_9_35, vertex 6, deg 4
    }

    results = {
        'total_counterexamples': 0,
        'total_harmless': 0,
        'total_harmful': 0,
        'total_any_harmless': 0,
        'by_graph': {},
        'all_details': [],
    }

    for graph_idx, vertices in counterexample_specs.items():
        T = db[9][graph_idx]
        name = T.graph.get('name', f'T_9_{graph_idx}')
        print(f"\n{'='*50}")
        print(f"Graph: {name}")
        print(f"Edges: {T.number_of_edges()}, Nodes: {T.number_of_nodes()}")
        print(f"Degree sequence: {sorted([T.degree(n) for n in T.nodes()])}")

        for v in vertices:
            deg = T.degree(v)
            nbrs = sorted(T.neighbors(v))
            print(f"\n  Vertex {v}, degree {deg}, neighbours {nbrs}")

            all_cols = enumerate_colourings(T, 5)
            v5_cols = [c for c in all_cols if c[v] == 5 and num_colours(c) == 5]
            print(f"  5-colourings with c(v)=5: {len(v5_cols)}")

            H = T.copy()
            H.remove_node(v)

            ce_count = 0
            harmless_count = 0
            harmful_count = 0
            any_harmless_count = 0

            for col in v5_cols:
                col_H = {u: col[u] for u in H.nodes()}

                is_mp = False
                for a in range(1, 5):
                    nbrs_in = [u for u in nbrs
                               if u in H.nodes() and col_H.get(u) in (a, 5)]
                    if len(nbrs_in) < 2:
                        continue
                    chains = set()
                    for u in nbrs_in:
                        chains.add(get_kempe_chain(H, col_H, u, a, 5))
                    if len(chains) >= 2:
                        is_mp = True
                        break
                if not is_mp:
                    continue

                first_path = bfs_reduce_to_4(H, col_H, k=5)
                if first_path is None or len(first_path) <= 1:
                    continue

                first_safe = check_path_safety(T, H, v, col, first_path)
                if first_safe:
                    continue

                verif = find_safe_bfs_path(T, H, v, col, max_paths=10000)
                if verif['safe_path_exists']:
                    continue

                ce_count += 1
                results['total_counterexamples'] += 1

                check = check_merge_tolerant_lifting(T, v, col, verbose=(ce_count <= 3))

                detail = {
                    'graph': name,
                    'graph_idx': graph_idx,
                    'vertex': v,
                    'degree': deg,
                    'colouring': dict(col),
                    'nbr_colours': {u: col[u] for u in nbrs},
                    'check': check,
                }
                results['all_details'].append(detail)

                if check['all_harmless']:
                    harmless_count += 1
                    results['total_harmless'] += 1
                elif check['any_harmless']:
                    any_harmless_count += 1
                    results['total_any_harmless'] += 1
                else:
                    harmful_count += 1
                    results['total_harmful'] += 1
                    if harmful_count <= 3:
                        print(f"\n  *** HARMFUL CASE #{harmful_count}: "
                              f"colouring={dict(col)}")
                        for pr in check['path_results'][:2]:
                            print(f"      Path: nbr_cols={pr['nbr_colours_final']}, "
                                  f"free={pr['free_colours_final']}")

            print(f"\n  Counterexamples at {name} v={v}: {ce_count}")
            print(f"    All paths harmless: {harmless_count}")
            print(f"    Some paths harmless: {any_harmless_count}")
            print(f"    ALL paths harmful: {harmful_count}")

            results['by_graph'][f"{name}_v{v}"] = {
                'total_ces': ce_count,
                'all_harmless': harmless_count,
                'any_harmless': any_harmless_count,
                'all_harmful': harmful_count,
            }

    results['total_time_s'] = round(time.time() - t_start, 1)

    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"Total counterexamples checked: {results['total_counterexamples']}")
    print(f"  All BFS paths harmless: {results['total_harmless']}")
    print(f"  Some BFS paths harmless: {results['total_any_harmless']}")
    print(f"  ALL BFS paths harmful: {results['total_harmful']}")
    print(f"  Time: {results['total_time_s']}s")

    if results['total_harmful'] == 0:
        print(f"\n*** MERGE-TOLERANT LIFTING SUCCEEDS ***")
        print("Every counterexample has at least one BFS path where the final")
        print("4-colouring of G-v leaves a free colour for v.")
    else:
        print(f"\n*** MERGE-TOLERANT LIFTING FAILS for {results['total_harmful']} cases ***")
        print("Some counterexamples have NO BFS path where v can be recoloured.")

    return results


def check_all_4col_targets(verbose: bool = True) -> Dict:
    """
    Stronger check: for each counterexample, enumerate ALL reachable
    4-colourings of G-v (not just BFS-optimal) and check each for v-extensibility.

    If even ONE reachable 4-colouring allows v to be coloured, the merge-tolerant
    approach works (with a possibly non-optimal path).
    """
    print("\n" + "=" * 70)
    print("Agent 1545-M1-S1: EXHAUSTIVE 4-Colouring Target Check")
    print("=" * 70)

    t_start = time.time()
    db = generate_triangulations(9)

    counterexample_specs = {25: [3], 35: [6]}
    results = {
        'total_ces': 0,
        'extensible': 0,
        'not_extensible': 0,
        'details': [],
    }

    for graph_idx, vertices in counterexample_specs.items():
        T = db[9][graph_idx]
        name = T.graph.get('name', f'T_9_{graph_idx}')

        for v in vertices:
            H = T.copy()
            H.remove_node(v)
            nbrs = sorted(T.neighbors(v))

            all_cols_T = enumerate_colourings(T, 5)
            v5_cols = [c for c in all_cols_T if c[v] == 5 and num_colours(c) == 5]

            all_cols_H = enumerate_colourings(H, 5)
            four_cols_H = [c for c in all_cols_H if num_colours(c) <= 4]
            four_col_canons = set()
            for c in four_cols_H:
                four_col_canons.add(canonical_form(H, c))

            extensible_4cols = set()
            non_extensible_4cols = set()
            for canon in four_col_canons:
                c4 = colouring_from_canonical(H, canon)
                nbr_colours = set(c4[u] for u in nbrs)
                free = {1, 2, 3, 4} - nbr_colours
                if free:
                    extensible_4cols.add(canon)
                else:
                    non_extensible_4cols.add(canon)

            if verbose:
                print(f"\n  {name} v={v}: {len(four_col_canons)} distinct 4-colourings of G-v")
                print(f"    Extensible (v has free colour): {len(extensible_4cols)}")
                print(f"    Non-extensible (no free colour): {len(non_extensible_4cols)}")

            for col in v5_cols:
                col_H = {u: col[u] for u in H.nodes()}

                is_mp = False
                for a in range(1, 5):
                    nbrs_in = [u for u in nbrs
                               if u in H.nodes() and col_H.get(u) in (a, 5)]
                    if len(nbrs_in) < 2:
                        continue
                    chains = set()
                    for u in nbrs_in:
                        chains.add(get_kempe_chain(H, col_H, u, a, 5))
                    if len(chains) >= 2:
                        is_mp = True
                        break
                if not is_mp:
                    continue

                first_path = bfs_reduce_to_4(H, col_H, k=5)
                if first_path is None or len(first_path) <= 1:
                    continue

                first_safe = check_path_safety(T, H, v, col, first_path)
                if first_safe:
                    continue

                verif = find_safe_bfs_path(T, H, v, col, max_paths=10000)
                if verif['safe_path_exists']:
                    continue

                results['total_ces'] += 1

                bfs_target = first_path[-1]
                bfs_extensible = bfs_target in extensible_4cols

                all_paths = find_all_bfs_paths_to_4col(H, col_H, k=5, max_paths=100)
                all_targets = set(p[-1] for p in all_paths)
                any_target_extensible = any(t in extensible_4cols for t in all_targets)

                start_c = canonical_form(H, col_H)
                reachable_ext = start_c in extensible_4cols
                if not reachable_ext:
                    from collections import deque
                    visited = {start_c}
                    q = deque([start_c])
                    found_extensible = False
                    while q and not found_extensible:
                        cur = q.popleft()
                        cur_col = colouring_from_canonical(H, cur)
                        for nbr_c in all_kempe_neighbours(H, cur_col, 5):
                            if nbr_c in visited:
                                continue
                            visited.add(nbr_c)
                            if nbr_c in extensible_4cols:
                                found_extensible = True
                                break
                            q.append(nbr_c)
                    reachable_ext = found_extensible

                detail = {
                    'graph': name,
                    'vertex': v,
                    'colouring': dict(col),
                    'bfs_target_extensible': bfs_extensible,
                    'any_bfs_target_extensible': any_target_extensible,
                    'any_reachable_extensible': reachable_ext,
                    'num_bfs_targets': len(all_targets),
                }
                results['details'].append(detail)

                if reachable_ext:
                    results['extensible'] += 1
                else:
                    results['not_extensible'] += 1

    results['total_time_s'] = round(time.time() - t_start, 1)

    print(f"\n{'='*70}")
    print("EXHAUSTIVE CHECK SUMMARY")
    print(f"{'='*70}")
    print(f"Total CEs: {results['total_ces']}")
    print(f"  Extensible (some reachable 4-col has free colour for v): {results['extensible']}")
    print(f"  Not extensible: {results['not_extensible']}")

    return results


if __name__ == '__main__':
    results_bfs = run_full_check(verbose=True)

    results_exhaustive = check_all_4col_targets(verbose=True)

    out_dir = os.path.join(
        os.path.dirname(__file__), '..', '..',
        'backgroundMaterial', 'agent1545', 'coordinator',
        'manager_M1', 'sub_S1'
    )
    os.makedirs(out_dir, exist_ok=True)

    serializable_bfs = {
        k: v for k, v in results_bfs.items() if k != 'all_details'
    }
    serializable_bfs['detail_count'] = len(results_bfs.get('all_details', []))

    summary_details = []
    for d in results_bfs.get('all_details', []):
        sd = {
            'graph': d['graph'],
            'vertex': d['vertex'],
            'degree': d['degree'],
            'colouring': d['colouring'],
            'nbr_colours': d['nbr_colours'],
            'all_harmless': d['check']['all_harmless'],
            'any_harmless': d['check']['any_harmless'],
            'num_paths': d['check']['num_paths'],
        }
        if d['check'].get('path_results'):
            sd['sample_path'] = {
                'nbr_colours_final': d['check']['path_results'][0]['nbr_colours_final'],
                'free_colours_final': d['check']['path_results'][0]['free_colours_final'],
                'harmless': d['check']['path_results'][0]['harmless'],
            }
        summary_details.append(sd)

    out_path = os.path.join(out_dir, 'merge_tolerant_results.json')
    with open(out_path, 'w') as f:
        json.dump({
            'bfs_summary': serializable_bfs,
            'exhaustive_summary': {k: v for k, v in results_exhaustive.items() if k != 'details'},
            'exhaustive_details': results_exhaustive.get('details', []),
            'ce_details': summary_details,
        }, f, indent=2, default=str)
    print(f"\nResults saved to {out_path}")
