"""
triangulation_db.py — Generate and catalog small planar triangulations.

Uses face-splitting and edge-flipping with isomorphism filtering to
enumerate all triangulations of the sphere up to a given vertex count.

Agent 0050 / Plan 2: Kempe Swap Game + Topological Non-Crossing
"""

from typing import List, Tuple, Dict, Optional
import networkx as nx


# ---------------------------------------------------------------------------
# Named triangulations
# ---------------------------------------------------------------------------

def make_K4() -> nx.Graph:
    """K4 — the unique triangulation on 4 vertices (tetrahedron)."""
    G = nx.complete_graph(4)
    G.graph['name'] = 'K4'
    return G


def make_bipyramid() -> nx.Graph:
    """Triangular bipyramid — unique triangulation on 5 vertices (K5 \\ e)."""
    G = nx.complete_graph(5)
    G.remove_edge(0, 4)
    G.graph['name'] = 'bipyramid_5'
    return G


def make_octahedron() -> nx.Graph:
    """Octahedron K_{2,2,2} — 6 vertices, all degree 4."""
    G = nx.octahedral_graph()
    G.graph['name'] = 'octahedron'
    return G


def make_icosahedron() -> nx.Graph:
    """Icosahedron — 12 vertices, all degree 5."""
    G = nx.icosahedral_graph()
    G.graph['name'] = 'icosahedron'
    return G


# ---------------------------------------------------------------------------
# Planar-embedding utilities
# ---------------------------------------------------------------------------

def get_planar_embedding(G: nx.Graph) -> Optional[nx.PlanarEmbedding]:
    """Return a planar embedding, or None if G is not planar."""
    is_planar, emb = nx.check_planarity(G)
    return emb if is_planar else None


def get_faces(emb: nx.PlanarEmbedding) -> List[Tuple[int, ...]]:
    """Extract all faces from a planar embedding as vertex tuples."""
    seen_half_edges: set = set()
    faces: List[Tuple[int, ...]] = []
    for v in emb:
        for w in emb.neighbors_cw_order(v):
            if (v, w) not in seen_half_edges:
                face = emb.traverse_face(v, w)
                for i in range(len(face)):
                    seen_half_edges.add((face[i], face[(i + 1) % len(face)]))
                faces.append(tuple(face))
    return faces


def is_triangulation(G: nx.Graph) -> bool:
    """Check if G is a maximal planar graph (triangulation of the sphere)."""
    n = G.number_of_nodes()
    if n < 4:
        return False
    if G.number_of_edges() != 3 * n - 6:
        return False
    is_planar, _ = nx.check_planarity(G)
    return is_planar


# ---------------------------------------------------------------------------
# Generation: face splitting
# ---------------------------------------------------------------------------

def split_face(G: nx.Graph, face: Tuple[int, ...]) -> nx.Graph:
    """Place a new vertex inside a triangular face, connecting to all 3 corners."""
    assert len(face) == 3, f"Expected triangular face, got {len(face)} vertices"
    new_v = max(G.nodes()) + 1
    H = G.copy()
    H.add_node(new_v)
    for v in face:
        H.add_edge(new_v, v)
    return H


# ---------------------------------------------------------------------------
# Generation: edge flipping
# ---------------------------------------------------------------------------

def flip_edge(G: nx.Graph, u: int, v: int,
              emb: nx.PlanarEmbedding) -> Optional[nx.Graph]:
    """
    Flip edge (u,v): replace with the edge joining the opposite vertices
    of the two triangles sharing (u,v).  Returns None if invalid.
    """
    if not G.has_edge(u, v):
        return None
    face1 = emb.traverse_face(u, v)
    face2 = emb.traverse_face(v, u)
    if len(face1) != 3 or len(face2) != 3:
        return None
    opp1 = [x for x in face1 if x != u and x != v]
    opp2 = [x for x in face2 if x != u and x != v]
    if len(opp1) != 1 or len(opp2) != 1:
        return None
    a, b = opp1[0], opp2[0]
    if a == b or G.has_edge(a, b):
        return None
    H = G.copy()
    H.remove_edge(u, v)
    H.add_edge(a, b)
    if not is_triangulation(H):
        return None
    return H


# ---------------------------------------------------------------------------
# Systematic enumeration
# ---------------------------------------------------------------------------

def generate_triangulations(max_n: int) -> Dict[int, List[nx.Graph]]:
    """
    Generate all triangulations on 4..max_n vertices.

    Strategy: face-splitting for each n, then edge-flipping within each n
    until no new triangulations are found.  Isomorphism filtering via
    networkx.is_isomorphic.

    Known counts (OEIS A000109):
      n=4:1  n=5:1  n=6:2  n=7:5  n=8:14  n=9:50  n=10:233
    """
    result: Dict[int, List[nx.Graph]] = {}
    result[4] = [make_K4()]

    for n in range(5, max_n + 1):
        candidates: List[nx.Graph] = []

        # Phase 1: face splitting from (n-1)-vertex triangulations
        for T in result[n - 1]:
            emb = get_planar_embedding(T)
            if emb is None:
                continue
            for face in get_faces(emb):
                if len(face) == 3:
                    candidates.append(split_face(T, face))

        # Deduplicate
        unique: List[nx.Graph] = []
        for H in candidates:
            if not any(nx.is_isomorphic(H, U) for U in unique):
                unique.append(H)

        # Phase 2: edge flipping until stable
        changed = True
        while changed:
            changed = False
            additions: List[nx.Graph] = []
            for T in unique:
                emb = get_planar_embedding(T)
                if emb is None:
                    continue
                for u_edge, v_edge in list(T.edges()):
                    H = flip_edge(T, u_edge, v_edge, emb)
                    if H is not None:
                        if not any(nx.is_isomorphic(H, U) for U in unique) and \
                           not any(nx.is_isomorphic(H, U) for U in additions):
                            additions.append(H)
                            changed = True
            unique.extend(additions)

        for i, T in enumerate(unique):
            T.graph['name'] = f'T_{n}_{i}'
        result[n] = unique

    return result
