"""Independent Python check of engine BAD results, using only mass_core / wp11_cert functions.

For a (graph ascii or rotation, root, weight, colouring): checks the colouring is a proper colouring of
T - r in the canonical form over vertex order V, that p = 1, recomputes the COMPLETE 1- and 2-move
endpoint list with wp11_cert.endpoints and confirms no endpoint rank (wp11_cert.rank) is strictly lower.
Mode 'sweep FILE': checks every bad_root_witness in a sweep JSON, and for every weight with a graph
that has no good root, re-runs the engine on every root of that graph and checks every stuck witness.
Writes verify-<input stem>.json.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from engine import run_engine  # noqa: E402
from mass_core import canon, degree_five, parse_ascii  # noqa: E402
from wp11_cert import endpoints, features, rank  # noqa: E402


def check_stuck(rot, r, w, coloring):
    V = [v for v in range(len(rot)) if v != r]
    adj = {v: [x for x in rot[v] if x != r] for v in V}
    B = list(rot[r])
    col = dict(zip(V, coloring))
    assert len(coloring) == len(V) and tuple(coloring) == canon(coloring)
    assert all(col[v] != col[x] for v in V for x in adj[v]), "not proper"
    f0 = features(adj, B, col)
    assert f0[0] == 1, "not a non-target state"
    r0 = rank(f0, w)
    eps = endpoints(adj, col)
    lower = [e for e in eps if rank(features(adj, B, e[3]), w) < r0]
    return {"start_rank": list(r0), "endpoints_checked": len(eps), "lower_endpoints": len(lower),
            "stuck": not lower}


def main():
    path = Path(sys.argv[2])
    sw = json.loads(path.read_text())
    out = {"input": path.name, "checks": [], "existential": []}
    ok = True
    for pw in sw["per_weight"]:
        w = pw["weights"]
        for wit in pw["bad_root_witnesses"]:
            rot = parse_ascii(wit["ascii"])
            c = check_stuck(rot, wit["root"], w, wit["first_stuck"]["coloring"])
            ok &= c["stuck"]
            out["checks"].append({"weights": w, "graph_index": wit["graph_index"], "root": wit["root"], **c})
        for gi in pw["graphs_with_no_good_root"] or []:
            line = next(x["ascii"] for x in pw["bad_root_witnesses"] if x["graph_index"] == gi) \
                if any(x["graph_index"] == gi for x in pw["bad_root_witnesses"]) else None
            assert line is not None, "graph ascii not among listed witnesses; extend witness cap"
            rot = parse_ascii(line)
            roots = []
            for r in degree_five(rot):
                res = run_engine(rot, r, [w])["results"][0]
                assert not res["good"]
                c = check_stuck(rot, r, w, res["first_stuck"]["coloring"])
                ok &= c["stuck"]
                roots.append({"root": r, "coloring": res["first_stuck"]["coloring"], **c})
            out["existential"].append({"weights": w, "graph_index": gi, "ascii": line, "roots": roots,
                                       "every_root_stuck_witness_verified": all(x["stuck"] for x in roots)})
    out["all_verified"] = ok
    (HERE / f"verify-{path.stem}.json").write_text(json.dumps(out, indent=1) + "\n")
    print(path.name, "checks", len(out["checks"]), "existential graphs", len(out["existential"]), "all verified:", ok)


if __name__ == "__main__":
    main()
