"""Group D2 (Agent 1720): Penrose sign-sum versus the Tait count.

``compute/topology/penrose_eval.py`` defines ``penrose_eval`` as
``count_tait_colourings``. This script computes a different integer on the
plane dual of each cached triangulation.

Colours are ``{0, 1, 2}``. If ``(e, f, g)`` is the cyclic order of the three
edges at a vertex, ``ε(i, j, k)`` is the sign of the permutation
``(0, 1, 2) -> (i, j, k)``, and ``ε = 0`` when the three labels are not all
different. The Penrose sign-sum of a rotation system ``ρ`` is

    Pen_ε(G, ρ) = sum_{ℓ : E -> {0,1,2}} prod_v ε(ℓ(e_v), ℓ(f_v), ℓ(g_v)).

The Tait count is the same sum with ``|ε|`` in place of ``ε``. On a cubic
graph every improper labelling has a zero factor, so the support of either
sum is the set of Tait colourings; only the signs can make the two integers
differ.

``ρ`` for a dual comes from ``nx.check_planarity`` on the triangulation:
dual vertices are the primal faces, in the order the faces are discovered,
and the cyclic order at a dual vertex is the facial walk
(``PlanarEmbedding.traverse_face``, face on the right). A cubic graph has
even order, so reversing every cyclic order multiplies the sign-sum by
``(+1)`` and the value does not depend on that global choice.

The search fixes colours ``0, 1, 2`` on the three edges at vertex ``0`` and
multiplies by ``6``. That is valid because ``|V|`` is even, so every global
relabelling of the colours preserves the product of the local signs, and the
action on Tait colourings is free.

Usage::

    .venv/bin/python compute/topology/a1720_penrose_state_sum.py
"""

from __future__ import annotations

import itertools
import json
import time
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "compute" / "data" / "triangulations_n4_11.json"
OUT = ROOT / "backgroundMaterial" / "agent1720" / "groups" / "D2_results.json"
D1 = ROOT / "backgroundMaterial" / "agent1720" / "groups" / "D1_results.json"

# Required census. Higher n is continued only while the deadline allows.
REQUIRED_MAX_N = 8
EXTRA_MAX_N = 11
DEADLINE_S = 540.0

Edge = tuple[int, int]
Triple = tuple[int, int, int]


def levi(i: int, j: int, k: int) -> int:
    """Levi-Civita symbol ``ε_ijk`` on colours ``{0, 1, 2}``."""
    if i == j or j == k or i == k:
        return 0
    sign = 1
    if i > j:
        sign = -sign
    if i > k:
        sign = -sign
    if j > k:
        sign = -sign
    return sign


def plane_dual_rotation(T: nx.Graph) -> tuple[list[Edge], list[Triple]]:
    """Plane dual of a triangulation, with the facial cyclic order at each vertex.

    Returns ``(edges, rotation)`` where ``rotation[v]`` is a cyclic order of
    the three edge indices incident with dual vertex ``v``.
    """
    n = T.number_of_nodes()
    ok, emb = nx.check_planarity(T)
    if not ok:
        raise ValueError("triangulation is not planar")
    face_of: dict[tuple[int, int], int] = {}
    faces: list[list[int]] = []
    for u, v in emb.edges():
        if (u, v) in face_of:
            continue
        marked: set[tuple[int, int]] = set()
        face = emb.traverse_face(u, v, mark_half_edges=marked)
        for he in marked:
            face_of[he] = len(faces)
        faces.append(list(face))
    m = T.number_of_edges()
    if len(faces) != 2 * n - 4 or any(len(f) != 3 for f in faces):
        raise ValueError("not a triangulation")
    if n - m + len(faces) != 2:
        raise ValueError("Euler's formula fails")
    edges: list[Edge] = []
    index: dict[frozenset[int], int] = {}
    for u, v in T.edges():
        a, b = face_of[(u, v)], face_of[(v, u)]
        if a == b:
            raise ValueError("dual loop")
        key = frozenset((u, v))
        index[key] = len(edges)
        edges.append((a, b))
    rotation: list[Triple] = []
    seen = [0] * len(edges)
    for face in faces:
        trip = []
        for i in range(3):
            ei = index[frozenset((face[i], face[(i + 1) % 3]))]
            trip.append(ei)
            seen[ei] += 1
        if len(set(trip)) != 3:
            raise ValueError("face does not give three dual edges")
        rotation.append((trip[0], trip[1], trip[2]))
    if any(c != 2 for c in seen):
        raise ValueError("dual edge is not in exactly two rotations")
    if len(set(map(frozenset, edges))) != len(edges):
        raise ValueError("dual has parallel edges")
    return edges, rotation


