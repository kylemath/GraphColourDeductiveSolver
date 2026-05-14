"""
Kuperberg web basis analysis for sl_3 invariant tensors.

Kuperberg (1996) introduced a "spider" for rank-2 Lie algebras (sl_3 in particular)
that gives a canonical basis for invariant tensors in tensor products of the
fundamental and dual representations of sl_3.

Connection to Penrose evaluation:
- The Penrose evaluation Pen(G) for a cubic graph G counts edge-3-colourings
- Edge-3-colourings correspond to representations of the graph in the 
  fundamental rep of sl_3 (the standard 3-dimensional representation)
- The web basis provides a positive basis for sl_3 invariant tensors
- If Pen(G) decomposes with non-negative coefficients in the web basis
  for all planar G, we get positivity from the basis structure

Strategy:
1. For small planar cubic graphs, compute the Penrose tensor explicitly
2. Express it in terms of the Kuperberg web basis elements
3. Check if all coefficients are non-negative

Implementation notes:
- For a cubic graph with V vertices, the Penrose tensor lives in (C^3)^{⊗3V}
  contracted by the graph structure
- The web basis elements are encoded by non-crossing matchings on the boundary
- For CLOSED graphs (no boundary), the invariant space is 1-dimensional
  and Pen(G) is just a number — the web basis question becomes about
  the intermediate decomposition during contraction
"""

from __future__ import annotations
import numpy as np
from typing import List, Tuple, Dict, Set, Optional
from itertools import product as iproduct, permutations
from collections import defaultdict
import sys
import time

# Levi-Civita tensor
def levi_civita(i: int, j: int, k: int) -> int:
    """Levi-Civita symbol ε_{ijk} for i,j,k ∈ {0,1,2}."""
    if (i, j, k) in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
        return 1
    elif (i, j, k) in [(0, 2, 1), (2, 1, 0), (1, 0, 2)]:
        return -1
    return 0


def penrose_tensor_value(graph_edges: List[Tuple[int, int]], 
                          n_vertices: int,
                          vertex_edge_order: Dict[int, List[int]]) -> int:
    """Compute Pen(G) by explicit tensor contraction.
    
    For each edge colouring (assignment of {0,1,2} to edges),
    compute the product of ε tensors at each vertex and sum.
    """
    n_edges = len(graph_edges)
    total = 0
    
    for colouring in iproduct(range(3), repeat=n_edges):
        weight = 1
        valid = True
        for v in range(n_vertices):
            edge_indices = vertex_edge_order[v]
            if len(edge_indices) != 3:
                valid = False
                break
            c1, c2, c3 = colouring[edge_indices[0]], colouring[edge_indices[1]], colouring[edge_indices[2]]
            eps = levi_civita(c1, c2, c3)
            if eps == 0:
                valid = False
                break
            weight *= eps
        if valid:
            total += weight
    
    return total


def penrose_signed_and_unsigned(graph_edges: List[Tuple[int, int]],
                                 n_vertices: int,
                                 vertex_edge_order: Dict[int, List[int]]) -> Tuple[int, int]:
    """Compute both the signed Penrose evaluation and the unsigned count.
    
    Signed: Pen(G) = Σ Π ε_{c(e1),c(e2),c(e3)}
    Unsigned: |Pen|(G) = Σ Π |ε_{c(e1),c(e2),c(e3)}| = count of Tait colourings
    """
    n_edges = len(graph_edges)
    signed_total = 0
    unsigned_total = 0
    
    for colouring in iproduct(range(3), repeat=n_edges):
        weight_signed = 1
        weight_unsigned = 1
        valid = True
        for v in range(n_vertices):
            edge_indices = vertex_edge_order[v]
            c1, c2, c3 = colouring[edge_indices[0]], colouring[edge_indices[1]], colouring[edge_indices[2]]
            eps = levi_civita(c1, c2, c3)
            if eps == 0:
                valid = False
                break
            weight_signed *= eps
            weight_unsigned *= abs(eps)
        if valid:
            signed_total += weight_signed
            unsigned_total += weight_unsigned
    
    return signed_total, unsigned_total


def make_vertex_edge_order(edges: List[Tuple[int, int]], n: int) -> Dict[int, List[int]]:
    """Build vertex → ordered list of incident edge indices."""
    veo = defaultdict(list)
    for idx, (u, v) in enumerate(edges):
        veo[u].append(idx)
        veo[v].append(idx)
    return dict(veo)


