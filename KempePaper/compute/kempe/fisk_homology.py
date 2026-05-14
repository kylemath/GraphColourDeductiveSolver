"""
fisk_homology.py — Compute Fisk group structure for 4-colourings.

Fisk (1977) showed that 4-colourings of a triangulation of a surface
of genus g, modulo Kempe swaps, form a group isomorphic to Z_2^g.
For the sphere (g=0), all 4-colourings should be Kempe-equivalent.

Agent 0050 / Plan 2: Kempe Swap Game + Topological Non-Crossing
"""

from typing import Dict, List, Set
import networkx as nx

from kempe_ops import (
    CanonicalColouring,
    canonical_form, colouring_from_canonical,
    enumerate_colourings, get_all_kempe_chains, kempe_swap,
)


def _find(parent: Dict, x: CanonicalColouring) -> CanonicalColouring:
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def _union(parent: Dict, rank: Dict, x: CanonicalColouring,
           y: CanonicalColouring) -> None:
    rx, ry = _find(parent, x), _find(parent, y)
    if rx == ry:
        return
    if rank[rx] < rank[ry]:
        rx, ry = ry, rx
    parent[ry] = rx
    if rank[rx] == rank[ry]:
        rank[rx] += 1


def build_fisk_equivalence(G: nx.Graph, k: int = 4) -> Dict:
    """
    Compute Fisk equivalence classes: k-colourings modulo single-pair
    Kempe swaps.

    For triangulations of the sphere (genus 0), expects one class.
    """
    colourings = enumerate_colourings(G, k)
    canon_set: Set[CanonicalColouring] = set()
    for c in colourings:
        canon_set.add(canonical_form(G, c))

    parent = {c: c for c in canon_set}
    rank = {c: 0 for c in canon_set}

    for canon in canon_set:
        col = colouring_from_canonical(G, canon)
        for a in range(1, k + 1):
            for b in range(a + 1, k + 1):
                for chain in get_all_kempe_chains(G, col, a, b):
                    new_col = kempe_swap(col, chain, a, b)
                    new_canon = canonical_form(G, new_col)
                    if new_canon in canon_set:
                        _union(parent, rank, canon, new_canon)

    classes: Dict[CanonicalColouring, List[CanonicalColouring]] = {}
    for canon in canon_set:
        root = _find(parent, canon)
        classes.setdefault(root, []).append(canon)

    return {
        'num_colourings': len(canon_set),
        'num_classes': len(classes),
        'class_sizes': sorted([len(v) for v in classes.values()], reverse=True),
        'is_single_class': len(classes) == 1,
    }
