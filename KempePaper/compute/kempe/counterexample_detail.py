"""
counterexample_detail.py — Extract full details of counterexamples to {1,2,3,4}-Swap Sufficiency.

KILL CRITERION TRIGGERED: At n=9, T_9_25 (vertex 3, deg 5) and T_9_35 (vertex 6, deg 4)
have colourings where ALL BFS-optimal paths use unsafe (merge-prone) swaps.
"""

import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))

from typing import Dict, List, Set, Tuple, Optional, FrozenSet
from collections import deque
import networkx as nx

from kempe_ops import (
    Colouring, CanonicalColouring,
    get_kempe_chain, get_all_kempe_chains, kempe_swap,
    enumerate_colourings, num_colours,
    canonical_form, colouring_from_canonical, all_kempe_neighbours,
)
from triangulation_db import generate_triangulations
from reduction_search import bfs_reduce_to_4, _identify_swap
from verify_counterexamples import is_step_unsafe, check_path_safety, find_safe_bfs_path


def extract_counterexample_details(T: nx.Graph, v: int, col: Colouring) -> Dict:
    """Extract full details of a counterexample case."""
    H = T.copy()
    H.remove_node(v)
    col_H = {u: col[u] for u in H.nodes()}

    nbrs = sorted(T.neighbors(v))
    nbr_colours = {u: col[u] for u in nbrs}

    merge_info = {}
    for a in range(1, 5):
        nbrs_in = [u for u in nbrs if col_H.get(u) in (a, 5)]
        if len(nbrs_in) < 2:
            continue
        chains = {}
        for u in nbrs_in:
            chains[u] = get_kempe_chain(H, col_H, u, a, 5)
        distinct = set(chains.values())
        if len(distinct) >= 2:
            merge_info[a] = {
                'nbrs_in_ba5': nbrs_in,
                'num_distinct_chains': len(distinct),
                'chain_sizes': [len(ch) for ch in distinct],
            }

    path_H = bfs_reduce_to_4(H, col_H, k=5)
    path_length = len(path_H) if path_H else 0

    path_details = []
    if path_H and len(path_H) > 1:
        col_G = dict(col)
        for i in range(len(path_H) - 1):
            cur_H = colouring_from_canonical(H, path_H[i])
            nxt_H = colouring_from_canonical(H, path_H[i + 1])
            a, b = _identify_swap(H, cur_H, nxt_H)
            swapped = frozenset(u for u in H.nodes() if cur_H[u] != nxt_H[u])
            unsafe = is_step_unsafe(T, H, v, col_G, cur_H, nxt_H)

            step = {
                'step': i,
                'swap_pair': (a, b),
                'chain_size': len(swapped),
                'is_a5': a is not None and 5 in (a, b),
                'is_14': a is not None and 5 not in (a, b),
                'is_unsafe': unsafe,
                'swapped_vertices': sorted(swapped),
            }

            if a is not None and 5 in (a, b):
                the_a = a if a != 5 else b
                col_H_cur = {w: col_G[w] for w in H.nodes()}
                v_nbrs_in = [u for u in T.neighbors(v)
                             if u in H.nodes() and col_H_cur.get(u) in (the_a, 5)]
                chains_nbrs = set()
                for u in v_nbrs_in:
                    chains_nbrs.add(get_kempe_chain(H, col_H_cur, u, the_a, 5))
                step['merge_prone'] = len(chains_nbrs) >= 2
                step['num_chains_at_v'] = len(chains_nbrs)
                step['v_nbrs_in_ba5'] = v_nbrs_in

            if swapped and a is not None:
                col_G = kempe_swap(col_G, swapped, a, b)

            path_details.append(step)

    verification = find_safe_bfs_path(T, H, v, col, max_paths=10000)

    return {
        'graph_edges': sorted(T.edges()),
        'graph_nodes': sorted(T.nodes()),
        'vertex': v,
        'degree': T.degree(v),
        'colouring': dict(col),
        'neighbours': nbrs,
        'neighbour_colours': nbr_colours,
        'merge_info': merge_info,
        'bfs_path_length': path_length,
        'path_details': path_details,
        'verification': verification,
    }


def main():
    print("=" * 70)
    print("COUNTEREXAMPLE DETAIL EXTRACTION")
    print("=" * 70)

    db = generate_triangulations(9)

    counterexample_graphs = {
        25: [3],
        35: [6],
    }

    all_details = []

    for graph_idx, vertices in counterexample_graphs.items():
        T = db[9][graph_idx]
        name = T.graph.get('name', f'T_9_{graph_idx}')
        print(f"\n{'='*50}")
        print(f"Graph: {name}")
        print(f"Edges: {sorted(T.edges())}")
        print(f"Degree sequence: {sorted([T.degree(v) for v in T.nodes()])}")

        for v in vertices:
            print(f"\nVertex {v}, degree {T.degree(v)}")
            print(f"Neighbours: {sorted(T.neighbors(v))}")

            all_cols = enumerate_colourings(T, 5)
            v5_cols = [c for c in all_cols if c[v] == 5 and num_colours(c) == 5]
            print(f"5-colourings with c(v)=5: {len(v5_cols)}")

            ce_count = 0
            for col in v5_cols:
                col_H = {u: col[u] for u in T.nodes() if u != v}

                H = T.copy()
                H.remove_node(v)
                is_mp = False
                for a in range(1, 5):
                    nbrs_in = [u for u in T.neighbors(v)
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

                path_H = bfs_reduce_to_4(H, col_H, k=5)
                if path_H is None or len(path_H) <= 1:
                    continue

                first_safe = check_path_safety(T, H, v, col, path_H)
                if first_safe:
                    continue

                verif = find_safe_bfs_path(T, H, v, col, max_paths=10000)
                if not verif['safe_path_exists']:
                    ce_count += 1
                    if ce_count <= 3:
                        details = extract_counterexample_details(T, v, col)
                        all_details.append(details)
                        print(f"\n  COUNTEREXAMPLE #{ce_count}:")
                        print(f"    Colouring: {dict(col)}")
                        nbrs = sorted(T.neighbors(v))
                        print(f"    Neighbour colours: {[col[u] for u in nbrs]}")
                        print(f"    Merge info: {details['merge_info']}")
                        print(f"    BFS path length: {details['bfs_path_length']}")
                        for step in details['path_details']:
                            unsafe_marker = " *** UNSAFE ***" if step['is_unsafe'] else ""
                            print(f"      Step {step['step']}: swap {step['swap_pair']}, "
                                  f"chain_size={step['chain_size']}{unsafe_marker}")
                            if step.get('merge_prone'):
                                print(f"        merge_prone=True, chains_at_v={step['num_chains_at_v']}, "
                                      f"v_nbrs={step.get('v_nbrs_in_ba5')}")
                        print(f"    Verification: {verif}")

            print(f"\n  Total counterexamples at vertex {v}: {ce_count}")

    out_path = os.path.join(os.path.dirname(__file__),
                            '..', '..', 'backgroundMaterial', 'agent1520',
                            'coordinator', 'manager_M1', 'sub_S3',
                            'counterexample_details.json')
    with open(out_path, 'w') as f:
        serializable = []
        for d in all_details:
            sd = dict(d)
            sd['graph_edges'] = [list(e) for e in sd['graph_edges']]
            sd['path_details'] = [{k: (list(v) if isinstance(v, (frozenset, set)) else v)
                                   for k, v in step.items()} for step in sd['path_details']]
            serializable.append(sd)
        json.dump(serializable, f, indent=2, default=str)
    print(f"\nDetails saved to {out_path}")


if __name__ == '__main__':
    main()
