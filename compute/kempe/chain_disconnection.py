"""
chain_disconnection.py — Test the Chain Disconnection Lemma computationally.

For each 5-colouring c and each vertex v coloured 5, simulate sequential
elimination: recolour v, then check whether the NEXT vertex w (still coloured
5) can be recoloured using only "safe" Kempe swaps — swaps on colour pairs
that don't involve v's new colour.

Also implements sequential elimination: process all colour-5 vertices one
at a time, tracking success/failure and swap counts.

Agent 0050 / Plan 2: Kempe Swap Game + Topological Non-Crossing
"""

from typing import Dict, List, Set, Tuple, Optional, FrozenSet
from collections import deque
from itertools import permutations
import networkx as nx

from kempe_ops import (
    Colouring, CanonicalColouring,
    is_proper_colouring, canonical_form, colouring_from_canonical,
    get_kempe_chain, get_all_kempe_chains, kempe_swap,
    enumerate_colourings, num_colours, colours_used,
)


def vertices_with_colour(colouring: Colouring, colour: int) -> List[int]:
    """Return sorted list of vertices with the given colour."""
    return sorted(v for v, c in colouring.items() if c == colour)


def free_colours_at(G: nx.Graph, colouring: Colouring,
                    v: int, palette: Set[int]) -> Set[int]:
    """Return colours from palette not used by any neighbour of v."""
    used = {colouring[u] for u in G.neighbors(v)}
    return palette - used


def can_recolour_with_restricted_swaps(
    G: nx.Graph, colouring: Colouring, target_v: int,
    protected_colour: int, palette: Set[int],
    max_prep_swaps: int = 3,
) -> Dict:
    """
    Check if target_v (coloured 5) can be recoloured to palette using only
    "safe" swaps — Kempe swaps on pairs NOT involving protected_colour.

    Returns dict with:
      - 'can_recolour': bool
      - 'method': 'direct' | 'safe_swap' | 'prep+swap' | 'unsafe_needed'
      - 'num_prep_swaps': int (0 if direct or single safe swap)
      - 'detail': str description
    """
    assert colouring[target_v] == 5
    target_palette = palette - {5}

    free = free_colours_at(G, colouring, target_v, target_palette)
    if free:
        return {
            'can_recolour': True,
            'method': 'direct',
            'num_prep_swaps': 0,
            'detail': f'Free colour(s) {free} available at v={target_v}',
        }

    safe_pairs = [(a, b) for a in sorted(target_palette) for b in sorted(target_palette)
                  if a < b and a != protected_colour and b != protected_colour]

    for a, b in safe_pairs:
        for chain in get_all_kempe_chains(G, colouring, a, b):
            new_col = kempe_swap(colouring, chain, a, b)
            free = free_colours_at(G, new_col, target_v, target_palette)
            if free:
                return {
                    'can_recolour': True,
                    'method': 'safe_swap',
                    'num_prep_swaps': 0,
                    'detail': f'({a},{b})-swap frees colour {free} at v={target_v}',
                }

    if max_prep_swaps >= 1:
        result = _bfs_safe_recolour(G, colouring, target_v, protected_colour,
                                     target_palette, safe_pairs, max_prep_swaps)
        if result is not None:
            return {
                'can_recolour': True,
                'method': 'prep+swap',
                'num_prep_swaps': result,
                'detail': f'{result} preparatory safe swap(s) then recolour v={target_v}',
            }

    return {
        'can_recolour': False,
        'method': 'unsafe_needed',
        'num_prep_swaps': -1,
        'detail': f'Cannot recolour v={target_v} with safe swaps (up to {max_prep_swaps} prep)',
    }


def _bfs_safe_recolour(
    G: nx.Graph, colouring: Colouring, target_v: int,
    protected_colour: int, target_palette: Set[int],
    safe_pairs: List[Tuple[int, int]], max_depth: int,
) -> Optional[int]:
    """
    BFS over sequences of safe swaps to find one that makes target_v
    recolourable. Returns number of preparatory swaps, or None.
    """
    start_c = canonical_form(G, colouring)
    visited = {start_c}
    queue: deque = deque([(start_c, 0)])

    while queue:
        current_c, depth = queue.popleft()
        if depth >= max_depth:
            continue
        current_col = colouring_from_canonical(G, current_c)
        for a, b in safe_pairs:
            for chain in get_all_kempe_chains(G, current_col, a, b):
                new_col = kempe_swap(current_col, chain, a, b)
                new_c = canonical_form(G, new_col)
                if new_c in visited:
                    continue
                visited.add(new_c)

                free = free_colours_at(G, new_col, target_v, target_palette)
                if free:
                    return depth + 1

                for a2, b2 in safe_pairs:
                    for chain2 in get_all_kempe_chains(G, new_col, a2, b2):
                        swap2 = kempe_swap(new_col, chain2, a2, b2)
                        free2 = free_colours_at(G, swap2, target_v, target_palette)
                        if free2:
                            return depth + 2

                if depth + 1 < max_depth:
                    queue.append((new_c, depth + 1))

    return None


