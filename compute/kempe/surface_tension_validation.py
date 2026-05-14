"""
surface_tension_validation.py — Agent 1520-M2-S1

Compute surface tension rigidity ρ_{ab}(c) for ALL merge-prone colourings
across all planar triangulations at n ≤ 12. Tests multiple variants of
the Surface Tension Rigidity Conjecture.

Variant A (Global): ρ over ALL (a,b)-chains in G-v
Variant B (Local):  ρ over only the (a,b)-chains INCIDENT TO v
Variant C (BFS-aware): ρ conditioned on whether the BFS first-step is unsafe

Definitions:
  σ(K) = |{(u,w) ∈ E : u ∈ K, w ∉ K}|  (boundary edges of chain K)
  σ̄(K) = σ(K)/|K|  (normalized surface tension)
  ρ_{ab}(c) = Var(σ̄(K_1), ..., σ̄(K_m))
"""

import sys
import os
import time
import json
from typing import Dict, List, Set, Tuple, Optional, FrozenSet
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import networkx as nx

from kempe_ops import (
    Colouring, CanonicalColouring,
    get_kempe_chain, get_all_kempe_chains, kempe_swap,
    enumerate_colourings, num_colours,
    canonical_form, colouring_from_canonical,
)
from triangulation_db import generate_triangulations
from physical_analogies import _nx_to_adj


def compute_chain_boundary_edges(adj: Dict[int, List[int]],
                                  chain: FrozenSet[int]) -> int:
    """σ(K) = number of edges from chain K to vertices outside K."""
    count = 0
    for u in chain:
        for w in adj[u]:
            if w not in chain:
                count += 1
    return count


def compute_normalized_surface_tension(adj: Dict[int, List[int]],
                                        chain: FrozenSet[int]) -> float:
    """σ̄(K) = σ(K) / |K|."""
    if len(chain) == 0:
        return 0.0
    return compute_chain_boundary_edges(adj, chain) / len(chain)


def compute_rigidity_variants(T: nx.Graph, H: nx.Graph, v: int,
                                col_H: Colouring, color_a: int,
                                adj_H: Dict[int, List[int]]) -> Dict:
    """
    Compute multiple variants of surface tension rigidity for colour pair (a, 5).

    Returns dict with:
      - global_rigidity: Var over ALL (a,5)-chains
      - local_rigidity: Var over chains incident to v
      - incident_tensions: σ̄ values for v-incident chains
      - all_tensions: σ̄ values for all chains
      - incident_chains: list of chain info dicts
    """
    all_chains = get_all_kempe_chains(H, col_H, color_a, 5)

    all_tensions = []
    chain_infos = []
    for K in all_chains:
        sigma_bar = compute_normalized_surface_tension(adj_H, K)
        all_tensions.append(sigma_bar)
        is_incident = any(u in K for u in T.neighbors(v) if u in H.nodes())
        chain_infos.append({
            'size': len(K),
            'sigma': compute_chain_boundary_edges(adj_H, K),
            'sigma_bar': sigma_bar,
            'incident_to_v': is_incident,
        })

    incident_tensions = [ci['sigma_bar'] for ci in chain_infos if ci['incident_to_v']]
    non_incident_tensions = [ci['sigma_bar'] for ci in chain_infos if not ci['incident_to_v']]

    global_rigidity = float(np.var(all_tensions)) if len(all_tensions) > 1 else 0.0
    local_rigidity = float(np.var(incident_tensions)) if len(incident_tensions) > 1 else 0.0

    return {
        'global_rigidity': global_rigidity,
        'local_rigidity': local_rigidity,
        'all_tensions': all_tensions,
        'incident_tensions': incident_tensions,
        'non_incident_tensions': non_incident_tensions,
        'num_total_chains': len(all_chains),
        'num_incident_chains': len(incident_tensions),
        'chain_infos': chain_infos,
    }