def tait_and_sign(edges: list[Edge], rotation: list[Triple]) -> tuple[int, int]:
    """Return ``(Tait count, Penrose sign-sum)`` for a cubic rotation system.

    Both numbers count the same proper edge-3-colourings. The sign-sum weights
    each colouring by ``prod_v ε``.
    """
    n = len(rotation)
    if n % 2 != 0:
        raise ValueError("cubic order is even; refusing an odd vertex set")
    m = len(edges)
    adj: list[list[int]] = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        adj[u].append(i)
        adj[v].append(i)
    if any(len(a) != 3 for a in adj):
        raise ValueError("graph is not cubic")
    for v, trip in enumerate(rotation):
        if set(trip) != set(adj[v]):
            raise ValueError("rotation is not the incident edges")

    order: list[int] = []
    seen_e: set[int] = set()
    seen_v: set[int] = {0}
    queue = [0]
    while queue:
        u = queue.pop()
        for ei in adj[u]:
            if ei in seen_e:
                continue
            seen_e.add(ei)
            order.append(ei)
            a, b = edges[ei]
            w = b if a == u else a
            if w not in seen_v:
                seen_v.add(w)
                queue.append(w)
    if len(order) != m or set(order[:3]) != set(adj[0]):
        raise ValueError("edge search did not start with the root star")

    colour = [-1] * m
    used = [0] * n
    for c, ei in enumerate(order[:3]):
        colour[ei] = c
        u, v = edges[ei]
        used[u] |= 1 << c
        used[v] |= 1 << c
    rest = order[3:]
    tait_rep = 0
    sign_rep = 0

    def rec(i: int) -> None:
        nonlocal tait_rep, sign_rep
        if i == len(rest):
            sg = 1
            for a, b, c in rotation:
                sg *= levi(colour[a], colour[b], colour[c])
            tait_rep += 1
            sign_rep += sg
            return
        ei = rest[i]
        u, v = edges[ei]
        free = 7 & ~(used[u] | used[v])
        for c in range(3):
            bit = 1 << c
            if free & bit:
                colour[ei] = c
                used[u] |= bit
                used[v] |= bit
                rec(i + 1)
                used[u] &= ~bit
                used[v] &= ~bit
                colour[ei] = -1

    rec(0)
    return 6 * tait_rep, 6 * sign_rep


def brute_sign(edges: list[Edge], rotation: list[Triple]) -> tuple[int, int]:
    """Sign-sum and Tait count by enumerating every map ``E -> {0,1,2}``."""
    m = len(edges)
    tait = 0
    signed = 0
    for colouring in itertools.product(range(3), repeat=m):
        weight = 1
        for a, b, c in rotation:
            weight *= levi(colouring[a], colouring[b], colouring[c])
            if weight == 0:
                break
        if weight == 0:
            continue
        tait += 1
        signed += weight
    return tait, signed


def split(tait: int, signed: int) -> tuple[int, int]:
    """Numbers of Tait colourings of sign ``+1`` and of sign ``-1``."""
    if (tait + signed) % 2 or abs(signed) > tait:
        raise ValueError(f"inconsistent pair tait={tait}, signed={signed}")
    return (tait + signed) // 2, (tait - signed) // 2


def k4_rotation_scan() -> dict:
    """Every cyclic-order choice on ``K_4``. Planarity of ``ρ`` is not assumed."""
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    index = {frozenset(e): i for i, e in enumerate(edges)}
    nbrs = {v: sorted(w for u, w in edges if u == v) + sorted(u for u, w in edges if w == v) for v in range(4)}
    # each vertex has the sorted cyclic order or its reverse: 2^4 = 16 systems
    rows = []
    for bits in itertools.product((0, 1), repeat=4):
        rotation: list[Triple] = []
        for v, bit in enumerate(bits):
            order = nbrs[v] if bit == 0 else list(reversed(nbrs[v]))
            rotation.append(tuple(index[frozenset((v, w))] for w in order))
        tait, signed = tait_and_sign(edges, list(rotation))  # type: ignore[arg-type]
        rows.append({"bits": "".join(map(str, bits)), "tait": tait, "signed": signed})
    T = nx.complete_graph(4)
    _e, emb_rot = plane_dual_rotation(T)
    # K4 is isomorphic to its dual; compare values, not the edge indexing.
    emb_tait, emb_signed = tait_and_sign(_e, emb_rot)
    brute_t, brute_s = brute_sign(_e, emb_rot)
    return {
        "embedding_tait": emb_tait,
        "embedding_signed": emb_signed,
        "brute_matches_embedding": brute_t == emb_tait and brute_s == emb_signed,
        "scan": rows,
        "n_signed_eq_tait": sum(1 for r in rows if r["signed"] == r["tait"] == 6),
        "n_signed_eq_minus_tait": sum(1 for r in rows if r["signed"] == -6 and r["tait"] == 6),
        "n_cancelled": sum(1 for r in rows if r["tait"] == 6 and r["signed"] == 0),
    }


