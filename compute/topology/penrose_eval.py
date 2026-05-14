"""
Penrose evaluation Pen(G) for bridgeless planar cubic graphs.

Pen(G) = number of proper edge-3-colourings (Tait colourings) of G,
weighted by the Levi-Civita sign product at each vertex.

For a cubic graph G, a Tait colouring assigns labels {1,2,3} to edges
such that all three labels appear at every vertex. The Penrose evaluation
counts these colourings (each contributes +1 because |ε_{abc}| = 1 for
any permutation of {1,2,3}).

Kauffman (1990): 4CT ⟺ Pen(G) > 0 for all bridgeless planar cubic G.

This module:
- Generates bridgeless planar cubic graphs up to ~20 vertices
- Counts Tait colourings by backtracking
- Verifies Pen(G) > 0 for planar, Pen(Petersen) = 0
"""

from __future__ import annotations
import sys
import os
from typing import List, Tuple, Dict, Set, Optional
from itertools import product as iproduct
from collections import defaultdict
import time

try:
    import networkx as nx
    HAS_NX = True
except ImportError:
    HAS_NX = False
    print("WARNING: networkx not available, using manual graph construction only")


def make_cubic_graph(edges: List[Tuple[int, int]], n: int) -> Dict:
    """Create a cubic graph from edge list."""
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return {
        'n': n,
        'edges': edges,
        'adj': dict(adj),
    }


def is_bridgeless(graph: Dict) -> bool:
    """Check if graph is bridgeless (2-edge-connected) using DFS."""
    n = graph['n']
    adj = graph['adj']
    if n == 0:
        return True

    visited = [False] * n
    disc = [0] * n
    low = [0] * n
    timer = [0]
    has_bridge = [False]

    def dfs(u: int, parent: int):
        visited[u] = True
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        for v in adj.get(u, []):
            if not visited[v]:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    has_bridge[0] = True
            elif v != parent:
                low[u] = min(low[u], disc[v])

    sys.setrecursionlimit(10000)
    dfs(0, -1)
    return not has_bridge[0]


def count_tait_colourings(graph: Dict) -> int:
    """Count edge-3-colourings (Tait colourings) by backtracking.
    
    A Tait colouring assigns {1,2,3} to edges so that at each vertex,
    all three colours appear.
    """
    edges = graph['edges']
    adj = graph['adj']
    n_edges = len(edges)
    
    edge_colours = [0] * n_edges
    
    vertex_edges = defaultdict(list)
    for idx, (u, v) in enumerate(edges):
        vertex_edges[u].append(idx)
        vertex_edges[v].append(idx)
    
    vertex_edge_colours = defaultdict(set)
    
    count = [0]
    
    def backtrack(edge_idx: int):
        if edge_idx == n_edges:
            count[0] += 1
            return
        
        u, v = edges[edge_idx]
        used_u = vertex_edge_colours[u]
        used_v = vertex_edge_colours[v]
        
        for colour in [1, 2, 3]:
            if colour not in used_u and colour not in used_v:
                edge_colours[edge_idx] = colour
                used_u.add(colour)
                used_v.add(colour)
                backtrack(edge_idx + 1)
                used_u.discard(colour)
                used_v.discard(colour)
        
        edge_colours[edge_idx] = 0
    
    backtrack(0)
    return count[0]


def penrose_eval(graph: Dict) -> int:
    """Compute Pen(G) = number of Tait colourings.
    
    For cubic graphs, every valid edge-3-colouring contributes +1 to
    Pen(G) because |ε(σ)| = 1 for any permutation σ of {1,2,3}.
    """
    return count_tait_colourings(graph)


# ============================================================
# GRAPH LIBRARY: Bridgeless planar cubic graphs
# ============================================================

def tetrahedron_graph() -> Dict:
    """K4 — smallest cubic graph, 4 vertices, 6 edges. Planar."""
    edges = [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]
    return make_cubic_graph(edges, 4)

def prism_graph() -> Dict:
    """Triangular prism (K3 × K2) — 6 vertices, 9 edges. Planar."""
    edges = [
        (0,1), (1,2), (2,0),
        (3,4), (4,5), (5,3),
        (0,3), (1,4), (2,5),
    ]
    return make_cubic_graph(edges, 6)

