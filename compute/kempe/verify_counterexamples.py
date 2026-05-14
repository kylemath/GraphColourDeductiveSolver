"""
verify_counterexamples.py — Verify reported counterexamples from swap_sufficiency_test.

CRITICAL DISTINCTION: The {1,2,3,4}-Swap Sufficiency conjecture is EXISTENTIAL:
  "there EXISTS a BFS-optimal path that is safe"
NOT universal ("every BFS-optimal path is safe").

The initial test only checked ONE BFS path. If that path uses an unsafe swap,
it's NOT a counterexample if other BFS-optimal paths of the same length are safe.

A TRUE counterexample requires: ALL BFS-optimal paths use at least one unsafe swap.

This script verifies each reported case by checking if ANY safe alternative
BFS-optimal path exists.
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(__file__))

from typing import Dict, List, Set, Tuple, Optional, FrozenSet
from collections import deque, Counter
import networkx as nx

from kempe_ops import (
    Colouring, CanonicalColouring,
    get_kempe_chain, get_all_kempe_chains, kempe_swap,
    enumerate_colourings, num_colours,
    canonical_form, colouring_from_canonical, all_kempe_neighbours,
)
from triangulation_db import generate_triangulations
from reduction_search import bfs_reduce_to_4, _identify_swap, bulk_distance_to_4col


def is_step_unsafe(G: nx.Graph, H: nx.Graph, v: int,
                   col_G: Colouring, cur_H: Colouring,
                   nxt_H: Colouring) -> bool:
    """Check if a single BFS step would cause a merge at vertex v."""
    a, b = _identify_swap(H, cur_H, nxt_H)
    if a is None or 5 not in (a, b):
        return False

    the_a = a if a != 5 else b
    col_H_cur = {w: col_G[w] for w in H.nodes()}
    swapped_verts = frozenset(u for u in H.nodes() if cur_H[u] != nxt_H[u])

    v_nbrs_in_ba5 = [u for u in G.neighbors(v)
                     if u in H.nodes() and col_H_cur.get(u, 0) in (the_a, 5)]
    chains: Set[FrozenSet[int]] = set()
    for u in v_nbrs_in_ba5:
        chains.add(get_kempe_chain(H, col_H_cur, u, the_a, 5))

    if len(chains) < 2:
        return False

    if swapped_verts:
        sv = next(iter(swapped_verts))
        if col_H_cur.get(sv, 0) in (the_a, 5):
            swapped_chain = get_kempe_chain(H, col_H_cur, sv, the_a, 5)
            if swapped_chain in chains:
                return True

    return False


def find_safe_bfs_path(G: nx.Graph, H: nx.Graph, v: int,
                       col: Colouring, max_paths: int = 1000) -> Dict:
    """
    For a given merge-prone (G, v, colouring), search for a safe BFS-optimal path.

    Uses modified BFS that tracks whether each partial path has hit an unsafe step.
    Returns info about whether a safe path exists.
    """
    col_H = {u: col[u] for u in H.nodes()}
    start_c = canonical_form(H, col_H)

    if num_colours(col_H) <= 4:
        return {'safe_path_exists': True, 'reason': 'already 4-colourable'}

    dist: Dict[CanonicalColouring, int] = {start_c: 0}
    queue: deque = deque([start_c])
    target_dist: Optional[int] = None
    targets: List[CanonicalColouring] = []
    parents: Dict[CanonicalColouring, List[CanonicalColouring]] = {start_c: []}

    while queue:
        current = queue.popleft()
        d = dist[current]
        if target_dist is not None and d > target_dist:
            break

        current_col = colouring_from_canonical(H, current)
        for nbr in all_kempe_neighbours(H, current_col, 5):
            nd = d + 1
            if target_dist is not None and nd > target_dist:
                continue

            if nbr not in dist:
                dist[nbr] = nd
                parents[nbr] = [current]
                queue.append(nbr)
                nbr_col = colouring_from_canonical(H, nbr)
                if num_colours(nbr_col) <= 4:
                    if target_dist is None:
                        target_dist = nd
                    targets.append(nbr)
            elif dist[nbr] == nd:
                parents[nbr].append(current)

    if not targets:
        return {'safe_path_exists': False, 'reason': 'no 4-colouring reachable'}

    paths_checked = 0
    safe_found = False
    unsafe_count = 0

    for t in targets:
        stack: List[Tuple[CanonicalColouring, List[CanonicalColouring]]] = [(t, [t])]
        while stack and paths_checked < max_paths:
            node, path_so_far = stack.pop()
            if not parents[node]:
                full_path = list(reversed(path_so_far))
                paths_checked += 1

                path_safe = check_path_safety(G, H, v, col, full_path)
                if path_safe:
                    safe_found = True
                    return {
                        'safe_path_exists': True,
                        'paths_checked': paths_checked,
                        'path_length': len(full_path),
                    }
                else:
                    unsafe_count += 1
            else:
                for p in parents[node]:
                    stack.append((p, path_so_far + [p]))

    return {
        'safe_path_exists': safe_found,
        'paths_checked': paths_checked,
        'unsafe_count': unsafe_count,
        'reason': 'exhausted' if paths_checked < max_paths else 'max_paths_reached',
    }


def check_path_safety(G: nx.Graph, H: nx.Graph, v: int,
                      col: Colouring,
                      path: List[CanonicalColouring]) -> bool:
    """Check if an entire BFS path is safe (no merge-prone steps use unsafe chains)."""
    col_G = dict(col)

    for i in range(len(path) - 1):
        cur_H = colouring_from_canonical(H, path[i])
        nxt_H = colouring_from_canonical(H, path[i + 1])

        if is_step_unsafe(G, H, v, col_G, cur_H, nxt_H):
            return False

        swapped = frozenset(u for u in H.nodes() if cur_H[u] != nxt_H[u])
        a, b = _identify_swap(H, cur_H, nxt_H)
        if swapped and a is not None:
            col_G = kempe_swap(col_G, swapped, a, b)

    return True


def verify_at_n(target_n: int) -> Dict:
    """
    Run proper existential verification at n = target_n.
    For each merge-prone case, check if ANY safe BFS-optimal path exists.
    """
    print(f"\n{'='*70}")
    print(f"Existential Verification: n = {target_n}")
    print(f"{'='*70}")

    t_start = time.time()
    db = generate_triangulations(target_n)
    triangulations = db[target_n]
    print(f"Generated {len(triangulations)} triangulations in {time.time()-t_start:.1f}s")

    results = {
        'n': target_n,
        'num_graphs': len(triangulations),
        'total_merge_prone_colourings': 0,
        'safe_path_exists': 0,
        'no_safe_path': 0,
        'true_counterexamples': [],
        'first_path_unsafe_but_alternative_exists': 0,
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

            for col in v5_cols:
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

                results['total_merge_prone_colourings'] += 1

                path_H = bfs_reduce_to_4(H, col_H, k=5)
                if path_H is None or len(path_H) <= 1:
                    results['safe_path_exists'] += 1
                    continue

                first_path_safe = check_path_safety(T, H, v, col, path_H)
                if first_path_safe:
                    results['safe_path_exists'] += 1
                    continue

                verification = find_safe_bfs_path(T, H, v, col)

                if verification['safe_path_exists']:
                    results['safe_path_exists'] += 1
                    results['first_path_unsafe_but_alternative_exists'] += 1
                else:
                    results['no_safe_path'] += 1
                    ce_info = {
                        'graph': name,
                        'vertex': v,
                        'degree': deg,
                        'paths_checked': verification['paths_checked'],
                        'reason': verification.get('reason', '?'),
                    }
                    results['true_counterexamples'].append(ce_info)
                    print(f"\n*** TRUE COUNTEREXAMPLE: {ce_info} ***")

        if (idx + 1) % max(1, len(triangulations) // 10) == 0 or idx == 0:
            elapsed = time.time() - t_start
            print(f"  [{idx+1}/{len(triangulations)}] {name}: "
                  f"mp={results['total_merge_prone_colourings']}, "
                  f"safe={results['safe_path_exists']}, "
                  f"mixed={results['first_path_unsafe_but_alternative_exists']}, "
                  f"fail={results['no_safe_path']} "
                  f"({elapsed:.0f}s)")

    results['total_time_s'] = round(time.time() - t_start, 1)

    print(f"\n{'='*70}")
    print(f"RESULTS for n={target_n}")
    print(f"{'='*70}")
    print(f"  Merge-prone colourings: {results['total_merge_prone_colourings']}")
    print(f"  Safe path exists (first path safe): "
          f"{results['safe_path_exists'] - results['first_path_unsafe_but_alternative_exists']}")
    print(f"  Safe path exists (alternative found): "
          f"{results['first_path_unsafe_but_alternative_exists']}")
    print(f"  NO safe path (true counterexample): {results['no_safe_path']}")
    print(f"  Time: {results['total_time_s']}s")

    if results['true_counterexamples']:
        print(f"\n*** KILL CRITERION: {len(results['true_counterexamples'])} "
              f"TRUE COUNTEREXAMPLE(S) ***")
    else:
        print(f"\n  Conjecture HOLDS existentially at n={target_n}")
        if results['first_path_unsafe_but_alternative_exists'] > 0:
            print(f"  NOTE: {results['first_path_unsafe_but_alternative_exists']} cases "
                  f"where first BFS path was unsafe but safe alternative exists")
            print(f"  → Conjecture is EXISTENTIAL, not universal")

    return results


if __name__ == '__main__':
    print("=" * 70)
    print("Agent 1520-M1-S3: Existential Verification of Swap Sufficiency")
    print("Checking: does there EXIST a safe BFS-optimal path?")
    print("=" * 70)

    print("\n--- First: verify at n=8 (should be clean) ---")
    r8 = verify_at_n(8)

    print("\n--- Now: verify at n=9 (where initial test found issues) ---")
    r9 = verify_at_n(9)

    print("\n" + "=" * 70)
    print("FINAL EXISTENTIAL VERIFICATION SUMMARY")
    print("=" * 70)
    for n, r in [(8, r8), (9, r9)]:
        ce = len(r['true_counterexamples'])
        mixed = r['first_path_unsafe_but_alternative_exists']
        print(f"  n={n}: {r['total_merge_prone_colourings']} merge-prone, "
              f"mixed={mixed}, true_counterexamples={ce}, time={r['total_time_s']}s")

    if r9['true_counterexamples']:
        print("\n*** KILL CRITERION CONFIRMED ***")
    elif r9['first_path_unsafe_but_alternative_exists'] > 0:
        print(f"\n  Conjecture is EXISTENTIAL (not universal): "
              f"{r9['first_path_unsafe_but_alternative_exists']} mixed cases at n=9")
        print("  This refines our understanding but does NOT disprove the conjecture.")
    else:
        print("\n  All clean at n=9.")
