"""Speculative inquiry: Kempe preparation of a degree-five vacancy slide.

Reads the published mass-macro table and re-enumerates the six graphs that contain
a mass failure. It does not search past those graphs, does not touch orders beyond
the published table, and does not assign a navigator status.

A second half builds two symmetric triangulations only to measure distances between
degree-five vertices. No colourings of those graphs are enumerated.
"""

import json
import math
from collections import deque

from mass_core import FIXTURES, parse_ascii, validate_triangulation

OUT = FIXTURES / "longtable" / "inquiry-slide.json"


def neighbour_type(rot, r):
    degs = sorted(len(rot[w]) for w in rot[r])
    return {
        "degrees": degs,
        "n5": sum(d == 5 for d in degs),
        "n6": sum(d == 6 for d in degs),
        "n7plus": sum(d >= 7 for d in degs),
    }


def type_key(info):
    return (info["n5"], info["n6"], info["n7plus"])


def colour_view(rot, s, i):
    col = dict(zip(s.V, s.C[i]))
    boundary = list(rot[s.r])
    cols = [col[v] for v in boundary]
    counts = {a: cols.count(a) for a in set(cols)}
    repeated = [a for a, k in counts.items() if k >= 2]
    singletons = [v for v in boundary if counts[col[v]] == 1]
    gap = None
    if len(repeated) == 1:
        pos = [j for j, v in enumerate(boundary) if col[v] == repeated[0]]
        if len(pos) == 2:
            gap = min((pos[1] - pos[0]) % 5, (pos[0] - pos[1]) % 5)
    d5 = [v for v in boundary if len(rot[v]) == 5]
    if not d5:
        locked = None
    else:
        locked = all(counts[col[v]] >= 2 for v in d5)
    return col, boundary, singletons, gap, d5, locked


def slide_returns(rot, r, col, x):
    """After the singleton slide r -> x, which other degree-five vertices are singleton colours on N(x)?"""
    new = dict(col)
    new[r] = col[x]
    boundary = rot[x]
    cols = [new[v] for v in boundary]
    counts = {a: cols.count(a) for a in set(cols)}
    back = counts[new[r]] == 1
    onward = [v for v in boundary if v != r and len(rot[v]) == 5 and counts[new[v]] == 1]
    return back, onward


def hubs_of(rot, s, i):
    boundary = set(rot[s.r])
    found = []
    for _pair, comp, _t in s.info[i]["moves"]:
        if len(comp) != 2:
            continue
        exterior = [v for v in comp if v not in boundary]
        if len(exterior) == 1 and any(v in boundary for v in comp):
            found.append(exterior[0])
    return sorted(set(found))


def classify_root(rot, s, failing):
    from mass_core import RootState  # local import keeps the module import light for geometry-only use
    assert isinstance(s, RootState)
    rows = []
    for i, info in enumerate(s.info):
        if info["p"] != 1:
            continue
        col, _boundary, singletons, gap, d5, locked = colour_view(rot, s, i)
        has_d5_slide = any(len(rot[v]) == 5 for v in singletons)

        def unlocked(j):
            _c, _b, sings, _g, _d, lock = colour_view(rot, s, j)
            return any(len(rot[v]) == 5 for v in sings), lock

        one = [t for _p, _k, t in info["moves"]]
        two = []
        seen = set(one)
        seen.add(i)
        for t in one:
            for _p, _k, u in s.info[t]["moves"]:
                if u not in seen:
                    seen.add(u)
                    two.append(u)
        k1 = any(unlocked(t)[0] for t in one)
        k2 = any(unlocked(u)[0] for u in two)
        stuck2 = s.descent(i, 2) is not None
        returns = []
        if stuck2:
            for x in singletons:
                back, onward = slide_returns(rot, s.r, col, x)
                returns.append({
                    "to": x,
                    "degree": len(rot[x]),
                    "slides_back": back,
                    "other_degree_five": onward,
                })
        rows.append({
            "stuck2": stuck2,
            "gap": gap,
            "locked": locked,
            "d5_neighbours": len(d5),
            "has_d5_slide": has_d5_slide,
            "kempe1_unlocks": k1,
            "kempe2_unlocks": k2,
            "q": info["q"],
            "hubs": hubs_of(rot, s, i) if stuck2 else [],
            "returns": returns,
        })
    stuck = [row for row in rows if row["stuck2"]]
    def count(pred):
        return sum(1 for row in rows if pred(row))
    return {
        "root": s.r,
        "mass_fails": failing,
        "type": neighbour_type(rot, s.r),
        "orbits": len(s.C),
        "non_target": len(rows),
        "two_swap_stuck": len(stuck),
        "locked_non_target": count(lambda row: row["locked"] is True),
        "isolated_non_target": count(lambda row: row["locked"] is None),
        "open_slide_non_target": count(lambda row: row["has_d5_slide"]),
        "stuck_and_open_slide": sum(1 for row in stuck if row["has_d5_slide"]),
        "stuck_and_kempe1_unlocks": sum(1 for row in stuck if row["kempe1_unlocks"]),
        "stuck_and_kempe2_unlocks": sum(1 for row in stuck if row["kempe2_unlocks"]),
        "stuck_gaps": sorted({row["gap"] for row in stuck}),
        "stuck_hubs": sorted({h for row in stuck for h in row["hubs"]}),
        "stuck_return_degree_five": sorted({v for row in stuck for step in row["returns"] for v in step["other_degree_five"]}),
        "stuck_landings": sorted({(step["to"], step["degree"]) for row in stuck for step in row["returns"]}),
    }


