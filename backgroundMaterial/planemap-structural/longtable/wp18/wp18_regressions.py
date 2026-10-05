"""WP18 regressions, run before any phase. Exit non-zero on failure."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "swarm"))
from wp18_core import HOLE, canon, graph_report, legal_fans, shortest_fill  # noqa: E402
import wp18_check  # noqa: E402
from icosahedron_fan import rotation_from_triangles, validate_sphere  # noqa: E402

m = json.loads((HERE.parent / "wp11-run-manifest.json").read_text())
ico = next(g for g in m["discovery_graphs"] if g["order"] == 12)
from wp18_core import parse_ascii  # noqa: E402

# 1. Icosahedron: 8 starts per fan, L = 1 at every (v, τ), 60 pairs.
rep = graph_report(parse_ascii(ico["ascii"]))
assert rep["pairs"] == 60, rep["pairs"]
assert all(r["starts"] == 8 and r["L"] == 1 for r in rep["rows"]), "icosahedron"
assert rep["m"] == 1
print("icosahedron: 60 pairs, 8 starts each, L = 1 everywhere")

# 2. Order 14 dipyramid, fan-link.md start, ell = 2.
names = ["N", "S"] + [f"U{i}" for i in range(6)] + [f"L{i}" for i in range(6)]
ix = {x: i for i, x in enumerate(names)}
tri = []
for i in range(6):
    j = (i + 1) % 6
    tri += [("N", f"U{i}", f"U{j}"), ("S", f"L{j}", f"L{i}"), (f"U{i}", f"L{i}", f"L{j}"), (f"U{i}", f"L{j}", f"U{j}")]
tri = [tuple(ix[x] for x in t) for t in tri]
try:
    rm = rotation_from_triangles(tri, list(range(14)))
except RuntimeError:
    rm = rotation_from_triangles([(c, b, a) for a, b, c in tri], list(range(14)))
rot = [rm[v] for v in range(14)]
validate_sphere(rot, 5)
col = {"N": 1, "S": 0, "U1": 0, "U2": 3, "U3": 0, "U4": 2, "U5": 0, "L0": 2, "L1": 3, "L2": 1, "L3": 2, "L4": 3, "L5": 1}
st = canon(tuple(col.get(x, HOLE) for x in names))
ell, path = shortest_fill(rot, st)
assert ell == 2, ell
fan = [f for f in legal_fans(rot, ix["U0"]) if {tuple(sorted(f[1])), tuple(sorted(f[2]))} == {tuple(sorted((ix["N"], ix["L0"]))), tuple(sorted((ix["N"], ix["L1"])))}]
assert len(fan) == 1, "fan {N L0, N L1} not legal"
row = {"v": ix["U0"], "chords": [list(fan[0][1]), list(fan[0][2])], "L": 2,
       "witness": {"start": list(st), "moves": [list(x) for x in path]}}
assert wp18_check.check_row(rot, row, 6) == ("exact", 2)
print("order 14 dipyramid start: ell = 2, witness replays")

# 3. Malformed witnesses must be rejected.
bad = 0
r1 = json.loads(json.dumps(row)); r1["witness"]["start"][ix["L0"]] = r1["witness"]["start"][ix["U5"]]  # improper / chord
r2 = json.loads(json.dumps(row)); r2["witness"]["moves"][0] = ["S", ix["S"]]                        # illegal slide
r3 = json.loads(json.dumps(row)); r3["witness"]["moves"] = r3["witness"]["moves"][:1]; r3["L"] = 1   # one move does not fill
for r in (r1, r2, r3):
    try:
        wp18_check.check_row(rot, r, 6)
    except ValueError:
        bad += 1
assert bad == 3, bad
print("malformed witnesses rejected: 3 of 3")

# 4. Amended checker (5 October): coverage, fan identity, and exact-depth exclusion on P-files
#    are exercised in wp18_check.main; here, a start with ell = 2 must fail a claim of L = 3.
r4 = json.loads(json.dumps(row)); r4["L"] = 3; r4["witness"]["moves"] = r4["witness"]["moves"] + [["S", ix["S"]]]
try:
    wp18_check.check_row(rot, r4, 6)
    raise AssertionError("over-claimed L accepted")
except ValueError:
    pass
print("over-claimed L = 3 on an ell = 2 start rejected")
