"""
counterexample_energy_analysis.py — Agent 1443-M2

Compute all physical analogy energy metrics on the real counterexample
graphs T_9_25 and T_9_35, comparing safe vs unsafe Kempe swap paths.

These two graphs are the only n=9 triangulations where ALL optimal BFS
paths from a merge-prone 5-coloring use unsafe (a,5)-swaps:
  T_9_25: v=3 (degree 5)
  T_9_35: v=6 (degree 4)
"""

import sys
import os
import json
import math

sys.path.insert(0, os.path.dirname(__file__))

from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import networkx as nx
import numpy as np

from triangulation_db import generate_triangulations
from kempe_ops import (
    Colouring, CanonicalColouring,
    enumerate_colourings, num_colours, get_kempe_chain,
    get_all_kempe_chains, kempe_swap,
    canonical_form, colouring_from_canonical, all_kempe_neighbours,
)
from counterexample_analysis import dump_graph_structure
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


def compute_all_metrics(G: nx.Graph, coloring: Colouring,
                         v: int) -> Dict:
    """Compute all physical analogy metrics for a coloring of G centered on v."""
    adj = _nx_to_adj(G)
    pot = compute_electrostatic_potential(adj, coloring)

    return {
        'global_magic_gem': compute_global_magic_gem_energy(adj, coloring),
        'local_magic_gem_v': compute_local_magic_gem_energy(adj, coloring, v),
        'potts_energy': compute_potts_energy(adj, coloring),
        'electrostatic_v': pot.get(v, 0.0),
        'electrostatic_neighbors': {u: pot.get(u, 0.0) for u in G.neighbors(v)},
        'local_entropy_v': compute_local_entropy(adj, coloring, v),
        'defect_interaction': compute_defect_interaction(adj, coloring),
        'electric_gradient_v': compute_electric_field_gradient(adj, coloring, v, pot),
        'potentials': pot,
    }


def compute_chain_metrics(G: nx.Graph, coloring: Colouring,
                           chain: Set[int], color_a: int, color_b: int) -> Dict:
    """Compute chain-specific metrics."""
    adj = _nx_to_adj(G)
    return {
        'chain_size': len(chain),
        'ruggedness': compute_ruggedness_metric(chain, adj),
        'surface_tension': compute_surface_tension(adj, coloring, chain, color_a, color_b),
    }


def find_merge_prone_colorings(T: nx.Graph, v: int) -> List[Dict]:
    """Find all merge-prone colorings for vertex v colored 5."""
    H = T.copy()
    H.remove_node(v)

    all_cols = enumerate_colourings(T, 5)
    v5_cols = [c for c in all_cols if c[v] == 5 and num_colours(c) == 5]

    results = []
    for col in v5_cols:
        col_H = {u: col[u] for u in H.nodes()}
        merge_colors = []

        for a_colour in range(1, 5):
            nbrs_in = [u for u in T.neighbors(v)
                       if u in H.nodes() and col_H[u] in (a_colour, 5)]
            if len(nbrs_in) < 2:
                continue
            chain_set = set()
            for u in nbrs_in:
                chain_set.add(get_kempe_chain(H, col_H, u, a_colour, 5))
            if len(chain_set) >= 2:
                merge_colors.append(a_colour)

        if merge_colors:
            results.append({
                'coloring': col,
                'col_H': col_H,
                'merge_colors': merge_colors,
            })

    return results


def analyze_path_energies(T: nx.Graph, H: nx.Graph, v: int,
                           col: Colouring, col_H: Colouring,
                           path: List[CanonicalColouring],
                           path_label: str) -> Dict:
    """Compute energy at each step of a BFS path."""
    adj_H = _nx_to_adj(H)
    step_energies = []

    current_col_H = dict(col_H)
    current_col_G = dict(col)

    for i, canon in enumerate(path):
        step_col_H = colouring_from_canonical(H, canon)
        full_col = dict(step_col_H)
        full_col[v] = 5

        adj_G = _nx_to_adj(T)
        pot = compute_electrostatic_potential(adj_G, full_col)

        step_data = {
            'step': i,
            'global_magic_gem': compute_global_magic_gem_energy(adj_G, full_col),
            'potts_energy': compute_potts_energy(adj_G, full_col),
            'electrostatic_v': pot.get(v, 0.0),
            'local_entropy_v': compute_local_entropy(adj_G, full_col, v),
            'defect_interaction': compute_defect_interaction(adj_G, full_col),
            'num_color5': sum(1 for c in full_col.values() if c == 5),
        }

        if i > 0:
            prev_col_H = colouring_from_canonical(H, path[i - 1])
            a, b = _identify_swap(H, prev_col_H, step_col_H)
            swapped = frozenset(u for u in H.nodes() if prev_col_H[u] != step_col_H[u])
            step_data['swap_colors'] = (a, b)
            step_data['chain_size'] = len(swapped)
            step_data['is_a5_swap'] = (a is not None and b is not None and 5 in (a, b))

            if step_data['is_a5_swap'] and swapped:
                the_a = a if a != 5 else b
                step_data['chain_ruggedness'] = compute_ruggedness_metric(
                    set(swapped), adj_H)
                step_data['chain_surface_tension'] = compute_surface_tension(
                    adj_H, prev_col_H, set(swapped), the_a, 5)

        step_energies.append(step_data)

    return {
        'path_label': path_label,
        'length': len(path) - 1,
        'steps': step_energies,
        'initial_energy': step_energies[0]['global_magic_gem'] if step_energies else 0,
        'final_energy': step_energies[-1]['global_magic_gem'] if step_energies else 0,
    }


