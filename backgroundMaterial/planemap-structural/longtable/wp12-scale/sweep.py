"""Sweep plantri min-degree-5 triangulations of one order (optionally a res/mod slice) with the C engine.

Usage: sweep.py ORDER [--roots all|isolated] [--res R --mod M] [--procs P]
plantri: compiled from the team's plantri 5.8 source (plantri -m5 -a ORDER [res/mod]); the plantri
path is given by $PLANTRI. Graph indices are zero-based in plantri output order within the slice.
Weights: the 8 unit vectors (q = e1, lin = e2, ...) plus the WP11 validation existential survivors
(read-only from ../wp11-validation/results.json). Root type = (#deg-5, #deg-6, #deg>=7 neighbours).
Writes sweep-<ORDER>[-<res>of<mod>]-<roots>.json here. Facts only.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from collections import Counter, defaultdict
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from engine import E, run_batch  # noqa: E402
from mass_core import degree_five, parse_ascii  # noqa: E402

PLANTRI = os.environ.get("PLANTRI", "plantri")


def weight_list():
    v = json.loads((HERE.parent / "wp11-validation" / "results.json").read_text())
    ws = [E[k] for k in E]
    for x in v["existential_survivors"]:
        if x["weights"] not in ws:
            ws.append(x["weights"])
    return ws, [x["weights"] for x in v["existential_survivors"]], [x["weights"] for x in v["all_roots_survivors"]]


def root_type(rot, r):
    d = [len(rot[w]) for w in rot[r]]
    return (d.count(5), d.count(6), sum(x >= 7 for x in d))


def work(args):
    items, weights = args
    jobs, meta = [], []
    for gi, line in items:
        rot = parse_ascii(line)
        for r in degree_five(rot):
            jobs.append((rot, r))
            meta.append((gi, r, root_type(rot, r)))
    res = run_batch(jobs, weights, threads=1) if jobs else []
    out = []
    for (gi, r, typ), x in zip(meta, res):
        out.append({"gi": gi, "r": r, "type": typ, "orbits": x["coloring_orbits"], "non_target": x["non_target"],
                    "hard": x["hard"], "sec": x["seconds_enumerate"] + x["seconds_check"],
                    "bad": [k for k, w in enumerate(x["results"]) if not w["good"]],
                    "stuck": {k: w["first_stuck"] for k, w in enumerate(x["results"]) if not w["good"]}})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("order", type=int)
    ap.add_argument("--roots", choices=["all", "isolated"], default="all")
    ap.add_argument("--res", type=int)
    ap.add_argument("--mod", type=int)
    ap.add_argument("--procs", type=int, default=12)
    a = ap.parse_args()
    cmd = [PLANTRI, "-m5", "-a", str(a.order)] + ([f"{a.res}/{a.mod}"] if a.mod else [])
    t0 = time.time()
    lines = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.splitlines()
    tgen = time.time() - t0
    weights, ex_surv, all_surv = weight_list()
    graphs = list(enumerate(lines))
    if a.roots == "isolated":
        keep = []
        for gi, line in graphs:
            rot = parse_ascii(line)
            if any(root_type(rot, r)[0] == 0 for r in degree_five(rot)):
                keep.append((gi, line))
        graphs = keep
    chunks = [graphs[i:i + 20] for i in range(0, len(graphs), 20)]
    t1 = time.time()
    with Pool(a.procs) as pool:
        rows = [row for part in pool.imap(work, [(c, weights) for c in chunks]) for row in part]
    tchk = time.time() - t1
    if a.roots == "isolated":
        rows = [x for x in rows if x["type"][0] == 0]
    by_graph = defaultdict(list)
    for x in rows:
        by_graph[x["gi"]].append(x)
    ascii_of = dict(graphs)
    per_weight = []
    for k, w in enumerate(weights):
        bad = [x for x in rows if k in x["bad"]]
        no_good = [gi for gi, rs in by_graph.items() if all(k in x["bad"] for x in rs)] if a.roots == "all" else None
        per_weight.append({"weights": w, "bad_roots": len(bad),
                           "bad_roots_by_type": {str(t): c for t, c in Counter(tuple(x["type"]) for x in bad).items()},
                           "graphs_with_no_good_root": no_good,
                           "bad_root_witnesses": [{"graph_index": x["gi"], "ascii": ascii_of[x["gi"]], "root": x["r"],
                                                   "type": x["type"], "first_stuck": x["stuck"][k]} for x in bad][:20]})
    types = Counter(tuple(x["type"]) for x in rows)
    out = {"scope": "WP12-scale sweep; facts only", "order": a.order, "plantri_cmd": " ".join(cmd[1:]),
           "plantri_output_sha256": hashlib.sha256(("\n".join(lines) + "\n").encode()).hexdigest(),
           "graphs_generated": len(lines), "graphs_checked": len(by_graph), "roots_mode": a.roots,
           "roots_checked": len(rows), "root_types": {str(t): c for t, c in sorted(types.items())},
           "isolated_roots_checked": sum(1 for x in rows if x["type"][0] == 0),
           "max_orbits": max((x["orbits"] for x in rows), default=0),
           "total_orbits": sum(x["orbits"] for x in rows), "total_non_target": sum(x["non_target"] for x in rows),
           "total_hard": sum(x["hard"] for x in rows),
           "roots_with_hard_states": sum(1 for x in rows if x["hard"]),
           "isolated_roots_with_hard_states": sum(1 for x in rows if x["hard"] and x["type"][0] == 0),
           "seconds_plantri": tgen, "seconds_check_wall": tchk, "procs": a.procs,
           "engine_seconds_sum": sum(x["sec"] for x in rows),
           "weights_count": len(weights), "wp11_validation_existential_survivors": len(ex_surv),
           "wp11_validation_all_roots_survivors": len(all_surv),
           "per_weight": per_weight}
    # survivor summaries
    def surv(ws, mode):
        idx = [weights.index(w) for w in ws]
        if mode == "exist" and a.roots == "all":
            return [weights[k] for k in idx if not per_weight[k]["graphs_with_no_good_root"]]
        return [weights[k] for k in idx if per_weight[k]["bad_roots"] == 0]
    out["validation_existential_survivors_still_existentially_good"] = surv(ex_surv, "exist") if a.roots == "all" else None
    out["validation_existential_survivors_with_no_bad_root_checked"] = surv(ex_surv, "allroots")
    out["validation_all_roots_survivors_with_no_bad_root_checked"] = surv(all_surv, "allroots")
    sl = f"-{a.res}of{a.mod}" if a.mod else ""
    path = HERE / f"sweep-{a.order}{sl}-{a.roots}.json"
    path.write_text(json.dumps(out, indent=1) + "\n")
    q, lin = per_weight[0], per_weight[1]
    print(f"order {a.order}{sl} {a.roots}: graphs {len(by_graph)} roots {len(rows)} isolated {out['isolated_roots_checked']} "
          f"hard {out['total_hard']} (roots with hard {out['roots_with_hard_states']}, isolated {out['isolated_roots_with_hard_states']}) "
          f"| q bad {q['bad_roots']} no-good-graphs {q['graphs_with_no_good_root']} | lin bad {lin['bad_roots']} "
          f"no-good-graphs {lin['graphs_with_no_good_root']} | ex-surv existential {len(out['validation_existential_survivors_still_existentially_good'] or [])}/{len(ex_surv)} "
          f"| all-roots surv clean {len(out['validation_all_roots_survivors_with_no_bad_root_checked'])}/{len(all_surv)} | {tchk:.1f}s")


if __name__ == "__main__":
    main()
