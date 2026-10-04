"""Group D3 (Agent 1720): signed Tait counts on duals of triangulations.

For each cached triangulation ``T`` with ``n <= max_n`` vertices, build the
plane dual ``T*`` (cubic, ``2n-4`` vertices) and enumerate its proper
3-edge-colourings with colours ``{0,1,2}``.

The sign of a colouring is the product, over vertices of ``T*``, of the sign
of the permutation ``(c_0, c_1, c_2)`` of ``(0,1,2)`` read in the planar
rotation at that vertex. The rotation is the boundary order of the
corresponding triangular face of ``T`` in the embedding returned by
``networkx.check_planarity``.

The dual has ``V = 2n-4 = 2(n-2)`` vertices, always even, so this sign is
unchanged by reversing every rotation and by relabelling the three colours.
On these 3-connected graphs the embedding is unique up to reflection
(Whitney), so the signed count is an invariant of the abstract dual.

The identity proved in ``groups/D3_report.md`` is that every such colouring
has sign ``(-1)^n``. The census below checks that identity on the cache.

Usage::

    /Users/fulkanjou/GraphColour/.venv/bin/python compute/flows/a1720_alon_tarsi.py [max_n]
"""

from __future__ import annotations

import itertools
import json
import sys
import time
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "compute" / "data" / "triangulations_n4_11.json"
OUT = ROOT / "backgroundMaterial" / "agent1720" / "groups" / "D3_results.json"
D1 = ROOT / "backgroundMaterial" / "agent1720" / "groups" / "D1_results.json"

SIGN = [[[0] * 3 for _ in range(3)] for _ in range(3)]
for _p in itertools.permutations(range(3)):
    _inv = (_p[0] > _p[1]) + (_p[0] > _p[2]) + (_p[1] > _p[2])
    SIGN[_p[0]][_p[1]][_p[2]] = 1 if _inv % 2 == 0 else -1

# Nonzero elements of Z2 x Z2, written as integers 1,2,3 under XOR, sent to
# the Tait colours 0,1,2.  Addition is XOR, which is subtraction in char 2.
MAP = {1: 0, 2: 1, 3: 2}


def permutation_sign(colours: tuple[int, int, int]) -> int:
    """Sign of ``colours`` as a permutation of ``(0, 1, 2)``."""
    return SIGN[colours[0]][colours[1]][colours[2]]


def dual_rotation(
    T: nx.Graph,
) -> tuple[nx.Graph, list[tuple[int, int, int]], list[list[int]]]:
    """Plane dual, neighbour rotations, and the primal face walks.

    Dual vertex ``i`` is face ``i``. Its rotation is the three neighbouring
    faces met while walking the boundary of face ``i``.
    """
    ok, emb = nx.check_planarity(T)
    if not ok:
        raise ValueError("graph is not planar")
    face_of: dict[tuple[int, int], int] = {}
    faces: list[list[int]] = []
    for u, v in emb.edges():
        if (u, v) in face_of:
            continue
        marked: set[tuple[int, int]] = set()
        face = list(emb.traverse_face(u, v, mark_half_edges=marked))
        for he in marked:
            face_of[he] = len(faces)
        faces.append(face)
    n = T.number_of_nodes()
    if len(faces) != 2 * n - 4 or any(len(f) != 3 for f in faces):
        raise ValueError("not a triangulation")
    graph = nx.Graph()
    graph.add_nodes_from(range(len(faces)))
    rotation: list[tuple[int, int, int]] = []
    for fi, face in enumerate(faces):
        nbrs: list[int] = []
        for i in range(3):
            a = face[i]
            b = face[(i + 1) % 3]
            if face_of[(a, b)] != fi:
                raise ValueError("face walk is not the boundary order")
            nbrs.append(face_of[(b, a)])
        if len(set(nbrs)) != 3:
            raise ValueError("dual has a loop or a digon")
        rotation.append((nbrs[0], nbrs[1], nbrs[2]))
        for other in nbrs:
            if fi < other:
                graph.add_edge(fi, other)
    if any(d != 3 for _, d in graph.degree()):
        raise ValueError("dual is not cubic")
    if graph.number_of_edges() != 3 * n - 6:
        raise ValueError("unexpected dual size")
    return graph, rotation, faces


