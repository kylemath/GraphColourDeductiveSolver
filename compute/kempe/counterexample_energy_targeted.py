"""
counterexample_energy_targeted.py — Agent 1443-M2-S1

Targeted analysis: find ONLY the colorings where ALL optimal BFS paths
are unsafe, then compute full energy profiles on those specific cases.
Also compute energy on the nearest safe (non-optimal) paths for comparison.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))

from typing import Dict, List, Set, Tuple
from collections import defaultdict, deque
import numpy as np

from triangulation_db import generate_triangulations
from kempe_ops import (
    Colouring, CanonicalColouring,
    enumerate_colourings, num_colours, get_kempe_chain,
    kempe_swap, canonical_form, colouring_from_canonical,
    all_kempe_neighbours,
)
from reduction_search import bfs_reduce_to_4, _identify_swap
from all_paths_analysis import bfs_all_optimal_paths, classify_path_safety
from physical_analogies import (
    compute_global_magic_gem_energy,
    compute_local_magic_gem_energy,
    compute_electrostatic_potential,
    compute_potts_energy,
    compute_ruggedness_metric,
    compute_surface_tension,
    compute_local_entropy,
    compute_defect_interaction,
    compute_electric_field_gradient,
    _nx_to_adj,
)


def full_metrics_at_step(T, v, col_H_step, adj_T):
    """Compute all metrics for a partial coloring on H, extending to T with v=5."""
    full_col = dict(col_H_step)
    full_col[v] = 5
    pot = compute_electrostatic_potential(adj_T, full_col)
    return {
        'global_magic_gem': compute_global_magic_gem_energy(adj_T, full_col),
        'local_magic_gem_v': compute_local_magic_gem_energy(adj_T, full_col, v),
        'potts_energy': compute_potts_energy(adj_T, full_col),
        'electrostatic_v': pot.get(v, 0.0),
        'local_entropy_v': compute_local_entropy(adj_T, full_col, v),
        'defect_interaction': compute_defect_interaction(adj_T, full_col),
        'electric_gradient_v': compute_electric_field_gradient(adj_T, full_col, v, pot),
        'num_color5': sum(1 for c in full_col.values() if c == 5),
    }


def find_safe_nonoptimal_path(T, H, v, col, col_H, opt_dist, max_extra=3):
    """
    BFS in R(H,5) for a safe path at distance opt_dist+1 .. opt_dist+max_extra.
    Returns the first safe path found, or None.
    """
    start_c = canonical_form(H, col_H)
    visited = {start_c: 0}
    parent = {start_c: None}
    queue = deque([start_c])
    max_dist = opt_dist + max_extra

    while queue:
        current = queue.popleft()
        d = visited[current]
        if d >= max_dist:
            continue

        current_col = colouring_from_canonical(H, current)
        for nbr in all_kempe_neighbours(H, current_col, 5):
            if nbr in visited:
                continue
            visited[nbr] = d + 1
            parent[nbr] = current

            nbr_col = colouring_from_canonical(H, nbr)
            if num_colours(nbr_col) <= 4 and d + 1 > opt_dist:
                path = [nbr]
                node = current
                while node is not None:
                    path.append(node)
                    node = parent[node]
                path_list = list(reversed(path))

                cls = classify_path_safety(T, H, v, col, path_list)
                if cls['path_is_safe']:
                    return path_list

            queue.append(nbr)

    return None


def analyze_path_full(T, H, v, path, label):
    """Full energy profile along a BFS path."""
    adj_T = _nx_to_adj(T)
    adj_H = _nx_to_adj(H)
    steps = []

    for i, canon in enumerate(path):
        col_H_step = colouring_from_canonical(H, canon)
        m = full_metrics_at_step(T, v, col_H_step, adj_T)
        m['step'] = i

        if i > 0:
            prev_col = colouring_from_canonical(H, path[i - 1])
            a, b = _identify_swap(H, prev_col, col_H_step)
            swapped = frozenset(u for u in H.nodes() if prev_col[u] != col_H_step[u])
            m['swap_colors'] = [a, b]
            m['chain_size'] = len(swapped)
            m['is_a5_swap'] = (a is not None and b is not None and 5 in (a, b))
            if m['is_a5_swap'] and swapped:
                the_a = a if a != 5 else b
                m['chain_ruggedness'] = compute_ruggedness_metric(set(swapped), adj_H)
                m['chain_surface_tension'] = compute_surface_tension(
                    adj_H, prev_col, set(swapped), the_a, 5)

        steps.append(m)

    return {'label': label, 'length': len(path) - 1, 'steps': steps}


if __name__ == '__main__':
    print("=" * 70)
    print("TARGETED COUNTEREXAMPLE ENERGY ANALYSIS — Agent 1443-M2")
    print("=" * 70)

    db = generate_triangulations(9)
    counterexamples = [(25, 3), (35, 6)]
    all_results = {}

    for graph_idx, target_v in counterexamples:
        T = db[9][graph_idx]
        name = T.graph.get('name', f'T_9_{graph_idx}')
        H = T.copy()
        H.remove_node(target_v)
        adj_T = _nx_to_adj(T)

        print(f"\n{'='*70}")
        print(f"Analyzing {name}, v={target_v} (degree {T.degree(target_v)})")
        print(f"{'='*70}")

        all_cols = enumerate_colourings(T, 5)
        v5_cols = [c for c in all_cols if c[target_v] == 5 and num_colours(c) == 5]
        print(f"  Total 5-colorings with v={target_v} colored 5: {len(v5_cols)}")

        true_counterexamples = []

        for col in v5_cols:
            col_H = {u: col[u] for u in H.nodes()}

            is_merge_prone = False
            merge_colors = []
            for a_c in range(1, 5):
                nbrs = [u for u in T.neighbors(target_v)
                        if u in H.nodes() and col_H[u] in (a_c, 5)]
                if len(nbrs) < 2:
                    continue
                chains = set()
                for u in nbrs:
                    chains.add(get_kempe_chain(H, col_H, u, a_c, 5))
                if len(chains) >= 2:
                    is_merge_prone = True
                    merge_colors.append(a_c)

            if not is_merge_prone:
                continue

            opt_dist, all_opt = bfs_all_optimal_paths(H, col_H, k=5)
            if not all_opt or opt_dist <= 0:
                continue

            has_safe = any(
                classify_path_safety(T, H, target_v, col, p)['path_is_safe']
                for p in all_opt
            )

            if not has_safe:
                true_counterexamples.append({
                    'col': col,
                    'col_H': col_H,
                    'merge_colors': merge_colors,
                    'opt_dist': opt_dist,
                    'all_opt': all_opt,
                })

        print(f"  TRUE counterexample colorings (all opt paths unsafe): "
              f"{len(true_counterexamples)}")

        graph_data = {
            'graph_name': name,
            'vertex': target_v,
            'degree': T.degree(target_v),
            'total_v5_colorings': len(v5_cols),
            'num_true_counterexamples': len(true_counterexamples),
            'counterexample_analyses': [],
        }

        safe_path_metrics_all = defaultdict(list)
        unsafe_path_metrics_all = defaultdict(list)

        for ce_idx, ce in enumerate(true_counterexamples):
            col = ce['col']
            col_H = ce['col_H']
            opt_dist = ce['opt_dist']

            base = full_metrics_at_step(T, target_v, col_H, adj_T)

            unsafe_path = ce['all_opt'][0]
            unsafe_profile = analyze_path_full(T, H, target_v, unsafe_path, 'unsafe')

            safe_path = find_safe_nonoptimal_path(
                T, H, target_v, col, col_H, opt_dist, max_extra=3)
            safe_profile = None
            if safe_path:
                safe_profile = analyze_path_full(T, H, target_v, safe_path, 'safe')

            chain_data = []
            for mc in ce['merge_colors']:
                nbrs = [u for u in T.neighbors(target_v)
                        if u in H.nodes() and col_H[u] in (mc, 5)]
                for u in nbrs:
                    chain = get_kempe_chain(H, col_H, u, mc, 5)
                    adj_H = _nx_to_adj(H)
                    chain_data.append({
                        'color_a': mc,
                        'chain_size': len(chain),
                        'ruggedness': compute_ruggedness_metric(set(chain), adj_H),
                        'surface_tension': compute_surface_tension(
                            adj_H, col_H, set(chain), mc, 5),
                    })

            for step in unsafe_profile['steps']:
                for k in ['global_magic_gem', 'potts_energy', 'local_entropy_v',
                           'electrostatic_v', 'defect_interaction', 'electric_gradient_v']:
                    unsafe_path_metrics_all[k].append(step[k])
                if 'chain_ruggedness' in step:
                    unsafe_path_metrics_all['chain_ruggedness'].append(step['chain_ruggedness'])
                    unsafe_path_metrics_all['chain_tension'].append(step.get('chain_surface_tension', 0))

            if safe_profile:
                for step in safe_profile['steps']:
                    for k in ['global_magic_gem', 'potts_energy', 'local_entropy_v',
                               'electrostatic_v', 'defect_interaction', 'electric_gradient_v']:
                        safe_path_metrics_all[k].append(step[k])
                    if 'chain_ruggedness' in step:
                        safe_path_metrics_all['chain_ruggedness'].append(step['chain_ruggedness'])
                        safe_path_metrics_all['chain_tension'].append(step.get('chain_surface_tension', 0))

            ce_data = {
                'index': ce_idx,
                'canonical': list(canonical_form(T, col)),
                'merge_colors': ce['merge_colors'],
                'opt_dist': opt_dist,
                'num_unsafe_paths': len(ce['all_opt']),
                'safe_path_found': safe_path is not None,
                'safe_path_dist': len(safe_path) - 1 if safe_path else None,
                'base_metrics': base,
                'chain_data': chain_data,
                'unsafe_profile': {
                    'magic_gem': [s['global_magic_gem'] for s in unsafe_profile['steps']],
                    'potts': [s['potts_energy'] for s in unsafe_profile['steps']],
                    'entropy': [s['local_entropy_v'] for s in unsafe_profile['steps']],
                    'color5_count': [s['num_color5'] for s in unsafe_profile['steps']],
                    'electrostatic_v': [s['electrostatic_v'] for s in unsafe_profile['steps']],
                },
            }
            if safe_profile:
                ce_data['safe_profile'] = {
                    'magic_gem': [s['global_magic_gem'] for s in safe_profile['steps']],
                    'potts': [s['potts_energy'] for s in safe_profile['steps']],
                    'entropy': [s['local_entropy_v'] for s in safe_profile['steps']],
                    'color5_count': [s['num_color5'] for s in safe_profile['steps']],
                    'electrostatic_v': [s['electrostatic_v'] for s in safe_profile['steps']],
                    'length': safe_profile['length'],
                }

            graph_data['counterexample_analyses'].append(ce_data)

            if ce_idx < 5:
                print(f"\n  CE {ce_idx}: opt_dist={opt_dist}, "
                      f"{len(ce['all_opt'])} paths all unsafe, "
                      f"merge_colors={ce['merge_colors']}")
                print(f"    Base: MG={base['global_magic_gem']:.4f}, "
                      f"Potts={base['potts_energy']:.1f}, "
                      f"Entropy={base['local_entropy_v']:.4f}, "
                      f"E-stat={base['electrostatic_v']:.4f}")
                print(f"    Unsafe path energy profile (MG): "
                      f"{[f'{x:.3f}' for x in ce_data['unsafe_profile']['magic_gem']]}")
                if safe_profile:
                    print(f"    Safe path (dist={safe_profile['length']}) "
                          f"energy profile (MG): "
                          f"{[f'{x:.3f}' for x in ce_data['safe_profile']['magic_gem']]}")
                else:
                    print(f"    No safe path found within opt+3")
                for cd in chain_data[:3]:
                    print(f"    Chain(a={cd['color_a']}): size={cd['chain_size']}, "
                          f"rugg={cd['ruggedness']:.3f}, tension={cd['surface_tension']:.1f}")

        def stat(lst):
            if not lst:
                return {'mean': 0, 'std': 0, 'n': 0}
            a = np.array(lst)
            return {'mean': float(np.mean(a)), 'std': float(np.std(a)),
                    'min': float(np.min(a)), 'max': float(np.max(a)), 'n': len(a)}

        graph_data['aggregates'] = {
            'unsafe': {k: stat(v) for k, v in unsafe_path_metrics_all.items()},
            'safe': {k: stat(v) for k, v in safe_path_metrics_all.items()},
        }

        print(f"\n  --- Aggregate Comparison (unsafe vs safe paths) ---")
        for metric in ['global_magic_gem', 'potts_energy', 'local_entropy_v',
                        'electrostatic_v', 'chain_ruggedness', 'chain_tension']:
            u = graph_data['aggregates']['unsafe'].get(metric, {'mean': 0, 'n': 0})
            s = graph_data['aggregates']['safe'].get(metric, {'mean': 0, 'n': 0})
            if u['n'] > 0 or s['n'] > 0:
                print(f"  {metric:25s}: unsafe={u.get('mean',0):.4f}±{u.get('std',0):.4f} "
                      f"(n={u['n']}), safe={s.get('mean',0):.4f}±{s.get('std',0):.4f} (n={s['n']})")

        all_results[name] = graph_data

    output_path = os.path.join(os.path.dirname(__file__),
                                '..', '..', 'backgroundMaterial', 'agent1443',
                                'deliverables', 'targeted_energy_results.json')
    with open(output_path, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)

    print(f"\n\nTargeted results saved to {output_path}")
    print("=" * 70)
