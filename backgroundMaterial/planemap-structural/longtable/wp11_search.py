"""WP11 rank-synthesis tier-1 search producer (declared; discovery and validation NOT to be run before release).

Reads the frozen run manifest `wp11-run-manifest.json`, verifies every bound hash, and evaluates
weight vectors on one stage:
  --stage discovery   orders 12-18, the whole registry; freezes the survivor lists
  --stage validation  orders 19-20, the frozen discovery existential survivors only, run once
  --stage smoke       the four named schema fixtures with weights e1 (q) and e3 (L), which
                      reproduce published results; tests the certificate path, not a discovery run

Evidence written per stage into `wp11-<stage>[-<label>]/`:
  tables/<order>-<graph>-r<root>.json.gz   (wp11-table-v1) one per (graph, root), weight-independent:
      the complete canonical state set with p and the eight features; for every non-target state
      either one macro to a target (p = 0) or, for a "hard" state, its COMPLETE list of 1- and
      2-move endpoints with endpoint features.  Shared by all certificates.
  certificates.json   (wp11-cert-v1-indexed) per weight vector, for EVERY graph and EVERY root:
      a good root carries, per hard state, the index of a decreasing endpoint in that table;
      a bad root carries the index of a stuck hard state.  Separate fields name the
      existential_fail_witness (every root of one graph is bad) and the all_roots_fail_witness
      (one bad root).  An existential pass is covered by any good root per graph; an all-roots
      pass by every root per graph.
  results.json   outcomes, survivors with every registry id and sub-tier, the certificate and
      table hashes, and for validation the frozen discovery digest and exact survivor list.
Moves use the wp11-cert-v1 named-colour serialisation (no renaming between moves).
Existing outputs are never overwritten; an authorised rerun needs --label and records what it follows.
Facts only; no status claims.
"""
import argparse
import gzip
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

from mass_core import FIXTURES, HERE, canon, degree_five, parse_ascii, rotation_from_fixture
from wp11_cert import FEATURES, as_list, endpoints, features, root_setup

MANIFEST = HERE / "wp11-run-manifest.json"
SMOKE_WEIGHTS = [[1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0]]
SMOKE_GRAPHS = [("icosahedron-fixture.json", 12, None), ("corpus", 17, 0), ("corpus", 17, 1), ("corpus", 17, 3)]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_manifest(m):
    for rel, digest in m["bound_files"].items():
        assert sha(HERE / rel) == digest, f"manifest hash mismatch: {rel}"


def macro(s, m1, c1, m2, c2):
    return {"move1": m1, "intermediate": as_list(s.V, c1) if c1 else None, "move2": m2,
            "endpoint": as_list(s.V, c2), "endpoint_canonical": list(canon(as_list(s.V, c2)))}


def build_table(graph, rot, r):
    """The weight-independent table at (T, r), and per hard state the matrix of endpoint feature diffs."""
    s, adj, B = root_setup(rot, r)
    states, hard, diffs = [], [], []
    for i, c in enumerate(s.C):
        col = dict(zip(s.V, c))
        p, f = features(adj, B, col)
        rec = {"coloring": list(c), "p": p, "features": f}
        if p == 1:
            eps = endpoints(adj, col)
            evals = [features(adj, B, c2) for *_, c2 in eps]
            t = next((k for k, (p2, _) in enumerate(evals) if p2 == 0), None)
            if t is not None:
                rec["target_macro"] = macro(s, *eps[t])
            else:
                rec["endpoints"] = [dict(macro(s, *e), endpoint_p=p2, endpoint_features=f2)
                                    for e, (p2, f2) in zip(eps, evals)]
                hard.append(i)
                diffs.append(np.array([[f2[k] - f[k] for k in FEATURES] for _, f2 in evals], dtype=np.int64))
        states.append(rec)
    table = {"schema": "wp11-table-v1", "graph": graph, "root": r, "degree_five_roots": degree_five(rot),
             "vertex_order": s.V, "boundary_cyclic_order": B, "features": FEATURES,
             "state_count": len(states), "hard_states": hard, "states": states,
             "note": "complete canonical state set; complete endpoint lists at hard states; weight-independent"}
    return table, diffs


