"""
Unit tests for physical_analogies.py — Agent 1443-M1-S2

Tests every energy functional on K4 and octahedron graphs.
Validates known mathematical properties and edge cases.
"""

import sys
import os
import math
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import networkx as nx
import numpy as np
from physical_analogies import (
    TETRAHEDRON_COORDS,
    compute_local_magic_gem_energy,
    compute_global_magic_gem_energy,
    compute_potts_energy,
    compute_electrostatic_potential,
    compute_ruggedness_metric,
    compute_surface_tension,
    compute_local_entropy,
    compute_defect_interaction,
    compute_electric_field_gradient,
    _bfs_distance,
    _nx_to_adj,
    compute_local_magic_gem_energy_nx,
    compute_global_magic_gem_energy_nx,
    compute_potts_energy_nx,
    compute_electrostatic_potential_nx,
    compute_ruggedness_metric_nx,
    compute_surface_tension_nx,
    compute_local_entropy_nx,
    compute_defect_interaction_nx,
    compute_electric_field_gradient_nx,
)


def make_K4_adj():
    """K4 as adjacency dict with a proper 4-coloring."""
    adj = {0: [1, 2, 3], 1: [0, 2, 3], 2: [0, 1, 3], 3: [0, 1, 2]}
    col_4 = {0: 1, 1: 2, 2: 3, 3: 4}
    return adj, col_4


def make_K4_nx():
    G = nx.complete_graph(4)
    col = {0: 1, 1: 2, 2: 3, 3: 4}
    return G, col


def make_octahedron_adj():
    """Octahedron (K_{2,2,2}) adjacency dict with verified proper 4-coloring.
    Independent sets: {0,5}, {1,4}, {2,3}."""
    G = nx.octahedral_graph()
    adj = {v: list(G.neighbors(v)) for v in G.nodes()}
    col_4 = {0: 1, 1: 2, 2: 3, 3: 3, 4: 2, 5: 4}
    return adj, col_4, G


def make_octahedron_with_defect():
    """Octahedron with vertex 0 as color-5 defect (proper coloring)."""
    G = nx.octahedral_graph()
    adj = {v: list(G.neighbors(v)) for v in G.nodes()}
    col_5 = {0: 5, 1: 2, 2: 3, 3: 3, 4: 2, 5: 4}
    return adj, col_5, G


class TestMagicGemEnergy(unittest.TestCase):

    def test_k4_perfect_coloring_includes_vertex(self):
        """On K4 with proper 4-coloring, center-of-mass includes vertex itself."""
        adj, col = make_K4_adj()
        energy = compute_local_magic_gem_energy(adj, col, 0)
        coords = [TETRAHEDRON_COORDS[col[v]] for v in [0, 1, 2, 3]]
        com = np.mean(coords, axis=0)
        expected = float(np.sum(com ** 2))
        self.assertAlmostEqual(energy, expected, places=10)

    def test_k4_all_four_colors_center_near_zero(self):
        """K4 with {1,2,3,4}: the 4 tetrahedron vertices average to origin."""
        adj, col = make_K4_adj()
        all_coords = [TETRAHEDRON_COORDS[c] for c in [1, 2, 3, 4]]
        com = np.mean(all_coords, axis=0)
        np.testing.assert_array_almost_equal(com, [0, 0, 0])
        e_global = compute_global_magic_gem_energy(adj, col)
        self.assertAlmostEqual(e_global, 0.0, places=10)

    def test_bugfix_vertex_included(self):
        """Verify the bug fix: vertex 0's own color is in center-of-mass.
        With a single defect among balanced neighbors, energy should be nonzero."""
        adj = {0: [1, 2, 3], 1: [0, 2, 3], 2: [0, 1, 3], 3: [0, 1, 2]}
        col = {0: 5, 1: 2, 2: 3, 3: 4}
        energy = compute_local_magic_gem_energy(adj, col, 0)
        self.assertGreater(energy, 0.0, "Color-5 vertex should have nonzero local energy")

    def test_octahedron_pure_4coloring(self):
        adj, col, _ = make_octahedron_adj()
        is_proper = all(col[u] != col[v] for u in adj for v in adj[u])
        self.assertTrue(is_proper)
        e = compute_global_magic_gem_energy(adj, col)
        self.assertIsInstance(e, float)

    def test_octahedron_defect_higher_energy(self):
        adj_pure, col_pure, _ = make_octahedron_adj()
        adj_def, col_def, _ = make_octahedron_with_defect()
        e_pure = compute_global_magic_gem_energy(adj_pure, col_pure)
        e_def = compute_global_magic_gem_energy(adj_def, col_def)
        self.assertGreater(e_def, e_pure,
                           "Defect coloring should have higher global energy")


