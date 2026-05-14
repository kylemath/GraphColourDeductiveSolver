"""
vertex_selection_check.py — Agent 1545-M1-S3: Vertex-Selection Strategy.

For each planar triangulation at n=9, for each degree-≤5 vertex v:
  1. Enumerate all 5-colourings with c(v)=5
  2. For each, check if a safe BFS-optimal path exists (no merge-prone swaps)
  3. Also check: if forced through merges, is the merge harmless (v can still
     be coloured after the full path)?

Goal: determine if there's ALWAYS at least one vertex where either:
  (a) all BFS paths are safe (merge-free), OR
  (b) all BFS paths are merge-tolerant (harmless merges)
"""

import sys
import os
import time
import json
from typing import Dict, List, Set, Optional
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
from merge_tolerant_check import find_all_bfs_paths_to_4col


def check_vertex_merge_status(
    T: nx.Graph, v: int, max_ce_check: int = 50
) -> Dict:
    """
    For vertex v in triangulation T, categorize all merge-prone colourings:
      - safe: a safe BFS-optimal path exists
      - merge_tolerant: no safe path, but merge is harmless (v has free colour)
      - harmful: no safe path AND merge is harmful (v has no free colour)
    """
    deg = T.degree(v)
    if deg > 5:
        return {'status': 'SKIP_HIGH_DEGREE', 'degree': deg}

    H = T.copy()
    H.remove_node(v)
    nbrs = sorted(T.neighbors(v))

    all_cols = enumerate_colourings(T, 5)
    v5_cols = [c for c in all_cols if c[v] == 5 and num_colours(c) == 5]

    stats = {
        'vertex': v,
        'degree': deg,
        'num_v5_colourings': len(v5_cols),
        'merge_prone_count': 0,
        'safe_count': 0,
        'no_safe_but_tolerant': 0,
        'harmful_count': 0,
        'not_merge_prone': 0,
        'no_path_needed': 0,
    }

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
            stats['not_merge_prone'] += 1
            continue

        stats['merge_prone_count'] += 1

        first_path = bfs_reduce_to_4(H, col_H, k=5)
        if first_path is None or len(first_path) <= 1:
            stats['no_path_needed'] += 1
            continue

        first_safe = check_path_safety(T, H, v, col, first_path)
        if first_safe:
            stats['safe_count'] += 1
            continue

        verif = find_safe_bfs_path(T, H, v, col, max_paths=1000)
        if verif['safe_path_exists']:
            stats['safe_count'] += 1
            continue

        all_paths = find_all_bfs_paths_to_4col(H, col_H, k=5, max_paths=50)
        any_harmless = False
        for path in all_paths:
            final_col = colouring_from_canonical(H, path[-1])
            nbr_colours = set(final_col[u] for u in nbrs)
            free = {1, 2, 3, 4} - nbr_colours
            if free:
                any_harmless = True
                break

        if any_harmless:
            stats['no_safe_but_tolerant'] += 1
        else:
            stats['harmful_count'] += 1

    stats['fully_safe'] = stats['harmful_count'] == 0
    stats['fully_safe_no_merges'] = (stats['merge_prone_count'] == 0 or
                                     (stats['safe_count'] == stats['merge_prone_count']))
    return stats


