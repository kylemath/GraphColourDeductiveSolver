"""
reduction_search.py — BFS for 5→4 colour reduction via Kempe swaps.

For each proper 5-colouring of a planar graph, search for a sequence of
Kempe swaps that eliminates the fifth colour.

Agent 0050 / Plan 2: Kempe Swap Game + Topological Non-Crossing
"""

from typing import Dict, List, Optional
from collections import deque
import networkx as nx

from kempe_ops import (
    Colouring, CanonicalColouring,
    canonical_form, colouring_from_canonical,
    is_proper_colouring, num_colours,
    all_kempe_neighbours, enumerate_colourings,
)


def bfs_reduce_to_4(G: nx.Graph, start: Colouring,
                     k: int = 5) -> Optional[List[CanonicalColouring]]:
    """
    BFS from start through Kempe swaps to find a colouring using <= 4 colours.

    Returns the path (list of canonical colourings from start to target),
    or None if no 4-colouring is reachable.
    """
    start_c = canonical_form(G, start)
    if num_colours(start) <= 4:
        return [start_c]

    visited = {start_c}
    parent: Dict[CanonicalColouring, Optional[CanonicalColouring]] = {start_c: None}
    queue: deque = deque([start_c])

    while queue:
        current = queue.popleft()
        current_col = colouring_from_canonical(G, current)
        for nbr in all_kempe_neighbours(G, current_col, k):
            if nbr in visited:
                continue
            visited.add(nbr)
            parent[nbr] = current
            nbr_col = colouring_from_canonical(G, nbr)
            if num_colours(nbr_col) <= 4:
                path = [nbr]
                node: Optional[CanonicalColouring] = current
                while node is not None:
                    path.append(node)
                    node = parent[node]
                return list(reversed(path))
            queue.append(nbr)

    return None


def test_all_5_colourings(G: nx.Graph) -> Dict:
    """
    For every proper 5-colouring of G, BFS for a 4-colouring reachable
    by Kempe swaps.  Returns statistics dict.
    """
    all_cols = enumerate_colourings(G, 5)
    five_only = [c for c in all_cols if num_colours(c) == 5]
    at_most_4 = [c for c in all_cols if num_colours(c) <= 4]

    stats: Dict = {
        'total_5_colourings': len(all_cols),
        'using_exactly_5': len(five_only),
        'using_at_most_4': len(at_most_4),
        'all_reducible': True,
        'max_path_length': 0,
        'hardest_colouring': None,
        'failures': [],
    }

    for col in five_only:
        path = bfs_reduce_to_4(G, col, k=5)
        if path is None:
            stats['all_reducible'] = False
            stats['failures'].append(canonical_form(G, col))
        elif len(path) > stats['max_path_length']:
            stats['max_path_length'] = len(path)
            stats['hardest_colouring'] = canonical_form(G, col)

    return stats
