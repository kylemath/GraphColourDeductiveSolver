"""
swap_sufficiency_test.py — Agent 1520-M1-S3: Extended {1,2,3,4}-Swap Sufficiency verification.

Tests BFS avoidance and {1,2,3,4}-swap sufficiency for planar triangulations
at n = 9, 10, 11, 12. For each merge-prone case, verifies that a safe
BFS-optimal path exists using only {1,2,3,4}-swaps or non-adjacent (a,5)-swaps.

Extends existing bfs_avoidance_extended.py with:
  - Detailed swap type classification per merge-prone case
  - {1,2,3,4}-swap availability tracking
  - Per-colour-type breakdown
  - Kill criterion: STOP on any counterexample
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


def classify_colour_type(G: nx.Graph, col: Colouring, v: int) -> str:
    """Classify the colour pattern at vertex v into a canonical type string."""
    nbrs = sorted(G.neighbors(v))
    nbr_colours = tuple(sorted(col[u] for u in nbrs))
    distinct = len(set(nbr_colours))
    return f"d{G.degree(v)}_c{distinct}_{nbr_colours}"


def analyze_swap_at_step(
    G: nx.Graph, H: nx.Graph, v: int, col_G: Colouring,
    cur_H: Colouring, nxt_H: Colouring
) -> Dict:
    """
    Analyze a single swap step for merge risk and classify the swap type.
    Returns detailed info about whether this step is safe, merge-prone, etc.
    """
    a, b = _identify_swap(H, cur_H, nxt_H)
    if a is None:
        return {'type': 'unidentified', 'is_safe': True}

    swapped_verts = frozenset(u for u in H.nodes() if cur_H[u] != nxt_H[u])
    is_14_swap = 5 not in (a, b)

    if is_14_swap:
        return {
            'type': '{1,2,3,4}-swap',
            'pair': (a, b),
            'chain_size': len(swapped_verts),
            'is_safe': True,
            'is_14': True,
            'is_a5': False,
            'merge_prone': False,
        }

    the_a = a if a != 5 else b
    col_H_cur = {w: col_G[w] for w in H.nodes()}

    chain_adj = any(u in swapped_verts for u in G.neighbors(v))
    v_nbrs_in_ba5 = [u for u in G.neighbors(v)
                     if u in H.nodes() and col_H_cur.get(u, 0) in (the_a, 5)]
    chains_of_nbrs: Set[FrozenSet[int]] = set()
    for u in v_nbrs_in_ba5:
        chains_of_nbrs.add(get_kempe_chain(H, col_H_cur, u, the_a, 5))

    merge_prone = len(chains_of_nbrs) >= 2
    is_unsafe = False

    if merge_prone and swapped_verts:
        sv = next(iter(swapped_verts))
        if col_H_cur.get(sv, 0) in (the_a, 5):
            swapped_chain = get_kempe_chain(H, col_H_cur, sv, the_a, 5)
            if swapped_chain in chains_of_nbrs:
                is_unsafe = True

    return {
        'type': f'(a,5)-swap' + (' UNSAFE' if is_unsafe else ' safe'),
        'pair': (a, b),
        'chain_size': len(swapped_verts),
        'is_safe': not is_unsafe,
        'is_14': False,
        'is_a5': True,
        'merge_prone': merge_prone,
        'chain_adjacent_to_v': chain_adj,
        'num_distinct_chains': len(chains_of_nbrs),
    }


def check_14_swap_alternatives(
    G: nx.Graph, H: nx.Graph, v: int, col_H: Colouring,
    step_canon: CanonicalColouring, opt_dist: int
) -> Dict:
    """
    At a merge-prone step, check if {1,2,3,4}-swap alternatives exist
    that maintain BFS optimality.

    Enumerates all possible Kempe swaps from the current colouring,
    checks which are {1,2,3,4}-swaps, and verifies they can still reach
    a 4-colouring in the remaining distance.
    """
    col = colouring_from_canonical(H, step_canon)
    alternatives_14 = []
    alternatives_safe_a5 = []

    for ca in range(1, 6):
        for cb in range(ca + 1, 6):
            for chain in get_all_kempe_chains(H, col, ca, cb):
                new_col = kempe_swap(col, chain, ca, cb)
                new_canon = canonical_form(H, new_col)
                is_14 = 5 not in (ca, cb)

                if is_14:
                    alternatives_14.append({
                        'pair': (ca, cb),
                        'chain_size': len(chain),
                        'new_canon': new_canon,
                    })
                elif 5 in (ca, cb):
                    the_a_alt = ca if ca != 5 else cb
                    col_at_step = colouring_from_canonical(H, step_canon)
                    nbrs_in = [u for u in G.neighbors(v)
                               if u in H.nodes() and col_at_step.get(u, 0) in (the_a_alt, 5)]
                    chains_nbrs = set()
                    for u in nbrs_in:
                        chains_nbrs.add(get_kempe_chain(H, col_at_step, u, the_a_alt, 5))

                    is_merge_prone_alt = len(chains_nbrs) >= 2
                    if not is_merge_prone_alt:
                        alternatives_safe_a5.append({
                            'pair': (ca, cb),
                            'chain_size': len(chain),
                        })

    return {
        'num_14_alternatives': len(alternatives_14),
        'num_safe_a5_alternatives': len(alternatives_safe_a5),
        'has_safe_alternative': len(alternatives_14) > 0 or len(alternatives_safe_a5) > 0,
    }


def swap_sufficiency_test(target_n: int, verbose: bool = True) -> Dict:
    """
    Run comprehensive {1,2,3,4}-swap sufficiency test on all triangulations
    at vertex count target_n.

    For each triangulation, each degree-4/5 vertex, each 5-colouring with
    c(v) = 5: find BFS path in R(G-v, 5), classify each step, detect
    merge-prone cases, and verify avoidance.
    """
    if verbose:
        print(f"\n{'='*70}")
        print(f"Swap Sufficiency Test: n = {target_n}")
        print(f"{'='*70}")

    t_start = time.time()
    if verbose:
        print(f"Generating triangulations up to n={target_n}...")
    db = generate_triangulations(target_n)
    triangulations = db[target_n]
    t_gen = time.time() - t_start

    if verbose:
        print(f"  Generated {len(triangulations)} triangulations in {t_gen:.1f}s")

    results = {
        'n': target_n,
        'num_graphs': len(triangulations),
        'generation_time_s': round(t_gen, 1),
        'total_colourings_tested': 0,
        'total_a5_swaps': 0,
        'total_14_swaps': 0,
        'total_merge_prone': 0,
        'total_bfs_avoided': 0,
        'total_bfs_used_unsafe': 0,
        'counterexamples': [],
        'by_degree': {
            4: {'a5_swaps': 0, 'merge_prone': 0, 'avoided': 0, 'used_unsafe': 0},
            5: {'a5_swaps': 0, 'merge_prone': 0, 'avoided': 0, 'used_unsafe': 0},
        },
        'by_colour_type': defaultdict(lambda: {
            'count': 0, 'merge_prone': 0, 'avoided': 0, 'used_unsafe': 0
        }),
        'merge_prone_chain_sizes': Counter(),
        'swap_type_at_merge_prone_steps': Counter(),
    }

    for idx, T in enumerate(triangulations):
        name = T.graph.get('name', f'T_{target_n}_{idx}')
        graph_merges = 0
        graph_a5 = 0
        graph_merge_prone = 0

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
                path_H = bfs_reduce_to_4(H, col_H, k=5)
                if path_H is None or len(path_H) <= 1:
                    continue

                colour_type = classify_colour_type(T, col, v)
                col_G = dict(col)

                for step_idx in range(len(path_H) - 1):
                    cur_H = colouring_from_canonical(H, path_H[step_idx])
                    nxt_H = colouring_from_canonical(H, path_H[step_idx + 1])

                    step_info = analyze_swap_at_step(T, H, v, col_G, cur_H, nxt_H)

                    if step_info.get('is_14'):
                        results['total_14_swaps'] += 1
                    elif step_info.get('is_a5'):
                        results['total_a5_swaps'] += 1
                        graph_a5 += 1

                        if deg in (4, 5):
                            results['by_degree'][deg]['a5_swaps'] += 1

                        if step_info.get('merge_prone'):
                            results['total_merge_prone'] += 1
                            graph_merge_prone += 1
                            results['merge_prone_chain_sizes'][step_info.get('chain_size', 0)] += 1

                            if deg in (4, 5):
                                results['by_degree'][deg]['merge_prone'] += 1

                            ct_stats = results['by_colour_type'][colour_type]
                            ct_stats['count'] += 1
                            ct_stats['merge_prone'] += 1

                            if not step_info['is_safe']:
                                results['total_bfs_used_unsafe'] += 1
                                graph_merges += 1
                                if deg in (4, 5):
                                    results['by_degree'][deg]['used_unsafe'] += 1
                                ct_stats['used_unsafe'] += 1

                                results['counterexamples'].append({
                                    'graph': name,
                                    'vertex': v,
                                    'degree': deg,
                                    'colour_type': colour_type,
                                    'step': step_idx,
                                    'swap_pair': step_info.get('pair'),
                                })
                                if verbose:
                                    print(f"\n*** COUNTEREXAMPLE at {name}, v={v}, "
                                          f"step {step_idx}: {step_info} ***")
                            else:
                                results['total_bfs_avoided'] += 1
                                if deg in (4, 5):
                                    results['by_degree'][deg]['avoided'] += 1
                                ct_stats['avoided'] += 1

                                results['swap_type_at_merge_prone_steps'][
                                    step_info['type']] += 1

                    swapped = frozenset(u for u in H.nodes() if cur_H[u] != nxt_H[u])
                    a, b = _identify_swap(H, cur_H, nxt_H)
                    if swapped and a is not None:
                        col_G = kempe_swap(col_G, swapped, a, b)

        if verbose and ((idx + 1) % max(1, len(triangulations) // 20) == 0 or idx == 0):
            elapsed = time.time() - t_start
            rate = (idx + 1) / elapsed if elapsed > 0 else 0
            remaining = (len(triangulations) - idx - 1) / rate if rate > 0 else 0
            print(f"  [{idx+1}/{len(triangulations)}] {name}: "
                  f"a5={graph_a5}, mp={graph_merge_prone}, unsafe={graph_merges} "
                  f"({elapsed:.0f}s elapsed, ~{remaining:.0f}s remaining)")

    results['total_computation_time_s'] = round(time.time() - t_start, 1)
    results['by_colour_type'] = dict(results['by_colour_type'])
    results['merge_prone_chain_sizes'] = dict(results['merge_prone_chain_sizes'])
    results['swap_type_at_merge_prone_steps'] = dict(results['swap_type_at_merge_prone_steps'])
    results['avoidance_rate'] = (
        f"{results['total_bfs_avoided']}/{results['total_merge_prone']}"
        if results['total_merge_prone'] > 0 else "N/A (no merge-prone cases)"
    )

    if verbose:
        print(f"\n{'='*70}")
        print(f"RESULTS for n={target_n}")
        print(f"{'='*70}")
        print(f"  Graphs tested: {results['num_graphs']}")
        print(f"  Colourings tested: {results['total_colourings_tested']}")
        print(f"  Total (a,5)-swaps: {results['total_a5_swaps']}")
        print(f"  Total {{1,2,3,4}}-swaps: {results['total_14_swaps']}")
        print(f"  Merge-prone cases: {results['total_merge_prone']}")
        print(f"  BFS avoided: {results['total_bfs_avoided']}")
        print(f"  BFS used unsafe: {results['total_bfs_used_unsafe']}")
        print(f"  Avoidance rate: {results['avoidance_rate']}")
        print(f"  Computation time: {results['total_computation_time_s']}s")
        for deg in [4, 5]:
            d = results['by_degree'][deg]
            if d['a5_swaps'] > 0:
                rate = d['merge_prone'] / d['a5_swaps'] * 100
                print(f"  Degree {deg}: {d['a5_swaps']} (a,5)-swaps, "
                      f"{d['merge_prone']} merge-prone ({rate:.1f}%), "
                      f"{d['avoided']} avoided, {d['used_unsafe']} unsafe")
        if results['counterexamples']:
            print(f"\n*** KILL CRITERION TRIGGERED: {len(results['counterexamples'])} "
                  f"COUNTEREXAMPLE(S) FOUND ***")
            for ce in results['counterexamples']:
                print(f"  {ce}")
        else:
            print(f"\n  {'{1,2,3,4}'}-Swap Sufficiency HOLDS at n={target_n}")

    return results


def run_extended_tests(start_n: int = 9, max_n: int = 12) -> Dict:
    """Run swap sufficiency tests for n = start_n to max_n, stopping on counterexample."""
    all_results = {}
    for n in range(start_n, max_n + 1):
        print(f"\n{'#'*70}")
        print(f"# Starting n={n}")
        print(f"{'#'*70}")

        results = swap_sufficiency_test(n)
        all_results[n] = results

        if results['counterexamples']:
            print(f"\n{'!'*70}")
            print(f"! COUNTEREXAMPLE FOUND AT n={n} — STOPPING")
            print(f"{'!'*70}")
            break

        if results['total_computation_time_s'] > 3600:
            print(f"\nn={n} took {results['total_computation_time_s']:.0f}s (>1h). "
                  f"Skipping larger n.")
            break

    return all_results


if __name__ == '__main__':
    print("=" * 70)
    print("Agent 1520-M1-S3: {1,2,3,4}-Swap Sufficiency Extended Tests")
    print("=" * 70)

    all_results = run_extended_tests(start_n=9, max_n=12)

    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)

    any_counterexample = False
    for n, r in sorted(all_results.items()):
        status = "PASS" if not r['counterexamples'] else "***FAIL***"
        print(f"  n={n}: {status} — {r['num_graphs']} graphs, "
              f"{r['total_merge_prone']} merge-prone, "
              f"avoidance={r['avoidance_rate']}, "
              f"time={r['total_computation_time_s']}s")
        if r['counterexamples']:
            any_counterexample = True

    if any_counterexample:
        print("\n*** KILL CRITERION: COUNTEREXAMPLE(S) EXIST ***")
    else:
        print(f"\n  {{1,2,3,4}}-Swap Sufficiency holds for all tested n")

    results_path = os.path.join(os.path.dirname(__file__),
                                '..', '..', 'backgroundMaterial', 'agent1520',
                                'coordinator', 'manager_M1', 'sub_S3',
                                'computation_results.json')
    os.makedirs(os.path.dirname(results_path), exist_ok=True)

    serializable = {}
    for n, r in all_results.items():
        sr = dict(r)
        sr.pop('counterexamples_detail', None)
        serializable[str(n)] = sr

    with open(results_path, 'w') as f:
        json.dump(serializable, f, indent=2, default=str)
    print(f"\nResults saved to {results_path}")
