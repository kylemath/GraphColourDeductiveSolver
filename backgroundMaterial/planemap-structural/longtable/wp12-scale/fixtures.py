"""Build and check the WP12 fixtures F32 (pentakis dodecahedron = class-(1,1) geodesic icosahedron)
and F42 (class-(2,0) geodesic icosahedron) as rotation systems, combinatorially from the icosahedron
fixture.  Checks: mass_core.validate_triangulation, degree sequence, isolation of every degree-five
vertex (all five neighbours of degree six), and one automorphism orbit on the degree-five vertices
(automorphisms.automorphisms).  Writes fixtures.json.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from automorphisms import automorphisms, orbits  # noqa: E402
from mass_core import FIXTURES, degree_five, rotation_from_fixture, validate_triangulation  # noqa: E402


def faces_of(rot):
    """Oriented faces by mass_core's tracing convention: dart (a,b) -> (b, succ_b(a))."""
    seen, out = set(), []
    for a, ns in enumerate(rot):
        for b in ns:
            if (a, b) in seen:
                continue
            f, d = [], (a, b)
            while d not in seen:
                seen.add(d)
                f.append(d[0])
                x, y = d
                d = (y, rot[y][(rot[y].index(x) + 1) % len(rot[y])])
            out.append(tuple(f))
    return out


def rotation_from_faces(n, faces):
    """Inverse of faces_of: in face (x,y,z), z follows x in the rotation at y (cyclically)."""
    succ = [dict() for _ in range(n)]
    for f in faces:
        assert len(f) == 3
        for i in range(3):
            x, y, z = f[i], f[(i + 1) % 3], f[(i + 2) % 3]
            assert x not in succ[y]
            succ[y][x] = z
    rot = []
    for v in range(n):
        start = min(succ[v])
        cyc, u = [start], succ[v][start]
        while u != start:
            cyc.append(u)
            u = succ[v][u]
        assert len(cyc) == len(succ[v])
        rot.append(cyc)
    return rot


def f42(ico):
    faces = faces_of(ico)
    n = len(ico)
    mid = {}
    for a, ns in enumerate(ico):
        for b in ns:
            if a < b:
                mid[(a, b)] = n
                n += 1
    m = lambda a, b: mid[(min(a, b), max(a, b))]  # noqa: E731
    new = []
    for a, b, c in faces:
        ab, bc, ca = m(a, b), m(b, c), m(c, a)
        new += [(a, ab, ca), (ab, b, bc), (ca, bc, c), (ab, bc, ca)]
    return rotation_from_faces(n, new)


def f32(ico):
    faces = faces_of(ico)
    n = len(ico)
    tri = []
    for a, b, c in faces:
        f = n
        n += 1
        tri += [(a, b, f), (b, c, f), (c, a, f)]
    # flip every original icosahedron edge (a,b): triangles (a,b,f1) and (b,a,f2) -> (a,f2,f1), (f2,b,f1)
    apex = {}
    for t in tri:
        apex[(t[0], t[1])] = t[2] if t[2] >= 12 else None
    new = []
    done = set()
    for t in tri:
        a, b, f1 = t
        if f1 < 12:
            continue
        # every triangle here is (x, y, centre) with x, y original; flip its original edge once
        if (b, a) in done:
            continue
        f2 = apex[(b, a)]
        new += [(a, f2, f1), (f2, b, f1)]
        done.add((a, b))
    return rotation_from_faces(n, new)


def check(name, rot):
    validate_triangulation(rot)
    deg = [len(ns) for ns in rot]
    D = degree_five(rot)
    isolated = all(all(deg[w] == 6 for w in rot[v]) for v in D)
    auts = automorphisms(rot)
    orbs = orbits(auts, D)
    info = {"name": name, "order": len(rot), "degree_sequence": {d: deg.count(d) for d in sorted(set(deg))},
            "degree_five_roots": D, "every_degree_five_root_has_five_degree_six_neighbours": isolated,
            "automorphism_group_order": len(auts), "degree_five_orbits": orbs,
            "rotation": rot, "rotation_sha256": hashlib.sha256(json.dumps(rot).encode()).hexdigest()}
    print(name, len(rot), info["degree_sequence"], "isolated:", isolated, "|Aut|:", len(auts), "orbits on D:", len(orbs))
    assert isolated and len(orbs) == 1 and len(D) == 12
    return info


def main():
    ico = rotation_from_fixture(FIXTURES / "icosahedron-fixture.json")
    out = {"source": "icosahedron-fixture.json",
           "construction": {"F32": "icosahedron; add a vertex in every face joined to its 3 corners; flip every original edge "
                                   "(= pentakis dodecahedron, class-(1,1) geodesic icosahedron)",
                            "F42": "icosahedron; split every face into 4 using edge midpoints (class-(2,0) geodesic icosahedron)"},
           "fixtures": {"F32": check("F32", f32(ico)), "F42": check("F42", f42(ico))}}
    (HERE / "fixtures.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