def vertex_selection_analysis(target_n: int = 9, verbose: bool = True) -> Dict:
    """
    For all triangulations at n=target_n, check each vertex.
    Determine if every triangulation has at least one "good" vertex.
    """
    print("=" * 70)
    print(f"Agent 1545-M1-S3: Vertex Selection Analysis (n={target_n})")
    print("=" * 70)

    t_start = time.time()
    db = generate_triangulations(target_n)
    triangulations = db[target_n]
    t_gen = time.time() - t_start
    print(f"Generated {len(triangulations)} triangulations in {t_gen:.1f}s")

    results = {
        'n': target_n,
        'num_graphs': len(triangulations),
        'graphs_with_safe_vertex': 0,
        'graphs_with_tolerant_vertex': 0,
        'graphs_with_no_good_vertex': 0,
        'per_graph': [],
    }

    for idx, T in enumerate(triangulations):
        name = T.graph.get('name', f'T_{target_n}_{idx}')

        graph_result = {
            'graph': name,
            'idx': idx,
            'vertex_stats': {},
            'has_safe_vertex': False,
            'has_tolerant_vertex': False,
            'safe_vertices': [],
            'tolerant_vertices': [],
            'problematic_vertices': [],
        }

        for v in sorted(T.nodes()):
            if T.degree(v) > 5:
                continue

            vstats = check_vertex_merge_status(T, v)
            graph_result['vertex_stats'][v] = vstats

            if vstats['fully_safe_no_merges']:
                graph_result['safe_vertices'].append(v)
                graph_result['has_safe_vertex'] = True
            elif vstats['fully_safe']:
                graph_result['tolerant_vertices'].append(v)
                graph_result['has_tolerant_vertex'] = True
            elif vstats['harmful_count'] > 0:
                graph_result['problematic_vertices'].append(v)

        if graph_result['has_safe_vertex'] or graph_result['has_tolerant_vertex']:
            if graph_result['has_safe_vertex']:
                results['graphs_with_safe_vertex'] += 1
            else:
                results['graphs_with_tolerant_vertex'] += 1
        else:
            all_v_tolerant = all(
                s.get('fully_safe', False)
                for s in graph_result['vertex_stats'].values()
            )
            if all_v_tolerant:
                results['graphs_with_tolerant_vertex'] += 1
                graph_result['has_tolerant_vertex'] = True
            else:
                results['graphs_with_no_good_vertex'] += 1

        results['per_graph'].append(graph_result)

        if verbose and ((idx + 1) % max(1, len(triangulations) // 10) == 0
                        or idx == 0
                        or graph_result['problematic_vertices']):
            elapsed = time.time() - t_start
            safe_v = graph_result['safe_vertices']
            tol_v = graph_result['tolerant_vertices']
            prob_v = graph_result['problematic_vertices']
            tag = "OK" if safe_v or tol_v else "PROBLEM"
            print(f"  [{idx+1}/{len(triangulations)}] {name}: "
                  f"safe_v={safe_v}, tolerant_v={tol_v}, problem_v={prob_v} "
                  f"[{tag}] ({elapsed:.0f}s)")

    results['total_time_s'] = round(time.time() - t_start, 1)

    print(f"\n{'='*70}")
    print(f"VERTEX SELECTION RESULTS (n={target_n})")
    print(f"{'='*70}")
    print(f"Graphs tested: {results['num_graphs']}")
    print(f"  With merge-free vertex: {results['graphs_with_safe_vertex']}")
    print(f"  With merge-tolerant vertex (no merge-free): "
          f"{results['graphs_with_tolerant_vertex']}")
    print(f"  No good vertex: {results['graphs_with_no_good_vertex']}")
    print(f"Time: {results['total_time_s']}s")

    if results['graphs_with_no_good_vertex'] == 0:
        print(f"\n*** VERTEX SELECTION STRATEGY WORKS at n={target_n} ***")
        if results['graphs_with_safe_vertex'] == results['num_graphs']:
            print("Every graph has a vertex where merge avoidance succeeds.")
        else:
            print("Every graph has a vertex where merge-tolerant lifting works.")
    else:
        print(f"\n*** VERTEX SELECTION FAILS for "
              f"{results['graphs_with_no_good_vertex']} graphs ***")

    return results


if __name__ == '__main__':
    results = vertex_selection_analysis(target_n=9, verbose=True)

    out_dir = os.path.join(
        os.path.dirname(__file__), '..', '..',
        'backgroundMaterial', 'agent1545', 'coordinator',
        'manager_M1', 'sub_S3'
    )
    os.makedirs(out_dir, exist_ok=True)

    summary = {
        'n': results['n'],
        'num_graphs': results['num_graphs'],
        'graphs_with_safe_vertex': results['graphs_with_safe_vertex'],
        'graphs_with_tolerant_vertex': results['graphs_with_tolerant_vertex'],
        'graphs_with_no_good_vertex': results['graphs_with_no_good_vertex'],
        'total_time_s': results['total_time_s'],
        'per_graph_summary': [],
    }

    for gr in results['per_graph']:
        pg = {
            'graph': gr['graph'],
            'safe_vertices': gr['safe_vertices'],
            'tolerant_vertices': gr['tolerant_vertices'],
            'problematic_vertices': gr['problematic_vertices'],
        }
        for v, vs in gr['vertex_stats'].items():
            if vs.get('harmful_count', 0) > 0 or vs.get('no_safe_but_tolerant', 0) > 0:
                pg[f'v{v}_detail'] = {
                    'merge_prone': vs['merge_prone_count'],
                    'safe': vs['safe_count'],
                    'tolerant': vs['no_safe_but_tolerant'],
                    'harmful': vs['harmful_count'],
                }
        summary['per_graph_summary'].append(pg)

    out_path = os.path.join(out_dir, 'vertex_selection_results.json')
    with open(out_path, 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\nResults saved to {out_path}")
