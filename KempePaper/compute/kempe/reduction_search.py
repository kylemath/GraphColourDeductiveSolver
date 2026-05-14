"""
reduction_search.py — BFS for 5→4 colour reduction via Kempe swaps.

For each proper 5-colouring of a planar graph, search for a sequence of
Kempe swaps that eliminates the fifth colour.

Includes optimized multi-source BFS (from 4-colourings outward) and
inductive-lift verification for the G-v → G correspondence.

Agent 0050 / Plan 2: Kempe Swap Game + Topological Non-Crossing
"""

from typing import Dict, List, Optional, Set, Tuple, FrozenSet
from collections import deque
import networkx as nx

from kempe_ops import (
    Colouring, CanonicalColouring,
    canonical_form, colouring_from_canonical,
    is_proper_colouring, num_colours, colours_used,
    all_kempe_neighbours, enumerate_colourings,
    get_kempe_chain, get_all_kempe_chains, kempe_swap,
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


# ---------------------------------------------------------------------------
# Optimized multi-source BFS: compute distance from every 5-colouring
# to the nearest 4-colouring in a single pass.
# ---------------------------------------------------------------------------

def bulk_distance_to_4col(G: nx.Graph, k: int = 5) -> Dict:
    """
    Multi-source BFS from all 4-colourings outward through R(G,k).

    Returns dict with:
      - 'max_distance': max distance from any 5-colouring to nearest 4-colouring
      - 'all_reachable': True if every 5-colouring is reachable
      - 'distance_histogram': {d: count}
      - 'hardest_colourings': list of canonical colourings at max distance
      - 'hardest_swap_sequences': for each hardest colouring, the BFS parent path
      - 'num_4col', 'num_5col': counts
    """
    all_cols = enumerate_colourings(G, k)
    canon_map: Dict[CanonicalColouring, bool] = {}
    four_colourings: List[CanonicalColouring] = []
    five_colourings: List[CanonicalColouring] = []

    for col in all_cols:
        c = canonical_form(G, col)
        if c in canon_map:
            continue
        is_4 = num_colours(col) <= 4
        canon_map[c] = is_4
        if is_4:
            four_colourings.append(c)
        else:
            five_colourings.append(c)

    dist: Dict[CanonicalColouring, int] = {}
    parent: Dict[CanonicalColouring, Optional[CanonicalColouring]] = {}
    queue: deque = deque()

    for c in four_colourings:
        dist[c] = 0
        parent[c] = None
        queue.append(c)

    while queue:
        current = queue.popleft()
        current_col = colouring_from_canonical(G, current)
        for nbr in all_kempe_neighbours(G, current_col, k):
            if nbr not in dist:
                dist[nbr] = dist[current] + 1
                parent[nbr] = current
                queue.append(nbr)

    max_d = 0
    histogram: Dict[int, int] = {}
    hardest: List[CanonicalColouring] = []
    unreachable: List[CanonicalColouring] = []

    for c in five_colourings:
        if c in dist:
            d = dist[c]
            histogram[d] = histogram.get(d, 0) + 1
            if d > max_d:
                max_d = d
                hardest = [c]
            elif d == max_d:
                hardest.append(c)
        else:
            unreachable.append(c)

    for c in four_colourings:
        histogram[0] = histogram.get(0, 0) + 1

    swap_sequences: List[List[CanonicalColouring]] = []
    for c in hardest[:5]:
        path = [c]
        node = parent.get(c)
        while node is not None:
            path.append(node)
            node = parent.get(node)
        swap_sequences.append(list(reversed(path)))

    return {
        'max_distance': max_d,
        'all_reachable': len(unreachable) == 0,
        'distance_histogram': dict(sorted(histogram.items())),
        'hardest_colourings': hardest,
        'hardest_swap_sequences': swap_sequences,
        'num_4col': len(four_colourings),
        'num_5col': len(five_colourings),
        'unreachable': unreachable,
    }


# ---------------------------------------------------------------------------
# Inductive lift verification: remove vertex v from G, check whether
# the swap sequence for G-v can be "lifted" to G.
# ---------------------------------------------------------------------------

def _vertices_coloured(col: Colouring, colour: int) -> List[int]:
    return sorted(v for v, c in col.items() if c == colour)


def verify_inductive_lift(G: nx.Graph, v: int) -> Dict:
    """
    For each 5-colouring of G where c(v) = 5:
    1. Restrict to G-v → get a 5-colouring of G-v
    2. Find the BFS swap sequence in G-v reaching a 4-colouring
    3. Attempt to apply the SAME swap sequence in G
    4. Check: does it produce a 4-colouring of G-v within G
       (leaving v the only possible colour-5 vertex)?
    5. Then check: can v be recoloured in {1..4}?

    Returns statistics on how often the lift succeeds vs fails,
    and what goes wrong when it fails.
    """
    H = G.copy()
    H.remove_node(v)
    H_nodes = sorted(H.nodes())
    G_nodes = sorted(G.nodes())

    all_G_cols = enumerate_colourings(G, 5)
    v5_cols = [c for c in all_G_cols if c[v] == 5 and num_colours(c) == 5]

    stats = {
        'vertex': v,
        'degree': G.degree(v),
        'num_v5_colourings': len(v5_cols),
        'lift_succeeded': 0,
        'lift_failed_chain_merge': 0,
        'lift_failed_other': 0,
        'v_recolourable_after_lift': 0,
        'total_tested': 0,
        'chain_merge_examples': [],
    }

    for col in v5_cols:
        stats['total_tested'] += 1
        col_H = {u: col[u] for u in H_nodes}

        path_H = bfs_reduce_to_4(H, col_H, k=5)
        if path_H is None or len(path_H) <= 1:
            continue

        col_G = dict(col)
        lift_ok = True
        merge_info = None

        for step_idx in range(len(path_H) - 1):
            cur_H = colouring_from_canonical(H, path_H[step_idx])
            nxt_H = colouring_from_canonical(H, path_H[step_idx + 1])

            swap_colour_a, swap_colour_b = _identify_swap(H, cur_H, nxt_H)
            if swap_colour_a is None:
                lift_ok = False
                merge_info = f"could not identify swap at step {step_idx}"
                break

            swapped_verts = {u for u in H_nodes if cur_H[u] != nxt_H[u]}

            chain_H = frozenset(swapped_verts)
            if not swapped_verts:
                continue

            start_vert = next(iter(swapped_verts))
            chain_G = get_kempe_chain(G, col_G, start_vert,
                                       swap_colour_a, swap_colour_b)

            extra_in_G = chain_G - chain_H - {v}
            if extra_in_G:
                lift_ok = False
                merge_info = (f"step {step_idx}: ({swap_colour_a},{swap_colour_b})-chain "
                              f"in G has {len(chain_G)} vertices vs {len(chain_H)} in G-v; "
                              f"extra={sorted(extra_in_G)}")
                break

            col_G = kempe_swap(col_G, chain_H, swap_colour_a, swap_colour_b)

        if lift_ok:
            stats['lift_succeeded'] += 1
            v5_remaining = _vertices_coloured(col_G, 5)
            neighbour_colours = {col_G[u] for u in G.neighbors(v)}
            free = {1, 2, 3, 4} - neighbour_colours
            if free or v not in v5_remaining:
                stats['v_recolourable_after_lift'] += 1
        else:
            stats['lift_failed_chain_merge'] += 1
            if merge_info and len(stats['chain_merge_examples']) < 5:
                stats['chain_merge_examples'].append(merge_info)

    return stats


def _identify_swap(G: nx.Graph, col_before: Colouring,
                   col_after: Colouring) -> Tuple[Optional[int], Optional[int]]:
    """Identify which colour pair was swapped between two colourings."""
    changed = {v for v in col_before if col_before[v] != col_after[v]}
    if not changed:
        return None, None
    colours_involved = set()
    for v in changed:
        colours_involved.add(col_before[v])
        colours_involved.add(col_after[v])
    if len(colours_involved) == 2:
        a, b = sorted(colours_involved)
        return a, b
    return None, None


# ---------------------------------------------------------------------------
# Monotone path analysis: check whether |V_5| decreases at each step.
# ---------------------------------------------------------------------------

def find_monotone_path(G: nx.Graph, start: Colouring,
                        k: int = 5) -> Optional[List[Tuple[CanonicalColouring, int]]]:
    """
    BFS for a path from start to a 4-colouring where |V_5| strictly decreases
    at every step.

    Returns list of (canonical_colouring, num_v5) tuples, or None if no
    monotone path exists. Uses BFS restricted to neighbours with strictly
    fewer colour-5 vertices.
    """
    def count_v5(col: Colouring) -> int:
        return sum(1 for c in col.values() if c == 5)

    start_c = canonical_form(G, start)
    start_v5 = count_v5(start)
    if start_v5 == 0:
        return [(start_c, 0)]

    visited: Set[CanonicalColouring] = {start_c}
    parent: Dict[CanonicalColouring, Optional[CanonicalColouring]] = {start_c: None}
    v5_count: Dict[CanonicalColouring, int] = {start_c: start_v5}
    queue: deque = deque([start_c])

    while queue:
        current = queue.popleft()
        cur_col = colouring_from_canonical(G, current)
        cur_v5 = v5_count[current]

        for nbr in all_kempe_neighbours(G, cur_col, k):
            if nbr in visited:
                continue
            nbr_col = colouring_from_canonical(G, nbr)
            nbr_v5 = count_v5(nbr_col)
            if nbr_v5 >= cur_v5:
                continue
            visited.add(nbr)
            parent[nbr] = current
            v5_count[nbr] = nbr_v5
            if nbr_v5 == 0:
                path = [(nbr, 0)]
                node = current
                while node is not None:
                    path.append((node, v5_count[node]))
                    node = parent[node]
                return list(reversed(path))
            queue.append(nbr)

    return None


def analyze_swap_sequence(G: nx.Graph, path: List[CanonicalColouring],
                           k: int = 5) -> List[Dict]:
    """
    Analyze a swap sequence: for each step, identify the colour pair,
    chain size, and |V_5| change.
    """
    steps = []
    for i in range(len(path) - 1):
        col_before = colouring_from_canonical(G, path[i])
        col_after = colouring_from_canonical(G, path[i + 1])
        a, b = _identify_swap(G, col_before, col_after)
        v5_before = sum(1 for c in col_before.values() if c == 5)
        v5_after = sum(1 for c in col_after.values() if c == 5)
        changed = {v for v in col_before if col_before[v] != col_after[v]}
        steps.append({
            'step': i,
            'colour_pair': (a, b),
            'chain_size': len(changed),
            'v5_before': v5_before,
            'v5_after': v5_after,
            'v5_delta': v5_after - v5_before,
            'monotone': v5_after <= v5_before,
        })
    return steps
