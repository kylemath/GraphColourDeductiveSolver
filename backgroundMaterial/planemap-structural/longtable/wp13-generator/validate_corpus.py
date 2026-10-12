"""Re-validate corpus.json independently of the generator's own checks.

For every graph: longtable/mass_core.validate_triangulation (simple, e = 3n-6, all faces
triangles under the corpus face convention, Euler, min degree >= 5); recompute degree counts,
degree-five roots and root types with mass_core.degree_five; ASCII round-trip for n <= 26;
pairwise non-isomorphism via trimap.canonical_code.  Writes validation.json.
"""
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import mass_core  # noqa: E402
from trimap import canonical_code  # noqa: E402

doc = json.loads((HERE / "corpus.json").read_text())
fails, codes = [], {}
for g in doc["graphs"]:
    rot = g["rotation"]
    try:
        mass_core.validate_triangulation(rot)
        assert len(rot) == g["order"]
        assert min(len(x) for x in rot) >= 5
        degs = Counter(len(x) for x in rot)
        assert {str(k): v for k, v in sorted(degs.items())} == g["degree_counts"]
        roots = mass_core.degree_five(rot)
        assert roots == g["degree_five_roots"]
        for rt in g["root_types"]:
            nd = [len(rot[w]) for w in rot[rt["root"]]]
            assert (rt["n5"], rt["n6"], rt["n7plus"]) == (nd.count(5), nd.count(6), sum(d >= 7 for d in nd))
        assert g["isolated_roots"] == [r for r in roots if all(len(rot[w]) >= 6 for w in rot[r])]
        if g["order"] <= 26:
            assert mass_core.parse_ascii(g["ascii"]) == rot
        else:
            assert g["ascii"] is None
        key = canonical_code(rot)
        assert key not in codes, ("isomorphic to", codes.get(key))
        codes[key] = g["id"]
    except AssertionError as e:
        fails.append({"id": g["id"], "error": repr(e)})

res = {"graphs_checked": len(doc["graphs"]), "failures": fails,
       "pairwise_non_isomorphic": len(codes) == len(doc["graphs"]),
       "checker": "mass_core.validate_triangulation + recomputed invariants + canonical BFS codes"}
(HERE / "validation.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