def edge_order(graph: nx.Graph) -> list[tuple[int, int]]:
    """BFS order of undirected edges, each as ``(u, v)`` with the first visit."""
    root = min(graph.nodes())
    order: list[tuple[int, int]] = []
    seen: set[frozenset[int]] = set()
    starts = [root] + [v for _, v in nx.bfs_edges(graph, root)]
    for u in starts:
        for w in sorted(graph[u]):
            key = frozenset((u, w))
            if key not in seen:
                seen.add(key)
                order.append((u, w))
    if len(order) != graph.number_of_edges():
        raise ValueError("edge order missed an edge")
    return order


def rotation_edge_index(
    graph: nx.Graph, rotation: list[tuple[int, int, int]], edges: list[tuple[int, int]]
) -> list[tuple[int, int, int]]:
    """Replace each neighbour triple by the three incident edge indices."""
    index = {frozenset(e): i for i, e in enumerate(edges)}
    out: list[tuple[int, int, int]] = []
    for v, nbrs in enumerate(rotation):
        triple = tuple(index[frozenset((v, w))] for w in nbrs)
        incident = {index[frozenset((v, w))] for w in graph[v]}
        if set(triple) != incident:
            raise ValueError("rotation is not the star of the vertex")
        out.append(triple)  # type: ignore[arg-type]
    return out


def colouring_sign(col: list[int], rot_edges: list[tuple[int, int, int]]) -> int:
    """Product over vertices of the rotation sign of ``col``."""
    sign = 1
    for a, b, c in rot_edges:
        sign *= SIGN[col[a]][col[b]][col[c]]
    return sign


def walk_colourings(edges: list[tuple[int, int]], on_colouring) -> None:
    """Call ``on_colouring(col)`` for every proper labelling by ``{0,1,2}``."""
    n = 0
    for u, v in edges:
        n = max(n, u + 1, v + 1)
    used = [0] * n
    col = [0] * len(edges)

    def rec(i: int) -> None:
        if i == len(edges):
            on_colouring(col)
            return
        u, w = edges[i]
        free = 7 & ~(used[u] | used[w])
        for c in range(3):
            bit = 1 << c
            if free & bit:
                used[u] |= bit
                used[w] |= bit
                col[i] = c
                rec(i + 1)
                used[u] ^= bit
                used[w] ^= bit

    rec(0)


def tally(edges: list[tuple[int, int]], rot_edges: list[tuple[int, int, int]]) -> tuple[int, int]:
    """Return ``(positive, negative)`` colouring counts."""
    pos = 0
    neg = 0

    def on(col: list[int]) -> None:
        nonlocal pos, neg
        if colouring_sign(col, rot_edges) == 1:
            pos += 1
        else:
            neg += 1

    walk_colourings(edges, on)
    return pos, neg


def reverse_one(rot_edges: list[tuple[int, int, int]], vertex: int = 0) -> list[tuple[int, int, int]]:
    """Reverse the rotation at a single vertex."""
    out = list(rot_edges)
    a, b, c = out[vertex]
    out[vertex] = (a, c, b)
    return out


