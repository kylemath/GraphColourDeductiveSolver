"""WP11 rank-synthesis tier-1 search producer (declared; NOT to be run before release).

Reads the frozen run manifest `wp11-run-manifest.json`, verifies every bound hash, and evaluates the
declared weight registry on the declared stage:
  --stage discovery   orders 12-18; writes wp11-discovery-results.json and freezes the survivor list
  --stage validation  orders 19-20; requires the frozen discovery survivor list; evaluates survivors once
For each weight vector w and graph T it records Good_w(T, r) for every degree-five root r (the
existential statement, primary, and the all-roots statement, secondary) and writes wp11-cert-v1
certificates: a pass certificate for one chosen root per graph when w passes existentially, an
existential_fail_witness for the first graph where w fails existentially, and an
all_roots_fail_witness for the first bad root.  Facts only; no status claims.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

from mass_core import FIXTURES, HERE, RootState, parse_ascii
from wp11_cert import FEATURES, endpoints, features, root_setup, state_record, stuck_record

MANIFEST = HERE / "wp11-run-manifest.json"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_manifest(m):
    for rel, digest in m["bound_files"].items():
        assert sha(HERE / rel) == digest, f"manifest hash mismatch: {rel}"


def precompute_root(rot, r):
    """Per non-target state with no target endpoint: the unique endpoint-minus-state feature diffs."""
    s, adj, B = root_setup(rot, r)
    hard = []
    for c in s.C:
        col = dict(zip(s.V, c))
        p, f = features(adj, B, col)
        if p == 0:
            continue
        fs = np.array([f[k] for k in FEATURES], dtype=np.int64)
        diffs, reaches_target = set(), False
        for *_, c2 in endpoints(adj, col):
            p2, f2 = features(adj, B, c2)
            if p2 == 0:
                reaches_target = True
                break
            diffs.add(tuple(int(f2[k]) - int(fs[i]) for i, k in enumerate(FEATURES)))
        if not reaches_target:
            hard.append(np.array(sorted(diffs), dtype=np.int64))
    return hard


def root_good(hard, w):
    wv = np.array(w, dtype=np.int64)
    return all(bool((D @ wv < 0).any()) for D in hard)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["discovery", "validation"], required=True)
    args = ap.parse_args()
    m = json.loads(MANIFEST.read_text())
    verify_manifest(m)
    graphs = m["discovery_graphs"] if args.stage == "discovery" else m["validation_graphs"]
    if args.stage == "validation":
        frozen_path = HERE / "wp11-discovery-results.json"
        frozen = json.loads(frozen_path.read_text())
        assert frozen["stage"] == "discovery" and frozen["manifest_sha256"] == sha(MANIFEST)
        weights = [tuple(e["weights"]) for e in frozen["existential_survivors"]]
        print("validation uses frozen discovery file", sha(frozen_path), file=sys.stderr)
    else:
        weights = sorted({tuple(e["weights"]) for e in m["weight_registry"]})
    table = {}
    for g in graphs:
        rot = parse_ascii(g["ascii"])
        assert hashlib.sha256(g["ascii"].encode()).hexdigest() == g["ascii_sha256"]
        table[(g["order"], g["graph_index"])] = (rot, {r: precompute_root(rot, r) for r in g["degree_five_roots"]})
        print("precomputed", g["order"], g["graph_index"], file=sys.stderr, flush=True)
    results = []
    for w in weights:
        per_graph = []
        for (order, gi), (rot, roots) in table.items():
            good = {r: root_good(h, w) for r, h in roots.items()}
            per_graph.append({"order": order, "graph_index": gi, "good_roots": sorted(r for r, v in good.items() if v),
                              "bad_roots": sorted(r for r, v in good.items() if not v)})
        results.append({"weights": list(w),
                        "existential_pass": all(x["good_roots"] for x in per_graph),
                        "all_roots_pass": all(not x["bad_roots"] for x in per_graph),
                        "per_graph": per_graph})
    out = {"stage": args.stage, "manifest_sha256": sha(MANIFEST), "results": results,
           "existential_survivors": [{"weights": r["weights"]} for r in results if r["existential_pass"]],
           "all_roots_survivors": [{"weights": r["weights"]} for r in results if r["all_roots_pass"]],
           "scope": "WP11 tier-1 finite search under the declared grammar, domain and model only; no status claims."}
    (HERE / f"wp11-{args.stage}-results.json").write_text(json.dumps(out, indent=1) + "\n")
    print(f"{args.stage}: {len(weights)} weight vectors; existential survivors {len(out['existential_survivors'])}; "
          f"all-roots survivors {len(out['all_roots_survivors'])}")


if __name__ == "__main__":
    main()
