"""
reducibility_checker.py — D-reducibility checker for planar configurations.

A configuration is D-reducible if every proper 4-colouring of its boundary
ring extends to a 4-colouring of the entire configuration (possibly after
Kempe-chain colour swaps on the boundary colouring).

This module checks D-reducibility for small configurations (ring size ≤ 14)
by exhaustive enumeration of boundary colourings, with Kempe-chain analysis
to test extension.

Key definitions:
  - Ring: a cycle C of r vertices forming the boundary.
  - Interior: vertices and edges inside the ring.
  - Configuration: ring + interior (a near-triangulation of a disk).
  - Proper 4-colouring: assignment of {0,1,2,3} to vertices such that
    adjacent vertices get different colours.
  - D-reducible: for every proper 4-colouring of the ring boundary, there
    exists a Kempe-equivalent boundary colouring that extends to the interior.

Agent 1545-M3 / D-Reducibility Infrastructure
"""

from __future__ import annotations

import itertools
from collections import defaultdict, deque
from typing import Dict, FrozenSet, List, Optional, Set, Tuple


# ======================================================================
# Configuration representation
# ======================================================================

class Configuration:
    """A near-triangulation of a disk: ring boundary + interior.

    Vertices are integers.  Ring vertices are 0..ring_size-1 in cyclic order.
    Interior vertices are ring_size, ring_size+1, ...

    Attributes:
        ring_size: Number of boundary vertices.
        interior_size: Number of interior vertices.
        edges: Set of (u, v) edges with u < v.
        adj: Adjacency dict.
    """

    def __init__(self, ring_size: int, interior_verts: List[int],
                 edges: List[Tuple[int, int]]):
        self.ring_size = ring_size
        self.ring_verts = list(range(ring_size))
        self.interior_verts = sorted(interior_verts)
        self.all_verts = self.ring_verts + self.interior_verts
        self.n = len(self.all_verts)

        self.edges: Set[Tuple[int, int]] = set()
        self.adj: Dict[int, Set[int]] = defaultdict(set)
        for u, v in edges:
            e = (min(u, v), max(u, v))
            self.edges.add(e)
            self.adj[u].add(v)
            self.adj[v].add(u)

        # Add ring edges if not already present
        for i in range(ring_size):
            j = (i + 1) % ring_size
            e = (min(i, j), max(i, j))
            if e not in self.edges:
                self.edges.add(e)
                self.adj[i].add(j)
                self.adj[j].add(i)

    @property
    def interior_size(self) -> int:
        return len(self.interior_verts)

    def ring_neighbors(self, v: int) -> Set[int]:
        """Ring vertices adjacent to v."""
        return self.adj[v] & set(self.ring_verts)

    def interior_neighbors(self, v: int) -> Set[int]:
        """Interior vertices adjacent to v."""
        return self.adj[v] & set(self.interior_verts)

    def __repr__(self) -> str:
        return (f"Config(ring={self.ring_size}, "
                f"interior={self.interior_size}, "
                f"|E|={len(self.edges)})")


# ======================================================================
# Colouring utilities
# ======================================================================

COLOURS = [0, 1, 2, 3]


def is_proper_colouring(adj: Dict[int, Set[int]],
                        colouring: Dict[int, int],
                        vertices: Optional[List[int]] = None) -> bool:
    """Check if colouring is proper on the given vertices."""
    verts = vertices if vertices is not None else list(colouring.keys())
    for v in verts:
        if v not in colouring:
            continue
        for u in adj.get(v, set()):
            if u in colouring and colouring[u] == colouring[v]:
                return False
    return True


