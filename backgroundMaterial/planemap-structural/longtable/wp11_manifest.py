"""Build the frozen WP11 run manifest (wp11-run-manifest.json). Building it runs no search."""
import hashlib
import itertools
import json
from math import gcd
from functools import reduce
from pathlib import Path

from mass_core import FIXTURES, HERE, degree_five, parse_ascii

FEATURES = ["q", "lin", "L", "Lall", "links", "shortLinks", "repMass", "hubToggles"]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def registry():
    out = []
    for i in range(8):
        w = [0] * 8; w[i] = 1
        out.append(("1a", w))
    for i, j in itertools.combinations(range(8), 2):
        for a in (1, 2, 3):
            for b in (1, 2, 3):
                w = [0] * 8; w[i] = a; w[j] = b
                out.append(("1b", w))
    for bits in itertools.product((0, 1), repeat=8):
        if any(bits):
            out.append(("1c", list(bits)))
    assert len(out) == 8 + 252 + 255
    rows = []
    for k, (tier, w) in enumerate(out):
        g = reduce(gcd, [x for x in w if x])
        rows.append({"id": k, "subtier": tier, "weights": w, "proportional_class": [x // g for x in w]})
    return rows


def graphs(table, lo, hi):
    out = []
    for o in table["orders"]:
        if lo <= o["order"] <= hi:
            for g in o["graphs_checked"]:
                rot = parse_ascii(g["ascii"])
                out.append({"order": o["order"], "graph_index": g["graph_index"], "ascii": g["ascii"],
                            "ascii_sha256": hashlib.sha256(g["ascii"].encode()).hexdigest(),
                            "degree_five_roots": degree_five(rot)})
    return out


def main():
    table = json.loads((FIXTURES / "mass-macro-results.json").read_text())
    reg = registry()
    bound = ["WP11-rank-synthesis-tier1-declaration.md", "mass_core.py", "wp11_cert.py", "wp11_search.py",
             "wp11_regression_root13.py", "wp11_manifest.py", "wp11_check_output.py",
             "../wp11-independent-replay.py", "../wp11-independent-replay-regressions.py",
             "../wp11-pre-release-check.py",
             "../mass-macro-results.json", "../search-results.json"]
    bound += [f"../triangulations-min5-{n}.txt" for n in range(12, 21)]
    manifest = {
        "schema": "wp11-run-manifest-v1",
        "declaration": "WP11-rank-synthesis-tier1-declaration.md (version 2, inline overrides; version 2.1 certificate storage)",
        "features": FEATURES,
        "rank": "lexicographic (p, sum_i w_i f_i); macro <= 2 whole active component swaps; endpoint must decrease",
        "quantifiers": {"primary": "for all T exists r in D(T) for all non-target c exists decreasing macro",
                        "secondary": "for all T for all r in D(T) ...",
                        "root_choice": "recorded as a witness only; not a selector"},
        "weight_registry": reg,
        "distinct_weight_vectors": len({tuple(r["weights"]) for r in reg}),
        "distinct_proportional_classes": len({tuple(r["proportional_class"]) for r in reg}),
        "discovery_graphs": graphs(table, 12, 18),
        "validation_graphs": graphs(table, 19, 20),
        "validation_disclosure": "orders 19-20 were inspected in earlier research; a fixed out-of-discovery pass, run once, no re-tuning",
        "bound_files": {rel: sha(HERE / rel) for rel in bound},
        "status": "frozen before any run; release requires the math team's replay check and the user's explicit approval",
    }
    (HERE / "wp11-run-manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    print("registry", len(reg), "distinct", manifest["distinct_weight_vectors"],
          "proportional classes", manifest["distinct_proportional_classes"],
          "discovery graphs", len(manifest["discovery_graphs"]), "validation graphs", len(manifest["validation_graphs"]))


if __name__ == "__main__":
    main()