def k33_control() -> dict:
    """``K_{3,3}`` has Tait colourings. Some rotation systems cancel in the sign-sum."""
    parts = (range(3), range(3, 6))
    edges = [(u, v) for u in parts[0] for v in parts[1]]
    index = {frozenset(e): i for i, e in enumerate(edges)}
    nbrs = {v: [w for a, b in edges if a == v for w in (b,)] + [u for a, b in edges if b == v for u in (a,)] for v in range(6)}
    cancel = None
    n_cancel = 0
    n_systems = 0
    for bits in itertools.product((0, 1), repeat=6):
        rotation = []
        for v, bit in enumerate(bits):
            order = nbrs[v] if bit == 0 else list(reversed(nbrs[v]))
            rotation.append(tuple(index[frozenset((v, w))] for w in order))
        tait, signed = tait_and_sign(edges, rotation)
        n_systems += 1
        if signed == 0:
            n_cancel += 1
            if cancel is None:
                cancel = {"bits": "".join(map(str, bits)), "tait": tait, "signed": signed}
    if cancel is None:
        raise RuntimeError("no cancelling rotation on K33")
    return {"systems": n_systems, "n_cancelled": n_cancel, "example": cancel}


def petersen_control() -> dict:
    """Petersen has no Tait colouring, so both sums are zero for every rotation."""
    G = nx.petersen_graph()
    edges = [(u, v) for u, v in G.edges()]
    index = {frozenset(e): i for i, e in enumerate(edges)}
    rotation = []
    for v in range(G.order()):
        order = sorted(G.neighbors(v))
        rotation.append(tuple(index[frozenset((v, w))] for w in order))
    tait, signed = tait_and_sign(edges, rotation)
    return {"tait": tait, "signed": signed, "planar": bool(nx.check_planarity(G)[0])}