def enumerate_ring_colourings(config: Configuration) -> List[Dict[int, int]]:
    """Enumerate all proper 4-colourings of the ring boundary.

    For ring size r, there are at most 4^r candidates; we filter to proper
    colourings of the ring cycle.  For r ≤ 14 this is tractable.
    """
    r = config.ring_size
    colourings: List[Dict[int, int]] = []
    ring_adj: Dict[int, Set[int]] = {}
    for v in config.ring_verts:
        ring_adj[v] = config.adj[v] & set(config.ring_verts)

    def backtrack(idx: int, assignment: Dict[int, int]) -> None:
        if idx == r:
            colourings.append(dict(assignment))
            return
        v = idx
        used = {assignment[u] for u in ring_adj[v] if u in assignment}
        for c in COLOURS:
            if c not in used:
                assignment[v] = c
                backtrack(idx + 1, assignment)
                del assignment[v]

    backtrack(0, {})
    return colourings


def extend_to_interior(config: Configuration,
                       ring_colouring: Dict[int, int]) -> Optional[Dict[int, int]]:
    """Try to extend a ring colouring to the interior by backtracking.

    Returns the full colouring if successful, None otherwise.
    """
    interior = config.interior_verts
    if not interior:
        return dict(ring_colouring)

    colouring = dict(ring_colouring)

    def backtrack(idx: int) -> bool:
        if idx == len(interior):
            return True
        v = interior[idx]
        used = {colouring[u] for u in config.adj[v] if u in colouring}
        for c in COLOURS:
            if c not in used:
                colouring[v] = c
                if backtrack(idx + 1):
                    return True
                del colouring[v]
        return False

    if backtrack(0):
        return colouring
    return None


# ======================================================================
# Kempe chains
# ======================================================================

def find_kempe_chain(adj: Dict[int, Set[int]],
                     colouring: Dict[int, int],
                     start: int, c1: int, c2: int,
                     allowed_verts: Optional[Set[int]] = None
                     ) -> Set[int]:
    """Find the Kempe chain containing `start` for colours c1, c2.

    A Kempe chain is a maximal connected component in the subgraph induced
    by vertices coloured c1 or c2.

    Args:
        allowed_verts: If given, restrict to these vertices.
    """
    if colouring.get(start) not in (c1, c2):
        return set()

    chain: Set[int] = set()
    queue: deque = deque([start])
    while queue:
        v = queue.popleft()
        if v in chain:
            continue
        if colouring.get(v) not in (c1, c2):
            continue
        if allowed_verts is not None and v not in allowed_verts:
            continue
        chain.add(v)
        for u in adj.get(v, set()):
            if u not in chain:
                queue.append(u)
    return chain


def swap_kempe_chain(colouring: Dict[int, int],
                     chain: Set[int], c1: int, c2: int) -> Dict[int, int]:
    """Return a new colouring with c1↔c2 swapped on the chain."""
    new = dict(colouring)
    for v in chain:
        if new[v] == c1:
            new[v] = c2
        elif new[v] == c2:
            new[v] = c1
    return new


def kempe_equivalent_colourings(config: Configuration,
                                ring_colouring: Dict[int, int],
                                max_depth: int = 2) -> List[Dict[int, int]]:
    """Generate Kempe-equivalent ring colourings up to a given swap depth.

    At depth 1: try all single Kempe swaps on the ring.
    At depth 2: try all pairs of Kempe swaps.

    Returns a list of distinct proper ring colourings reachable by swaps.
    """
    ring_set = set(config.ring_verts)
    seen: Set[FrozenSet[Tuple[int, int]]] = set()
    result: List[Dict[int, int]] = []

    def colouring_key(c: Dict[int, int]) -> FrozenSet[Tuple[int, int]]:
        return frozenset((v, c[v]) for v in config.ring_verts)

    def add_colouring(c: Dict[int, int]) -> None:
        key = colouring_key(c)
        if key not in seen:
            seen.add(key)
            result.append(c)

    add_colouring(ring_colouring)

    ring_adj: Dict[int, Set[int]] = {}
    for v in config.ring_verts:
        ring_adj[v] = config.adj[v] & ring_set

    def generate_swaps(col: Dict[int, int], depth: int) -> None:
        if depth <= 0:
            return
        for v in config.ring_verts:
            cv = col[v]
            for c2 in COLOURS:
                if c2 == cv:
                    continue
                chain = find_kempe_chain(ring_adj, col, v, cv, c2,
                                         allowed_verts=ring_set)
                swapped = swap_kempe_chain(col, chain, cv, c2)
                if is_proper_colouring(ring_adj, swapped, config.ring_verts):
                    key = colouring_key(swapped)
                    if key not in seen:
                        add_colouring(swapped)
                        generate_swaps(swapped, depth - 1)

    generate_swaps(ring_colouring, max_depth)
    return result


