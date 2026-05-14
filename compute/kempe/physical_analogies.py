"""
Physical Analogies for Kempe Chain Reconfiguration
Author: Agent 1243 (original), Agent 1443-M1-S1 (extended)

This module formalizes the physical analogies derived from the "Fever Dream" and
subsequent skeptical review. It defines computational energy functionals and
metrics that map the discrete Kempe swap graph into continuous physical models.

Models included:
1. Magic Gem Covariance (Polyhedral embedding)  [BUGFIXED: includes vertex color]
2. Anti-Ferromagnetic Potts Model (Spin Glass)
3. Electrostatic Charge Flow
4. Protein Folding Funnel (Rugged Landscape)
5. Surface Tension (chain boundary cost)
6. Local Entropy (neighbor color disorder)
7. Defect Interaction (color-5 pairwise coupling)
8. Electric Field Gradient (potential difference)

NetworkX wrappers (_nx suffix) provided for codebase integration.
"""

import math
import numpy as np
from typing import Dict, List, Tuple, Set, Optional
from collections import Counter, deque

# =====================================================================
# 1. Magic Gem Covariance Energy
# =====================================================================

TETRAHEDRON_COORDS = {
    1: np.array([1.0, 1.0, 1.0]),
    2: np.array([1.0, -1.0, -1.0]),
    3: np.array([-1.0, 1.0, -1.0]),
    4: np.array([-1.0, -1.0, 1.0]),
    5: np.array([0.0, 0.0, 0.0])
}


def compute_local_magic_gem_energy(graph_adj: Dict[int, List[int]],
                                    coloring: Dict[int, int],
                                    vertex: int) -> float:
    """
    Local frustration of a vertex in the Magic Gem embedding.

    The center-of-mass includes the vertex's OWN color vector plus all
    neighbor color vectors.  Energy = ||center_of_mass||^2.
    A perfectly balanced 4-coloring neighborhood yields zero energy.

    BUGFIX (Agent 1443): previous version excluded the vertex itself from
    the center-of-mass, understating frustration for color-5 vertices.
    """
    neighbors = graph_adj[vertex]
    points = [TETRAHEDRON_COORDS[coloring[vertex]]]
    for n in neighbors:
        points.append(TETRAHEDRON_COORDS[coloring[n]])

    if not points:
        return 0.0

    center_of_mass = np.mean(points, axis=0)
    return float(np.sum(center_of_mass ** 2))


def compute_global_magic_gem_energy(graph_adj: Dict[int, List[int]],
                                     coloring: Dict[int, int]) -> float:
    """Sum of local Magic Gem energies across the entire graph."""
    return sum(compute_local_magic_gem_energy(graph_adj, coloring, v)
               for v in graph_adj)


# =====================================================================
# 2. Anti-Ferromagnetic Potts Model
# =====================================================================

def compute_potts_energy(graph_adj: Dict[int, List[int]],
                          coloring: Dict[int, int],
                          J: float = 1.0,
                          h_defect: float = 10.0) -> float:
    """
    Anti-Ferromagnetic Potts Hamiltonian with defect field.

    H = J * sum_{(i,j)} delta(c_i, c_j) + h * sum_i delta(c_i, 5)

    For proper colorings the Potts coupling is zero; the energy comes
    entirely from the defect-field penalty on color-5 vertices.
    """
    energy = 0.0
    for v, c in coloring.items():
        if c == 5:
            energy += h_defect
    for v in graph_adj:
        for u in graph_adj[v]:
            if u > v and coloring[u] == coloring[v]:
                energy += J
    return energy


# =====================================================================
# 3. Electrostatic Charge Flow
# =====================================================================

def compute_electrostatic_potential(graph_adj: Dict[int, List[int]],
                                     coloring: Dict[int, int]) -> Dict[int, float]:
    """
    Treat color-5 vertices as +1 charge; solve discrete Poisson L*V = rho
    via pseudoinverse of the graph Laplacian.
    """
    n_vertices = len(graph_adj)
    if n_vertices == 0:
        return {}

    nodes = sorted(list(graph_adj.keys()))
    node_to_idx = {n: i for i, n in enumerate(nodes)}

    L = np.zeros((n_vertices, n_vertices))
    for i, u in enumerate(nodes):
        neighbors = graph_adj[u]
        L[i, i] = len(neighbors)
        for v in neighbors:
            L[i, node_to_idx[v]] = -1.0

    rho = np.zeros(n_vertices)
    for i, u in enumerate(nodes):
        if coloring[u] == 5:
            rho[i] = 1.0

    V = np.linalg.pinv(L).dot(rho)
    return {nodes[i]: float(V[i]) for i in range(n_vertices)}