def write_gz(path, obj):
    data = json.dumps(obj, separators=(",", ":")).encode()
    path.write_bytes(gzip.compress(data, mtime=0))
    return sha(path)


def stage_graphs(args, m):
    if args.stage == "smoke":
        table = json.loads((FIXTURES / "mass-macro-results.json").read_text())
        out = []
        for source, order, gi in SMOKE_GRAPHS:
            if gi is None:
                out.append({"source": source, "order": order, "graph_index": None, "ascii": None,
                            "rotation": rotation_from_fixture(FIXTURES / source)})
            else:
                line = next(g for o in table["orders"] if o["order"] == order
                            for g in o["graphs_checked"] if g["graph_index"] == gi)["ascii"]
                out.append({"source": source, "order": order, "graph_index": gi, "ascii": line})
        return out
    return m["discovery_graphs"] if args.stage == "discovery" else m["validation_graphs"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["discovery", "validation", "smoke"], required=True)
    ap.add_argument("--label", help="authorised rerun or correction; written beside, never over, earlier output")
    args = ap.parse_args()
    m = json.loads(MANIFEST.read_text())
    verify_manifest(m)
    name = f"wp11-{args.stage}" + (f"-{args.label}" if args.label else "")
    outdir = HERE / name
    if outdir.exists():
        sys.exit(f"refusing to overwrite {outdir.name}; an authorised rerun needs a new --label")
    earlier = sorted(p.name for p in HERE.glob(f"wp11-{args.stage}*") if p.is_dir())
    members = {}
    for e in m["weight_registry"]:
        members.setdefault(tuple(e["weights"]), []).append({"id": e["id"], "subtier": e["subtier"]})

    frozen = None
    if args.stage == "validation":
        fpath = HERE / "wp11-discovery" / "results.json"
        disc = json.loads(fpath.read_text())
        assert disc["stage"] == "discovery" and disc["manifest_sha256"] == sha(MANIFEST)
        frozen = {"path": "wp11-discovery/results.json", "sha256": sha(fpath),
                  "existential_survivors": disc["existential_survivors"],
                  "all_roots_survivors": disc["all_roots_survivors"]}
        weights = [tuple(e["weights"]) for e in disc["existential_survivors"]]
    elif args.stage == "smoke":
        weights = [tuple(w) for w in SMOKE_WEIGHTS]
    else:
        weights = sorted(members)

    (outdir / "tables").mkdir(parents=True)
    tables, hard = {}, {}
    graphs = stage_graphs(args, m)
    for g in graphs:
        rot = g.get("rotation") or parse_ascii(g["ascii"])
        h = hashlib.sha256(g["ascii"].encode()).hexdigest() if g["ascii"] else None
        assert g.get("ascii_sha256", h) == h, "graph ASCII does not match its manifest hash"
        graph = {"source": g.get("source", "corpus"), "order": g["order"], "graph_index": g["graph_index"],
                 "ascii": g["ascii"], "ascii_sha256": h, "rotation": rot}
        roots = degree_five(rot)
        assert "degree_five_roots" not in g or g["degree_five_roots"] == roots
        key = (g["order"], g["graph_index"])
        hard[key] = {}
        for r in roots:
            table, diffs = build_table(graph, rot, r)
            tid = f"{g['order']}-{g['graph_index'] if g['graph_index'] is not None else 'ico'}-r{r}"
            path = outdir / "tables" / f"{tid}.json.gz"
            tables[tid] = {"path": f"tables/{tid}.json.gz", "sha256": write_gz(path, table),
                           "order": g["order"], "graph_index": g["graph_index"], "root": r,
                           "state_count": table["state_count"], "hard_states": len(diffs)}
            hard[key][r] = (tid, table["hard_states"], diffs)
        print("tables", key, len(roots), "roots", file=sys.stderr, flush=True)

    certs, results = [], []
    for w in weights:
        wv = np.array(w, dtype=np.int64)
        per_graph, ex_fail, all_fail = [], None, None
        for key, roots in hard.items():
            good, bad = {}, {}
            for r, (tid, hs, diffs) in roots.items():
                idx = [int(np.argmax(D @ wv < 0)) if (D @ wv < 0).any() else None for D in diffs]
                if all(x is not None for x in idx):
                    good[str(r)] = {"table": tid, "decreasing_endpoint": idx}
                else:
                    bad[str(r)] = {"table": tid, "stuck_state": hs[idx.index(None)]}
            rec = {"order": key[0], "graph_index": key[1], "good_roots": good, "bad_roots": bad}
            per_graph.append(rec)
            if not good and ex_fail is None:
                ex_fail = {"order": key[0], "graph_index": key[1], "roots": bad}
            if bad and all_fail is None:
                r0 = min(bad, key=int)
                all_fail = {"order": key[0], "graph_index": key[1], "root": int(r0), **bad[r0]}
        mem = members.get(w, [])
        certs.append({"weights": list(w), "registry": mem, "per_graph": per_graph,
                      "existential_fail_witness": ex_fail, "all_roots_fail_witness": all_fail})
        results.append({"weights": list(w), "registry": mem,
                        "existential_pass": ex_fail is None, "all_roots_pass": all_fail is None,
                        "per_graph": [{"order": x["order"], "graph_index": x["graph_index"],
                                       "good_roots": sorted(int(r) for r in x["good_roots"]),
                                       "bad_roots": sorted(int(r) for r in x["bad_roots"])} for x in per_graph]})

    cpath = outdir / "certificates.json"
    cpath.write_text(json.dumps({
        "schema": "wp11-cert-v1-indexed", "stage": args.stage, "manifest_sha256": sha(MANIFEST),
        "features": FEATURES, "rank": "lexicographic (p, sum_i w_i f_i)", "macro_bound": 2,
        "colour_coordinates": "moves named in the colours of the colouring they act on; no renaming between moves",
        "witness_semantics": {
            "target_macro": "in the table; weight-independent; reaches p = 0",
            "decreasing_endpoint": "per hard state in table order, an index into that state's complete endpoint list "
                                   "whose endpoint rank is lower under w",
            "stuck_state": "a hard state index; no endpoint in its complete list is lower under w"},
        "tables": tables, "certificates": certs}, separators=(",", ":")) + "\n")
    out = {"stage": args.stage, "label": args.label, "earlier_outputs_for_stage": earlier,
           "manifest_sha256": sha(MANIFEST),
           "certificates": {"path": "certificates.json", "sha256": sha(cpath)},
           "tables_index_sha256": hashlib.sha256(json.dumps(tables, sort_keys=True).encode()).hexdigest(),
           "frozen_discovery": frozen, "weight_count": len(weights), "results": results,
           "existential_survivors": [{"weights": r["weights"], "registry": r["registry"]}
                                     for r in results if r["existential_pass"]],
           "all_roots_survivors": [{"weights": r["weights"], "registry": r["registry"]}
                                   for r in results if r["all_roots_pass"]],
           "scope": "WP11 tier-1 finite search under the declared grammar, domain and model only; no status claims."}
    if args.stage == "smoke":
        out["scope"] = "Smoke test of the certificate path on named fixtures reproducing published results; not a discovery run."
    (outdir / "results.json").write_text(json.dumps(out, indent=1) + "\n")
    (outdir / "SHA256SUMS").write_text("".join(f"{sha(p)}  {p.relative_to(outdir)}\n"
                                               for p in sorted(outdir.rglob("*")) if p.is_file()))
    print(f"{args.stage}: {len(weights)} weight vectors; {len(tables)} tables; existential survivors "
          f"{len(out['existential_survivors'])}; all-roots survivors {len(out['all_roots_survivors'])}")


if __name__ == "__main__":
    main()
