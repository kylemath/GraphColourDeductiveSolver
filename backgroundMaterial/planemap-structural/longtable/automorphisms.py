"""Long Table diagnostic: map automorphisms and whether mass-macro good-root sets are unions of orbits.

For a 3-connected planar triangulation every graph automorphism is a map automorphism, possibly
orientation-reversing (Whitney).  An automorphism is fixed by the image of one dart and an
orientation, so it is found by extending from dart (0, rot[0][0]) to each dart and sign.
Uses rotations only; no colouring is enumerated.  Optional diagnostic, not a prerequisite.
"""
import hashlib
import json
from pathlib import Path

from mass_core import FIXTURES, HERE, degree_five, parse_ascii


def extend(rot, v0, w0, v1, w1, sign):
    """Try the map automorphism sending dart (v0,w0) to (v1,w1); sign -1 reverses rotations."""
    n = len(rot)
    phi = {v0: v1}
    stack = [(v0, w0, v1, w1)]
    while stack:
        a, b, x, y = stack.pop()
        if len(rot[a]) != len(rot[x]):
            return None
        i, j, d = rot[a].index(b), rot[x].index(y), len(rot[a])
        for k in range(d):
            u = rot[a][(i + k) % d]
            z = rot[x][(j + sign * k) % d]
            if u in phi:
                if phi[u] != z:
                    return None
            else:
                if z in phi.values():
                    return None
                phi[u] = z
                stack.append((u, a, z, x))
    return phi if len(phi) == n else None


def automorphisms(rot):
    v0, w0 = 0, rot[0][0]
    out = []
    for v1 in range(len(rot)):
        if len(rot[v1]) != len(rot[v0]):
            continue
        for w1 in rot[v1]:
            for sign in (1, -1):
                phi = extend(rot, v0, w0, v1, w1, sign)
                if phi is not None and all(sorted(phi[u] for u in rot[v]) == sorted(rot[phi[v]]) for v in phi):
                    out.append(phi)
    return out


def orbits(auts, verts):
    seen, out = set(), []
    for v in sorted(verts):
        if v in seen:
            continue
        orb = sorted({phi[v] for phi in auts})
        seen |= set(orb)
        out.append(orb)
    return out


def main():
    path = FIXTURES / "mass-macro-results.json"
    table = json.loads(path.read_text())
    rows, all_union = [], True
    for o in table["orders"]:
        for g in o["graphs_checked"]:
            rot = parse_ascii(g["ascii"])
            auts = automorphisms(rot)
            D = degree_five(rot)
            orbs = orbits(auts, D)
            failing = set(g["failing_roots"])
            union = all(set(orb) <= failing or not (set(orb) & failing) for orb in orbs)
            all_union &= union
            rows.append({"order": o["order"], "graph_index": g["graph_index"], "aut_order": len(auts),
                         "degree_five_orbits": orbs, "failing_roots": sorted(failing),
                         "failing_set_is_union_of_orbits": union})
            if failing:
                print(f"order {o['order']} graph {g['graph_index']}: |Aut|={len(auts)} "
                      f"orbits on D(T)={orbs} failing={sorted(failing)} union={union}")
    print("failing set is a union of Aut-orbits in every graph:", all_union)
    print("graphs with trivial automorphism group:", sum(r["aut_order"] == 1 for r in rows), "of", len(rows))
    out = {"scope": "Diagnostic: map automorphism groups from rotations and orbit-closure of the published "
                    "mass-macro failing-root sets. Not a proof; no status claims.",
           "inputs": {path.name: hashlib.sha256(path.read_bytes()).hexdigest()},
           "all_failing_sets_are_orbit_unions": all_union, "rows": rows}
    (HERE / "automorphisms.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