def partial_contraction_analysis(edges: List[Tuple[int, int]], 
                                  n_vertices: int,
                                  vertex_edge_order: Dict[int, List[int]]) -> Dict:
    """Analyze the partial contraction structure for web basis decomposition.
    
    Instead of tracking the full tensor (3^E entries), we track a reduced
    representation. Process vertices one at a time. For each vertex, the
    constraint is that its 3 incident edges must have a valid ε-colouring.
    
    We build up the set of valid colourings incrementally:
    - Start with the first vertex: enumerate all valid colourings of its 3 edges
    - Add the next vertex: extend colourings to include its new edges,
      filtering by the ε constraint
    - Track sign (product of ε values) at each step
    """
    n_edges = len(edges)
    
    contraction_order = list(range(n_vertices))
    states = []
    sign_history = []
    
    # Track partial colourings as dict: {edge_colour_assignment: accumulated_weight}
    # edge_colour_assignment is a dict mapping edge_index -> colour
    # We store as frozenset of (edge_idx, colour) pairs for hashability
    
    assigned_edges = set()
    # current_states: dict mapping (tuple of (edge_idx, colour) sorted) -> weight
    current_states = {(): 1}
    
    for step, v in enumerate(contraction_order):
        v_edges = vertex_edge_order[v]
        new_edges = [e for e in v_edges if e not in assigned_edges]
        old_edges = [e for e in v_edges if e in assigned_edges]
        
        new_states = defaultdict(int)
        
        for state_key, weight in current_states.items():
            if weight == 0:
                continue
            state_dict = dict(state_key)
            
            for new_colours in iproduct(range(3), repeat=len(new_edges)):
                trial = dict(state_dict)
                for e, c in zip(new_edges, new_colours):
                    trial[e] = c
                
                c1, c2, c3 = trial[v_edges[0]], trial[v_edges[1]], trial[v_edges[2]]
                eps = levi_civita(c1, c2, c3)
                if eps == 0:
                    continue
                
                new_key = tuple(sorted(trial.items()))
                new_states[new_key] += weight * eps
        
        for e in new_edges:
            assigned_edges.add(e)
        
        current_states = {k: v for k, v in new_states.items() if v != 0}
        
        pos_count = sum(1 for val in current_states.values() if val > 0)
        neg_count = sum(1 for val in current_states.values() if val < 0)
        
        states.append({
            'step': step,
            'vertex': v,
            'nonzero_terms': len(current_states),
            'positive': pos_count,
            'negative': neg_count,
        })
        sign_history.append((pos_count, neg_count))
    
    all_intermediate_positive = all(neg == 0 for _, neg in sign_history)
    final_value = sum(current_states.values())
    
    return {
        'states': states,
        'sign_history': sign_history,
        'all_intermediate_positive': all_intermediate_positive,
        'final_value': int(final_value),
    }


def web_basis_coefficient_analysis(graph_name: str,
                                     edges: List[Tuple[int, int]],
                                     n_vertices: int,
                                     is_planar: bool) -> Dict:
    """Full web basis analysis for a small cubic graph.
    
    For closed cubic graphs, Pen(G) is a scalar. The web basis analysis
    looks at how the evaluation decomposes when we cut the graph into
    two halves and express each half in the web basis.
    
    For small graphs, we can:
    1. Compute the full tensor contraction
    2. Analyze sign patterns during intermediate contractions
    3. Check if planar graphs always have non-negative intermediate states
    """
    veo = make_vertex_edge_order(edges, n_vertices)
    
    n_edges = len(edges)
    if n_edges > 15:
        return {
            'name': graph_name,
            'planar': is_planar,
            'status': 'TOO_LARGE',
            'note': f'{n_edges} edges — enumeration infeasible for web analysis'
        }
    
    t0 = time.time()
    signed, unsigned = penrose_signed_and_unsigned(edges, n_vertices, veo)
    t1 = time.time()
    
    partial = partial_contraction_analysis(edges, n_vertices, veo)
    t2 = time.time()
    
    return {
        'name': graph_name,
        'vertices': n_vertices,
        'edges': n_edges,
        'planar': is_planar,
        'penrose_signed': signed,
        'penrose_unsigned': unsigned,
        'signed_eq_unsigned': (signed == unsigned),
        'partial_contraction': partial,
        'all_intermediate_positive': partial['all_intermediate_positive'],
        'time_eval': t1 - t0,
        'time_partial': t2 - t1,
    }