def cube_graph() -> Dict:
    """Cube Q3 — 8 vertices, 12 edges. Planar."""
    edges = [
        (0,1), (1,2), (2,3), (3,0),
        (4,5), (5,6), (6,7), (7,4),
        (0,4), (1,5), (2,6), (3,7),
    ]
    return make_cubic_graph(edges, 8)

def petersen_graph() -> Dict:
    """Petersen graph — 10 vertices, 15 edges. NON-PLANAR. Pen should be 0."""
    edges = [
        (0,1), (1,2), (2,3), (3,4), (4,0),
        (5,7), (6,8), (7,9), (8,5), (9,6),
        (0,5), (1,6), (2,7), (3,8), (4,9),
    ]
    return make_cubic_graph(edges, 10)

def dodecahedron_graph() -> Dict:
    """Dodecahedron — 20 vertices, 30 edges. Planar."""
    edges = [
        (0,1), (1,2), (2,3), (3,4), (4,0),
        (0,5), (1,6), (2,7), (3,8), (4,9),
        (5,10), (6,10), (6,11), (7,11), (7,12),
        (8,12), (8,13), (9,13), (9,14), (5,14),
        (10,15), (11,16), (12,17), (13,18), (14,19),
        (15,16), (16,17), (17,18), (18,19), (19,15),
    ]
    return make_cubic_graph(edges, 20)

def octahedron_dual_graph() -> Dict:
    """Dual of octahedron = cube. Same as cube_graph."""
    return cube_graph()

def k33_graph() -> Dict:
    """K_{3,3} — 6 vertices, 9 edges. NON-PLANAR. Tait colourings exist but it's not planar."""
    edges = [
        (0,3), (0,4), (0,5),
        (1,3), (1,4), (1,5),
        (2,3), (2,4), (2,5),
    ]
    return make_cubic_graph(edges, 6)

def icosahedron_dual_graph() -> Dict:
    """Dual of icosahedron = dodecahedron. Same as dodecahedron."""
    return dodecahedron_graph()

def truncated_tetrahedron() -> Dict:
    """Truncated tetrahedron — 12 vertices, 18 edges. Planar, cubic."""
    edges = [
        (0,1), (1,2), (2,3), (3,4), (4,5), (5,0),
        (0,6), (2,7), (4,8),
        (6,9), (7,10), (8,11),
        (9,10), (10,11), (11,9),
        (1,6), (3,7), (5,8),
    ]
    g = make_cubic_graph(edges, 12)
    return g

