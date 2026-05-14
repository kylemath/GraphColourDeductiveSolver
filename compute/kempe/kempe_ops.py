"""
kempe_ops.py — Core Kempe chain operations for graph colouring.

Provides proper colouring verification, Kempe chain extraction, Kempe swaps,
and colouring enumeration for small graphs.

Agent 0050 / Plan 2: Kempe Swap Game + Topological Non-Crossing
"""

from typing import Dict, List, Set, Tuple, FrozenSet
from collections import deque
import networkx as nx

Colouring = Dict[int, int]
CanonicalColouring = Tuple[int, ...]


def is_proper_colouring(G: nx.Graph, colouring: Colouring) -> bool:
    """Check if colouring is a proper vertex colouring of G."""
    if set(G.nodes()) != set(colouring.keys()):
        return False
    for u, v in G.edges():
        if colouring[u] == colouring[v]:
            return False
    return True


def colours_used(colouring: Colouring) -> Set[int]:
    """Return the set of distinct colours used."""
    return set(colouring.values())


def num_colours(colouring: Colouring) -> int:
    """Return the count of distinct colours used."""
    return len(colours_used(colouring))


def canonical_form(G: nx.Graph, colouring: Colouring) -> CanonicalColouring:
    """Convert colouring to hashable tuple indexed by sorted vertex order."""
    return tuple(colouring[v] for v in sorted(G.nodes()))


def colouring_from_canonical(G: nx.Graph, canon: CanonicalColouring) -> Colouring:
    """Reconstruct colouring dict from canonical tuple."""
    return dict(zip(sorted(G.nodes()), canon))


def get_kempe_chain(G: nx.Graph, colouring: Colouring,
                    vertex: int, colour_a: int, colour_b: int) -> FrozenSet[int]:
    """
    Extract the (colour_a, colour_b)-Kempe chain containing vertex via BFS.

    The chain is the maximal connected subgraph of the bichromatic subgraph
    G[{v : c(v) in {a,b}}] containing the given vertex.
    """
    if colouring[vertex] not in (colour_a, colour_b):
        raise ValueError(
            f"Vertex {vertex} coloured {colouring[vertex]}, expected {colour_a} or {colour_b}")
    chain = {vertex}
    queue = deque([vertex])
    while queue:
        v = queue.popleft()
        for u in G.neighbors(v):
            if u not in chain and colouring[u] in (colour_a, colour_b):
                chain.add(u)
                queue.append(u)
    return frozenset(chain)


def get_all_kempe_chains(G: nx.Graph, colouring: Colouring,
                         colour_a: int, colour_b: int) -> List[FrozenSet[int]]:
    """Get all (a,b)-Kempe chains as a list of vertex frozensets."""
    ab_verts = {v for v in G.nodes() if colouring[v] in (colour_a, colour_b)}
    visited: Set[int] = set()
    chains: List[FrozenSet[int]] = []
    for v in sorted(ab_verts):
        if v not in visited:
            chain = get_kempe_chain(G, colouring, v, colour_a, colour_b)
            chains.append(chain)
            visited |= chain
    return chains


def kempe_swap(colouring: Colouring, chain: FrozenSet[int],
               colour_a: int, colour_b: int) -> Colouring:
    """Swap colours a <-> b on all vertices in chain. Returns new dict."""
    new = dict(colouring)
    for v in chain:
        if new[v] == colour_a:
            new[v] = colour_b
        elif new[v] == colour_b:
            new[v] = colour_a
    return new


def enumerate_colourings(G: nx.Graph, k: int) -> List[Colouring]:
    """
    Enumerate all proper k-colourings of G via backtracking.

    Colours are integers 1, 2, ..., k.  Practical for n <= 12.
    """
    vertices = sorted(G.nodes())
    n = len(vertices)
    adj = {v: set(G.neighbors(v)) for v in vertices}
    results: List[Colouring] = []
    assignment: Dict[int, int] = {}

    def backtrack(idx: int) -> None:
        if idx == n:
            results.append(dict(assignment))
            return
        v = vertices[idx]
        used = {assignment[u] for u in adj[v] if u in assignment}
        for c in range(1, k + 1):
            if c not in used:
                assignment[v] = c
                backtrack(idx + 1)
                del assignment[v]

    backtrack(0)
    return results


def all_kempe_neighbours(G: nx.Graph, colouring: Colouring,
                         k: int) -> List[CanonicalColouring]:
    """
    Return all distinct colourings reachable by a single Kempe swap.

    Deduplicates by canonical form.
    """
    seen: Set[CanonicalColouring] = set()
    results: List[CanonicalColouring] = []
    for a in range(1, k + 1):
        for b in range(a + 1, k + 1):
            for chain in get_all_kempe_chains(G, colouring, a, b):
                new_col = kempe_swap(colouring, chain, a, b)
                canon = canonical_form(G, new_col)
                if canon not in seen:
                    seen.add(canon)
                    results.append(canon)
    return results