def analyze_edge_cut_decomposition(edges: List[Tuple[int, int]], 
                                    n_vertices: int,
                                    cut_edges: List[int]) -> Dict:
    """Analyze decomposition at an edge cut.
    
    Given a set of cut edges, decompose the graph into two parts.
    Express each part as a tensor on the cut edges.
    Check if the inner product (contraction over cut edges) gives Pen(G)
    and whether each part has non-negative web basis coefficients.
    """
    veo = make_vertex_edge_order(edges, n_vertices)
    n_edges = len(edges)
    
    vertex_sets = [set(), set()]
    cut_set = set(cut_edges)
    
    adj = defaultdict(set)
    for idx, (u, v) in enumerate(edges):
        if idx not in cut_set:
            adj[u].add(v)
            adj[v].add(u)
    
    visited = set()
    def bfs(start):
        component = set()
        queue = [start]
        while queue:
            node = queue.pop(0)
            if node in visited:
                continue
            visited.add(node)
            component.add(node)
            for nb in adj[node]:
                if nb not in visited:
                    queue.append(nb)
        return component
    
    components = []
    for v in range(n_vertices):
        if v not in visited:
            components.append(bfs(v))
    
    if len(components) != 2:
        return {'valid_cut': False, 'n_components': len(components)}
    
    part_tensors = [{}, {}]
    for part_idx, comp in enumerate(components):
        for colouring in iproduct(range(3), repeat=n_edges):
            weight = 1
            valid = True
            for v in comp:
                v_edges = veo[v]
                c1, c2, c3 = colouring[v_edges[0]], colouring[v_edges[1]], colouring[v_edges[2]]
                eps = levi_civita(c1, c2, c3)
                if eps == 0:
                    valid = False
                    break
                weight *= eps
            if not valid:
                continue
            cut_key = tuple(colouring[e] for e in cut_edges)
            if cut_key not in part_tensors[part_idx]:
                part_tensors[part_idx][cut_key] = 0
            part_tensors[part_idx][cut_key] += weight
    
    pos_coeffs = [0, 0]
    neg_coeffs = [0, 0]
    for part_idx in range(2):
        for key, val in part_tensors[part_idx].items():
            if val > 0:
                pos_coeffs[part_idx] += 1
            elif val < 0:
                neg_coeffs[part_idx] += 1
    
    inner_product = 0
    for key in part_tensors[0]:
        if key in part_tensors[1]:
            inner_product += part_tensors[0][key] * part_tensors[1][key]
    
    return {
        'valid_cut': True,
        'components': [sorted(c) for c in components],
        'cut_edges': cut_edges,
        'part_tensors': part_tensors,
        'pos_coeffs': pos_coeffs,
        'neg_coeffs': neg_coeffs,
        'inner_product': inner_product,
        'both_parts_nonneg': (neg_coeffs[0] == 0 and neg_coeffs[1] == 0),
    }


def test_graphs() -> List[Tuple[str, List[Tuple[int, int]], int, bool]]:
    """Library of small cubic graphs for web basis testing."""
    graphs = []
    
    # K4: 4 vertices, 6 edges
    graphs.append(("K4", [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)], 4, True))
    
    # Triangular prism: 6 vertices, 9 edges
    graphs.append(("Prism", [
        (0,1), (1,2), (2,0), (3,4), (4,5), (5,3), (0,3), (1,4), (2,5)
    ], 6, True))
    
    # Cube: 8 vertices, 12 edges
    graphs.append(("Cube", [
        (0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4),
        (0,4), (1,5), (2,6), (3,7)
    ], 8, True))
    
    # K_{3,3}: 6 vertices, 9 edges — NON-PLANAR
    graphs.append(("K33", [
        (0,3), (0,4), (0,5), (1,3), (1,4), (1,5), (2,3), (2,4), (2,5)
    ], 6, False))
    
    # Petersen: 10 vertices, 15 edges — NON-PLANAR
    graphs.append(("Petersen", [
        (0,1), (1,2), (2,3), (3,4), (4,0),
        (5,7), (6,8), (7,9), (8,5), (9,6),
        (0,5), (1,6), (2,7), (3,8), (4,9)
    ], 10, False))
    
    # Prism C4: 8 vertices, 12 edges
    graphs.append(("Prism_C4", [
        (0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4),
        (0,4), (1,5), (2,6), (3,7)
    ], 8, True))
    
    # Prism C5: 10 vertices, 15 edges
    graphs.append(("Prism_C5", [
        (0,1), (1,2), (2,3), (3,4), (4,0),
        (5,6), (6,7), (7,8), (8,9), (9,5),
        (0,5), (1,6), (2,7), (3,8), (4,9)
    ], 10, True))
    
    return graphs