def reverse_all(rot_edges: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    """Reverse every rotation (the mirror embedding)."""
    return [(a, c, b) for a, b, c in rot_edges]


def local_lemma() -> None:
    """Check ε(α,β,γ) = σ(α,β,γ) · (-1)^{α+β+γ} on all 24 colour triples.

    σ is the inversion sign of the vertex colours in boundary order. ε is the
    inversion sign of the three Klein sums α+β, β+γ, γ+α after ``MAP``.
    """
    for a, b, c in itertools.permutations(range(4), 3):
        inversions = (a > b) + (a > c) + (b > c)
        sigma = 1 if inversions % 2 == 0 else -1
        epsilon = SIGN[MAP[a ^ b]][MAP[b ^ c]][MAP[c ^ a]]
        parity = 1 if (a + b + c) % 2 == 0 else -1
        if epsilon != sigma * parity:
            raise AssertionError((a, b, c, epsilon, sigma, parity))


def one_4_colouring(T: nx.Graph) -> list[int]:
    """Return one proper vertex colouring with colours ``{0,1,2,3}``."""
    n = T.number_of_nodes()
    nbrs = [list(T[v]) for v in range(n)]
    col = [-1] * n

    def rec(i: int) -> bool:
        if i == n:
            return True
        used = 0
        for w in nbrs[i]:
            if col[w] >= 0:
                used |= 1 << col[w]
        for c in range(4):
            if (used >> c) & 1 == 0:
                col[i] = c
                if rec(i + 1):
                    return True
                col[i] = -1
        return False

    if not rec(0):
        raise AssertionError("no proper 4-colouring")
    return col


def klein_edge_colours(
    faces: list[list[int]],
    phi: list[int],
    rotation: list[tuple[int, int, int]],
    edges: list[tuple[int, int]],
) -> list[int]:
    """Tait colours on ``edges`` induced by the vertex colouring ``phi``."""
    colour_of: dict[frozenset[int], int] = {}
    for fi, face in enumerate(faces):
        for i in range(3):
            a = face[i]
            b = face[(i + 1) % 3]
            key = frozenset((fi, rotation[fi][i]))
            colour_of[key] = MAP[phi[a] ^ phi[b]]
    return [colour_of[frozenset(e)] for e in edges]


def self_test() -> dict:
    """K4 has 6 Tait colourings and one 1-factorization; the sign table is S_3."""
    local_lemma()
    expected = {
        (0, 1, 2): 1,
        (1, 2, 0): 1,
        (2, 0, 1): 1,
        (0, 2, 1): -1,
        (1, 0, 2): -1,
        (2, 1, 0): -1,
    }
    for colours, sign in expected.items():
        if permutation_sign(colours) != sign:
            raise AssertionError((colours, sign, permutation_sign(colours)))
    k4 = nx.complete_graph(4)
    graph, rotation, faces = dual_rotation(k4)
    if graph.number_of_nodes() != 4 or not nx.is_isomorphic(graph, k4):
        raise AssertionError("dual of K4 is not K4")
    edges = edge_order(graph)
    rot_edges = rotation_edge_index(graph, rotation, edges)
    pos, neg = tally(edges, rot_edges)
    if pos + neg != 6 or pos * neg != 0:
        raise AssertionError(f"K4 signed tally {(pos, neg)}")
    # One stored colouring, checked locally against the rotation.
    sample: dict = {}

    def grab(col: list[int]) -> None:
        if sample:
            return
        local = []
        for v, (a, b, c) in enumerate(rot_edges):
            cols = (col[a], col[b], col[c])
            local.append({"vertex": v, "colours": list(cols), "sign": permutation_sign(cols)})
        sample["edges"] = [[u, v, col[i]] for i, (u, v) in enumerate(edges)]
        sample["local"] = local
        sample["product"] = colouring_sign(col, rot_edges)

    walk_colourings(edges, grab)
    product = 1
    for item in sample["local"]:
        product *= item["sign"]
    if product != sample["product"] or abs(product) != 1:
        raise AssertionError("K4 sample sign mismatch")
    if colouring_sign(sample_col_from(sample, edges), reverse_one(rot_edges)) != -product:
        raise AssertionError("reversing one K4 rotation did not negate the sign")
    phi = one_4_colouring(k4)
    induced = klein_edge_colours(faces, phi, rotation, edges)
    if colouring_sign(induced, rot_edges) != 1:
        raise AssertionError("induced K4 colouring does not have sign (-1)^4")
    return {
        "K4_tait": pos + neg,
        "K4_signed": pos - neg,
        "K4_positive": pos,
        "K4_negative": neg,
        "K4_sample": sample,
    }


def sample_col_from(sample: dict, edges: list[tuple[int, int]]) -> list[int]:
    """Rebuild a colour array from the stored edge list."""
    col = [0] * len(edges)
    for u, v, c in sample["edges"]:
        for i, (x, y) in enumerate(edges):
            if {x, y} == {u, v}:
                col[i] = c
                break
    return col


def load_d1_tait() -> dict[str, int]:
    """Tait counts already computed by D1, keyed by ``T_n_i``."""
    if not D1.exists():
        return {}
    data = json.loads(D1.read_text())
    out: dict[str, int] = {}
    for rows in data.get("graphs", {}).values():
        for row in rows:
            out[row["name"]] = row["tait"]
    return out


def orientation_audit(cache: dict) -> dict:
    """Check the descent half of the sign proof on every cached triangulation.

    For one proper 4-colouring of each ``T_n_i`` with ``n <= 11``, the product
    of the inversion signs of the face colour-triples equals ``(-1)^n``, and
    the oriented face boundaries have exactly ``3n-6`` colour descents.
    """
    t0 = time.perf_counter()
    failures = []
    checked = 0
    for n in range(4, 12):
        for i, el in enumerate(cache["graphs"][str(n)]):
            T = nx.Graph([tuple(e) for e in el])
            T.add_nodes_from(range(n))
            _graph, _rotation, faces = dual_rotation(T)
            phi = one_4_colouring(T)
            sigma = 1
            descents = 0
            for face in faces:
                cols = [phi[v] for v in face]
                inversions = (cols[0] > cols[1]) + (cols[0] > cols[2]) + (cols[1] > cols[2])
                sigma *= 1 if inversions % 2 == 0 else -1
                for j in range(3):
                    if cols[j] > cols[(j + 1) % 3]:
                        descents += 1
            checked += 1
            if sigma != (1 if n % 2 == 0 else -1) or descents != 3 * n - 6:
                failures.append(f"T_{n}_{i}")
    return {
        "range": "n<=11",
        "graphs": checked,
        "failures": failures,
        "elapsed_seconds": round(time.perf_counter() - t0, 3),
    }


def main(max_n: int = 8) -> None:
    """Enumerate signed Tait colourings through ``max_n`` and write the JSON."""
    t0 = time.perf_counter()
    sanity = self_test()
    cache = json.loads(DATA.read_text())
    d1_tait = load_d1_tait()
    out: dict = {
        "definition": (
            "sign(phi) = product over vertices v of sgn(colours of the three "
            "edges of phi in the planar rotation at v); signed count = sum_phi sign(phi)"
        ),
        "colours": [0, 1, 2],
        "command": f"{sys.executable} compute/flows/a1720_alon_tarsi.py {max_n}",
        "sanity": sanity,
        "per_n": {},
        "graphs": {},
        "mixed_sign_graphs": [],
        "checks": {
            "matches_d1_tait": True,
            "rotation_reversal_checks": True,
            "every_colouring_same_sign_within_its_graph": True,
            "one_sign_across_all_colourings": True,
            "sign_equals_minus_one_to_n": True,
            "induced_colouring_matches": True,
        },
    }
    signs_seen: set[int] = set()
    for n in range(4, max_n + 1):
        tn = time.perf_counter()
        rows = []
        for i, el in enumerate(cache["graphs"][str(n)]):
            T = nx.Graph([tuple(e) for e in el])
            T.add_nodes_from(range(n))
            graph, rotation, faces = dual_rotation(T)
            if len(rotation) % 2 != 0:
                raise AssertionError("dual vertex count is odd; sign would depend on the mirror")
            edges = edge_order(graph)
            rot_edges = rotation_edge_index(graph, rotation, edges)
            pos, neg = tally(edges, rot_edges)
            tait = pos + neg
            signed = pos - neg
            name = f"T_{n}_{i}"
            if name in d1_tait and d1_tait[name] != tait:
                out["checks"]["matches_d1_tait"] = False
                raise AssertionError(f"{name}: tait {tait} != D1 {d1_tait[name]}")
            if tait % 6 != 0 or tait == 0:
                raise AssertionError(f"{name}: unexpected tait count {tait}")
            # Re-enumerate under a reversed rotation. One vertex must negate the
            # signed count; reversing every vertex must preserve it (V even).
            # These reruns are the check that the sign uses the rotation.
            if n <= 8:
                p1, n1 = tally(edges, reverse_one(rot_edges))
                pa, na = tally(edges, reverse_all(rot_edges))
                if (p1 - n1) != -signed or (pa - na) != signed:
                    out["checks"]["rotation_reversal_checks"] = False
                    raise AssertionError(f"{name}: rotation reversal failed")
            same = pos == 0 or neg == 0
            if not same:
                out["checks"]["every_colouring_same_sign_within_its_graph"] = False
                out["mixed_sign_graphs"].append(name)
            common = 0 if not same else (1 if pos else -1)
            predicted = 1 if n % 2 == 0 else -1
            phi = one_4_colouring(T)
            induced_col = klein_edge_colours(faces, phi, rotation, edges)
            induced = colouring_sign(induced_col, rot_edges)
            if induced != predicted or common != predicted or signed != predicted * tait:
                out["checks"]["sign_equals_minus_one_to_n"] = False
                out["checks"]["induced_colouring_matches"] = False
                raise AssertionError(
                    f"{name}: tait {tait} signed {signed} common {common} induced {induced}"
                )
            if same:
                signs_seen.add(common)
            row = {
                "name": name,
                "dual_vertices": graph.number_of_nodes(),
                "tait": tait,
                "signed": signed,
                "positive": pos,
                "negative": neg,
                "all_same_sign": same,
                "common_sign": common,
                "induced_sign": induced,
                "factorizations": tait // 6,
            }
            rows.append(row)
            print(
                f"{name}: tait={tait} signed={signed} same={same}",
                flush=True,
            )
        elapsed_n = time.perf_counter() - tn
        commons = {r["common_sign"] for r in rows}
        out["graphs"][str(n)] = rows
        out["per_n"][str(n)] = {
            "count": len(rows),
            "all_same_sign_within_each_graph": all(r["all_same_sign"] for r in rows),
            "common_signs": sorted(commons),
            "tait_min": min(r["tait"] for r in rows),
            "tait_max": max(r["tait"] for r in rows),
            "signed_min": min(r["signed"] for r in rows),
            "signed_max": max(r["signed"] for r in rows),
            "abs_signed_equals_tait": all(abs(r["signed"]) == r["tait"] for r in rows),
            "elapsed_seconds": round(elapsed_n, 3),
        }
        print(
            f"n={n}: {len(rows)} graphs, signs {sorted(commons)}, {elapsed_n:.3f}s",
            flush=True,
        )
    out["checks"]["one_sign_across_all_colourings"] = signs_seen == {1} or signs_seen == {-1}
    out["sign_identity"] = "every Tait colouring of the dual has sign (-1)^n"
    out["signs_seen"] = sorted(signs_seen)
    out["orientation_audit"] = orientation_audit(cache)
    out["elapsed_seconds"] = round(time.perf_counter() - t0, 3)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1) + "\n")
    print(
        f"signs_seen={sorted(signs_seen)} mixed={out['mixed_sign_graphs']} "
        f"total {out['elapsed_seconds']}s wrote {OUT}",
        flush=True,
    )


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 8)