def census(table):
    buckets = {}
    failing_graphs = []
    for order in table["orders"]:
        for graph in order["graphs_checked"]:
            rot = parse_ascii(graph["ascii"])
            failing = set(graph["failing_roots"])
            if failing:
                failing_graphs.append((order["order"], graph["graph_index"], graph["ascii"], failing))
            for root in graph["degree_five_roots"]:
                info = neighbour_type(rot, root)
                key = type_key(info) + (("fail",) if root in failing else ("pass",))
                buckets[key] = buckets.get(key, 0) + 1
    summary = []
    types = sorted({key[:3] for key in buckets})
    for n5, n6, n7 in types:
        summary.append({
            "type": [n5, n6, n7],
            "pass": buckets.get((n5, n6, n7, "pass"), 0),
            "fail": buckets.get((n5, n6, n7, "fail"), 0),
        })
    return summary, failing_graphs


def probe(failing_graphs):
    from mass_core import RootState
    graphs = []
    for order, index, ascii_line, failing in failing_graphs:
        rot = parse_ascii(ascii_line)
        roots = []
        for root in [v for v, ns in enumerate(rot) if len(ns) == 5]:
            state = RootState(rot, root)
            roots.append(classify_root(rot, state, root in failing))
            print(f"  {order}:{index} root {root} stuck {roots[-1]['two_swap_stuck']}"
                  f" open {roots[-1]['stuck_and_open_slide']}"
                  f" kempe1 {roots[-1]['stuck_and_kempe1_unlocks']}", flush=True)
        graphs.append({"order": order, "graph_index": index, "roots": roots})
    return graphs


def dist_histogram(rot, sources):
    hist = {}
    for src in sources:
        seen = {src: 0}
        queue = deque([src])
        while queue:
            v = queue.popleft()
            for w in rot[v]:
                if w not in seen:
                    seen[w] = seen[v] + 1
                    queue.append(w)
        for dst in sources:
            if dst <= src:
                continue
            d = seen[dst]
            hist[d] = hist.get(d, 0) + 1
    return hist


def angular_rotation(verts, adj):
    def sub(a, b):
        return tuple(a[i] - b[i] for i in range(3))

    def dot(a, b):
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

    def cross(a, b):
        return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])

    rot = []
    for v, ns in enumerate(adj):
        normal = verts[v]
        base = sub(verts[ns[0]], verts[v])
        scale = dot(base, normal) / dot(normal, normal)
        tangent = tuple(base[i] - scale * normal[i] for i in range(3))
        bitangent = cross(normal, tangent)

        def angle(u):
            step = sub(verts[u], verts[v])
            scale_u = dot(step, normal) / dot(normal, normal)
            flat = tuple(step[i] - scale_u * normal[i] for i in range(3))
            return math.atan2(dot(flat, bitangent), dot(flat, tangent))

        rot.append(sorted(ns, key=angle))
    return rot


def graph_from_triangles(verts, triangles):
    adj = [set() for _ in verts]
    for a, b, c in triangles:
        for u, v in ((a, b), (b, c), (c, a)):
            adj[u].add(v)
            adj[v].add(u)
    adj = [sorted(ns) for ns in adj]
    rot = angular_rotation(verts, adj)
    try:
        validate_triangulation(rot)
    except AssertionError:
        rot = [list(reversed(ns)) for ns in rot]
        validate_triangulation(rot)
    return rot