class TestPottsEnergy(unittest.TestCase):

    def test_k4_proper_coloring_no_clash(self):
        adj, col = make_K4_adj()
        e = compute_potts_energy(adj, col)
        self.assertAlmostEqual(e, 0.0)

    def test_defect_penalty(self):
        adj, col, _ = make_octahedron_with_defect()
        e = compute_potts_energy(adj, col, h_defect=10.0)
        self.assertAlmostEqual(e, 10.0)  # 1 defect, no same-color clashes

    def test_two_defects(self):
        adj, col = make_K4_adj()
        col[0] = 5
        col[1] = 5
        e = compute_potts_energy(adj, col, h_defect=7.0, J=1.0)
        # 2 defects (14.0) + 1 same-color edge clash 0-1 (1.0) = 15.0
        self.assertAlmostEqual(e, 15.0)


class TestElectrostaticPotential(unittest.TestCase):

    def test_no_defects_zero_potential(self):
        adj, col = make_K4_adj()
        pot = compute_electrostatic_potential(adj, col)
        for v, p in pot.items():
            self.assertAlmostEqual(p, 0.0, places=10)

    def test_single_defect_positive(self):
        adj, col, _ = make_octahedron_with_defect()
        pot = compute_electrostatic_potential(adj, col)
        self.assertGreater(pot[0], 0.0, "Defect vertex should have highest potential")

    def test_empty_graph(self):
        pot = compute_electrostatic_potential({}, {})
        self.assertEqual(pot, {})

    def test_octahedron_defect_highest_at_source(self):
        adj, col, _ = make_octahedron_with_defect()
        pot = compute_electrostatic_potential(adj, col)
        self.assertEqual(max(pot, key=pot.get), 0)


class TestRuggednessMetric(unittest.TestCase):

    def test_empty_chain(self):
        adj, col = make_K4_adj()
        self.assertAlmostEqual(compute_ruggedness_metric(set(), adj), 0.0)

    def test_single_vertex_chain(self):
        adj, col = make_K4_adj()
        r = compute_ruggedness_metric({0}, adj)
        self.assertAlmostEqual(r, 3.0)  # 3 edges out / 1 vertex

    def test_full_graph_chain(self):
        adj, col = make_K4_adj()
        r = compute_ruggedness_metric({0, 1, 2, 3}, adj)
        self.assertAlmostEqual(r, 0.0)  # no outgoing edges


class TestSurfaceTension(unittest.TestCase):

    def test_chain_inside_matching_colors(self):
        adj = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
        col = {0: 1, 1: 5, 2: 1}
        chain = {0, 2}  # both color 1
        tension = compute_surface_tension(adj, col, chain, 1, 5)
        self.assertAlmostEqual(tension, 0.0)

    def test_chain_with_foreign_boundary(self):
        adj, col, _ = make_octahedron_with_defect()
        chain = {0, 1}
        tension = compute_surface_tension(adj, col, chain, 5, 2)
        self.assertGreater(tension, 0.0)

    def test_k4_single_vertex_chain(self):
        adj, col = make_K4_adj()
        col[0] = 5
        chain = {0}
        tension = compute_surface_tension(adj, col, chain, 1, 5)
        self.assertEqual(tension, 3.0)


class TestLocalEntropy(unittest.TestCase):

    def test_uniform_neighbors(self):
        """All neighbors same color → entropy = 0."""
        adj = {0: [1, 2, 3], 1: [0], 2: [0], 3: [0]}
        col = {0: 1, 1: 2, 2: 2, 3: 2}
        self.assertAlmostEqual(compute_local_entropy(adj, col, 0), 0.0)

    def test_all_different_neighbors(self):
        """All neighbors different colors → maximum entropy."""
        adj = {0: [1, 2, 3, 4], 1: [0], 2: [0], 3: [0], 4: [0]}
        col = {0: 5, 1: 1, 2: 2, 3: 3, 4: 4}
        e = compute_local_entropy(adj, col, 0)
        self.assertAlmostEqual(e, 2.0)  # log2(4) = 2.0

    def test_no_neighbors(self):
        adj = {0: []}
        col = {0: 1}
        self.assertAlmostEqual(compute_local_entropy(adj, col, 0), 0.0)

    def test_octahedron_entropy(self):
        adj, col, _ = make_octahedron_adj()
        e = compute_local_entropy(adj, col, 0)
        self.assertGreater(e, 0.0)


class TestDefectInteraction(unittest.TestCase):

    def test_no_defects(self):
        adj, col = make_K4_adj()
        self.assertAlmostEqual(compute_defect_interaction(adj, col), 0.0)

    def test_single_defect(self):
        adj, col = make_K4_adj()
        col[0] = 5
        self.assertAlmostEqual(compute_defect_interaction(adj, col), 0.0)

    def test_adjacent_defects(self):
        adj, col = make_K4_adj()
        col[0] = 5
        col[1] = 5
        e = compute_defect_interaction(adj, col, decay_rate=1.0)
        self.assertAlmostEqual(e, math.exp(-1.0))

    def test_two_defects_distance_2(self):
        adj = {0: [1], 1: [0, 2], 2: [1]}
        col = {0: 5, 1: 1, 2: 5}
        e = compute_defect_interaction(adj, col, decay_rate=1.0)
        self.assertAlmostEqual(e, math.exp(-2.0))


