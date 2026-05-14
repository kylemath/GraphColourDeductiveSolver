"""
surface_tension_targeted.py — Agent 1520-M2-S1 (Targeted Analysis)

For the n=9 counterexample graphs (T_9_25 and T_9_35), compare surface
tension rigidity between:
  A) The 48 TRUE counterexample colorings (all BFS-optimal paths unsafe)
  B) Other merge-prone colorings (where safe optimal paths exist)

This is the precise test of Agent 1443's finding.
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(__file__))

from typing import Dict, List, Set, Tuple, FrozenSet
from collections import defaultdict
import numpy as np
import networkx as nx

from kempe_ops import (
    Colouring, CanonicalColouring,
    get_kempe_chain, get_all_kempe_chains, kempe_swap,
    enumerate_colourings, num_colours,
    canonical_form, colouring_from_canonical,
)
from triangulation_db import generate_triangulations
from all_paths_analysis import bfs_all_optimal_paths, classify_path_safety
from physical_analogies import _nx_to_adj


def compute_chain_boundary(adj: Dict[int, List[int]], chain: FrozenSet[int]) -> int:
    return sum(1 for u in chain for w in adj[u] if w not in chain)


def compute_normalized_tension(adj: Dict[int, List[int]], chain: FrozenSet[int]) -> float:
    if len(chain) == 0:
        return 0.0
    return compute_chain_boundary(adj, chain) / len(chain)


def analyze_counterexample_graphs():
    """Targeted analysis of T_9_25 and T_9_35."""
    db = generate_triangulations(9)

    targets = [
        (25, 3),  # T_9_25, v=3, degree 5
        (35, 6),  # T_9_35, v=6, degree 4
    ]

    for graph_idx, target_v in targets:
        T = db[9][graph_idx]
        name = T.graph.get('name', f'T_9_{graph_idx}')
        v = target_v
        deg = T.degree(v)

        H = T.copy()
        H.remove_node(v)
        adj_H = _nx_to_adj(H)

        print(f"\n{'='*70}")
        print(f"TARGETED ANALYSIS: {name}, v={v} (degree {deg})")
        print(f"{'='*70}")

        all_cols = enumerate_colourings(T, 5)
        v5_cols = [c for c in all_cols if c[v] == 5 and num_colours(c) == 5]
        print(f"Total 5-colorings with c(v)=5: {len(v5_cols)}")

        categories = {
            'all_unsafe': [],     # TRUE counterexamples
            'has_safe_opt': [],   # merge-prone but safe optimal path exists
            'not_merge_prone': [],
        }

        for col in v5_cols:
            col_H = {u: col[u] for u in H.nodes()}

            merge_colors = []
            for a in range(1, 5):
                nbrs = [u for u in T.neighbors(v)
                         if u in H.nodes() and col_H[u] in (a, 5)]
                if len(nbrs) < 2:
                    continue
                chains = set()
                for u in nbrs:
                    chains.add(get_kempe_chain(H, col_H, u, a, 5))
                if len(chains) >= 2:
                    merge_colors.append(a)

            if not merge_colors:
                categories['not_merge_prone'].append((col, col_H, []))
                continue

            opt_dist, all_opt = bfs_all_optimal_paths(H, col_H, k=5)
            if not all_opt or opt_dist <= 0:
                categories['not_merge_prone'].append((col, col_H, merge_colors))
                continue

            has_safe = any(
                classify_path_safety(T, H, v, col, p)['path_is_safe']
                for p in all_opt
            )

            if has_safe:
                categories['has_safe_opt'].append((col, col_H, merge_colors))
            else:
                categories['all_unsafe'].append((col, col_H, merge_colors))

        print(f"\nCategories:")
        print(f"  All-paths-unsafe (TRUE CE):  {len(categories['all_unsafe'])}")
        print(f"  Has safe optimal path:       {len(categories['has_safe_opt'])}")
        print(f"  Not merge-prone / trivial:   {len(categories['not_merge_prone'])}")

        # Compute rigidity for each category
        for cat_name, cat_data in categories.items():
            if not cat_data:
                continue

            rigidities_global = []
            rigidities_local = []
            incident_tension_lists = []

            for col, col_H, mcolors in cat_data:
                for a in (mcolors if mcolors else range(1, 5)):
                    all_chains = get_all_kempe_chains(H, col_H, a, 5)
                    if len(all_chains) <= 1:
                        continue

                    all_t = [compute_normalized_tension(adj_H, K) for K in all_chains]
                    rho_g = float(np.var(all_t))
                    rigidities_global.append(rho_g)

                    incident_chains = []
                    for K in all_chains:
                        if any(u in K for u in T.neighbors(v) if u in H.nodes()):
                            incident_chains.append(K)

                    inc_t = [compute_normalized_tension(adj_H, K) for K in incident_chains]
                    incident_tension_lists.append(inc_t)
                    if len(inc_t) > 1:
                        rho_l = float(np.var(inc_t))
                        rigidities_local.append(rho_l)

            print(f"\n  --- {cat_name} ({len(cat_data)} colorings) ---")

            if rigidities_global:
                rg = np.array(rigidities_global)
                print(f"  Global ρ: mean={np.mean(rg):.6f}, "
                      f"std={np.std(rg):.6f}, "
                      f"min={np.min(rg):.6f}, max={np.max(rg):.6f}")
                print(f"    ρ=0: {np.sum(rg < 1e-12)}/{len(rg)}, "
                      f"ρ>0: {np.sum(rg >= 1e-12)}/{len(rg)}")

            if rigidities_local:
                rl = np.array(rigidities_local)
                print(f"  Local ρ:  mean={np.mean(rl):.6f}, "
                      f"std={np.std(rl):.6f}, "
                      f"min={np.min(rl):.6f}, max={np.max(rl):.6f}")
                print(f"    ρ=0: {np.sum(rl < 1e-12)}/{len(rl)}, "
                      f"ρ>0: {np.sum(rl >= 1e-12)}/{len(rl)}")

            if incident_tension_lists:
                all_inc = [t for ts in incident_tension_lists for t in ts]
                if all_inc:
                    ait = np.array(all_inc)
                    print(f"  Incident σ̄: mean={np.mean(ait):.4f}, "
                          f"std={np.std(ait):.4f}, "
                          f"unique={sorted(set(np.round(ait, 4)))}")

            for idx, (col, col_H, mcolors) in enumerate(cat_data[:3]):
                for a in (mcolors if mcolors else []):
                    all_chains = get_all_kempe_chains(H, col_H, a, 5)
                    all_t = [compute_normalized_tension(adj_H, K) for K in all_chains]
                    sizes = [len(K) for K in all_chains]

                    incident_info = []
                    for K in all_chains:
                        inc = any(u in K for u in T.neighbors(v) if u in H.nodes())
                        if inc:
                            incident_info.append({
                                'size': len(K),
                                'sigma_bar': compute_normalized_tension(adj_H, K),
                                'sigma': compute_chain_boundary(adj_H, K),
                            })

                    print(f"    Example {idx}: a={a}, "
                          f"{len(all_chains)} chains, sizes={sizes}")
                    print(f"      All σ̄: {[round(t, 4) for t in all_t]}")
                    print(f"      v-incident chains: {incident_info}")


def full_n9_merge_rigidity():
    """
    Compute rigidity for ALL merge-prone cases across ALL n=9 triangulations,
    classified by whether they have safe optimal paths.
    """
    db = generate_triangulations(9)
    print(f"\n{'='*70}")
    print("FULL n=9 MERGE-PRONE RIGIDITY ANALYSIS")
    print(f"{'='*70}")

    all_data = {
        'all_unsafe': {'global_rig': [], 'local_rig': []},
        'has_safe': {'global_rig': [], 'local_rig': []},
    }

    total_graphs = len(db[9])
    for idx, T in enumerate(db[9]):
        name = T.graph.get('name', f'T_9_{idx}')
        t0 = time.time()

        for v in T.nodes():
            deg = T.degree(v)
            if deg not in (4, 5):
                continue

            H = T.copy()
            H.remove_node(v)
            adj_H = _nx_to_adj(H)

            all_cols = enumerate_colourings(T, 5)
            v5_cols = [c for c in all_cols if c[v] == 5 and num_colours(c) == 5]

            for col in v5_cols:
                col_H = {u: col[u] for u in H.nodes()}

                for a in range(1, 5):
                    nbrs = [u for u in T.neighbors(v)
                             if u in H.nodes() and col_H[u] in (a, 5)]
                    if len(nbrs) < 2:
                        continue
                    chains_at_v = set()
                    for u in nbrs:
                        chains_at_v.add(get_kempe_chain(H, col_H, u, a, 5))
                    if len(chains_at_v) < 2:
                        continue

                    # This is merge-prone; compute rigidity
                    all_chains = get_all_kempe_chains(H, col_H, a, 5)
                    all_t = [compute_normalized_tension(adj_H, K) for K in all_chains]
                    rho_g = float(np.var(all_t)) if len(all_t) > 1 else 0.0

                    inc_chains = [K for K in all_chains
                                   if any(u in K for u in T.neighbors(v) if u in H.nodes())]
                    inc_t = [compute_normalized_tension(adj_H, K) for K in inc_chains]
                    rho_l = float(np.var(inc_t)) if len(inc_t) > 1 else 0.0

                    # Check BFS safety
                    opt_dist, all_opt = bfs_all_optimal_paths(H, col_H, k=5)
                    if not all_opt or opt_dist <= 0:
                        continue

                    has_safe = any(
                        classify_path_safety(T, H, v, col, p)['path_is_safe']
                        for p in all_opt
                    )

                    cat = 'has_safe' if has_safe else 'all_unsafe'
                    all_data[cat]['global_rig'].append(rho_g)
                    all_data[cat]['local_rig'].append(rho_l)

        elapsed = time.time() - t0
        if (idx + 1) % 10 == 0 or idx == 0:
            au = len(all_data['all_unsafe']['global_rig'])
            hs = len(all_data['has_safe']['global_rig'])
            print(f"  [{idx+1}/{total_graphs}] {name} ({elapsed:.1f}s): "
                  f"all_unsafe={au}, has_safe={hs}")

    print(f"\n  RESULTS:")
    for cat in ['all_unsafe', 'has_safe']:
        gd = all_data[cat]['global_rig']
        ld = all_data[cat]['local_rig']
        if gd:
            ga = np.array(gd)
            la = np.array(ld) if ld else np.array([0])
            print(f"\n  {cat} ({len(gd)} cases):")
            print(f"    Global ρ: mean={np.mean(ga):.6f}, ρ=0: {np.sum(ga<1e-12)}, ρ>0: {np.sum(ga>=1e-12)}")
            print(f"    Local ρ:  mean={np.mean(la):.6f}, ρ=0: {np.sum(la<1e-12)}, ρ>0: {np.sum(la>=1e-12)}")

    return all_data


if __name__ == '__main__':
    print("=" * 70)
    print("TARGETED SURFACE TENSION ANALYSIS — Agent 1520-M2-S1")
    print("=" * 70)

    analyze_counterexample_graphs()

    print("\n\n" + "=" * 70)
    print("PHASE 2: Full n=9 all-paths classification")
    print("WARNING: This may take several minutes")
    print("=" * 70)

    data = full_n9_merge_rigidity()

    print("\n" + "=" * 70)
    print("TARGETED ANALYSIS COMPLETE")
    print("=" * 70)