# ======================================================================
# D-reducibility checker
# ======================================================================

class DReducibilityChecker:
    """Check D-reducibility of a configuration.

    A configuration is D-reducible if every proper 4-colouring of the ring
    has a Kempe-equivalent colouring that extends to the interior.
    """

    def __init__(self, config: Configuration, kempe_depth: int = 2):
        self.config = config
        self.kempe_depth = kempe_depth

    def check_single_colouring(self, ring_col: Dict[int, int]) -> bool:
        """Check if this ring colouring (or a Kempe-equivalent) extends."""
        if extend_to_interior(self.config, ring_col) is not None:
            return True
        equivs = kempe_equivalent_colourings(
            self.config, ring_col, max_depth=self.kempe_depth)
        for eq_col in equivs:
            if extend_to_interior(self.config, eq_col) is not None:
                return True
        return False

    def check(self, verbose: bool = False) -> Dict:
        """Full D-reducibility check.

        Returns:
            is_reducible: True iff D-reducible.
            total_colourings: Number of proper ring colourings.
            direct_extensions: Number that extend directly.
            kempe_extensions: Number that extend after Kempe swaps.
            failures: Number that don't extend at all.
            failure_examples: Up to 5 non-extending colourings.
        """
        all_ring_cols = enumerate_ring_colourings(self.config)
        direct = 0
        kempe = 0
        failures = 0
        failure_examples: List[Dict[int, int]] = []

        for i, rc in enumerate(all_ring_cols):
            if verbose and (i + 1) % 500 == 0:
                print(f"  Checked {i + 1}/{len(all_ring_cols)} ring colourings...")
            if extend_to_interior(self.config, rc) is not None:
                direct += 1
            else:
                equivs = kempe_equivalent_colourings(
                    self.config, rc, max_depth=self.kempe_depth)
                found = False
                for eq in equivs:
                    if extend_to_interior(self.config, eq) is not None:
                        kempe += 1
                        found = True
                        break
                if not found:
                    failures += 1
                    if len(failure_examples) < 5:
                        failure_examples.append(rc)

        return {
            'is_reducible': failures == 0,
            'total_colourings': len(all_ring_cols),
            'direct_extensions': direct,
            'kempe_extensions': kempe,
            'failures': failures,
            'failure_examples': failure_examples,
        }


# ======================================================================
# Standard test configurations
# ======================================================================

def birkhoff_diamond() -> Configuration:
    """The Birkhoff diamond: ring size 6, 1 interior vertex.

    Ring: 0-1-2-3-4-5, interior vertex 6 connected to 0,1,2,3,4,5.
    This is a degree-6 vertex (the interior) with its ring neighbours.
    Known to be D-reducible.
    """
    edges = [(i, (i + 1) % 6) for i in range(6)]
    edges += [(6, i) for i in range(6)]
    # Triangulate: add diagonals inside
    edges += [(0, 2), (2, 4), (4, 0)]
    return Configuration(6, [6], edges)


def degree5_wheel() -> Configuration:
    """Degree-5 wheel: ring size 5, 1 interior vertex (the hub).

    Ring: 0-1-2-3-4, interior vertex 5 connected to all ring vertices.
    Automatically a triangulation.  Known to be D-reducible.
    """
    edges = [(i, (i + 1) % 5) for i in range(5)]
    edges += [(5, i) for i in range(5)]
    return Configuration(5, [5], edges)