def full_validation(max_n: int = 8, verbose: bool = True) -> Dict:
    """
    Full surface tension rigidity validation for n ≤ max_n.

    For each 5-colouring with a degree-4/5 vertex coloured 5, examine
    every colour a ∈ {1,2,3,4} with at least 2 v-incident neighbors in
    B_{a,5}(G-v). Compute both global and local rigidity. Classify as
    merge-prone or safe based on chain structure.
    """
    db = generate_triangulations(max_n)

    stats = {
        'max_n': max_n,
        'global': {'rigid_mp': 0, 'rigid_safe': 0, 'flex_mp': 0, 'flex_safe': 0},
        'local': {'rigid_mp': 0, 'rigid_safe': 0, 'flex_mp': 0, 'flex_safe': 0},
        'by_n': {},
        'counterexamples_global': [],
        'counterexamples_local': [],
        'tension_data': [],
    }

    for n in range(4, max_n + 1):
        t0 = time.time()
        n_stats = {
            'num_graphs': len(db[n]),
            'total_cases': 0,
            'merge_prone': 0,
            'safe': 0,
            'global': {'rigid_mp': 0, 'rigid_safe': 0, 'flex_mp': 0, 'flex_safe': 0},
            'local': {'rigid_mp': 0, 'rigid_safe': 0, 'flex_mp': 0, 'flex_safe': 0},
        }

        for idx, T in enumerate(db[n]):
            name = T.graph.get('name', f'T_{n}_{idx}')

            all_cols = enumerate_colourings(T, 5)
            five_cols = [c for c in all_cols if num_colours(c) == 5]

            for col in five_cols:
                for v in T.nodes():
                    if col[v] != 5:
                        continue
                    deg = T.degree(v)
                    if deg not in (4, 5):
                        continue

                    H = T.copy()
                    H.remove_node(v)
                    col_H = {u: col[u] for u in H.nodes()}
                    adj_H = _nx_to_adj(H)

                    for a in range(1, 5):
                        nbrs_in_a5 = [u for u in T.neighbors(v)
                                       if u in H.nodes() and col_H[u] in (a, 5)]
                        if len(nbrs_in_a5) < 2:
                            continue

                        chains_at_v = set()
                        for u in nbrs_in_a5:
                            chains_at_v.add(get_kempe_chain(H, col_H, u, a, 5))

                        is_merge_prone = len(chains_at_v) >= 2

                        rv = compute_rigidity_variants(T, H, v, col_H, a, adj_H)
                        g_rigid = rv['global_rigidity'] < 1e-12
                        l_rigid = rv['local_rigidity'] < 1e-12

                        n_stats['total_cases'] += 1
                        if is_merge_prone:
                            n_stats['merge_prone'] += 1
                        else:
                            n_stats['safe'] += 1

                        # Global classification
                        if g_rigid and is_merge_prone:
                            n_stats['global']['rigid_mp'] += 1
                            stats['global']['rigid_mp'] += 1
                        elif g_rigid and not is_merge_prone:
                            n_stats['global']['rigid_safe'] += 1
                            stats['global']['rigid_safe'] += 1
                        elif not g_rigid and is_merge_prone:
                            n_stats['global']['flex_mp'] += 1
                            stats['global']['flex_mp'] += 1
                        else:
                            n_stats['global']['flex_safe'] += 1
                            stats['global']['flex_safe'] += 1

                        # Local classification
                        if l_rigid and is_merge_prone:
                            n_stats['local']['rigid_mp'] += 1
                            stats['local']['rigid_mp'] += 1
                        elif l_rigid and not is_merge_prone:
                            n_stats['local']['rigid_safe'] += 1
                            stats['local']['rigid_safe'] += 1
                            if len(stats['counterexamples_local']) < 20:
                                stats['counterexamples_local'].append({
                                    'type': 'local_rigid_but_safe',
                                    'graph': name, 'vertex': v, 'degree': deg,
                                    'color_a': a,
                                    'local_rigidity': rv['local_rigidity'],
                                    'incident_tensions': rv['incident_tensions'],
                                    'all_tensions': rv['all_tensions'],
                                    'num_incident': rv['num_incident_chains'],
                                    'canonical': list(canonical_form(T, col)),
                                })
                        elif not l_rigid and is_merge_prone:
                            n_stats['local']['flex_mp'] += 1
                            stats['local']['flex_mp'] += 1
                            if len(stats['counterexamples_local']) < 20:
                                stats['counterexamples_local'].append({
                                    'type': 'local_flex_but_merge_prone',
                                    'graph': name, 'vertex': v, 'degree': deg,
                                    'color_a': a,
                                    'local_rigidity': rv['local_rigidity'],
                                    'incident_tensions': rv['incident_tensions'],
                                    'all_tensions': rv['all_tensions'],
                                    'num_incident': rv['num_incident_chains'],
                                    'canonical': list(canonical_form(T, col)),
                                })
                        else:
                            n_stats['local']['flex_safe'] += 1
                            stats['local']['flex_safe'] += 1

                        if n <= 8 and len(stats['tension_data']) < 5000:
                            stats['tension_data'].append({
                                'n': n, 'graph': name, 'v': v, 'deg': deg,
                                'color_a': a,
                                'merge_prone': is_merge_prone,
                                'global_rigidity': rv['global_rigidity'],
                                'local_rigidity': rv['local_rigidity'],
                                'num_incident': rv['num_incident_chains'],
                                'num_total': rv['num_total_chains'],
                                'incident_tensions': rv['incident_tensions'],
                            })

        elapsed = time.time() - t0
        stats['by_n'][n] = n_stats

        if verbose:
            print(f"n={n} ({n_stats['num_graphs']} graphs, {elapsed:.1f}s): "
                  f"{n_stats['total_cases']} cases = "
                  f"{n_stats['merge_prone']} mp + {n_stats['safe']} safe")
            g = n_stats['global']
            l = n_stats['local']
            print(f"  Global: R∧MP={g['rigid_mp']}, R∧S={g['rigid_safe']}, "
                  f"F∧MP={g['flex_mp']}, F∧S={g['flex_safe']}")
            print(f"  Local:  R∧MP={l['rigid_mp']}, R∧S={l['rigid_safe']}, "
                  f"F∧MP={l['flex_mp']}, F∧S={l['flex_safe']}")

    return stats