def icosahedron():
    phi = (1 + 5 ** 0.5) / 2
    verts = []
    for i in range(3):
        for a in (-1.0, 1.0):
            for b in (-phi, phi):
                point = [0.0, 0.0, 0.0]
                point[i] = a
                point[(i + 1) % 3] = b
                verts.append(tuple(point))
    def dist2(i, j):
        return sum((verts[i][k] - verts[j][k]) ** 2 for k in range(3))
    edge = min(dist2(i, j) for i in range(12) for j in range(i + 1, 12))
    adj = [[] for _ in range(12)]
    for i in range(12):
        for j in range(12):
            if i != j and abs(dist2(i, j) - edge) < 1e-6:
                adj[i].append(j)
    return verts, angular_rotation(verts, adj)


def faces_of(rot):
    seen, out = set(), []
    for v, ns in enumerate(rot):
        for w in ns:
            if (v, w) in seen:
                continue
            face, dart = [], (v, w)
            while dart not in seen:
                seen.add(dart)
                face.append(dart[0])
                a, b = dart
                dart = (b, rot[b][(rot[b].index(a) + 1) % len(rot[b])])
            out.append(face)
    return out


def pentakis_dodecahedron(verts, rot):
    face_list = faces_of(rot)
    index = {frozenset(face): i for i, face in enumerate(face_list)}
    dual = [tuple(sum(verts[v][k] for v in face) / 3 for k in range(3)) for face in face_list]
    apex0 = len(dual)
    new_verts = dual + list(verts)
    triangles = []
    for v, ns in enumerate(rot):
        incident = []
        for w in ns:
            third = rot[w][(rot[w].index(v) + 1) % len(rot[w])]
            incident.append(index[frozenset((v, w, third))])
        apex = apex0 + v
        for i, face_id in enumerate(incident):
            triangles.append((apex, face_id, incident[(i + 1) % len(incident)]))
    return graph_from_triangles(new_verts, triangles), apex0


def geodesic_icosahedron(verts, rot):
    face_list = faces_of(rot)
    new_verts = list(verts)
    mid = {}

    def midpoint(a, b):
        key = (min(a, b), max(a, b))
        if key not in mid:
            mid[key] = len(new_verts)
            new_verts.append(tuple((verts[a][k] + verts[b][k]) / 2 for k in range(3)))
        return mid[key]

    triangles = []
    for a, b, c in face_list:
        ab, bc, ca = midpoint(a, b), midpoint(b, c), midpoint(c, a)
        triangles.extend(((a, ab, ca), (b, bc, ab), (c, ca, bc), (ab, bc, ca)))
    return graph_from_triangles(new_verts, triangles)


def geometry_report():
    verts, rot = icosahedron()
    validate_triangulation(rot)
    pentakis, apex0 = pentakis_dodecahedron(verts, rot)
    geodesic = geodesic_icosahedron(verts, rot)
    reports = []
    for name, graph, sources in (
        ("pentakis dodecahedron", pentakis, list(range(apex0, len(pentakis)))),
        ("frequency-2 icosahedron", geodesic, [v for v, ns in enumerate(geodesic) if len(ns) == 5]),
    ):
        types = {}
        for root in sources:
            key = tuple(type_key(neighbour_type(graph, root)))
            types[str(list(key))] = types.get(str(list(key)), 0) + 1
        reports.append({
            "name": name,
            "vertices": len(graph),
            "degree_five": len(sources),
            "degree_histogram": {
                str(d): sum(1 for ns in graph if len(ns) == d)
                for d in sorted({len(ns) for ns in graph})
            },
            "neighbour_types_of_degree_five": types,
            "distances_between_degree_five": {str(k): v for k, v in sorted(dist_histogram(graph, sources).items())},
        })
    return reports