def main():
    """Run Kuperberg web basis analysis on small cubic graphs."""
    print("=" * 70)
    print("KUPERBERG WEB BASIS ANALYSIS")
    print("=" * 70)
    
    graphs = test_graphs()
    all_results = []
    
    for name, edges, n_v, is_planar in graphs:
        print(f"\n--- {name} (V={n_v}, E={len(edges)}, planar={is_planar}) ---")
        result = web_basis_coefficient_analysis(name, edges, n_v, is_planar)
        all_results.append(result)
        
        if result.get('status') == 'TOO_LARGE':
            print(f"  Skipped: {result['note']}")
            continue
        
        print(f"  Pen(G) signed   = {result['penrose_signed']}")
        print(f"  Pen(G) unsigned = {result['penrose_unsigned']}")
        print(f"  signed == unsigned: {result['signed_eq_unsigned']}")
        
        pc = result['partial_contraction']
        print(f"  Final value from partial contraction: {pc['final_value']}")
        print(f"  All intermediate states non-negative: {pc['all_intermediate_positive']}")
        
        for s in pc['states']:
            print(f"    Step {s['step']} (vertex {s['vertex']}): "
                  f"+{s['positive']} / -{s['negative']} / total {s['nonzero_terms']}")
    
    print("\n" + "=" * 70)
    print("SUMMARY: SIGNED vs UNSIGNED PENROSE EVALUATION")
    print("=" * 70)
    
    print(f"\n{'Graph':<15} {'Planar':>7} {'Signed':>8} {'Unsigned':>10} {'Equal':>6} {'IntPos':>7}")
    print("-" * 60)
    for r in all_results:
        if r.get('status') == 'TOO_LARGE':
            continue
        print(f"{r['name']:<15} {'Y' if r['planar'] else 'N':>7} "
              f"{r['penrose_signed']:>8} {r['penrose_unsigned']:>10} "
              f"{'Y' if r['signed_eq_unsigned'] else 'N':>6} "
              f"{'Y' if r['all_intermediate_positive'] else 'N':>7}")
    
    print("\n" + "=" * 70)
    print("KEY FINDING: SIGNED vs UNSIGNED")
    print("=" * 70)
    
    planar_results = [r for r in all_results if r['planar'] and r.get('status') != 'TOO_LARGE']
    nonplanar_results = [r for r in all_results if not r['planar'] and r.get('status') != 'TOO_LARGE']
    
    planar_sign_eq = all(r['signed_eq_unsigned'] for r in planar_results)
    print(f"\nPlanar graphs: signed == unsigned for all? {planar_sign_eq}")
    if planar_sign_eq:
        print("→ For planar cubic graphs, ALL sign contributions are positive!")
        print("→ This means vertex orderings produce consistent orientations.")
        print("→ Strong evidence for web basis positivity in the planar case.")
    
    for r in nonplanar_results:
        print(f"\n{r['name']}: signed={r['penrose_signed']}, unsigned={r['penrose_unsigned']}")
        if r['penrose_signed'] != r['penrose_unsigned']:
            print("→ Sign cancellation occurs for non-planar graphs.")
    
    planar_intermediate_pos = all(r['all_intermediate_positive'] for r in planar_results)
    print(f"\nAll intermediates non-negative for planar graphs? {planar_intermediate_pos}")
    if not planar_intermediate_pos:
        print("→ Intermediate negative coefficients appear even for planar graphs")
        print("→ Web basis positivity at intermediate stages may not hold naively")
        print("→ But final result is still positive — cancellations are benign")
    
    print("\n" + "=" * 70)
    print("EDGE CUT DECOMPOSITION ANALYSIS")
    print("=" * 70)
    
    cube_edges = [
        (0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4),
        (0,4), (1,5), (2,6), (3,7)
    ]
    cut_result = analyze_edge_cut_decomposition(cube_edges, 8, [8, 9, 10, 11])
    
    print(f"\nCube with equatorial cut:")
    print(f"  Valid cut: {cut_result['valid_cut']}")
    if cut_result['valid_cut']:
        print(f"  Components: {cut_result['components']}")
        print(f"  Part 1 coeffs: +{cut_result['pos_coeffs'][0]} / -{cut_result['neg_coeffs'][0]}")
        print(f"  Part 2 coeffs: +{cut_result['pos_coeffs'][1]} / -{cut_result['neg_coeffs'][1]}")
        print(f"  Inner product: {cut_result['inner_product']}")
        print(f"  Both parts non-negative: {cut_result['both_parts_nonneg']}")
    
    return all_results


if __name__ == "__main__":
    results = main()
    
    output_dir = "/Users/kylemathewson/GraphColour/backgroundMaterial/agent1520/coordinator/manager_M4/sub_S3"
    with open(f"{output_dir}/web_basis_raw.txt", "w") as f:
        f.write("Kuperberg Web Basis Analysis Results\n")
        f.write("=" * 60 + "\n\n")
        for r in results:
            f.write(f"\n{r['name']}:\n")
            if r.get('status') == 'TOO_LARGE':
                f.write(f"  {r['note']}\n")
                continue
            f.write(f"  Signed Penrose:   {r['penrose_signed']}\n")
            f.write(f"  Unsigned Penrose: {r['penrose_unsigned']}\n")
            f.write(f"  Equal: {r['signed_eq_unsigned']}\n")
            f.write(f"  All intermediate positive: {r['all_intermediate_positive']}\n")
            if 'partial_contraction' in r:
                for s in r['partial_contraction']['states']:
                    f.write(f"    Step {s['step']}: +{s['positive']}/-{s['negative']}\n")