def print_assessment(stats: Dict, label: str = "Global") -> None:
    """Print conjecture assessment for one variant."""
    key = label.lower()
    d = stats[key]
    r_mp = d['rigid_mp']
    r_s = d['rigid_safe']
    f_mp = d['flex_mp']
    f_s = d['flex_safe']
    total = r_mp + r_s + f_mp + f_s

    print(f"\n  === {label} Rigidity (ρ over {'ALL chains' if key == 'global' else 'v-incident chains'}) ===")
    print(f"  Confusion Matrix (n ≤ {stats['max_n']}):")
    print(f"                     Merge-prone    Safe       Total")
    print(f"    Rigid (ρ=0)      {r_mp:>8}       {r_s:>8}   {r_mp+r_s:>8}")
    print(f"    Flexible (ρ>0)   {f_mp:>8}       {f_s:>8}   {f_mp+f_s:>8}")
    print(f"    Total            {r_mp+f_mp:>8}       {r_s+f_s:>8}   {total:>8}")

    total_rigid = r_mp + r_s
    total_mp = r_mp + f_mp
    if total_rigid > 0:
        precision = r_mp / total_rigid
        print(f"\n  ρ=0 ⟹ merge-prone:  {r_mp}/{total_rigid} = {precision:.4f}", end="")
        if r_s == 0:
            print("  ✓ PERFECT")
        else:
            print(f"  ✗ ({r_s} exceptions)")

    if total_mp > 0:
        recall = r_mp / total_mp
        print(f"  merge-prone ⟹ ρ=0:  {r_mp}/{total_mp} = {recall:.4f}", end="")
        if f_mp == 0:
            print("  ✓ PERFECT")
        else:
            print(f"  ✗ ({f_mp} exceptions)")

    total_flex = f_mp + f_s
    total_safe = r_s + f_s
    if total_flex > 0:
        print(f"  ρ>0 ⟹ merge-prone:  {f_mp}/{total_flex} = {f_mp/total_flex:.4f}", end="")
        if f_s == 0:
            print("  ✓ PERFECT")
        else:
            print(f"  ✗ ({f_s} exceptions)")

    if total_safe > 0:
        print(f"  safe ⟹ ρ=0:         {r_s}/{total_safe} = {r_s/total_safe:.4f}", end="")
        if f_s == 0:
            print("  ✓ PERFECT")
        else:
            print(f"  ✗ ({f_s} exceptions)")