def analyze_counterexample(T: nx.Graph, v: int, graph_name: str) -> Dict:
    """Full energy analysis of one counterexample graph."""
    H = T.copy()
    H.remove_node(v)

    structure = dump_graph_structure(T)

    merge_prone = find_merge_prone_colorings(T, v)
    print(f"\n  {graph_name}: {len(merge_prone)} merge-prone colorings for v={v}")

    all_coloring_data = []

    for mp_idx, mp in enumerate(merge_prone):
        col = mp['coloring']
        col_H = mp['col_H']

        base_metrics = compute_all_metrics(T, col, v)

        opt_dist, all_opt_paths = bfs_all_optimal_paths(H, col_H, k=5)
        if not all_opt_paths:
            continue

        safe_paths = []
        unsafe_paths = []
        for p in all_opt_paths:
            cls = classify_path_safety(T, H, v, col, p)
            if cls['path_is_safe']:
                safe_paths.append(p)
            else:
                unsafe_paths.append(p)

        unsafe_chain_data = []
        for mc in mp['merge_colors']:
            nbrs_in = [u for u in T.neighbors(v)
                       if u in H.nodes() and col_H[u] in (mc, 5)]
            for u in nbrs_in:
                chain = get_kempe_chain(H, col_H, u, mc, 5)
                cm = compute_chain_metrics(H, col_H, set(chain), mc, 5)
                cm['color_a'] = mc
                cm['start_vertex'] = u
                unsafe_chain_data.append(cm)

        path_analyses = []
        for i, p in enumerate(unsafe_paths[:3]):
            pa = analyze_path_energies(T, H, v, col, col_H, p, f"unsafe_{i}")
            path_analyses.append(pa)

        for i, p in enumerate(safe_paths[:3]):
            pa = analyze_path_energies(T, H, v, col, col_H, p, f"safe_{i}")
            path_analyses.append(pa)

        coloring_data = {
            'coloring_index': mp_idx,
            'canonical': canonical_form(T, col),
            'merge_colors': mp['merge_colors'],
            'opt_dist': opt_dist,
            'num_optimal_paths': len(all_opt_paths),
            'num_safe_paths': len(safe_paths),
            'num_unsafe_paths': len(unsafe_paths),
            'base_metrics': base_metrics,
            'unsafe_chain_data': unsafe_chain_data,
            'path_analyses': path_analyses,
        }
        all_coloring_data.append(coloring_data)

        if mp_idx < 3:
            print(f"    Coloring {mp_idx}: opt_dist={opt_dist}, "
                  f"paths={len(all_opt_paths)} "
                  f"(safe={len(safe_paths)}, unsafe={len(unsafe_paths)})")
            print(f"      Magic Gem: {base_metrics['global_magic_gem']:.4f}, "
                  f"Potts: {base_metrics['potts_energy']:.1f}, "
                  f"Entropy@v: {base_metrics['local_entropy_v']:.4f}")
            if unsafe_chain_data:
                for cd in unsafe_chain_data[:2]:
                    print(f"      Chain(a={cd['color_a']}): size={cd['chain_size']}, "
                          f"rugg={cd['ruggedness']:.3f}, "
                          f"tension={cd['surface_tension']:.1f}")

    return {
        'graph_name': graph_name,
        'vertex': v,
        'degree': T.degree(v),
        'structure': structure,
        'num_merge_prone': len(merge_prone),
        'coloring_analyses': all_coloring_data,
    }