# =====================================================================
# 4. Protein Folding Funnel / Rugged Landscape
# =====================================================================

def compute_ruggedness_metric(kempe_chain: Set[int],
                               graph_adj: Dict[int, List[int]]) -> float:
    """
    Surface-to-volume ratio of a Kempe chain: number of edges leaving the
    chain divided by chain size.  High ratio = high activation energy.
    """
    if len(kempe_chain) == 0:
        return 0.0
    surface_edges = 0
    for u in kempe_chain:
        for v in graph_adj[u]:
            if v not in kempe_chain:
                surface_edges += 1
    return surface_edges / len(kempe_chain)


# =====================================================================
# 5. Surface Tension (NEW — Agent 1443)
# =====================================================================

def compute_surface_tension(graph_adj: Dict[int, List[int]],
                             coloring: Dict[int, int],
                             kempe_chain: Set[int],
                             color_a: int,
                             color_b: int) -> float:
    """
    Count boundary edges between the (color_a, color_b)-Kempe chain and
    vertices colored with OTHER colors (not a or b).

    This measures how embedded the chain is in a foreign-color region.
    Higher tension = more topological resistance to swapping.
    """
    boundary_edges = 0
    for u in kempe_chain:
        for v in graph_adj[u]:
            if v not in kempe_chain and coloring[v] not in (color_a, color_b):
                boundary_edges += 1
    return float(boundary_edges)


# =====================================================================
# 6. Local Entropy (NEW — Agent 1443)
# =====================================================================

def compute_local_entropy(graph_adj: Dict[int, List[int]],
                           coloring: Dict[int, int],
                           vertex: int) -> float:
    """
    Shannon entropy of the color distribution among neighbors of vertex.

    H = -sum_c p(c) * log2(p(c))

    High entropy = diverse neighborhood (many colors equally represented).
    Low entropy = homogeneous neighborhood (dominated by one color).
    """
    neighbors = graph_adj[vertex]
    if not neighbors:
        return 0.0

    counts = Counter(coloring[n] for n in neighbors)
    total = sum(counts.values())

    entropy = 0.0
    for count in counts.values():
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)
    return entropy


# =====================================================================
# 7. Defect Interaction (NEW — Agent 1443)
# =====================================================================

def _bfs_distance(graph_adj: Dict[int, List[int]],
                   source: int, target: int) -> int:
    """BFS shortest path distance; returns -1 if unreachable."""
    if source == target:
        return 0
    visited = {source}
    queue = deque([(source, 0)])
    while queue:
        v, d = queue.popleft()
        for u in graph_adj[v]:
            if u == target:
                return d + 1
            if u not in visited:
                visited.add(u)
                queue.append((u, d + 1))
    return -1


def compute_defect_interaction(graph_adj: Dict[int, List[int]],
                                coloring: Dict[int, int],
                                decay_rate: float = 1.0) -> float:
    """
    Pairwise interaction energy between color-5 vertices.

    E = sum_{i<j, c(i)=c(j)=5} exp(-decay_rate * d(i,j))

    where d(i,j) is the BFS shortest-path distance.  Nearby defects
    interact strongly; distant defects are decoupled.  High energy
    signals defect clustering.
    """
    defects = [v for v, c in coloring.items() if c == 5]
    if len(defects) < 2:
        return 0.0

    energy = 0.0
    for i in range(len(defects)):
        for j in range(i + 1, len(defects)):
            d = _bfs_distance(graph_adj, defects[i], defects[j])
            if d > 0:
                energy += math.exp(-decay_rate * d)
    return energy


# =====================================================================
# 8. Electric Field Gradient (NEW — Agent 1443)
# =====================================================================

def compute_electric_field_gradient(graph_adj: Dict[int, List[int]],
                                     coloring: Dict[int, int],
                                     vertex: int,
                                     potential: Optional[Dict[int, float]] = None) -> float:
    """
    Maximum electrostatic potential difference between vertex and its
    neighbors: max_{u ~ v} |V(v) - V(u)|.

    If potential is not provided, it is computed from scratch.
    This measures the local "electric field strength" — high gradient
    means the defect charge is under strong pressure to move.
    """
    if potential is None:
        potential = compute_electrostatic_potential(graph_adj, coloring)

    neighbors = graph_adj[vertex]
    if not neighbors:
        return 0.0

    v_pot = potential.get(vertex, 0.0)
    max_diff = 0.0
    for u in neighbors:
        diff = abs(v_pot - potential.get(u, 0.0))
        if diff > max_diff:
            max_diff = diff
    return max_diff


