"""Long Table's own consistency check of a wp11_search.py output directory (not the independent replay).

  python3 wp11_check_output.py wp11-smoke

Checks every hash; that each table's state set equals the enumerated deletion colourings and its
root set the degree-five vertices; every target macro and every cited decreasing endpoint by
re-applying the moves (each a whole active component of the colouring it acts on) and recomputing
features and rank; and every stuck state by recomputing its complete endpoint list, comparing it
with the table, and confirming no endpoint is lower.  Shares code with the producer, so it checks
consistency only; the math team's replayer is the independent check.
"""
import gzip
import hashlib
import json
import sys
from pathlib import Path

from mass_core import HERE, canon, degree_five, deletion_colourings
from wp11_cert import components, endpoints, features, rank, swap


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def apply(adj, B, V, start, mac):
    col = dict(zip(V, start))
    for mv, before in ((mac["move1"], None), (mac["move2"], mac["intermediate"])):
        if mv is None:
            continue
        if before is not None:
            assert [col[v] for v in V] == before, "intermediate mismatch"
        K, pr = frozenset(mv["component"]), tuple(mv["pair"])
        assert (pr, K) in components(adj, col), "move is not a whole active component"
        col = swap(col, pr, K)
    assert [col[v] for v in V] == mac["endpoint"] and list(canon(mac["endpoint"])) == mac["endpoint_canonical"]
    return col


def main(d):
    d = HERE / d
    for line in (d / "SHA256SUMS").read_text().splitlines():
        h, rel = line.split("  ")
        assert sha(d / rel) == h, rel
    res = json.loads((d / "results.json").read_text())
    assert sha(d / "certificates.json") == res["certificates"]["sha256"]
    cert = json.loads((d / "certificates.json").read_text())
    loaded = {}
    for tid, meta in cert["tables"].items():
        assert sha(d / meta["path"]) == meta["sha256"]
        t = json.loads(gzip.decompress((d / meta["path"]).read_bytes()))
        rot, r = t["graph"]["rotation"], t["root"]
        assert t["degree_five_roots"] == degree_five(rot)
        V, C = deletion_colourings(rot, r)
        assert t["vertex_order"] == V and [tuple(s["coloring"]) for s in t["states"]] == C
        adj = {v: [w for w in rot[v] if w != r] for v in V}
        B = t["boundary_cyclic_order"]
        assert B == list(rot[r])
        for i, s in enumerate(t["states"]):
            col = dict(zip(V, s["coloring"]))
            p, f = features(adj, B, col)
            assert (p, f) == (s["p"], s["features"])
            if "target_macro" in s:
                assert features(adj, B, apply(adj, B, V, s["coloring"], s["target_macro"]))[0] == 0
            elif p == 1:
                assert i in t["hard_states"]
                full = [[m1, as_raw(V, c1), m2, as_raw(V, c2)] for m1, c1, m2, c2 in endpoints(adj, col)]
                got = [[e["move1"], e["intermediate"], e["move2"], e["endpoint"]] for e in s["endpoints"]]
                assert full == got, "endpoint list not complete"
                assert all(features(adj, B, apply(adj, B, V, s["coloring"], e)) == (e["endpoint_p"], e["endpoint_features"])
                           for e in s["endpoints"])
        loaded[tid] = (t, adj, B, V)
    n_dec = n_stuck = 0
    for c in cert["certificates"]:
        w = c["weights"]
        ex = next((g for g in c["per_graph"] if not g["good_roots"]), None)
        al = next((g for g in c["per_graph"] if g["bad_roots"]), None)
        assert (ex is None) == (c["existential_fail_witness"] is None)
        assert (al is None) == (c["all_roots_fail_witness"] is None)
        if ex:
            assert c["existential_fail_witness"]["roots"] == ex["bad_roots"]
        if al:
            assert c["all_roots_fail_witness"]["stuck_state"] == al["bad_roots"][str(c["all_roots_fail_witness"]["root"])]["stuck_state"]
        for g in c["per_graph"]:
            for rs, x in g["good_roots"].items():
                t, adj, B, V = loaded[x["table"]]
                assert t["root"] == int(rs) and len(x["decreasing_endpoint"]) == len(t["hard_states"])
                for i, k in zip(t["hard_states"], x["decreasing_endpoint"]):
                    s, e = t["states"][i], t["states"][i]["endpoints"][k]
                    assert rank((e["endpoint_p"], e["endpoint_features"]), w) < rank((s["p"], s["features"]), w)
                    n_dec += 1
            for rs, x in g["bad_roots"].items():
                t, adj, B, V = loaded[x["table"]]
                s = t["states"][x["stuck_state"]]
                r0 = rank((s["p"], s["features"]), w)
                assert all(rank((e["endpoint_p"], e["endpoint_features"]), w) >= r0 for e in s["endpoints"])
                n_stuck += 1
            roots = {int(k) for k in g["good_roots"]} | {int(k) for k in g["bad_roots"]}
            some = next(t for t, *_ in loaded.values()
                        if (t["graph"]["order"], t["graph"]["graph_index"]) == (g["order"], g["graph_index"]))
            assert roots == set(some["degree_five_roots"]), "a root is missing from the certificate"
    print(f"{d.name}: {len(loaded)} tables, {len(cert['certificates'])} weight vectors, "
          f"{n_dec} decreasing witnesses and {n_stuck} stuck witnesses checked")


def as_raw(V, col):
    return [col[v] for v in V] if col else None


if __name__ == "__main__":
    main(sys.argv[1])