def stacking_ratio() -> int:
    """Sign ratio for stacking a vertex into a clockwise triangle.

    Clockwise faces ``(a,b,v), (b,c,v), (c,a,v)`` replace clockwise face
    ``(a,b,c)``. The ratio of the products of ``σ`` is ``-1`` for every
    proper colouring of the four vertices by ``Z_2^2``.
    """

    def sig(x: int, y: int, z: int) -> int:
        return levi(x ^ y, y ^ z, z ^ x)

    # (a,b,c) clockwise, v inside: these four walks all have negative planar area.
    a, b, c, v = (0.0, 2.0), (2.0, -1.0), (-2.0, -1.0), (0.0, 0.0)

    def area(o: tuple[float, float], p: tuple[float, float], q: tuple[float, float]) -> float:
        return (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])

    if not all(area(*t) < 0 for t in ((a, b, c), (a, b, v), (b, c, v), (c, a, v))):
        raise RuntimeError("stacking walks are not clockwise")
    ratios = set()
    for cols in itertools.permutations(range(4)):
        ca, cb, cc, cv = cols
        num = sig(ca, cb, cv) * sig(cb, cc, cv) * sig(cc, ca, cv)
        den = sig(ca, cb, cc)
        ratios.add(num // den)
    if ratios != {-1}:
        raise RuntimeError(f"stacking ratios {ratios}")
    return -1


def k4_colouring_signs() -> dict:
    """Product of face signs for every proper 4-colouring of ``K_4``.

    Edge colours are differences in ``Z_2^2 = {0,1,2,3}`` and ``ε`` is the
    sign of that triple as a permutation of ``(1,2,3)``. Every one of the
    ``4! = 24`` colourings has product ``+1``.
    """
    T = nx.complete_graph(4)
    _edges, rotation = plane_dual_rotation(T)
    # Recover clockwise primal faces from the same embedding used for the dual.
    ok, emb = nx.check_planarity(T)
    if not ok:
        raise RuntimeError("K4 is planar")
    faces: list[tuple[int, int, int]] = []
    seen: set[tuple[int, int]] = set()
    for u, v in emb.edges():
        if (u, v) in seen:
            continue
        marked: set[tuple[int, int]] = set()
        face = emb.traverse_face(u, v, mark_half_edges=marked)
        for he in marked:
            seen.add(he)
        faces.append((face[0], face[1], face[2]))
    products = []
    for cols in itertools.permutations(range(4)):
        colour = dict(enumerate(cols))
        prod = 1
        for a, b, c in faces:
            x, y, z = colour[a], colour[b], colour[c]
            prod *= levi(x ^ y, y ^ z, z ^ x)
        products.append(prod)
    if products != [1] * 24:
        raise RuntimeError(f"K4 colouring signs {products}")
    # ``rotation`` is retained so a refactor that drops the dual cannot
    # silently skip the embedding; the face walk above is the same embedding.
    if len(rotation) != 4:
        raise RuntimeError("K4 dual should have 4 vertices")
    return {"colourings": 24, "all_products": 1}


def library_planarity() -> list[dict]:
    """Compare ``build_graph_library`` planarity flags with ``nx.check_planarity``."""
    import importlib.util

    path = ROOT / "compute" / "topology" / "penrose_eval.py"
    spec = importlib.util.spec_from_file_location("penrose_eval_audit", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load penrose_eval.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    cube = nx.cubical_graph()
    rows = []
    for name, graph, flag in mod.build_graph_library():
        H = nx.Graph()
        H.add_nodes_from(range(graph["n"]))
        H.add_edges_from(graph["edges"])
        degrees = [d for _, d in H.degree()]
        cubic = bool(degrees) and all(d == 3 for d in degrees) and H.order() == graph["n"]
        planar = bool(nx.check_planarity(H)[0]) if H.number_of_nodes() else False
        rows.append({
            "name": name,
            "vertices": graph["n"],
            "edges": H.number_of_edges(),
            "cubic": cubic,
            "flag_planar": flag,
            "actually_planar": planar,
            "flag_matches": flag == planar,
            "isomorphic_to_cube": H.order() == 8 and nx.is_isomorphic(H, cube),
        })
    return rows


def load_d1_tait() -> dict[tuple[int, int], int]:
    """Gated D1 Tait counts, used only as a checksum of this script's counter."""
    if not D1.exists():
        return {}
    raw = json.loads(D1.read_text())
    out = {}
    for n, rows in raw.get("graphs", {}).items():
        for row in rows:
            # name T_{n}_{i}
            parts = row["name"].split("_")
            out[(int(parts[1]), int(parts[2]))] = int(row["tait"])
    return out


def main() -> dict:
    """Compare the sign-sum with the Tait count. Stop at the deadline."""
    t0 = time.perf_counter()
    deadline = t0 + DEADLINE_S
    data = json.loads(DATA.read_text())
    d1 = load_d1_tait()
    out: dict = {
        "required_max_n": REQUIRED_MAX_N,
        "deadline_seconds": DEADLINE_S,
        "stopped_early": False,
        "controls": {},
        "per_n": {},
        "graphs": {},
        "mismatches": [],
    }
    print("controls", flush=True)
    k4 = k4_rotation_scan()
    k33 = k33_control()
    pet = petersen_control()
    out["controls"] = {"K4": k4, "K33": k33, "Petersen": pet}
    if not (k4["embedding_tait"] == k4["embedding_signed"] == 6 and k4["brute_matches_embedding"]):
        raise RuntimeError(f"K4 control failed: {k4}")
    if pet["tait"] != 0 or pet["signed"] != 0:
        raise RuntimeError(f"Petersen control failed: {pet}")
    if k33["example"]["tait"] != 12 or k33["example"]["signed"] != 0:
        raise RuntimeError(f"K33 control failed: {k33}")
    print(
        f"  K4 embedding {k4['embedding_signed']}/{k4['embedding_tait']}; "
        f"of 16 rotations, cancel {k4['n_cancelled']}, "
        f"+6 {k4['n_signed_eq_tait']}, -6 {k4['n_signed_eq_minus_tait']}",
        flush=True,
    )
    print(
        f"  K33 systems {k33['systems']}, cancelled {k33['n_cancelled']}, "
        f"example bits {k33['example']['bits']} signed {k33['example']['signed']} tait {k33['example']['tait']}",
        flush=True,
    )
    print(f"  Petersen tait {pet['tait']} signed {pet['signed']}", flush=True)

    # One-vertex reversal must negate the sum. |V| even does not protect a partial reversal.
    T4 = nx.Graph()
    T4.add_nodes_from(range(4))
    T4.add_edges_from(data["graphs"]["4"][0])
    e4, r4 = plane_dual_rotation(T4)
    t4, s4 = tait_and_sign(e4, r4)
    flipped = [(r4[0][0], r4[0][2], r4[0][1])] + list(r4[1:])
    t4b, s4b = tait_and_sign(e4, flipped)
    if not (t4b == t4 and s4b == -s4 and s4 == t4 == 6):
        raise RuntimeError(f"reversal test failed: {(t4, s4, t4b, s4b)}")
    out["controls"]["one_vertex_reversal_negates"] = True
    out["controls"]["stacking_ratio"] = stacking_ratio()
    out["controls"]["K4_colouring_signs"] = k4_colouring_signs()
    print(f"  stacking ratio {out['controls']['stacking_ratio']}; K4 colourings all +1", flush=True)

    for n in range(4, EXTRA_MAX_N + 1):
        if time.perf_counter() > deadline:
            out["stopped_early"] = True
            print(f"stop before n={n}: deadline", flush=True)
            break
        tn = time.perf_counter()
        rows = []
        graphs_n = data["graphs"][str(n)]
        for i, el in enumerate(graphs_n):
            if time.perf_counter() > deadline:
                out["stopped_early"] = True
                print(f"stop during n={n} at index {i}: deadline", flush=True)
                break
            T = nx.Graph()
            T.add_nodes_from(range(n))
            T.add_edges_from(tuple(e) for e in el)
            edges, rotation = plane_dual_rotation(T)
            tait, signed = tait_and_sign(edges, rotation)
            if n <= 5:
                bt, bs = brute_sign(edges, rotation)
                if (bt, bs) != (tait, signed):
                    raise RuntimeError(f"brute mismatch T_{n}_{i}: {(bt, bs)} != {(tait, signed)}")
            pos, neg = split(tait, signed)
            predicted = ((-1) ** n) * tait
            row = {
                "name": f"T_{n}_{i}",
                "dual_vertices": len(rotation),
                "dual_edges": len(edges),
                "tait": tait,
                "signed": signed,
                "positive": pos,
                "negative": neg,
                "sign": (signed // tait) if tait else None,
                "matches_sign_formula": signed == predicted,
            }
            checksum = d1.get((n, i))
            if checksum is not None:
                row["d1_tait"] = checksum
                row["d1_match"] = checksum == tait
                if checksum != tait:
                    out["mismatches"].append({"name": row["name"], "why": "d1", "tait": tait, "d1": checksum})
            if signed != predicted:
                out["mismatches"].append(row)
            rows.append(row)
        elapsed_n = time.perf_counter() - tn
        if not rows:
            break
        out["graphs"][str(n)] = rows
        out["per_n"][str(n)] = {
            "count": len(rows),
            "complete": len(rows) == len(graphs_n),
            "all_match_sign_formula": all(r["matches_sign_formula"] for r in rows),
            "common_sign": rows[0]["sign"],
            "tait_min": min(r["tait"] for r in rows),
            "tait_max": max(r["tait"] for r in rows),
            "signed_min": min(r["signed"] for r in rows),
            "signed_max": max(r["signed"] for r in rows),
            "elapsed_seconds": round(elapsed_n, 4),
        }
        summary = out["per_n"][str(n)]
        print(
            f"n={n}: {summary['count']}/{len(graphs_n)} "
            f"signed=(-1)^n*tait {summary['all_match_sign_formula']} "
            f"sign {summary['common_sign']} "
            f"tait {summary['tait_min']}..{summary['tait_max']} "
            f"{elapsed_n:.3f}s",
            flush=True,
        )
        if out["stopped_early"]:
            break
        if n == REQUIRED_MAX_N and time.perf_counter() - t0 > DEADLINE_S * 0.5:
            # Keep half the budget in reserve only if the required range was already slow.
            pass

    out["library_planarity"] = library_planarity()
    out["elapsed_seconds"] = round(time.perf_counter() - t0, 4)
    out["command"] = ".venv/bin/python compute/topology/a1720_penrose_state_sum.py"
    bad_flags = [r for r in out["library_planarity"] if not r["flag_matches"]]
    print(f"planarity-flag mismatches: {[r['name'] for r in bad_flags]}", flush=True)
    print(
        f"mismatches {len(out['mismatches'])}; total {out['elapsed_seconds']}s; writing {OUT}",
        flush=True,
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    main()