def run_extended_validation(target_n: int, verbose: bool = True) -> Dict:
    """Validate at a single n value."""
    t0 = time.time()
    db = generate_triangulations(target_n)
    gen_time = time.time() - t0

    if verbose:
        print(f"\nGenerated {len(db[target_n])} triangulations at n={target_n} "
              f"in {gen_time:.1f}s")

    triangulations = db[target_n]
    stats = {
        'max_n': target_n,
        'global': {'rigid_mp': 0, 'rigid_safe': 0, 'flex_mp': 0, 'flex_safe': 0},
        'local': {'rigid_mp': 0, 'rigid_safe': 0, 'flex_mp': 0, 'flex_safe': 0},
        'counterexamples_local': [],
    }

    for idx, T in enumerate(triangulations):
        name = T.graph.get('name', f'T_{target_n}_{idx}')
        graph_t0 = time.time()

        all_cols = enumerate_colourings(T, 5)
        five_cols = [c for c in all_cols if num_colours(c) == 5]

        for col in five_cols:
            for v in T.nodes():
                if col[v] != 5:
                    continue
                deg = T.degree(v)
                if deg not in (4, 5):
                    continue

                H = T.copy()
                H.remove_node(v)
                col_H = {u: col[u] for u in H.nodes()}
                adj_H = _nx_to_adj(H)

                for a in range(1, 5):
                    nbrs_in_a5 = [u for u in T.neighbors(v)
                                   if u in H.nodes() and col_H[u] in (a, 5)]
                    if len(nbrs_in_a5) < 2:
                        continue

                    chains_at_v = set()
                    for u in nbrs_in_a5:
                        chains_at_v.add(get_kempe_chain(H, col_H, u, a, 5))

                    is_mp = len(chains_at_v) >= 2

                    rv = compute_rigidity_variants(T, H, v, col_H, a, adj_H)
                    g_rigid = rv['global_rigidity'] < 1e-12
                    l_rigid = rv['local_rigidity'] < 1e-12

                    gk = 'rigid_mp' if g_rigid and is_mp else \
                         'rigid_safe' if g_rigid else \
                         'flex_mp' if is_mp else 'flex_safe'
                    stats['global'][gk] += 1

                    lk = 'rigid_mp' if l_rigid and is_mp else \
                         'rigid_safe' if l_rigid else \
                         'flex_mp' if is_mp else 'flex_safe'
                    stats['local'][lk] += 1

                    if lk in ('rigid_safe', 'flex_mp') and len(stats['counterexamples_local']) < 10:
                        stats['counterexamples_local'].append({
                            'type': lk.replace('_', ' '),
                            'graph': name, 'vertex': v, 'degree': deg,
                            'color_a': a,
                            'local_rig': rv['local_rigidity'],
                            'inc_tensions': rv['incident_tensions'],
                        })

        g_elapsed = time.time() - graph_t0
        if verbose and ((idx + 1) % max(1, len(triangulations) // 5) == 0
                         or idx == 0):
            print(f"  [{idx+1}/{len(triangulations)}] {name} ({g_elapsed:.1f}s)")

    return stats


if __name__ == '__main__':
    print("=" * 70)
    print("SURFACE TENSION RIGIDITY VALIDATION — Agent 1520-M2-S1")
    print("Dual Variant: Global (all chains) vs Local (v-incident chains)")
    print("=" * 70)

    print("\n--- Phase 1: Retroactive Validation (n ≤ 8) ---")
    stats_8 = full_validation(max_n=8)

    print("\n" + "=" * 70)
    print("CONJECTURE ASSESSMENT — n ≤ 8")
    print("=" * 70)
    print_assessment(stats_8, "Global")
    print_assessment(stats_8, "Local")

    if stats_8['counterexamples_local']:
        print(f"\n  Local counterexamples (first 10):")
        for ce in stats_8['counterexamples_local'][:10]:
            print(f"    {ce['type']}: {ce['graph']} v={ce['vertex']} a={ce['color_a']} "
                  f"ρ_local={ce.get('local_rigidity', 0):.6f} "
                  f"inc_tensions={ce.get('incident_tensions', [])}")

    print("\n--- Phase 2: Extension to n=9 ---")
    stats_9 = run_extended_validation(9)
    print("\nCONJECTURE ASSESSMENT — n=9")
    print_assessment(stats_9, "Global")
    print_assessment(stats_9, "Local")

    if stats_9['counterexamples_local']:
        print(f"\n  Local counterexamples at n=9:")
        for ce in stats_9['counterexamples_local'][:10]:
            print(f"    {ce['type']}: {ce['graph']} v={ce['vertex']} a={ce['color_a']} "
                  f"ρ_local={ce.get('local_rig', 0):.6f} "
                  f"inc_tensions={ce.get('inc_tensions', [])}")

    results = {
        'phase1': {
            'max_n': 8,
            'global': stats_8['global'],
            'local': stats_8['local'],
            'by_n': {str(k): v for k, v in stats_8['by_n'].items()},
            'local_counterexamples': stats_8['counterexamples_local'][:50],
        },
        'phase2_n9': {
            'global': stats_9['global'],
            'local': stats_9['local'],
            'local_counterexamples': stats_9['counterexamples_local'][:50],
        },
    }

    output_dir = os.path.join(os.path.dirname(__file__),
                               '..', '..', 'backgroundMaterial', 'agent1520',
                               'coordinator', 'manager_M2', 'sub_S1')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'rigidity_validation_results.json')
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {output_path}")

    print("\n" + "=" * 70)
    print("VALIDATION COMPLETE")
    print("=" * 70)