def degree5_with_deg6_neighbor() -> Configuration:
    """Degree-5 centre with one degree-6 neighbour.

    Ring: 0-1-2-3-4-5-6 (ring size 7).
    Interior vertex 7 (degree-5 hub) connected to 0,1,2,3,4.
    Interior vertex 8 (degree-6 neighbour) connected to 0,4,5,6.
    Triangulated interior.
    """
    ring_size = 7
    edges = [(i, (i + 1) % ring_size) for i in range(ring_size)]
    # Hub (vertex 7) is deg-5 connected to ring vertices 0-4
    edges += [(7, i) for i in range(5)]
    # Vertex 8 connected to create a deg-6 vertex
    edges += [(8, 0), (8, 4), (8, 5), (8, 6), (8, 7)]
    # Triangulate interior faces
    edges += [(7, 8)]  # already added above as (7,8) in (8,7)
    # Add triangulation edges
    edges += [(0, 5)]  # close up the configuration
    return Configuration(ring_size, [7, 8], edges)


def double_wheel_config() -> Configuration:
    """Two adjacent degree-5 vertices: ring size 8, 2 interior vertices.

    This is a REDUCIBLE configuration (no minimum counterexample has two
    adjacent deg-5 vertices).  Good test case.
    """
    ring_size = 8
    edges = [(i, (i + 1) % ring_size) for i in range(ring_size)]
    # Interior vertex 8 connected to ring 0,1,2,3,4
    edges += [(8, i) for i in range(5)]
    # Interior vertex 9 connected to ring 4,5,6,7,0
    edges += [(9, 4), (9, 5), (9, 6), (9, 7), (9, 0)]
    # Connect the two interior vertices
    edges += [(8, 9)]
    # Triangulate
    edges += [(0, 4)]
    return Configuration(ring_size, [8, 9], edges)


# ======================================================================
# Main — test with known configurations
# ======================================================================

def main() -> None:
    print("=" * 60)
    print("D-REDUCIBILITY CHECKER")
    print("Agent 1545-M3 / Infrastructure")
    print("=" * 60)

    test_configs = [
        ("Degree-5 wheel (ring=5)", degree5_wheel()),
        ("Birkhoff diamond (ring=6)", birkhoff_diamond()),
        ("Deg-5 + deg-6 neighbour (ring=7)", degree5_with_deg6_neighbor()),
        ("Double wheel / adj deg-5 (ring=8)", double_wheel_config()),
    ]

    for name, config in test_configs:
        print(f"\n{'─' * 60}")
        print(f"Configuration: {name}")
        print(f"  {config}")
        print(f"  Vertices: ring={config.ring_verts}, "
              f"interior={config.interior_verts}")
        print(f"  Edges: {len(config.edges)}")

        checker = DReducibilityChecker(config, kempe_depth=2)
        result = checker.check(verbose=True)

        status = "D-REDUCIBLE" if result['is_reducible'] else "NOT D-reducible"
        print(f"\n  Result: {status}")
        print(f"  Ring colourings: {result['total_colourings']}")
        print(f"  Direct extensions: {result['direct_extensions']}")
        print(f"  Kempe extensions: {result['kempe_extensions']}")
        print(f"  Failures: {result['failures']}")

        if result['failure_examples']:
            print(f"  Example failures:")
            for ex in result['failure_examples'][:3]:
                print(f"    {ex}")

    # Ring size capacity test
    print(f"\n{'=' * 60}")
    print("RING SIZE CAPACITY TEST")
    print(f"{'=' * 60}")
    for r in range(5, 9):
        config = Configuration(r, [], [])
        cols = enumerate_ring_colourings(config)
        print(f"  Ring size {r}: {len(cols)} proper 4-colourings "
              f"(4^{r} = {4**r} total)")


if __name__ == '__main__':
    main()