class TestElectricFieldGradient(unittest.TestCase):

    def test_uniform_potential_zero_gradient(self):
        adj, col = make_K4_adj()
        pot = compute_electrostatic_potential(adj, col)
        for v in adj:
            grad = compute_electric_field_gradient(adj, col, v, pot)
            self.assertAlmostEqual(grad, 0.0, places=10)

    def test_defect_has_gradient(self):
        adj, col, _ = make_octahedron_with_defect()
        pot = compute_electrostatic_potential(adj, col)
        grad = compute_electric_field_gradient(adj, col, 0, pot)
        self.assertGreater(grad, 0.0)

    def test_no_neighbors(self):
        adj = {0: []}
        col = {0: 5}
        pot = {0: 1.0}
        self.assertAlmostEqual(compute_electric_field_gradient(adj, col, 0, pot), 0.0)


class TestBFSDistance(unittest.TestCase):

    def test_same_vertex(self):
        adj, _ = make_K4_adj()
        self.assertEqual(_bfs_distance(adj, 0, 0), 0)

    def test_adjacent(self):
        adj, _ = make_K4_adj()
        self.assertEqual(_bfs_distance(adj, 0, 1), 1)

    def test_path_graph(self):
        adj = {0: [1], 1: [0, 2], 2: [1, 3], 3: [2]}
        self.assertEqual(_bfs_distance(adj, 0, 3), 3)


class TestNetworkXWrappers(unittest.TestCase):

    def test_nx_to_adj(self):
        G = nx.complete_graph(4)
        adj = _nx_to_adj(G)
        for v in G.nodes():
            self.assertEqual(set(adj[v]), set(G.neighbors(v)))

    def test_magic_gem_nx_matches(self):
        G, col = make_K4_nx()
        adj = _nx_to_adj(G)
        for v in G.nodes():
            e_raw = compute_local_magic_gem_energy(adj, col, v)
            e_nx = compute_local_magic_gem_energy_nx(G, col, v)
            self.assertAlmostEqual(e_raw, e_nx)

    def test_global_magic_gem_nx(self):
        G, col = make_K4_nx()
        adj = _nx_to_adj(G)
        self.assertAlmostEqual(
            compute_global_magic_gem_energy(adj, col),
            compute_global_magic_gem_energy_nx(G, col))

    def test_potts_nx(self):
        G, col = make_K4_nx()
        adj = _nx_to_adj(G)
        self.assertAlmostEqual(
            compute_potts_energy(adj, col),
            compute_potts_energy_nx(G, col))

    def test_electrostatic_nx(self):
        G, col = make_K4_nx()
        adj = _nx_to_adj(G)
        p1 = compute_electrostatic_potential(adj, col)
        p2 = compute_electrostatic_potential_nx(G, col)
        for v in p1:
            self.assertAlmostEqual(p1[v], p2[v])

    def test_ruggedness_nx(self):
        G = nx.complete_graph(4)
        adj = _nx_to_adj(G)
        chain = {0, 1}
        self.assertAlmostEqual(
            compute_ruggedness_metric(chain, adj),
            compute_ruggedness_metric_nx(G, chain))

    def test_surface_tension_nx(self):
        G = nx.complete_graph(4)
        col = {0: 5, 1: 1, 2: 2, 3: 3}
        adj = _nx_to_adj(G)
        chain = {0, 1}
        self.assertAlmostEqual(
            compute_surface_tension(adj, col, chain, 1, 5),
            compute_surface_tension_nx(G, col, chain, 1, 5))

    def test_entropy_nx(self):
        G, col = make_K4_nx()
        adj = _nx_to_adj(G)
        for v in G.nodes():
            self.assertAlmostEqual(
                compute_local_entropy(adj, col, v),
                compute_local_entropy_nx(G, col, v))

    def test_defect_interaction_nx(self):
        G = nx.complete_graph(4)
        col = {0: 5, 1: 5, 2: 3, 3: 4}
        adj = _nx_to_adj(G)
        self.assertAlmostEqual(
            compute_defect_interaction(adj, col),
            compute_defect_interaction_nx(G, col))

    def test_gradient_nx(self):
        G = nx.complete_graph(4)
        col = {0: 5, 1: 1, 2: 2, 3: 3}
        adj = _nx_to_adj(G)
        pot = compute_electrostatic_potential(adj, col)
        for v in G.nodes():
            self.assertAlmostEqual(
                compute_electric_field_gradient(adj, col, v, pot),
                compute_electric_field_gradient_nx(G, col, v, pot))


if __name__ == '__main__':
    unittest.main()