def test_cdl_for_colouring(
    G: nx.Graph, colouring: Colouring, max_prep: int = 3,
) -> Dict:
    """
    Test the Chain Disconnection Lemma for a single 5-colouring.

    For each vertex v coloured 5, simulate recolouring v (to all possible
    colours), then check if each remaining colour-5 vertex w can be
    recoloured using restricted swaps.

    Returns detailed statistics.
    """
    v5_list = vertices_with_colour(colouring, 5)
    palette = {1, 2, 3, 4, 5}
    result = {
        'num_v5': len(v5_list),
        'all_pairs_ok': True,
        'failures': [],
        'stats': {'direct': 0, 'safe_swap': 0, 'prep+swap': 0, 'unsafe_needed': 0},
        'max_prep_needed': 0,
    }

    if len(v5_list) <= 1:
        return result

    for v in v5_list:
        free_at_v = free_colours_at(G, colouring, v, {1, 2, 3, 4})
        if not free_at_v:
            for a in range(1, 5):
                for b in range(a + 1, 5):
                    for chain in get_all_kempe_chains(G, colouring, a, b):
                        if v in chain or any(u in chain for u in G.neighbors(v)):
                            new_col = kempe_swap(colouring, chain, a, b)
                            f = free_colours_at(G, new_col, v, {1, 2, 3, 4})
                            if f:
                                free_at_v = f
                                colouring_after_v = dict(new_col)
                                colouring_after_v[v] = min(f)
                                break
                    if free_at_v:
                        break
                if free_at_v:
                    break
            if not free_at_v:
                continue
            protected = min(free_at_v)
        else:
            protected = min(free_at_v)
            colouring_after_v = dict(colouring)
            colouring_after_v[v] = protected

        for w in v5_list:
            if w == v:
                continue
            check = can_recolour_with_restricted_swaps(
                G, colouring_after_v, w, protected, palette, max_prep)
            result['stats'][check['method']] += 1
            if check['can_recolour'] and check['num_prep_swaps'] > result['max_prep_needed']:
                result['max_prep_needed'] = check['num_prep_swaps']
            if not check['can_recolour']:
                result['all_pairs_ok'] = False
                result['failures'].append({
                    'v': v, 'w': w,
                    'protected': protected,
                    'detail': check['detail'],
                })

    return result


def test_cdl_for_graph(G: nx.Graph, max_prep: int = 3) -> Dict:
    """
    Test CDL for all 5-colourings of G that use colour 5.

    Returns aggregate statistics.
    """
    all_cols = enumerate_colourings(G, 5)
    five_cols = [c for c in all_cols if num_colours(c) == 5]
    multi_v5 = [c for c in five_cols if sum(1 for v in c if c[v] == 5) >= 2]

    stats = {
        'graph_name': G.graph.get('name', '?'),
        'num_5_colourings': len(five_cols),
        'num_multi_v5': len(multi_v5),
        'all_ok': True,
        'failures': [],
        'method_counts': {'direct': 0, 'safe_swap': 0, 'prep+swap': 0, 'unsafe_needed': 0},
        'max_prep_needed': 0,
    }

    for col in multi_v5:
        result = test_cdl_for_colouring(G, col, max_prep)
        for method, count in result['stats'].items():
            stats['method_counts'][method] += count
        if result['max_prep_needed'] > stats['max_prep_needed']:
            stats['max_prep_needed'] = result['max_prep_needed']
        if not result['all_pairs_ok']:
            stats['all_ok'] = False
            stats['failures'].extend(result['failures'])

    return stats