def cuboctahedron_graph() -> Dict:
    """Cuboctahedron dual (rhombic dodecahedron). 
    Actually let's use the Frucht graph — 12 vertices, 18 edges, cubic, planar."""
    edges = [
        (0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (6,0),
        (0,7), (1,7), (2,8), (3,8), (4,9), (5,9), (6,10),
        (7,11), (8,11), (9,10), (10,11),
    ]
    return make_cubic_graph(edges, 12)

def generate_planar_cubic_from_nx(n: int) -> List[Dict]:
    """Generate small bridgeless planar cubic graphs using networkx utilities."""
    if not HAS_NX:
        return []
    
    graphs = []
    
    if n == 4:
        G = nx.complete_graph(4)
        edges = list(G.edges())
        graphs.append(make_cubic_graph(edges, 4))
    
    if n == 6:
        G = nx.circular_ladder_graph(3)
        edges = list(G.edges())
        graphs.append(make_cubic_graph(edges, 6))
    
    if n == 8:
        G = nx.cubical_graph()
        edges = list(G.edges())
        graphs.append(make_cubic_graph(edges, 8))
        
        G2 = nx.moebius_kantor_graph()
        if nx.check_planarity(G2)[0]:
            edges2 = list(G2.edges())
            graphs.append(make_cubic_graph(edges2, G2.number_of_nodes()))
    
    if n == 10:
        G = nx.petersen_graph()
        edges = list(G.edges())
        graphs.append(make_cubic_graph(edges, 10))
    
    if n == 12:
        try:
            G = nx.frucht_graph()
            edges = list(G.edges())
            g = make_cubic_graph(edges, G.number_of_nodes())
            graphs.append(g)
        except:
            pass
    
    if n == 20:
        G = nx.dodecahedral_graph()
        edges = list(G.edges())
        graphs.append(make_cubic_graph(edges, 20))
    
    return graphs


def double_triangle_graph() -> Dict:
    """Two triangles sharing an edge then doubled — 
    actually: K4 with one edge subdivided twice and reconnected.
    Let's use a simpler well-known one: the dipyramid dual."""
    return tetrahedron_graph()


def generate_cubic_by_expansion(base: Dict, steps: int = 1) -> Dict:
    """Generate a larger cubic graph by edge expansion.
    
    Replace an edge (u,v) with a square: u-a-b-v and u-c-d-v 
    where a-c and b-d are new edges. This adds 4 vertices.
    """
    edges = list(base['edges'])
    n = base['n']
    adj = dict(base['adj'])
    
    for _ in range(steps):
        if not edges:
            break
        eu, ev = edges[0]
        
        a, b, c, d = n, n+1, n+2, n+3
        
        new_edges = []
        for e in edges:
            if e == (eu, ev) or e == (ev, eu):
                continue
            new_edges.append(e)
        
        new_edges.extend([
            (eu, a), (a, b), (b, ev),
            (eu, c), (c, d), (d, ev),
            (a, c), (b, d),
        ])
        
        n += 4
        edges = new_edges
    
    return make_cubic_graph(edges, n)


def build_graph_library() -> List[Tuple[str, Dict, bool]]:
    """Build a library of test graphs: (name, graph, is_planar)."""
    library = []
    
    library.append(("K4 (tetrahedron)", tetrahedron_graph(), True))
    library.append(("Triangular prism", prism_graph(), True))
    library.append(("Cube Q3", cube_graph(), True))
    library.append(("Petersen graph", petersen_graph(), False))
    library.append(("K_{3,3}", k33_graph(), False))
    library.append(("Dodecahedron", dodecahedron_graph(), True))
    
    if HAS_NX:
        G = nx.circular_ladder_graph(4)
        library.append(("Möbius-Kantor ladder C_4×K_2", 
                        make_cubic_graph(list(G.edges()), 8), True))
        
        G = nx.circular_ladder_graph(5)
        library.append(("Prism C_5×K_2",
                        make_cubic_graph(list(G.edges()), 10), True))
        
        G = nx.circular_ladder_graph(6)
        library.append(("Prism C_6×K_2",
                        make_cubic_graph(list(G.edges()), 12), True))
        
        G = nx.circular_ladder_graph(7)
        library.append(("Prism C_7×K_2",
                        make_cubic_graph(list(G.edges()), 14), True))
        
        G = nx.circular_ladder_graph(8)
        library.append(("Prism C_8×K_2",
                        make_cubic_graph(list(G.edges()), 16), True))
        
        G = nx.circular_ladder_graph(9)
        library.append(("Prism C_9×K_2",
                        make_cubic_graph(list(G.edges()), 18), True))
        
        G = nx.circular_ladder_graph(10)
        library.append(("Prism C_10×K_2",
                        make_cubic_graph(list(G.edges()), 20), True))
        
        try:
            G = nx.frucht_graph()
            library.append(("Frucht graph", 
                           make_cubic_graph(list(G.edges()), G.number_of_nodes()), True))
        except:
            pass
        
        try:
            G = nx.tutte_graph()
            library.append(("Tutte graph (46v)",
                           make_cubic_graph(list(G.edges()), G.number_of_nodes()), True))
        except:
            pass
        
        try:
            G = nx.desargues_graph()
            library.append(("Desargues graph",
                           make_cubic_graph(list(G.edges()), G.number_of_nodes()), False))
        except:
            pass
        
        try:
            G = nx.pappus_graph()
            library.append(("Pappus graph",
                           make_cubic_graph(list(G.edges()), G.number_of_nodes()), True))
        except:
            pass
        
        try:
            G = nx.heawood_graph()
            library.append(("Heawood graph",
                           make_cubic_graph(list(G.edges()), G.number_of_nodes()), False))
        except:
            pass

    expanded_8 = generate_cubic_by_expansion(tetrahedron_graph(), 1)
    library.append(("K4-expanded (8v)", expanded_8, True))
    
    expanded_12 = generate_cubic_by_expansion(cube_graph(), 1)
    library.append(("Cube-expanded (12v)", expanded_12, True))

    return library


def verify_cubic(graph: Dict) -> bool:
    """Verify that graph is cubic (every vertex has degree 3)."""
    for v, neighbors in graph['adj'].items():
        if len(neighbors) != 3:
            return False
    return True


def main():
    """Run Penrose evaluation on all test graphs."""
    print("=" * 70)
    print("PENROSE EVALUATION — Tait Colouring Count")
    print("=" * 70)
    
    library = build_graph_library()
    
    results = []
    
    print(f"\n{'Graph':<30} {'V':>4} {'E':>4} {'Cubic':>6} {'Bless':>6} {'Pen(G)':>8} {'Time':>8} {'Planar':>7}")
    print("-" * 85)
    
    for name, graph, expected_planar in library:
        n_v = graph['n']
        n_e = len(graph['edges'])
        cubic = verify_cubic(graph)
        bridgeless = is_bridgeless(graph) if cubic else False
        
        if n_v > 30 and n_e > 45:
            pen = "SKIP"
            elapsed = 0
        else:
            t0 = time.time()
            pen = penrose_eval(graph) if (cubic and bridgeless) else "N/A"
            elapsed = time.time() - t0
        
        status = ""
        if expected_planar and isinstance(pen, int):
            status = "✓" if pen > 0 else "✗ FAIL"
        elif not expected_planar and isinstance(pen, int):
            status = f"(non-planar, Pen={pen})"
        
        print(f"{name:<30} {n_v:>4} {n_e:>4} {'Y' if cubic else 'N':>6} {'Y' if bridgeless else 'N':>6} {str(pen):>8} {elapsed:>7.3f}s {status}")
        
        results.append({
            'name': name,
            'vertices': n_v,
            'edges': n_e,
            'cubic': cubic,
            'bridgeless': bridgeless,
            'planar': expected_planar,
            'penrose': pen,
            'time': elapsed,
        })
    
    print("\n" + "=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    
    planar_results = [r for r in results if r['planar'] and isinstance(r['penrose'], int)]
    nonplanar_results = [r for r in results if not r['planar'] and isinstance(r['penrose'], int)]
    
    print(f"\nPlanar graphs tested: {len(planar_results)}")
    all_positive = all(r['penrose'] > 0 for r in planar_results)
    print(f"All Pen(G) > 0: {'YES ✓' if all_positive else 'NO ✗'}")
    
    if planar_results:
        min_pen = min(r['penrose'] for r in planar_results)
        max_pen = max(r['penrose'] for r in planar_results)
        print(f"Pen(G) range: [{min_pen}, {max_pen}]")
    
    print(f"\nNon-planar graphs tested: {len(nonplanar_results)}")
    for r in nonplanar_results:
        print(f"  {r['name']}: Pen = {r['penrose']}")
    
    petersen_results = [r for r in results if 'Petersen' in r['name']]
    if petersen_results:
        p = petersen_results[0]
        print(f"\nPetersen graph: Pen = {p['penrose']} {'(= 0, as expected ✓)' if p['penrose'] == 0 else '(UNEXPECTED!)'}")
    
    if planar_results:
        print("\nPen(G) vs. vertex count:")
        for r in sorted(planar_results, key=lambda x: x['vertices']):
            ratio = r['penrose'] / r['vertices'] if r['vertices'] > 0 else 0
            print(f"  {r['name']:<30} V={r['vertices']:>3}  Pen={r['penrose']:>6}  Pen/V={ratio:>8.1f}")
    
    return results


if __name__ == "__main__":
    results = main()
    
    output_dir = "/Users/kylemathewson/GraphColour/backgroundMaterial/agent1520/coordinator/manager_M4/sub_S2"
    with open(f"{output_dir}/penrose_raw_results.txt", "w") as f:
        f.write("Penrose Evaluation Results\n")
        f.write("=" * 60 + "\n\n")
        for r in results:
            f.write(f"{r['name']}: V={r['vertices']}, E={r['edges']}, ")
            f.write(f"Planar={r['planar']}, Pen={r['penrose']}\n")