# =====================================================================
# NetworkX Compatibility Wrappers (_nx suffix)
# =====================================================================

def _nx_to_adj(G) -> Dict[int, List[int]]:
    """Convert nx.Graph to adjacency dict used internally."""
    return {v: list(G.neighbors(v)) for v in G.nodes()}


def compute_local_magic_gem_energy_nx(G, coloring: Dict[int, int],
                                       vertex: int) -> float:
    """NetworkX wrapper for compute_local_magic_gem_energy."""
    return compute_local_magic_gem_energy(_nx_to_adj(G), coloring, vertex)


def compute_global_magic_gem_energy_nx(G, coloring: Dict[int, int]) -> float:
    """NetworkX wrapper for compute_global_magic_gem_energy."""
    return compute_global_magic_gem_energy(_nx_to_adj(G), coloring)


def compute_potts_energy_nx(G, coloring: Dict[int, int],
                             J: float = 1.0,
                             h_defect: float = 10.0) -> float:
    """NetworkX wrapper for compute_potts_energy."""
    return compute_potts_energy(_nx_to_adj(G), coloring, J, h_defect)


def compute_electrostatic_potential_nx(G, coloring: Dict[int, int]) -> Dict[int, float]:
    """NetworkX wrapper for compute_electrostatic_potential."""
    return compute_electrostatic_potential(_nx_to_adj(G), coloring)


def compute_ruggedness_metric_nx(G, kempe_chain: Set[int]) -> float:
    """NetworkX wrapper for compute_ruggedness_metric."""
    return compute_ruggedness_metric(kempe_chain, _nx_to_adj(G))


def compute_surface_tension_nx(G, coloring: Dict[int, int],
                                kempe_chain: Set[int],
                                color_a: int, color_b: int) -> float:
    """NetworkX wrapper for compute_surface_tension."""
    return compute_surface_tension(_nx_to_adj(G), coloring, kempe_chain,
                                   color_a, color_b)


def compute_local_entropy_nx(G, coloring: Dict[int, int],
                              vertex: int) -> float:
    """NetworkX wrapper for compute_local_entropy."""
    return compute_local_entropy(_nx_to_adj(G), coloring, vertex)


def compute_defect_interaction_nx(G, coloring: Dict[int, int],
                                   decay_rate: float = 1.0) -> float:
    """NetworkX wrapper for compute_defect_interaction."""
    return compute_defect_interaction(_nx_to_adj(G), coloring, decay_rate)


def compute_electric_field_gradient_nx(G, coloring: Dict[int, int],
                                        vertex: int,
                                        potential: Optional[Dict[int, float]] = None) -> float:
    """NetworkX wrapper for compute_electric_field_gradient."""
    return compute_electric_field_gradient(_nx_to_adj(G), coloring, vertex, potential)


# =====================================================================
# Main Execution / Demo
# =====================================================================

if __name__ == "__main__":
    adj = {
        0: [1, 2, 3, 4],
        1: [0, 2, 4],
        2: [0, 1, 3],
        3: [0, 2, 4],
        4: [0, 1, 3]
    }

    col = {
        0: 5,
        1: 1,
        2: 2,
        3: 3,
        4: 4
    }

    print("--- Physical Analogy Metrics (Agent 1443 extended) ---")
    print(f"Global Magic Gem Energy: {compute_global_magic_gem_energy(adj, col):.4f}")

    potentials = compute_electrostatic_potential(adj, col)
    print(f"Electrostatic Potential at defect (node 0): {potentials[0]:.4f}")
    print(f"Electrostatic Potential at boundary (node 1): {potentials[1]:.4f}")

    chain = {0, 1}
    print(f"Ruggedness of {{0,1}} chain: {compute_ruggedness_metric(chain, adj):.4f}")
    print(f"Surface Tension of {{0,1}} (1,5)-chain: {compute_surface_tension(adj, col, chain, 1, 5):.4f}")

    print(f"\nLocal Entropy at node 0: {compute_local_entropy(adj, col, 0):.4f}")
    print(f"Local Entropy at node 1: {compute_local_entropy(adj, col, 1):.4f}")

    print(f"\nDefect Interaction Energy: {compute_defect_interaction(adj, col):.4f}")

    print(f"\nElectric Field Gradient at node 0: {compute_electric_field_gradient(adj, col, 0, potentials):.4f}")
    print(f"Electric Field Gradient at node 1: {compute_electric_field_gradient(adj, col, 1, potentials):.4f}")

    print(f"\nPotts Energy: {compute_potts_energy(adj, col):.4f}")
