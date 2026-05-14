"""
noncrossing_verifier.py — Verify the non-crossing property of Kempe chains
in planar graphs.

For disjoint colour pairs {a,b} and {c,d} in a planar graph, the Jordan
Curve Theorem guarantees their Kempe chains don't topologically interleave.

KEY INSIGHT: The local check at a vertex v (positions on the neighbour cycle
don't interleave) is valid ONLY when v is external to all chains being
checked — i.e., v's colour is NOT in {a,b,c,d}.  For 4-colourings every
vertex is in some chain, so the local check is vacuously inapplicable.
For 5-colourings, vertices coloured 5 are external to all {1,2,3,4} chains.

Agent 0050 / Plan 2: Kempe Swap Game + Topological Non-Crossing
"""

from typing import List, Tuple, Dict, Optional, Set
from itertools import combinations
import networkx as nx

from kempe_ops import (
    Colouring, get_kempe_chain, enumerate_colourings, num_colours,
)


def get_cyclic_neighbours(emb: nx.PlanarEmbedding, v: int) -> List[int]:
    """Get neighbours of v in clockwise cyclic order from the embedding."""
    return list(emb.neighbors_cw_order(v))


def check_noncrossing_pair(positions_A: List[int],
                           positions_B: List[int],
                           cycle_length: int) -> bool:
    """
    Check if two sets of positions on a cycle are non-crossing.

    Non-crossing iff the cyclic label sequence has at most 2 transitions
    between A-labels and B-labels.
    """
    if not positions_A or not positions_B:
        return True
    labelled = [(p, 'A') for p in positions_A] + [(p, 'B') for p in positions_B]
    labelled.sort(key=lambda x: x[0])
    if len(labelled) <= 1:
        return True
    transitions = sum(
        1 for i in range(len(labelled))
        if labelled[i][1] != labelled[(i + 1) % len(labelled)][1]
    )
    return transitions <= 2


def verify_noncrossing_at_vertex(
    G: nx.Graph,
    emb: nx.PlanarEmbedding,
    colouring: Colouring,
    v: int,
) -> Tuple[bool, Optional[str]]:
    """
    Verify non-crossing at vertex v for all disjoint colour pair partitions
    where v's colour is NOT in either pair.

    For 4-colourings (colours {1..4}), this is vacuously true since v is
    always in some pair.  For 5-colourings at a vertex coloured 5, this
    tests the Theorem A scenario.
    """
    neighbours = get_cyclic_neighbours(emb, v)
    d = len(neighbours)
    if d < 4:
        return True, None

    v_colour = colouring[v]
    all_colours = sorted(set(colouring.values()))
    chain_colours = sorted(c for c in all_colours if c != v_colour)

    if len(chain_colours) < 4:
        return True, None

    for pair_ab in combinations(chain_colours, 2):
        a, b = pair_ab
        remaining = sorted(set(chain_colours) - {a, b})
        if len(remaining) < 2:
            continue
        for pair_cd in combinations(remaining, 2):
            c, d_col = pair_cd
            ab_by_chain: Dict[frozenset, List[int]] = {}
            cd_by_chain: Dict[frozenset, List[int]] = {}

            for idx, w in enumerate(neighbours):
                wc = colouring[w]
                if wc in (a, b):
                    chain = get_kempe_chain(G, colouring, w, a, b)
                    ab_by_chain.setdefault(chain, []).append(idx)
                elif wc in (c, d_col):
                    chain = get_kempe_chain(G, colouring, w, c, d_col)
                    cd_by_chain.setdefault(chain, []).append(idx)

            for ab_pos in ab_by_chain.values():
                for cd_pos in cd_by_chain.values():
                    if not check_noncrossing_pair(ab_pos, cd_pos, d):
                        return False, (
                            f"Crossing at v={v} (colour {v_colour}): "
                            f"({a},{b})-chain positions {ab_pos} "
                            f"interleave with ({c},{d_col})-chain positions "
                            f"{cd_pos} among {d} neighbours")

    return True, None


def verify_noncrossing_5col(G: nx.Graph,
                            colouring: Colouring) -> Tuple[bool, List[str]]:
    """
    Verify non-crossing at every vertex whose colour is outside {1..4}.

    In a 5-colouring, this checks at all vertices coloured 5 — exactly
    the Theorem A scenario.
    """
    is_planar, emb = nx.check_planarity(G)
    if not is_planar:
        return False, ["Graph is not planar"]
    chain_colours = {1, 2, 3, 4}
    violations: List[str] = []
    for v in G.nodes():
        if colouring[v] in chain_colours:
            continue
        ok, desc = verify_noncrossing_at_vertex(G, emb, colouring, v)
        if not ok and desc:
            violations.append(desc)
    return len(violations) == 0, violations


def verify_noncrossing_exhaustive_5col(G: nx.Graph) -> Dict:
    """
    Verify non-crossing for ALL proper 5-colourings of G, at all vertices
    coloured 5.  This is the computational test of Theorem A.
    """
    all_cols = enumerate_colourings(G, 5)
    result: Dict = {
        'num_5_colourings': len(all_cols),
        'colourings_with_colour5': 0,
        'vertices_checked': 0,
        'all_noncrossing': True,
        'violations': [],
    }
    for col in all_cols:
        has_5 = any(c == 5 for c in col.values())
        if not has_5:
            continue
        result['colourings_with_colour5'] += 1
        ok, violations = verify_noncrossing_5col(G, col)
        v5_count = sum(1 for c in col.values() if c == 5)
        result['vertices_checked'] += v5_count
        if not ok:
            result['all_noncrossing'] = False
            result['violations'].extend(violations)
    return result


def classify_chain_config_at_vertex(
    G: nx.Graph,
    emb: nx.PlanarEmbedding,
    colouring: Colouring,
    v: int,
) -> Dict:
    """
    Classify the Kempe chain configuration at a degree-5 vertex v
    coloured 5.  Returns the colour pattern and chain connectivity.
    """
    neighbours = get_cyclic_neighbours(emb, v)
    colour_pattern = tuple(colouring[w] for w in neighbours)

    chain_info: Dict = {
        'vertex': v,
        'degree': len(neighbours),
        'colour_pattern': colour_pattern,
        'distinct_colours': len(set(colour_pattern)),
        'partitions': {},
    }

    if len(set(colour_pattern)) < 4:
        chain_info['easy_case'] = True
        missing = set(range(1, 5)) - set(colour_pattern)
        chain_info['free_colours'] = sorted(missing)
        return chain_info

    chain_info['easy_case'] = False
    chain_colours = sorted(set(colour_pattern))

    for pair_ab in combinations(chain_colours, 2):
        a, b = pair_ab
        remaining = sorted(set(chain_colours) - {a, b})
        if len(remaining) != 2:
            continue
        c, d = remaining

        ab_chains: Dict[frozenset, List[int]] = {}
        cd_chains: Dict[frozenset, List[int]] = {}

        for idx, w in enumerate(neighbours):
            wc = colouring[w]
            if wc in (a, b):
                chain = get_kempe_chain(G, colouring, w, a, b)
                ab_chains.setdefault(chain, []).append(idx)
            elif wc in (c, d):
                chain = get_kempe_chain(G, colouring, w, c, d)
                cd_chains.setdefault(chain, []).append(idx)

        key = f"({a},{b})|({c},{d})"
        chain_info['partitions'][key] = {
            'ab_chain_count': len(ab_chains),
            'cd_chain_count': len(cd_chains),
            'ab_positions': [sorted(p) for p in ab_chains.values()],
            'cd_positions': [sorted(p) for p in cd_chains.values()],
        }

    return chain_info