def sequential_eliminate(
    G: nx.Graph, colouring: Colouring, ordering: List[int],
    use_restricted: bool = True, max_prep: int = 3,
) -> Dict:
    """
    Try to sequentially eliminate colour 5 by processing vertices in the
    given ordering.

    If use_restricted=True, each step only uses "safe" swaps that avoid
    the colours assigned to previously recoloured vertices.

    Returns dict with success/failure, swap count, and detail.
    """
    current = dict(colouring)
    palette = {1, 2, 3, 4}
    protected_colours: Set[int] = set()
    steps: List[Dict] = []
    total_swaps = 0

    for v in ordering:
        if current[v] != 5:
            steps.append({'v': v, 'status': 'already_done', 'swaps': 0})
            continue

        free = free_colours_at(G, current, v, palette)
        if free:
            chosen = min(free)
            current[v] = chosen
            if use_restricted:
                protected_colours.add(chosen)
            steps.append({'v': v, 'status': 'direct', 'colour': chosen, 'swaps': 0})
            continue

        if use_restricted:
            safe_pairs = [(a, b) for a in sorted(palette) for b in sorted(palette)
                          if a < b and a not in protected_colours and b not in protected_colours]
        else:
            safe_pairs = [(a, b) for a in sorted(palette) for b in sorted(palette)
                          if a < b]

        found = False
        for a, b in safe_pairs:
            for chain in get_all_kempe_chains(G, current, a, b):
                new_col = kempe_swap(current, chain, a, b)
                free = free_colours_at(G, new_col, v, palette)
                if free:
                    current = new_col
                    chosen = min(free)
                    current[v] = chosen
                    if use_restricted:
                        protected_colours.add(chosen)
                    total_swaps += 1
                    steps.append({'v': v, 'status': 'swap', 'colour': chosen, 'swaps': 1,
                                  'pair': (a, b)})
                    found = True
                    break
            if found:
                break

        if not found and max_prep > 0:
            best = _try_prep_then_swap(G, current, v, palette, safe_pairs, max_prep)
            if best is not None:
                current, chosen, n_swaps = best
                current[v] = chosen
                if use_restricted:
                    protected_colours.add(chosen)
                total_swaps += n_swaps
                steps.append({'v': v, 'status': 'prep+swap', 'colour': chosen, 'swaps': n_swaps})
                found = True

        if not found:
            return {
                'success': False,
                'stuck_at': v,
                'steps': steps,
                'total_swaps': total_swaps,
                'vertices_done': sum(1 for s in steps if s['status'] not in ('already_done',)),
                'detail': f'Stuck at v={v}, protected={protected_colours}',
            }

    assert is_proper_colouring(G, current), "Final colouring is improper!"
    assert num_colours(current) <= 4, f"Final colouring uses {num_colours(current)} colours!"

    return {
        'success': True,
        'stuck_at': None,
        'steps': steps,
        'total_swaps': total_swaps,
        'vertices_done': sum(1 for s in steps if s['status'] not in ('already_done',)),
    }


def _try_prep_then_swap(
    G: nx.Graph, colouring: Colouring, target_v: int,
    palette: Set[int], safe_pairs: List[Tuple[int, int]], max_depth: int,
) -> Optional[Tuple[Colouring, int, int]]:
    """BFS to find preparatory swap sequence that enables recolouring target_v."""
    start_c = canonical_form(G, colouring)
    visited = {start_c}
    queue: deque = deque([(start_c, 0)])

    while queue:
        current_c, depth = queue.popleft()
        if depth >= max_depth:
            continue
        current_col = colouring_from_canonical(G, current_c)
        for a, b in safe_pairs:
            for chain in get_all_kempe_chains(G, current_col, a, b):
                new_col = kempe_swap(current_col, chain, a, b)
                new_c = canonical_form(G, new_col)
                if new_c in visited:
                    continue
                visited.add(new_c)
                free = free_colours_at(G, new_col, target_v, palette)
                if free:
                    return (new_col, min(free), depth + 1)
                if depth + 1 < max_depth:
                    queue.append((new_c, depth + 1))
    return None


def test_sequential_elimination(
    G: nx.Graph, max_orderings: int = 100, use_restricted: bool = True,
    max_prep: int = 3,
) -> Dict:
    """
    Test sequential elimination for all 5-colourings of G.

    For each 5-colouring with multiple colour-5 vertices, try up to
    max_orderings permutations of the colour-5 vertices.
    """
    all_cols = enumerate_colourings(G, 5)
    five_cols = [c for c in all_cols if num_colours(c) == 5]
    multi_v5 = [c for c in five_cols if sum(1 for v in c if c[v] == 5) >= 2]

    stats = {
        'graph_name': G.graph.get('name', '?'),
        'num_multi_v5': len(multi_v5),
        'all_succeed': True,
        'some_ordering_works': True,
        'total_attempts': 0,
        'total_successes': 0,
        'total_failures': 0,
        'max_swaps': 0,
        'failure_details': [],
    }

    for col in multi_v5:
        v5_list = vertices_with_colour(col, 5)
        n_perms = 1
        for i in range(1, len(v5_list) + 1):
            n_perms *= i

        if n_perms <= max_orderings:
            orderings = list(permutations(v5_list))
        else:
            import random
            rng = random.Random(42)
            orderings = [list(v5_list)]
            seen = {tuple(v5_list)}
            for _ in range(max_orderings - 1):
                perm = list(v5_list)
                rng.shuffle(perm)
                if tuple(perm) not in seen:
                    seen.add(tuple(perm))
                    orderings.append(perm)

        any_works = False
        all_work = True
        for ordering in orderings:
            result = sequential_eliminate(G, col, list(ordering),
                                          use_restricted=use_restricted,
                                          max_prep=max_prep)
            stats['total_attempts'] += 1
            if result['success']:
                stats['total_successes'] += 1
                any_works = True
                if result['total_swaps'] > stats['max_swaps']:
                    stats['max_swaps'] = result['total_swaps']
            else:
                stats['total_failures'] += 1
                all_work = False
                stats['failure_details'].append({
                    'colouring': canonical_form(G, col),
                    'ordering': list(ordering),
                    'stuck_at': result['stuck_at'],
                    'detail': result.get('detail', ''),
                })

        if not any_works:
            stats['some_ordering_works'] = False
        if not all_work:
            stats['all_succeed'] = False

    return stats
