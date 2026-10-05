"""WP11 pre-release regression: raw versus complementary toggle at order 17, graph 3, root 13.

For each of the five trap/twin pits at root 13, take the trap (strictly two-swap stuck under the
mass rank), and swap (a) the two-vertex chain at the opposite hub 3 and (b) the complementary
component of the same colour pair, both in the trap's named colours.  Assert: both swaps are
legal whole active components; their raw endpoints differ by a global colour renaming; both
canonicalise to the twin; all eight WP11 features and the (p, q) rank agree on both endpoints.
Writes wp11-schema-examples/regression-17-3-root13-toggles.json.  Not a WP11 search output.
"""
import hashlib
import json

from mass_core import FIXTURES, HERE, canon, parse_ascii
from wp11_cert import FEATURES, components, features, rank, root_setup, swap

OUT = HERE / "wp11-schema-examples" / "regression-17-3-root13-toggles.json"
E1 = [1, 0, 0, 0, 0, 0, 0, 0]


def main():
    table = json.loads((FIXTURES / "mass-macro-results.json").read_text())
    line = next(g for o in table["orders"] if o["order"] == 17
                for g in o["graphs_checked"] if g["graph_index"] == 3)["ascii"]
    rot = parse_ascii(line)
    r, hub = 13, 3
    s, adj, B = root_setup(rot, r)
    assert hub not in B and hub != r
    rows = []
    for i, c in enumerate(s.C):
        if not (s.info[i]["p"] == 1 and s.descent(i, 2) is not None):
            continue
        col = dict(zip(s.V, c))
        comps = components(adj, col)
        two = [(pr, K) for pr, K in comps if len(K) == 2 and hub in K]
        assert len(two) == 1, "Lemma S: at most one two-vertex component at the hub"
        pr, K2 = two[0]
        others = [K for p2, K in comps if p2 == pr and K != K2]
        assert len(others) == 1, "the toggle pair has exactly two components"
        K6 = others[0]
        e2, e6 = swap(col, pr, K2), swap(col, pr, K6)
        raw2 = [e2[v] for v in s.V]
        raw6 = [e6[v] for v in s.V]
        perm = {x: y for x, y in zip(raw2, raw6)}
        assert all(perm[x] == y for x, y in zip(raw2, raw6)), "raw endpoints differ by a renaming"
        assert canon(raw2) == canon(raw6)
        twin = s.index[tuple(canon(raw2))]
        assert s.info[twin]["p"] == 1 and s.descent(twin, 2) is None
        f2, f6 = features(adj, B, e2), features(adj, B, e6)
        assert f2 == f6
        rows.append({"trap_state": i, "trap_coloring": list(c), "pair": list(pr),
                     "two_vertex_component": sorted(K2), "complementary_component": sorted(K6),
                     "raw_endpoint_two_vertex_swap": raw2, "raw_endpoint_complementary_swap": raw6,
                     "raw_vertices_changed": [len(K2), len(K6)],
                     "global_renaming_between_raw_endpoints": {str(k): v for k, v in perm.items()},
                     "canonical_endpoint": list(canon(raw2)), "twin_state": twin,
                     "endpoint_features": f2[1], "endpoint_rank_pq": list(rank(f2, E1)),
                     "trap_rank_pq": list(rank(features(adj, B, col), E1))})
    assert len(rows) == 5
    out = {"schema": "wp11-regression-v1", "graph": {"order": 17, "graph_index": 3, "ascii": line,
           "ascii_sha256": hashlib.sha256(line.encode()).hexdigest()}, "root": r, "opposite_hub": hub,
           "vertex_order": s.V, "boundary_cyclic_order": B, "features": FEATURES, "pits": rows,
           "producer": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in (HERE / "wp11_regression_root13.py", HERE / "wp11_cert.py", HERE / "mass_core.py")},
           "note": "Pre-release regression; reproduces the published WP7d toggles. Not a WP11 search output."}
    OUT.write_text(json.dumps(out, indent=1) + "\n")
    print(f"5 pits checked at root 13; raw changes {[x['raw_vertices_changed'] for x in rows]}")


if __name__ == "__main__":
    main()