def compute_aggregate_stats(analysis: Dict) -> Dict:
    """Aggregate statistics across all colorings for a counterexample."""
    safe_energies = defaultdict(list)
    unsafe_energies = defaultdict(list)
    chain_ruggedness_safe = []
    chain_ruggedness_unsafe = []
    chain_tension_safe = []
    chain_tension_unsafe = []

    for cd in analysis['coloring_analyses']:
        for pa in cd['path_analyses']:
            bucket = safe_energies if 'safe' in pa['path_label'] else unsafe_energies
            bucket['global_magic_gem'].append(pa['initial_energy'])
            for step in pa['steps']:
                bucket['potts_per_step'].append(step['potts_energy'])
                bucket['entropy_per_step'].append(step['local_entropy_v'])
                if 'chain_ruggedness' in step:
                    if 'safe' in pa['path_label']:
                        chain_ruggedness_safe.append(step['chain_ruggedness'])
                        chain_tension_safe.append(step.get('chain_surface_tension', 0))
                    else:
                        chain_ruggedness_unsafe.append(step['chain_ruggedness'])
                        chain_tension_unsafe.append(step.get('chain_surface_tension', 0))

    def summarize(lst):
        if not lst:
            return {'mean': 0, 'std': 0, 'min': 0, 'max': 0, 'n': 0}
        arr = np.array(lst)
        return {
            'mean': float(np.mean(arr)),
            'std': float(np.std(arr)),
            'min': float(np.min(arr)),
            'max': float(np.max(arr)),
            'n': len(arr),
        }

    return {
        'safe_initial_magic_gem': summarize(safe_energies.get('global_magic_gem', [])),
        'unsafe_initial_magic_gem': summarize(unsafe_energies.get('global_magic_gem', [])),
        'safe_potts': summarize(safe_energies.get('potts_per_step', [])),
        'unsafe_potts': summarize(unsafe_energies.get('potts_per_step', [])),
        'safe_entropy': summarize(safe_energies.get('entropy_per_step', [])),
        'unsafe_entropy': summarize(unsafe_energies.get('entropy_per_step', [])),
        'chain_ruggedness_safe': summarize(chain_ruggedness_safe),
        'chain_ruggedness_unsafe': summarize(chain_ruggedness_unsafe),
        'chain_tension_safe': summarize(chain_tension_safe),
        'chain_tension_unsafe': summarize(chain_tension_unsafe),
    }


if __name__ == '__main__':
    print("=" * 70)
    print("COUNTEREXAMPLE ENERGY ANALYSIS — Agent 1443-M2")
    print("=" * 70)

    db = generate_triangulations(9)

    counterexamples = [(25, 3), (35, 6)]
    all_results = {}

    for graph_idx, target_v in counterexamples:
        T = db[9][graph_idx]
        name = T.graph.get('name', f'T_9_{graph_idx}')

        print(f"\n{'='*70}")
        print(f"Analyzing {name}, v={target_v} (degree {T.degree(target_v)})")
        print(f"{'='*70}")

        analysis = analyze_counterexample(T, target_v, name)
        stats = compute_aggregate_stats(analysis)
        analysis['aggregate_stats'] = stats

        all_results[name] = analysis

        print(f"\n  --- Aggregate Stats ---")
        for key, val in stats.items():
            if val['n'] > 0:
                print(f"  {key}: mean={val['mean']:.4f} ±{val['std']:.4f} "
                      f"[{val['min']:.4f}, {val['max']:.4f}] (n={val['n']})")

    output_path = os.path.join(os.path.dirname(__file__),
                                '..', '..', 'backgroundMaterial', 'agent1443',
                                'deliverables', 'energy_analysis_results.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    serializable = {}
    for name, analysis in all_results.items():
        s = {
            'graph_name': analysis['graph_name'],
            'vertex': analysis['vertex'],
            'degree': analysis['degree'],
            'num_merge_prone': analysis['num_merge_prone'],
            'aggregate_stats': analysis['aggregate_stats'],
            'sample_colorings': [],
        }
        for cd in analysis['coloring_analyses'][:5]:
            sample = {
                'coloring_index': cd['coloring_index'],
                'merge_colors': cd['merge_colors'],
                'opt_dist': cd['opt_dist'],
                'num_safe_paths': cd['num_safe_paths'],
                'num_unsafe_paths': cd['num_unsafe_paths'],
                'base_metrics': {
                    'global_magic_gem': cd['base_metrics']['global_magic_gem'],
                    'local_magic_gem_v': cd['base_metrics']['local_magic_gem_v'],
                    'potts_energy': cd['base_metrics']['potts_energy'],
                    'electrostatic_v': cd['base_metrics']['electrostatic_v'],
                    'local_entropy_v': cd['base_metrics']['local_entropy_v'],
                    'defect_interaction': cd['base_metrics']['defect_interaction'],
                    'electric_gradient_v': cd['base_metrics']['electric_gradient_v'],
                },
                'unsafe_chain_data': cd['unsafe_chain_data'],
                'path_energy_profiles': [],
            }
            for pa in cd['path_analyses']:
                profile = {
                    'label': pa['path_label'],
                    'length': pa['length'],
                    'magic_gem_profile': [s['global_magic_gem'] for s in pa['steps']],
                    'potts_profile': [s['potts_energy'] for s in pa['steps']],
                    'entropy_profile': [s['local_entropy_v'] for s in pa['steps']],
                    'color5_profile': [s['num_color5'] for s in pa['steps']],
                }
                sample['path_energy_profiles'].append(profile)
            s['sample_colorings'].append(sample)
        serializable[name] = s

    with open(output_path, 'w') as f:
        json.dump(serializable, f, indent=2)

    print(f"\n\nResults saved to {output_path}")
    print("=" * 70)
    print("ENERGY ANALYSIS COMPLETE")
    print("=" * 70)
