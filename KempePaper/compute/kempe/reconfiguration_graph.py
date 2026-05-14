"""
reconfiguration_graph.py — Build and analyze Kempe reconfiguration graphs R(G,k).

R(G,k) has proper k-colourings as nodes and single Kempe swaps as edges.

Agent 0050 / Plan 2: Kempe Swap Game + Topological Non-Crossing
"""

from typing import Dict, Set
import networkx as nx

from kempe_ops import (
    Colouring, CanonicalColouring,
    canonical_form, colouring_from_canonical,
    enumerate_colourings, all_kempe_neighbours, num_colours,
)


def build_reconfiguration_graph(G: nx.Graph, k: int) -> nx.Graph:
    """
    Build R(G,k): nodes = proper k-colourings (canonical tuples),
    edges = single Kempe swaps.
    """
    colourings = enumerate_colourings(G, k)
    canon_set: Set[CanonicalColouring] = set()
    for col in colourings:
        canon_set.add(canonical_form(G, col))

    R = nx.Graph()
    R.add_nodes_from(canon_set)

    for canon in canon_set:
        col = colouring_from_canonical(G, canon)
        for nbr in all_kempe_neighbours(G, col, k):
            if nbr in canon_set and nbr != canon:
                R.add_edge(canon, nbr)

    return R


def analyze_reconfiguration_graph(R: nx.Graph) -> Dict:
    """Compute structural properties of a reconfiguration graph."""
    components = list(nx.connected_components(R))
    info: Dict = {
        'num_nodes': R.number_of_nodes(),
        'num_edges': R.number_of_edges(),
        'num_components': len(components),
        'is_connected': len(components) == 1,
        'component_sizes': sorted([len(c) for c in components], reverse=True),
    }
    if info['is_connected'] and R.number_of_nodes() > 1:
        info['diameter'] = nx.diameter(R)
    elif info['is_connected']:
        info['diameter'] = 0
    else:
        info['diameter'] = None
        info['component_diameters'] = []
        for comp in components:
            sub = R.subgraph(comp)
            info['component_diameters'].append(
                nx.diameter(sub) if len(comp) > 1 else 0)
    return info


def check_5_to_4_connectivity(G: nx.Graph) -> Dict:
    """
    In R(G,5), check whether every 5-colouring can reach a 4-colouring
    via Kempe swaps.
    """
    R = build_reconfiguration_graph(G, 5)

    four_nodes: Set[CanonicalColouring] = set()
    five_nodes: Set[CanonicalColouring] = set()
    vertices = sorted(G.nodes())
    for node in R.nodes():
        col = dict(zip(vertices, node))
        if num_colours(col) <= 4:
            four_nodes.add(node)
        else:
            five_nodes.add(node)

    unreachable = []
    for node in five_nodes:
        comp = nx.node_connected_component(R, node)
        if not comp & four_nodes:
            unreachable.append(node)

    return {
        'total_colourings': R.number_of_nodes(),
        'four_colourings': len(four_nodes),
        'five_only_colourings': len(five_nodes),
        'all_5_reach_4': len(unreachable) == 0,
        'unreachable_count': len(unreachable),
        'R5_connected': nx.is_connected(R) if R.number_of_nodes() > 0 else True,
    }