def escape_audit(table, failing_graphs):
    """A stuck colouring escapes if a vacancy path of length at most two reaches a descending orbit at a passing root."""
    from mass_core import RootState, canon
    memo = {}

    def orbits(rot, root):
        if root not in memo:
            state = RootState(rot, root)
            stuck, descend, target = set(), set(), set()
            for i, info in enumerate(state.info):
                colouring = state.C[i]
                if info["p"] == 0:
                    target.add(colouring)
                elif state.descent(i, 2) is not None:
                    stuck.add(colouring)
                else:
                    descend.add(colouring)
            memo[root] = (stuck, descend, target)
        return memo[root]

    def landed(rot, root, colouring):
        stuck, descend, target = orbits(rot, root)
        if colouring in target:
            return "target"
        if colouring in descend:
            return "descends"
        if colouring in stuck:
            return "stuck"
        return "missing"

    escapes = 0
    trapped = []
    twins = []
    for order, index, ascii_line, failing in failing_graphs:
        rot = parse_ascii(ascii_line)
        passing = set()
        for block in table["orders"]:
            if block["order"] != order:
                continue
            for graph in block["graphs_checked"]:
                if graph["graph_index"] == index:
                    passing = set(graph["passing_roots"])
        memo.clear()
        for root in sorted(failing):
            state = RootState(rot, root)
            for i, info in enumerate(state.info):
                if info["p"] != 1 or state.descent(i, 2) is None:
                    continue
                col, _boundary, singletons, _gap, _d5, locked = colour_view(rot, state, i)
                good = []
                twin = []
                for x in singletons:
                    new = dict(col)
                    new[root] = col[x]
                    if len(rot[x]) == 5:
                        order_x = [v for v in range(len(rot)) if v != x]
                        label = landed(rot, x, canon(tuple(new[v] for v in order_x)))
                        if label in ("descends", "target") and x in passing:
                            good.append({"kind": "direct", "to": x, "orbit": label})
                        elif label == "stuck":
                            twin.append(x)
                    counts = {}
                    for vertex in rot[x]:
                        counts[new[vertex]] = counts.get(new[vertex], 0) + 1
                    for y in rot[x]:
                        if y == root or len(rot[y]) != 5 or counts[new[y]] != 1:
                            continue
                        new2 = dict(new)
                        new2[x] = new[y]
                        order_y = [v for v in range(len(rot)) if v != y]
                        label = landed(rot, y, canon(tuple(new2[v] for v in order_y)))
                        if label in ("descends", "target") and y in passing:
                            good.append({"kind": "two-step", "via": x, "to": y, "orbit": label})
                if good:
                    escapes += 1
                else:
                    trapped.append({"order": order, "graph": index, "root": root, "locked": locked})
                if twin:
                    twins.append({"order": order, "graph": index, "root": root, "stuck_twins": twin,
                                  "also_escapes": bool(good)})
    return {"stuck_states_with_an_escape": escapes, "stuck_states_without_an_escape": trapped, "direct_slides_onto_a_stuck_twin": twins}


def headline(graphs):
    stuck_open = 0
    stuck_k1 = 0
    stuck_k2 = 0
    stuck_n = 0
    good_stuck = 0
    for graph in graphs:
        for root in graph["roots"]:
            stuck_n += root["two_swap_stuck"]
            stuck_open += root["stuck_and_open_slide"]
            stuck_k1 += root["stuck_and_kempe1_unlocks"]
            stuck_k2 += root["stuck_and_kempe2_unlocks"]
            if not root["mass_fails"]:
                good_stuck += root["two_swap_stuck"]
    return {
        "two_swap_stuck_states": stuck_n,
        "stuck_with_a_degree_five_slide": stuck_open,
        "stuck_unlocked_by_one_kempe_swap": stuck_k1,
        "stuck_unlocked_by_a_state_at_distance_two": stuck_k2,
        "two_swap_stuck_states_at_passing_roots": good_stuck,
    }


def main():
    table = json.loads((FIXTURES / "mass-macro-results.json").read_text())
    summary, failing_graphs = census(table)
    print("census types", len(summary), "failing graphs", len(failing_graphs), flush=True)
    graphs = probe(failing_graphs)
    report = {
        "scope": "Published mass-failing graphs only, plus the geometry of two symmetric triangulations. No colouring search on those triangulations.",
        "neighbour_types_in_the_mass_corpus": summary,
        "headline": headline(graphs),
        "escape": escape_audit(table, failing_graphs),
        "graphs": graphs,
        "symmetric_geometry": geometry_report(),
    }
    OUT.write_text(json.dumps(report, indent=1) + "\n")
    print(json.dumps({"headline": report["headline"], "geometry": report["symmetric_geometry"]}, indent=1))


if __name__ == "__main__":
    main()
